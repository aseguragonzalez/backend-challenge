from typing import Generic, TypeVar

from src.seedwork.domain.events import DomainEvent


TId = TypeVar("TId")


class AggregateRoot(Generic[TId]):
    def __init__(self, id: TId, events: list[DomainEvent] = []) -> None:
        self._id = id
        self._events = events

    @property
    def id(self) -> TId:
        return self._id

    @property
    def events(self) -> list[DomainEvent]:
        return self._events

    def add_event(self, event: DomainEvent) -> None:
        self._events.append(event)

    def clear_events(self) -> None:
        self._events = []
