from uuid import UUID, uuid4

from src.domain.entities import AssistanceRequest
from src.domain.repositories import AssistancesRepository
from src.domain.value_objects import Topic


class CreateAssistanceService:
    def __init__(self, repository: AssistancesRepository):
        self._repository = repository

    def execute(self, topic: Topic, description: str, id: UUID = uuid4()) -> None:
        assistance_request = AssistanceRequest.new(id=id, topic=topic, description=description)
        self._repository.save(assistance_request=assistance_request)
        return None
