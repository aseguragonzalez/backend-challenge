import os

from pymongo import MongoClient
from pymongo.client_session import ClientSession

from src.seedwork.infrastructure.events import EventsDb, EventsPublisher
from src.seedwork.infrastructure.events.mongo_db import MongoDbEventsDb, MongoDbEventsDbSettings, MongoDbPublisher
from src.seedwork.infrastructure.ports.dependency_injection import ServiceProvider


def events_db_settings(sp: ServiceProvider) -> None:
    settings = MongoDbEventsDbSettings(
        database_url=os.getenv("EVENTS_DATABASE_URL"),
        database_name=os.getenv("EVENTS_DATABASE_NAME"),
        collection_name=os.getenv("EVENTS_COLLECTION_NAME"),
    )
    sp.register_singleton(MongoDbEventsDbSettings, lambda _: settings)


def mongo_db_events_db(sp: ServiceProvider) -> None:
    def _configure(sp: ServiceProvider):
        try:
            client_session: ClientSession = sp.get(ClientSession)
        except ValueError:
            client_session = None

        settings = sp.get(MongoDbEventsDbSettings)
        mongo_client = sp.get(MongoClient)
        db_collection = mongo_client[settings.database_name][settings.processed_collection_name]
        return MongoDbEventsDb(db_collection=db_collection, client_session=client_session)

    sp.register_singleton(EventsDb, _configure)


def mongo_db_events_db_publisher(sp: ServiceProvider) -> None:
    def _configure(sp: ServiceProvider):
        try:
            client_session: ClientSession = sp.get(ClientSession)
        except ValueError:
            client_session = None

        settings = sp.get(MongoDbEventsDbSettings)
        mongo_client = sp.get(MongoClient)
        db_collection = mongo_client[settings.database_name][settings.collection_name]
        return MongoDbPublisher(db_collection=db_collection, client_session=client_session)

    sp.register_singleton(EventsPublisher, _configure)
