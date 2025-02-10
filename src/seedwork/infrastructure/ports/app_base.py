from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, TypeVar

from src.seedwork.infrastructure.ports.dependency_injection import BasicServiceProvider, ServiceProvider


TService = TypeVar("TService")


class AppBase(ABC):
    def __init__(self, service_provider: ServiceProvider | None) -> None:
        self._service_provider = service_provider if service_provider else BasicServiceProvider()

    @property
    def service_provider(self) -> ServiceProvider:
        return self._service_provider

    def register(self, dependencies: Callable[[ServiceProvider], None]) -> None:
        dependencies(self._service_provider)

    @abstractmethod
    def run(self, *args: tuple[str, Any], **kwargs: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError
