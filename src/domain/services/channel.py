from abc import ABC, abstractmethod

from src.domain.entities import AssistanceRequest


class Channel(ABC):
    @abstractmethod
    def send(self, assistance_request: AssistanceRequest) -> None:
        """
        Send the acceptance request through the channel service

        It should raise an UnavailableChannelError if the channel is not available or has an error.
        """
        raise NotImplementedError()
