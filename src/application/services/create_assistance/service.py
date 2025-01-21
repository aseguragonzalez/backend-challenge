from src.application.services.create_assistance.request import CreateAssistanceRequest
from src.domain.entities import AssistanceRequest
from src.domain.repositories import AssistancesRepository
from src.seedwork.application.services import ApplicationService


class CreateAssistanceService(ApplicationService[CreateAssistanceRequest, None]):
    def __init__(self, repository: AssistancesRepository):
        self._repository = repository

    def execute(self, request: CreateAssistanceRequest) -> None:
        assistance_request = AssistanceRequest.new(id=request.id, topic=request.topic, description=request.description)
        self._repository.save(entity=assistance_request)
        return None
