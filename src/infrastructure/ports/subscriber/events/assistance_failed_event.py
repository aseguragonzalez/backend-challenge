from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from src.seedwork.infrastructure.events import Event
from src.seedwork.infrastructure.queues.exceptions import UnrecoverableError


@dataclass(frozen=True, init=False)
class AssistanceFailedEvent(Event):
    def __init__(
        self,
        payload: dict[str, Any],
        id: UUID = uuid4(),
        created_at: datetime = datetime.now(timezone.utc),
        version: str = "1.0",
        type: str = "assistance_request_failed",
    ):
        super().__init__(id=id, created_at=created_at, version=version, type=type, payload=payload)

    @property
    def assistance_id(self) -> UUID:
        if "id" not in self.payload:
            raise UnrecoverableError(message="Assistance id is missing from the payload")

        return UUID(str(self.payload["id"]))

    @classmethod
    def from_event(cls, event: Event) -> "AssistanceFailedEvent":
        return cls(
            id=event.id, created_at=event.created_at, version=event.version, payload=event.payload, type=event.type
        )
