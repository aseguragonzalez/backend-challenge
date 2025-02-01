import logging
import os

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
        max_retries=int(os.getenv("SETTINGS_MAX_RETRIES")),
        minutes_between_errors=int(os.getenv("SETTINGS_MINUTES_BETWEEN_ERRORS")),
        seconds_between_retries=int(os.getenv("SETTINGS_SECONDS_BETWEEN_RETRIES")),
    )
    component.execute(
        lambda: configure(app=App(logger=logger), logger=logger),
        delay_time=int(os.getenv("SETTINGS_DELAY_TIME")),
        timeout_interval=int(os.getenv("SETTINGS_TIMEOUT_INTERVAL")),
    )
