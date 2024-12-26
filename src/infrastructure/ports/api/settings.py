from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_keys: str
