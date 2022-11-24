import configparser
import Util.log as log
import os

LOGLEVEL = 'DEBUG'
CONFIG_FILE_NAME = 'D:\\projects\\python\\registryPopulateionBot\\Util\\config.ini'

ORACLE_HOST = '127.0.0.1'
ORACLE_PORT = 1521
ORACLE_SID = 'sid'
ORACLE_USER = 'user'
ORACLE_PASSWORD = '**********'

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DATABASE = 'Mongo_database'
MONGO_COLLECTION = 'mongo_collection'

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0


def get_config(file_name):
    config = configparser.ConfigParser()
    config.read(file_name)
    return config


def get_props(config, section, option, default):
    result = default
    if option in os.environ:
        log.logging.info('get option : ' + option + ' from environment')
        result = os.environ[option]
    else:
        log.logging.info('environment: ' + option + ' is empty')
        if option in config[section]:
            log.logging.info('get option : ' + option + ' from config')
            result = config[section][option]
        else:
            log.logging.info('congif : ' + option + ' is empty')
    return result


def set_log_level():
    log.user_set_level(get_props(get_config(CONFIG_FILE_NAME), 'Application', 'LogLevel', 'DEBUG'))


def init_values():
    config = get_config(CONFIG_FILE_NAME)

    global ORACLE_HOST
    ORACLE_HOST = get_props(config, 'ORACLE', 'ORACLE_HOST', ORACLE_HOST)

    global ORACLE_PORT
    ORACLE_PORT = get_props(config, 'ORACLE', 'ORACLE_PORT', ORACLE_PORT)

    global ORACLE_SID
    ORACLE_SID = get_props(config, 'ORACLE', 'ORACLE_SID', ORACLE_SID)

    global ORACLE_USER
    ORACLE_USER = get_props(config, 'ORACLE', 'ORACLE_USER', ORACLE_USER)

    global ORACLE_PASSWORD
    ORACLE_PASSWORD = get_props(config, 'ORACLE', 'ORACLE_PASSWORD', ORACLE_PASSWORD)

    global MONGO_HOST
    MONGO_HOST = get_props(config, 'MONGO', 'MONGO_HOST', MONGO_HOST)

    global MONGO_PORT
    MONGO_PORT = get_props(config, 'MONGO', 'MONGO_PORT', MONGO_PORT)

    global MONGO_DATABASE
    MONGO_DATABASE = get_props(config, 'MONGO', 'MONGO_DATABASE', MONGO_DATABASE)

    global MONGO_COLLECTION
    MONGO_COLLECTION = get_props(config, 'MONGO', 'MONGO_COLLECTION', MONGO_COLLECTION)

    global REDIS_HOST
    REDIS_HOST = get_props(config, 'REDIS', 'REDIS_HOST', REDIS_HOST)

    global REDIS_PORT
    REDIS_PORT = get_props(config, 'REDIS', 'REDIS_PORT', REDIS_PORT)

    global REDIS_DB
    REDIS_DB = get_props(config, 'REDIS', 'REDIS_DB', REDIS_DB)
