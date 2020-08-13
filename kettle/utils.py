import os
from PyQt5.QtGui import QIcon

basedir = os.path.abspath(os.path.dirname(__file__))


def select_asset_based_on_theme(white_theme_icon, dark_theme_icon, configparser):
    if str2bool(configparser.get_setting('General', 'use_dark_theme')):
        return QIcon(os.path.join(basedir, f'../assets/{dark_theme_icon}'))
    else:
        return QIcon(os.path.join(basedir, f'../assets/{white_theme_icon}'))


def str2bool(str):
    return str.lower() in ('True', 'true', 'yes', '1')


def find_file_location(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
