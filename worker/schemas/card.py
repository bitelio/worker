from schematics.types import IntType
from schematics.types import ListType
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
    Version = IntType(required=True)
