from src.application.services.get_assistance.request import GetAssistanceRequest
from src.domain.entities import AssistanceRequest
from src.domain.repositories import AssistancesRepository
from src.seedwork.application.services import ApplicationService


class GetAssistanceService(ApplicationService[GetAssistanceRequest, AssistanceRequest]):
    def __init__(self, repository: AssistancesRepository):
        self._repository = repository

    def execute(self, request: GetAssistanceRequest) -> AssistanceRequest:
        return self._repository.get(id=request.id)
