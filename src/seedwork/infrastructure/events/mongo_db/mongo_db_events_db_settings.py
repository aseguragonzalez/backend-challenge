from dataclasses import dataclass


@dataclass(frozen=True)
class MongoDbEventsDbSettings:
    database_url: str
    database_name: str
    collection_name: str | None = None
    processed_collection_name: str | None = None
