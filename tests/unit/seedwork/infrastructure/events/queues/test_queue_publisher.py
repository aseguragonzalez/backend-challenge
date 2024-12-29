from unittest.mock import Mock

from src.seedwork.infrastructure.events import Event
from src.seedwork.infrastructure.events.queues import QueuePublisher
from src.seedwork.infrastructure.queues import Producer


def test_publish_should_send_an_integration_event(faker):
    event = Event.new(type=faker.word(), payload=faker.pydict())
    producer = Mock(spec=Producer)
    publisher = QueuePublisher(producer=producer)

    publisher.publish(events=[event])

    producer.send_message.assert_called_once_with(event.to_bytes())
