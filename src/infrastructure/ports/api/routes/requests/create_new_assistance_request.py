from pydantic import BaseModel, Field

from src.domain.value_objects import Topic


class CreateNewAssistanceRequest(BaseModel):
    topic: Topic = Field(
        title="Topic name", description="Topic related to the assistance request.", examples=["sales", "pricing"]
    )
    description: str = Field(
        title="Assistance request description",
        description="Assistance request detail provided by the requester bot.",
        min_length=1,
        max_length=300,
        examples=["We need some details about the product #REF00123654"],
    )
