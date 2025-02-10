from dataclasses import dataclass
from uuid import UUID

from src.seedwork.domain.events import DomainEvent


@dataclass(frozen=True, init=False)
class AssistanceRequestSucceeded(DomainEvent):
    def __init__(self, id: UUID) -> None:
        super().__init__(type="assistance_request_succeeded", payload={"id": str(id)})

    @classmethod
    def new(cls, id: UUID) -> "AssistanceRequestSucceeded":
        return cls(id=id)
