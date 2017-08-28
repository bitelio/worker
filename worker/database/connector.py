import pymongo

from .. import config


client = pymongo.MongoClient(config.MONGODB)
db = None
# try:
    # db = client.get_default_database()
# except pymongo.errors.ConfigurationError:
    # db = client[config.DATABASE]
