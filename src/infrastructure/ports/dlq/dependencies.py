import os

from src.application.dependencies import fail_assistance_service
from src.infrastructure.adapters.dependencies import client_session, mongo_client, unit_of_work
from src.infrastructure.adapters.repositories import MongoDbSettings
from src.infrastructure.adapters.repositories.dependencies import (
    assistances_repository,
    mongo_db_assistances_repositories,
)
from src.infrastructure.ports.dlq.app import App
from src.infrastructure.ports.dlq.events.dependencies import event_handlers, events_dispatcher
from src.seedwork.infrastructure.events.mongo_db import MongoDbEventsDbSettings
from src.seedwork.infrastructure.events.mongo_db.dependencies import mongo_db_events_db
from src.seedwork.infrastructure.events.queues.dependencies import queue_publisher, queue_subscriber
from src.seedwork.infrastructure.ports.dependency_injection import ServiceProvider
from src.seedwork.infrastructure.queues.rabbit_mq import ConsumerSettings, ProducerSettings, RabbitMqSettings
from src.seedwork.infrastructure.queues.rabbit_mq.dependencies import (
    rabbit_mq_connection,
    rabbit_mq_consumer,
    rabbit_mq_producer,
)


def _assistance_db_settings(sp: ServiceProvider) -> None:
    settings = MongoDbSettings(
        database_url=os.getenv("ASSISTANCE_DATABASE_URL"),
        database_name=os.getenv("ASSISTANCE_DATABASE_NAME"),
        collection_name=os.getenv("ASSISTANCE_COLLECTION_NAME"),
    )
    sp.register_singleton(MongoDbSettings, lambda _: settings)


def _mongo_db_events_db_settings(sp: ServiceProvider) -> None:
    settings = MongoDbEventsDbSettings(
        database_url=os.getenv("EVENTS_DATABASE_URL"),
        database_name=os.getenv("EVENTS_DATABASE_NAME"),
        collection_name=os.getenv("PROCESSED_EVENTS_COLLECTION_NAME"),
    )
    sp.register_singleton(MongoDbEventsDbSettings, lambda _: settings)


def _rabbit_mq_settings(sp: ServiceProvider) -> None:
    settings = RabbitMqSettings(
        host=os.getenv("RABBITMQ_HOST"),
        port=os.getenv("RABBITMQ_PORT"),
        username=os.getenv("RABBITMQ_USERNAME"),
        password=os.getenv("RABBITMQ_PASSWORD"),
    )
    sp.register_singleton(RabbitMqSettings, lambda _: settings)


def _consumer_settings(sp: ServiceProvider) -> None:
    settings = ConsumerSettings(queue_name=os.getenv("RABBITMQ_CONSUMER_DLQ_QUEUE_NAME"))
    sp.register_singleton(ConsumerSettings, lambda _: settings)


def _producer_settings(sp: ServiceProvider) -> None:
    settings = ProducerSettings(
        exchange=os.getenv("RABBITMQ_PRODUCER_EXCHANGE_NAME"),
        routing_key=os.getenv("RABBITMQ_PRODUCER_ROUTING_KEY"),
    )
    sp.register_singleton(ProducerSettings, lambda _: settings)


def configure(app: App) -> App:
    app.register(_rabbit_mq_settings)
    app.register(_consumer_settings)
    app.register(_producer_settings)
    app.register(_mongo_db_events_db_settings)
    app.register(_assistance_db_settings)
    app.register(rabbit_mq_connection)
    app.register(rabbit_mq_consumer)
    app.register(rabbit_mq_producer)
    app.register(queue_publisher)
    app.register(queue_subscriber)
    app.register(mongo_client)
    app.register(client_session)
    app.register(events_dispatcher)
    app.register(event_handlers)
    app.register(fail_assistance_service)
    app.register(unit_of_work)
    app.register(assistances_repository)
    app.register(mongo_db_assistances_repositories)
    app.register(mongo_db_events_db)
    return app
