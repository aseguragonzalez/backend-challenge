import json

from fastapi import status

from src.domain.entities import AssistanceRequest
from src.domain.value_objects import Status, Topic
from src.infrastructure.ports.api.routes.endpoints import retrieve_request


def test_get_assistance_request(faker, get_assistance_service):
    assistance_request = AssistanceRequest.stored(
        id=faker.uuid4(),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
        status=faker.random_element(elements=[Status.Accepted, Status.Failed, Status.Succeeded]),
    )
    get_assistance_service.execute.return_value = assistance_request

    response = retrieve_request(assistance_id=assistance_request.id, service=get_assistance_service)

    get_assistance_service.execute.assert_called_once_with(id=assistance_request.id)
    assert response.status_code == status.HTTP_200_OK
    body = json.loads(response.body)
    assert body["id"] == str(assistance_request.id)
    assert body["topic"] == assistance_request.topic.value
    assert body["description"] == assistance_request.description
    assert body["status"] == assistance_request.status.value
