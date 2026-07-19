import json

from loguru import logger

from app.ai.agents import load_agents_markdown
from app.ai.prompts import build_user_prompt
from app.ai.providers.base import AIProvider
from app.core.exceptions import AIProviderError
from app.schemas.response import GenerateResponse


class TestGenerator:
    """Orchestrates system/user prompts and invokes the configured AIProvider."""

    def __init__(self, provider: AIProvider):
        self.provider = provider

    async def generate_test_cases(self, requirement: str) -> GenerateResponse:
        """Loads agent guidelines, calls the AI provider, and parses the response.

        Args:
            requirement: The software requirement.

        Returns:
            GenerateResponse: Structured data containing summary, analysis, test/edge cases.

        Raises:
            AIProviderError: If generating or parsing results fails.
        """
        # 1. Load system prompt from agents.md
        system_prompt = load_agents_markdown()

        # 2. Build user prompt
        user_prompt = build_user_prompt(requirement)

        logger.info("System prompt length: {}", len(system_prompt))
        logger.info("User prompt length: {}", len(user_prompt))

        # 3. Call provider
        logger.info("Executing generation request via AI Provider...")
        try:
            raw_response = await self.provider.generate(system_prompt, user_prompt)
        except Exception as e:
            logger.error("AI Provider generation failed: {}", e)
            raise AIProviderError(f"AI generation failed: {e}")

        # 4. Parse JSON response
        try:
            # Strip potential markdown code fences in case the provider returned them
            cleaned_response = raw_response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()

            data = json.loads(cleaned_response)
            return GenerateResponse.model_validate(data)
        except json.JSONDecodeError as e:
            logger.error(
                "Failed to parse JSON response from AI provider. Raw response: {}",
                raw_response,
            )
            raise AIProviderError(
                "AI Provider returned invalid JSON", {"error": str(e)}
            )
        except Exception as e:
            logger.error("Response validation failed: {}", e)
            raise AIProviderError(
                "Generated response does not match the required schema",
                {"error": str(e)},
            )
