import Util
from Databases import RedisUtils


def test_connect():
    Util.config.init_values()
    redis = RedisUtils.connect()
    redis.set('mykey', 'Hello from Python!')
    value = redis.get('mykey')
    assert value == b'Hello from Python!'

def test_read_unknown():
    redis = RedisUtils.connect()
    print(redis.get('12123'))

