from typing import Any
from uuid import UUID

from pymongo.client_session import ClientSession
from pymongo.collection import Collection

from src.domain.entities import AssistanceRequest
from src.domain.exceptions import AssistanceRequestNotFoundError
from src.domain.repositories import AssistancesRepository
from src.domain.value_objects import Status, Topic


class MongoDbAssistancesRepository(AssistancesRepository):
    def __init__(self, db_collection: Collection, client_session: ClientSession | None = None) -> None:
        self._db_collection = db_collection
        self._client_session = client_session

    def save(self, entity: AssistanceRequest) -> None:
        id = str(entity.id)
        request_dto = {
            "_id": id,
            "topic": entity.topic.value,
            "description": entity.description,
            "status": entity.status.value,
        }
        self._db_collection.update_one(
            filter={"_id": id}, update={"$set": request_dto}, upsert=True, session=self._client_session
        )
        return None

    def get(self, id: UUID) -> AssistanceRequest:
        dto: dict[Any, Any] | None = self._db_collection.find_one({"_id": str(id)})
        if not dto:
            raise AssistanceRequestNotFoundError()

        return AssistanceRequest.stored(
            id=UUID(dto["_id"]),
            description=str(dto["description"]),
            topic=Topic(dto["topic"]),
            status=Status(dto["status"]),
        )
