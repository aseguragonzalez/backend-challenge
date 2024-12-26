from typing import Any
from uuid import UUID

from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.infrastructure.ports.api.models import BadRequestError, NotFoundError


class ResponseBase(JSONResponse):
    def render(self, content: Any) -> bytes:
        if isinstance(content, BaseModel):
            content = content.model_dump()

        if isinstance(content, dict):
            for key, value in content.items():
                if isinstance(value, UUID):
                    content[key] = str(value)

        return super().render(content)


class BadRequestResponse(ResponseBase):
    def __init__(self, model: BadRequestError) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, content=model)


class NotFoundResponse(ResponseBase):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, content=NotFoundError())
