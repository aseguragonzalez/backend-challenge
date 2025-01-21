from dataclasses import dataclass


@dataclass(frozen=True)
class ThirdPartySettings:
    api_key: str
    host: str
    port: int
