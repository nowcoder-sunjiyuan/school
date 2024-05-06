from sshtunnel import SSHTunnelForwarder

from utils.logger_helper import logger


def bind(remote_host: str, remote_port: int):
    """
    通过中转服务器, 将远程的地址+端口映射到本地的某个端口
    """
    logger.info("==> Establish SSH Tunnel for remote_host: %s, remote_port: %d", remote_host, remote_port)
    try:
        return SSHTunnelForwarder(
            ('172.16.33.235', 22),
            ssh_username="web",
            ssh_password="92ce6a70fbf2ac4df071ce7ef21a87c1",
            remote_bind_address=(remote_host, remote_port))
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    server = bind('rm-bp1t25mc6rirlygt8720.mysql.rds.aliyuncs.com', 3306)
    server.start()
    print(server.local_bind_host)
    print(server.local_bind_port)
    server.stop()

    # 更多例子参见 export_data.py
