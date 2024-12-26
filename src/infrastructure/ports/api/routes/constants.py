from typing import Any

from fastapi import status

from src.infrastructure.ports.api.models import BadRequestError, NotFoundError
from src.infrastructure.ports.api.routes.models import AssistanceRequest
from src.infrastructure.ports.api.routes.responses import AssistanceAccepted


requests_endpoint_definition: dict[str, Any] = {
    "prefix": "/api/assistances",
    "tags": ["Assistance requests"],
    "responses": {
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid input error",
            "model": BadRequestError,
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "The current request requires authentication."},
        status.HTTP_403_FORBIDDEN: {"description": "The current request requires authorization."},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "[Deprecated response code]",
            "model": None,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "An internal server error was produced."},
    },
}

requests_enpoint_post: dict[str, Any] = {
    "path": "",
    "name": "Create a new assistance request",
    "summary": "Create a new request",
    "description": "Allows creating a new assistance request by the bot.",
    "status_code": status.HTTP_202_ACCEPTED,
    "responses": {
        status.HTTP_202_ACCEPTED: {
            "description": "The assistance request has been created successfully.",
            "model": AssistanceAccepted,
        },
    },
}

requests_endpoint_get: dict[str, Any] = {
    "path": "/{assistance_id}",
    "name": "Get assistance request",
    "summary": "Retrieve request by ID",
    "description": "Allows retrieving the assistance request by the request ID.",
    "status_code": status.HTTP_200_OK,
    "responses": {
        status.HTTP_200_OK: {
            "description": "The request was founded.",
            "model": AssistanceRequest,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The resource requested has not been found.",
            "model": NotFoundError,
        },
    },
}
