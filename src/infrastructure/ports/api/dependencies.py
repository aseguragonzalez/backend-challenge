import logging
from collections.abc import Generator
from functools import lru_cache
from typing import Any

from fastapi import Depends
from pymongo import MongoClient
from pymongo.client_session import ClientSession

from src.application.services import CreateAssistanceService, GetAssistanceService
from src.domain.repositories import AssistancesRepository
from src.infrastructure.adapters import MongoDbUnitOfWork
from src.infrastructure.adapters.repositories import MongoDbAssistancesRepository
from src.infrastructure.ports.api.settings import Settings
from src.seedwork.domain import UnitOfWork
from src.seedwork.infrastructure.events import EventsInterceptor
from src.seedwork.infrastructure.events.mongo_db import MongoDbPublisher


logger = logging.getLogger(__name__)


@lru_cache
def settings() -> Settings:
    return Settings()  # type: ignore


def mongo_client(settings: Settings = Depends(settings)) -> MongoClient[Any]:
    return MongoClient(settings.assistance_database_url)


def client_session(mongo_client: MongoClient[Any] = Depends(mongo_client)) -> Generator[ClientSession, None, None]:
    with mongo_client.start_session() as session:
        yield session


def unit_of_work(client_session: ClientSession | None = Depends(client_session)) -> Generator[UnitOfWork, None, None]:
    unit_of_work: UnitOfWork = MongoDbUnitOfWork(session=client_session)
    with unit_of_work as uow:
        yield uow


def assistance_repository(
    settings: Settings = Depends(settings),
    mongo_client: MongoClient[Any] = Depends(mongo_client),
    client_session: ClientSession | None = Depends(client_session),
) -> EventsInterceptor:
    db_assistances_collection = mongo_client[settings.assistance_database_name][settings.assistance_collection_name]
    repository = MongoDbAssistancesRepository(db_collection=db_assistances_collection, client_session=client_session)
    db_events_collection = mongo_client[settings.events_database_name][settings.events_collection_name]
    events_publisher = MongoDbPublisher(db_collection=db_events_collection, client_session=client_session)
    return EventsInterceptor(events_publisher=events_publisher, repository=repository)  # type: ignore


def create_assistance_service(
    assistance_repository: AssistancesRepository = Depends(assistance_repository),
) -> CreateAssistanceService:
    return CreateAssistanceService(repository=assistance_repository)


def get_assistance_service(
    assistance_repository: AssistancesRepository = Depends(assistance_repository),
) -> GetAssistanceService:
    return GetAssistanceService(repository=assistance_repository)
