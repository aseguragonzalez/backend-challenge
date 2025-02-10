from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.seedwork.infrastructure.events.event import Event


TEvent = TypeVar("TEvent", bound=Event)


class EventsDb(ABC, Generic[TEvent]):
    @abstractmethod
    def exist(self, event: TEvent) -> bool:
        raise NotImplementedError

    @abstractmethod
    def create(self, event: TEvent) -> None:
        raise NotImplementedError
