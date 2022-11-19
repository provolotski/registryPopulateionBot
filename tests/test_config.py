import Util.config


def test_set_log_level():
    Util.config.set_log_level()
    assert True


def test_get_props():
    config = ''
    print(Util.config.get_props('', 'Application', 'LogLevel', 'DEBUG'))
    print(Util.config.get_props(Util.config.get_config(Util.config.config_file_name),'ORACLE','host','127.0.0.1'))
    assert True
