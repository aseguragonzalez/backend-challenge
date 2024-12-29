from dataclasses import dataclass
from uuid import UUID

from src.seedwork.infrastructure.events import Event


@dataclass(frozen=True, init=False)
class AssistanceFailedEvent(Event):
    def __init__(self, payload: dict[str, str]):
        super().__init__(type="assistance_created_event", payload=payload)

    @property
    def assistance_id(self) -> UUID:
        if "id" not in self.payload:
            raise ValueError("id is missing from the payload")

        return UUID(str(self.payload["id"]))
