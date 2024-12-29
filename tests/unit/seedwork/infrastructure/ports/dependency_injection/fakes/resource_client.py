class ResourceClient:
    def __init__(self) -> None:
        self._state: bool | None = None

    def __enter__(self) -> "ResourceClient":
        self._state = True
        return self

    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb: object) -> None:
        if self._state is None:
            raise ValueError("Resource is not open")
        self._state = False

    def is_open(self) -> bool:
        if self._state is None:
            raise ValueError("Resource is not open")
        return self._state

    def do_things(self) -> None:
        if self._state is None:
            raise ValueError("Resource is not open")
        if not self._state:
            raise ValueError("Resource is closed")
