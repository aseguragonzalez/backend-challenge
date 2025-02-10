from uuid import UUID

from src.seedwork.domain.events import DomainEvent


class CustomEvent(DomainEvent):
    def __init__(self, id: UUID) -> None:
        super().__init__(type="fake_event", payload={"id": str(id)})

    @classmethod
    def new(cls, id: UUID) -> "CustomEvent":
        return cls(id=id)
