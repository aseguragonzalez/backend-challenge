import os
from smtplib import SMTP

from httpx import Client

from src.infrastructure.adapters.services import EmailChannel, EmailSettings, SlackChannel, SlackSettings
from src.seedwork.infrastructure.ports.dependency_injection import ServiceProvider


def email_channel(sp: ServiceProvider) -> None:
    sp.register_singleton(EmailChannel, EmailChannel)


def email_settings(sp: ServiceProvider) -> None:
    email_settings = EmailSettings(
        from_email=os.getenv("EMAIL_CHANNEL_EMAIL_FROM"),
        to_email=os.getenv("EMAIL_CHANNEL_EMAIL_TO"),
        server=os.getenv("EMAIL_CHANNEL_SERVER"),
        port=int(os.getenv("EMAIL_CHANNEL_PORT")),
        username=os.getenv("EMAIL_CHANNEL_USERNAME"),
        password=os.getenv("EMAIL_CHANNEL_PASSWORD"),
    )
    sp.register_singleton(EmailSettings, lambda _: email_settings)


def smtp_client(sp: ServiceProvider) -> None:
    def _configure(sp: ServiceProvider):
        email_settings = sp.get(EmailSettings)
        return SMTP(host=email_settings.server, port=email_settings.port)

    sp.register_singleton(SMTP, _configure)


def slack_channel(sp: ServiceProvider) -> None:
    sp.register_singleton(SlackChannel, SlackChannel)


def slack_settings(sp: ServiceProvider) -> None:
    slack_settings = SlackSettings(
        channel=os.getenv("SLACK_CHANNEL_CHANNEL"),
        url=os.getenv("SLACK_CHANNEL_URL"),
        private_key=os.getenv("SLACK_CHANNEL_PRIVATE_KEY"),
    )
    sp.register_singleton(SlackSettings, lambda _: slack_settings)


def http_client(sp: ServiceProvider) -> None:
    sp.register_singleton(Client, lambda _: Client())
