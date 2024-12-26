from uuid import UUID

from src.domain.repositories import AssistancesRepository


class FailAssistanceService:
    def __init__(self, assistance_repository: AssistancesRepository):
        self._assistance_repository = assistance_repository

    def execute(self, id: UUID) -> None:
        assistance_request = self._assistance_repository.get(id=id)
        assistance_request.fail()
        self._assistance_repository.save(assistance_request=assistance_request)
        return None
