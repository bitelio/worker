from re import sub
from importlib import import_module


class Item:
    __slots__ = ["type", "name", "schema", "collection"]

    def __init__(self, i):
        self.type = types[i]
        self.name = names[i]
        self.schema = schemas[i]
        self.collection = collections[i]


types = ['Lane', 'Card', 'User', 'CardType', 'ClassOfService']
names = [sub("([a-z])([A-Z])", "\g<1> \g<2>", _).capitalize() for _ in types]
variables = [name.lower().replace(' ', '_') for name in names]
modules = [import_module('worker.schemas.' + var) for var in variables]
schemas = [getattr(module, name) for module, name in zip(modules, types)]
collections = [var + 's' for var in variables[:-1]] + ['classes_of_service']
items = [Item(i) for i in range(len(types))]
