from uuid import UUID

from src.application.services.create_assistance_service import CreateAssistanceService
from src.domain.entities import AssistanceRequest
from src.domain.value_objects import Topic


def test_create_assistant_request(faker, assistances_repository):
    assistance_request = AssistanceRequest.new(
        id=UUID(faker.uuid4()),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
    )
    service = CreateAssistanceService(repository=assistances_repository)

    service.execute(
        topic=assistance_request.topic, description=assistance_request.description, id=assistance_request.id
    )

    assistances_repository.save.assert_called_once_with(assistance_request=assistance_request)
