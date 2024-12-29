from unittest.mock import Mock
from uuid import UUID

import pytest

from src.domain.entities import AssistanceRequest
from src.domain.services import Channel, ChannelNotFoundError, ChannelsService
from src.domain.value_objects import Status, Topic


def test_send_assistance_request_should_be_succeeded(faker):
    sales_channel = Mock(Channel)
    sales_channel.send.return_value = None
    pricing_channel = Mock(Channel)
    pricing_channel.send.return_value = None
    channels_service = ChannelsService(
        channels_map={
            Topic.Sales.value: sales_channel,
            Topic.Pricing.value: pricing_channel,
        }
    )
    assistance_request = AssistanceRequest.new(
        id=UUID(faker.uuid4()),
        topic=Topic.Sales,
        description=faker.sentence(),
    )

    channels_service.send_assistance_request(assistance_request)

    assert assistance_request.status == Status.Succeeded
    sales_channel.send.assert_called_once_with(assistance_request)
    pricing_channel.send.assert_not_called()


def test_send_assistance_request_should_fail_when_channel_not_found_error(faker):
    assistance_request = AssistanceRequest.new(
        id=UUID(faker.uuid4()),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
    )
    channels_service = ChannelsService()

    with pytest.raises(ChannelNotFoundError):
        channels_service.send_assistance_request(assistance_request)
