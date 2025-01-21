from unittest.mock import Mock
from uuid import UUID

import pytest

from src.domain.entities import AssistanceRequest
from src.domain.services import Channel, ChannelNotFoundError, ChannelsService
from src.domain.value_objects import Status, Topic


def test_send_assistance_request_should_be_succeeded(faker):
    channel = Mock(Channel)
    channel.send.return_value = None
    channels_service = ChannelsService(
        channels_map={
            Topic.Sales: channel,
            Topic.Pricing: channel,
        }
    )
    assistance_request = AssistanceRequest.new(
        id=UUID(faker.uuid4()),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
    )

    channels_service.send_assistance_request(assistance_request)

    assert assistance_request.status == Status.Succeeded


def test_send_assistance_request_should_fail_when_channel_not_found_error(faker):
    assistance_request = AssistanceRequest.new(
        id=UUID(faker.uuid4()),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
    )
    channels_service = ChannelsService()

    with pytest.raises(ChannelNotFoundError):
        channels_service.send_assistance_request(assistance_request)
