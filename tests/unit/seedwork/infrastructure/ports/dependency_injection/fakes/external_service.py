from abc import ABC, abstractmethod


class ExternalService(ABC):
    @abstractmethod
    def get_data(self) -> str:
        raise NotImplementedError
