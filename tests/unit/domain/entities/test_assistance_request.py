import pytest
from src.domain.exceptions import UnavailableChangeOfStatusError
from src.domain.entities import AssistanceRequest
from src.domain.value_objects import Topic, Status


def test_new_assistance_request(faker):
    id = faker.uuid4()
    topic = faker.random_element(elements=[Topic.Sales, Topic.Pricing])
    description = faker.sentence()

    assistance_request = AssistanceRequest.new(id=id, topic=topic, description=description)

    assert assistance_request.id == id
    assert assistance_request.topic == topic
    assert assistance_request.description == description
    assert assistance_request.status == Status.Accepted


def test_stored_assistance_request(faker):
    id = faker.uuid4()
    topic = faker.random_element(elements=[Topic.Sales, Topic.Pricing])
    status = faker.random_element(elements=[Status.Accepted, Status.Succeeded, Status.Failed])
    description = faker.sentence()

    assistance_request = AssistanceRequest.stored(
        id=id, topic=topic, description=description, status=status
    )

    assert assistance_request.id == id
    assert assistance_request.topic == topic
    assert assistance_request.description == description
    assert assistance_request.status == status


def test_failed_assistance_request(faker):
    assistance_request = AssistanceRequest.new(
        id=faker.uuid4(),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence()
    )

    assistance_request.failed()

    assert assistance_request.status == Status.Failed


def test_failed_assistance_request_unavailable_change_of_status_error(faker):
    assistance_request = AssistanceRequest.stored(
        id=faker.uuid4(),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
        status=faker.random_element(elements=[Status.Failed, Status.Succeeded])
    )

    with pytest.raises(UnavailableChangeOfStatusError):
        assistance_request.failed()


def test_succeeded_assistance_request(faker):
    assistance_request = AssistanceRequest.new(
        id=faker.uuid4(),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence()
    )

    assistance_request.succeeded()

    assert assistance_request.status == Status.Succeeded


def test_succeeded_assistance_request_unavailable_change_of_status_error(faker):
    assistance_request = AssistanceRequest.stored(
        id=faker.uuid4(),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
        status=faker.random_element(elements=[Status.Failed, Status.Succeeded])
    )

    with pytest.raises(UnavailableChangeOfStatusError):
        assistance_request.succeeded()
