from uuid import UUID

import pytest

from src.application.services import GetAssistanceRequest, GetAssistanceService
from src.domain.entities import AssistanceRequest
from src.domain.value_objects import Status, Topic


@pytest.mark.unit
def test_execute_should_return_an_assistance_request(faker, assistances_repository):
    expected_assistance_request = AssistanceRequest.stored(
        id=UUID(faker.uuid4()),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
        status=faker.random_element(elements=[Status.Accepted, Status.Succeeded, Status.Failed]),
    )
    assistances_repository.get.return_value = expected_assistance_request
    request = GetAssistanceRequest(id=expected_assistance_request.id)
    service = GetAssistanceService(repository=assistances_repository)

    assistance_request = service.execute(request=request)

    assistances_repository.get.assert_called_once_with(id=expected_assistance_request.id)
    assert assistance_request.id == expected_assistance_request.id
    assert assistance_request.topic == expected_assistance_request.topic
    assert assistance_request.description == expected_assistance_request.description
    assert assistance_request.status == expected_assistance_request.status
