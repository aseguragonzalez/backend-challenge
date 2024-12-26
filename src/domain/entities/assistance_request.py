from typing import Any
from uuid import UUID, uuid4

from src.domain.exceptions import UnavailableChangeOfStatusError
from src.domain.value_objects import Status, Topic


class AssistanceRequest:
    def __init__(self, id: UUID, topic: Topic, description: str, status: Status):
        self._id = id
        self._topic = topic
        self._description = description
        self._status = status

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def topic(self) -> Topic:
        return self._topic

    @property
    def description(self) -> str:
        return self._description

    @property
    def status(self) -> Status:
        return self._status

    def failed(self) -> None:
        if self._status != Status.Accepted:
            raise UnavailableChangeOfStatusError()
        self._status = Status.Failed
        return None

    def succeeded(self) -> None:
        if self._status != Status.Accepted:
            raise UnavailableChangeOfStatusError()
        self._status = Status.Succeeded
        return None

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, AssistanceRequest):
            return False

        return self.id == other.id

    @classmethod
    def new(cls, topic: Topic, description: str, id: UUID = uuid4()) -> "AssistanceRequest":
        return cls(id=id, topic=topic, description=description, status=Status.Accepted)

    @classmethod
    def stored(cls, id: UUID, topic: Topic, description: str, status: Status) -> "AssistanceRequest":
        return cls(id=id, topic=topic, description=description, status=status)
