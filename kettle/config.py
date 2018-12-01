import configparser
import os

CONFIG_PATH = os.path.expanduser('~/.kettle/')
CONFIG_FILE = 'config.ini'


def create_config():
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)
    if not os.path.exists(CONFIG_PATH + CONFIG_FILE):
        config = configparser.ConfigParser()

        config.add_section('General')

        config.set('General', 'view_statusbar', 'True')

        with open(CONFIG_PATH + CONFIG_FILE, 'w') as config_file:
            config.write(config_file)


def get_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH + CONFIG_FILE)
    return config


def get_setting(section, setting, fallback=None):
    config = get_config()
    return config.get(section, setting, fallback=fallback)


def update_config(section, setting, value):
    config = get_config()
    config.set(section, setting, value)
    with open(CONFIG_PATH + CONFIG_FILE, 'w') as config_file:
        config.write(config_file)
