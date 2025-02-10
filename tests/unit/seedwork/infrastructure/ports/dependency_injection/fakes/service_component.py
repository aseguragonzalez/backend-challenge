from abc import ABC, abstractmethod


class ServiceComponent(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError
