import math
from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from logging import Logger
from time import sleep

from pika.exceptions import AMQPConnectionError

from src.seedwork.infrastructure.ports import AppBase


class Component:
    def __init__(
        self, logger: Logger, app_name: str, max_retries: int, minutes_between_errors: int, seconds_between_retries: int
    ) -> None:
        self._logger = logger
        self._app_name = app_name
        self._max_retries = max_retries
        self._minutes_between_errors = minutes_between_errors
        self._seconds_between_retries = seconds_between_retries
        self._is_running = True
        self._reboots_number = 0
        self._last_reboot: datetime | None = None

    def execute(self, create_app: Callable[[], AppBase], **kwargs: dict[str, str]) -> None:
        while self._is_running:
            app = create_app()
            self._logger.info(f"Starting {self._app_name}")
            try:
                app.run(**kwargs)
            except KeyboardInterrupt:
                self._quit()
            except AMQPConnectionError:
                self._reboot()
            finally:
                app.stop()
        self._logger.info(f"{self._app_name} stopped")

    def _quit(self) -> None:
        self._logger.info("We have to close the app beacuse of a KeyboardInterrupt.")
        self._is_running = False

    def _reboot(self) -> None:
        if self._last_reboot is None:
            self._last_reboot = datetime.now(timezone.utc)

        self._reboots_number = 0 if self._should_reset_reboots_number() else self._reboots_number + 1
        if self._reboots_number >= self._max_retries:
            self._logger.error(f"We have reached the maximum retries. The {self._app_name} is going to stop.")
            self._is_running = False
            return None

        sleep_time = self._get_sleep_time()
        self._logger.info(f"We have to wait during {sleep_time} seconds before reboot the {self._app_name}.")
        sleep(sleep_time)
        self._logger.info(f"We are ready to reboot {self._app_name}.")

    def _should_reset_reboots_number(self) -> bool:
        return datetime.now(timezone.utc) - self._last_reboot > timedelta(minutes=self._minutes_between_errors)

    def _get_sleep_time(self) -> float:
        return (math.e**self._reboots_number) * self._seconds_between_retries
