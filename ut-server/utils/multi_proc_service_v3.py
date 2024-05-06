import gc
import json
import multiprocessing
import sys
import threading
import time
from queue import Queue

from ..utils.logger_helper import logger, alarm_algorithm


# FIFO LOCK
class QLock:
    def __init__(self):
        self.queue = Queue(maxsize=50)
        self.lock = threading.Lock()
        self.count = 0

    def acquire(self):
        self.lock.acquire()
        self.count += 1
        if self.count == 1:
            self.lock.release()
            return
        self.lock.release()
        q_lock = threading.Lock()
        q_lock.acquire()
        self.queue.put(q_lock)
        q_lock.acquire()

    def release(self):
        self.lock.acquire()
        self.count -= 1
        if self.count > 0:
            self.queue.get().release()
        self.lock.release()


# master_end -> (pipe, 进程编号, 已调用次数)
def create_service_process_pool(service_class, process_num=2, args=None, kargs=None):
    ps = []
    master_ends = []
    for i in range(process_num):
        master_end, worker_end = multiprocessing.Pipe()
        master_ends.append((master_end, i, time.time()))
        if args is None and kargs is None:
            obj = service_class(worker_end, i)
        else:
            obj = service_class(worker_end, i, *args, **kargs)
        ps.append(multiprocessing.Process(target=obj.run))
    for i in range(process_num):
        ps[i].start()
    time.sleep(10)
    for i in range(process_num):
        logger.info('%s pid: %s', service_class, ps[i].pid)
        print('%s pid: %s' % (service_class, ps[i].pid))
        master_ends[i][0].send(None)
        master_ends[i][0].recv()
    return master_ends


# handler层
class BaseHandler(object):
    def __init__(self, service_class, process_num=2, *args, **kargs):
        self.pipe_queue = Queue(maxsize=10)
        self.fair_lock = QLock()
        self.master_ends = create_service_process_pool(service_class=service_class,
                                                       process_num=process_num, args=args, kargs=kargs)
        for end in self.master_ends:
            self.pipe_queue.put(end)
        self.lock = threading.Lock()
        self.check_interval = 100
        self.check_flag = True
        self.prepared_end = None
        self.check_thread = threading.Thread(target=self.send_check_order)
        self.check_thread.start()

    def communicate_with_worker(self, request):
        self.fair_lock.acquire()
        master_end, proc_num, timestamp = self.pipe_queue.get()
        self.fair_lock.release()
        master_end.send(request)
        result = master_end.recv()
        self.lock.acquire()
        if self.check_flag and time.time() - timestamp > self.check_interval:
            self.check_flag = False
            self.prepared_end = (master_end, proc_num, timestamp)
        else:
            self.pipe_queue.put((master_end, proc_num, timestamp))
        self.lock.release()
        return result

    def send_check_order(self):
        while True:
            time.sleep(5)
            if not self.check_flag:
                master_end, proc_num, count = self.prepared_end
                master_end.send(None)
                master_end.recv()
                self.lock.acquire()
                self.pipe_queue.put((master_end, proc_num, time.time()))
                self.check_flag = True
                self.lock.release()


# service层
class BaseService(object):

    def __init__(self, pipe_end, proc_num, *args, **kwargs):
        self.pipe_end = pipe_end
        self.proc_num = proc_num
        self.monitor_list = []
        self.crontab_list = [gc.collect]
        self.cntx = None
        self.args = args
        self.kwargs = kwargs
        # 这里不要创建线程或者not pickleable 的东西
        # threading.Thread(target=self.exec_task).start()

    def init(self, *args, **kwargs):
        pass

    def warm_up(self):
        pass

    def _warm_up(self):
        pass

    def run_update(self, item_list, args=None):
        if args is None:
            for item in item_list:
                try:
                    item.load()
                except Exception as e:
                    logger.exception(e)
        else:
            for item in item_list:
                try:
                    item.load(args)
                except Exception as e:
                    logger.exception(e)

    def exec_task(self):
        for item in self.monitor_list:
            if type(item) == tuple:
                item[0].check_update()
                flag = True
                consistent = True
                current_ts = item[0].get_current_ts()
                for sub_item in item:
                    flag &= sub_item.is_old
                    consistent &= (current_ts == sub_item.get_current_ts())
                if flag or not consistent:
                    ts = int(2e10)
                    for sub_item in item:
                        ts = min(ts, sub_item.get_latest_ts())
                    self.run_update(item, ts)
            else:
                item.check_update()
                if item.is_old:
                    self.run_update([item])
        for item in self.crontab_list:
            if type(item) == tuple:
                item[0]()
            else:
                item()

    def run(self):
        self.init(*self.args, **self.kwargs)
        sys.setcheckinterval(10000000)
        gc.disable()
        while True:
            try:
                cntx = self.pipe_end.recv()
            except Exception as e:
                logger.exception('process %d read pipe error: %s', self.proc_num, e)
                continue
            start = time.time()

            # LBS health deteact
            if cntx is None:
                try:
                    self.exec_task()
                    self.warm_up()
                    self._warm_up()
                except Exception as e:
                    logger.exception('process %d exec_task error: %s', self.proc_num, e)
                    alarm_algorithm("线上服务执行定时任务失败")
                finally:
                    logger.info('process %d complete task', self.proc_num)
                self.pipe_end.send(True)
                continue

            try:
                self.cntx = cntx
                result = self.work(cntx)
            except Exception as e:
                result = {"code": 1, "data": []}
                logger.exception('some error happened: %s', e)
            if type(result) == dict:
                self.pipe_end.send(json.dumps(result))
            else:
                self.pipe_end.send(result)
            result = None
            logger.info('cost: %d', int((time.time() - start) * 1000))

    def work(self, cntx):
        raise NotImplementedError
