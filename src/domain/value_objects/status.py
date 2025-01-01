from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True)
class Status(StrEnum):
    Accepted = "accepted"
    Succeeded = "succeeded"
    Failed = "failed"
