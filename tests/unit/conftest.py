from typing import Any
from unittest.mock import Mock

import pytest
from faker import Faker
from mongomock import MongoClient
from pymongo.synchronous.collection import Collection

from src.application.services import CreateAssistanceService, GetAssistanceService
from src.domain.repositories import AssistancesRepository
from src.domain.services import ChannelsService
from src.infrastructure.adapters.repositories import MongoDbSettings
from src.infrastructure.adapters.services import EmailSettings
from src.seedwork.domain import UnitOfWork
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
def events_db_mock() -> EventsDb[Any]:
    events_db = Mock(EventsDb)
    events_db.exist.return_value = False
    events_db.create.return_value = None
    return events_db


@pytest.fixture
def events_dispatcher_mock() -> EventsDispatcher:
    events_dispatcher = Mock(EventsDispatcher)
    events_dispatcher.dispatch.return_value = None
    return events_dispatcher


@pytest.fixture
def mongo_client() -> MongoClient:  # type: ignore
    return MongoClient()


@pytest.fixture
def mongo_db_settings(faker: Faker) -> MongoDbSettings:
    return MongoDbSettings(
        collection_name=faker.word(),
        database_name=faker.word(),
        database_url=faker.word(),
    )


@pytest.fixture
def db_collection(mongo_db_settings: MongoDbSettings, mongo_client: MongoClient) -> Collection[Any]:  # type: ignore
    return mongo_client[mongo_db_settings.database_name][mongo_db_settings.collection_name]


@pytest.fixture
def events_db_settings(faker: Faker) -> MongoDbEventsDbSettings:
    return MongoDbEventsDbSettings(
        collection_name=faker.word(),
        database_name=faker.word(),
        database_url=faker.word(),
        processed_collection_name=faker.word(),
        dlq_processed_collection_name=faker.word(),
    )


@pytest.fixture
def db_events_collection(
    events_db_settings: MongoDbEventsDbSettings, mongo_client: MongoClient  # type: ignore
) -> Collection[Any]:
    return mongo_client[events_db_settings.database_name][events_db_settings.collection_name]


@pytest.fixture
def db_processed_events_collection(
    events_db_settings: MongoDbEventsDbSettings, mongo_client: MongoClient  # type: ignore
) -> Collection[Any]:
    return mongo_client[events_db_settings.database_name][events_db_settings.processed_collection_name]


@pytest.fixture
def db_dlq_events_collection(
    faker: Faker, events_db_settings: MongoDbEventsDbSettings, mongo_client: MongoClient  # type: ignore
) -> Collection[Any]:
    db_dlq_colletion_name = faker.word()
    return mongo_client[events_db_settings.database_name][db_dlq_colletion_name]


@pytest.fixture
def email_settings(faker: Faker) -> EmailSettings:
    return EmailSettings(
        from_email=faker.email(),
        to_email=faker.email(),
        server="smtp",
        port=25,
        username=faker.user_name(),
        password=faker.password(),
    )


@pytest.fixture
def unit_of_work_mock() -> UnitOfWork:
    # HACK: We have to mock uow beacuse MongoDb transactions are not available without a replica set
    unit_of_work = Mock(UnitOfWork)
    unit_of_work.__enter__ = Mock(return_value=unit_of_work)
    unit_of_work.__exit__ = Mock(return_value=None)
    unit_of_work.commit = Mock()
    unit_of_work.rollback = Mock()
    return unit_of_work
