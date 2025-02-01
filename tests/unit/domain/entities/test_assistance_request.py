from uuid import UUID

import pytest

from src.domain.entities import AssistanceRequest
from src.domain.events import AssistanceRequestCreated, AssistanceRequestFailed, AssistanceRequestSucceeded
from src.domain.exceptions import UnavailableChangeOfStatusError
from src.domain.value_objects import Status, Topic


@pytest.mark.unit
def test_new_should_create_assistance_request_instance(faker):
    id = UUID(faker.uuid4())
    topic = faker.random_element(elements=[Topic.Sales, Topic.Pricing])
    description = faker.sentence()

    assistance_request = AssistanceRequest.new(id=id, topic=topic, description=description)

    assert assistance_request.id == id
    assert assistance_request.topic == topic
    assert assistance_request.description == description
    assert assistance_request.status == Status.Accepted
    assert len(assistance_request.events) == 1
    event = assistance_request.events[0]
    assert isinstance(event, AssistanceRequestCreated)
    assert event.type == "assistance_request_created"
    assert event.payload == {"id": str(id)}


@pytest.mark.unit
def test_stored_should_retrieve_an_assistance_request(faker):
    id = UUID(faker.uuid4())
    topic = faker.random_element(elements=[Topic.Sales, Topic.Pricing])
    status = faker.random_element(elements=[Status.Accepted, Status.Succeeded, Status.Failed])
    description = faker.sentence()

    assistance_request = AssistanceRequest.stored(id=id, topic=topic, description=description, status=status)

    assert assistance_request.id == id
    assert assistance_request.topic == topic
    assert assistance_request.description == description
    assert assistance_request.status == status
    assert len(assistance_request.events) == 0


@pytest.mark.unit
def test_fail_should_mark_as_failed(faker):
    assistance_request = AssistanceRequest.stored(
        id=UUID(faker.uuid4()),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
        status=Status.Accepted,
    )

    assistance_request.fail()

    assert assistance_request.status == Status.Failed
    assert len(assistance_request.events) == 1
    event = assistance_request.events[0]
    assert isinstance(event, AssistanceRequestFailed)
    assert event.type == "assistance_request_failed"
    assert event.payload == {"id": str(assistance_request.id)}


@pytest.mark.unit
def test_fail_should_raise_an_unavailable_change_of_status_error_when_status_is_invalid(faker):
    assistance_request = AssistanceRequest.stored(
        id=UUID(faker.uuid4()),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
        status=faker.random_element(elements=[Status.Failed, Status.Succeeded]),
    )

    with pytest.raises(UnavailableChangeOfStatusError):
        assistance_request.fail()


@pytest.mark.unit
def test_success_should_mark_as_succeeded(faker):
    assistance_request = AssistanceRequest.stored(
        id=UUID(faker.uuid4()),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
        status=Status.Accepted,
    )

    assistance_request.success()

    assert assistance_request.status == Status.Succeeded
    event = assistance_request.events[0]
    assert isinstance(event, AssistanceRequestSucceeded)
    assert event.type == "assistance_request_succeeded"
    assert event.payload == {"id": str(assistance_request.id)}


@pytest.mark.unit
def test_success_should_raise_an_unavailable_change_of_status_error_when_status_is_invalid(faker):
    assistance_request = AssistanceRequest.stored(
        id=UUID(faker.uuid4()),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
        status=faker.random_element(elements=[Status.Failed, Status.Succeeded]),
    )

    with pytest.raises(UnavailableChangeOfStatusError):
        assistance_request.success()


@pytest.mark.unit
def test_equals_should_be_true_when_compares_same_requests(faker):
    assistance_request = AssistanceRequest.new(
        id=UUID(faker.uuid4()),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
    )

    assert assistance_request == assistance_request


@pytest.mark.unit
def test_equals_should_be_true_when_compares_different_attributes_and_same_id(faker):
    id = UUID(faker.uuid4())
    assistance_request_1 = AssistanceRequest.new(
        id=id, topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]), description=faker.sentence()
    )

    assistance_request_2 = AssistanceRequest.new(
        id=id, topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]), description=faker.sentence()
    )

    assert assistance_request_1 == assistance_request_2
