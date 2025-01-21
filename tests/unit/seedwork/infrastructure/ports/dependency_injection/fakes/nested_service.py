from tests.unit.seedwork.infrastructure.ports.dependency_injection.fakes.abstract_service import AbstractService
from tests.unit.seedwork.infrastructure.ports.dependency_injection.fakes.external_service import ExternalService


class NestedService:
    def __init__(self, abstract_service: AbstractService, external_service: ExternalService) -> None:
        self.concrete_service = abstract_service
        self.external_service = external_service
