from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from src.seedwork.domain.entities import AggregateRoot


TId = TypeVar("TId")
TAggregateRoot = TypeVar("TAggregateRoot", bound=AggregateRoot[Any])


class Repository(ABC, Generic[TAggregateRoot, TId]):
    @abstractmethod
    def save(self, entity: TAggregateRoot) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get(self, id: TId) -> TAggregateRoot:
        raise NotImplementedError()
