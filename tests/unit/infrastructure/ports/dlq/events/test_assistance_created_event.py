import pytest

from src.infrastructure.ports.dlq.events import AssistanceCreatedEvent
from src.seedwork.infrastructure.queues.exceptions import UnrecoverableError


@pytest.mark.unit
def test_assistance_failed_event(faker):
    asssistance_id = faker.uuid4()
    event = AssistanceCreatedEvent(payload={"id": asssistance_id})

    assert str(event.assistance_id) == asssistance_id


@pytest.mark.unit
def test_assistance_failed_event_fails_when_no_assistance_id_in_payload():
    event = AssistanceCreatedEvent(payload={})

    with pytest.raises(UnrecoverableError):
        _ = event.assistance_id
