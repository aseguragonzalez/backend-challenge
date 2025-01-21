from dataclasses import dataclass


@dataclass
class MongoDbEventsDbSettings:
    database_url: str
    database_name: str
    collection_name: str
