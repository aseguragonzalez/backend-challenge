from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TypeVar


TService = TypeVar("TService")


class ServiceProvider(ABC):
    @abstractmethod
    def __enter__(self) -> "ServiceProvider":
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb: object) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, service_type: type[TService]) -> TService:
        raise NotImplementedError

    @abstractmethod
    def register(self, service_type: TService, type_rule: TService | Callable[["ServiceProvider"], TService]) -> None:
        raise NotImplementedError

    @abstractmethod
    def register_singleton(
        self, service_type: TService, type_rule: TService | Callable[["ServiceProvider"], TService]
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def register_context_managed_singleton(
        self, service_type: TService, type_rule: TService | Callable[["ServiceProvider"], TService]
    ) -> None:
        raise NotImplementedError
