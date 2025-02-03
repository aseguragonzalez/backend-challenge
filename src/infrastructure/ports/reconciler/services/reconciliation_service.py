from collections.abc import Mapping, Sequence
from datetime import datetime, timedelta, timezone
from typing import Any

from pymongo.collection import Collection

from src.seedwork.infrastructure.events.mongo_db.event import Event
from src.seedwork.infrastructure.queues.producer import Producer


class ReconciliationService:
    def __init__(
        self,
        db_events_collection: Collection[dict[str, Any]],
        db_dlq_events_collection: Collection[dict[str, Any]],
        db_processed_collection: Collection[dict[str, Any]],
        producer: Producer,
    ) -> None:
        self._db_events_collection = db_events_collection
        self._db_dlq_events_collection = db_dlq_events_collection
        self._db_processed_collection = db_processed_collection
        self._producer = producer

    def execute(self, seconds_delayed: int) -> None:
        filter_date = datetime.now(timezone.utc) - timedelta(seconds=seconds_delayed)
        pipeline: Sequence[Mapping[str, Any]] = [
            {"$match": {"created_at": {"$lte": filter_date.isoformat()}}},
            {
                "$lookup": {
                    "from": self._db_processed_collection.name,
                    "localField": "_id",
                    "foreignField": "_id",
                    "as": "processed",
                }
            },
            {
                "$lookup": {
                    "from": self._db_dlq_events_collection.name,
                    "localField": "_id",
                    "foreignField": "_id",
                    "as": "dlq_processed",
                }
            },
            {
                "$match": {
                    "processed": {"$eq": []},
                    "dlq_processed": {"$eq": []},
                }
            },
        ]

        [self._publish_event(document) for document in self._db_events_collection.aggregate(pipeline)]

    def _publish_event(self, document: dict[str, Any]) -> dict[str, Any]:
        self._producer.send_message(Event.from_dict(document).to_integration_event().to_bytes())
        return document
