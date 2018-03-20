from os import getenv
from sys import stdout
from redis import StrictRedis
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from logging.handlers import RotatingFileHandler
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
rotating_handler = RotatingFileHandler("/var/log/worker.log", "a", 5**10, 2)
env.log.addHandler(rotating_handler)
sentry_handler = SentryHandler(getenv("SENTRY"))
sentry_handler.setLevel("ERROR")
setup_logging(sentry_handler)
env.processors.append(JSONRenderer())
env.configure(processors=env.processors)
env.log.setLevel("INFO")

leankit = getLogger("leankit")
stream_handler = StreamHandler(stdout)
stream_handler.setFormatter(JsonFormatter())
leankit.addHandler(stream_handler)
leankit.addHandler(rotating_handler)
leankit.setLevel("WARNING")
