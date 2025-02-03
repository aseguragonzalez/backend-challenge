from collections.abc import Callable
from typing import Any

from pymongo.change_stream import CollectionChangeStream
from pymongo.collection import Collection

from src.seedwork.infrastructure.events import Event
from src.seedwork.infrastructure.events.mongo_db.event import Event as EventDto


class MongoDbEventsWatcher:
    def __init__(self, db_collection: Collection[dict[str, Any]]) -> None:
        self._db_collection = db_collection
        self._change_stream: CollectionChangeStream[dict[str, Any]] | None = None

    def watch(self, on_change_event: Callable[[Event], Event]) -> None:
        self._change_stream = self._db_collection.watch()
        [
            on_change_event(EventDto.from_dict(dict(change["fullDocument"])).to_integration_event())
            for change in self._change_stream
            if change["operationType"] == "insert"
        ]

    def close(self) -> None:
        if self._change_stream:
            self._change_stream.close()
