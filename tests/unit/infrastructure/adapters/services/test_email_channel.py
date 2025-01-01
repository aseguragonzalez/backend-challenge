from smtplib import SMTP, SMTPHeloError, SMTPNotSupportedError, SMTPRecipientsRefused, SMTPSenderRefused
from unittest.mock import Mock

import pytest

from src.domain.entities import AssistanceRequest
from src.domain.services import UnavailableChannelError
from src.domain.value_objects import Topic
from src.infrastructure.adapters.services import EmailChannel


def test_send_should_send_email(faker):
    client = Mock(SMTP)
    from_address = faker.email()
    to_address = faker.email()
    assistance_request = AssistanceRequest.new(
        topic=faker.random_element(elements=[Topic.Pricing, Topic.Sales]), description=faker.sentence()
    )
    channel = EmailChannel(client=client, from_address=from_address, to_address=to_address)

    channel.send(assistance_request=assistance_request)

    client.sendmail.assert_called_once_with(
        msg=assistance_request.description, from_addr=from_address, to_addrs=to_address
    )


def test_send_should_raise_unavailable_channel_error_when_client_raises_exception(faker):
    client = Mock(SMTP)
    from_address = faker.email()
    to_address = faker.email()
    assistance_request = AssistanceRequest.new(
        topic=faker.random_element(elements=[Topic.Pricing, Topic.Sales]), description=faker.sentence()
    )
    client.sendmail.side_effect = faker.random_element(
        elements=[
            SMTPRecipientsRefused(recipients={}),
            SMTPSenderRefused(code=1, msg="", sender=""),
            SMTPHeloError(code=1, msg=""),
            SMTPNotSupportedError(),
        ]
    )
    channel = EmailChannel(client=client, from_address=from_address, to_address=to_address)

    with pytest.raises(UnavailableChannelError):
        channel.send(assistance_request=assistance_request)
