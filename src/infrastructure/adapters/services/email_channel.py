from smtplib import (  # SMTPAuthenticationError,; SMTPException,
    SMTP,
    SMTPHeloError,
    SMTPNotSupportedError,
    SMTPRecipientsRefused,
    SMTPSenderRefused,
)

from src.domain.entities import AssistanceRequest
from src.domain.services import Channel, UnavailableChannelError
from src.infrastructure.adapters.services.email_settings import EmailSettings


class EmailChannel(Channel):
    def __init__(self, client: SMTP, settings: EmailSettings) -> None:
        self._client = client
        self._settings = settings

    def send(self, assistance_request: AssistanceRequest) -> None:
        # TODO: check if we need to connect, login and close the connection
        # self._client.connect()
        # try:
        #     self._client.login(self._settings.username, self._settings.password)
        # except (SMTPHeloError, SMTPAuthenticationError, SMTPNotSupportedError, SMTPException):
        #     raise UnavailableChannelError()
        # finally:
        #     self._client.close()
        try:
            self._client.sendmail(
                msg=assistance_request.description,
                from_addr=self._settings.from_email,
                to_addrs=self._settings.to_email,
            )
        except (SMTPHeloError, SMTPRecipientsRefused, SMTPSenderRefused, SMTPNotSupportedError):
            raise UnavailableChannelError()
        # finally:
        #     self._client.close()
