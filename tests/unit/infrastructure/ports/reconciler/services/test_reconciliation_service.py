from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

import pytest

from src.infrastructure.ports.reconciler.services import ReconciliationService
from src.seedwork.infrastructure.events import Event as Event
from src.seedwork.infrastructure.events.mongo_db.event_model import EventModel
from src.seedwork.infrastructure.queues.producer import Producer


@pytest.mark.unit
def test_reconciliation_service_should_publish_events_not_processed(
    faker, db_events_collection, db_processed_events_collection, db_dlq_events_collection
):
    seconds_delayed = faker.random_int(min=30, max=60)
    producer = Mock(Producer)
    created_at = datetime.now(timezone.utc) - timedelta(seconds=seconds_delayed)
    event_1 = Event.new(id=faker.uuid4(), type=faker.word(), payload=faker.pydict())
    event_2 = Event.new(id=faker.uuid4(), type=faker.word(), payload=faker.pydict(), created_at=created_at)
    event_3 = Event.new(id=faker.uuid4(), type=faker.word(), payload=faker.pydict())
    event_4 = Event.new(id=faker.uuid4(), type=faker.word(), payload=faker.pydict(), created_at=created_at)
    db_events_collection.insert_many(
        [
            EventModel.from_event(event_1).to_document(),
            EventModel.from_event(event_2).to_document(),
            EventModel.from_event(event_3).to_document(),
            EventModel.from_event(event_4).to_document(),
        ]
    )
    db_processed_events_collection.insert_one(EventModel.from_event(event_3).to_document())
    db_dlq_events_collection.insert_one(EventModel.from_event(event_4).to_document())
    service = ReconciliationService(
        db_events_collection=db_events_collection,
        db_processed_collection=db_processed_events_collection,
        db_dlq_events_collection=db_dlq_events_collection,
        producer=producer,
    )

    service.execute(seconds_delayed=seconds_delayed)

    producer.send_message.assert_called_once_with(event_2.to_bytes())


@pytest.mark.unit
def test_reconciliation_service_should_do_nothing_when_no_events_to_be_processed(
    faker, db_events_collection, db_processed_events_collection, db_dlq_events_collection
):
    seconds_delayed = faker.random_int(min=30, max=60)
    producer = Mock(Producer)
    event_1 = Event.new(id=faker.uuid4(), type=faker.word(), payload=faker.pydict())
    event_2 = Event.new(id=faker.uuid4(), type=faker.word(), payload=faker.pydict())
    event_3 = Event.new(id=faker.uuid4(), type=faker.word(), payload=faker.pydict())
    db_events_collection.insert_one(EventModel.from_event(event_1).to_document())
    db_events_collection.insert_one(EventModel.from_event(event_2).to_document())
    db_events_collection.insert_one(EventModel.from_event(event_3).to_document())
    db_processed_events_collection.insert_one(EventModel.from_event(event_3).to_document())
    service = ReconciliationService(
        db_events_collection=db_events_collection,
        db_processed_collection=db_processed_events_collection,
        db_dlq_events_collection=db_dlq_events_collection,
        producer=producer,
    )

    service.execute(seconds_delayed=seconds_delayed)

    producer.send_message.assert_not_called()
