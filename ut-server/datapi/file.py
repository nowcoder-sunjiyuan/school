# -*- coding: utf-8 -*-
"""
文件相关工具类
"""
import os
import shutil
import time
import pickle
from .env import g_project_root

__author__ = 'jx'

RETRY_TIMES = 3


def ensure_file_dir(file_path):
    """确保文件的目录路径"""
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)


def ensure_dir(dir_path):
    """确保文件夹的目录路径"""
    os.makedirs(os.path.abspath(dir_path), exist_ok=True)


def clear_dir(dir_path, keep_dir=True):
    """确保文件夹的目录路径"""
    dir_path = os.path.abspath(dir_path)
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    if keep_dir:
        os.makedirs(dir_path)


def iter_dir(dir_fn):
    dir_fn = os.path.abspath(dir_fn)
    if os.path.exists(dir_fn):
        for _fn in os.listdir(dir_fn):
            yield os.path.join(dir_fn, _fn)


def is_data_file_ok(data_file_path):
    """是否为有数据的文件"""
    return data_file_path is not None and os.path.exists(data_file_path) and os.path.getsize(data_file_path) > 0


def add_col_to_file(input_path, col, output_path):
    """增加一列用于merge文件"""
    awk_shell = os.path.join(g_project_root, 'datapi', 'awk_col.sh')

    if not is_data_file_ok(input_path):
        print('Missing {}'.format(input_path))
        return
    os.system('bash {} {} {} >> {}'.format(awk_shell, input_path, col, output_path))


def sort_id(s_file, uniq=False, num_id=True):
    """
    按第一列id排序文件，【id必须是数字】
    :param s_file: 输入文件
    :param uniq: 是否去重
    :param num_id: id列是否是数字
    :return:
    """
    if not is_data_file_ok(s_file):
        print('no file {} found!'.format(s_file))
        return

    s_tmp_file = s_file + '.s'
    num_str = ' -n' if num_id else ''
    if uniq:
        # sort -unt $\'\t\' {} -o {} un会导致按id uniq，丢失行数据
        os.system('sort{} {} | uniq > {}'.format(num_str, s_file, s_tmp_file))
    else:
        os.system('sort{} {} -o {}'.format(num_str, s_file, s_tmp_file))

    if is_data_file_ok(s_tmp_file):
        os.system('mv {} {}'.format(s_tmp_file, s_file))
    else:
        os.system('rm {}'.format(s_tmp_file))


def shuffle(s_file):
    """shuf命令实现的随机化"""
    if not is_data_file_ok(s_file):
        print('no file {} found!'.format(s_file))
        return
    s_tmp_file = s_file + '.shuf'
    os.system('shuf {} > {}'.format(s_file, s_tmp_file))

    if is_data_file_ok(s_tmp_file):
        os.system('mv {} {}'.format(s_tmp_file, s_file))
    else:
        os.system('rm {}'.format(s_tmp_file))


def random_sample(s_file, nrow):
    """随机采样行"""
    if not is_data_file_ok(s_file):
        print('no file {} found!'.format(s_file))
        return
    s_tmp_file = s_file + '.sample'
    os.system("shuf -n {} {} > {}".format(nrow, s_file, s_tmp_file))


def split_by_line(input_file, line_count):
    """按行分割文件，返回文件路径列表"""
    if not is_data_file_ok(input_file):
        print('no file {} found!'.format(input_file))
        return
    dir_name = os.path.dirname(input_file)
    # signature = str(os.path.getsize(input_file))+"#"+str(math.floor(os.path.getmtime(input_file)))
    signature = str(int(time.time())) + '_'
    os.system('rm -rf {}*'.format(signature))
    os.system('cd {} && split -l {} {} {}'.format(dir_name, line_count, input_file, signature))
    return [os.path.join(dir_name, f) for f in os.listdir(dir_name) if f.startswith(signature)]


def split_two(input_path, split_line, output_a_path, output_b_path):
    """
    分割成同文件夹下的两个文件
    :param input_path: 输入文件
    :param split_line:
    :param output_a_path:
    :param output_b_path:
    :return:
    """
    if not is_data_file_ok(input_path):
        print('no file {} found!'.format(input_path))
        return

    os.system('head -n {} {} > {} && tail -n +{} {} > {}'.format(
        split_line, input_path, output_a_path, split_line + 1, input_path, output_b_path))


def split_three(input_path, split_line_a, split_line_b, output_a_path, output_b_path, output_c_path):
    """
    分割成同文件夹下的两个文件
    :param input_path:
    :param split_line_a:
    :param split_line_b:
    :param output_a_path:
    :param output_b_path:
    :param output_c_path:
    :return:
    """
    if not is_data_file_ok(input_path):
        print('no file {} found!'.format(input_path))
        return

    signature = str(int(time.time())) + '_'
    dir_name = os.path.dirname(input_path)

    tmp_path = os.path.join(dir_name, '{}.split'.format(signature))
    os.system('head -n {} {} > {} && tail -n +{} {} > {} && head -n {} {} > {} && tail -n +{} {} > {} && rm {}'.format(
        split_line_a, input_path, output_a_path, split_line_a + 1, input_path, tmp_path, split_line_b, tmp_path,
        output_b_path, split_line_b + 1, tmp_path, output_c_path, tmp_path))


def count_line(input_file):
    """统计文件行数"""

    def _blocks(files, size=65536):
        while True:
            b = files.read(size)
            if not b:
                break
            yield b

    with open(input_file) as r:
        return sum(bl.count('\n') for bl in _blocks(r))


def dump_pickle(data, fn):
    ensure_file_dir(fn)
    with open(fn, 'wb') as w:
        pickle.dump(data, w)


def load_pickle(fn):
    if is_data_file_ok(fn):
        with open(fn, 'rb') as r:
            return pickle.load(r)
