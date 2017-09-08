import logging
from pytz import timezone as tz
from bson.codec_options import CodecOptions

from . import mongo


log = logging.getLogger(__name__)


def one(collection, item_id, timezone=None):
    log.debug(f'Loading document {item_id} from {collection}')
    return _cursor_(collection, timezone).find_one({'Id': item_id}, {'_id': 0})


def many(collection, query=None, projection=None, timezone=None, sort=None):
    if isinstance(projection, dict) and '_id' not in projection:
        projection.update({'_id': 0})
    items = collection.replace('_', ' ')
    if query:
        log.debug(f'Loading {items} matching {query}')
    else:
        log.debug(f'Loading all {items}')
    args = (query or {}, projection or {'_id': 0})
    results = _cursor_(collection, timezone).find(*args)
    if sort:
        results.sort(sort)
    return list(results)


def field(collection, field='Id', query=None):
    projection = {'_id': 0, field: 1} if field is not '_id' else {'_id': 1}
    documents = many(collection, query, projection)
    return [document[field] for document in documents if field in document]


def table(collection, key='Id', query=None, projection=None, timezone=None):
    return {doc[key]: doc for doc in
            many(collection, query, projection, timezone) if key in doc}


def _cursor_(collection, timezone):
    if timezone:
        codec_options = CodecOptions(tz_aware=True, tzinfo=tz(timezone))
        return mongo.db[collection].with_options(codec_options)
    else:
        return mongo.db[collection]

