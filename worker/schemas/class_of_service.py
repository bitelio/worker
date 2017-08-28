from schematics.types import StringType
from schematics.types import BooleanType

from .models import KanbanModel
from .types import KanbanIdType


class ClassOfService(KanbanModel):
    BoardId = KanbanIdType()
    ColorHex = StringType()
    Id = KanbanIdType()
    Title = StringType()
    UseColor = BooleanType()
