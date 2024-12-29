import pytest

from src.infrastructure.ports.dlq.events import AssistanceFailedEvent


def test_assistance_failed_event(faker):
    asssistance_id = faker.uuid4()
    event = AssistanceFailedEvent(payload={"id": asssistance_id})

    assert str(event.assistance_id) == asssistance_id


def test_assistance_failed_event_fails_when_no_assistance_id_in_payload():
    event = AssistanceFailedEvent(payload={})

    with pytest.raises(ValueError):
        _ = event.assistance_id
