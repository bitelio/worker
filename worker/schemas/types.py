from datetime import datetime, date
from schematics.types import IntType, DateType, StringType
from schematics.exceptions import ValidationError


class KanbanIdType(IntType):  # pragma: no cover
    MESSAGES = {'id_length': "Kanban ids must have 8 or 9 digits"}

    def to_native(self, value, *args, **kwargs):
        value = super().to_native(value, *args, **kwargs)

        if value is 0:
            return None
        elif 7 < len(str(value)) < 10:
            return value
        else:
            raise ValidationError(self.messages['id_length'])


class LowerCaseType(StringType):
    def to_native(self, value, context=None):
        native = super().to_native(value, context)
        return native.lower() if isinstance(native, str) else native


class MongoDateType(DateType):  # pragma: no cover
    SERIALIZED_FORMAT = '%Y-%m-%dT%H:%M:%S'

    def to_native(self, value, *args, **kwargs):
        if isinstance(value, date):
            return datetime.combine(value, datetime.min.time())
        else:
            value = super().to_native(value, *args, **kwargs)
