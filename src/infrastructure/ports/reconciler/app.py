import time
from logging import Logger

from src.infrastructure.ports.reconciler.services import ReconciliationService
from src.seedwork.infrastructure.ports import AppBase
from src.seedwork.infrastructure.ports.dependency_injection import ServiceProvider


class App(AppBase):
    def __init__(self, logger: Logger, service_provider: ServiceProvider | None = None) -> None:
        super().__init__(service_provider=service_provider)
        self._logger = logger
        self._is_running: bool = False

    def run(self, *args: dict[str, str], **kwargs: dict[str, str]) -> None:
        self._is_running = True
        delay_time = int(kwargs["delay_time"])
        timeout_interval = int(kwargs["timeout_interval"])
        with self._service_provider as sp:
            reconciliation_service = sp.get(ReconciliationService)
            while self._is_running:
                reconciliation_service.execute(seconds_delayed=delay_time)
                time.sleep(timeout_interval)

    def stop(self) -> None:
        self._logger.info("Stopping recincilier")
        self._is_running = False
        self._logger.info("Reconcilier stopped")
