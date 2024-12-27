from uuid import UUID

from pydantic import BaseModel

from src.domain.value_objects import Status


class AssistanceAccepted(BaseModel):
    id: UUID
    status: Status
    link: str

    @staticmethod
    def build(id: UUID) -> "AssistanceAccepted":
        return AssistanceAccepted(id=id, status=Status.Accepted, link=f"/api/assistances/{id}")
