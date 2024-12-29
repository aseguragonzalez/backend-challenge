from src.seedwork.infrastructure.events import EventsPublisher, EventsSubscriber
from src.seedwork.infrastructure.events.queues import QueuePublisher, QueueSubscriber
from src.seedwork.infrastructure.ports.dependency_injection import ServiceProvider


def queue_publisher(sp: ServiceProvider) -> None:
    sp.register_singleton(EventsPublisher, QueuePublisher)


def queue_subscriber(sp: ServiceProvider) -> None:
    sp.register_singleton(EventsSubscriber, QueueSubscriber)
