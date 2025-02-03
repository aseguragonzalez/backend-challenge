from typing import Any

from pymongo import MongoClient
from pymongo.client_session import ClientSession

from src.infrastructure.adapters import MongoDbUnitOfWork
from src.infrastructure.adapters.repositories import MongoDbSettings
from src.seedwork.domain import UnitOfWork
from src.seedwork.infrastructure.ports.dependency_injection import ServiceProvider


def client_session(sp: ServiceProvider) -> None:
    def configure(sp: ServiceProvider) -> ClientSession:
        mongo_client = sp.get(MongoClient)
        return mongo_client.start_session()

    # TODO: ensure closing the session before delete
    sp.register_singleton(ClientSession, configure)


def mongo_client(sp: ServiceProvider) -> None:
    def configure(sp: ServiceProvider) -> MongoClient[Any]:
        settings = sp.get(MongoDbSettings)
        return MongoClient(settings.database_url)

    sp.register_singleton(MongoClient, configure)


def unit_of_work(sp: ServiceProvider) -> None:
    sp.register_singleton(UnitOfWork, MongoDbUnitOfWork)  # type: ignore
