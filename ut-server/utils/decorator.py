import argparse

def command_input(arg_name):
    """
    实现利用命令行传参来强行替换被封装函数的代码传参

    Example：
    @command_input('info')
    def print_fn(info):
        print(info)
    if __name__ == '__main__':
        print_fn(info=123)

    1.python xx.py 打印123
    2.python xx.py --info 456 打印456
    :param arg_name: 需要强制传值的参数
    :return: 被封装的函数
    """
    def wrapper(func):
        parser = argparse.ArgumentParser()
        parser.add_argument('--{}'.format(arg_name))
        parsed, _ = parser.parse_known_args()
        arg_value = getattr(parsed, arg_name)
        def deco(*args, **kwargs):
            if arg_value is not None:
                kwargs[arg_name] = arg_value
            return func(*args, **kwargs)
        return deco
    return wrapper
