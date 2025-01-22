import os

from src.application.dependencies import send_assistance_service
from src.infrastructure.adapters.dependencies import client_session, mongo_client, unit_of_work
from src.infrastructure.adapters.repositories import MongoDbSettings
from src.infrastructure.adapters.repositories.dependencies import (
    assistances_repository,
    mongo_db_assistances_repositories,
)
from src.infrastructure.adapters.services.dependencies import (
    email_channel,
    email_settings,
    http_client,
    slack_channel,
    slack_settings,
    smtp_client,
)
from src.infrastructure.ports.subscriber.app import App
from src.infrastructure.ports.subscriber.events.dependencies import channel_service, event_handlers, events_dispatcher
from src.seedwork.infrastructure.events.mongo_db import MongoDbEventsDbSettings
from src.seedwork.infrastructure.events.mongo_db.dependencies import mongo_db_events_db, mongo_db_events_db_publisher
from src.seedwork.infrastructure.events.queues.dependencies import queue_subscriber
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
        collection_name=os.getenv("EVENTS_COLLECTION_NAME"),
        processed_collection_name=os.getenv("EVENTS_PROCESSED_COLLECTION_NAME"),
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
    settings = ConsumerSettings(queue_name=os.getenv("RABBITMQ_CONSUMER_QUEUE_NAME"))
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
    app.register(email_settings)
    app.register(slack_settings)
    app.register(mongo_client)
    app.register(client_session)
    app.register(channel_service)
    app.register(events_dispatcher)
    app.register(event_handlers)
    app.register(send_assistance_service)
    app.register(unit_of_work)
    app.register(assistances_repository)
    app.register(mongo_db_assistances_repositories)
    app.register(email_channel)
    app.register(smtp_client)
    app.register(slack_channel)
    app.register(http_client)
    app.register(rabbit_mq_consumer)
    app.register(rabbit_mq_producer)
    app.register(mongo_db_events_db)
    app.register(mongo_db_events_db_publisher)
    app.register(queue_subscriber)
    return app
