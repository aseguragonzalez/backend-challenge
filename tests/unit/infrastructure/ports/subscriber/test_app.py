from logging import Logger
from unittest.mock import Mock, call

from src.infrastructure.ports.subscriber.app import App
from src.seedwork.infrastructure.events import EventsSubscriber


def test_main_should_start_listening():
    events_subscriber = Mock(EventsSubscriber)
    logger = Mock(Logger)
    app = App(logger=logger)
    app.register(lambda sp: sp.register(EventsSubscriber, lambda _: events_subscriber))

    app.run()

    events_subscriber.start_listening.assert_called_once()
    logger.info.assert_has_calls(
        [
            call("Starting app. Press Ctrl+C to end the process."),
            call("Subscriber starts listening"),
            call("Stopping subscriber"),
            call("Subscriber stops listening"),
            call("Subscriber is stopped"),
            call("App closed"),
        ]
    )


def test_main_should_stop_listening_on_keyboard_interrupt():
    events_subscriber = Mock(EventsSubscriber)
    logger = Mock(Logger)
    app = App(logger=logger)
    app.register(lambda sp: sp.register(EventsSubscriber, lambda _: events_subscriber))
    events_subscriber.start_listening.side_effect = KeyboardInterrupt

    app.run()

    events_subscriber.stop_listening.assert_called_once()
    logger.info.assert_has_calls(
        [
            call("Starting app. Press Ctrl+C to end the process."),
            call("Subscriber starts listening"),
            call("Clossing because of KeyboardInterrupt"),
            call("Stopping subscriber"),
            call("Subscriber stops listening"),
            call("Subscriber is stopped"),
            call("App closed"),
        ]
    )
