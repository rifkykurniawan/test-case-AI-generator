from pydantic import BaseModel, Field


class TestCase(BaseModel):
    id: str = Field(
        ..., description="Unique identifier for the test case (e.g., TC-001)."
    )
    title: str = Field(..., description="A concise title describing the test scenario.")


class GenerateResponse(BaseModel):
    testCases: list[TestCase] = Field(..., serialization_alias="testCases")
