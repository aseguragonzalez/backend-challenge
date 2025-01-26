import os
from logging import Logger

from pymongo import MongoClient

from src.infrastructure.ports.subscriber.app import App
from src.seedwork.infrastructure.events.mongo_db import MongoDbEventsDbSettings, MongoDbEventsWatcher
from src.seedwork.infrastructure.events.mongo_db.dependencies import mongo_db_events_db
from src.seedwork.infrastructure.ports.dependency_injection import ServiceProvider
from src.seedwork.infrastructure.queues.rabbit_mq import ProducerSettings, RabbitMqSettings
from src.seedwork.infrastructure.queues.rabbit_mq.dependencies import rabbit_mq_connection, rabbit_mq_producer


def _mongo_db_events_db_settings(sp: ServiceProvider) -> None:
    settings = MongoDbEventsDbSettings(
        database_url=os.getenv("EVENTS_DATABASE_URL"),
        database_name=os.getenv("EVENTS_DATABASE_NAME"),
        collection_name=os.getenv("EVENTS_COLLECTION_NAME"),
    )
    sp.register_singleton(MongoDbEventsDbSettings, lambda _: settings)


def _mongo_client(sp: ServiceProvider) -> None:
    def _configure(sp: ServiceProvider):
        settings = sp.get(MongoDbEventsDbSettings)
        client = MongoClient(settings.database_url)
        return client

    sp.register_singleton(MongoClient, _configure)


def _rabbit_mq_settings(sp: ServiceProvider) -> None:
    settings = RabbitMqSettings(
        host=os.getenv("RABBITMQ_HOST"),
        port=os.getenv("RABBITMQ_PORT"),
        username=os.getenv("RABBITMQ_USERNAME"),
        password=os.getenv("RABBITMQ_PASSWORD"),
    )
    sp.register_singleton(RabbitMqSettings, lambda _: settings)


def _producer_settings(sp: ServiceProvider) -> None:
    settings = ProducerSettings(
        exchange=os.getenv("RABBITMQ_PRODUCER_EXCHANGE_NAME"),
        routing_key=os.getenv("RABBITMQ_PRODUCER_ROUTING_KEY"),
    )
    sp.register_singleton(ProducerSettings, lambda _: settings)


def _events_watcher(sp: ServiceProvider) -> None:
    def _configure(sp: ServiceProvider):
        settings = sp.get(MongoDbEventsDbSettings)
        client = sp.get(MongoClient)
        db_collection = client[settings.database_name][settings.collection_name]
        return MongoDbEventsWatcher(db_collection=db_collection)

    sp.register_singleton(MongoDbEventsWatcher, _configure)


def configure(app: App, logger: Logger) -> App:
    app.register(_rabbit_mq_settings)
    app.register(_producer_settings)
    app.register(_mongo_db_events_db_settings)
    app.register(rabbit_mq_connection)
    app.register(rabbit_mq_producer)
    app.register(_mongo_client)
    app.register(mongo_db_events_db)
    app.register(_events_watcher)
    app.register(lambda sp: sp.register_singleton(Logger, lambda _: logger))
    return app
