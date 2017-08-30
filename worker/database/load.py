from . import db


def one(collection, item_id):
    return db[collection].find_one({'Id': item_id}, {'_id': 0})


def many(collection, query=None, projection=None):
    if isinstance(projection, dict) and '_id' not in projection:
        projection.update({'_id': 0})
    return list(db[collection].find(query or {}, projection or {'_id': 0}))


def field(collection, field='Id', query=None):
    projection = {'_id': 0, field: 1} if field is not '_id' else {'_id': 1}
    documents = many(collection, query, projection)
    return [document[field] for document in documents]


def table(collection, key='Id', query=None, projection=None):
    return {doc[key]: doc for doc in many(collection, query, projection)}
