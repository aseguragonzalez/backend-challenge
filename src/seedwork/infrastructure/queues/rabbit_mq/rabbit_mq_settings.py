from dataclasses import dataclass


@dataclass(frozen=True)
class RabbitMqSettings:
    host: str
    port: str
    username: str
    password: str
