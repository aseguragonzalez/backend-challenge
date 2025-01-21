import pytest
from pydantic_core._pydantic_core import ValidationError

from src.infrastructure.ports.api.routes.requests.create_new_assistance_request import CreateNewAssistanceRequest


def test_create_new_assistance_request_should_create_instance(faker):
    topic = faker.random_element(elements=["sales", "pricing"])
    description = faker.sentence()

    request = CreateNewAssistanceRequest(topic=topic, description=description)

    assert request.topic == topic
    assert request.description == description


@pytest.mark.parametrize(
    "topic, description",
    [
        (None, "Valid description"),
        ("", "Valid description"),
        ("sales", None),
        ("sales", ""),
    ],
)
def test_create_new_assistance_request_should_fails_when_is_invalid(topic, description):
    with pytest.raises(ValidationError):
        CreateNewAssistanceRequest(topic=topic, description=description)
