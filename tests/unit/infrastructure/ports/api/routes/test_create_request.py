import json

from fastapi import status

from src.infrastructure.ports.api.routes.endpoints import create_request
from src.infrastructure.ports.api.routes.requests import CreateNewAssistanceRequest


def test_create_request_should_return_an_created_request_response(faker, create_assistance_service):
    request = CreateNewAssistanceRequest(
        topic=faker.random_element(elements=("sales", "pricing")), description=faker.sentence()
    )

    response = create_request(request=request, service=create_assistance_service)

    create_assistance_service.execute.assert_called_once()
    assert response.status_code == status.HTTP_202_ACCEPTED
    body = json.loads(response.body)
    assert "id" in body
    assert body["status"] == "accepted"
    assert body["link"] == f"/api/assistances/{body['id']}"
