from tests.unit.seedwork.infrastructure.ports.dependency_injection.fakes.service import Service


class CustomService(Service):
    def execute(self) -> None:
        return None
