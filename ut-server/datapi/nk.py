# -*- coding: utf-8 -*-
"""
fetch
"""
import random
import pandas as pd
from collections import defaultdict
from conf import settings
from .env import *
from .file import *
from .db import is_null
from .dt import *
from .batch import batch_list
from . import instance

__author__ = 'jx'


def all_logs():
    """服务器日志路径"""
    pc_dir_list = [os.path.join('/mnt/logs', p) for p in os.listdir('/mnt/logs') if
                   p.startswith('s') and p[1:].isdigit()]
    mobile_dir_list = [os.path.join('/mnt/logs/mobile', p) for p in os.listdir('/mnt/logs/mobile') if
                       p.startswith('s') and p[1:].isdigit()]
    return pc_dir_list + mobile_dir_list


LOG_DIR_PATH = all_logs() if settings['env'] not in ["dev", "local"] else [os.path.join(g_user_root, 'web_context', 'logs')]

"""big_statistic.log文件起始时间"""
LOG_BIG_STATIC_START_DATE = '2019-08-01'


class LogFetch(object):
    """flow 大big static log日志"""

    def get_log_files(self, days=None, log_name=None):
        """时间上从前往后的顺序返回用户行为日志"""
        log_name = 'big_statistic.log' if log_name is None else log_name
        log_dot_name = log_name + '.'

        if days is None or len(days) == 0:
            days = between_days(LOG_BIG_STATIC_START_DATE, today(), including_end=True)

        days = sorted(days)
        alive_log = False
        if days[-1][:10] == today():
            alive_log = True
            days = days[:-1]

        files = [os.path.join(log_dir, '{}{}'.format(log_dot_name, date_str[:10])) for date_str in days for log_dir in
                 LOG_DIR_PATH]
        if alive_log:
            files.extend([os.path.join(log_dir, log_name) for log_dir in LOG_DIR_PATH])
        return files

    def flow(self, filter_func, result_func, start=None, end=None, days=None, ends=None, log_name=None):
        """
        登录用户浏览帖子   x[2] != '0' 登录用户
            filter_func=lambda x: x[5] == 'discussTerminal' and x[4] == 'visit' and x[2] != '0' and x[
                    7] in ends
            result_func=lambda x: [x[0][1:20], int(x[2]), int(x[6].split('&')[0])] # time, user_id, discuss_id


        :param filter_func: 过滤函数 e.g.  lambda x: x[1] and x[2] != 0
        :param result_func: 返回值函数 e.g.  lambda x: [ x[1] ,x[2].strip()]
        :param start:
        :param end:
        :param days:
        :param ends: log种类
        :param log_name: ???
        :return:
        """
        if (start is not None and len(start) not in (10, 19)) or (end is not None and len(end) not in (10, 19)):
            raise TypeError('TIME FORMAT should be 2020-04-01 or 2020-04-01 20:03:02')

        if start is not None and end is not None:
            days = between_days(start, end, including_end=True)
        elif start is None and end is not None:
            days = between_days(LOG_BIG_STATIC_START_DATE, end, including_end=True)
        elif end is None and start is not None:
            days = between_days(start, today(), including_end=True)

        start_check = lambda x: True
        end_check = lambda x: True
        if start is not None:
            if len(start) == 10:
                start_check = lambda x: x[1:11] >= start
            else:
                start_check = lambda _x: _x[1:20] >= start
        if end is not None:
            if len(start) == 10:
                end_check = lambda x: x[1:11] <= end
            else:
                end_check = lambda _x: _x[1:20] < end

        big_logs = self.get_log_files(days, log_name=log_name)
        for log in big_logs:
            if not is_data_file_ok(log):
                print('missing {} file for {}!'.format('big_statistic log' if log_name is None else log_name, log))
                continue

            # 不需要过滤pc的log
            if ends is not None and 'pc' not in ends and not log.__contains__('mobile'):
                continue

            # 不需要过滤mobile的log
            if ends is not None and ('ios' not in ends and 'android' not in ends) and log.__contains__('mobile'):
                continue

            with open(log) as r:
                for li in r:
                    if not li.strip():
                        continue
                    items = li.rstrip('\n').split('\t')
                    try:
                        if filter_func(items) and len(items[0].strip()) > 20 and start_check(items[0]) and end_check(
                                items[0]):
                            res = result_func(items)
                            if res:
                                yield res
                    except Exception as _:
                        pass


class BatchConfigTable(object):
    def gets(self, keys):
        data = {k: 0 for k in keys}
        with instance.read_mysql_db('recommend') as rec_db:
            for r in rec_db.query('select k,v from global_batch_config where k in ({})'.format(
                    ','.join(map(lambda x: '"{}"'.format(x), keys)))):
                data[r['k']] = r['v']

        return data

    def get(self, k, default=0):
        with instance.read_mysql_db('recommend') as rec_db:
            data = rec_db.query(
                'select k,v from global_batch_config where k="{}"'.format(k))
            if data:
                res = list(data)[0]['v']
                if res:
                    return res
        return default

    def set(self, config_dict):
        with instance.write_mysql_db('recommend') as rec_db:
            rec_db.insert_or_update('global_batch_config', ['k', 'v'], ((k, v) for k, v in six.iteritems(config_dict)))

    def update_diff(self, old_dict, new_dict):
        diff_dict = {k: v for k, v in six.iteritems(new_dict) if v != old_dict.get(k)}
        if len(diff_dict) > 0:
            self.set(diff_dict)


# def tag2name_dict():
#     def _load_from_db():
#         with instance.read_mirror_db() as online_db:
#             return {r['id']: r['name'] for r in online_db.query('select id,name from wenyibi_online.question_tag')}
#
#     from embapi import emb_env
#
#     fn = os.path.join(emb_env.g_global_root, 'tag', 'tag2name.pik')
#     if random.random() > .01 and os.path.exists(fn):
#         return load_pickle(fn)
#     else:
#         data = _load_from_db()
#         dump_pickle(data, fn)
#         return data


# def tag2word_dict():
#     def _proc_name(emb, s):
#         if not s:
#             return
#         s = str(s).lower()
#         if not emb.ann.has_item(s):
#
#             _top_s = list(jieba.cut(str(s)))
#             for _s in _top_s:
#                 if emb.ann.has_item(_s):
#                     return _s
#         else:
#             return s
#
#     def _load_from_db():
#         from embapi import embedding
#         emb = embedding.WordAnn()
#         with instance.read_mirror_db() as online_db:
#             d = {r['id']: _proc_name(emb, r['name']) for r in
#                  online_db.query('select id,name from wenyibi_online.question_tag')}
#             return {k: v for k, v in six.iteritems(d) if v}
#
#     from embapi import emb_env
#     import jieba
#
#     fn = os.path.join(emb_env.g_global_root, 'tag', 'tag2word.pik')
#     if random.random() > .001 and os.path.exists(fn):
#         return load_pickle(fn)
#     else:
#         data = _load_from_db()
#         dump_pickle(data, fn)
#         return data


# def parent2ids_dict():
#     def _load_from_db():
#         parent2id = defaultdict(list)
#         with instance.read_mirror_db() as online_db:
#             for r in online_db.query('select id,parent_id from wenyibi_online.question_tag'):
#                 parent2id[r['parent_id']].append(r['id'])
#         return parent2id
#
#     from embapi import emb_env
#
#     fn = os.path.join(emb_env.g_global_root, 'tag', 'parent2ids.pik')
#     if random.random() > .01 and os.path.exists(fn):
#         return load_pickle(fn)
#     else:
#         data = _load_from_db()
#         dump_pickle(data, fn)
#         return data


def job_tag2name_dict():
    with instance.read_mirror_db() as online_db:
        return {r['id']: r['name'] for r in
                online_db.query('select id,name from wenyibi_online.question_tag where parent_id=638 and id<4643')}


def career_tag2name_dict():
    with instance.read_mirror_db() as online_db:
        return {r['id']: r['name'] for r in
                online_db.query('select id,name from wenyibi_online.question_tag where parent_id=300')}


def job2big_dict(check=False):
    d = {
        # 技术（软件）/信息技术类
        4643: [4643, 639, 640, 649, 2656, 644, 642, 641, 645, 733, 4367, 643, 682, 894, 684, 1194, 4368, 2678, 680],
        # 技术（硬件）/电子信息类
        4644: [4644, 2672, 2671, 2675, 2655],
        # 机械/汽车制造类
        4645: [4645, 4369, 4370, 4371, 4372, 4373, 4374, 4375, 4376],
        # 产品/运营/游戏策划/设计类
        4646: [4646, 891, 892, 976, 1636],
        # 财务财会类/经济学类/金融学类
        4647: [4647, 4377, 4378, 4379, 4380, 2661, 4382, 4383],
        # 市场营销类
        4648: [4648, 4384, 4385, 2665, 4386, 1676, 4387, 4388, 4389, 4390, 4391, 4392, 4393, 4394, 4557],
        # 管理类
        4649: [4649, 4395, 4396, 4397],
        # 职能类
        4650: [4650, 2664, 4398, 4399, 4558],
    }

    ex_d = {
        4643: [683, 1635, 2673, 2674, 2676, 2677],
        4644: [2668],
        4645: [],
        4646: [2681],
        4647: [],
        4648: [2657, 2658, 2669],
        4649: [2663, 2667],
        4650: [1634, 2659, 2660, 2662, 2666, 2670],

    }
    for k, v in ex_d.items():
        d[k].extend(v)

    if check:
        with instance.read_mirror_db() as wyb_db:
            sql = 'select id from wenyibi_online.question_tag where id<4643 and parent_id=638'
            jobs = {r['id'] for r in wyb_db.query(sql)}
            miss = jobs - set(d.keys())
            if len(miss) > 0:
                print('missing {}'.format(miss))

    return {i: k for k, v in six.iteritems(d) for i in v}


def company2name_dict():
    with instance.read_mirror_db() as wyb_db:
        return {r['company_id']: r['name'] for r in
                wyb_db.query('select company_id,name from wenyibi_online.company')}


def name2company_dict():
    with instance.read_mirror_db() as wyb_db:
        name2company = {}
        for r in wyb_db.query('select company_id,name,other_names from wenyibi_online.company'):
            if r['name']:
                name = r['name'].strip()
                if name and name not in name2company:
                    name2company[name] = r['company_id']
            if r['other_names']:
                for name in str(r['other_names']).split(','):
                    if name and name not in name2company:
                        name2company[name] = r['company_id']
        return name2company


def big2name_dict():
    with instance.read_mirror_db() as wyb_db:
        return {r['id']: r['name'] for r in
                wyb_db.query('select id,name from wenyibi_online.question_tag where parent_id=638 and id>=4643')}


def describe_user(ids, batch_size=5000):
    # def _t2name(x):
    #     if x:
    #         names = [tag2name[int(_s)] for _s in str(x).split(',') if _s.isdigit() and int(_s) in tag2name]
    #         if len(names) > 0:
    #             return ','.join(names)

    def _t2big(x):
        if x:
            for _s in str(x).split(','):
                if _s.isdigit() and int(_s) in job2big:
                    return job2big[int(_s)]

    # tag2name = tag2name_dict()

    sql_form = """
            select fea.id,fea.channel_seed,bas.nickname,bas.gender,bas.work_info,bas.education_info,bas.live_place,adi.work_time,
            adi.edu_level,adi.career_job,adi.work_want_place,adi.job,adi.major,fea.seq_update_time,fea.register_time
            from (select * from recommend_online.user_feature where id in ({})) fea 
            inner join wenyibi_online.user_basic_info bas on fea.id=bas.id
            inner join wenyibi_online.user_addition_info adi on fea.id=adi.user_id
            """.strip().replace('\n', '').replace('\t', '')

    df_list = []
    job2big = job2big_dict()
    big2name = big2name_dict()
    with instance.read_mirror_db() as ai_db:
        for b in batch_list(list(ids), batch_size):
            df = pd.DataFrame(ai_db.query(sql_form.format(','.join(map(str, b)))))
            # df['job_name'] = df.job.apply(_t2name)
            # df['career_name'] = df.career_job.apply(_t2name)
            df['big'] = df.job.apply(_t2big)
            df['big_name'] = df.big.apply(lambda x: big2name[x] if not is_null(x) else None)
            df_list.append(df)
    if len(df_list) > 0:
        res = pd.concat(df_list).set_index('id')
        # noinspection PyUnresolvedReferences
        res = res[~res.index.duplicated(keep='first')]
        # noinspection PyTypeChecker
        res_inds = set(res.index)
        ids = [i for i in list(ids) if i in res_inds]
        res = res[~res.index.duplicated(keep='first')]
        # noinspection PyUnresolvedReferences
        return res.reindex(ids)


def describe_question(ids, batch_size=5000):
    sql_form = 'select id,type,title,content from question where id in ({})'

    df_list = []
    with instance.read_mirror_db() as wyb_db:
        for b in batch_list(list(ids), batch_size):
            df = pd.DataFrame(wyb_db.query(sql_form.format(','.join(map(str, b)))))
            df_list.append(df)

    if len(df_list) > 0:
        res = pd.concat(df_list).set_index('id')
        # noinspection PyTypeChecker
        res_inds = set(res.index)
        ids = [i for i in list(ids) if i in res_inds]
        # noinspection PyUnresolvedReferences
        return res.reindex(ids)


def describe_discuss(ids, batch_size=5000):
    sql_form = """
            select fea.id,pos.type,pos.view_cnt,pos.comment_cnt,fea.like_cnt,fea.follow_cnt,fea.uc_cnt,fea.content_len,
            fea.ugc_cnt,pos.hot_value,fea.keyword,pos.title,pos.content,fea.ugc_last_time,pos.create_time,pos.update_time
            from (select * from recommend_online.discuss_feature where id in ({})) fea 
            inner join wenyibi_online.discuss_post pos on fea.id=pos.id
            """.strip().replace('\n', '').replace('\t', '')

    df_list = []
    with instance.read_mirror_db() as ai_db:
        for b in batch_list(list(ids), batch_size):
            df = pd.DataFrame(ai_db.query(sql_form.format(','.join(map(str, b)))))
            df_list.append(df)

    if len(df_list) > 0:
        res = pd.concat(df_list).set_index('id')
        # noinspection PyTypeChecker
        res_inds = set(res.index)
        ids = [i for i in list(ids) if i in res_inds]
        # noinspection PyUnresolvedReferences
        return res.reindex(ids)


def describe_moment(ids):
    sql_form = """
               select fea.id,m.type,fea.like_cnt,fea.comment_cnt,fea.uc_cnt,fea.ugc_cnt,fea.keyword,m.content,fea.ugc_last_time,m.created_at, m.circle
               from (select * from recommend_online.moment_feature where id in ({})) fea 
               inner join wenyibi_online.moments m on fea.id=m.id
               """.strip().replace('\n', '').replace('\t', '')
    with instance.read_mirror_db() as ai_db:
        res = pd.DataFrame(ai_db.query(sql_form.format(','.join(map(str, ids))))).set_index('id')
        # noinspection PyTypeChecker
        res_inds = set(res.index)
        ids = [i for i in list(ids) if i in res_inds]
        # noinspection PyUnresolvedReferences
        return res.reindex(ids)


def describe_job(ids):
    sql_form = """
    select id,recommand_company_id,job_name,job_city,update_time from hr_online.recommand_job where id in ({})
    """
    company2name = company2name_dict()
    with instance.read_mirror_db() as ai_db:
        res = pd.DataFrame(ai_db.query(sql_form.format(','.join(map(str, ids))))).set_index('id')
        # noinspection PyUnresolvedReferences,SpellCheckingInspection,PyTypeChecker
        res['company_name'] = res['recommand_company_id'].apply(lambda x: company2name.get(x))
        # noinspection PyTypeChecker
        res_inds = set(res.index)
        ids = [i for i in list(ids) if i in res_inds]
        # noinspection PyUnresolvedReferences
        return res.reindex(ids)


def describe_boss_job(ids):
    _edu_map = {
        0: '不要求',
        1000: '小学',
        2000: '初中',
        3000: '高中',
        4000: '专科',
        5000: '本科',
        5500: '双学位',
        6000: '硕士',
        7000: '博士',
        8000: '博士后',
    }
    _cmp_scale = {
        0: '未知',
        1: '0-20人',
        2: '20-99人',
        3: '100-499人',
        4: '500-999人',
        5: '1000-9999人',
        6:'10000人以上',
    }

    def _tag_indus(x):
        arr = []
        tids = set()
        if x['company_tags'] is not None:
            for t in str(x['company_tags']).split(','):
                if int(t) in tid2indus:
                    tids.add(int(t))
                    arr.append(tid2indus[int(t)])

        if x['industry_id'] is not None and int(x['industry_id']) in tid2indus and int(
                x['industry_id']) not in tids:
            arr.append(tid2indus[int(x['industry_id'])])
        if len(arr) > 0:
            return ','.join(arr[:2])

    def _tag_abc(x):
        if x is not None:
            for t in str(x).split(','):
                if int(t) in tid2abc:
                    return tid2abc[int(t)]

    def _tag_ctype(x):
        if x is not None:
            for t in str(x).split(','):
                if int(t) in tid2ctype:
                    return tid2ctype[int(t)]

    def _salary_year(x):
        if x['salary_min'] == 0 or x['salary_max'] == 9999999:
            return

        if x['salary_type'] == 2:
            # 月薪
            s_mon = x['salary_month'] if x['salary_month'] > 0 else 12
            return x['salary_min'] * s_mon
        elif x['salary_type'] == 1:
            # 日薪
            return x['salary_min'] * 12 / 1000

    def _salary_des(x):
        if x['salary_min'] == 0 or x['salary_max'] == 9999999:
            return '面议'
        s_mon = x['salary_month'] if x['salary_month'] > 0 else 12
        if x['salary_type'] == 2:
            # 月薪
            return '{}K-{}K * {}'.format(x['salary_min'], x['salary_max'], s_mon)
        elif x['salary_type'] == 1:
            # 日薪
            return '{}-{} 日薪 '.format(x['salary_min'] , x['salary_max'] )

    def _avg_process_des(x):
        des = ''
        if 0 < x['avg_process_rate'] <= 100:
            des += 'hr反馈率: {}%'.format(x['avg_process_rate'])
        if 0 < x['avg_process_day'] < 999999:
            if des != '':
                des += ' | '
            des += 'hr反馈时长: {}天'.format(x['avg_process_day'])
        return des



    sql_form = """
    select brj.id,brj.boss_uid,brj.recruit_type,brj.job_city,brj.company_id,brj.edu_level,brj.job_name,brj.create_time,
        brj.salary_type,brj.salary_min,brj.salary_max,brj.salary_month,buo.last_online_time,brj.refresh_time,brj.latest_process_time,
        bu.avg_process_rate,bu.avg_process_sec,bu.avg_process_day,bccar.company_scales,cmp.name as company_name,cmp.tags as company_tags,
        bccar.industry_id

    from (select * from boss_online.boss_recommend_job where id in ({})) brj 
    left join boss_online.boss_user_online buo on brj.boss_uid=buo.boss_uid
    left join boss_online.boss_user bu on brj.boss_uid=bu.id
    left join boss_online.boss_company_cert_audit_record bccar on brj.company_id=bccar.company_id
    left join wenyibi_online.company cmp on brj.company_id=cmp.company_id
    """
    sql = sql_form.format(','.join(map(str, ids)))
    with instance.read_mirror_db() as odb:
        tid2abc = {r['id']: r['name'] for r in odb.query(
            'select id,name from wenyibi_online.question_tag where parent_id=2818')}
        tid2indus = {r['id']: r['name'] for r in odb.query(
            'select id,name from wenyibi_online.question_tag where parent_id=2819')}
        tid2ctype = {r['id']: r['name'] for r in odb.query(
            'select id,name from wenyibi_online.question_tag where parent_id=4711')}

        df = pd.DataFrame(odb.query(sql))
        if len(df) > 0:
            # noinspection PyUnresolvedReferences
            df = df.set_index('id').drop_duplicates(keep='first')
            # index去重
            df = df[~df.index.duplicated(keep='first')]
            df = df.where(pd.notnull(df), None)
            df['industry_name'] = df.apply(_tag_indus, axis=1)
            df['company_abc'] = df.company_tags.apply(_tag_abc)
            df['company_type'] = df.company_tags.apply(_tag_ctype)
            df['edu_des'] = df.edu_level.apply(lambda x: _edu_map.get(x))
            df['salary_year'] = df.apply(_salary_year, axis=1)
            df['salary_des'] = df.apply(_salary_des, axis=1)
            df['hr_process_des'] = df.apply(_avg_process_des, axis=1)
            df['company_scale_des'] = df.company_scales.apply(lambda x: _cmp_scale.get(x))
            df = df.where(pd.notnull(df), None)
            res_inds = set(df.index)
            ids = [i for i in list(ids) if i in res_inds]
            df = df[~df.index.duplicated(keep='first')]
            return df.reindex(ids)


def gen_seed(n_job, uids=None, max_search=100000, start_time=None):
    jobs = list(job_tag2name_dict().keys())
    job2cnt = {j: 0 for j in jobs}
    if start_time is None:
        start_time = before_n_hours(1)

    select_uids = set() if uids is None else set(uids)
    with instance.read_mirror_db() as ai_db:
        sql_form = """
                       select fea.id,adi.job,fea.seq_update_time
                       from (select id,seq_update_time from recommend_online.user_feature where seq_update_time<"{batch_id}" order by seq_update_time desc limit {batch_size}) fea 
                       inner join wenyibi_online.user_addition_info adi on fea.id=adi.user_id
                       """.strip().replace('\n', '').replace('\t', '')

        b_cnt = 0
        batch_size = 5000
        for b in ai_db.query_on_batch(sql_form, 'seq_update_time', start_time, batch_size):
            b_cnt += 1
            for r in b:
                if r['id'] in select_uids or not r['job'] or str(r['job']).count(',') > 3:
                    continue
                for j_str in str(r['job']).split(','):
                    if j_str.isdigit() and job2cnt.get(int(j_str), n_job + 1) < n_job:
                        select_uids.add(r['id'])
                        job2cnt[int(j_str)] += 1

            done = True
            if b_cnt * batch_size < max_search:
                for v in six.itervalues(job2cnt):
                    if v < n_job:
                        done = False
                        break
            if done:
                break
    return select_uids

#
# def define_word():
#     from embapi import emb_env
#     words = set()
#
#     fn = os.path.join(emb_env.g_emb_root, 'lib/define_word/nk_words.txt')
#     if is_data_file_ok(fn):
#         with open(fn) as r:
#             for line in r:
#                 if line.strip():
#                     words.add(line.strip())
#     return words
#
#
# def stop_word():
#     from embapi import emb_env
#     words = set()
#
#     fn = os.path.join(emb_env.g_emb_root, 'lib/stop_word/nk_words.txt')
#     if is_data_file_ok(fn):
#
#         with open(fn) as r:
#             for line in r:
#                 if line.strip():
#                     words.add(line.strip())
#     return words


def sync_word():
    import embedding_api.embapi.core.env as emb_env
    w2w = dict()

    fn = os.path.join(emb_env.g_emb_root, 'lib/sync_word/nk_words.txt')
    if is_data_file_ok(fn):

        with open(fn) as r:
            for line in r:
                try:
                    a, b = line.strip().split('\t')
                    w2w[a.strip()] = b.strip()
                except:
                    pass
    return w2w
#
#
# def all_word():
#     from embapi import emb_env
#     fn = os.path.join(emb_env.g_emb_root, 'lib/tq/all_words.pik')
#     return load_pickle(fn)


def find_ann(entity_name, ann_name):
    import embedding_api.embapi.core.env as emb_env
    from .db import AnnDb
    return AnnDb(os.path.join(emb_env.g_emb_root, entity_name, ann_name))
