from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from mongomock import MongoClient

from src.application.services import CreateAssistanceService, GetAssistanceService
from src.domain.repositories import AssistancesRepository
from src.domain.services import ChannelsService
from src.infrastructure.ports.api.dependencies import assistance_repository, settings
from src.infrastructure.ports.api.main import app
from src.infrastructure.ports.api.settings import Settings


@pytest.fixture
def headers():
    return {"X-API-Key": "fake-api-key"}


@pytest.fixture
def test_settings():
    return Settings(api_keys="fake-api-key")


@pytest.fixture
def assistances_repository() -> AssistancesRepository:
    return Mock(AssistancesRepository)


@pytest.fixture
def channels_service() -> ChannelsService:
    return Mock(ChannelsService)


@pytest.fixture
def create_assistance_service() -> CreateAssistanceService:
    return Mock(CreateAssistanceService)


@pytest.fixture
def get_assistance_service() -> GetAssistanceService:
    return Mock(GetAssistanceService)


@pytest.fixture
def mongo_db_client():
    return MongoClient()


@pytest.fixture
def db_collection(mongo_db_client):
    return mongo_db_client["test"]["assistances"]


@pytest.fixture
def client(assistances_repository, test_settings):
    app.dependency_overrides[assistance_repository] = lambda: assistances_repository
    app.dependency_overrides[settings] = lambda: test_settings
    return TestClient(app)
