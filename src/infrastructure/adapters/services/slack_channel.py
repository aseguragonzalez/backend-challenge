from httpx import Client, HTTPStatusError

from src.domain.entities import AssistanceRequest
from src.domain.services import Channel, UnavailableChannelError


class SlackChannel(Channel):
    def __init__(self, client: Client, channel: str, url: str, private_key: str):
        self._channel = channel
        self._client = client
        self._url = url
        self._private_key = private_key

    def send(self, assistance_request: AssistanceRequest) -> None:
        response = self._client.post(
            url=f"{self._url}/api/chat.postMessage?channel={self._channel}",
            json={"text": assistance_request.description},
            headers={"X-API-KEY": self._private_key},
        )
        try:
            response.raise_for_status()
        except HTTPStatusError:
            raise UnavailableChannelError()

        data = response.json()
        if not data["ok"]:
            raise UnavailableChannelError()
