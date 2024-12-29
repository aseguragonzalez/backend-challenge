import logging


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Dead letter queue (DLQ) Subscriber started. Press Ctrl+C to stop")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")


if __name__ == "__main__":
    main()
