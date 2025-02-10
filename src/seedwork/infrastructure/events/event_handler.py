from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.seedwork.infrastructure.events.event import Event


TEvent = TypeVar("TEvent", bound=Event)


class EventHandler(ABC, Generic[TEvent]):
    @abstractmethod
    def handle(self, event: TEvent) -> None:
        raise NotImplementedError
