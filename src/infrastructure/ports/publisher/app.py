from logging import Logger

from src.seedwork.infrastructure.events import Event
from src.seedwork.infrastructure.events.mongo_db import MongoDbEventsWatcher
from src.seedwork.infrastructure.ports import AppBase
from src.seedwork.infrastructure.ports.dependency_injection import ServiceProvider
from src.seedwork.infrastructure.queues.producer import Producer


class App(AppBase):
    def __init__(self, logger: Logger, service_provider: ServiceProvider | None = None):
        super().__init__(service_provider=service_provider)
        self._logger = logger

    def run(self, *args: dict[str, str], **kwargs: dict[str, str]) -> None:
        with self.service_provider:
            watcher: MongoDbEventsWatcher = self.service_provider.get(MongoDbEventsWatcher)
            producer: Producer = self.service_provider.get(Producer)  # type: ignore
            watcher.watch(lambda event: self._publish_event(event=event, producer=producer))

    def _publish_event(self, event: Event, producer: Producer) -> None:
        self._logger.info(f"Sending event: {event.id}")
        producer.send_message(event.to_bytes())
        self._logger.info(f"Event sent: {event.id}")

    def stop(self) -> None:
        watcher: MongoDbEventsWatcher = self.service_provider.get(MongoDbEventsWatcher)
        self._logger.info("Stopping watcher")
        watcher.close()
        self._logger.info("Watcher stopped")
