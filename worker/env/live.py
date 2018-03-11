from os import getenv
from redis import StrictRedis
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from logging.handlers import RotatingFileHandler
# from sendgrid import SendGridAPIClient
from raven.handlers.logging import SentryHandler
from raven.conf import setup_logging

from worker import env


env.cache = StrictRedis("redis")
env.mongo = MongoClient(getenv("MONGODB"), connectTimeoutMS=30000,
                        socketTimeoutMS=None, socketKeepAlive=True)
env.db = env.mongo.bitelio
# sg = SendGridAPIClient(apikey=config.SENDGRID['APIKEY'])
env.log.setLevel("INFO")
sentry_handler = SentryHandler(getenv("SENTRY"))
sentry_handler.setLevel("ERROR")
setup_logging(sentry_handler)
rotating_handler = RotatingFileHandler("/var/log/worker.log", "a", 5**10, 2)
rotating_handler.setFormatter(env.formatter)
env.log.addHandler(rotating_handler)
