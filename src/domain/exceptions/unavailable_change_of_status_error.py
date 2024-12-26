from src.domain.exceptions.domain_error import DomainError


class UnavailableChangeOfStatusError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            code="unavailable_change_of_status",
            message="The change of status is not available"
        )
