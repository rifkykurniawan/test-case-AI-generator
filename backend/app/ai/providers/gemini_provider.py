import json

from loguru import logger

from app.ai.providers.base import AIProvider


class GeminiProvider(AIProvider):
    """Gemini AI Provider implementation.

    Phase 1: Returns mocked JSON corresponding to the required schema.
    """

    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Mock Gemini implementation for Phase 1.

        Returns static mock JSON structure containing realistic test scenarios.
        """
        logger.info(
            "GeminiProvider: generate called with model={}. Prompts length: system={}, user={}",
            self.model_name,
            len(system_prompt),
            len(user_prompt),
        )

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
                },
                {
                    "id": "TC-002",
                    "title": "Registration fails with existing email",
                    "priority": "High",
                    "type": "Negative",
                    "precondition": "User 'testuser@example.com' already exists in the system.",
                    "steps": [
                        "Enter email 'testuser@example.com'.",
                        "Enter password 'P@ssword123'.",
                        "Click 'Sign Up' button.",
                    ],
                    "expectedResult": "Error message displayed: 'Email already registered'. User account not created.",
                },
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
                },
                {
                    "id": "EC-002",
                    "title": "Registration with password at minimum length boundary",
                    "priority": "Medium",
                    "type": "Boundary",
                    "precondition": "User is on the registration page.",
                    "steps": [
                        "Enter valid email 'boundarytest@example.com'.",
                        "Enter password 'A1b2C3d4' (exactly 8 characters).",
                        "Click 'Sign Up' button.",
                    ],
                    "expectedResult": "User account is created successfully and confirmation email sent.",
                },
            ],
        }
        return json.dumps(mock_data)
