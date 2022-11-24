import Util
from Databases import MongoUtils


def test_check_relative():
    Util.config.init_values()
    MongoUtils.check_relative(0)
    print('asdasd')
