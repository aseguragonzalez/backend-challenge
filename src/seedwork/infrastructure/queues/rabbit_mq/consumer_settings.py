from dataclasses import dataclass


@dataclass(frozen=True)
class ConsumerSettings:
    queue_name: str
