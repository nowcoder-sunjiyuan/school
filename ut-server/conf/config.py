import os

import yaml
import sys
sys.path.append("..")

from utils.decorator import command_input
from utils.logger_helper import logger


def decrypt(s):
    key = "NOWCODER#UT"
    key = (key * (len(s) // len(key) + 1))[0:len(s)]
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s, key))


@command_input('env')
def load_config(env):
    """Current possible env values: {dev, prod}"""
    dirname = os.path.dirname(os.path.realpath(__file__))
    filename = '{}/application-{}.yml'.format(dirname, env)
    logger.info(filename)
    with open(filename, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    config["rec_max_compute"]["read"]["access_id"] = decrypt(bytearray.fromhex(config["rec_max_compute"]["read"]["access_id"]).decode())
    config['oss']['accessKeyID'] = decrypt(bytearray.fromhex(config['oss']['accessKeyID']).decode())
    return config


# 默认dev环境，可以通过命令行指定 ex: --env prod
settings = load_config(env='local')
