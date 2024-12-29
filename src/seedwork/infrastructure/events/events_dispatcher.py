from abc import ABC, abstractmethod
from typing import TypeVar

from src.seedwork.infrastructure.events.event import Event
from src.seedwork.infrastructure.events.event_handler import EventHandler


TEvent = TypeVar("TEvent", bound=Event)


class EventsDispatcher(ABC):
    def __init__(self, event_handlers: dict[TEvent, list[EventHandler[TEvent]]] = {}):
        self._event_handlers = event_handlers

    def dispatch(self, event: Event) -> None:
        concrete_event = self.get_concrete_event(event)
        event_handlers = self._event_handlers.get(type(concrete_event), [])
        [handler.handle(event=concrete_event) for handler in event_handlers]

    @abstractmethod
    def get_concrete_event(self, event: Event) -> Event:
        raise NotImplementedError
