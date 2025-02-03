from collections.abc import Sequence
from typing import Any

from pydantic import Field

from src.infrastructure.ports.api.models.error import Error
from src.infrastructure.ports.api.models.input_error import InputError


class BadRequestError(Error):
    code: str = "invalid_request"
    message: str = "One or more input errors was found"
    errors: list[InputError] = Field(
        title="Error list",
        description="List of errors produced after the model validation process.",
    )

    @classmethod
    def from_validation_errors(cls, validation_errors: Sequence[Any]) -> "BadRequestError":
        errors = []
        for error in validation_errors:
            if len(error["loc"]) > 1:
                errors.append(InputError(path=f"body.{error['loc'][1]}", code=error["type"], message=error["msg"]))
        return cls(errors=errors)
