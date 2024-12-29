from collections.abc import Generator
from typing import Any
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from pymongo.collection import Collection

from src.infrastructure.ports.api.dependencies import client_session, settings
from src.infrastructure.ports.api.main import app
from src.infrastructure.ports.api.settings import Settings


@pytest.fixture(scope="session")
def api_settings(mongodb_container) -> Settings:
    mongo_db_url = mongodb_container.get_connection_url()
    instance = str(uuid4())
    return Settings(
        assistance_api_keys=instance,
        assistance_collection_name="assistances",
        assistance_database_name=f"assistance_db_{instance}",
        assistance_database_url=mongo_db_url,
        events_database_name=f"events_db_{instance}",
        events_collection_name="events",
        events_database_url=mongo_db_url,
    )


@pytest.fixture
def db_collection(api_settings: Settings, mongo_client: MongoClient) -> Collection:
    return mongo_client[api_settings.assistance_database_name][api_settings.assistance_collection_name]


@pytest.fixture
def db_events_collection(api_settings: Settings, mongo_client: MongoClient) -> Collection:
    return mongo_client[api_settings.events_database_name][api_settings.events_collection_name]


@pytest.fixture(autouse=True)
def clean_db(api_settings: Settings, mongo_client: MongoClient) -> Generator[Any, Any, Any]:
    mongo_client.drop_database(api_settings.assistance_database_name)
    mongo_client.drop_database(api_settings.events_database_name)
    yield
    mongo_client.drop_database(api_settings.assistance_database_name)
    mongo_client.drop_database(api_settings.events_database_name)


@pytest.fixture
def client(api_settings: Settings) -> TestClient:
    app.dependency_overrides[settings] = lambda: api_settings
    # HACK: We disable client_session and MongoDb transactions because it requires a replica set
    app.dependency_overrides[client_session] = lambda: None
    return TestClient(app, headers={"X-API-Key": api_settings.assistance_api_keys})
