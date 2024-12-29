from typing import TypeVar

from tests.unit.seedwork.infrastructure.events.fakes.concrete_event import ConcreteEvent

from src.seedwork.infrastructure.events import Event, EventHandler, EventsDispatcher


TEvent = TypeVar("TEvent", bound=Event)


class CustomDispatcher(EventsDispatcher):
    def __init__(self, event_handlers: dict[TEvent, list[EventHandler[TEvent]]]):
        super().__init__(event_handlers=event_handlers)

    def get_concrete_event(self, event: Event) -> Event:
        if event.type == "concrete_event":
            return ConcreteEvent.from_event(event=event)
        raise ValueError("Event not found")
