import os


def str2bool(str):
    return str.lower() in ('True', 'true', 'yes', '1')


def find_file_location(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
