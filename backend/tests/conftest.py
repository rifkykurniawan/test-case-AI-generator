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
        "summary": {
            "feature": "User Authentication (Sign Up)",
            "description": "System requirement allowing users to create new accounts using email and password.",
        },
        "analysis": {
            "functionalRequirements": [
                "User must provide a valid email and a strong password.",
                "The system must check if the email already exists in the database.",
                "A confirmation email must be sent upon successful registration.",
            ],
            "validationRules": [
                "Email must follow standard format (RFC 5322).",
                "Password must be at least 8 characters long, contain one uppercase letter, one lowercase letter, and one digit.",
                "Email cannot be duplicate.",
            ],
        },
        "testCases": [
            {
                "id": "TC-001",
                "title": "Successful registration with valid details",
                "priority": "High",
                "type": "Positive",
                "precondition": "User is on the registration page and database has no record of the email.",
                "steps": [
                    "Enter valid email 'testuser@example.com'.",
                    "Enter strong password 'P@ssword123'.",
                    "Click 'Sign Up' button.",
                ],
                "expectedResult": "User account is created successfully and redirected to dashboard. Confirmation email sent.",
            }
        ],
        "edgeCases": [
            {
                "id": "EC-001",
                "title": "Registration fails with malformed email",
                "priority": "Medium",
                "type": "Negative",
                "precondition": "User is on the registration page.",
                "steps": [
                    "Enter invalid email 'invalid-email-format'.",
                    "Enter password 'P@ssword123'.",
                    "Click 'Sign Up' button.",
                ],
                "expectedResult": "Client-side validation error displayed: 'Please enter a valid email address'.",
            }
        ],
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

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as ac:
        yield ac
