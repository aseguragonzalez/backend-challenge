from src.infrastructure.ports.subscriber.events import (
    AssistanceCreatedEvent,
    AssistanceFailedEvent,
    AssistanceSucceededEvent,
)
from src.seedwork.infrastructure.events import Event, EventHandler, EventsDispatcher


class CustomDispatcher(EventsDispatcher):
    def __init__(self, event_handlers: dict[type[Event], list[EventHandler[Event]]]):
        super().__init__(event_handlers=event_handlers)

    def get_concrete_event(self, event: Event) -> Event:
        if event.type == "assistance_request_created":
            return AssistanceCreatedEvent.from_event(event=event)
        if event.type == "assistance_request_failed":
            return AssistanceFailedEvent.from_event(event=event)
        if event.type == "assistance_request_succeeded":
            return AssistanceSucceededEvent.from_event(event=event)
        return event
