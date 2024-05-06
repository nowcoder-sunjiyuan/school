import os
import os.path as osp
import socket
import sys
import threading
import time

import oss2

from conf import settings
from datapi import instance
from utils import logger
from utils.file_util import ensure_dir
from utils.logger_helper import alarm_algorithm
from utils.singleton import Singleton


@Singleton
class OSSUtil:
    def __init__(self):
        endpoint = settings['oss']['endpoint']
        accessKeyID = settings['oss']['accessKeyID']
        accessKeySecret = settings['oss']['accessKeySecret']

        auth = oss2.Auth(accessKeyID, accessKeySecret)
        self.bucket = oss2.Bucket(auth, endpoint, 'caesar-model')

    def get_latest_model_path(self, model_path):
        dirs = self.get_matching_dirs(model_path, isdigit=True)
        newest_dir = self.get_local_model_path(dirs[-1])
        logger.info('load latest model from %s', newest_dir)
        return newest_dir

    def split_bucket_key(self, model_path):
        """
        规范化模型路径, 支持 oss path, 即以 oss:// 打头; 或者简化的 oss key
        """
        model_path = model_path.strip('/')
        if not model_path.startswith('oss://'):
            return 'caesar-model', model_path
        pieces = model_path.split('/')
        bucket_name = pieces[2]
        key_name = '/'.join(pieces[3:])
        return bucket_name, key_name

    def convert_to_local_path(self, file_path, root):
        _, key_name = self.split_bucket_key(file_path)
        return osp.join(root, key_name)

    def get_local_model_path(self, model_path, root='/home/web/sunjiyuan/models'):
        files = self.get_matching_keys(model_path)
        for file_path in files:
            if file_path.endswith('/'):
                continue
            local_path = self.convert_to_local_path(file_path, root)
            if not osp.exists(local_path):
                ensure_dir(local_path)
                logger.info('download: %s => %s', file_path, local_path)
                self.bucket.get_object_to_file(file_path, local_path, progress_callback=self.percentage)
        return self.convert_to_local_path(model_path, root)

    def get_matching_keys(self, model_path, max_keys=100):
        _, key_name = self.split_bucket_key(model_path)
        return [obj.key for obj in self.bucket.list_objects(prefix=key_name, max_keys=max_keys).object_list]

    def get_matching_dirs(self, model_path, isdigit=False, max_keys=100):
        """
        严格匹配以 model_path 为前缀的目录, 并按升序排列
        """
        keys = self.get_matching_keys(model_path, max_keys=max_keys)
        _, key_name = self.split_bucket_key(model_path)
        start_idx = len(key_name)
        # 若 key_name 不为空字符串, 则严格过滤出 key_name/ 打头的 keys
        if key_name:
            prefix = f'{key_name}/'
            keys = [key for key in keys if key.startswith(prefix)]
            start_idx = len(prefix)
        # 获取真实的目录
        rows = [key[start_idx:].split('/') for key in keys]
        dirs = [row[0] for row in rows if len(row) > 1]
        dirs = [osp.join(key_name, d) for d in set(dirs) if d.isdigit() or not isdigit]
        dirs.sort(key=lambda x: (len(x), x))
        return dirs

    def percentage(self, consumed_bytes, total_bytes):
        if total_bytes:
            rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
            print('\r{0}% '.format(rate), end='')

            sys.stdout.flush()

    def download(self, file_path, target_directory="/data", keep_dir=True):
        for object in self.bucket.list_objects(file_path).object_list:
            object_name = object.key
            if object_name.endswith("/"):
                continue
            if keep_dir:
                target_path = osp.join(target_directory, object_name.strip("/"))
            else:
                target_path = osp.join(target_directory, object_name.split("/")[-1])
            if not osp.exists(target_path):
                ensure_dir(target_path)
                logger.info('%s => %s', object_name, target_path)
                self.bucket.get_object_to_file(object_name, target_path, progress_callback=self.percentage)

    def upload(self, latest_model_path, local_path):
        _, oss_dir = self.split_bucket_key(latest_model_path)
        pieces = oss_dir.split('/')
        if len(pieces) < 2 or not pieces[-1].isdigit():
            logger.error('latest_model_path 必须形如 model_path/digit_version')
            return
        model_path = '/'.join(pieces[:-1])
        self.delete_oldest_dir(model_path, keep=7)
        local_path = osp.abspath(local_path)
        logger.info('uploading %s', local_path)
        if osp.isdir(local_path):
            for root, dirs, files in os.walk(local_path):
                for f in files:
                    file_path = osp.join(root, f)
                    relative_path = file_path[len(local_path):].strip('/')
                    key = osp.join(oss_dir, relative_path)
                    logger.info('upload: %s => %s', file_path, key)
                    self.bucket.put_object_from_file(key, file_path, progress_callback=self.percentage)
        else:
            file_name = local_path.split('/')[-1]
            key = osp.join(oss_dir, file_name)
            logger.info('upload: %s => %s', local_path, key)
            self.bucket.put_object_from_file(key, local_path, progress_callback=self.percentage)

    def delete_oldest_dir(self, model_path, keep=5):
        # 过滤出仅仅是数字版本号的 dir
        dirs = self.get_matching_dirs(model_path, isdigit=True)
        if len(dirs) <= keep:
            return
        dirs = dirs[:-keep]
        for dir in dirs:
            logger.info('delete dir: %s', dir)
            keys = self.get_matching_keys(dir)
            if not keys:
                continue
            self.bucket.batch_delete_objects(key_list=keys)

    def reset_external(self):
        """
        供 monster 使用, 接不上内网所以走外网
        """
        auth = oss2.Auth(settings['oss']['accessKeyID'], settings['oss']['accessKeySecret'])
        self.bucket = oss2.Bucket(auth, settings['oss']['external_endpoint'], 'caesar-model')


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]


class HotOssDir:

    def __init__(self, path, callback=None):
        self.oss_util = OSSUtil.Instance()
        self.path = path
        dirs = self.oss_util.get_matching_dirs(self.path)
        self.latest_dir = dirs[-1]
        self.ip = get_ip()
        self.callback = callback
        local_path = self.download()
        self.callback(local_path)
        self.update_thread = threading.Thread(target=self._check_update)
        self.update_thread.start()

    def download(self):
        return self.oss_util.get_local_model_path(self.latest_dir)

    def _check_update(self):
        while True:
            time.sleep(60)
            try:
                dirs = self.oss_util.get_matching_dirs(self.path)
            except Exception as e:
                continue
            dirs.sort(key=lambda x: (len(x), x))
            if self.latest_dir != dirs[-1]:
                self.latest_dir = dirs[-1]
                try:
                    path = self.download()
                except Exception as e:
                    alarm_algorithm("下载模型%s失败, %s" % (self.path, self.ip))
                    continue
                self.callback(path)


class ProcessHotOssDir:

    def __init__(self, path, callback=None, passive=False):
        self.oss_util = OSSUtil.Instance()
        self.path = path
        dirs = self.oss_util.get_matching_dirs(self.path)
        self.latest_dir = dirs[-1]
        self.ip = get_ip()
        self.callback = callback
        local_path = self.download()
        self.callback(local_path)
        self.is_old = False
        self.update_thread = threading.Thread(target=self._check_update)
        if not passive:
            self.update_thread.start()

    def download(self):
        redis_client = instance.write_redis(is_pool=True)
        redis_key = "%s#%s" % (self.ip, self.latest_dir)
        # 分布式锁
        while True:
            if redis_client.client.setnx(redis_key, time.time()):
                break
            value = redis_client.get(redis_key)
            # 三分钟肯定拷贝完了
            if value is not None and time.time() - float(value) > 180:
                redis_client.client.delete(redis_key)
                print("some process not release %s lock!!!" % redis_key)
            time.sleep(30)
        # 先获取锁，再判读是否存在
        local_path = self.oss_util.get_local_model_path(self.latest_dir)
        redis_client.client.delete(redis_key)
        return local_path

    def _check_update(self):
        while True:
            time.sleep(60)
            self.check_update()

    def check_update(self):
        try:
            dirs = self.oss_util.get_matching_dirs(self.path)
        except Exception as e:
            print(time.time(), "get oss directory %s info error: %s" % (self.path, e))
            return
        dirs.sort(key=lambda x: (len(x), x))
        if self.latest_dir != dirs[-1]:
            self.latest_dir = dirs[-1]
            self.is_old = True

    def load(self):
        for i in range(3):
            try:
                path = self.download()
                break
            except Exception as e:
                alarm_algorithm("下载模型%s失败" % self.path)
                continue
        self.callback(path)
        self.is_old = False


# 通过数据库更新版本
class HotOssModel:

    def __init__(self, name, callback=None):
        self.oss_util = OSSUtil.Instance()
        self.name = name
        self.model_info = self.get_model_info()
        self.latest_dir = ""
        self.callback = callback
        self.callback(self.oss_util.get_latest_model_path(self.model_info["path"]))
        self.update_thread = threading.Thread(target=self._check_update)
        self.update_thread.start()

    def get_model_info(self):
        with instance.read_mysql_db("recommend") as db_client:  # env="online"
            res = db_client.query("select * from model_config where name = '%s'" % self.name)
            for r in res:
                return r

    def _check_update(self):
        while True:
            time.sleep(60)
            model_info = self.get_model_info()
            if model_info.version != self.model_info.version:
                self.model_info = model_info
                self.callback(self.oss_util.get_local_model_path(model_info["path"]))


if __name__ == '__main__':
    inst = OSSUtil.Instance()
    dirs = inst.get_matching_dirs('discuss_post_classification', isdigit=True)
    [print(d) for d in dirs]
    inst.get_latest_model_path("discuss_post_classification")
    print(inst.get_local_model_path('oss://caesar-model/discuss_post_classification/20210925115401/test.txt'))

    # 扫描各个模型的版本数量
    models = inst.get_matching_dirs('oss://caesar-model', max_keys=1000)
    for model in models:
        versions = len(inst.get_matching_dirs(model, isdigit=True))
        if versions > 5:
            inst.delete_oldest_dir(model, keep=7)
            print((versions, model))
