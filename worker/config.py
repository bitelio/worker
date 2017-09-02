import os


LOGGING = os.getenv('LOGGING', 'INFO')
MONGODB = os.getenv('MONGODB_URI', 'localhost')
DATABASE = os.getenv('DATABASE', 'kanban')
THROTTLE = os.getenv('THROTTLE', 60)
TIMEZONE = os.getenv('TIMEZONE', 'Europe/Berlin')
