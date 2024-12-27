import pytest

from src.domain.entities import AssistanceRequest
from src.domain.exceptions import UnavailableChangeOfStatusError
from src.domain.value_objects import Status, Topic


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

    assistance_request = AssistanceRequest.stored(id=id, topic=topic, description=description, status=status)

    assert assistance_request.id == id
    assert assistance_request.topic == topic
    assert assistance_request.description == description
    assert assistance_request.status == status


def test_fail_assistance_request(faker):
    assistance_request = AssistanceRequest.new(
        id=faker.uuid4(),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
    )

    assistance_request.fail()

    assert assistance_request.status == Status.Failed


def test_fail_assistance_request_unavailable_change_of_status_error(faker):
    assistance_request = AssistanceRequest.stored(
        id=faker.uuid4(),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
        status=faker.random_element(elements=[Status.Failed, Status.Succeeded]),
    )

    with pytest.raises(UnavailableChangeOfStatusError):
        assistance_request.fail()


def test_success_assistance_request(faker):
    assistance_request = AssistanceRequest.new(
        id=faker.uuid4(),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
    )

    assistance_request.success()

    assert assistance_request.status == Status.Succeeded


def test_success_assistance_request_unavailable_change_of_status_error(faker):
    assistance_request = AssistanceRequest.stored(
        id=faker.uuid4(),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
        status=faker.random_element(elements=[Status.Failed, Status.Succeeded]),
    )

    with pytest.raises(UnavailableChangeOfStatusError):
        assistance_request.success()


def test_equals_assistance_request_same_request(faker):
    assistance_request = AssistanceRequest.new(
        id=faker.uuid4(),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence()
    )

    assert assistance_request == assistance_request


def test_equals_assistance_request_different_attributes_same_id(faker):
    id = faker.uuid4()
    assistance_request_1 = AssistanceRequest.new(
        id=id,
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence()
    )

    assistance_request_2 = AssistanceRequest.new(
        id=id,
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence()
    )

    assert assistance_request_1 == assistance_request_2
