from functools import lru_cache

from fastapi import Depends
from src.application.services import CreateAssistanceService, GetAssistanceService
from src.domain.repositories import AssistancesRepository
from src.infrastructure.ports.api.settings import Settings


@lru_cache
def settings() -> Settings:
    return Settings()


def assistance_repository():
    pass


def create_assistance_service(
        assistance_repository: AssistancesRepository = Depends(assistance_repository)
        ) -> CreateAssistanceService:
    return CreateAssistanceService(repository=assistance_repository)


def get_assistance_service(
        assistance_repository: AssistancesRepository = Depends(assistance_repository)
        ) -> GetAssistanceService:
    return GetAssistanceService(repository=assistance_repository)
