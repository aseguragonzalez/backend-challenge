from typing import Any

from tests.unit.seedwork.infrastructure.ports.fakes.fake_service import FakeService

from src.seedwork.infrastructure.ports import AppBase
from src.seedwork.infrastructure.ports.dependency_injection import ServiceProvider


class FakeApp(AppBase):
    def __init__(self, service_provider: ServiceProvider | None = None):
        super().__init__(service_provider=service_provider)

    def run(self, *args: tuple[str, Any], **kwargs: dict[str, Any]) -> None:
        service = self.service_provider.get(FakeService)
        service.execute()

    def stop(self) -> None:
        pass
