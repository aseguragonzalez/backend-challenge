from src.infrastructure.ports.dlq.events import AssistanceCreatedEvent, AssistanceCreatedEventHandler, CustomDispatcher
from src.seedwork.infrastructure.events import EventsDispatcher
from src.seedwork.infrastructure.ports.dependency_injection import ServiceProvider


def event_handlers(sp: ServiceProvider) -> None:
    sp.register_singleton(AssistanceCreatedEventHandler, AssistanceCreatedEventHandler)


def events_dispatcher(sp: ServiceProvider) -> None:
    def configure(sp: ServiceProvider):
        event_handlers: dict[type, list] = {
            AssistanceCreatedEvent: [sp.get(AssistanceCreatedEventHandler)],
        }
        return CustomDispatcher(event_handlers=event_handlers)

    sp.register_singleton(EventsDispatcher, configure)
