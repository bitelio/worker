from schematics.types import IntType
from schematics.types import ListType
from schematics.types import StringType
from schematics.types import BooleanType
from schematics.models import Model

from .types import KanbanIdType


class Board(Model):
    ArchiveTopLevelLaneId = IntType(required=False)
    AvailableTags = ListType(StringType, required=False)
    BacklogTopLevelLaneId = IntType(required=False)
    Id = KanbanIdType()
    Title = StringType()
    TopLevelLaneIds = ListType(KanbanIdType, required=False)
    Version = IntType(required=False)

    def populate(self):
        data = self.to_native()
        data.update({"Holidays": [], "Timezone": "UTC",
                     "OfficeHours": ["8:00", "16:00"]})
        return data
