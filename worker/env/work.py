from redis import StrictRedis
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from structlog.dev import ConsoleRenderer

from worker import env


env.cache = StrictRedis()
env.mongo = MongoClient()
env.db = env.mongo.debug
env.log.setLevel("DEBUG")
env.processors.append(ConsoleRenderer())
env.configure(processors=env.processors)
