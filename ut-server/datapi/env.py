# -*- coding: utf-8 -*-
"""
环境
"""

import os
import six

__author__ = 'jx'

g_is_py3 = six.PY3

try:
    # noinspection PyUnresolvedReferences
    import psutil

    """有psutil，使用psutil.cpu_count计算cpu个数"""
    g_cpu_cnt = psutil.cpu_count(logical=True) * 1
except ImportError:
    if g_is_py3:
        # noinspection PyUnresolvedReferences
        g_cpu_cnt = os.cpu_count() * 1
    else:
        import multiprocessing as mp

        g_cpu_cnt = mp.cpu_count()
except Exception:
    # 获取cpu个数失败，默认4个
    g_cpu_cnt = 4

g_user_root = os.path.expanduser('~')
g_local_rsa = os.path.join(g_user_root, '.ssh/id_rsa')
g_cache_root = os.path.join(g_user_root, 'datapi_cache')

"""工程目录"""
g_project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir))

"""
    NK_STATISTIC 牛客统计数据库的
    NK_AI NK_AI_ONLINE 离线AI数据库
    NK_EMAIL_ROBOT 邮件配置
"""
