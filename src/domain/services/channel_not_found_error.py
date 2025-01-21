class ChannelNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__("No channel found for the given topic")
