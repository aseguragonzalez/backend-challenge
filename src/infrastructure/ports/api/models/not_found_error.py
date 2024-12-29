from src.infrastructure.ports.api.models.error import Error


class NotFoundError(Error):
    code: str = "request_not_found"
    message: str = "The resource was not found"
