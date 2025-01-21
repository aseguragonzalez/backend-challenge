import pytest

from src.infrastructure.ports.subscriber.events import AssistanceCreatedEvent
from src.seedwork.infrastructure.queues.exceptions import UnrecoverableError


def test_assistance_created_event(faker):
    asssistance_id = faker.uuid4()
    event = AssistanceCreatedEvent(payload={"id": asssistance_id})

    assert str(event.assistance_id) == asssistance_id


def test_assistance_created_event_fails_when_no_assistance_id_in_payload():
    event = AssistanceCreatedEvent(payload={})

    with pytest.raises(UnrecoverableError):
        _ = event.assistance_id
