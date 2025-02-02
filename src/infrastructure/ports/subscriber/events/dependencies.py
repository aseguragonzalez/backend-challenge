from src.domain.services import ChannelsService
from src.domain.value_objects import Topic
from src.infrastructure.adapters.services import EmailChannel, SlackChannel
from src.infrastructure.ports.subscriber.events import (
    AssistanceCreatedEvent,
    AssistanceCreatedEventHandler,
    AssistanceFailedEvent,
    AssistanceFailedEventHandler,
    AssistanceSucceededEvent,
    AssistanceSucceededEventHandler,
    CustomDispatcher,
)
from src.seedwork.infrastructure.events import EventsDispatcher
from src.seedwork.infrastructure.ports.dependency_injection import ServiceProvider


def channel_service(sp: ServiceProvider) -> None:
    def configure(sp: ServiceProvider):
        channels_map = {
            Topic.Pricing.value: sp.get(EmailChannel),
            Topic.Sales.value: sp.get(SlackChannel),
        }
        return ChannelsService(channels_map=channels_map)

    sp.register_singleton(ChannelsService, configure)


def event_handlers(sp: ServiceProvider) -> None:
    sp.register_singleton(AssistanceCreatedEventHandler, AssistanceCreatedEventHandler)
    sp.register_singleton(AssistanceFailedEventHandler, AssistanceFailedEventHandler)
    sp.register_singleton(AssistanceSucceededEventHandler, AssistanceSucceededEventHandler)


def events_dispatcher(sp: ServiceProvider) -> None:
    def configure(sp: ServiceProvider):
        event_handlers: dict[type, list] = {
            AssistanceCreatedEvent: [sp.get(AssistanceCreatedEventHandler)],
            AssistanceFailedEvent: [sp.get(AssistanceFailedEventHandler)],
            AssistanceSucceededEvent: [sp.get(AssistanceSucceededEventHandler)],
        }
        return CustomDispatcher(event_handlers=event_handlers)

    sp.register_singleton(EventsDispatcher, configure)
