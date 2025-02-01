from logging import Logger
from smtplib import SMTP, SMTPHeloError, SMTPNotSupportedError, SMTPRecipientsRefused, SMTPSenderRefused
from unittest.mock import Mock

import pytest

from src.domain.entities import AssistanceRequest
from src.domain.services import UnavailableChannelError
from src.domain.value_objects import Topic
from src.infrastructure.adapters.services import EmailChannel


@pytest.mark.unit
def test_send_should_send_email(faker, email_settings):
    logger = Mock(Logger)
    client = Mock(SMTP)
    assistance_request = AssistanceRequest.new(
        topic=faker.random_element(elements=[Topic.Pricing, Topic.Sales]), description=faker.sentence()
    )
    channel = EmailChannel(client=client, settings=email_settings, logger=logger)

    channel.send(assistance_request=assistance_request)

    client.sendmail.assert_called_once_with(
        msg=assistance_request.description, from_addr=email_settings.from_email, to_addrs=email_settings.to_email
    )


@pytest.mark.unit
def test_send_should_raise_unavailable_channel_error_when_client_raises_exception(faker, email_settings):
    logger = Mock(Logger)
    client = Mock(SMTP)
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
    channel = EmailChannel(client=client, settings=email_settings, logger=logger)

    with pytest.raises(UnavailableChannelError):
        channel.send(assistance_request=assistance_request)
