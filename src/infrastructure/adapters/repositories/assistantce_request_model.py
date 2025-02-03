from dataclasses import dataclass
from uuid import UUID

from src.domain.entities import AssistanceRequest as EntityAssistanceRequest
from src.domain.value_objects import Status, Topic


@dataclass(frozen=True)
class AssistanceRequestModel:
    id: str
    topic: str
    description: str
    status: str

    @classmethod
    def from_document(cls, document: dict[str, str]) -> "AssistanceRequestModel":
        return cls(
            id=document["_id"],
            description=document["description"],
            topic=document["topic"],
            status=document["status"],
        )

    @classmethod
    def from_entity(cls, entity: EntityAssistanceRequest) -> "AssistanceRequestModel":
        return cls(
            id=str(entity.id),
            topic=entity.topic.value,
            description=entity.description,
            status=entity.status.value,
        )

    def to_document(self) -> dict[str, str]:
        return {
            "_id": self.id,
            "description": self.description,
            "topic": self.topic,
            "status": self.status,
        }

    def to_entity(self) -> EntityAssistanceRequest:
        return EntityAssistanceRequest.stored(
            id=UUID(self.id),
            description=self.description,
            topic=Topic(self.topic),
            status=Status(self.status),
        )

    def get_by_id(self) -> dict[str, str]:
        return {"_id": self.id}

    @staticmethod
    def get_by_id_filter(id: UUID) -> dict[str, str]:
        return {"_id": str(id)}
