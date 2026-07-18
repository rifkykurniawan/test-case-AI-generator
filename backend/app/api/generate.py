from fastapi import APIRouter, Depends

from app.core.dependencies import get_ai_service
from app.schemas.request import GenerateRequest
from app.schemas.response import GenerateResponse
from app.services.ai_service import AIService

router = APIRouter(prefix="/api/v1")


@router.post(
    "/generate",
    response_model=GenerateResponse,
    summary="Generate Test Cases",
    description="Analyzes requirements and generates structured test cases and edge cases.",
)
async def generate_test_cases(
    payload: GenerateRequest,
    ai_service: AIService = Depends(get_ai_service),
) -> GenerateResponse:
    """Invokes the AI generation service with the provided requirement payload."""
    return await ai_service.generate_scenarios(payload.requirement)
