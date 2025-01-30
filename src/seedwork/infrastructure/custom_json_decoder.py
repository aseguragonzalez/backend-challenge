import json
from datetime import datetime
from decimal import Decimal, InvalidOperation
from uuid import UUID


class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        for key, value in obj.items():
            if isinstance(value, str):
                try:
                    obj[key] = datetime.fromisoformat(value)
                except ValueError:
                    pass

            if isinstance(value, str):
                try:
                    obj[key] = UUID(value)
                except ValueError:
                    pass

            if isinstance(value, str):
                try:
                    obj[key] = Decimal(value)
                except (InvalidOperation, TypeError, ValueError):
                    pass

            if isinstance(value, str) and "b'" in value:
                obj[key] = value.decode("utf-8")

        return obj
