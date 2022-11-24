import redis
import Util.config as config

def connect():
    pool = redis.ConnectionPool(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB)
    return redis.Redis(connection_pool=pool)


