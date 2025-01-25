from pika import BlockingConnection

from src.seedwork.infrastructure.queues import Producer
from src.seedwork.infrastructure.queues.rabbit_mq.producer_settings import ProducerSettings


class RabbitMqProducer(Producer):
    def __init__(self, connection: BlockingConnection, settings: ProducerSettings) -> None:
        self._channel = connection.channel()
        self._settings = settings

    def __enter__(self) -> "RabbitMqProducer":
        return self

    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb: object) -> None:
        if self._channel.is_open:
            self._channel.close()

    def send_message(self, body: bytes) -> None:
        self._channel.basic_publish(
            exchange=self._settings.exchange,
            routing_key=self._settings.routing_key,
            body=body,
        )
