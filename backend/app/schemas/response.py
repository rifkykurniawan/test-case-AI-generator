from pydantic import BaseModel, Field


class Summary(BaseModel):
    feature: str = Field(
        ..., description="The feature name derived from the requirement."
    )
    description: str = Field(
        ..., description="High-level description of the requirement."
    )


class RequirementAnalysis(BaseModel):
    functionalRequirements: list[str] = Field(
        ...,
        description="List of functional requirements extracted from the requirement text.",
    )
    validationRules: list[str] = Field(
        ..., description="List of business validation and constraint rules."
    )


class TestCase(BaseModel):
    id: str = Field(
        ..., description="Unique identifier for the test case (e.g., TC-001)."
    )
    title: str = Field(..., description="A concise title describing the test scenario.")
    priority: str = Field(..., description="Priority level (e.g., High, Medium, Low).")
    type: str = Field(
        ..., description="Test type (e.g., Positive, Negative, Boundary)."
    )
    precondition: str = Field(
        ..., description="Preconditions required before starting execution."
    )
    steps: list[str] = Field(
        ..., description="Sequential steps to execute the test case."
    )
    expectedResult: str = Field(
        ..., description="The expected outcome of the test case."
    )


class EdgeCase(BaseModel):
    id: str = Field(
        ..., description="Unique identifier for the edge case (e.g., EC-001)."
    )
    title: str = Field(
        ..., description="A concise title describing the edge case scenario."
    )
    priority: str = Field(..., description="Priority level (e.g., High, Medium, Low).")
    type: str = Field(..., description="Test type (e.g., Boundary, Negative).")
    precondition: str = Field(
        ..., description="Preconditions required before starting execution."
    )
    steps: list[str] = Field(
        ..., description="Sequential steps to execute the edge case."
    )
    expectedResult: str = Field(
        ..., description="The expected outcome of the edge case."
    )


class GenerateResponse(BaseModel):
    summary: Summary
    analysis: RequirementAnalysis
    testCases: list[TestCase] = Field(..., serialization_alias="testCases")
    edgeCases: list[EdgeCase] = Field(..., serialization_alias="edgeCases")
