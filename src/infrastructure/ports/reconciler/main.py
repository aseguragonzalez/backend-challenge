import logging
import os
from typing import Any

from src.infrastructure.ports.reconciler.app import App
from src.infrastructure.ports.reconciler.dependencies import configure
from src.seedwork.infrastructure.ports.component import Component


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("RECONCILER")
    logger.info("Starting reconciler component. Press Ctrl+C to end the process.")
    component = Component(
        logger=logger,
        app_name="Reconciler",
        max_retries=int(os.environ["SETTINGS_MAX_RETRIES"]),
        minutes_between_errors=int(os.environ["SETTINGS_MINUTES_BETWEEN_ERRORS"]),
        seconds_between_retries=int(os.environ["SETTINGS_SECONDS_BETWEEN_RETRIES"]),
    )
    params: dict[str, Any] = {
        "delay_time": int(os.environ["SETTINGS_DELAY_TIME"]),
        "timeout_interval": int(os.environ["SETTINGS_TIMEOUT_INTERVAL"]),
    }
    component.execute(lambda: configure(app=App(logger=logger), logger=logger), **params)
