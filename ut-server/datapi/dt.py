# -*- coding: utf-8 -*-
"""
"""

__author__ = 'jx'

from datetime import timedelta, datetime, date
import time

g_time_format = '%Y-%m-%d %H:%M:%S'
g_date_format = '%Y-%m-%d'


def timeit(func):
    def wraps(*args, **kwargs):
        print("timeit>>> start function {} at {}".format(func.__name__, str(datetime.now())))
        result = func(*args, **kwargs)
        print("timeit>>> end function {} at {}".format(func.__name__, str(datetime.now())))
        return result

    return wraps


def range_day(n, date_str=None, rev=False):
    """
    获得前N天，只支持%Y-%m-%d格式
    :param n:
    :param date_str: None以当前时间为准
    :param rev: 倒序
    :return:
    """
    if date_str is None:
        date_ts = date.today()
    else:
        date_ts = datetime.strptime(date_str[:10], '%Y-%m-%d')

    return [str(date_ts - timedelta(days=i))[:10] for i in range(n)] if rev else \
        [str(date_ts - timedelta(days=n - 1 - i))[:10] for i in range(n)]


def point_last_n_hour(n, end_date_str=None, form='str'):
    """
    获得前N小时的整点小时，只支持%Y-%m-%d %H:%M:%S格式
    :param n:
    :param end_date_str: None以当前时间为准
    :param form: str or ts
    :return: start, end
    """

    if end_date_str is None:
        end_dt = datetime.strptime(now()[:14] + '00:00', '%Y-%m-%d %H:%M:%S')
    else:
        end_dt = datetime.strptime(end_date_str[:14] + '00:00', '%Y-%m-%d %H:%M:%S')

    if form == 'str':
        return str(end_dt - timedelta(hours=n)), str(end_dt)
    elif form == 'ts':
        return int((end_dt - timedelta(hours=n)).timestamp()), int(end_dt.timestamp())
    else:
        raise TypeError('Unsupported form {}'.format(form))


def point_last_n_second(n, end_hour_str=None, form='str'):
    """
    获得前N秒，只支持%Y-%m-%d %H:%M:%S格式
    :param n:
    :param end_hour_str: None以当前时间为准
    :param form: str or ts
    :return: start, end
    """

    if end_hour_str is None:
        end_dt = datetime.now()
    else:
        end_dt = datetime.strptime(end_hour_str, '%Y-%m-%d %H:%M:%S')

    if form == 'str':
        return str(end_dt - timedelta(seconds=n))[:19], str(end_dt)[:19]
    elif form == 'ts':
        return int((end_dt - timedelta(seconds=n)).timestamp()), int(end_dt.timestamp())
    else:
        raise TypeError('Unsupported form {}'.format(form))


def before_n_days(n, date_str=None):
    """
    获得前N天，只支持%Y-%m-%d格式
    :param n:
    :param date_str: None以当前时间为准
    :return:
    """
    if date_str is None:
        date_ts = date.today()
    else:
        date_ts = datetime.strptime(date_str[:10], '%Y-%m-%d')

    return str(date_ts - timedelta(days=n))[:10]


def before_n_hours(n, date_str=None):
    """
    获得现在n小时前的时间格式
    :param n:
    :param date_str:
    :return:
    """
    if date_str is None:
        before_date = datetime.now() - timedelta(hours=n)
    else:
        before_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') - timedelta(hours=n)
    return before_date.strftime('%Y-%m-%d %H:00:00')


def before_n_seconds(n, date_str=None):
    """
    获得现在n秒前的时间格式
    :param n:
    :param date_str:
    :return:
    """
    if date_str is None:
        before_date = datetime.now() - timedelta(seconds=n)
    else:
        before_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') - timedelta(seconds=n)
    return before_date.strftime('%Y-%m-%d %H:%M:%S')


def between_days(start_date_str, end_date_str, rev=False, including_end=False):
    end_date = datetime.strptime(end_date_str[:10], '%Y-%m-%d')
    start_date = datetime.strptime(start_date_str[:10], '%Y-%m-%d')
    if start_date >= end_date:
        return [str(end_date)] if including_end else []
    diff_day_cnt = (end_date - start_date).days
    total_cnt = diff_day_cnt + 1 if including_end else diff_day_cnt
    result = [str(start_date + timedelta(days=i))[:10] for i in range(total_cnt)]
    return result[::-1] if rev else result


def between_hours(start_date_str, end_date_str, rev=False, including_end=False, delta_type='hour', interval=1):
    # 格式必须是 %Y-%m-%d %H:%M:%S
    end_date = datetime.strptime(end_date_str[:19], '%Y-%m-%d %H:%M:%S')
    start_date = datetime.strptime(start_date_str[:19], '%Y-%m-%d %H:%M:%S')
    if start_date >= end_date:
        return [str(end_date)] if including_end else []
    if delta_type == 'hour':
        diff_cnt = int((end_date - start_date).total_seconds() / (60 * 60))
        total_cnt = diff_cnt + 1 if including_end else diff_cnt
        result = [str(start_date + timedelta(hours=i))[:19] for i in range(1, total_cnt, interval)]
    elif delta_type == 'minutes':
        diff_cnt = int((end_date - start_date).total_seconds() / 60)
        total_cnt = diff_cnt + 1 if including_end else diff_cnt
        result = [str(start_date + timedelta(hours=i))[:19] for i in range(1, total_cnt, interval)]
    elif delta_type == 'seconds':
        diff_cnt = (end_date - start_date).total_seconds()
        total_cnt = diff_cnt + 1 if including_end else diff_cnt
        # noinspection PyTypeChecker
        result = [str(start_date + timedelta(hours=i))[:19] for i in range(1, total_cnt, interval)]
    else:
        raise TypeError('no delta_type format'.format(delta_type))
    return result[::-1] if rev else result


def is_later(a_date_str, b_date_str):
    """a 比b 晚？"""
    a_date = datetime.strptime(a_date_str[:10], '%Y-%m-%d')
    b_date = datetime.strptime(b_date_str[:10], '%Y-%m-%d')
    return a_date > b_date


def is_dayout(date_str, dayout_num):
    """超时"""
    if dayout_num is None:
        return False
    return datetime.strptime(date_str[:10], '%Y-%m-%d').date() + timedelta(days=dayout_num) < date.today()


def today():
    return str(date.today())


def yesterday():
    return str(date.today() - timedelta(days=1))


def day_after(n, date_str):
    return str(datetime.strptime(date_str[:10], '%Y-%m-%d') + timedelta(days=n))[:10]


def diff(end_date_str, start_date_str):
    """a距b 多少天"""
    a_date = datetime.strptime(str(end_date_str)[:10], '%Y-%m-%d')
    b_date = datetime.strptime(str(start_date_str)[:10], '%Y-%m-%d')
    return (a_date - b_date).days


def diff_seconds(end_date_str, start_date_str):
    """a距b 多少小时"""
    a_date = datetime.strptime(str(end_date_str), '%Y-%m-%d %H:%M:%S')
    b_date = datetime.strptime(str(start_date_str), '%Y-%m-%d %H:%M:%S')
    res = (a_date - b_date)
    return res.seconds + res.days * 24 * 3600


def now_diff(date_str):
    """距今多少天"""
    a_date = datetime.now()
    b_date = datetime.strptime(date_str[:10], '%Y-%m-%d')
    return (a_date - b_date).days


def now_diff_seconds(date_str):
    """距今多少天"""
    a_date = datetime.now()
    b_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    res = (a_date - b_date)
    return res.seconds + res.days * 24 * 3600


def parse_date(date_arg, start_date=None, rev=False):
    """
    fetch系脚本专用，解析date参数
    """
    if date_arg.strip() == 'all':
        # 返回距今（不包含当天）所有dates
        if start_date is None:
            print('parse all need start_date, will return None!')
            return
        return between_days(start_date, yesterday(), rev=rev)
    elif date_arg.strip() == 'today':
        return [today()]
    elif date_arg.strip() == 'yesterday':
        return [yesterday()]
    elif len(date_arg) == 10 and '-' in date_arg:
        # 2020-03-05
        return [date_arg]
    elif date_arg.isdigit():
        # before n days
        return range_day(int(date_arg), rev=rev)
    elif ':' in date_arg and len(date_arg.split(':')) == 2 and len(date_arg.split(':')[0]) == 10 and len(
            date_arg.split(':')[1]) == 10 and '-' in date_arg.split(':')[1]:
        # 2020-03-03:2020-03-05
        items = date_arg.split(':')
        return between_days(items[0], items[1], rev=rev)
    elif ':' in date_arg and len(date_arg.split(':')) == 2 and len(date_arg.split(':')[0]) == 10 and \
            date_arg.split(':')[1].isdigit():
        items = date_arg.split(':')
        # 2020-03-03:30 output # before 2020-03-03 30 day
        return range_day(int(items[1]), date_str=items[0], rev=rev)
    elif '|' in date_arg and len(date_arg.split('|')) == 2 and len(date_arg.split('|')[0]) == 19 and \
                    len(date_arg.split('|')[1]) == 19:
        # 支持小时级别的返回list
        items = date_arg.split('|')
        return between_hours(items[0], items[1])

    raise TypeError('date_arg={} bad format!'.format(date_arg))


def now():
    """
    获取当前时间日期，时间单位只取到秒，返回如'2018-07-03 12:52:43'
    :return: 返回如'2018-07-03 12:52:43' str对象
    """
    return str(datetime.now()).split('.')[0]


def sort_date(date_list, rev=False):
    """
        返回一个str date list 的排序
    """
    return sorted(date_list, key=lambda x: datetime.strptime(x, '%Y-%m-%d'), reverse=rev)


def ts2str(ts, time_format=g_time_format):
    return datetime.fromtimestamp(ts).strftime(time_format)


def str2ts(time_str, time_format=g_time_format):
    return int(time.mktime(datetime.strptime(time_str, time_format).timetuple()))
