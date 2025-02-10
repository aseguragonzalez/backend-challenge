from src.seedwork.infrastructure.events import Event, EventsPublisher
from src.seedwork.infrastructure.queues import Producer


class QueuePublisher(EventsPublisher):
    def __init__(self, producer: Producer):
        self._producer = producer

    def publish(self, events: list[Event]) -> None:
        [self._producer.send_message(event.to_bytes()) for event in events]
