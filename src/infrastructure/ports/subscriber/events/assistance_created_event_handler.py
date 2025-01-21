from src.application.services import SendAssistanceRequest, SendAssistanceService
from src.infrastructure.ports.subscriber.events.assistance_created_event import AssistanceCreatedEvent
from src.seedwork.infrastructure.events import EventHandler


class AssistanceCreatedEventHandler(EventHandler[AssistanceCreatedEvent]):
    def __init__(self, send_assistance_service: SendAssistanceService):
        self._send_assistance_service = send_assistance_service

    def handle(self, event: AssistanceCreatedEvent) -> None:
        request = SendAssistanceRequest(id=event.assistance_id)
        self._send_assistance_service.execute(request=request)
