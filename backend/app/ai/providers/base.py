from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Abstract interface for AI Model Providers."""

    @abstractmethod
    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Asynchronously send prompts to the provider and return raw text response.

        Args:
            system_prompt: Guidelines and behavior instructions for the model.
            user_prompt: The requirements to be processed.

        Returns:
            str: Raw generated string (typically JSON format).
        """
        pass
