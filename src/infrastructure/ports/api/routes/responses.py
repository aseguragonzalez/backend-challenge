from uuid import UUID

from fastapi import status
from pydantic import BaseModel

from src.domain.value_objects import Status
from src.infrastructure.ports.api.responses import ResponseBase
from src.infrastructure.ports.api.routes.models import AssistanceRequest


class AssistanceAccepted(BaseModel):
    id: UUID
    status: Status
    link: str

    @staticmethod
    def build(id: UUID) -> "AssistanceAccepted":
        return AssistanceAccepted(id=id, status=Status.Accepted, link=f"/api/assistances/{id}")


class CreatedRequestResponse(ResponseBase):
    def __init__(self, model: AssistanceAccepted):
        super().__init__(
            status_code=status.HTTP_202_ACCEPTED,
            content=model,
            headers={},
        )


class RequestResponse(ResponseBase):
    def __init__(self, model: AssistanceRequest):
        super().__init__(status_code=status.HTTP_200_OK, content=model)
