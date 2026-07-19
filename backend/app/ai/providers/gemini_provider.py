import json

from google import genai
from google.genai import types
from google.genai.errors import APIError
from loguru import logger

from app.ai.providers.base import AIProvider
from app.core.exceptions import AIProviderError
from app.schemas.response import GenerateResponse


class GeminiProvider(AIProvider):
    """Gemini AI Provider implementation using the official google-genai SDK."""

    def __init__(self, api_key: str, model_name: str):
        if not api_key:
            logger.warning("GEMINI_API_KEY is not set. Gemini API calls will fail.")
        self.api_key = api_key
        self.model_name = model_name or "gemini-2.0-flash"
        # Initialize GenAI Client
        self.client = genai.Client(api_key=self.api_key)

    def _is_valid_response(self, text: str) -> bool:
        """Checks if the output text is valid JSON and conforms to the response model."""
        try:
            # Strip potential markdown code fences
            cleaned = text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

            data = json.loads(cleaned)
            # Validate with Pydantic
            GenerateResponse.model_validate(data)
            return True
        except (json.JSONDecodeError, Exception) as e:
            logger.warning("Response validation check failed: {}", str(e))
            return False

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generates content using Gemini models, validating and retrying once if JSON is invalid."""
        logger.info(
            "GeminiProvider: Sending request to model={}...",
            self.model_name,
        )

        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            temperature=0.2,
        )

        try:
            # Call Gemini using async client
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=user_prompt,
                config=config,
            )
            raw_text = response.text or ""

            # Validate output
            if self._is_valid_response(raw_text):
                return raw_text

            # If validation fails, retry once with a stricter instruction
            logger.warning(
                "Initial response was invalid. Retrying with a stricter instruction..."
            )
            stricter_user_prompt = (
                f"{user_prompt}\n\n"
                "IMPORTANT: The previous attempt failed to generate valid JSON that complies with the schema. "
                "You must strictly return only valid JSON matching the schema outlined in the system instructions. "
                "Do not include any normal conversational text, explanation, or markdown formatting."
            )

            retry_response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=stricter_user_prompt,
                config=config,
            )
            raw_text_retry = retry_response.text or ""

            return raw_text_retry

        except APIError as e:
            logger.error("Gemini API Error: {}", str(e))
            raise AIProviderError(
                f"Gemini API returned an error: {e.message}", detail={"code": e.code}
            )
        except Exception as e:
            logger.error("Error during Gemini generation: {}", str(e))
            raise AIProviderError(f"Gemini generation failed: {str(e)}")
