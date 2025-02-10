import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from src.seedwork.domain.events import DomainEvent
from src.seedwork.infrastructure import CustomJSONDecoder, CustomJSONEncoder
from src.seedwork.infrastructure.events.exceptions import DecodingError, EncodingError


@dataclass(frozen=True)
class Event:
    _DEFAULT_VERSION = "v1.0"
    type: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    id: UUID = field(default_factory=uuid4)
    payload: dict[str, Any] = field(default_factory=dict)
    version: str = field(default=_DEFAULT_VERSION)

    @classmethod
    def from_bytes(cls, data: bytes) -> "Event":
        try:
            decoded_data = data.decode("utf-8")
        except UnicodeDecodeError:
            raise DecodingError()
        return cls.from_json(data=decoded_data)

    @classmethod
    def from_domain_event(cls, event: DomainEvent) -> "Event":
        return cls.new(
            type=event.type, payload=event.payload, created_at=event.created_at, id=event.id, version=event.version
        )

    @classmethod
    def from_json(cls, data: str) -> "Event":
        try:
            json_data = json.loads(data, cls=CustomJSONDecoder)
        except json.JSONDecodeError:
            raise DecodingError()
        return cls(**json_data)

    @classmethod
    def new(
        cls,
        payload: dict[str, Any],
        type: str,
        created_at: datetime = datetime.now(timezone.utc),
        id: UUID = uuid4(),
        version: str = _DEFAULT_VERSION,
    ) -> "Event":
        return cls(type=type, payload=payload, created_at=created_at, id=id, version=version)

    def to_bytes(self) -> bytes:
        return self.to_json().encode("utf-8")

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "created_at": self.created_at,
            "id": self.id,
            "payload": self.payload,
            "version": self.version,
        }

    def to_json(self) -> str:
        try:
            return json.dumps(self.to_dict(), cls=CustomJSONEncoder)
        except UnicodeEncodeError:
            raise EncodingError()
