from logging import Logger

from src.application.services import FailAssistanceRequest, FailAssistanceService
from src.domain.exceptions import AssistanceRequestNotFoundError, UnavailableChangeOfStatusError
from src.infrastructure.ports.dlq.events.assistance_created_event import AssistanceCreatedEvent
from src.seedwork.infrastructure.events import EventHandler
from src.seedwork.infrastructure.queues.exceptions import UnrecoverableError


class AssistanceCreatedEventHandler(EventHandler[AssistanceCreatedEvent]):
    def __init__(self, fail_assistance_service: FailAssistanceService, logger: Logger):
        self._fail_assistance_service = fail_assistance_service
        self._logger = logger

    def handle(self, event: AssistanceCreatedEvent) -> None:
        self._logger.info(f"Handling assistance created event {event.assistance_id}")
        request = FailAssistanceRequest(id=event.assistance_id)
        try:
            self._fail_assistance_service.execute(request=request)
        except (AssistanceRequestNotFoundError, UnavailableChangeOfStatusError) as exc:
            self._logger.error(f"{exc}")
            raise UnrecoverableError(message=f"Inconsistency in Assistance {event.assistance_id}")
        finally:
            self._logger.info(f"Handled assistance created event {event.assistance_id}")
