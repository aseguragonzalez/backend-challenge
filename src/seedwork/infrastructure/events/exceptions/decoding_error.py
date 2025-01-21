class DecodingError(Exception):
    def __init__(self) -> None:
        super().__init__("Event decoding fails")
