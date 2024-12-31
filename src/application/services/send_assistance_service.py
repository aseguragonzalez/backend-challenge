from uuid import UUID

from src.domain.repositories import AssistancesRepository
from src.domain.services import ChannelsService


class SendAssistanceService:
    def __init__(self, assistance_repository: AssistancesRepository, channels_service: ChannelsService):
        self._assistance_repository = assistance_repository
        self._channels_service = channels_service

    def execute(self, id: UUID) -> None:
        assistance_request = self._assistance_repository.get(id=id)
        assistance_request.success()
        self._assistance_repository.save(assistance_request=assistance_request)
        self._channels_service.send_assistance_request(assistance_request=assistance_request)
        return None
