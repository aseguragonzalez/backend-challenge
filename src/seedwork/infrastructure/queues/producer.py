from abc import ABC, abstractmethod


class Producer(ABC):
    @abstractmethod
    def __enter__(self) -> "Producer":
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb: object) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_message(self, body: bytes) -> None:
        raise NotImplementedError
