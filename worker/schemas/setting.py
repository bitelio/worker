from schematics.types import DictType
from schematics.types import ListType
from schematics.types import StringType
from schematics.types import BooleanType
from schematics.models import Model

from .types import KanbanIdType


class Setting(Model):
    Id = KanbanIdType()
    Holidays = ListType(StringType, default=[], required=False)
    Timezone = StringType(default='UTC', required=False)
    Update = BooleanType(default=False, required=False)
    OfficeHours = DictType(StringType, required=False,
                           default={'Open': '8:00', 'Close': '16:00'})
