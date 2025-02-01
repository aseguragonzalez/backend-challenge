from datetime import datetime, timezone
from uuid import UUID

import pytest

from src.seedwork.infrastructure.events import Event
from src.seedwork.infrastructure.events.mongo_db import Event as EventDto


@pytest.mark.unit
def test_to_dict(faker):
    event = EventDto(
        _id=str(faker.uuid4()),
        type="event_type",
        created_at=datetime.now(timezone.utc).isoformat(),
        id=str(faker.uuid4()),
        payload=faker.pydict(),
        version="1.0",
    )

    event_dto = event.to_dict()

    assert event_dto == {
        "_id": event._id,
        "type": event.type,
        "created_at": event.created_at,
        "id": event.id,
        "payload": event.payload,
        "version": event.version,
    }


@pytest.mark.unit
def test_from_dict(faker):
    event_dict = {
        "_id": str(faker.uuid4()),
        "type": "event_type",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "id": str(faker.uuid4()),
        "payload": faker.pydict(),
        "version": "1.0",
    }

    event = EventDto.from_dict(data=event_dict)

    assert event._id == event_dict["_id"]
    assert event.type == event_dict["type"]
    assert event.created_at == event_dict["created_at"]
    assert event.id == event_dict["id"]
    assert event.payload == event_dict["payload"]
    assert event.version == event_dict["version"]


@pytest.mark.unit
def test_from_integration_event(faker):
    event = Event(
        type="event_type",
        created_at=datetime.now(timezone.utc),
        id=faker.uuid4(),
        payload=faker.pydict(),
        version="1.0",
    )

    event_dto = EventDto.from_integration_event(event=event)

    assert event_dto._id == str(event.id)
    assert event_dto.type == event.type
    assert event_dto.created_at == event.created_at.isoformat()
    assert event_dto.id == str(event.id)
    assert event_dto.payload == event.payload
    assert event_dto.version == event.version


@pytest.mark.unit
def test_to_integration_event(faker):
    event_dto = EventDto(
        _id=str(faker.uuid4()),
        type="event_type",
        created_at=datetime.now(timezone.utc).isoformat(),
        id=str(faker.uuid4()),
        payload=faker.pydict(),
        version="1.0",
    )

    event = event_dto.to_integration_event()

    assert event.type == event_dto.type
    assert event.created_at == datetime.fromisoformat(event_dto.created_at)
    assert event.id == UUID(event_dto.id)
    assert event.payload == event_dto.payload
    assert event.version == event_dto.version
