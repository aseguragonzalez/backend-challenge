from unittest.mock import Mock

import pytest
from httpx import Client, HTTPStatusError, Response

from src.domain.entities import AssistanceRequest
from src.domain.services import UnavailableChannelError
from src.domain.value_objects import Topic
from src.infrastructure.adapters.services import SlackChannel, SlackSettings


@pytest.fixture
def settings(faker):
    return SlackSettings(
        url=faker.url(),
        private_key=faker.uuid4(),
        channel=faker.word(),
    )


def test_send_should_post_http_message(faker, settings):
    client = Mock(Client)
    assistance_request = AssistanceRequest.new(
        topic=faker.random_element(elements=[Topic.Pricing, Topic.Sales]), description=faker.sentence()
    )
    slack_channel = SlackChannel(client=client, settings=settings)
    response = Mock(Response)
    response.status_code = 200
    response.json.return_value = {"ok": True}
    client.post.return_value = response

    slack_channel.send(assistance_request=assistance_request)

    client.post.assert_called_once_with(
        url=f"{settings.url}/api/chat.postMessage?channel={settings.channel}",
        json={"text": assistance_request.description},
        headers={"Authorization": f"Bearer {settings.private_key}"},
    )


def test_send_should_raise_unavailable_channel_error_when_client_raises_exception(faker, settings):
    client = Mock(Client)
    assistance_request = AssistanceRequest.new(
        topic=faker.random_element(elements=[Topic.Pricing, Topic.Sales]), description=faker.sentence()
    )
    slack_channel = SlackChannel(client=client, settings=settings)
    response = Mock(Response)
    response.status_code = faker.random_int(min=400, max=599)
    response.json.return_value = {}
    response.raise_for_status.side_effect = HTTPStatusError(message=faker.sentence(), request=Mock(), response=response)
    client.post.return_value = response

    with pytest.raises(UnavailableChannelError):
        slack_channel.send(assistance_request=assistance_request)
