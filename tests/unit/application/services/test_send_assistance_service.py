import pytest

from src.application.services import SendAssistanceService
from src.domain.entities import AssistanceRequest
from src.domain.value_objects import Topic


def test_execute_should_send_assistance_request(faker, assistances_repository, channels_service):
    assistance_request = AssistanceRequest.new(
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
    )
    assistances_repository.get.return_value = assistance_request
    channels_service.send_assistance_request.return_value = None
    service = SendAssistanceService(assistance_repository=assistances_repository, channels_service=channels_service)

    service.execute(id=assistance_request.id)

    assistances_repository.get.assert_called_once_with(id=assistance_request.id)
    assistances_repository.save.assert_called_once_with(assistance_request=assistance_request)
    channels_service.send_assistance_request.assert_called_once_with(assistance_request=assistance_request)


def test_execute_should_raise_error_when_execution_fails(faker, assistances_repository, channels_service):
    assistance_request = AssistanceRequest.new(
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
        description=faker.sentence(),
    )
    assistances_repository.get.return_value = assistance_request
    channels_service.send_assistance_request.side_effect = Exception()

    service = SendAssistanceService(assistance_repository=assistances_repository, channels_service=channels_service)

    with pytest.raises(Exception):
        service.execute(id=assistance_request.id)

    assistances_repository.get.assert_called_once_with(id=assistance_request.id)
    assistances_repository.save.assert_called_once_with(assistance_request=assistance_request)
    channels_service.send_assistance_request.assert_called_once_with(assistance_request=assistance_request)
