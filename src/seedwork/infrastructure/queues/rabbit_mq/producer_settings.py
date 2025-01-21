from dataclasses import dataclass


@dataclass(frozen=True)
class ProducerSettings:
    exchange: str
    routing_key: str
