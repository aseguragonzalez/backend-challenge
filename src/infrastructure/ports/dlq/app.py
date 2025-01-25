from logging import Logger

from src.seedwork.infrastructure.events import EventsSubscriber
from src.seedwork.infrastructure.ports import AppBase
from src.seedwork.infrastructure.ports.dependency_injection import ServiceProvider


class App(AppBase):
    def __init__(self, logger: Logger, service_provider: ServiceProvider | None = None):
        super().__init__(service_provider=service_provider)
        self._logger = logger

    def run(self, *args: dict[str, str], **kwargs: dict[str, str]) -> None:
        with self.service_provider:
            subscriber: EventsSubscriber = self.service_provider.get(EventsSubscriber)  # type:ignore
            subscriber.start_listening()

    def stop(self) -> None:
        subscriber: EventsSubscriber = self.service_provider.get(EventsSubscriber)  # type:ignore
        self._logger.info("Stopping subscriber")
        subscriber.stop_listening()
        self._logger.info("Subscriber is stopped")
