import logging

from pika.exceptions import AMQPConnectionError

from src.infrastructure.ports.subscriber.app import App
from src.infrastructure.ports.subscriber.dependencies import configure


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("SUBSCRIBER")

    should_run = True
    max_retries = 3

    while should_run and max_retries > 0:
        app = configure(App(logger=logger))
        app.register(lambda sp: sp.register_singleton(logging.Logger, lambda _: logger))
        logger.info("Starting subscriber")
        try:
            app.run()
        except KeyboardInterrupt:
            logger.info("Clossing because of KeyboardInterrupt")
            should_run = False
        except AMQPConnectionError as exc:
            logger.error(f"We have to restart the subscriber app. AMQPConnectionError: {exc}")
            max_retries -= 1
        finally:
            app.stop()

    if max_retries == 0:
        logger.error("We have reached the maximum retries. The subscriber will stop.")

    logger.info("Subscriber stopped")
