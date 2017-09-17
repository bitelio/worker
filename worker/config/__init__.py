from os import path
from os import getenv
from yaml import safe_load


def load(filename):
    with open(path.join(path.dirname(__file__), filename + '.yml')) as data:
        return safe_load(data)


LOGGING = getenv('LOGGING', 'INFO')
MONGODB = getenv('MONGODB_URI', 'mongodb://localhost/kanban')
THROTTLE = getenv('THROTTLE', 60)
TIMEZONE = getenv('TIMEZONE', 'Europe/Berlin')
SENTRY = getenv('SENTRY_DSN', '')
SENDGRID = {'APIKEY': getenv('SENDGRID_APIKEY'),
            'SENDER': getenv('SENDGRID_SENDER'),
            'RECEIVER': getenv('SENDGRID_RECEIVER')}

collections = load('collections')
logging = load('logging')
