from fastapi import status

from src.infrastructure.ports.api.responses import ResponseBase
from src.infrastructure.ports.api.routes.models import AssistanceAccepted


class CreatedRequestResponse(ResponseBase):
    def __init__(self, model: AssistanceAccepted):
        super().__init__(
            status_code=status.HTTP_202_ACCEPTED,
            content=model,
            headers={},
        )
