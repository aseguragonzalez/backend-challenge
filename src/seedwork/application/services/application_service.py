from abc import ABC, abstractmethod
from typing import Generic, TypeVar


T = TypeVar("T")
Z = TypeVar("Z")


class ApplicationService(ABC, Generic[T, Z]):
    @abstractmethod
    def execute(self, request: T) -> Z:
        raise NotImplementedError()
