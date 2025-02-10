class UnrecoverableError(Exception):
    def __init__(self, message: str = "unknown") -> None:
        super().__init__(f"Unrecoverable error: {message}")
