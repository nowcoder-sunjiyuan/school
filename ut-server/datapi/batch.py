# -*- coding: utf-8 -*-
"""
序列相关
"""
import math
import numpy as np

__author__ = 'jx'


def batch_list(list_obj, batch_size):
    """
    切分list
    :param list_obj: list数据，如 [1,2,3,4,5]
    :param batch_size: 每片list长度，如 size=3 [1,2,3,4,5] -> [[1,2,3], [4,5]]
    :return:
    """
    list_obj = list(list_obj)
    if batch_size is None:
        yield list_obj
    else:
        list_len = len(list_obj)
        chunk_len = int(math.ceil(list_len / batch_size))
        for i in range(chunk_len):
            start = i * batch_size
            end = (i + 1) * batch_size
            if end >= list_len:
                end = list_len
            yield list_obj[start:end]


def batch_generator(gen_obj, batch_size):
    """
    切分生成器，会先全部生成
    :param gen_obj:
    :param batch_size:
    :return:
    """
    if batch_size is None:
        yield gen_obj
    else:
        batch_count = 0
        data = np.empty(batch_size, dtype=object)
        for o in gen_obj:
            data[batch_count] = o
            batch_count += 1
            if batch_count == batch_size:
                yield data.tolist()
                batch_count = 0
                data[:] = None

        if batch_count > 0:
            yield data[:batch_count].tolist()
