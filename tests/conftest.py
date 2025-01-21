from unittest.mock import Mock

import pytest
from pika import BlockingConnection
from pymongo import MongoClient
from testcontainers.core.container import DockerContainer
from testcontainers.mongodb import MongoDbContainer
from testcontainers.rabbitmq import RabbitMqContainer

from src.infrastructure.adapters.services import EmailSettings
from src.seedwork.domain import UnitOfWork
from src.seedwork.infrastructure.queues.rabbit_mq import RabbitMqSettings


@pytest.fixture(scope="session")
def rabbitmq_container(request):
    rabbitmq = RabbitMqContainer("rabbitmq:3.9.10")
    rabbitmq.start()

    def remove_container():
        rabbitmq.stop()

    request.addfinalizer(remove_container)

    return rabbitmq


@pytest.fixture
def rabbitmq_connection(rabbitmq_container):
    with BlockingConnection(parameters=rabbitmq_container.get_connection_params()) as connection:
        yield connection


@pytest.fixture
def rabbit_mq_settings(rabbitmq_container):
    params = rabbitmq_container.get_connection_params()
    return RabbitMqSettings(
        host=params.host,
        port=params.port,
        username=params.credentials.username,
        password=params.credentials.password,
    )


@pytest.fixture(scope="session")
def mongodb_container(request):
    mongodb_container = MongoDbContainer("mongo:6.0")
    mongodb_container.start()

    def remove_container():
        mongodb_container.stop()

    request.addfinalizer(remove_container)
    return mongodb_container


@pytest.fixture
def mongo_client(mongodb_container):
    return MongoClient(mongodb_container.get_connection_url())


@pytest.fixture(scope="session")
def email_server_container(request):
    email_server_container = DockerContainer("rnwood/smtp4dev")
    email_server_container.with_name("smtp")
    email_server_container.with_exposed_ports(25, 25)
    email_server_container.with_env("ServerOptions__HostName", "smtp")
    email_server_container.with_env("RelayOptions__Login", "email_user")
    email_server_container.with_env("RelayOptions__Password", "email_secret")
    email_server_container.start()

    def remove_container():
        email_server_container.stop()

    request.addfinalizer(remove_container)
    return email_server_container


@pytest.fixture
def email_settings(email_server_container):
    return EmailSettings(
        from_email="source@email.com",
        to_email="source@email.com",
        server="smtp",
        port=25,
        username=email_server_container.env["RelayOptions__Login"],
        password=email_server_container.env["RelayOptions__Password"],
    )


@pytest.fixture
def unit_of_work_mock():
    # HACK: We have to mock uow beacuse MongoDb transactions are not available without a replica set
    unit_of_work = Mock(UnitOfWork)
    unit_of_work.__enter__ = Mock(return_value=unit_of_work)
    unit_of_work.__exit__ = Mock(return_value=None)
    unit_of_work.commit = Mock()
    unit_of_work.rollback = Mock()
    return unit_of_work
