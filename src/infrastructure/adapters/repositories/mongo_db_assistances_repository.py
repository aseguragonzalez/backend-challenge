from typing import Any
from uuid import UUID

from pymongo.collection import Collection

from src.domain.entities import AssistanceRequest
from src.domain.exceptions import AssistanceRequestNotFoundError
from src.domain.repositories import AssistancesRepository
from src.domain.value_objects import Status, Topic


class MongoDbAssistancesRepository(AssistancesRepository):
    def __init__(self, db_collection: Collection):
        self._db_collection = db_collection

    def save(self, assistance_request: AssistanceRequest) -> None:
        id = str(assistance_request.id)
        request_dto = {
            "id": id,
            "topic": assistance_request.topic.value,
            "description": assistance_request.description,
            "status": assistance_request.status.value,
        }
        self._db_collection.update_one(filter={"id": id}, update={"$set": request_dto}, upsert=True)
        return None

    def get(self, id: UUID) -> AssistanceRequest:
        dto: dict[Any, Any] | None = self._db_collection.find_one({"id": str(id)})

        if dto:
            return AssistanceRequest.stored(
                id=UUID(dto["id"]),
                description=str(dto["description"]),
                topic=Topic(dto["topic"]),
                status=Status(dto["status"]),
            )

        raise AssistanceRequestNotFoundError()
