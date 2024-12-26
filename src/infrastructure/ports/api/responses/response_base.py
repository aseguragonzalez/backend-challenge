from typing import Any
from uuid import UUID

from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ResponseBase(JSONResponse):
    def render(self, content: Any) -> bytes:
        if isinstance(content, BaseModel):
            content = content.model_dump()

        if isinstance(content, dict):
            for key, value in content.items():
                if isinstance(value, UUID):
                    content[key] = str(value)

        return super().render(content)
