from datetime import datetime, timezone
from uuid import UUID

import pytest

from src.seedwork.infrastructure.events import Event
from src.seedwork.infrastructure.events.mongo_db import EventModel


@pytest.mark.unit
def test_to_document(faker):
    event_model = EventModel(
        id=str(faker.uuid4()),
        type="event_type",
        created_at=datetime.now(timezone.utc).isoformat(),
        payload=faker.pydict(),
        version="v1.0",
    )

    document = event_model.to_document()

    assert document == {
        "_id": event_model.id,
        "created_at": event_model.created_at,
        "payload": event_model.payload,
        "type": event_model.type,
        "version": event_model.version,
    }


@pytest.mark.unit
def test_from_document(faker):
    document = {
        "_id": str(faker.uuid4()),
        "type": "event_type",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "payload": faker.pydict(),
        "version": "1.0",
    }

    event_model = EventModel.from_document(data=document)

    assert event_model.id == document["_id"]
    assert event_model.type == document["type"]
    assert event_model.created_at == document["created_at"]
    assert event_model.payload == document["payload"]
    assert event_model.version == document["version"]


@pytest.mark.unit
def test_from_event(faker):
    event = Event(
        type="event_type",
        created_at=datetime.now(timezone.utc),
        id=faker.uuid4(),
        payload=faker.pydict(),
        version="1.0",
    )

    event_model = EventModel.from_event(event=event)

    assert event_model.id == str(event.id)
    assert event_model.type == event.type
    assert event_model.created_at == event.created_at.isoformat()
    assert event_model.payload == event.payload
    assert event_model.version == event.version


@pytest.mark.unit
def test_to_event(faker):
    event_model = EventModel(
        id=str(faker.uuid4()),
        type="event_type",
        created_at=datetime.now(timezone.utc).isoformat(),
        payload=faker.pydict(),
        version="1.0",
    )

    event = event_model.to_event()

    assert event.type == event_model.type
    assert event.created_at == datetime.fromisoformat(event_model.created_at)
    assert event.id == UUID(event_model.id)
    assert event.payload == event_model.payload
    assert event.version == event_model.version
