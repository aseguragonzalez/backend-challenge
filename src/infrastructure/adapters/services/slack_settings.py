from dataclasses import dataclass


@dataclass(frozen=True)
class SlackSettings:
    channel: str
    url: str
    private_key: str
