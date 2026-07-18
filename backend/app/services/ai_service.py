import time

from loguru import logger

from app.ai.generator import TestGenerator
from app.ai.providers.base import AIProvider
from app.schemas.response import GenerateResponse


class AIService:
    """Service handling high-level AI generation logic."""

    def __init__(self, provider: AIProvider):
        self.generator = TestGenerator(provider)

    async def generate_scenarios(self, requirement: str) -> GenerateResponse:
        """Generates test cases and edge cases, tracking execution time.

        Args:
            requirement: The requirement text.

        Returns:
            GenerateResponse: Structured output.
        """
        start_time = time.perf_counter()
        logger.info("Starting AI test case generation service...")

        response = await self.generator.generate_test_cases(requirement)

        execution_time = time.perf_counter() - start_time
        logger.info("AI execution completed in {:.4f} seconds", execution_time)
        return response
