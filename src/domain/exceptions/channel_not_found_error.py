from src.domain.exceptions.domain_error import DomainError


class ChannelNotFoundError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            code="channel_not_found",
            message="No channel found for the given topic"
        )
