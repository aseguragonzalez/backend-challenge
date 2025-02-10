from typing import Any

from pymongo.client_session import ClientSession
from pymongo.collection import Collection

from src.seedwork.infrastructure.events import Event, EventsDb
from src.seedwork.infrastructure.events.mongo_db.event_model import EventModel


class MongoDbEventsDb(EventsDb[Event]):
    def __init__(self, db_collection: Collection[dict[str, Any]], client_session: ClientSession | None = None) -> None:
        self._db_collection = db_collection
        self._client_session = client_session

    def exist(self, event: Event) -> bool:
        event_model = EventModel.from_event(event)
        document = self._db_collection.find_one(event_model.get_by_id())
        return True if document else False

    def create(self, event: Event) -> None:
        document = EventModel.from_event(event).to_document()
        self._db_collection.insert_one(document, session=self._client_session)
        return None
