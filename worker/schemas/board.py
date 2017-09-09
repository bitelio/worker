from schematics.types import ListType
from schematics.types import IntType
from schematics.types import StringType
from schematics.types import BooleanType
from schematics.models import Model

from .types import KanbanIdType


class Board(Model):
    ArchiveTopLevelLaneId = IntType()
    AvailableTags = ListType(StringType)
    BacklogTopLevelLaneId = IntType()
    Id = KanbanIdType()
    Title = StringType()
    TopLevelLaneIds = ListType(KanbanIdType)
    Version = IntType()
    Reindex = BooleanType(default=False)
