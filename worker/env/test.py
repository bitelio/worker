from fakeredis import FakeStrictRedis
from mongomock import MongoClient, DuplicateKeyError

from . import log


cache = FakeStrictRedis()
mongo = MongoClient()
db = mongo.bitelio
log.setLevel("WARNING")
