from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any
from uuid import UUID

from bson import Binary

from src.seedwork.infrastructure.events import Event


@dataclass(frozen=True)
class EventModel:
    id: str
    created_at: str
    payload: dict[str, Any]
    type: str
    version: str

    @classmethod
    def from_document(cls, data: dict[str, Any]) -> "EventModel":
        return cls(
            id=data["_id"],
            type=data["type"],
            created_at=data["created_at"],
            payload=data["payload"],
            version=data["version"],
        )

    @classmethod
    def from_event(cls, event: Event) -> "EventModel":
        return cls(
            id=str(event.id),
            created_at=event.created_at.isoformat(),
            type=event.type,
            payload=EventModel._normalize_to_mongo_db(data=event.payload),
            version=event.version,
        )

    @staticmethod
    def _normalize_to_mongo_db(data: dict[str, Any]) -> dict[str, Any]:
        for key, value in data.items():
            if isinstance(value, UUID):
                data[key] = str(value)
            elif isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, bytes):
                data[key] = Binary(value)
            elif isinstance(value, Decimal):
                # HACK: Decimal is not a native type in MongoDB
                data[key] = f"d|{value}"
            elif isinstance(value, Enum):
                data[key] = value.value
            elif isinstance(value, dict):
                data[key] = EventModel._normalize_to_mongo_db(data=value)
        return data

    def to_document(self) -> dict[str, Any]:
        return {
            "_id": self.id,
            "created_at": self.created_at,
            "payload": self.payload,
            "type": self.type,
            "version": self.version,
        }

    def to_event(self) -> Event:
        return Event(
            id=UUID(self.id),
            created_at=datetime.fromisoformat(self.created_at),
            payload=EventModel._desnormalize_from_mongo_db(data=self.payload),
            type=self.type,
            version=self.version,
        )

    @staticmethod
    def _desnormalize_from_mongo_db(data: dict[str, Any]) -> dict[str, Any]:
        for key, value in data.items():
            if isinstance(value, Binary):
                data[key] = bytes(value)
            elif isinstance(value, dict):
                data[key] = EventModel._desnormalize_from_mongo_db(data=value)
            elif isinstance(value, str) and value.startswith("d|"):
                data[key] = Decimal(value.replace("d|", ""))
            elif isinstance(value, str):
                try:
                    data[key] = UUID(value)
                except ValueError:
                    pass
                try:
                    data[key] = datetime.fromisoformat(value)
                except ValueError:
                    pass
        return data

    def get_by_id(self) -> dict[str, str]:
        return {"_id": self.id}
