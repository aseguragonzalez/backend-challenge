from dataclasses import dataclass, field
from uuid import UUID, uuid4

from src.domain.value_objects import Topic


@dataclass(frozen=True)
class CreateAssistanceRequest:
    description: str
    topic: Topic
    id: UUID = field(default_factory=uuid4)
