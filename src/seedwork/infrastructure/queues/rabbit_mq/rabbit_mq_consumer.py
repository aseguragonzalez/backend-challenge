from collections.abc import Callable

from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from src.seedwork.infrastructure.queues import Consumer
from src.seedwork.infrastructure.queues.exceptions import RecoverableError, UnrecoverableError
from src.seedwork.infrastructure.queues.rabbit_mq import ConsumerSettings


class RabbitMqConsumer(Consumer):
    def __init__(self, connection: BlockingConnection, settings: ConsumerSettings) -> None:
        self._settings = settings
        self._channel = connection.channel()
        self._consumer_tag: str | None = None

    def __enter__(self) -> "RabbitMqConsumer":
        return self

    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb: object) -> None:
        if self._channel.is_open:
            self._channel.close()

    def start(self, message_handler: Callable[[bytes], None]) -> None:
        message_callback = self._message_callback(message_handler)
        self._consumer_tag = self._channel.basic_consume(
            queue=self._settings.queue_name,
            on_message_callback=message_callback,
        )
        self._channel.start_consuming()

    def cancel(self) -> None:
        if self._channel.is_open:
            self._channel.stop_consuming(consumer_tag=self._consumer_tag)

    def _message_callback(
        self, message_handler: Callable[[bytes], None]
    ) -> Callable[[BlockingChannel, Basic.Deliver, BasicProperties, bytes], None]:
        def message_callback(channel: BlockingChannel, method: Basic.Deliver, _: BasicProperties, body: bytes) -> None:
            try:
                message_handler(body)
            except RecoverableError:
                channel.basic_nack(delivery_tag=method.delivery_tag)
            except UnrecoverableError:
                channel.basic_ack(delivery_tag=method.delivery_tag)
            else:
                channel.basic_ack(delivery_tag=method.delivery_tag)

        return message_callback
