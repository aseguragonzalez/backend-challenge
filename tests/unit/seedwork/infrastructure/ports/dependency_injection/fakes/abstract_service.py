from abc import ABC, abstractmethod


class AbstractService(ABC):
    @abstractmethod
    def id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def hello_world(self) -> None:
        raise NotImplementedError
