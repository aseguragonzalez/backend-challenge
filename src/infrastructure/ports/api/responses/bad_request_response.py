from fastapi import status

from src.infrastructure.ports.api.models import BadRequestError
from src.infrastructure.ports.api.responses.response_base import ResponseBase


class BadRequestResponse(ResponseBase):
    def __init__(self, model: BadRequestError) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, content=model)
