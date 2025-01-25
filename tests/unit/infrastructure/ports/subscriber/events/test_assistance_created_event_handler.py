from logging import Logger
from unittest.mock import Mock

import pytest

from src.application.services import SendAssistanceService
from src.domain.exceptions import AssistanceRequestNotFoundError, UnavailableChangeOfStatusError
from src.domain.services import UnavailableChannelError
from src.infrastructure.ports.subscriber.events import AssistanceCreatedEvent, AssistanceCreatedEventHandler
from src.seedwork.infrastructure.queues.exceptions import RecoverableError, UnrecoverableError


def test_assistance_created_event_handler(faker):
    event = AssistanceCreatedEvent(payload={"id": faker.uuid4()})
    service = Mock(SendAssistanceService)
    logger = Mock(Logger)
    service.execute.return_value = None
    handler = AssistanceCreatedEventHandler(send_assistance_service=service, logger=logger)

    handler.handle(event)

    service.execute.assert_called_once()


def test_assistance_created_event_handler_with_unrecoverable_error(faker):
    event = AssistanceCreatedEvent(payload={"id": faker.uuid4()})
    service = Mock(SendAssistanceService)
    logger = Mock(Logger)
    service.execute.side_effect = faker.random_element(
        elements=[AssistanceRequestNotFoundError(), UnavailableChangeOfStatusError()]
    )

    with pytest.raises(UnrecoverableError):
        handler = AssistanceCreatedEventHandler(send_assistance_service=service, logger=logger)
        handler.handle(event)


def test_assistance_created_event_handler_with_recoverable_error(faker):
    event = AssistanceCreatedEvent(payload={"id": faker.uuid4()})
    service = Mock(SendAssistanceService)
    logger = Mock(Logger)
    service.execute.side_effect = UnavailableChannelError()

    with pytest.raises(RecoverableError):
        handler = AssistanceCreatedEventHandler(send_assistance_service=service, logger=logger)
        handler.handle(event)
