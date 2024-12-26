from unittest.mock import Mock

import pytest
from fastapi import testclient

from src.domain.repositories import AssistancesRepository
from src.infrastructure.ports.api.dependencies import assistance_repository, settings
from src.infrastructure.ports.api.main import app
from src.infrastructure.ports.api.security import api_key
from src.infrastructure.ports.api.settings import Settings


@pytest.fixture
def headers():
    return {"X-API-Key": "fake-api-key"}


@pytest.fixture
def fake_settings():
    return Settings(api_keys="fake-api-key")


@pytest.fixture
def assistances_repository() -> AssistancesRepository:
    return Mock(AssistancesRepository)


@pytest.fixture
def client(assistances_repository, fake_settings):
    app.dependency_overrides[assistance_repository] = lambda: assistances_repository
    app.dependency_overrides[api_key] = lambda: None
    app.dependency_overrides[settings] = lambda: fake_settings
    return testclient.TestClient(app)
