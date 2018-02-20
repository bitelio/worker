from schematics.types import IntType
from schematics.types import ListType
from schematics.types import StringType

from .models import KanbanModel
from .types import KanbanIdType


class Lane(KanbanModel):
    BoardId = KanbanIdType()
    ChildLaneIds = ListType(KanbanIdType)
    Height = IntType(min_value=0)
    Id = KanbanIdType()
    Index = IntType()
    Left = IntType(min_value=0)
    Orientation = IntType()
    ParentLaneId = KanbanIdType(required=False)
    SiblingLaneIds = ListType(KanbanIdType)
    Title = StringType()
    Top = IntType(min_value=0)
    Width = IntType(min_value=0)

    def __init__(self, raw_data, *args, **kwargs):
        for attr in ["top", "height", "left", "width"]:
            raw_data[attr.capitalize()] = getattr(raw_data, attr)
        super().__init__(raw_data, *args, **kwargs)
