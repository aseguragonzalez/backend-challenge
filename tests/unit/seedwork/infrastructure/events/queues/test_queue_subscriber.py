import pytest
from tests.unit.seedwork.infrastructure.events.queues.fakes import FakeConsumer

from src.seedwork.infrastructure.events import Event
from src.seedwork.infrastructure.events.queues import QueueSubscriber
from src.seedwork.infrastructure.queues.exceptions import UnrecoverableError


def test_start_listening_should_handle_events_when_consumer_receives_messages(
    faker, events_dispatcher_mock, events_db_mock, unit_of_work_mock
):
    event = Event.new(type=faker.word(), payload=faker.pydict())
    consumer = FakeConsumer()
    subscriber = QueueSubscriber(
        consumer=consumer,
        events_db=events_db_mock,
        events_dispatcher=events_dispatcher_mock,
        unit_of_work=unit_of_work_mock,
    )
    subscriber.start_listening()

    consumer.execute(event.to_bytes())

    events_db_mock.exist.assert_called_once_with(event=event)
    events_db_mock.create.assert_called_once_with(event)
    events_dispatcher_mock.dispatch.assert_called_once_with(event=event)
    unit_of_work_mock.__enter__.assert_called_once()
    unit_of_work_mock.__exit__.assert_called_once()


def test_start_listening_should_raise_unrecoverable_error_when_consumer_receives_invalid_message(
    faker, events_dispatcher_mock, events_db_mock, unit_of_work_mock
):
    consumer = FakeConsumer()
    subscriber = QueueSubscriber(
        consumer=consumer,
        events_db=events_db_mock,
        events_dispatcher=events_dispatcher_mock,
        unit_of_work=unit_of_work_mock,
    )
    subscriber.start_listening()

    with pytest.raises(UnrecoverableError):
        consumer.execute(faker.word().encode("utf-8"))

    events_db_mock.exist.assert_not_called()
    events_db_mock.create.assert_not_called()
    events_dispatcher_mock.dispatch.assert_not_called()
    unit_of_work_mock.__enter__.assert_not_called()
    unit_of_work_mock.__exit__.assert_not_called()


def test_start_listening_should_do_nothing_when_event_was_processed_before(
    faker, events_dispatcher_mock, events_db_mock, unit_of_work_mock
):
    events_db_mock.exist.return_value = True
    event = Event.new(type=faker.word(), payload=faker.pydict())
    consumer = FakeConsumer()
    subscriber = QueueSubscriber(
        consumer=consumer,
        events_db=events_db_mock,
        events_dispatcher=events_dispatcher_mock,
        unit_of_work=unit_of_work_mock,
    )
    subscriber.start_listening()

    consumer.execute(event.to_bytes())

    events_db_mock.exist.assert_called_once_with(event=event)
    events_db_mock.create.assert_not_called()
    events_dispatcher_mock.dispatch.assert_not_called()
    unit_of_work_mock.__enter__.assert_not_called()
    unit_of_work_mock.__exit__.assert_not_called()
