from logging import Logger

from src.application.services import SendAssistanceRequest, SendAssistanceService
from src.domain.services import UnavailableChannelError
from src.infrastructure.ports.subscriber.events.assistance_created_event import AssistanceCreatedEvent
from src.seedwork.infrastructure.events import EventHandler
from src.seedwork.infrastructure.queues.exceptions import RecoverableError


class AssistanceCreatedEventHandler(EventHandler[AssistanceCreatedEvent]):
    def __init__(self, send_assistance_service: SendAssistanceService, logger: Logger) -> None:
        self._send_assistance_service = send_assistance_service
        self._logger = logger

    def handle(self, event: AssistanceCreatedEvent) -> None:
        self._logger.info(f"Handling assistance created event {event.assistance_id}")
        request = SendAssistanceRequest(id=event.assistance_id)
        try:
            self._send_assistance_service.execute(request=request)
        except UnavailableChannelError as exc:
            self._logger.error(f"Channel is not available for: {exc}")
            raise RecoverableError(message=f"Channel is not available for assistance {event.assistance_id}")
        finally:
            self._logger.info(f"Handled assistance created event {event.assistance_id}")
