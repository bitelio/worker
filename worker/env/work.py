from redis import StrictRedis
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from worker import env


env.cache = StrictRedis()
env.mongo = MongoClient()
env.db = env.mongo.debug
env.log.setLevel("DEBUG")
