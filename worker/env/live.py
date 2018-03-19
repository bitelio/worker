from os import getenv
from sys import stdout
from redis import StrictRedis
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from raven.handlers.logging import SentryHandler
from raven.conf import setup_logging
from pythonjsonlogger.jsonlogger import JsonFormatter
from structlog.processors import JSONRenderer
from logging import getLogger, StreamHandler

from worker import env


env.cache = StrictRedis("redis")
env.mongo = MongoClient(getenv("MONGODB"), connectTimeoutMS=30000,
                        socketTimeoutMS=None, socketKeepAlive=True)
env.db = env.mongo.bitelio
env.log.setLevel("INFO")
sentry_handler = SentryHandler(getenv("SENTRY"))
sentry_handler.setLevel("ERROR")
setup_logging(sentry_handler)
env.processors.append(JSONRenderer())
env.configure(processors=env.processors)

leankit = getLogger("leankit")
handler = StreamHandler(stdout)
handler.setFormatter(JsonFormatter())
leankit.addHandler(handler)
