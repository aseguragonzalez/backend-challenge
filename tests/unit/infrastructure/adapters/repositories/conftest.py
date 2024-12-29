import pytest


@pytest.fixture(autouse=True)
def clean(clean_db):
    # HACK: This fixture is used to force clean the database before and after each test
    yield
