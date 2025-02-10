from logging import Logger
from unittest.mock import Mock

import pytest

from src.infrastructure.ports.subscriber.app import App
from src.seedwork.infrastructure.events import EventsSubscriber


@pytest.mark.unit
def test_main_should_start_listening():
    events_subscriber = Mock(EventsSubscriber)
    logger = Mock(Logger)
    app = App(logger=logger)
    app.register(lambda sp: sp.register(EventsSubscriber, lambda _: events_subscriber))

    app.run()

    events_subscriber.start_listening.assert_called_once()
