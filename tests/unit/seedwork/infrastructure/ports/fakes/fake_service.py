from tests.unit.seedwork.infrastructure.ports.fakes.fake_settings import FakeSettings


class FakeService:
    def __init__(self, settings: FakeSettings) -> None:
        self._host = settings.service_host
        self._port = settings.service_port
        self._api_key = settings.api_key

    def execute(self) -> None:
        return None
