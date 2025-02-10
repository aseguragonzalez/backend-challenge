from logging import Logger
from threading import Thread
from unittest.mock import Mock, patch

import pytest

from src.infrastructure.ports.reconciler.app import App
from src.infrastructure.ports.reconciler.services import ReconciliationService


@pytest.mark.unit
@patch("time.sleep")
def test_app_should_wait_reconcile_and_wait(sleep_mock, faker):
    logger = Mock(Logger)
    reconciliation_service = Mock(ReconciliationService)
    delay_time = faker.random_int(min=1, max=60)
    timeout_interval = faker.random_int(min=1, max=60)
    app = App(logger=logger)
    app.register(lambda sp: sp.register(ReconciliationService, lambda _: reconciliation_service))
    sleep_mock.side_effect = lambda _: app.stop()

    def _run_app():
        app.run(delay_time=delay_time, timeout_interval=timeout_interval)

    thread = Thread(target=_run_app)
    thread.start()
    thread.join()

    reconciliation_service.execute.assert_called_once_with(seconds_delayed=delay_time)
    sleep_mock.assert_called_once_with(timeout_interval)
