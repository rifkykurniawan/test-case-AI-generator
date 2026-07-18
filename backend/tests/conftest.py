import os
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app

# Ensure testing environment is set
os.environ["APP_ENV"] = "testing"
os.environ["GEMINI_API_KEY"] = "mock_key"


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient]:
    """Async client fixture for endpoint testing."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as ac:
        yield ac
