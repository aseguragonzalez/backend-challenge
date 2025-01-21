from unittest.mock import Mock

import pytest

from src.application.services import FailAssistanceService
from src.domain.entities import AssistanceRequest


def test_execute_should_set_assistance_request_as_failed(faker, assistances_repository):
    id = faker.uuid4()
    assistance_request = Mock(AssistanceRequest)
    assistance_request.fail.return_value = None
    assistances_repository.get.return_value = assistance_request
    service = FailAssistanceService(assistance_repository=assistances_repository)

    service.execute(id=id)

    assistance_request.fail.assert_called_once_with()
    assistances_repository.get.assert_called_once_with(id=id)
    assistances_repository.save.assert_called_once_with(assistance_request=assistance_request)


def test_execute_should_raise_error_when_execution_fails(faker, assistances_repository, channels_service):
    id = faker.uuid4()
    assistance_request = Mock(AssistanceRequest)
    assistance_request.fail.side_effect = Exception()
    assistances_repository.get.return_value = assistance_request
    service = FailAssistanceService(assistance_repository=assistances_repository)

    with pytest.raises(Exception):
        service.execute(id=id)

    assistance_request.fail.assert_called_once_with()
    assistances_repository.get.assert_called_once_with(id=id)
    assistances_repository.save.assert_not_called()
