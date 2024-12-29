from uuid import uuid4

from tests.unit.seedwork.infrastructure.ports.dependency_injection.fakes.abstract_service import AbstractService


class ConcreteService(AbstractService):
    def __init__(self) -> None:
        self._id = uuid4()

    def id(self) -> str:
        return str(self._id)

    def hello_world(self) -> None:
        return None
