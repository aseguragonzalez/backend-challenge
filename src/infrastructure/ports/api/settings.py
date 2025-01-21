from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    assistance_api_keys: str
    assistance_collection_name: str
    assistance_database_name: str
    assistance_database_url: str
    events_collection_name: str
    events_database_name: str
    events_database_url: str
