from schematics.models import Model
from schematics.types import IntType
from schematics.types import ListType
from schematics.types import ModelType
from schematics.types import StringType
from schematics.types import BooleanType
from schematics.types import DateTimeType

from .models import KanbanModel
from .types import KanbanIdType


class Change(Model):
    FieldName = StringType()
    NewValue = StringType()
    OldValue = StringType()


class Event(KanbanModel):
    AssignedUserId = KanbanIdType(required=False)
    BoardId = KanbanIdType()
    BoardIdMove = KanbanIdType(required=False)
    CardId = KanbanIdType()
    Changes = ListType(ModelType(Change), required=False)
    Comment = StringType(required=False)
    CommentText = StringType(required=False)
    DateTime = DateTimeType()
    FromLaneId = KanbanIdType(required=False)
    IsUnassigning = BooleanType(required=False)
    ToLaneId = KanbanIdType(required=False)
    Type = StringType()
    UserId = KanbanIdType()
    WipOverrideComment = KanbanIdType(required=False)
    class Options:
        serialize_when_none=False
