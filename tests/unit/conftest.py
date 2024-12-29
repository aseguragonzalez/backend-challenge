from collections.abc import Generator
from typing import Any
from unittest.mock import Mock
from uuid import uuid4

import pytest
from pymongo import MongoClient
from pymongo.collection import Collection

from src.application.services import CreateAssistanceService, GetAssistanceService
from src.domain.repositories import AssistancesRepository
from src.domain.services import ChannelsService
from src.infrastructure.adapters.repositories import MongoDbSettings
from src.seedwork.infrastructure.events import EventsDb, EventsDispatcher
from src.seedwork.infrastructure.events.mongo_db import MongoDbEventsDbSettings


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
def events_db_mock() -> EventsDb:
    events_db = Mock(EventsDb)
    events_db.exist.return_value = False
    events_db.create.return_value = None
    return events_db


@pytest.fixture
def events_dispatcher_mock() -> EventsDispatcher:
    events_dispatcher = Mock(EventsDispatcher)
    events_dispatcher.dispatch.return_value = None
    return events_dispatcher


@pytest.fixture(scope="session")
def mongo_db_settings(mongodb_container) -> MongoDbSettings:
    mongo_db_url = mongodb_container.get_connection_url()
    database_name = f"assistance_db_{str(uuid4())}"
    return MongoDbSettings(
        collection_name="assistances",
        database_name=database_name,
        database_url=mongo_db_url,
    )


@pytest.fixture
def db_collection(mongo_db_settings: MongoDbSettings, mongo_client: MongoClient) -> Collection:
    return mongo_client[mongo_db_settings.database_name][mongo_db_settings.collection_name]


@pytest.fixture(scope="session")
def events_db_settings(mongodb_container) -> MongoDbEventsDbSettings:
    mongo_db_url = mongodb_container.get_connection_url()
    database_name = f"events_db_{str(uuid4())}"
    return MongoDbEventsDbSettings(
        collection_name="events",
        database_name=database_name,
        database_url=mongo_db_url,
    )


@pytest.fixture
def db_events_collection(events_db_settings: MongoDbEventsDbSettings, mongo_client: MongoClient) -> Collection:
    return mongo_client[events_db_settings.database_name][events_db_settings.collection_name]


@pytest.fixture
def clean_db(
    mongo_db_settings: MongoDbSettings, events_db_settings: MongoDbEventsDbSettings, mongo_client: MongoClient
) -> Generator[Any, Any, Any]:
    mongo_client.drop_database(mongo_db_settings.database_name)
    mongo_client.drop_database(events_db_settings.database_name)
    yield
    mongo_client.drop_database(mongo_db_settings.database_name)
    mongo_client.drop_database(events_db_settings.database_name)
