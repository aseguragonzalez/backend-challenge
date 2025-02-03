from datetime import datetime, timezone

import pytest
from freezegun import freeze_time

from src.seedwork.infrastructure.events import Event
from src.seedwork.infrastructure.events.mongo_db import EventModel, MongoDbPublisher


@freeze_time(datetime.now(timezone.utc))
@pytest.mark.unit
def test_publish_should_save_events_in_mongo_db(faker, db_collection):
    event = Event.new(type=faker.word(), payload=faker.pydict())
    events_publisher = MongoDbPublisher(db_collection=db_collection)
    event_model = EventModel.from_event(event).to_document()

    events_publisher.publish(events=[event])

    documents = list(db_collection.find())
    assert len(documents) == 1
    assert event_model == documents[0]
