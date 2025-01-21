from httpx import Client, HTTPStatusError

from src.domain.entities import AssistanceRequest
from src.domain.services import Channel, UnavailableChannelError
from src.infrastructure.adapters.services.slack_settings import SlackSettings


class SlackChannel(Channel):
    def __init__(self, client: Client, settings: SlackSettings):
        self._client = client
        self._settings = settings

    def send(self, assistance_request: AssistanceRequest) -> None:
        response = self._client.post(
            url=f"{self._settings.url}/api/chat.postMessage?channel={self._settings.channel}",
            json={"text": assistance_request.description},
            headers={"X-API-KEY": self._settings.private_key},
        )
        try:
            response.raise_for_status()
        except HTTPStatusError:
            raise UnavailableChannelError()

        data = response.json()
        if not data["ok"]:
            raise UnavailableChannelError()
