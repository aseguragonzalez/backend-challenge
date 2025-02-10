class RecoverableError(Exception):
    def __init__(self, message: str = "unknown") -> None:
        super().__init__(f"Recoverable error: {message}")
