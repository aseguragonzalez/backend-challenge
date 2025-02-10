from dataclasses import dataclass
from uuid import UUID

from src.seedwork.domain.events import DomainEvent


@dataclass(frozen=True, init=False)
class AssistanceRequestFailed(DomainEvent):
    def __init__(self, id: UUID) -> None:
        super().__init__(type="assistance_request_failed", payload={"id": str(id)})

    @classmethod
    def new(cls, id: UUID) -> "AssistanceRequestFailed":
        return cls(id=id)
