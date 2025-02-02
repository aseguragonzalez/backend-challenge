from src.application.services.send_assistance.send_assistance_request import SendAssistanceRequest
from src.domain.repositories import AssistancesRepository
from src.domain.services import ChannelsService
from src.seedwork.application.services import ApplicationService


class SendAssistanceService(ApplicationService[SendAssistanceRequest, None]):
    def __init__(self, assistance_repository: AssistancesRepository, channels_service: ChannelsService):
        self._assistance_repository = assistance_repository
        self._channels_service = channels_service

    def execute(self, request: SendAssistanceRequest) -> None:
        assistance_request = self._assistance_repository.get(id=request.id)
        assistance_request.success()
        self._assistance_repository.save(entity=assistance_request)
        self._channels_service.send_assistance_request(assistance_request=assistance_request)
        return None
