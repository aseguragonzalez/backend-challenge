from pydantic import BaseModel, Field
from typing import Any


class Error(BaseModel):
    code: str = Field(
        examples=["request_not_found"],
        title="Error code",
        description="Contains the related to the error.",
    )
    message: str = Field(
        examples=["The resource was not found"],
        title="Error message",
        description="Contains the error message related to the error.",
    )


class NotFoundError(Error):
    code: str = "request_not_found"
    message: str = "The resource was not found"


class InputError(BaseModel):
    path: str = Field(
        examples=["body.topic"],
        title="Field path which has been failed",
        description="Indicates the field path - from the root - where we found some validation error.",
    )
    code: str = Field(
        examples=["value_error.missing"],
        title="Error type",
        description="Contains one of the standard types related to validation rules",
    )
    message: str = Field(
        examples=["field required"],
        title="Error description",
        description="Provide more details about the error.",
    )


class BadRequestError(Error):
    code: str = "invalid_request"
    message: str = "One or more input errors was found"
    errors: list[InputError] = Field(
        title="Error list",
        description="List of errors produced after the model validation process.",
    )

    @classmethod
    def from_validation_errors(cls, validation_errors: list[dict[str, Any]]) -> "BadRequestError":
        errors = []
        for error in validation_errors:
            if len(error["loc"]) > 1:
                errors.append(InputError(path=f"body.{error['loc'][1]}", code=error["type"], message=error["msg"]))
        return cls(errors=errors)
