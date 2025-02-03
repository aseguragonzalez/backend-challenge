from typing import Any

from pymongo.client_session import ClientSession
from pymongo.collection import Collection

from src.seedwork.infrastructure.events import Event, EventsDb
from src.seedwork.infrastructure.events.mongo_db.event import Event as EventDto


class MongoDbEventsDb(EventsDb[Event]):
    def __init__(self, db_collection: Collection[dict[str, Any]], client_session: ClientSession | None = None) -> None:
        self._db_collection = db_collection
        self._client_session = client_session

    def exist(self, event: Event) -> bool:
        event_dto = EventDto.from_integration_event(event)
        document = self._db_collection.find_one({"_id": str(event_dto._id)})
        return True if document else False

    def create(self, event: Event) -> None:
        document = EventDto.from_integration_event(event).to_dict()
        self._db_collection.insert_one(document, session=self._client_session)
        return None
