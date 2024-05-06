#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 参考资料: https://codelieche.com/article/56852
import logging
import socket
import os
import json
from logging.handlers import TimedRotatingFileHandler

from utils.decorator import command_input
from utils.file_util import make_dir


class GroupWriteTimedRotatingFileHandler(TimedRotatingFileHandler):
    def _open(self):
        prevumask = os.umask(0o002)
        rtv = TimedRotatingFileHandler._open(self)
        os.umask(prevumask)
        return rtv


@command_input('env')
@command_input('port')
@command_input('mode')
def getLogger(env, port, mode):
    hostname = socket.gethostname()
    if mode == 'common':
        log_dir = '/home/web/sunjiyuan/applogs/ut-caesar'
    else:
        log_dir = '/home/web/sunjiyuan/logs/ut-caesar/{}'.format(hostname)

    make_dir(log_dir)
    fmt = logging.Formatter(
        '%(asctime)s [%(threadName)s] %(levelname)s (%(filename)s:%(lineno)d) - %(message)s')

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.getLogger('nacos').setLevel(logging.WARNING)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    if env == 'local' or env == 'pre':
        logger.addHandler(ch)

    fh = GroupWriteTimedRotatingFileHandler(
        '{}/ut-caesar-{}.log'.format(log_dir, port),
        when='D', interval=1, backupCount=5, encoding='utf-8')
    fh.setLevel(logging.INFO)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    rh = GroupWriteTimedRotatingFileHandler(
        '{}/ut-caesar-{}.error.log'.format(log_dir, port),
        when='D', interval=1, backupCount=5, encoding='utf-8')
    rh.setLevel(logging.ERROR)
    rh.setFormatter(fmt)
    logger.addHandler(rh)

    return logger


def color(string):
    CRED, CGREEN = '\033[91m', '\33[32m'
    CEND = '\033[0m'
    return CGREEN + string + CEND


def alarm_algorithm(message):
    # url = ""
    # data = {"msgtype": "text", "text": {"content": message}}
    try:
        # response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
        print(response.text)
    except Exception:
        logger.error("fatal error: send message to weixin failed !!!!")


logger = getLogger(env='local', port=9090, mode='common')

if __name__ == '__main__':
    logger.debug('debug...')
    logger.info('info...')
    logger.warning('warning...')
    logger.error('error...')
