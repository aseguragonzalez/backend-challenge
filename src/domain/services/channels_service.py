from src.domain.entities import AssistanceRequest
from src.domain.services.channel import Channel
from src.domain.services.channel_not_found_error import ChannelNotFoundError


class ChannelsService:
    def __init__(self, channels_map: dict[str, Channel] = {}) -> None:
        self._channels_map = channels_map

    def send_assistance_request(self, assistance_request: AssistanceRequest) -> None:
        try:
            channel = self._channels_map[assistance_request.topic.value]
        except KeyError:
            raise ChannelNotFoundError()

        return channel.send(assistance_request)
