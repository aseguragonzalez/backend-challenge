import json
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any
from uuid import UUID


class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self, *args: tuple[str, Any], **kwargs: dict[str, Any]) -> None:
        super().__init__(object_hook=self.object_hook, *args, **kwargs)  # type: ignore

    def object_hook(self, obj: Any) -> Any:
        for key, value in obj.items():
            if isinstance(value, str):
                try:
                    obj[key] = datetime.fromisoformat(value)
                except ValueError:
                    pass

                try:
                    obj[key] = UUID(value)
                except ValueError:
                    pass

                try:
                    obj[key] = Decimal(value)
                except (InvalidOperation, TypeError, ValueError):
                    pass

            if isinstance(value, bytes):
                obj[key] = value.decode("utf-8")

        return obj
