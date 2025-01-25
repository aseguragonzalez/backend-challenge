from logging import Logger
from smtplib import (
    SMTP,
    SMTPAuthenticationError,
    SMTPException,
    SMTPHeloError,
    SMTPNotSupportedError,
    SMTPRecipientsRefused,
    SMTPSenderRefused,
    SMTPServerDisconnected,
)

from src.domain.entities import AssistanceRequest
from src.domain.services import Channel, UnavailableChannelError
from src.infrastructure.adapters.services.email_settings import EmailSettings


class EmailChannel(Channel):
    def __init__(self, client: SMTP, settings: EmailSettings, logger: Logger) -> None:
        self._client = client
        self._settings = settings
        self._logger = logger

    def send(self, assistance_request: AssistanceRequest) -> None:
        try:
            self._client.connect(host=self._settings.server, port=self._settings.port)
        except ConnectionRefusedError as exc:
            self._logger.error(f"We can't connect with SMTP Server: {exc}")
            raise UnavailableChannelError()

        try:
            self._client.login(self._settings.username, self._settings.password)
        except (SMTPHeloError, SMTPAuthenticationError, SMTPNotSupportedError, SMTPException) as exc:
            self._logger.error(f"We can't login with SMTP Server: {exc}")
            raise UnavailableChannelError()

        try:
            self._client.sendmail(
                msg=assistance_request.description,
                from_addr=self._settings.from_email,
                to_addrs=self._settings.to_email,
            )
        except (
            SMTPHeloError,
            SMTPRecipientsRefused,
            SMTPSenderRefused,
            SMTPNotSupportedError,
            SMTPServerDisconnected,
        ) as exc:
            self._logger.error(f"We can't sendemail: {exc}")
            raise UnavailableChannelError()

        self._client.close()
