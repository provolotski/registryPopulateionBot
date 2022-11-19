import configparser
import Util.Log as log
import os

logLevel = 'DEBUG'
config_file_name = '/home/kpss/projects/python/registryPopulateionBot/Util/config.ini'

oracle_host = '127.0.0.1'
oracle_port = 1521
oracle_sid = 'sid'
oracle_user = 'user'
oracle_password = '**********'



def get_config(file_Name):
    config = configparser.ConfigParser()
    config.read(file_Name)
    return config


def get_props(config,section,option,default):
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
    log.user__set_level(get_props(get_config(config_file_name),'Application','LogLevel','DEBUG'))

def init_values():
    config = get_config(config_file_name)

    global oracle_host
    oracle_host = get_props(config,'ORACLE','ORACLE_HOST', oracle_host)

    global oracle_port
    oracle_port = get_props(config,'ORACLE','ORACLE_PORT', oracle_port)

    global oracle_sid
    oracle_sid = get_props(config,'ORACLE','ORACLE_SID',oracle_sid)

    global oracle_user
    oracle_user = get_props(config,'ORACLE','ORACLE_USER',oracle_user)

    global oracle_password
    oracle_password = get_props(config,'ORACLE','ORACLE_PASSWORD',oracle_password)

