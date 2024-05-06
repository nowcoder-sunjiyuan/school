from conf import settings
from datapi.db import MysqlDB, ThreadMysqlDB, MongoDB, RedisClient, ClickHouseDb, InfluxDB, MaxCompute
import copy

db_name_key = {
    "david": "nk_david",
    "recommend": "nk_recommend",
    "wenyibi": "nk_wyb",
    "hr": "nk_hr",
    "boss": "nk_boss",
    "question": "nk_question"
}


def use_ssh():
    """
    是否使用ssh
    在 dev及local 中需要使用ssh
    """
    ssh = False
    if settings["env"] in ["local", "dev"]:
        ssh = True
    return ssh


def read_mirror_db():
    """
    读镜像库
    """
    ssh = False if settings["env"] != "local" else True
    return MysqlDB(copy.deepcopy(settings["nk_mirror"]['read']), ssh)


def read_mysql_db(db_name, is_pool=False):
    db_class = ThreadMysqlDB if is_pool else MysqlDB
    db_key = db_name_key[db_name]
    return db_class(copy.deepcopy(settings[db_key]["read"]))


def write_mysql_db(db_name, is_pool=False):
    db_class = ThreadMysqlDB if is_pool else MysqlDB
    db_key = db_name_key[db_name]
    return db_class(copy.deepcopy(settings[db_key]["write"]), False)


def read_mongo_db():
    return MongoDB(copy.deepcopy(settings["mongo_db"]["read"]), False)


def read_redis(is_pool=False):
    ssh = use_ssh()
    return RedisClient(copy.deepcopy(settings["redis"]["read"]), return_pool=is_pool, ssh=ssh)


def write_redis(is_pool=False):
    return RedisClient(copy.deepcopy(settings["redis"]["write"]), return_pool=is_pool)


def read_influx_db():
    return InfluxDB(copy.deepcopy(settings["nk_influx"]["read"]))


def write_influx_db():
    return InfluxDB(copy.deepcopy(settings["nk_influx"]["write"]))


def read_max_compute(project='columbus'):
    return MaxCompute(copy.deepcopy(settings["rec_max_compute"]["read"]), project)
