from logging import Logger

from src.seedwork.infrastructure.events import EventsSubscriber
from src.seedwork.infrastructure.ports import AppBase
from src.seedwork.infrastructure.ports.dependency_injection import ServiceProvider


class App(AppBase):
    def __init__(self, logger: Logger, service_provider: ServiceProvider | None = None):
        super().__init__(service_provider=service_provider)
        self._logger = logger

    def run(self, *args: dict[str, str], **kwargs: dict[str, str]) -> None:
        self._logger.info("Starting DLQ subscriber. Press Ctrl+C to end the process.")
        with self.service_provider:
            subscriber: EventsSubscriber = self.service_provider.get(EventsSubscriber)  # type:ignore
            self._logger.info("Subscriber starts listening")
            try:
                subscriber.start_listening()
            except KeyboardInterrupt:
                self._logger.info("Clossing because of KeyboardInterrupt")
            finally:
                self.stop()
                self._logger.info("DLQ subscriber closed")

    def stop(self) -> None:
        self._logger.info("Stopping subscriber")
        subscriber: EventsSubscriber = self.service_provider.get(EventsSubscriber)  # type:ignore
        self._logger.info("Subscriber stops listening")
        subscriber.stop_listening()
        self._logger.info("Subscriber is stopped")
