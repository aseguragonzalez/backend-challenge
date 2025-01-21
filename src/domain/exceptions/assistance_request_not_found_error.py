from src.domain.exceptions.domain_error import DomainError


class AssistanceRequestNotFoundError(DomainError):
    def __init__(self) -> None:
        super().__init__(code="request_not_found", message="The request was not found")
