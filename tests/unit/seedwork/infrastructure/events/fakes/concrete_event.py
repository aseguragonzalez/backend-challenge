from datetime import datetime
from typing import Any
from uuid import UUID

from src.seedwork.infrastructure.events import Event


class ConcreteEvent(Event):
    def __init__(self, id: UUID, created_at: datetime, version: str, payload: dict[str, Any], type: str):
        super().__init__(id=id, created_at=created_at, version=version, type=type, payload=payload)

    @property
    def payload_id(self) -> UUID:
        if "id" not in self.payload:
            raise ValueError("id is missing from the payload")

        return UUID(str(self.payload["id"]))

    @classmethod
    def from_event(cls, event: Event) -> "ConcreteEvent":
        return cls(
            id=event.id, created_at=event.created_at, version=event.version, payload=event.payload, type=event.type
        )
