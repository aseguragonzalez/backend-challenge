from tests.unit.seedwork.infrastructure.ports.dependency_injection.fakes.custom_service import CustomService
from tests.unit.seedwork.infrastructure.ports.dependency_injection.fakes.service_component import ServiceComponent


class ServiceDecorator(ServiceComponent):
    def __init__(self, service: CustomService) -> None:
        self._service = service

    def execute(self) -> None:
        return None
