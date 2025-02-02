from pymongo import MongoClient
from pymongo.client_session import ClientSession

from src.domain.repositories import AssistancesRepository
from src.infrastructure.adapters.repositories import MongoDbAssistancesRepository, MongoDbSettings
from src.seedwork.infrastructure.events import EventsInterceptor, EventsPublisher
from src.seedwork.infrastructure.ports.dependency_injection import ServiceProvider


def assistances_repository(sp: ServiceProvider) -> None:
    def configure(sp: ServiceProvider):
        repository = sp.get(MongoDbAssistancesRepository)
        events_publisher = sp.get(EventsPublisher)
        return EventsInterceptor(repository=repository, events_publisher=events_publisher)

    sp.register_singleton(AssistancesRepository, configure)


def mongo_db_assistances_repositories(sp: ServiceProvider) -> None:
    def configure(sp: ServiceProvider):
        try:
            client_session: ClientSession = sp.get(ClientSession)
        except ValueError:
            client_session = None

        client = sp.get(MongoClient)
        mongo_db_settings = sp.get(MongoDbSettings)
        db_collection = client[mongo_db_settings.database_name][mongo_db_settings.collection_name]
        return MongoDbAssistancesRepository(db_collection=db_collection, client_session=client_session)

    sp.register_singleton(MongoDbAssistancesRepository, configure)
