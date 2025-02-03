from typing import TypeVar

from src.seedwork.domain import UnitOfWork
from src.seedwork.infrastructure.events import Event, EventsDb, EventsDispatcher, EventsSubscriber
from src.seedwork.infrastructure.events.exceptions import DecodingError
from src.seedwork.infrastructure.queues.consumer import Consumer
from src.seedwork.infrastructure.queues.exceptions import UnrecoverableError


TEvent = TypeVar("TEvent", bound=Event)


class QueueSubscriber(EventsSubscriber):
    def __init__(
        self,
        consumer: Consumer,
        events_db: EventsDb[Event],
        unit_of_work: UnitOfWork,
        events_dispatcher: EventsDispatcher,
    ) -> None:
        self._consumer = consumer
        self._events_db = events_db
        self._unit_of_work = unit_of_work
        self._events_dispatcher = events_dispatcher

    def start_listening(self) -> None:
        self._consumer.start(message_handler=self._handle_message)

    def _handle_message(self, message: bytes) -> None:
        try:
            event = Event.from_bytes(data=message)
        except DecodingError:
            raise UnrecoverableError()

        if self._events_db.exist(event=event):
            return None

        with self._unit_of_work:
            self._events_db.create(event)
            self._events_dispatcher.dispatch(event=event)

    def stop_listening(self) -> None:
        self._consumer.cancel()
