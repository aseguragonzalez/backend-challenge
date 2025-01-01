from smtplib import SMTP, SMTPHeloError, SMTPNotSupportedError, SMTPRecipientsRefused, SMTPSenderRefused

from src.domain.entities import AssistanceRequest
from src.domain.services import Channel, UnavailableChannelError


class EmailChannel(Channel):
    def __init__(self, client: SMTP, from_address: str, to_address: str):
        self._client = client
        self._from_address = from_address
        self._to_address = to_address

    def send(self, assistance_request: AssistanceRequest) -> None:
        try:
            self._client.sendmail(
                msg=assistance_request.description, from_addr=self._from_address, to_addrs=self._to_address
            )
        except (SMTPHeloError, SMTPRecipientsRefused, SMTPSenderRefused, SMTPNotSupportedError):
            raise UnavailableChannelError()
