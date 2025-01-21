import pytest
from fastapi import status


@pytest.mark.integration
def test_create_new_assistance_request_should_return_an_accepted_assistance(faker, client):
    response = client.post(url="/api/assistances", json={"topic": "sales", "description": faker.sentence()})

    data = response.json()
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert data["id"] is not None
    assert data["status"] == "accepted"
    assert data["link"] == f"/api/assistances/{data['id']}"


@pytest.mark.integration
def test_create_new_assistance_request_should_fail_when_topic_is_missing(faker, client):
    response = client.post(
        url="/api/assistances",
        json={"description": faker.sentence()},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "code": "invalid_request",
        "message": "One or more input errors was found",
        "errors": [
            {
                "path": "body.topic",
                "code": "missing",
                "message": "Field required",
            }
        ],
    }


@pytest.mark.integration
def test_create_new_assistance_request_should_fail_when_topic_is_invalid(faker, client):
    response = client.post(
        url="/api/assistances",
        json={"topic": faker.uuid4(), "description": faker.sentence()},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "code": "invalid_request",
        "message": "One or more input errors was found",
        "errors": [
            {
                "path": "body.topic",
                "code": "enum",
                "message": "Input should be 'sales' or 'pricing'",
            }
        ],
    }


@pytest.mark.integration
def test_create_new_assistance_request_should_fail_when_description_is_missing(faker, client):
    response = client.post(
        url="/api/assistances",
        json={"topic": faker.random_element(elements=["sales", "pricing"])},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "code": "invalid_request",
        "message": "One or more input errors was found",
        "errors": [
            {
                "path": "body.description",
                "code": "missing",
                "message": "Field required",
            }
        ],
    }


@pytest.mark.integration
def test_create_new_assistance_request_should_fail_when_description_is_too_long(faker, client):
    response = client.post(
        url="/api/assistances",
        json={
            "topic": faker.random_element(elements=["sales", "pricing"]),
            "description": faker.pystr(min_chars=500, max_chars=500),
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "code": "invalid_request",
        "message": "One or more input errors was found",
        "errors": [
            {
                "path": "body.description",
                "code": "string_too_long",
                "message": "String should have at most 300 characters",
            }
        ],
    }
