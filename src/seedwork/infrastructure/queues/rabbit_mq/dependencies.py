from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from src.seedwork.infrastructure.ports.dependency_injection import ServiceProvider
from src.seedwork.infrastructure.queues import Consumer, Producer
from src.seedwork.infrastructure.queues.rabbit_mq import RabbitMqConsumer, RabbitMqProducer, RabbitMqSettings


def rabbit_mq_consumer(sp: ServiceProvider) -> None:
    sp.register_context_managed_singleton(Consumer, RabbitMqConsumer)  # type: ignore


def rabbit_mq_producer(sp: ServiceProvider) -> None:
    sp.register_context_managed_singleton(Producer, RabbitMqProducer)  # type: ignore


def rabbit_mq_connection(sp: ServiceProvider) -> None:
    def configure(sp: ServiceProvider) -> BlockingConnection:
        settings = sp.get(RabbitMqSettings)
        credentials = PlainCredentials(
            username=settings.username,
            password=settings.password,
            erase_on_connect=False,
        )
        connection_parameters = ConnectionParameters(
            host=settings.host,
            port=settings.port,
            credentials=credentials,
        )
        return BlockingConnection(parameters=connection_parameters)

    sp.register_singleton(BlockingConnection, configure)
