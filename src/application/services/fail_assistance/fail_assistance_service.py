from src.application.services.fail_assistance.fail_assistance_request import FailAssistanceRequest
from src.domain.repositories import AssistancesRepository
from src.seedwork.application.services import ApplicationService


class FailAssistanceService(ApplicationService[FailAssistanceRequest, None]):
    def __init__(self, assistance_repository: AssistancesRepository):
        self._assistance_repository = assistance_repository

    def execute(self, request: FailAssistanceRequest) -> None:
        assistance_request = self._assistance_repository.get(id=request.id)
        assistance_request.fail()
        self._assistance_repository.save(entity=assistance_request)
        return None
