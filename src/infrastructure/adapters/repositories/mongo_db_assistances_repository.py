from uuid import UUID

from pymongo.client_session import ClientSession
from pymongo.collection import Collection

from src.domain.entities import AssistanceRequest
from src.domain.exceptions import AssistanceRequestNotFoundError
from src.domain.repositories import AssistancesRepository
from src.infrastructure.adapters.repositories.assistantce_request_model import AssistanceRequestModel


class MongoDbAssistancesRepository(AssistancesRepository):
    def __init__(self, db_collection: Collection[dict[str, str]], client_session: ClientSession | None = None) -> None:
        self._db_collection = db_collection
        self._client_session = client_session

    def save(self, entity: AssistanceRequest) -> None:
        model = AssistanceRequestModel.from_entity(entity)
        self._db_collection.update_one(
            filter=model.get_by_id(), update={"$set": model.to_document()}, upsert=True, session=self._client_session
        )
        return None

    def get(self, id: UUID) -> AssistanceRequest:
        document: dict[str, str] | None = self._db_collection.find_one(AssistanceRequestModel.get_by_id_filter(id))
        if not document:
            raise AssistanceRequestNotFoundError()

        return AssistanceRequestModel.from_document(document).to_entity()
