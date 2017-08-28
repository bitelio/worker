from . import db
from . import log


def one(collection, item_id):
    result = db[collection].delete_one({'Id': doc_id})
    log.info(f'Item removed: ({item_id})')


def many(collection, query):
    db[collection].delete_many(query)
    # log.info(f'{result.deleted_count} items removed')


def card(card_id):
    one('cards', card_id)
    many('events', {'CardId': card_id})
    log.info(f'Card removed: {card_id}')
