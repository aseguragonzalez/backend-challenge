from abc import ABC, abstractmethod
from collections.abc import Callable


class Consumer(ABC):
    @abstractmethod
    def __enter__(self) -> "Consumer":
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb: object) -> None:
        raise NotImplementedError

    @abstractmethod
    def start(self, message_handler: Callable[[bytes], None]) -> None:
        raise NotImplementedError

    @abstractmethod
    def cancel(self) -> None:
        raise NotImplementedError
