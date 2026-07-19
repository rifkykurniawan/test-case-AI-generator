from fastapi import Depends

from app.ai.providers.base import AIProvider
from app.ai.providers.gemini_provider import GeminiProvider
from app.ai.providers.ollama_provider import OllamaProvider
from app.core.config import settings
from app.services.ai_service import AIService
from app.services.excel_service import ExcelService


def get_ai_provider() -> AIProvider:
    """Dependency to retrieve the configured AIProvider."""
    if settings.AI_PROVIDER == "ollama":
        return OllamaProvider(
            base_url=settings.OLLAMA_BASE_URL,
            model_name=settings.MODEL_NAME,
        )
    return GeminiProvider(
        api_key=settings.GEMINI_API_KEY,
        model_name=settings.MODEL_NAME,
    )



def get_ai_service(provider: AIProvider = Depends(get_ai_provider)) -> AIService:
    """Dependency to retrieve the AIService instance."""
    return AIService(provider=provider)


def get_excel_service() -> ExcelService:
    """Dependency to retrieve the ExcelService instance."""
    return ExcelService()
