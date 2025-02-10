from dataclasses import dataclass, field


@dataclass(frozen=True)
class EnvironmentVariables:
    api_key: str = field(default="api-key")
    host: str = field(default="host")
    port: int = field(default=80)
