from unittest.mock import Mock

from src.application.services import FailAssistanceService
from src.infrastructure.ports.dlq.events import AssistanceFailedEvent, AssistanceFailedEventHandler


def test_assistance_event_handler(faker):
    event = AssistanceFailedEvent(payload={"id": faker.uuid4()})
    service = Mock(FailAssistanceService)
    service.execute.return_value = None
    handler = AssistanceFailedEventHandler(fail_assistance_service=service)

    handler.handle(event)

    service.execute.assert_called_once()
