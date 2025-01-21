from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True)
class DomainEvent(ABC):
    type: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    id: UUID = field(default_factory=uuid4)
    payload: dict[str, Any] = field(default_factory=dict)
    version: str = field(default="1.0")
