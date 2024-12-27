import pytest
from fastapi import status


@pytest.mark.integration
def test_create_new_assistance_request(faker, headers, client):
    response = client.post(
        url="/api/assistances", json={"topic": "sales", "description": faker.sentence()}, headers=headers
    )

    data = response.json()
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert data["id"] is not None
    assert data["status"] == "accepted"
    assert data["link"] == f"/api/assistances/{data['id']}"


@pytest.mark.integration
def test_create_new_assistance_request_fails_when_topic_is_missing(faker, headers, client):
    response = client.post(
        url="/api/assistances",
        json={"description": faker.sentence()},
        headers=headers,
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


def test_create_new_assistance_request_fails_when_topic_is_invalid(faker, headers, client):
    response = client.post(
        url="/api/assistances",
        json={"topic": faker.uuid4(), "description": faker.sentence()},
        headers=headers,
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


def test_create_new_assistance_request_fails_when_description_is_missing(faker, headers, client):
    response = client.post(
        url="/api/assistances",
        json={"topic": faker.random_element(elements=["sales", "pricing"])},
        headers=headers,
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


def test_create_new_assistance_request_fails_when_description_is_too_long(faker, headers, client):
    response = client.post(
        url="/api/assistances",
        json={
            "topic": faker.random_element(elements=["sales", "pricing"]),
            "description": faker.pystr(min_chars=500, max_chars=500),
        },
        headers=headers,
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
