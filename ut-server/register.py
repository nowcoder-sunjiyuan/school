import socket
import sys
import threading
import time

import nacos
import signal

from conf import settings
from utils import logger


class LifeCycle(object):
    def __init__(self, service, port):
        self.name = service
        self.port = port
        self.flag = True

        # Todo: dev 环境上报公网 ip
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        self.ip = s.getsockname()[0]

        self.client = nacos.NacosClient(
            server_addresses=settings['nacos']['server-addr'],
            namespace=settings['nacos']['namespace']
        )

    def register(self, cost=None):
        elapsed = '' if cost is None else f' (cost: {cost:.0f}ms)'
        logger.info('register ip: %s%s', self.ip, elapsed)
        self.client.add_naming_instance(self.name, self.ip, self.port, cluster_name='DEFAULT')
        signal.signal(signal.SIGTERM, self.exit_handler)
        t1 = threading.Thread(target=self.heartbeat)
        t1.start()

    def heartbeat(self):
        while self.flag:
            try:
                self.client.send_heartbeat(self.name, self.ip, self.port, cluster_name='DEFAULT')
                time.sleep(1)
            except:
                pass

    def unregister(self):
        self.flag = False
        self.client.remove_naming_instance(self.name, self.ip, self.port, cluster_name='DEFAULT')

    def exit_handler(self, signum, frame):
        print(signum, frame)
        self.unregister()
        time.sleep(35)
        sys.exit(0)


if __name__ == '__main__':
    lc = LifeCycle('tornado', 8888)
    lc.unregister()
