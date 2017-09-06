import logging
import pymongo

from .. import config


log = logging.getLogger(__name__)


log.info(f'Connecting to {config.MONGODB}')
client = pymongo.MongoClient(config.MONGODB)
try:
    db = client.get_default_database()
except pymongo.errors.ConfigurationError:
    db = client[config.DATABASE]
