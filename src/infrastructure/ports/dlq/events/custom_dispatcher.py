from typing import TypeVar

from src.infrastructure.ports.dlq.events import AssistanceCreatedEvent
from src.seedwork.infrastructure.events import Event, EventHandler, EventsDispatcher


TEvent = TypeVar("TEvent", bound=Event)


class CustomDispatcher(EventsDispatcher):
    def __init__(self, event_handlers: dict[TEvent, list[EventHandler[TEvent]]]):
        super().__init__(event_handlers=event_handlers)

    def get_concrete_event(self, event: Event) -> Event:
        if event.type == "assistance_request_created":
            return AssistanceCreatedEvent.from_event(event=event)
        return event
