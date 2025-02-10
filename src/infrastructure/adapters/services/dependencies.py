import os
from smtplib import SMTP

from httpx import Client

from src.infrastructure.adapters.services import EmailChannel, EmailSettings, SlackChannel, SlackSettings
from src.seedwork.infrastructure.ports.dependency_injection import ServiceProvider


def email_channel(sp: ServiceProvider) -> None:
    sp.register_singleton(EmailChannel, EmailChannel)


def email_settings(sp: ServiceProvider) -> None:
    email_settings = EmailSettings(
        from_email=os.environ["EMAIL_FROM"],
        to_email=os.environ["EMAIL_TO"],
        server=os.environ["EMAIL_HOST"],
        port=int(os.environ["EMAIL_PORT"]),
        username=os.environ["EMAIL_USERNAME"],
        password=os.environ["EMAIL_PASSWORD"],
    )
    sp.register_singleton(EmailSettings, lambda _: email_settings)


def smtp_client(sp: ServiceProvider) -> None:
    def configure(sp: ServiceProvider) -> SMTP:
        email_settings = sp.get(EmailSettings)
        return SMTP(host=email_settings.server, port=email_settings.port)

    sp.register_singleton(SMTP, configure)


def slack_channel(sp: ServiceProvider) -> None:
    sp.register_singleton(SlackChannel, SlackChannel)


def slack_settings(sp: ServiceProvider) -> None:
    slack_settings = SlackSettings(
        channel=os.environ["SLACK_CHANNEL_NAME"],
        url=os.environ["SLACK_SERVER_URL"],
        private_key=os.environ["SLACK_PRIVATE_KEY"],
    )
    sp.register_singleton(SlackSettings, lambda _: slack_settings)


def http_client(sp: ServiceProvider) -> None:
    sp.register_singleton(Client, lambda _: Client())
