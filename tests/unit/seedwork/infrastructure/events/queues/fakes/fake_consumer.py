from collections.abc import Callable

from src.seedwork.infrastructure.queues import Consumer


class FakeConsumer(Consumer):
    def __init__(self) -> None:
        self._message_handler: Callable[[bytes], None] | None = None

    def __enter__(self) -> "FakeConsumer":
        return self

    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb: object) -> None:
        return None

    def start(self, message_handler: Callable[[bytes], None]) -> None:
        self._message_handler = message_handler

    def cancel(self) -> None:
        return None

    def execute(self, message: bytes) -> None:
        if not self._message_handler:
            raise ValueError("Message handler is not set")

        self._message_handler(message)
