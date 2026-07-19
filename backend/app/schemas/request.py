from pydantic import BaseModel, Field

from app.schemas.response import GenerateResponse


class GenerateRequest(BaseModel):
    requirement: str = Field(
        ...,
        min_length=10,
        description="The software requirement to analyze and generate test cases for.",
        examples=[
            "I have login feature, login with username and password. Create test cases"
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


class SaveMarkdownRequest(BaseModel):
    filename: str = Field(
        ...,
        description="The desired filename without extension, e.g. 'login_tests'",
    )
    requirement: str = Field(
        ...,
        description="The original software requirement text.",
    )
    testCases: list = Field(
        ...,
        description="The list of test cases.",
    )
