from pydantic import BaseModel, Field


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
