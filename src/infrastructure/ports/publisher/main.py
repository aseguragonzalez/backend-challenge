import logging

from pika.exceptions import AMQPConnectionError

from src.infrastructure.ports.publisher.app import App
from src.infrastructure.ports.publisher.dependencies import configure


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("PUBLISHER")
    logger.info("Starting publisher. Press Ctrl+C to end the process.")

    should_run = True
    max_retries = 3
    while should_run and max_retries > 0:
        app = configure(App(logger=logger))
        logger.info("Starting watcher events insertion")
        try:
            app.run()
        except KeyboardInterrupt:
            logger.info("Stoping watcher events insertion")
            should_run = False
        except AMQPConnectionError as exc:
            logger.error(f"We have to restart the publisher app. AMQPConnectionError: {exc}")
            max_retries -= 1
        finally:
            app.stop()

    if max_retries == 0:
        logger.error("We have reached the maximum retries. The publisher will stop.")

    logger.info("Publisher stopped")
