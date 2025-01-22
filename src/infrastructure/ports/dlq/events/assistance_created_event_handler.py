from src.application.services import FailAssistanceRequest, FailAssistanceService
from src.infrastructure.ports.dlq.events.assistance_created_event import AssistanceCreatedEvent
from src.seedwork.infrastructure.events import EventHandler


class AssistanceCreatedEventHandler(EventHandler[AssistanceCreatedEvent]):
    def __init__(self, fail_assistance_service: FailAssistanceService):
        self._fail_assistance_service = fail_assistance_service

    def handle(self, event: AssistanceCreatedEvent) -> None:
        request = FailAssistanceRequest(id=event.assistance_id)
        self._fail_assistance_service.execute(request=request)
