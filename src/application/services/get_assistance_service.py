from uuid import UUID

from src.domain.entities import AssistanceRequest
from src.domain.repositories import AssistancesRepository


class GetAssistanceService:
    def __init__(self, repository: AssistancesRepository):
        self._repository = repository

    def execute(self, id: UUID) -> AssistanceRequest:
        return self._repository.get(id=id)
