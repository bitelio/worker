from re import sub
from importlib import import_module


def get(transform, item):
    name = item.__class__.__name__
    return mapping[transform][name]


types = ['Board', 'Lane', 'Card', 'User', 'CardType', 'ClassOfService', 'Event']
names = [sub("([a-z])([A-Z])", "\g<1> \g<2>", _).capitalize() for _ in types]
variables = [name.lower().replace(' ', '_') for name in names]
modules = [import_module('worker.schemas.' + var) for var in variables]
schemas = [getattr(module, name) for module, name in zip(modules, types)]
collections = [var + 's' for var in variables] + ['classes_of_service']
categories = {'name': names, 'collection': collections, 'schema': schemas}
mapping = {key: dict(zip(types, value)) for key, value in categories.items()}
