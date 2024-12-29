from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True)
class Topic(StrEnum):
    Sales = "sales"
    Pricing = "pricing"
