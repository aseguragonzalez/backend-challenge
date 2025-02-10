from abc import ABC, abstractmethod

from src.seedwork.infrastructure.events.event import Event
from src.seedwork.infrastructure.events.event_handler import EventHandler


class EventsDispatcher(ABC):
    def __init__(self, event_handlers: dict[type[Event], list[EventHandler[Event]]] = {}):
        self._event_handlers = event_handlers

    def dispatch(self, event: Event) -> None:
        concrete_event = self.get_concrete_event(event)
        concrete_event_type: type[Event] = type(concrete_event)
        event_handlers = self._event_handlers.get(concrete_event_type, [])
        [handler.handle(event=concrete_event) for handler in event_handlers]

    @abstractmethod
    def get_concrete_event(self, event: Event) -> Event:
        raise NotImplementedError
