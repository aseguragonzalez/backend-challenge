from unittest.mock import Mock

import pytest
from mongomock import MongoClient
from mongomock.collection import Collection

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


@pytest.fixture
def mongo_client() -> MongoClient:
    return MongoClient()


@pytest.fixture
def mongo_db_settings(faker) -> MongoDbSettings:
    return MongoDbSettings(
        collection_name=faker.uuid4(),
        database_name=faker.uuid4(),
        database_url=faker.uuid4(),
    )


@pytest.fixture
def db_collection(mongo_db_settings: MongoDbSettings, mongo_client: MongoClient) -> Collection:
    return mongo_client[mongo_db_settings.database_name][mongo_db_settings.collection_name]


@pytest.fixture
def events_db_settings(faker) -> MongoDbEventsDbSettings:
    return MongoDbEventsDbSettings(
        collection_name=faker.uuid4(),
        database_name=faker.uuid4(),
        database_url=faker.uuid4(),
        processed_collection_name=faker.uuid4(),
    )


@pytest.fixture
def db_events_collection(events_db_settings: MongoDbEventsDbSettings, mongo_client: MongoClient) -> Collection:
    return mongo_client[events_db_settings.database_name][events_db_settings.collection_name]


@pytest.fixture
def db_processed_events_collection(
    events_db_settings: MongoDbEventsDbSettings, mongo_client: MongoClient
) -> Collection:
    return mongo_client[events_db_settings.database_name][events_db_settings.processed_collection_name]


@pytest.fixture
def db_dlq_events_collection(
    faker, events_db_settings: MongoDbEventsDbSettings, mongo_client: MongoClient
) -> Collection:
    db_dlq_colletion_name = faker.uuid4()
    return mongo_client[events_db_settings.database_name][db_dlq_colletion_name]


@pytest.fixture
def email_settings(faker):
    return EmailSettings(
        from_email=faker.email(),
        to_email=faker.email(),
        server="smtp",
        port=25,
        username=faker.user_name(),
        password=faker.password(),
    )


@pytest.fixture
def unit_of_work_mock():
    # HACK: We have to mock uow beacuse MongoDb transactions are not available without a replica set
    unit_of_work = Mock(UnitOfWork)
    unit_of_work.__enter__ = Mock(return_value=unit_of_work)
    unit_of_work.__exit__ = Mock(return_value=None)
    unit_of_work.commit = Mock()
    unit_of_work.rollback = Mock()
    return unit_of_work
