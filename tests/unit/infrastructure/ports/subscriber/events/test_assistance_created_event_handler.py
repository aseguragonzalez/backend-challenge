from logging import Logger
from unittest.mock import Mock

from src.application.services import SendAssistanceService
from src.infrastructure.ports.subscriber.events import AssistanceCreatedEvent, AssistanceCreatedEventHandler


def test_assistance_created_event_handler(faker):
    event = AssistanceCreatedEvent(payload={"id": faker.uuid4()})
    service = Mock(SendAssistanceService)
    logger = Mock(Logger)
    service.execute.return_value = None
    handler = AssistanceCreatedEventHandler(send_assistance_service=service, logger=logger)

    handler.handle(event)

    service.execute.assert_called_once()
