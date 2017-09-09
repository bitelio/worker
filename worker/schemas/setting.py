from schematics.types import ListType
from schematics.types import StringType
from schematics.types import BooleanType
from schematics.types import DateTimeType
from schematics.models import Model

from .types import KanbanIdType


class Setting(Model):
    Id = KanbanIdType()
    Holidays = ListType(DateTimeType, default=[], required=False)
    Timezone = StringType(default='UTC', required=False)
    Update = BooleanType(default=False, required=False)
    OfficeHours = ListType(StringType, default=['8:00', '16:00'],
                           required=False)
