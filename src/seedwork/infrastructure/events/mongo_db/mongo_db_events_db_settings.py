from dataclasses import dataclass


@dataclass(frozen=True)
class MongoDbEventsDbSettings:
    database_name: str
    database_url: str
    collection_name: str | None = None
    processed_collection_name: str | None = None
