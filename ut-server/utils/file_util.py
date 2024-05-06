import os
import threading
import time


def delete_dir(dirname):
    if os.path.exists(dirname):
        os.rmdir(dirname)


def make_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname, mode=0o755, exist_ok=True)


def ensure_dir(file_path):
    dirname = os.path.dirname(file_path)
    make_dir(dirname)


class FileMonitor(object):
    def __init__(self, file_path, load_func, interval=300, passive=False):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            print("******** env is local *******")
            self.download_file()
        self.update_ts = os.path.getmtime(self.file_path)
        self.is_old = False
        self.interval = interval
        self.load_func = load_func
        self.th = threading.Thread(target=self.monitor)
        if not passive:
            self.th.start()

    def monitor(self):
        while True:
            time.sleep(self.interval)
            self.check_update()

    def check_update(self):
        update_ts = os.path.getmtime(self.file_path)
        if update_ts - self.update_ts > 1:
            self.is_old = True
            self.update_ts = update_ts

    def is_new(self):
        if self.is_old:
            self.is_old = False
            return True
        return False

    def load(self):
        self.is_old = False
        self.load_func(self)

    def get_current_ts(self):
        return self.update_ts

    def get_latest_ts(self):
        return os.path.getmtime(self.file_path)

    def download_file(self):
        directory = "/".join(self.file_path.split("/")[:-1])
        self.file_path = "/data" + self.file_path
        res = os.popen("mkdir -p /data%s && scp web@172.20.2.2:%s/* /data%s" % (directory, directory, directory), mode='r')
        res.read()


