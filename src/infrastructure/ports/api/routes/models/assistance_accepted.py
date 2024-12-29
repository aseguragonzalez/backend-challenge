from uuid import UUID

from pydantic import BaseModel, Field

from src.domain.value_objects import Status


class AssistanceAccepted(BaseModel):
    id: UUID = Field(
        title="Assistance request ID.",
        description="Assistance request ID generated by the system.",
        examples=["649757dcee7d6681992a9c22"],
    )
    status: Status = Field(
        title="Request status",
        description="Indicates the current status of the request.",
        examples=["accepted", "succeeded", "failed"],
    )
    link: str = Field(
        title="Request link",
        description="Link associated with the request.",
        examples=["/api/assistances/649757dcee7d6681992a9c22"],
    )

    @staticmethod
    def build(id: UUID) -> "AssistanceAccepted":
        return AssistanceAccepted(id=id, status=Status.Accepted, link=f"/api/assistances/{id}")