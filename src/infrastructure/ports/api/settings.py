from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_keys: str
    database_url: str
    database_name: str
