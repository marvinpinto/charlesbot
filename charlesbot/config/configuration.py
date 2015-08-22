import yaml
import os


def read_config_dict(filename):
    with open(filename, 'r') as f:
        return yaml.load(f)


def get_config_file_name():
    env_var = "CHARLESBOT_SETTINGS_FILE"
    if env_var in os.environ:
        if os.environ[env_var]:
            return os.environ[env_var]
    return './development.yaml'


def get():
    config_dict = read_config_dict(get_config_file_name())
    return config_dict
