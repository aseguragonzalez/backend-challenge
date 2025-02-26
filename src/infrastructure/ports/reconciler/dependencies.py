import os
from logging import Logger
from typing import Any

from pymongo import MongoClient

from src.infrastructure.ports.reconciler.app import App
from src.infrastructure.ports.reconciler.services import ReconciliationService
from src.seedwork.infrastructure.ports.dependency_injection import ServiceProvider
from src.seedwork.infrastructure.queues import Producer
from src.seedwork.infrastructure.queues.rabbit_mq import ProducerSettings, RabbitMqSettings
from src.seedwork.infrastructure.queues.rabbit_mq.dependencies import rabbit_mq_connection, rabbit_mq_producer


def _mongo_client(sp: ServiceProvider) -> None:
    def configure(sp: ServiceProvider) -> MongoClient[Any]:
        database_url = os.environ["EVENTS_DATABASE_URL"]
        return MongoClient(database_url)

    sp.register_singleton(MongoClient, configure)


def _reconciliation_service(sp: ServiceProvider) -> None:
    def configure(sp: ServiceProvider) -> ReconciliationService:
        mongo_client = sp.get(MongoClient)
        producer = sp.get(Producer)  # type: ignore
        database_name = os.environ["EVENTS_DATABASE_NAME"]
        db_events_collection = mongo_client[database_name][os.environ["EVENTS_COLLECTION_NAME"]]
        db_processed_collection = mongo_client[database_name][os.environ["EVENTS_PROCESSED_COLLECTION_NAME"]]
        db_dlq_events_collection = mongo_client[database_name][os.environ["EVENTS_DLQ_PROCESSED_COLLECTION_NAME"]]
        return ReconciliationService(
            db_events_collection=db_events_collection,
            db_processed_collection=db_processed_collection,
            db_dlq_events_collection=db_dlq_events_collection,
            producer=producer,
        )

    sp.register_singleton(ReconciliationService, configure)


def _rabbit_mq_settings(sp: ServiceProvider) -> None:
    settings = RabbitMqSettings(
        host=os.environ["RABBITMQ_HOST"],
        port=os.environ["RABBITMQ_PORT"],
        username=os.environ["RABBITMQ_USERNAME"],
        password=os.environ["RABBITMQ_PASSWORD"],
    )
    sp.register_singleton(RabbitMqSettings, lambda _: settings)


def _producer_settings(sp: ServiceProvider) -> None:
    settings = ProducerSettings(
        exchange=os.environ["RABBITMQ_PRODUCER_EXCHANGE_NAME"],
        routing_key=os.environ["RABBITMQ_PRODUCER_ROUTING_KEY"],
    )
    sp.register_singleton(ProducerSettings, lambda _: settings)


def configure(app: App, logger: Logger) -> App:
    app.register(_mongo_client)
    app.register(_rabbit_mq_settings)
    app.register(_producer_settings)
    app.register(rabbit_mq_connection)
    app.register(rabbit_mq_producer)
    app.register(_reconciliation_service)
    app.register(lambda sp: sp.register_singleton(Logger, lambda _: logger))
    return app
