from logging import Logger

from src.infrastructure.ports.subscriber.events.assistance_failed_event import AssistanceFailedEvent
from src.seedwork.infrastructure.events import EventHandler


class AssistanceFailedEventHandler(EventHandler[AssistanceFailedEvent]):
    def __init__(self, logger: Logger):
        self._logger = logger

    def handle(self, event: AssistanceFailedEvent) -> None:
        self._logger.info(f"Assistance request {event.assistance_id} was failed")
