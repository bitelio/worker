from schematics.types import IntType
from schematics.types import ListType
from schematics.types import StringType

from .models import KanbanModel
from .types import KanbanIdType


class Lane(KanbanModel):
    BoardId = KanbanIdType()
    ChildLaneIds = ListType(KanbanIdType)
    Id = KanbanIdType()
    Index = IntType()
    LaneState = StringType()
    Orientation = IntType()
    ParentLaneId = KanbanIdType(required=False)
    SiblingLaneIds = ListType(KanbanIdType)
    Title = StringType()
    Width = IntType()
