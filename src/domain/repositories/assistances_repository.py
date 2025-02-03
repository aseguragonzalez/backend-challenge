from uuid import UUID

from src.domain.entities import AssistanceRequest
from src.seedwork.domain.repositories import Repository


class AssistancesRepository(Repository[AssistanceRequest, UUID]):
    pass
