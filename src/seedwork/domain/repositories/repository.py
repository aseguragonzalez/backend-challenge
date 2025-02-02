from abc import ABC, abstractmethod
from typing import TypeVar

from src.seedwork.domain.entities import AggregateRoot


TId = TypeVar("TId")


class Repository(ABC, AggregateRoot[TId]):
    @abstractmethod
    def save(self, entity: AggregateRoot[TId]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get(self, id: TId) -> AggregateRoot[TId]:
        raise NotImplementedError()
