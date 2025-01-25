from logging import Logger
from unittest.mock import Mock

import pytest

from src.application.services import FailAssistanceService
from src.domain.exceptions import AssistanceRequestNotFoundError, UnavailableChangeOfStatusError
from src.infrastructure.ports.dlq.events import AssistanceCreatedEvent, AssistanceCreatedEventHandler
from src.seedwork.infrastructure.queues.exceptions import UnrecoverableError


def test_assistance_event_handler(faker):
    logger = Mock(Logger)
    event = AssistanceCreatedEvent(payload={"id": faker.uuid4()})
    service = Mock(FailAssistanceService)
    service.execute.return_value = None
    handler = AssistanceCreatedEventHandler(fail_assistance_service=service, logger=logger)

    handler.handle(event)

    service.execute.assert_called_once()


def test_assistance_created_event_handler_with_unrecoverable_error(faker):
    event = AssistanceCreatedEvent(payload={"id": faker.uuid4()})
    service = Mock(FailAssistanceService)
    logger = Mock(Logger)
    service.execute.side_effect = faker.random_element(
        elements=[AssistanceRequestNotFoundError(), UnavailableChangeOfStatusError()]
    )

    with pytest.raises(UnrecoverableError):
        handler = AssistanceCreatedEventHandler(fail_assistance_service=service, logger=logger)
        handler.handle(event)
