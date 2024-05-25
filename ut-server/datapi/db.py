# -*- coding: utf-8 -*-
"""
数据库相关工具类
"""
import datetime
# import fcntl
import json
import os
import random
import shutil
import sqlite3
import time
from itertools import groupby

import numpy as np
import pandas as pd
import pymysql
import six

try:
    from pymysql.converters import escape_string
except:
    from pymysql import escape_string
from annoy import AnnoyIndex
from bidict import bidict
from clickhouse_driver import connect as ch_connect
from sklearn.metrics.pairwise import cosine_similarity
import redis
from dbutils.persistent_db import PersistentDB
from dbutils.pooled_db import PooledDB
from functools import partial
# influxdb
import tzlocal
import pytz
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS, WriteOptions

from . import file
from .text import sign

from .env import g_cache_root
from .batch import batch_generator
from aliyun.log import GetProjectLogsRequest, LogClient
from pymongo import MongoClient
from odps import ODPS
from datapi import tunnel
from utils.logger_helper import logger
from utils.time_util import timeit_no_res

# 连接池
# from pymysqlpool.pool import Pool


__author__ = 'jx'

RETRY_TIMES = 3
MAX_SQL_ID_COUNT = 3000

g_max_text_length = 65535
g_max_m_text_length = 16777215
g_max_l_text_length = 4294967295


def is_null(val):
    return val is None or str(val) == '' or str(val).strip().lower() in ('none', 'null', 'nan')


def auto_format(value):
    # noinspection PyUnresolvedReferences
    def _fm(val):
        if isinstance(val, (bool, np.integer)):
            return int(val)
        if isinstance(val, np.inexact):
            return float(val)
        if isinstance(val, (datetime.datetime, datetime.date)):
            return str(val)
        if is_null(val):
            return
        return val

    if isinstance(value, dict):
        for k, v in six.iteritems(value):
            value[k] = _fm(v)
        return value
    elif isinstance(value, (np.ndarray, pd.Series, list, set, tuple)):
        return [_fm(val) for val in value]
    else:
        return _fm(value)


class BaseDb(object):
    def __init__(self):
        self.conn = None

    @staticmethod
    def wrap(conn, **kwargs):
        raise NotImplementedError

    def __iter__(self):
        return self

    def __enter__(self):
        return self.open()

    def __del__(self):
        try:
            self.close()
        except:
            pass

    def close(self):
        raise NotImplementedError

    def disconnect(self):
        """兼容server的pooled db关闭方式"""
        raise NotImplementedError

    def open(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def _auto_decode(self, x):
        return x

    def _auto_encode(self, x):
        return x

    # noinspection PyUnresolvedReferences
    def query(self, sql, *args, **kwargs):
        """返回数据长度，用fetch获得具体数据"""
        cursor = self.conn.cursor()
        cursor.execute(sql, *args, **kwargs)
        for r in cursor.fetchall():
            yield {k: self._auto_decode(v) for k, v in six.iteritems(r)}
        cursor.close()

    # noinspection PyUnresolvedReferences
    def commit(self, sql, *args, **kwargs):
        """提交sql or sql list"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, *args, **kwargs)
            self.conn.commit()
            cursor.close()
        except Exception as e:
            # 如果执行sql语句出现问题，则执行回滚操作
            self.conn.rollback()
            if e.args:
                return e.args[0]

    # noinspection PyUnresolvedReferences
    def commit_many(self, sql, data_info):
        """批量提交 sql + list(tuple())"""
        try:
            cursor = self.conn.cursor()
            data_info = ([self._auto_encode(val) for val in values] for values in data_info)
            cursor.executemany(sql, data_info)
            self.conn.commit()
            cursor.close()
        except Exception as e:
            # 如果执行sql语句出现问题，则执行回滚操作
            self.conn.rollback()
            if e.args:
                return e.args[0]

    def query_on_batch(self, sql_form, batch_key, batch_begin_id, batch_size):
        # func: data, args，，，空batch end
        if '{batch_id}' not in sql_form:
            raise TypeError('batch_id not in sql={}'.format(sql_form))

        if '{batch_size}' not in sql_form:
            raise TypeError('batch_size not in sql={}'.format(sql_form))

        batch_id = batch_begin_id
        while True:
            data = [q for q in self.query(sql_form.format(batch_id=batch_id, batch_size=batch_size))]
            last_batch_id = batch_id
            if len(data) > 0:
                batch_id = data[-1][batch_key]

            if last_batch_id != batch_id:
                yield data
            elif len(data) == batch_size:
                batch_size = int(batch_size * 1.5)
                print('batch_size too small, auto expand -> {}'.format(batch_size))
            else:
                break

    def query_on_group(self, sql_form, group_key, batch_begin_id, batch_size, expand_ratio=.6):
        """sql_form 必须是>={batch_id}"""
        # 空batch end
        batch_id_exist = False
        for _c in ('>={batch_id}', '>= {batch_id}', '<={batch_id}', '<= {batch_id}'):
            if _c in sql_form:
                batch_id_exist = True
                break
        if not batch_id_exist:
            raise TypeError('batch_id not in sql={}'.format(sql_form))

        if '{batch_size}' not in sql_form:
            raise TypeError('batch_size not in sql={}'.format(sql_form))

        end_tag = False
        batch_id = batch_begin_id
        last_batch_id = None
        expand_mode = False
        while True:
            sql = sql_form.format(batch_id=batch_id, batch_size=batch_size)
            group_data = [(_id, list(_g)) for _id, _g in groupby(self.query(sql), lambda x: x[group_key])]
            if not expand_mode and (len(group_data) == 0 or last_batch_id == batch_id):
                end_tag = True
            elif len(group_data) == 1:
                if len(group_data[-1][1]) >= int(batch_size * expand_ratio):
                    batch_size = int(batch_size * 1.5)
                    expand_mode = True
                    print('batch_size too small, auto expand -> {}'.format(batch_size))
                else:
                    expand_mode = False
                    end_tag = True
            else:
                expand_mode = False
                for _id, _g in group_data[:-1]:
                    yield _id, _g
                last_batch_id = batch_id
                batch_id = group_data[-1][0]

            if end_tag:
                for _id, _g in group_data:
                    yield _id, _g
                break

    # noinspection PyUnresolvedReferences
    def all_fields(self, table_name):
        cursor = self.conn.cursor()
        cursor.execute('select * from {} limit 0'.format(table_name))
        res = [x[0] for x in cursor.description]
        cursor.close()
        return res

    def all_tables(self):
        """获取所有表"""
        return [list(r.values())[0] for r in self.query('show tables')]

    def count(self, table):
        for r in self.query('select count(*) from {}'.format(table)):
            return list(r.values())[0]


class MongoDB(object):
    def __init__(self, db_param, ssh):
        self.param = db_param
        self.server = None
        if ssh:
            host, port = db_param["host"].split(":")
            port = int(port)
            self.server = tunnel.bind(host, port)
            self.server.start()
            db_param["host"] = "127.0.0.1:%d" % self.server.local_bind_port
        self.host = db_param.get('host')
        self.dbname = db_param.get('database')
        self.colname = db_param.get('collection')
        self.user = db_param.get('user')
        self.password = db_param.get('password')
        self.authsource = db_param.get('authsource')
        self.replicaSet = db_param.get('replicaSet')

        self.client = MongoClient(self.host,
                                  username=self.user,
                                  password=self.password,
                                  authSource=self.authsource)

        self.db = self.client[self.dbname]
        self.col = self.db[self.colname]

        # self.client = MongoClient(self.url, username='')
        # self.db = self.client[self.dbname]
        # self.col = self.db[self.colname]

    def disconnect(self):
        self.client.close()
        if self.server:
            logger.info("==> MongoDB Stop SSH Tunnel")
            self.server.stop()
        return

    def query(self, mgq, fields, size=0):
        res = []
        for x in self.col.find(mgq).limit(size):
            curdic = {k: x.get(k) for k in fields}
            res.append(curdic)
        return res


class MysqlDB(BaseDb):
    def __init__(self, db_param, ssh=False, **kwargs):
        super().__init__()
        if 'charset' not in db_param:
            db_param['charset'] = 'utf8'
        self.param = db_param

        self.server = None
        self.retry_times = RETRY_TIMES
        self.ss_cursor = kwargs.get('ss_cursor', False)
        self.ssh = ssh

    @staticmethod
    def wrap(conn, **kwargs):
        kwargs['db_param'] = kwargs.get('db_param', {})
        db = MysqlDB(**kwargs)
        db.conn = conn
        return db

    def __str__(self):
        if self.param:
            return 'mysql -h%s -P%s -u%s -p%s -D%s' % (self.param.get('host', ''),
                                                       self.param.get('port', 3306),
                                                       self.param.get('user', ''),
                                                       self.param.get('password', ''),
                                                       self.param.get('db', ''))

    # noinspection PyAttributeOutsideInit
    def open(self):
        if self.param:
            not_connected = True
            cursor_class = pymysql.cursors.SSDictCursor if self.ss_cursor else pymysql.cursors.DictCursor

            while not_connected and self.retry_times > 0:
                try:
                    self.retry_times -= 1
                    self.param["cursorclass"] = cursor_class
                    self.param["autocommit"] = True
                    if not self.ssh:
                        self.conn = pymysql.connect(**self.param)
                    else:
                        self.server = tunnel.bind(self.param.get('host', ''), self.param.get('port', 3306))
                        self.server.start()
                        self.param["port"] = self.server.local_bind_port
                        self.param["host"] = "127.0.0.1"
                        self.conn = pymysql.connect(**self.param)

                    not_connected = False
                except pymysql.err.OperationalError as _:
                    # 阶梯时间间隔，尝试重连
                    time.sleep(3)
            self.retry_times = RETRY_TIMES
        return self

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def close(self):
        if self.conn:
            self.conn.close()
        if self.server:
            logger.info("==> MysqlDB Stop SSH Tunnel")
            self.server.stop()

        self.server = None
        self.conn = None

    def _auto_encode(self, x):
        if is_null(x):
            return
        x = auto_format(x)
        if isinstance(x, str):
            return escape_string(x)
        else:
            return json.dumps(x)

    def _auto_decode(self, x):
        if is_null(x):
            return
        if isinstance(x, str):
            try:
                return json.loads(x)
            except:
                pass
        return x

    # def query_df(self, sql, batch_size=None):
    #    """表导出到dataframe batch_size 行数"""
    #    return pd.read_sql(sql, con=self.conn, chunksize=batch_size)

    def insert(self, table, fields, values_iterator, batch_size=None):
        """
        多行插入
        :param table:
        :param fields:
        :param values_iterator: [[一行数据],[另一行数据]]
        :param batch_size: 批次限制
        :return:
        """
        sql_fields = ','.join(['`' + field.strip() + '`' for field in fields])
        sql = 'INSERT INTO {} ({}) VALUES({})'.format(table, sql_fields,
                                                      ','.join(['%s'] * len(fields)))

        data = ([self._auto_encode(v) for v in vs] for vs in values_iterator)
        try:
            cursor = self.conn.cursor()
            if batch_size is None:
                cursor.executemany(sql, data)
            else:
                for batch_data in batch_generator(data, batch_size):
                    cursor.executemany(sql, batch_data)
            cursor.close()
            self.conn.commit()
            return True
        except Exception as e:
            print(str(e))
            # 如果执行sql语句出现问题，则执行回滚操作
            self.conn.rollback()
            return False

    def replace(self, table, fields, values_iterator, batch_size=None):
        """
        批量replace功能，先删除后插入，必须要有primary key 或 unique key
        :param table:
        :param fields:
        :param values_iterator: [[一行数据],[另一行数据]] 其中要包含primary key 或 unique key
        :param batch_size: 批次限制
        :return:
        """
        sql_fields = ','.join(['`' + field.strip() + '`' for field in fields])
        sql = 'REPLACE INTO {} ({}) VALUES({})'.format(table, sql_fields,
                                                       ','.join(['%s'] * len(fields)))
        data = ([self._auto_encode(v) for v in vs] for vs in values_iterator)
        try:
            cursor = self.conn.cursor()
            if batch_size is None:
                cursor.executemany(sql, data)
            else:
                for batch_data in batch_generator(data, batch_size):
                    cursor.executemany(sql, batch_data)
            cursor.close()
            self.conn.commit()
            return True
        except Exception as e:
            print(str(e))
            # 如果执行sql语句出现问题，则执行回滚操作
            self.conn.rollback()
            return False

    def update(self, table, data_dict, condition_sql):
        """
        限定范围的批量update功能
        :param table:
        :param data_dict:
        :param condition_sql:
        :return:
        """
        update_list = ['`{}`=%s'.format(f) for f in six.iterkeys(data_dict)]

        sql = 'UPDATE {} SET {} where {}'.format(table, ','.join(update_list), condition_sql)
        return self.commit_many(sql, [list(six.itervalues(data_dict))])

    def update_from_file(self, file_path, table, fields, sep='\t', unique_keys=None):
        """
        从文件中覆盖表数据
        :param file_path:
        :param table:
        :param fields: string list
        :param sep:
        :param unique_keys:
        :return:
        """

        def _file_data():
            with open(file_path) as r:
                data_len = len(fields)
                for li in r:
                    items = li.rstrip('\n').split(sep)
                    if len(items) == data_len:
                        yield items

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            self.insert_or_update(table, fields, _file_data(), unique_keys=unique_keys)
        else:
            print('Missing file!')

    def all_fields(self, table):
        """
        查询
        :param table:
        :return:
        """
        return [r['Field'] for r in self.query('show full columns from {}'.format(table))]

    def insert_or_update(self, table, fields, values_iterator, unique_keys=None, batch_size=None):
        """
        :param table:
        :param fields:
        :param unique_keys:
        :param batch_size: 用于限制读入内存的或者要控制插入速度的case
        :param values_iterator:
        :return:
        """

        if unique_keys is None:
            unique_keys = ['id']

        update_fields = [fi for fi in fields if fi not in unique_keys]
        sql_fields = ','.join(['`' + field.strip() + '`' for field in fields])
        sql_update_fields = ', '.join(map(lambda x: '`{}`=VALUES(`{}`)'.format(x, x), update_fields))

        sql = 'INSERT INTO {} ({}) VALUES({}) ON DUPLICATE KEY UPDATE {}'.format(
            table, sql_fields, ','.join(['%s'] * len(fields)), sql_update_fields)

        try:
            cursor = self.conn.cursor()
            data = ([self._auto_encode(v) for v in vs] for vs in values_iterator)
            if batch_size is None:
                cursor.executemany(sql, data)
            else:
                for batch_data in batch_generator(data, batch_size):
                    cursor.executemany(sql, batch_data)
            cursor.close()
            self.conn.commit()
            return True
        except Exception as e:
            print(str(e))
            # 如果执行sql语句出现问题，则执行回滚操作
            self.conn.rollback()
            return unique_keys


# 线上服务使用
class ThreadMysqlDB(MysqlDB):
    def open_persist(self):
        """
        自动重连，线程安全，适合任务型
        """
        if self.ssh:
            self.server = tunnel.bind(self.param.get('host', ''), self.param.get('port', 3306))
            self.server.start()
            self.param["port"] = self.server.local_bind_port
            self.param["host"] = "127.0.0.1"

        cursor_class = pymysql.cursors.SSDictCursor if self.ss_cursor else pymysql.cursors.DictCursor
        self.param["autocommit"] = True
        MysqlPool = partial(PersistentDB, creator=pymysql, threadlocal=False, cursorclass=cursor_class)
        self.pool = MysqlPool(**self.param)
        self.conn = self.pool.connection()
        return self

    def open_pool(self, size=10):
        """
        适合服务，经常创建销毁线程
        """
        cursor_class = pymysql.cursors.SSDictCursor if self.ss_cursor else pymysql.cursors.DictCursor
        if self.ssh:
            self.server = tunnel.bind(self.param.get('host', ''), self.param.get('port', 3306))
            self.server.start()
            self.param["port"] = self.server.local_bind_port
            self.param["host"] = "127.0.0.1"

        self.param["read_timeout"] = 1
        self.param["autocommit"] = True
        # 初始创建一个连接，最多size个连接
        MysqlPool = partial(PooledDB, creator=pymysql, mincached=1, maxconnections=size, blocking=True,
                            cursorclass=cursor_class)
        self.pool = MysqlPool(**self.param)
        return self

    def query(self, sql, *args, **kwargs):
        """返回数据长度，用fetch获得具体数据"""
        conn = self.pool.connection(shareable=False)
        cursor = conn.cursor()
        cursor.execute(sql, *args, **kwargs)
        rows = cursor.fetchall()
        # 及早放回
        cursor.close()
        conn.close()
        return rows


class SqliteDb(BaseDb):
    """
    内存模式并发读，同步写，写入时可读
    文件模式写入时不可读，并发读

    CREATE TABLE company(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       name_id          INT,
       age            INT,
       addr        CHAR(50),
       salary         REAL
    )

    db.insert('test, ['id', 'text'], [[11, None], [12, 'ttt'], [13, {'a':None, 'b':{'c':[1,None]}}]])
    db.insert_or_update('test, ['id', 'text'], [[11, 33], [14, 'ccc']])
    db.update('test, {'text': 'mmmm'}, condition_sql='id=12')

    sql_form = 'select * from test where id>{batch_id} order by id limit {batch_size}'
    list(ai_db.query_on_batch(sql_form, 'id', 3, 2))

    sql_form = 'select * from company where name_id>={batch_id} order by name_id limit {batch_size}'
    list(ai_db.query_on_group(sql_form, 'name_id', 99, 3))
    """

    def __init__(self, db_file=None):
        super().__init__()
        self.db_file = db_file if db_file is not None else ':memory:'

    @staticmethod
    def wrap(conn, **kwargs):
        db = SqliteDb(**kwargs)
        db.conn = conn
        db.cursor = conn.cursor()
        return db

    # noinspection PyAttributeOutsideInit
    def open(self):
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        try:
            self.conn = sqlite3.connect(self.db_file)
            self.conn.row_factory = dict_factory
            self.cursor = self.conn.cursor()

        except sqlite3.Error as e:
            print(e)
        return self

    def __str__(self):
        return '{}: {}'.format(sqlite3.sqlite_version, self.db_file)

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

        self.cursor = None
        self.conn = None

    def all_tables(self):
        """获取所有表"""
        res = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [list(r.values())[0] for r in res]

    def _auto_encode(self, x):
        if is_null(x):
            return
        x = auto_format(x)
        if isinstance(x, (str, int, float)):
            return x
        else:
            return json.dumps(x)

    def _auto_decode(self, x):
        if isinstance(x, str):
            try:
                return json.loads(x)
            except:
                pass
        return x

    def insert(self, table, fields, values_iterator, batch_size=None):
        """
        多行插入
        :param table:
        :param fields:
        :param values_iterator: [[一行数据],[另一行数据]]
        :param batch_size: 批次限制
        :return:
        """
        sql_fields = ','.join(['`' + field.strip() + '`' for field in fields])
        sql = 'INSERT INTO {} ({}) VALUES({})'.format(table, sql_fields,
                                                      ','.join(['?'] * len(fields)))

        data = ([self._auto_encode(v) for v in vs] for vs in values_iterator)
        try:
            if batch_size is None:
                self.cursor.executemany(sql, data)
            else:
                for batch_data in batch_generator(data, batch_size):
                    self.cursor.executemany(sql, batch_data)

            self.conn.commit()
            return True
        except Exception as e:
            print(str(e))
            # 如果执行sql语句出现问题，则执行回滚操作
            self.conn.rollback()
            return False

    def replace(self, table, fields, values_iterator, batch_size=None):
        """
        批量replace功能，先删除后插入，必须要有primary key 或 unique key
        :param table:
        :param fields:
        :param values_iterator: [[一行数据],[另一行数据]] 其中要包含primary key 或 unique key
        :param batch_size: 批次限制
        :return:
        """
        sql_fields = ','.join(['`' + field.strip() + '`' for field in fields])
        sql = 'REPLACE INTO {} ({}) VALUES({})'.format(table, sql_fields,
                                                       ','.join(['?'] * len(fields)))
        data = ([self._auto_encode(v) for v in vs] for vs in values_iterator)
        try:
            if batch_size is None:
                self.cursor.executemany(sql, data)
            else:
                for batch_data in batch_generator(data, batch_size):
                    self.cursor.executemany(sql, batch_data)

            self.conn.commit()
            return True
        except Exception as e:
            print(str(e))
            # 如果执行sql语句出现问题，则执行回滚操作
            self.conn.rollback()
            return False

    def update(self, table, data_dict, condition_sql):
        """
        限定范围的批量update功能
        :param table:
        :param data_dict:
        :param condition_sql:
        :return:
        """
        update_list = ['`{}`=?'.format(k) for k in six.iterkeys(data_dict)]

        sql = 'UPDATE {} SET {} where {}'.format(table, ','.join(update_list), condition_sql)
        return self.commit_many(sql, [list(six.itervalues(data_dict))])

    def insert_or_update(self, table, fields, values_iterator, unique_keys=None, batch_size=None):
        """
        :param table:
        :param fields:
        :param unique_keys:
        :param values_iterator:
        :param batch_size: 用于限制读入内存的或者要控制插入速度的case
        :param values_iterator:
        :return:
        """

        if unique_keys is None:
            unique_keys = ['id']

        update_fields = [fi for fi in fields if fi not in unique_keys]
        sql_fields = ','.join(['`' + field.strip() + '`' for field in fields])
        sql_update_fields = ', '.join(map(lambda x: '{}=?'.format(x), update_fields))

        sql = 'INSERT INTO {} ({}) VALUES({}) ON CONFLICT({}) DO UPDATE SET {}'.format(
            table, sql_fields, ','.join(['?'] * len(fields)),
            ','.join(unique_keys), sql_update_fields)

        try:
            data = ([self._auto_encode(x) for x in _data] +
                    [self._auto_encode(x) for f, x in zip(fields, _data) if f in update_fields]
                    for _data in values_iterator)
            if batch_size is None:
                self.cursor.executemany(sql, data)
            else:
                for batch_data in batch_generator(data, batch_size):
                    self.cursor.executemany(sql, batch_data)

            self.conn.commit()
            return True
        except Exception as e:
            print(str(e))
            # 如果执行sql语句出现问题，则执行回滚操作
            self.conn.rollback()
            return unique_keys


class AnnItemIndexMixin(object):
    def __init__(self, ann_dir, ann_name, ts):
        self.ann_dir = ann_dir
        self.ann_name = ann_name
        self.ts = ts
        self.fn = os.path.join(self.ann_dir, '{}_{}.item'.format(self.ann_name, ts))
        file.ensure_dir(ann_dir)

    def __iter__(self):
        raise NotImplementedError

    def load(self):
        raise NotImplementedError

    def open(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def add_item(self, item):
        """存储item"""
        raise NotImplementedError

    def item2id(self, item):
        """读取item id"""
        raise NotImplementedError

    def id2item(self, item_ind):
        """读取item"""
        raise NotImplementedError

    def has_item(self, item):
        raise NotImplementedError

    def has_id(self, item_id):
        raise NotImplementedError

    def get_n_items(self):
        raise NotImplementedError

    def clear(self):
        if os.path.exists(self.fn):
            try:
                os.remove(self.fn)
            except:
                pass

    def move_to(self, dst_dir):
        dst_dir = os.path.abspath(dst_dir)
        if dst_dir == self.ann_dir:
            return self

        if os.path.exists(self.fn):
            file.ensure_dir(dst_dir)
            dst_fn = os.path.join(dst_dir, '{}_{}.item'.format(self.ann_name, self.ts))
            shutil.move(self.fn, dst_fn)
            self.ann_dir = dst_dir
            self.fn = dst_fn
        return self


class FileAnnIndex(AnnItemIndexMixin):
    def __init__(self, ann_dir, ann_name, ts, **kwargs):
        super().__init__(ann_dir, ann_name, ts)
        self.item2id_dict = bidict()
        self.item_ind = 0
        self.item_type = kwargs.get('item_type', 'str')
        self.item_func = {
            'str': str,
            'int': int,
            'float': float,
        }[kwargs.get('item_type', 'str')]

    def open(self):
        pass

    def load(self):
        if file.is_data_file_ok(self.fn):
            with open(self.fn, 'r', encoding='utf-8') as r:
                for line in r:
                    if not line.strip():
                        continue
                    id_str, item_str = line.strip().split('\t')
                    self.item2id_dict[self.item_func(item_str)] = int(id_str)
            if len(self.item2id_dict) > 0:
                self.item_ind = max(six.itervalues(self.item2id_dict)) + 1
        return self

    def __iter__(self):
        for _item, _ind in six.iteritems(self.item2id_dict):
            yield _item, _ind

    def close(self):
        file.ensure_file_dir(self.fn)
        with open(self.fn, mode='w', encoding='utf-8') as w:
            for k, v in six.iteritems(self.item2id_dict):
                w.write('{}\t{}\n'.format(v, k))

    def add_item(self, item):
        """存储item"""
        if self.has_item(item):
            return -1
        self.item2id_dict[item] = self.item_ind
        self.item_ind += 1
        return self.item_ind - 1

    def item2id(self, item):
        """读取item id"""
        return self.item2id_dict.get(item)

    def id2item(self, item_ind):
        """读取item"""
        return self.item2id_dict.inverse.get(item_ind)

    def has_item(self, item):
        return item in self.item2id_dict

    def has_id(self, item_id):
        return item_id in self.item2id_dict.inverse

    def get_n_items(self):
        return len(self.item2id_dict)

    def clear(self):
        if os.path.exists(self.fn):
            os.remove(self.fn)


class PikAnnIndex(AnnItemIndexMixin):
    def __init__(self, ann_dir, ann_name, ts, **kwargs):
        super().__init__(ann_dir, ann_name, ts)
        self.item2id_dict = bidict()
        self.item_ind = 0
        self.item_type = kwargs.get('item_type', 'str')
        self.item_func = {
            'str': str,
            'int': int,
            'float': float,
        }[kwargs.get('item_type', 'str')]

    def open(self):
        pass

    def load(self):
        self.item2id_dict = file.load_pickle(self.fn)
        if len(self.item2id_dict) > 0:
            self.item_ind = max(six.itervalues(self.item2id_dict)) + 1
        return self

    def __iter__(self):
        for _item, _ind in six.iteritems(self.item2id_dict):
            yield _item, _ind

    def close(self):
        file.dump_pickle(self.item2id_dict, self.fn)

    def add_item(self, item):
        """存储item"""
        if self.has_item(item):
            return -1
        self.item2id_dict[item] = self.item_ind
        self.item_ind += 1
        return self.item_ind - 1

    def item2id(self, item):
        """读取item id"""
        return self.item2id_dict.get(item)

    def id2item(self, item_ind):
        """读取item"""
        return self.item2id_dict.inverse.get(item_ind)

    def has_item(self, item):
        return item in self.item2id_dict

    def has_id(self, item_id):
        return item_id in self.item2id_dict.inverse

    def get_n_items(self):
        return len(self.item2id_dict)

    def clear(self):
        if os.path.exists(self.fn):
            os.remove(self.fn)


class SqliteAnnIndex(AnnItemIndexMixin):
    # noinspection PyUnusedLocal
    def __init__(self, ann_dir, ann_name, ts, **kwargs):
        super().__init__(ann_dir, ann_name, ts)
        self.read_fn = os.path.join(self.ann_dir, 'sqlite_read_{}_{}.item'.format(
            self.ann_name, sign(6, with_time=True)))
        self.conn = None
        self.cursor = None
        self.item_ind = 0

        try:
            with SqliteDb(self.fn) as sdb:
                sdb.commit("""CREATE TABLE IF NOT EXISTS item(
                                                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                               val TEXT NOT NULL UNIQUE)""")
        except:
            pass
        shutil.copyfile(self.fn, self.read_fn)

    def load(self):
        return self

    def __del__(self):
        try:
            if os.path.exists(self.read_fn):
                os.remove(self.read_fn)

            # 邪道 概率清理一下
            if random.random() < 0.0001:
                for fn_name in os.listdir(self.ann_dir):
                    if fn_name.startswith('sqlite_read_'):
                        fn = os.path.join(self.ann_dir, fn_name)
                        os.remove(fn)

        except:
            pass

    def open(self):
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        self.conn = sqlite3.connect(self.fn)
        self.conn.row_factory = dict_factory
        self.cursor = self.conn.cursor()
        self.item_ind = 0
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS item(
                                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                                               val TEXT NOT NULL UNIQUE)""")
        self.conn.commit()
        return self

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.commit()
            self.conn.close()

        self.conn = None
        self.cursor = None

    def __iter__(self):
        with SqliteDb(self.read_fn) as sdb:
            for q in sdb.query('select id, val from item'):
                yield q['val'], q['id']

    def add_item(self, item):
        """存储item"""
        try:
            self.cursor.execute('INSERT INTO item(val) VALUES(?)', (item,))
            self.item_ind += 1
        except sqlite3.Error as e:
            print(e)
            return -1

        return self.item_ind - 1

    def item2id(self, item):
        """读取item id"""
        with SqliteDb(self.read_fn) as sdb:
            for q in sdb.query('select id from item where val=?', (item,)):
                return q['id'] - 1

    def id2item(self, item_ind):
        """读取item"""
        with SqliteDb(self.read_fn) as sdb:
            for q in sdb.query('select val from item where id={}'.format(item_ind + 1)):
                return q['val']

    def has_item(self, item):
        try:
            with SqliteDb(self.read_fn) as sdb:
                for _ in sdb.query('select id from item where val=?', (item,)):
                    return True
        except:
            pass
        return False

    def has_id(self, item_ind):
        try:
            with SqliteDb(self.read_fn) as sdb:
                for _ in sdb.query('select id from item where id={}'.format(item_ind + 1)):
                    return True
        except:
            pass
        return False

    def get_n_items(self):
        with SqliteDb(self.read_fn) as sdb:
            return sdb.count('item')

    def clear(self):
        if os.path.exists(self.fn):
            os.remove(self.fn)
            try:
                with SqliteDb(self.fn) as sdb:
                    sdb.commit("""CREATE TABLE IF NOT EXISTS item(
                                                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                   val TEXT NOT NULL UNIQUE)""")
            except:
                pass


class AnnDb(object):
    """
    ann检索数据库，cpu机器用annoy，cuda机器用faiss
    annoy索引文件路径必须是英文路径

    annoy API：1.16.3
        a.get_nns_by_item(i,n,search_k=-1, include_distances=False):通过item id 进行查询
        a.get_nns_by_vector(v, n, search_k=-1, include_distances=False)：通过vector进行查询
        a.get_item_vector(i):通过item id 获取vector
        a.get_distance(i, j):传入两个item id返回两者之间的距离。
        a.get_n_items():返回共有多少个item
        a.get_n_trees():返回创建索引时共有多少颗树
    """

    def __init__(self, fn, cache_dir=None):
        """
        :param fn: db文件地址
        """

        self.me = sign(3, with_time=True)

        fn = os.path.abspath(fn)
        self.ann_name = os.path.basename(fn).split('.')[0]
        self.ann_dir = os.path.dirname(fn)

        self.config_fn = os.path.join(self.ann_dir, '{}.config'.format(self.ann_name))
        self.config = None

        self.db = None
        self.item_index_class = None

        self.fn_index = os.path.join(self.ann_dir, '{}.index'.format(self.ann_name))
        self.ann_index = None
        self.ts = None

        self.ann_bad_log = os.path.join(self.ann_dir, '{}.bad'.format(self.ann_name))

        if cache_dir is None:
            cache_dir = os.path.join(g_cache_root, sign(8))
        self.cache_dir = cache_dir

    def __len__(self):
        return self.ann_index.get_n_items() if self.ann_index is not None else 0

    def __getitem__(self, k):
        return self.get_item_vector(k)

    def __contains__(self, k):
        return self.has_item(k)

    def __iter__(self):
        if self.ann_index is not None:
            for _item, _ind in self.ann_index:
                yield _item, _ind, self.db.get_item_vector(_ind)

    def set_from_config(self, d):
        file.dump_pickle(d, self.config_fn)
        self.init_config(force=True)
        return self

    def set_config(self, item_type, vec_length=200, n_trees=100, ann_index_type='file', lifetime=1800, backup_count=3,
                   ann_type='dot', load_check=True):
        d = {
            'ann_type': ann_type,  # 距离计算方式 "angular", "euclidean", "manhattan", "hamming", "dot"
            'vec_length': vec_length,  # 向量长度
            'n_trees': n_trees,  # n_trees越高查询越准确(影响build速度和index长度)
            'item_type': item_type,  # "str" or "int"
            'ann_index_type': ann_index_type,  # file or db
            'lifetime': lifetime,
            'backup_count': backup_count,
            'load_check': load_check,
        }
        file.dump_pickle(d, self.config_fn)
        self.init_config(force=True)
        return self

    def init_config(self, force=False):
        if self.config is None or force:
            self.config = file.load_pickle(self.config_fn)
            self.db = AnnoyIndex(self.config['vec_length'], self.config['ann_type'])

            self.item_index_class = {
                'file': FileAnnIndex,
                'db': SqliteAnnIndex,
                'pik': PikAnnIndex,
            }[self.config['ann_index_type']]

    def __del__(self):
        try:
            self._close(self.ts)
        except:
            pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close(self.ts)
        return False

    def _open(self, ts):
        if ts:
            fn_py_lock = os.path.join(self.ann_dir, '{}_{}.py.lock'.format(self.ann_name, ts))
            file.ensure_file_dir(fn_py_lock)
            try:
                with open(fn_py_lock, 'a') as w:
                    #fcntl.flock(w.fileno(), fcntl.LOCK_EX)
                    w.write(self.me + '\n')
            except OSError as _:
                pass

    def _close(self, ts):
        if ts:
            rm_tag = False
            fn_py_lock = os.path.join(self.ann_dir, '{}_{}.py.lock'.format(self.ann_name, ts))
            if os.path.exists(fn_py_lock):
                try:
                    with open(fn_py_lock, 'w') as w:
                        #fcntl.flock(w.fileno(), fcntl.LOCK_EX)
                        with open(fn_py_lock) as r:
                            tags = r.readlines()
                            if self.me in tags:
                                tags.remove(self.me)
                                w.write('\n'.join(tags) + '\n')
                            if len(tags) == 0:
                                rm_tag = True
                        if rm_tag:
                            os.remove(fn_py_lock)
                except OSError as _:
                    pass

    def load(self, prefault=False):
        self.init_config()

        if self.config is None:
            print('no config found..')
            return self

        file.ensure_file_dir(self.fn_index)
        if os.path.exists(self.fn_index) and os.path.getsize(self.fn_index) > 0:
            try:
                with open(self.fn_index) as r:
                    ts = int(r.read().strip())
                    if self.load_ts(ts, prefault=prefault):
                        print('loading {} success! ts={},ann item count={}'.format(
                            self.fn_index, self.ts, self.db.get_n_items()))
                        return self
            except:
                pass

        print('loading {} from backup...'.format(self.fn_index))
        for _ts in self.iterbackup():
            if self.load_ts(_ts):
                with open(self.fn_index, 'w') as w:
                    w.write(str(self.ts))
                    print('loading {} success! ts={},ann item count={}'.format(
                        self.fn_index, self.ts, self.db.get_n_items()))
                    return self
        else:
            print('loading {} failed'.format(self.fn_index))
        return self

    def load_ts(self, ts, check=None, prefault=False):
        if self.config is None:
            self.init_config()
            if self.config is None:
                print('no config found..')
                return False

        if check is None:
            check = self.config['load_check'] if self.config is not None else True
        if not ts:
            return False
        _fn = os.path.join(self.ann_dir, '{}_{}.ann'.format(self.ann_name, ts))
        if file.is_data_file_ok(_fn):
            self.db.load(_fn, prefault)
            self.ann_index = self.item_index_class(self.ann_dir, self.ann_name, ts,
                                                   item_type=self.config['item_type']).load()

            if not check or self.db.get_n_items() == self.ann_index.get_n_items():
                self._close(self.ts)
                self._open(ts)
                self.ts = ts
                return True
        return False

    def iterbackup(self):
        ts_list = []
        for _f_name in os.listdir(self.ann_dir):
            try:
                if _f_name.endswith('.ann') and _f_name.startswith(self.ann_name):
                    ts = int(_f_name.split('.')[0][len(self.ann_name) + 1:])
                    ts_list.append(ts)
            except:
                continue
        if len(ts_list) > 0:
            s_ts_list = sorted(ts_list, reverse=True)
            for _ts in s_ts_list:
                yield _ts

    def iteritems(self):
        if self.ann_index is not None:
            for _item, _ind in self.ann_index:
                yield _item, self.db.get_item_vector(_ind)

    def iterkeys(self):
        if self.ann_index is not None:
            for _item, _ in self.ann_index:
                yield _item

    def itervalues(self):
        if self.ann_index is not None:
            for _, _ind in self.ann_index:
                yield self.db.get_item_vector(_ind)

    def update(self, data_generator, **kwargs):
        """更新时需要重新build，会比较慢，且内存X2"""
        self.init_config()

        if self.config is None:
            raise RuntimeError('not config yet!')

        if isinstance(data_generator, dict):
            data_generator = ((k, v) for k, v in six.iteritems(data_generator))

        def _merge():
            for k, v in self.iteritems():
                yield k, v
            for k, v in data_generator:
                yield k, v

        self.build(_merge(), **kwargs)

    def has_new(self, ts):
        file.ensure_file_dir(self.fn_index)
        if os.path.exists(self.fn_index) and os.path.getsize(self.fn_index) > 0:
            try:
                with open(self.fn_index) as r:
                    new_ts = int(r.read().strip())
                    return new_ts > ts
            except:
                pass
        return False

    @staticmethod
    def sync_build(anns, datas, on_disk=False, ts=None):
        if ts is None:
            ts = int(time.time())

        for ann, data in zip(anns, datas):
            ann.build(data, on_disk=on_disk, ts=ts)
        return ts

    @staticmethod
    def sync_load(fn_dir, ts, items=None):
        d = {}
        fn_dir = os.path.abspath(fn_dir)
        for i in items:
            ann = AnnDb(os.path.join(fn_dir, i))
            if not ann.load_ts(ts):
                return {}
            else:
                d[ann.ann_name] = ann
        return d

    def build(self, data_generator, on_disk=False, ts=None):
        """
        不支持增量build
        :param data_generator: (item, vec)数据流 or dict
        :param on_disk:
        :param ts:
        :return:
        """
        if self.config is None:
            raise RuntimeError('not config yet!')

        if isinstance(data_generator, dict):
            data_generator = ((k, v) for k, v in six.iteritems(data_generator))
        file.ensure_dir(self.ann_dir)

        db = AnnoyIndex(self.config['vec_length'], self.config['ann_type'])

        if ts is None:
            ts = int(time.time())

        file.ensure_dir(self.cache_dir)
        fn = os.path.join(self.cache_dir, '{}_{}.ann'.format(self.ann_name, ts))
        ann_index = self.item_index_class(self.cache_dir, self.ann_name, ts, item_type=self.config['item_type']).load()
        ann_index.open()

        if on_disk:
            # on_disk: 在add_item之前
            db.on_disk_build(fn)

        for item, vec in data_generator:
            if item is None or not str(item).strip() or vec is None:
                print('item {} ignored'.format(item))
                continue

            if ann_index.has_item(item):
                print('item {} repeat'.format(item))
                continue
            ind = ann_index.add_item(item)
            if ind > 0:
                db.add_item(ind, vec)

        db.build(self.config['n_trees'])
        if not on_disk:
            db.save(fn, prefault=True)

        ann_index.close()
        if not file.is_data_file_ok(fn):
            print('[warning] build failed on fn={}'.format(fn))
            ann_index.clear()
            if os.path.exists(fn):
                os.remove(fn)
            file.clear_dir(self.cache_dir, keep_dir=False)
            ts = None
        else:
            # 写入更新索引
            tar_fn = os.path.join(self.ann_dir, '{}_{}.ann'.format(self.ann_name, ts))
            shutil.move(fn, tar_fn)
            ann_index.move_to(self.ann_dir)

            if self.load_ts(ts, check=self.config['load_check']):
                print('build succcess fn={} count={}'.format(tar_fn, self.get_n_items()))
                if random.random() < .2:
                    # try clear backup
                    self.clear()

                with open(self.fn_index, 'w') as w:
                    w.write(str(ts))

        file.clear_dir(self.cache_dir, keep_dir=False)
        return ts

    def has_update(self):
        if os.path.exists(self.fn_index):
            with open(self.fn_index) as r:
                try:
                    return int(r.read().strip())
                except:
                    pass
        return False

    def has_item(self, i):
        return self.ann_index is not None and self.ann_index.has_item(i)

    def get_item_vector(self, i):
        """通过item id 获取vector"""
        if self.ann_index is not None:
            item_ind = self.ann_index.item2id(i)
            if item_ind is not None:
                return self.db.get_item_vector(item_ind)

    def _get_nns(self, func, item, n, search_k, include_distances):
        """通过item id 进行查询近邻"""
        if self.ann_index is None:
            return

        item_ind = self.ann_index.item2id(item)
        if item_ind is not None:
            result = func(item_ind, n, search_k=search_k, include_distances=include_distances)
            if result is not None:
                if include_distances:
                    item_ids, scores = result
                    return [self.ann_index.id2item(_id) for _id in item_ids], scores
                else:
                    return [self.ann_index.id2item(_id) for _id in result]

    def get_nns_by_item(self, i, n, search_k=-1, include_distances=False):
        """通过item id 进行模糊查询近邻"""
        if self.ann_index is None:
            return
        item_ind = self.ann_index.item2id(i)
        if item_ind is not None:
            result = self.db.get_nns_by_item(item_ind, n, search_k=search_k, include_distances=include_distances)
            if result is not None:
                if include_distances:
                    item_ids, scores = result
                    return [self.ann_index.id2item(_id) for _id in item_ids], scores
                else:
                    return [self.ann_index.id2item(_id) for _id in result]

    def get_nns_by_vector(self, v, n, search_k=-1, include_distances=False):
        """通过vector进行模糊查询近邻 (item_ids, scores)"""
        if self.ann_index is None:
            return

        result = self.db.get_nns_by_vector(v, n, search_k=search_k, include_distances=include_distances)
        if include_distances:
            item_ids, scores = result
            return [self.ann_index.id2item(_id) for _id in item_ids], scores
        else:
            return [self.ann_index.id2item(_id) for _id in result]

    def get_precise_nns_by_item(self, i, n=None, items=None, include_distances=False):
        """通过item id 进行精确查询近邻"""

        return self.get_precise_nns_by_vector(self.get_item_vector(i), n=n, items=items,
                                              include_distances=include_distances)

    def get_precise_nns_by_vector(self, v, n=None, items=None, include_distances=False):
        """通过item id 进行精确查询近邻"""
        if items is None:
            items = list(self.iterkeys())
        if n is None:
            n = len(items)

        j_vecs = [self.get_item_vector(_j) for _j in items]
        scores = (cosine_similarity([v], j_vecs)[0]).tolist()
        data = zip(items, scores)
        result = sorted(data, key=lambda x: x[1], reverse=True)[:n]
        if include_distances:
            res_i = []
            res_s = []
            for _i, _score in result:
                res_i.append(_i)
                res_s.append(_score)
            return res_i, res_s
        else:
            return [_i for _i, _ in result]

    def get_distance(self, i, j):
        """传入两个item id返回两者之间的距离。"""
        i_vec = self.get_item_vector(i)
        j_vec = self.get_item_vector(j)
        return cosine_similarity([i_vec], [j_vec])[0][0]

    def get_n_items(self):
        """返回共有多少个item, annoy 的get_n_items 返回id索引号+1"""
        return self.ann_index.get_n_items() if self.ann_index is not None else 0

    def get_n_trees(self):
        """返回创建索引时共有多少颗树"""
        return self.db.get_n_trees()

    def clear(self, ts=None, force_all=False):
        def _del(del_ts, rm_tag=None):
            _fn = os.path.join(self.ann_dir, '{}_{}.ann'.format(self.ann_name, del_ts))
            _index_fn = os.path.join(self.ann_dir, '{}_{}.item'.format(self.ann_name, del_ts))
            _java_lock_fn = os.path.join(self.ann_dir, '{}_{}.java.lock'.format(self.ann_name, del_ts))
            _py_lock_fn = os.path.join(self.ann_dir, '{}_{}.py.lock'.format(self.ann_name, del_ts))
            if rm_tag is None:
                rm_tag = True
                if now_ts - _ts < self.config['lifetime']:
                    for fn_lock in [_java_lock_fn, _py_lock_fn]:
                        if os.path.exists(fn_lock):
                            with open(fn_lock) as rf:
                                if rf.read().strip():
                                    rm_tag = False
                                    break
            if rm_tag:
                try:
                    for _rm_fn in [_fn, _index_fn, _java_lock_fn, _py_lock_fn]:
                        if os.path.exists(_rm_fn):
                            os.remove(_rm_fn)
                except:
                    pass

        self.init_config()

        if self.config is None:
            file.clear_dir(self.ann_dir)
            return

        if os.path.exists(self.ann_bad_log):
            with open(self.ann_bad_log) as r:
                for _ts in r.readlines():
                    _del(_ts.strip(), rm_tag=True)
            os.remove(self.ann_bad_log)

        now_ts = int(time.time())
        keep = self.config['backup_count']
        for _ts in self.iterbackup():
            if ts is not None and _ts > ts:
                continue

            if not force_all and keep > 0:
                keep -= 1
                continue

            _del(_ts)


class ClickHouseDb(BaseDb):
    def __init__(self, db_param):
        super().__init__()
        self.param = db_param

    @staticmethod
    def wrap(conn, **kwargs):
        kwargs['db_param'] = kwargs.get('db_param', {})
        db = ClickHouseDb(**kwargs)
        db.conn = conn
        db.cursor = conn.cursor()
        return db

    # noinspection PyAttributeOutsideInit
    def open(self):
        self.conn = ch_connect(**self.param)
        self.cursor = self.conn.cursor()
        return self

    def disconnect(self):
        self.close()

    # noinspection PyAttributeOutsideInit
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

        self.cursor = None
        self.conn = None

    def query(self, sql, *args, **kwargs):
        """返回数据长度，用fetch获得具体数据"""

        def dict_factory(row):
            d = {}
            for idx, col in enumerate(self.cursor.description):
                d[col[0]] = row[idx]
            return d

        self.cursor.execute(sql, *args, **kwargs)
        for r in self:
            yield dict_factory(r)


class LogDb(object):
    def __init__(self, db_param):
        self.client = LogClient(db_param['endpoint'], db_param['key_id'], db_param['key'])
        self.param = db_param

    def query(self, sql, ):
        """select * from recommend-impression where __date__ >'2021-05-19 00:10:10' and __date__ < '2021-05-19 10:20:10' limit 100"""

        req = GetProjectLogsRequest(self.param['project'], sql)
        res = self.client.get_project_logs(req).get_body()
        for row in res:
            yield row


class InfluxDB(object):
    def __init__(self, db_param, time_zone=None, enable_gzip=False):
        super().__init__()
        self.param = db_param
        self.host = db_param['url']
        self.user = "nowcoder"
        self.token = db_param['token']
        self.timeout = db_param['timeout']
        if time_zone is None:
            self.time_zone = tzlocal.get_localzone()
        else:
            self.time_zone = time_zone

    # server 使用保持客户端连接
    @staticmethod
    def wrap(**kwargs):
        kwargs['db_param'] = kwargs.get('db_param', {})
        db = InfluxDB(**kwargs)
        return db

    def __iter__(self):
        return self

    def __enter__(self):
        return self.open()

    def __del__(self):
        try:
            self.close()
        except:
            pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    # noinspection PyAttributeOutsideInit
    def open(self):
        self.client = self.get_client()
        return self

    def disconnect(self):
        self.close()

    # noinspection PyAttributeOutsideInit
    def close(self):
        if self.client:
            self.client.close()
        self.client = None

    def get_client(self):
        return InfluxDBClient(**self.param)

    def insert(self, bucket, records, whether_sync=True):
        if bucket is None or records is None:
            return

        if self.client is None:
            print("Please reconnect influxdb!")
            return

        if whether_sync:
            write_type = SYNCHRONOUS
        else:
            write_type = ASYNCHRONOUS

        write_api = self.client.write_api(write_options=write_type)
        write_api.write(bucket=bucket, org=self.user, record=records, timeout=self.timeout)
        write_api.close()
        # client.close()

    def insert_batch(self, bucket, records, whether_sync=True, write_options=None):
        if bucket is None or records is None:
            print('Please enter the bucket or records data!')
            return

        if len(records) == 1:
            self.insert(bucket, records[0], whether_sync)
        else:
            if self.client is None:
                print("Please reconnect influxdb!")
                return

            if whether_sync:
                write_type = SYNCHRONOUS
            else:
                write_type = ASYNCHRONOUS

            # write_options for batch write

            batch_size = 500 if write_options is None or write_options['batch_size'] is None else \
                write_options['batch_size']
            flush_interval = 10000 if write_options is None or write_options['flush_interval'] is None else \
                write_options['flush_interval']
            jitter_interval = 2000 if write_options is None or write_options['jitter_interval'] is None else \
                write_options['jitter_interval']
            retry_interval = 5000 if write_options is None or write_options['retry_interval'] is None else \
                write_options['retry_interval']
            max_retries = 5 if write_options is None or write_options['max_retries'] is None else \
                write_options['max_retries']
            max_retry_delay = 30000 if write_options is None or write_options['max_retry_delay'] is None else \
                write_options['max_retry_delay']
            exponential_base = 2 if write_options is None or write_options['exponential_base'] is None else \
                write_options['exponential_base']

            write_api = self.client.write_api(write_options=WriteOptions(write_type=write_type,
                                                                         batch_size=batch_size,
                                                                         flush_interval=flush_interval,
                                                                         jitter_interval=jitter_interval,
                                                                         retry_interval=retry_interval,
                                                                         max_retries=max_retries,
                                                                         max_retry_delay=max_retry_delay,
                                                                         exponential_base=exponential_base))
            write_api.write(bucket, self.user, records)

            write_api.close()

    def query(self, q):
        if q is None:
            return

        if self.client is None:
            print("Please reconnect influxdb!")
            return

        query_api = self.client.query_api()
        res = query_api.query_data_frame(org=self.user, query=q)

        # q中可能查询的为多表数据，则返回的是list，故需要判定，反之查询一个表，返回dataframe
        if isinstance(res, list):
            for i in range(len(res)):
                if res[i] is not None and '_time' in res[i].columns:
                    res[i] = res[i].set_index('_time').tz_convert(self.time_zone)
        else:
            if res is not None and '_time' in res.columns:
                res = res.set_index('_time').tz_convert(self.time_zone)
        # results = []
        # if res is not None:
        #     for table in res:
        #         for record in table.records:
        #             results.append((record.get_field(), record.get_value()))
        # client.close()
        # return results
        return res

    def delete(self, start, stop, bucket, measurement):
        if start is None or measurement is None or bucket is None:
            return
        # 将datetime格式的时间转化为RFC3339Nano，否则会报错
        if stop is None:
            stop = datetime.datetime.utcnow()
            stop = stop.replace(tzinfo=pytz.UTC)
            stop = stop.isoformat()

        start = start.replace(tzinfo=pytz.UTC)
        start = start.isoformat()

        if self.client is None:
            print("Please reconnect influxdb!")
            return

        delete_api = self.client.delete_api()
        print(start, stop, measurement, bucket)
        delete_api.delete(start, stop, '_measurement={}'.format(measurement), bucket=bucket, org=self.user)


class RedisClient(object):
    """
    self.client is thread safe
    multi-instance-share use connection_pool=true
    """

    def __init__(self, param, connection_pool=None, return_pool=False, ssh=False):
        self.host = param["host"]
        self.port = param["port"]
        if connection_pool is not None:
            self.client = redis.Redis(connection_pool=connection_pool)
            return
        if ssh:
            self.server = tunnel.bind(self.host, self.port)
            self.server.start()
            param["port"] = self.server.local_bind_port
            param["host"] = "127.0.0.1"
        if return_pool:
            self.pool = redis.ConnectionPool(**param)
            self.client = redis.Redis(connection_pool=self.pool)
        else:
            self.client = redis.Redis(**param)

    def get(self, key):
        return self.client.get(key)

    def set(self, key, value, expire_time=-1):
        if expire_time < 0:
            return self.client.set(key, value)
        return self.client.set(key, value, ex=expire_time)

    def mset(self, data_dict, expire_time=-1):
        if expire_time < 0:
            return self.client.mset(data_dict)
        else:
            with self.client.pipeline() as pipe:
                for key, value in data_dict.items():
                    pipe.set(key, value, ex=expire_time)
                return pipe.execute()

    def mget(self, keys):
        return self.client.mget(keys)

    def hset(self, name, data_dict, expire_time=-1):
        with self.client.pipeline() as pipe:
            for key, value in data_dict.items():
                pipe.hset(name, key, value)
            if expire_time > 0:
                pipe.expire(name, expire_time)
            return pipe.execute()

    def hget(self, name, keys):
        return self.client.hmget(name, keys)

    def mhget(self, names, keys):
        with self.client.pipeline() as pipe:
            for name in names:
                pipe.hmget(name, keys)
            return pipe.execute()

    def hgetall(self, name):
        return self.client.hgetall(name)

    def mhgetall(self, names):
        with self.client.pipeline() as pipe:
            for name in names:
                pipe.hgetall(name)
            return pipe.execute()

    def expire(self, names, expire_time):
        with self.client.pipeline() as pipe:
            for name in names:
                pipe.expire(name, expire_time)
            return pipe.execute()

    def get_all_keys(self):
        return self.client.keys()

    def delete(self, keys):
        num = 0
        for key in keys:
            num += self.client.delete(key)
        return num


class MaxCompute(object):
    def __init__(self, db_param, project='columbus'):
        super().__init__()
        self.param = db_param
        self.access_id = self.param['access_id']
        self.key = self.param['key']
        self.endpoint = self.param['endpoint']
        self.project = project
        self.client = ODPS(self.access_id, self.key,
                           project=self.project, endpoint=self.endpoint)

    def query(self, sql):
        with self.client.execute_sql(sql).open_reader() as reader:
            res = list(reader)

        return res

    def run_sql(self, sql):
        return self.client.run_sql(sql)

    def write_table(self, table_name, row_data, partition, create_partition=True):
        return self.client.write_table(table_name, row_data, partition, create_partition=create_partition)

    @timeit_no_res
    def execute_sql(self, sql):
        instance = self.client.run_sql(sql)
        logger.info("instance: %s", instance)
        logger.info("task name: %s", instance.get_task_names())
        logger.info("logview: %s", instance.get_logview_address())
        instance.wait_for_success()
        return instance

    def get_event(self, n, event, ed=None, table=None, platform=None, limit=None, date_form='%Y%m%d%H', split_n=24):
        if ed is None:
            ed_ts = datetime.datetime.now() - datetime.timedelta(seconds=3600)
        else:
            ed_ts = datetime.datetime.strptime(ed, date_form)
        st_ts = ed_ts - datetime.timedelta(seconds=3600 * n)

        if n > split_n:
            arr = list(range(0, n, split_n))
            if n not in arr:
                arr.append(n)
        else:
            arr = [0, n]
        for _st_i, _ed_i in zip(arr[:-1], arr[1:]):
            _ed = (st_ts + datetime.timedelta(seconds=3600 * _ed_i)).strftime(date_form)
            _st = (st_ts + datetime.timedelta(seconds=3600 * _st_i)).strftime(date_form)
            if table is None:
                unzip_data = True
                table = 'dwd_log_user_event_hour_inc'
            else:
                unzip_data = False
            sql = """
                select * from {}
                where pt >= '{}' and pt < '{}' and uid is not null
                and type = 'cstm' and event='{}'
            """.format(table, _st, _ed, event)
            if platform is not None:
                if platform == 'mobile':
                    sql += " and platform in ('Android', 'iOS')"
                elif platform == 'pc':
                    sql += " and platform='web'"
                else:
                    sql += " and platform='{}'".format(platform)
            if limit is not None:
                sql += ' limit {}'.format(limit)
            print(sql)
            with self.execute_sql(sql).open_reader() as reader:
                df = reader.to_pandas()
                if unzip_data:
                    data_df = df.data.apply(lambda x: pd.Series(json.loads(x)))
                    df = pd.concat([df, data_df], axis=1)
                    df = df[list(set(df.columns) - {'data'})]
                if df is not None and len(df) > 0:
                    yield df
