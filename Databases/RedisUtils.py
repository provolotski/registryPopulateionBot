import os

import redis

pool  = redis.ConnectionPool(host = os.environ['RedisServer'], port = os.environ['RedisPort'], db = 0)