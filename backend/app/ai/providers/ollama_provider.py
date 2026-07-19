import json
import httpx
from loguru import logger

from app.ai.providers.base import AIProvider
from app.core.exceptions import AIProviderError
from app.schemas.response import GenerateResponse


class OllamaProvider(AIProvider):
    """Ollama AI Provider implementation using httpx.AsyncClient."""

    def __init__(self, base_url: str, model_name: str):
        self.base_url = base_url or "http://localhost:11434"
        self.model_name = model_name or "qwen3:4b"

    def _clean_text(self, text: str) -> str:
        """Robustly extracts and cleans JSON content from the response text."""
        cleaned = text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        # Extract JSON object if there's surrounding text (like thinking blocks)
        if not (cleaned.startswith("{") or cleaned.startswith("[")):
            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start != -1 and end != -1 and end > start:
                cleaned = cleaned[start : end + 1]
        return cleaned

    def _is_valid_response(self, text: str) -> bool:
        """Checks if the output text is valid JSON and conforms to the response model."""
        try:
            cleaned = self._clean_text(text)
            data = json.loads(cleaned)
            GenerateResponse.model_validate(data)
            return True
        except (json.JSONDecodeError, Exception) as e:
            logger.warning("Ollama response validation check failed: {}", str(e))
            return False

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generates content using local Ollama model, validating and retrying once if JSON is invalid."""
        logger.info(
            "OllamaProvider: Sending request to base_url={} model={}...",
            self.base_url,
            self.model_name,
        )

        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_ctx": 4096,
                "num_predict": 2048,
            },
        }

        try:
            async with httpx.AsyncClient(timeout=300.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                )
                response.raise_for_status()
                res_data = response.json()
                
                # In Ollama API/chat response, the message content is in response['message']['content']
                raw_text = res_data.get("message", {}).get("content", "")

            if self._is_valid_response(raw_text):
                return self._clean_text(raw_text)

            logger.warning(
                "Initial Ollama response was invalid. Retrying with a stricter instruction and removing format constraint..."
            )
            stricter_user_prompt = (
                f"{user_prompt}\n\n"
                "IMPORTANT: The previous attempt failed to generate valid JSON that complies with the schema. "
                "You must strictly return only valid JSON matching the schema outlined in the system instructions. "
                "Do not include any normal conversational text, explanation, or markdown formatting."
            )
            
            payload["messages"][1]["content"] = stricter_user_prompt
            # Remove format constraint on retry to support reasoning/thinking models
            if "format" in payload:
                del payload["format"]

            async with httpx.AsyncClient(timeout=300.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                )
                response.raise_for_status()
                res_data = response.json()
                raw_text_retry = res_data.get("message", {}).get("content", "")

            return self._clean_text(raw_text_retry)

        except httpx.HTTPStatusError as e:
            logger.error("Ollama HTTP Error: {}", str(e))
            raise AIProviderError(
                f"Ollama returned HTTP error: {e.response.status_code}",
                detail={"status_code": e.response.status_code}
            )
        except Exception as e:
            logger.error("Error during Ollama generation: {}", str(e))
            raise AIProviderError(f"Ollama generation failed: {str(e)}")

