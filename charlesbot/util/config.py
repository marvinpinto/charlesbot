import os
from configparser import ConfigParser


def get_config_file_name():
    if 'CHARLESBOT_SETTINGS_FILE' in os.environ:
        if os.environ['CHARLESBOT_SETTINGS_FILE']:
            return os.environ['CHARLESBOT_SETTINGS_FILE']
    return './development.ini'


def read_config(config_file):
    config = ConfigParser(allow_no_value=False)
    config.read(config_file)
    return config
