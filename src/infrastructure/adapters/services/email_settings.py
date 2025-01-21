from dataclasses import dataclass


@dataclass
class EmailSettings:
    from_email: str
    to_email: str
    server: str
    port: int
    username: str
    password: str
