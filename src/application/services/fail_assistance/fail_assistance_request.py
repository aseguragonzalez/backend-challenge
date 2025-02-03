from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class FailAssistanceRequest:
    id: UUID
