from fastapi import status

from src.infrastructure.ports.api.responses import ResponseBase
from src.infrastructure.ports.api.routes.models import AssistanceRequest


class RequestResponse(ResponseBase):
    def __init__(self, model: AssistanceRequest):
        super().__init__(status_code=status.HTTP_200_OK, content=model)
