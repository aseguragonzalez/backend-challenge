import pytest


@pytest.fixture(autouse=True)
def force_clean_db(clean_db):
    pass
