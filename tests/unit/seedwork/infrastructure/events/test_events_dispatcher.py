from unittest.mock import Mock

from tests.unit.seedwork.infrastructure.events.fakes import ConcreteEvent, CustomDispatcher

from src.seedwork.infrastructure.events import Event, EventHandler


def test_dispatch_should_handle_event(faker):
    event = Event.new(type="concrete_event", payload={"id": str(faker.uuid4())})
    concrete_event = ConcreteEvent.from_event(event=event)
    handler_1 = Mock(EventHandler)
    handler_2 = Mock(EventHandler)
    event_handlers = {ConcreteEvent: [handler_1, handler_2]}
    events_dispatcher = CustomDispatcher(event_handlers=event_handlers)

    events_dispatcher.dispatch(event=event)

    # Assert
    handler_1.handle.assert_called_once_with(event=concrete_event)
    handler_2.handle.assert_called_once_with(event=concrete_event)


def test_dispatch_should_ignore_event_when_it_is_not_mapped(faker):
    event = Event.new(type="concrete_event", payload={"id": str(faker.uuid4())})
    handler_1 = Mock(EventHandler)
    handler_2 = Mock(EventHandler)
    event_handlers = {Event: [handler_1, handler_2]}
    events_dispatcher = CustomDispatcher(event_handlers=event_handlers)

    events_dispatcher.dispatch(event=event)

    # Assert
    handler_1.handle.assert_not_called()
    handler_2.handle.assert_not_called()
