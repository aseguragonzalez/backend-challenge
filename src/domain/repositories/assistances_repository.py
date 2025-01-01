from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities import AssistanceRequest


class AssistancesRepository(ABC):
    @abstractmethod
    def save(self, assistance_request: AssistanceRequest) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get(self, id: UUID) -> AssistanceRequest:
        """
        Get a request by its id. If no request found, it raise a src.domain.exceptions.RequestNotFoundError.

        :param id: The request id.
        :return: The request found.
        """
        raise NotImplementedError()
