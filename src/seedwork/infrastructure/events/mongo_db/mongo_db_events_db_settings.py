from dataclasses import dataclass


@dataclass(frozen=True)
class MongoDbEventsDbSettings:
    database_name: str
    database_url: str
    collection_name: str
    processed_collection_name: str
    dlq_processed_collection_name: str
