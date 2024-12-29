from typing import Any
from uuid import UUID, uuid4

from src.domain.events import AssistanceRequestCreated, AssistanceRequestFailed, AssistanceRequestSucceeded
from src.domain.exceptions import UnavailableChangeOfStatusError
from src.domain.value_objects import Status, Topic
from src.seedwork.domain.entities import AggregateRoot
from src.seedwork.domain.events import DomainEvent


class AssistanceRequest(AggregateRoot[UUID]):
    def __init__(self, id: UUID, topic: Topic, description: str, status: Status, events: list[DomainEvent]) -> None:
        super().__init__(id=id, events=events)
        self._topic = topic
        self._description = description
        self._status = status

    @property
    def topic(self) -> Topic:
        return self._topic

    @property
    def description(self) -> str:
        return self._description

    @property
    def status(self) -> Status:
        return self._status

    def fail(self) -> None:
        if self._status != Status.Accepted:
            raise UnavailableChangeOfStatusError()
        self._status = Status.Failed
        self.add_event(AssistanceRequestFailed.new(id=self.id))
        return None

    def success(self) -> None:
        if self._status != Status.Accepted:
            raise UnavailableChangeOfStatusError()
        self._status = Status.Succeeded
        self.add_event(AssistanceRequestSucceeded.new(id=self.id))
        return None

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, AssistanceRequest):
            return False

        return self.id == other.id

    @classmethod
    def new(cls, topic: Topic, description: str, id: UUID = uuid4()) -> "AssistanceRequest":
        created_event = AssistanceRequestCreated.new(id=id)
        return cls(id=id, topic=topic, description=description, status=Status.Accepted, events=[created_event])

    @classmethod
    def stored(cls, id: UUID, topic: Topic, description: str, status: Status) -> "AssistanceRequest":
        return cls(id=id, topic=topic, description=description, status=status, events=[])
