from tests.unit.seedwork.infrastructure.ports.dependency_injection.fakes.service_component import ServiceComponent


class CustomService(ServiceComponent):
    def execute(self) -> None:
        return None
