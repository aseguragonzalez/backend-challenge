from tests.unit.seedwork.infrastructure.ports.dependency_injection.fakes.external_service import ExternalService
from tests.unit.seedwork.infrastructure.ports.dependency_injection.fakes.third_party_settings import ThirdPartySettings


class ThirdPartyService(ExternalService):
    def __init__(self, settings: ThirdPartySettings | None) -> None:
        self._settings = settings

    def get_data(self) -> str:
        return "Third party data"
