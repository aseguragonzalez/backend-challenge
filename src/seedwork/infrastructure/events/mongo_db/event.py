from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any
from uuid import UUID

from src.seedwork.infrastructure.events import Event as IntegrationEvent


@dataclass(frozen=True)
class Event:
    _id: str
    type: str
    created_at: str
    id: str
    payload: dict[str, Any]
    version: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "_id": self._id,
            "type": self.type,
            "created_at": self.created_at,
            "id": self.id,
            "payload": self.payload,
            "version": self.version,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Event":
        return cls(
            _id=data["_id"],
            type=data["type"],
            created_at=data["created_at"],
            id=data["id"],
            payload=data["payload"],
            version=data["version"],
        )

    def to_integration_event(self) -> IntegrationEvent:
        payload = Event._deserialize_document(data=self.payload)
        return IntegrationEvent(
            type=self.type,
            created_at=datetime.fromisoformat(self.created_at),
            id=UUID(self.id),
            payload=payload,
            version=self.version,
        )

    @staticmethod
    def _deserialize_document(data: dict[str, Any]) -> dict[str, Any]:
        for key, value in data.items():
            if isinstance(value, str):
                try:
                    data[key] = datetime.fromisoformat(value)
                except ValueError:
                    pass

            if isinstance(value, str):
                try:
                    data[key] = UUID(value)
                except ValueError:
                    pass

            if isinstance(value, str):
                try:
                    data[key] = Decimal(value)
                except (InvalidOperation, TypeError, ValueError):
                    pass

            if isinstance(value, str) and "b'" in value:
                data[key] = value.decode("utf-8")

            if isinstance(value, dict):
                data[key] = Event._deserialize_document(data=value)
        return data

    @classmethod
    def from_integration_event(cls, event: IntegrationEvent) -> "Event":
        payload = Event._serialize_document(data=event.payload)
        return cls(
            _id=str(event.id),
            type=event.type,
            created_at=event.created_at.isoformat(),
            id=str(event.id),
            payload=payload,
            version=event.version,
        )

    @staticmethod
    def _serialize_document(data: dict[str, Any]) -> dict[str, Any]:
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, UUID):
                data[key] = str(value)
            elif isinstance(value, Decimal):
                data[key] = value.to_eng_string()
            elif isinstance(value, dict):
                data[key] = Event._serialize_document(data=value)
            else:
                data[key] = value
        return data
