from os import path
from os import getenv
from yaml import safe_load


def load(filename):
    with open(path.join(path.dirname(__file__), filename + '.yml')) as data:
        return safe_load(data)


LOGGING = getenv('LOGGING', 'INFO')
MONGODB = getenv('MONGODB_URI', 'localhost')
DATABASE = getenv('DATABASE', 'kanban')
THROTTLE = getenv('THROTTLE', 60)
TIMEZONE = getenv('TIMEZONE', 'Europe/Berlin')

collections = load('collections')
logging = load('logging')
