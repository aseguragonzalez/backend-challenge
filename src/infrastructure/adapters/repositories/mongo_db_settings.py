from dataclasses import dataclass


@dataclass
class MongoDbSettings:
    database_url: str
    database_name: str
    collection_name: str
