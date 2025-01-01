class UnavailableChannelError(Exception):
    def __init__(self) -> None:
        super().__init__("Channel is not available")
