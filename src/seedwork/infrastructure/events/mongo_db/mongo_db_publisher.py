from typing import Any

from pymongo.client_session import ClientSession
from pymongo.collection import Collection

from src.seedwork.infrastructure.events import Event, EventsPublisher
from src.seedwork.infrastructure.events.mongo_db.event import Event as EventDto


class MongoDbPublisher(EventsPublisher):
    def __init__(self, db_collection: Collection[dict[str, Any]], client_session: ClientSession | None = None):
        self._db_collection = db_collection
        self._client_session = client_session

    def publish(self, events: list[Event]) -> None:
        documents = [EventDto.from_integration_event(event).to_dict() for event in events]
        self._db_collection.insert_many(documents=documents, session=self._client_session)
        return None
