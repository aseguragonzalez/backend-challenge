import logging
import os

from src.infrastructure.ports.dlq.app import App
from src.infrastructure.ports.dlq.dependencies import configure
from src.seedwork.infrastructure.ports.component import Component


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("DLQ-SUBSCRIBER")
    logger.info("Starting DLQ subscriber. Press Ctrl+C to end the process.")
    component = Component(
        logger=logger,
        app_name="DLQ subscriber",
        max_retries=int(os.environ["SETTINGS_MAX_RETRIES"]),
        minutes_between_errors=int(os.environ["SETTINGS_MINUTES_BETWEEN_ERRORS"]),
        seconds_between_retries=int(os.environ["SETTINGS_SECONDS_BETWEEN_RETRIES"]),
    )
    component.execute(lambda: configure(app=App(logger=logger), logger=logger))
