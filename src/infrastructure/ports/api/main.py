from fastapi import FastAPI, Request, Depends
from fastapi.exceptions import RequestValidationError

from src.domain.exceptions import AssistanceRequestNotFoundError
from src.infrastructure.ports.api.models import BadRequestError
from src.infrastructure.ports.api.routes import endpoints
from src.infrastructure.ports.api.security import api_key
from src.infrastructure.ports.api.responses import BadRequestResponse, NotFoundResponse
from src.infrastructure.ports.api.constants import api_definition


app = FastAPI(**api_definition)

app.include_router(endpoints.router, dependencies=[Depends(api_key)])


@app.exception_handler(AssistanceRequestNotFoundError)
async def request_not_found_exception_handler(
    request: Request, exc: AssistanceRequestNotFoundError
) -> NotFoundResponse:
    return NotFoundResponse()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> BadRequestResponse:
    return BadRequestResponse(
        model=BadRequestError.from_validation_errors(validation_errors=exc.errors())
    )
