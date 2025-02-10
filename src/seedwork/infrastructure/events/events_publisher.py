from abc import ABC, abstractmethod

from src.seedwork.infrastructure.events.event import Event


class EventsPublisher(ABC):
    @abstractmethod
    def publish(self, events: list[Event]) -> None:
        raise NotImplementedError
