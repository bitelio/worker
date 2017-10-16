from schematics.types import IntType, StringType, BooleanType

from .models import KanbanModel
from .types import KanbanIdType, LowerCaseType


class User(KanbanModel):
    BoardId = KanbanIdType()
    Enabled = BooleanType()
    FullName = StringType()
    GravatarLink = StringType()
    Id = KanbanIdType()
    Role = IntType(choices=[1, 2, 3, 4])
    UserName = LowerCaseType()
