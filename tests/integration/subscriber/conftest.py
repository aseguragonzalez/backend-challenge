import logging

import pytest

from src.infrastructure.adapters.repositories import MongoDbSettings
from src.infrastructure.adapters.services import EmailSettings
from src.infrastructure.ports.subscriber.main import App
from src.seedwork.infrastructure.events.mongo_db import MongoDbEventsDbSettings
from src.seedwork.infrastructure.queues.rabbit_mq import ConsumerSettings, ProducerSettings, RabbitMqSettings


@pytest.fixture(scope="session")
def assistance_db_settings(mongodb_container):
    mongo_db_url = mongodb_container.get_connection_url()
    return MongoDbSettings(
        collection_name="assistances",
        database_name="assistance_db",
        database_url=mongo_db_url,
    )


@pytest.fixture(scope="session")
def consumer_settings(rabbitmq_connection, producer_settings):
    queue = "events"
    with rabbitmq_connection.channel() as channel:
        channel.queue_declare(queue=queue)
        channel.queue_bind(exchange=producer_settings.exchange, queue=queue, routing_key=producer_settings.routing_key)
    return ConsumerSettings(queue_name=queue)


@pytest.fixture(scope="session")
def email_settings(email_server_container):
    return EmailSettings(
        from_email="source@email.com",
        to_email="source@email.com",
        server="smtp",
        port=25,
        username=email_server_container.env["RelayOptions__Login"],
        password=email_server_container.env["RelayOptions__Password"],
    )


@pytest.fixture(scope="session")
def events_db_settings(mongodb_container):
    mongo_db_url = mongodb_container.get_connection_url()
    return MongoDbEventsDbSettings(
        collection_name="events",
        database_name="events_db",
        database_url=mongo_db_url,
    )


@pytest.fixture(scope="session")
def producer_settings(rabbitmq_connection):
    exchange = "events.ex"
    with rabbitmq_connection.channel() as channel:
        channel.exchange_declare(exchange=exchange, exchange_type="direct")
    return ProducerSettings(
        exchange=exchange,
        routing_key="",
    )


@pytest.fixture(scope="session")
def rabbit_mq_settings(rabbitmq_container):
    params = rabbitmq_container.get_connection_params()
    return RabbitMqSettings(
        host=params.host,
        port=params.port,
        username=params.credentials.username,
        password=params.credentials.password,
    )


@pytest.fixture(scope="session")
def app(
    assistance_db_settings,
    consumer_settings,
    email_settings,
    events_db_settings,
    producer_settings,
    rabbit_mq_settings,
):
    app = App(logger=logging.getLogger(__name__))
    app.register(lambda sp: sp.register_singleton(ConsumerSettings, lambda _: consumer_settings))
    app.register(lambda sp: sp.register_singleton(EmailSettings, lambda _: email_settings))
    app.register(lambda sp: sp.register_singleton(MongoDbEventsDbSettings, lambda _: events_db_settings))
    app.register(lambda sp: sp.register_singleton(MongoDbSettings, lambda _: assistance_db_settings))
    app.register(lambda sp: sp.register_singleton(ProducerSettings, lambda _: producer_settings))
    app.register(lambda sp: sp.register_singleton(RabbitMqSettings, lambda _: rabbit_mq_settings))
    return app
