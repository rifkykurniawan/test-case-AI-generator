import json
import os
from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient

# Ensure testing environment is set
os.environ["APP_ENV"] = "testing"
os.environ["GEMINI_API_KEY"] = "mock_key"


@pytest.fixture(autouse=True)
def mock_gemini_client(monkeypatch):
    """Automatically mock the google-genai Client for all tests."""
    mock_client = MagicMock()
    mock_aio = MagicMock()
    mock_models = MagicMock()

    # AsyncMock for generate_content
    mock_generate = AsyncMock()

    mock_data = {
        "testCases": [
            {
                "id": "TC-001",
                "title": "Valid login with correct username and password"
            },
            {
                "id": "TC-002",
                "title": "Login with incorrect password"
            }
        ]
    }

    mock_response = MagicMock()
    mock_response.text = json.dumps(mock_data)
    mock_generate.return_value = mock_response

    mock_models.generate_content = mock_generate
    mock_aio.models = mock_models
    mock_client.aio = mock_aio

    # Patch the google.genai.Client class constructor to return our mock_client
    monkeypatch.setattr("google.genai.Client", lambda *args, **kwargs: mock_client)

    return mock_generate


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient]:
    """Async client fixture for endpoint testing."""
    from app.main import app
    from app.core.dependencies import get_ai_provider
    from app.ai.providers.base import AIProvider

    class MockProvider(AIProvider):
        async def generate(self, system_prompt: str, user_prompt: str) -> str:
            mock_data = {
                "testCases": [
                    {
                        "id": "TC-001",
                        "title": "Valid login with correct username and password"
                    },
                    {
                        "id": "TC-002",
                        "title": "Login with incorrect password"
                    }
                ]
            }
            return json.dumps(mock_data)

    app.dependency_overrides[get_ai_provider] = lambda: MockProvider()

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()

