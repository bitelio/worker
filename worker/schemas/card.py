from schematics.models import Model
from schematics.types import IntType
from schematics.types import ListType
from schematics.types import ModelType
from schematics.types import StringType
from schematics.types import BooleanType
from schematics.types import DateTimeType

from .models import KanbanModel
from .types import KanbanIdType
from .types import MongoDateType


class Card(KanbanModel):
    # Description, ExternalCardID and BlockReason can be an empty string or None
    AssignedUserId = KanbanIdType(required=False)
    BlockReason = StringType(required=False)
    BoardId = KanbanIdType()
    ClassOfServiceId = KanbanIdType(required=False)
    DateArchived = MongoDateType(required=False)
    Description = StringType(required=False)
    DueDate = MongoDateType(required=False)
    ExternalCardID = StringType(required=False)
    Id = KanbanIdType()
    IsBlocked = BooleanType()
    LastActivity = DateTimeType()
    LastMove = DateTimeType()
    Priority = IntType(choices=[0, 1, 2, 3])
    Size = IntType()
    Tags = ListType(StringType)
    Title = StringType()
    TypeId = KanbanIdType()
    Version = IntType()

    def __init__(self, card):
        self.card = card
        super().__init__(card)

    @property
    def hash(self):
        return self.Version


class Change(Model):
    FieldName = StringType()
    NewValue = StringType(required=False)
    OldValue = StringType(required=False)


class Event(Model):
    BoardId = KanbanIdType()
    CardId = KanbanIdType()
    Changes = ListType(ModelType(Change), required=False)
    Comment = StringType(required=False)
    DateTime = DateTimeType()
    FromLaneId = KanbanIdType(required=False)
    TimeDelta = IntType(required=False, min_value=0)
    ToLaneId = KanbanIdType(required=False)
    TRT = IntType(required=False, min_value=0)
    Type = StringType()
    UserId = KanbanIdType()

    class Options:
        serialize_when_none = False
