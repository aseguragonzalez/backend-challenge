from logging import Logger

from src.infrastructure.ports.subscriber.events.assistance_succeeded_event import AssistanceSucceededEvent
from src.seedwork.infrastructure.events import EventHandler


class AssistanceSucceededEventHandler(EventHandler[AssistanceSucceededEvent]):
    def __init__(self, logger: Logger):
        self._logger = logger

    def handle(self, event: AssistanceSucceededEvent) -> None:
        self._logger.info(f"Assistance request {event.assistance_id} was succeeded")
