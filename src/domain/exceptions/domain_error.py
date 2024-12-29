class DomainError(Exception):
    def __init__(self, code: str, message: str):
        self._message = message
        self._code = code
        super().__init__(self.message)

    @property
    def code(self) -> str:
        return self._code

    @property
    def message(self) -> str:
        return self._message
