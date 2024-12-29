import pytest
from fastapi import status

from src.domain.value_objects import Status, Topic


@pytest.mark.integration
def test_retrieve_request_should_return_an_assistance_request(faker, client, db_collection):
    assistance_request_dto = {
        "_id": str(faker.uuid4()),
        "topic": faker.random_element(elements=[Topic.Sales, Topic.Pricing]).value,
        "description": faker.sentence(),
        "status": faker.random_element(elements=[Status.Failed, Status.Accepted, Status.Succeeded]).value,
    }
    db_collection.insert_one(assistance_request_dto)

    response = client.get(f"/api/assistances/{assistance_request_dto['_id']}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(assistance_request_dto["_id"])
    assert data["topic"] == assistance_request_dto["topic"]
    assert data["description"] == assistance_request_dto["description"]
    assert data["status"] == assistance_request_dto["status"]


@pytest.mark.integration
def test_retrieve_request_should_return_not_found_when_request_does_not_exist(faker, client):
    response = client.get(f"/api/assistances/{faker.uuid4()}")

    data = response.json()
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data["code"] == "request_not_found"
    assert data["message"] == "The resource was not found"
