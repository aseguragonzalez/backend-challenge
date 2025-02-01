import json
from base64 import b64encode
from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, Decimal):
            return obj.to_eng_string()
        elif isinstance(obj, bytes):
            return b64encode(obj).decode("utf-8")
        return super().default(obj)
