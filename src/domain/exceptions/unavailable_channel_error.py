from src.domain.exceptions.domain_error import DomainError


class UnavailableChannelError(DomainError):
    def __init__(self) -> None:
        super().__init__(code="unavailable_channel", message="Channel is not available")
