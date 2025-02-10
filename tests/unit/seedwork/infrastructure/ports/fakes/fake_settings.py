from dataclasses import dataclass


@dataclass(frozen=True)
class FakeSettings:
    service_host: str
    service_port: int
    api_key: str
