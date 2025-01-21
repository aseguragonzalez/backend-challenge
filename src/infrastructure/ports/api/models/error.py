from pydantic import BaseModel, Field


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
