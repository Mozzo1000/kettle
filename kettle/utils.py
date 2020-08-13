import os
from PyQt5.QtGui import QIcon

basedir = os.path.abspath(os.path.dirname(__file__))


def str2bool(str):
    return str.lower() in ('True', 'true', 'yes', '1')
