from pydantic import BaseModel, Field

from app.schemas.response import GenerateResponse


class GenerateRequest(BaseModel):
    requirement: str = Field(
        ...,
        min_length=10,
        description="The software requirement to analyze and generate test cases for.",
        examples=[
            "As a user, I want to be able to sign up using my email and password so that I can access the app."
        ],
    )


class ExportRequest(BaseModel):
    requirement: str = Field(
        ...,
        description="The original software requirement text.",
    )
    generated: GenerateResponse = Field(
        ...,
        description="The generated test case analysis JSON data.",
    )
