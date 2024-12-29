from fastapi import status

from src.infrastructure.ports.api.models import NotFoundError
from src.infrastructure.ports.api.responses.response_base import ResponseBase


class NotFoundResponse(ResponseBase):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, content=NotFoundError())
