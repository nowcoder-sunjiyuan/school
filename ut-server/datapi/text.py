import re
import html
import string
import time
import numpy as np


def sign(n, with_time=False):
    s = ''.join(np.random.choice(list(string.ascii_letters), n))
    if with_time:
        s += str(int(time.time()))
    return s


def is_null(val):
    return val is None or str(val) == '' or str(val).strip().lower() in ('none', 'null', 'nan')


def filter_unchi(s):
    if is_null(s):
        return ''
    s = str(s)
    filtrate = re.compile(u'[\s+\.\!\/_;,:【】┃$%^*(+\"\']+|[+——！，。？、~@#☆★￥%√〓……&*（）]+')
    return filtrate.sub(r'', s).strip()


def filter_bad(s):
    # 过滤脏字符
    if is_null(s):
        return ''
    s = str(s)
    filtrate = re.compile(u'[\s\/_$%^*┃(]+|[——~@#￥%&☆〓★√*（）]+')
    return filtrate.sub(r'', s)


def remove_html(content):
    if is_null(content):
        return ''
    s = str(content)
    content = html.unescape(content)
    dr = re.compile(r'<[^>]+>', re.S)
    result = dr.sub('', content)
    return result


def remove_blank(content):
    # 过滤长空格
    if is_null(content):
        return ''

    blank = re.compile('\\s+')
    return blank.sub('', str(content))


def clean_all(content):
    if is_null(content):
        return ''

    content = str(content)
    content = remove_html(content)
    content = filter_bad(content)
    content = filter_unchi(content)
    content = remove_blank(content)
    return content


def only_cn(s):
    # 过滤所有非中文
    if is_null(s):
        return ''
    s = str(s)

    arr = re.findall(r'[\u4e00-\u9fa5]+', s)
    return ''.join(arr)


def only_word(s):
    if is_null(s):
        return ''
    s = str(s)

    reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
    return re.sub(reg, '', s)


def only_charword(s):
    if is_null(s):
        return ''
    s = str(s)

    reg = "[^A-Za-z\u4e00-\u9fa5]"
    return re.sub(reg, '', s)
