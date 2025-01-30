import pytest

from src.seedwork.infrastructure.events import Event
from src.seedwork.infrastructure.events.mongo_db import MongoDbEventsDb


@pytest.mark.unit
def test_exist_should_be_false_when_the_event_has_not_been_processed(faker, db_events_collection):
    event = Event.new(type=faker.word(), payload={})
    events_db = MongoDbEventsDb(db_collection=db_events_collection)

    exist = events_db.exist(event=event)

    assert exist is False


@pytest.mark.unit
def test_exist_should_be_true_when_the_event_has_been_processed(faker, db_events_collection):
    event = Event.new(type=faker.word(), payload={})
    db_events_collection.insert_one({"_id": str(event.id)})
    events_db = MongoDbEventsDb(db_collection=db_events_collection)

    exist = events_db.exist(event=event)

    assert exist is True


@pytest.mark.unit
def test_create_should_insert_a_document(faker, db_events_collection):
    event = Event.new(type=faker.word(), payload={})
    events_db = MongoDbEventsDb(db_collection=db_events_collection)

    events_db.create(event=event)

    document = db_events_collection.find_one({"_id": str(event.id)})

    assert document is not None
    assert document["_id"] == str(event.id)
    assert document["type"] == event.type
    assert document["created_at"] == event.created_at.isoformat()
    assert document["id"] == str(event.id)
