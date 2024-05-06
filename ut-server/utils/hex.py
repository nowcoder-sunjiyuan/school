import os
import platform

import tensorflow

from logger_helper import logger

__all__ = ['tf_settings']


def tf_settings(silent=False):
    tf_version = tensorflow.__version__
    if tf_version.startswith('1.'):
        tf = tensorflow.compat.v1
    else:
        tf = tensorflow
    tf_logger = tf.get_logger()
    [tf_logger.removeHandler(h) for h in tf_logger.handlers]
    # 动态分配显存
    gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    if silent:
        return tf
    logger.info(f'Python Version: {platform.python_version()}')
    logger.info(f'TensorFlow Version: {tf_version}')
    return tf
