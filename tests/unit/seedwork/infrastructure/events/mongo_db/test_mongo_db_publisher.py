import pytest

from src.seedwork.infrastructure.events import Event
from src.seedwork.infrastructure.events.mongo_db import Event as EventDto, MongoDbPublisher


@pytest.mark.unit
def test_publish_should_save_events_in_mongo_db(faker, db_collection):
    event = Event.new(type=faker.word(), payload=faker.pydict())
    events_publisher = MongoDbPublisher(db_collection=db_collection)
    expected_document = EventDto.from_integration_event(event).to_dict()

    events_publisher.publish(events=[event])

    documents = list(db_collection.find())
    assert len(documents) == 1
    assert expected_document == documents[0]
