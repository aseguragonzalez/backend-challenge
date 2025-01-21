from pymongo import MongoClient
from pymongo.client_session import ClientSession

from src.infrastructure.adapters import MongoDbUnitOfWork
from src.infrastructure.adapters.repositories import MongoDbSettings
from src.seedwork.domain import UnitOfWork
from src.seedwork.infrastructure.ports.dependency_injection import ServiceProvider


def client_session(sp: ServiceProvider) -> None:
    def _configure(sp: ServiceProvider):
        mongo_client = sp.get(MongoClient)
        client_session = mongo_client.start_session()
        return client_session

    # TODO: ensure closing the session before delete
    sp.register_singleton(ClientSession, _configure)


def mongo_client(sp: ServiceProvider) -> None:
    def _configure(sp: ServiceProvider):
        settings = sp.get(MongoDbSettings)
        client = MongoClient(settings.database_url)
        return client

    sp.register_singleton(MongoClient, _configure)


def unit_of_work(sp: ServiceProvider) -> None:
    sp.register_singleton(UnitOfWork, MongoDbUnitOfWork)
