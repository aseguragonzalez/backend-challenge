from unittest.mock import Mock

from fastapi import status

from src.domain.entities import AssistanceRequest
from src.domain.exceptions import AssistanceRequestNotFoundError
from src.domain.value_objects import Status, Topic


def test_retrieve_request_should_return_an_assistance_request(faker, headers, client, assistances_repository):
    request = AssistanceRequest.stored(
        id=faker.uuid4(),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
        status=faker.random_element(elements=[Status.Failed, Status.Accepted, Status.Succeeded]),
    )
    assistances_repository.get = Mock(return_value=request)

    response = client.get(f"/api/assistances/{request.id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(request.id)
    assert data["topic"] == request.topic.value
    assert data["description"] == request.description
    assert data["status"] == request.status.value


def test_retrieve_request_should_return_not_found_when_request_does_not_exist(
    faker, headers, client, assistances_repository
):
    assistances_repository.get = Mock(side_effect=AssistanceRequestNotFoundError())

    response = client.get(f"/api/assistances/{faker.uuid4()}", headers=headers)

    data = response.json()
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data["code"] == "request_not_found"
    assert data["message"] == "The resource was not found"