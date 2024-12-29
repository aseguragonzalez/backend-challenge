from uuid import UUID

from src.application.services import CreateAssistanceRequest, CreateAssistanceService
from src.domain.entities import AssistanceRequest
from src.domain.value_objects import Topic


def test_execute_should_be_ok(faker, assistances_repository):
    assistance_request = AssistanceRequest.new(
        id=UUID(faker.uuid4()),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
    )
    request = CreateAssistanceRequest(
        topic=assistance_request.topic, description=assistance_request.description, id=assistance_request.id
    )
    service = CreateAssistanceService(repository=assistances_repository)

    service.execute(request=request)

    assistances_repository.save.assert_called_once_with(entity=assistance_request)
