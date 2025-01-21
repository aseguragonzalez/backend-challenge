import os

import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from testcontainers.mongodb import MongoDbContainer

from src.infrastructure.ports.api.main import app


API_KEY = "1234567"
DATABASE_NAME = "integration_test_db"


@pytest.fixture
def headers():
    return {"X-API-Key": API_KEY}


@pytest.fixture(scope="session", autouse=True)
def setup_api_db(request):
    mongodb = MongoDbContainer("mongo:6.0")
    mongodb.start()

    def remove_container():
        mongodb.stop()

    request.addfinalizer(remove_container)
    os.environ["DATABASE_URL"] = mongodb.get_connection_url()
    os.environ["API_KEYS"] = API_KEY
    os.environ["DATABASE_NAME"] = DATABASE_NAME


@pytest.fixture(scope="function", autouse=True)
def setup_api_data():
    yield
    mongo_client = MongoClient(os.environ["DATABASE_URL"])
    mongo_client.drop_database(DATABASE_NAME)


@pytest.fixture()
def db_collection():
    mongo_client = MongoClient(os.environ["DATABASE_URL"])
    return mongo_client[DATABASE_NAME]["assistances"]


@pytest.fixture
def client():
    return TestClient(app, headers={"X-API-Key": API_KEY})
