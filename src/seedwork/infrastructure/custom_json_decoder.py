import json
from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID


class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self, *args: tuple[str, Any], **kwargs: dict[str, Any]) -> None:
        super().__init__(object_hook=self.object_hook, *args, **kwargs)  # type: ignore

    def object_hook(self, obj: Any) -> Any:
        for key, value in obj.items():
            if isinstance(value, str) and value.startswith("d|"):
                obj[key] = Decimal(value.replace("d|", ""))
            elif isinstance(value, bytes):
                obj[key] = value.decode("utf-8")
            elif isinstance(value, str):
                try:
                    obj[key] = datetime.fromisoformat(value)
                except ValueError:
                    pass
                try:
                    obj[key] = UUID(value)
                except ValueError:
                    pass
        return obj
