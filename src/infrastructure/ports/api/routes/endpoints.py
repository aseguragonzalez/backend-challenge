from uuid import UUID

from fastapi import APIRouter, Depends

from src.application.services import (
    CreateAssistanceRequest,
    CreateAssistanceService,
    GetAssistanceRequest,
    GetAssistanceService,
)
from src.infrastructure.ports.api.dependencies import create_assistance_service, get_assistance_service
from src.infrastructure.ports.api.routes.constants import (
    requests_endpoint_definition,
    requests_endpoint_get,
    requests_enpoint_post,
)
from src.infrastructure.ports.api.routes.models import AssistanceAccepted, AssistanceRequest
from src.infrastructure.ports.api.routes.requests import CreateNewAssistanceRequest
from src.infrastructure.ports.api.routes.responses import AssistanceRequestResponse, CreatedRequestResponse


router = APIRouter(**requests_endpoint_definition)


@router.post(**requests_enpoint_post)
def create_request(
    request: CreateNewAssistanceRequest, service: CreateAssistanceService = Depends(create_assistance_service)
) -> CreatedRequestResponse:
    request = CreateAssistanceRequest(topic=request.topic, description=request.description)
    service.execute(request=request)
    return CreatedRequestResponse(model=AssistanceAccepted.build(id=request.id))


@router.get(**requests_endpoint_get)
def retrieve_request(
    assistance_id: UUID, service: GetAssistanceService = Depends(get_assistance_service)
) -> AssistanceRequestResponse:
    request = GetAssistanceRequest(id=assistance_id)
    assistance_request = service.execute(request=request)
    assistance_request_model = AssistanceRequest.from_entity(assistance_request=assistance_request)
    return AssistanceRequestResponse(model=assistance_request_model)
