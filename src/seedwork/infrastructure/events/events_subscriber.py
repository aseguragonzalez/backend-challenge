from abc import ABC, abstractmethod
from typing import TypeVar

from src.seedwork.infrastructure.events.event import Event


TEvent = TypeVar("TEvent", bound=Event)


class EventsSubscriber(ABC):
    @abstractmethod
    def start_listening(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop_listening(self) -> None:
        raise NotImplementedError
