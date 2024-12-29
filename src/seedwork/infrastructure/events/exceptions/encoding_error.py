class EncodingError(Exception):
    def __init__(self) -> None:
        super().__init__("Event encoding fails")
