import inspect
from collections.abc import Callable
from queue import LifoQueue
from typing import TypeVar, get_type_hints

from src.seedwork.infrastructure.ports.dependency_injection.service_provider import ServiceProvider


TService = TypeVar("TService")


class BasicServiceProvider(ServiceProvider):
    _MAX_RECURSION_LEVEL = 10

    def __init__(
        self,
        types: dict[type, type | Callable[[ServiceProvider], type]] = {},
        singleton_types: dict[type, type | Callable[[ServiceProvider], type]] = {},
        context_handled_singleton_types: dict[type, type | Callable[[ServiceProvider], type]] = {},
    ) -> None:
        self._types = types
        self._singleton_types = singleton_types
        self._context_handled_singleton_types = context_handled_singleton_types
        self._instances = {}
        self._stack = LifoQueue()

    def __enter__(self) -> "BasicServiceProvider":
        if not self._stack.empty():
            return self

        for service_type in self._context_handled_singleton_types:
            if service_type not in self._instances:
                continue
            instance = self._instances[service_type]
            instance.__enter__()
            self._stack.put(instance)

        return self

    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb: object) -> None:
        while not self._stack.empty():
            self._stack.get().__exit__(exc_type, exc_val, exc_tb)

    def get(self, service_type: type[TService]) -> TService:
        if service_type in self._singleton_types:
            return self._get_singleton(service_type, level=0)

        if service_type in self._context_handled_singleton_types:
            return self._get_context_handled_singleton(service_type, level=0)

        if service_type in self._types:
            return self._get_new_instance(service_type, level=0)

        raise ValueError(f"Service {service_type} not in service provider")

    def _get_singleton(self, service_type: TService, level: int = 0) -> TService:
        if service_type in self._instances:
            return self._instances[service_type]

        concreate_type = self._singleton_types[service_type]
        self._instances[service_type] = self._create_instance(concreate_type, level=level)
        return self._instances[service_type]

    def _create_instance(self, concreate_type: TService, level: int = 0) -> TService:
        if inspect.isfunction(concreate_type):
            return concreate_type(self)

        hints = get_type_hints(concreate_type.__init__)
        args = {
            arg: self._get_service_or_fail(self._get_hint(hint), level=level)
            for arg, hint in hints.items()
            if arg != "return"
        }
        return concreate_type(**args)

    def _get_hint(self, hint):
        if hasattr(hint, "__args__") and len(hint.__args__) > 1:
            return hint.__args__[0]
        return hint

    def _get_service_or_fail(self, service_type: TService, level: int = 0) -> TService:
        if level > self._MAX_RECURSION_LEVEL:
            raise RuntimeError(f"Max recursion level reached reaching: {service_type}")

        if service_type in self._singleton_types:
            return self._get_singleton(service_type, level=level + 1)

        if service_type in self._context_handled_singleton_types:
            return self._get_context_handled_singleton(service_type, level=level + 1)

        if service_type in self._types:
            return self._get_new_instance(service_type, level=level + 1)

        raise ValueError(f"Service {service_type} not in service provider")

    def _get_context_handled_singleton(self, service_type: TService, level: int = 0) -> TService:
        if service_type in self._instances:
            return self._instances[service_type]

        concreate_type = self._context_handled_singleton_types[service_type]
        if not hasattr(concreate_type, "__enter__") or not hasattr(concreate_type, "__exit__"):
            raise ValueError(f"Service {service_type} does not complaint with context manager protocol")

        self._instances[service_type] = self._create_instance(concreate_type, level=level)
        self._instances[service_type].__enter__()
        self._stack.put(self._instances[service_type])
        return self._instances[service_type]

    def _get_new_instance(self, service_type: TService, level: int = 0) -> TService:
        return self._create_instance(self._types[service_type], level=level)

    def register(
        self, service_type: TService, concreate_type: TService | Callable[[ServiceProvider], TService]
    ) -> None:
        self._types[service_type] = concreate_type

    def register_singleton(
        self, service_type: TService, concreate_type: TService | Callable[[ServiceProvider], TService]
    ) -> None:
        self._singleton_types[service_type] = concreate_type

    def register_context_managed_singleton(
        self, service_type: TService, type_rule: TService | Callable[[ServiceProvider], TService]
    ) -> None:
        self._context_handled_singleton_types[service_type] = type_rule
