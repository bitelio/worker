import logging

from . import mongo


log = logging.getLogger(__name__)


def one(collection, item_id):
    mongo.db[collection].delete_one({'Id': item_id})
    log.info(f'Item removed: ({item_id})')


def many(collection, query):
    mongo.db[collection].delete_many(query)


def card(card_id):
    one('cards', card_id)
    many('events', {'CardId': card_id})
    log.info(f'Card removed: {card_id}')