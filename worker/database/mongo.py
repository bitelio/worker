from logging import getLogger
from pymongo import MongoClient

from .. import config


log = getLogger(__name__)


log.info(f'Connecting to {config.MONGODB}')
client = MongoClient(config.MONGODB, connectTimeoutMS=30000,
                     socketTimeoutMS=None, socketKeepAlive=True)
db = client.get_default_database()
