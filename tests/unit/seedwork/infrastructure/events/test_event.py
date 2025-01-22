from datetime import datetime, timezone
from uuid import UUID

from freezegun import freeze_time
from tests.unit.seedwork.infrastructure.events.fakes import CustomEvent

from src.seedwork.infrastructure.events import Event


def test_new_should_create_a_new_instance(faker):
    with freeze_time(datetime.now(timezone.utc)):
        event_type = faker.word()
        event_payload = faker.pydict()
        version = faker.word()
        created_at = datetime.now(timezone.utc)
        event = Event.new(type=event_type, payload=event_payload, version=version, created_at=created_at)

    assert event.type == event_type
    assert event.payload == event_payload
    assert event.id is not None
    assert event.created_at == created_at
    assert event.version == version


def test_from_domain_event_should_create_event_from_domain_event(faker):
    with freeze_time(datetime.now(timezone.utc)):
        domain_event = CustomEvent.new(id=UUID(faker.uuid4()))
        now = datetime.now(timezone.utc)
        event = Event.from_domain_event(domain_event)

    assert event.type == domain_event.type
    assert event.payload["id"] == domain_event.payload["id"]
    assert event.id is not None
    assert event.created_at == now
    assert event.version == domain_event.version


def test_from_json_should_create_event_from_string_json(faker):
    expected_event = Event.new(type=faker.word(), payload=faker.pydict(), version=faker.word())
    json = expected_event.to_json()

    actual_event = Event.from_json(json)

    assert expected_event.type == actual_event.type
    assert expected_event.payload == actual_event.payload
    assert expected_event.id == actual_event.id
    assert expected_event.created_at == actual_event.created_at
    assert expected_event.version == actual_event.version


def test_from_bytes_should_create_the_event_from_bytes(faker):
    expected_event = Event.new(type=faker.word(), payload=faker.pydict(), version=faker.word())

    actual_event = Event.from_bytes(expected_event.to_bytes())

    assert expected_event.type == actual_event.type
    assert expected_event.payload == actual_event.payload
    assert expected_event.id == actual_event.id
    assert expected_event.created_at == actual_event.created_at
    assert expected_event.version == actual_event.version


def test_to_dict_should_return_new_dict_with_event_data(faker):
    expected_event = Event.new(type=faker.word(), payload=faker.pydict(), version=faker.word())

    actual_dict = expected_event.to_dict()

    assert expected_event.type == actual_dict["type"]
    assert expected_event.payload == actual_dict["payload"]
    assert expected_event.id == actual_dict["id"]
    assert expected_event.created_at == actual_dict["created_at"]
    assert expected_event.version == actual_dict["version"]
