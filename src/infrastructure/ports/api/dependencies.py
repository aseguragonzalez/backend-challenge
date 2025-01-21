from functools import lru_cache

from fastapi import Depends
from pymongo import MongoClient

from src.application.services import CreateAssistanceService, GetAssistanceService
from src.domain.repositories import AssistancesRepository
from src.infrastructure.adapters.repositories import MongoDbAssistancesRepository
from src.infrastructure.ports.api.settings import Settings


@lru_cache
def settings() -> Settings:
    return Settings()


def mongo_client(settings: Settings = Depends(settings)) -> MongoClient:
    return MongoClient(settings.database_url)


def assistance_repository(
    settings: Settings = Depends(settings), mongo_client: MongoClient = Depends(mongo_client)
) -> AssistancesRepository:
    db_collection = mongo_client[settings.database_name]["assistances"]
    return MongoDbAssistancesRepository(db_collection=db_collection)


def create_assistance_service(
    assistance_repository: AssistancesRepository = Depends(assistance_repository),
) -> CreateAssistanceService:
    return CreateAssistanceService(repository=assistance_repository)


def get_assistance_service(
    assistance_repository: AssistancesRepository = Depends(assistance_repository),
) -> GetAssistanceService:
    return GetAssistanceService(repository=assistance_repository)
