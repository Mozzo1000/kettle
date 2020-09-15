import os
import math
from PyQt5.QtGui import QIcon

basedir = os.path.abspath(os.path.dirname(__file__))


def str2bool(str):
    return str.lower() in ('True', 'true', 'yes', '1')


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])
