from pickle import dumps
from hashlib import sha1
from schematics.models import Model
from schematics.exceptions import DataError


class KanbanModel(Model):
    def __init__(self, raw_data, *args, **kwargs):
        try:
            raw_data["BoardId"] = raw_data.board.id
        except KeyError:
            raise DataError("A reference to the Kanban board is required")
        super().__init__(raw_data, *args, **kwargs)

    @property
    def hash(self):
        return sha1(dumps(self.to_native())).hexdigest()[:6]
