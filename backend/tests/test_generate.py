from httpx import AsyncClient


async def test_generate_success(client: AsyncClient):
    """Tests the /api/v1/generate endpoint with valid requirement text."""
    payload = {
        "requirement": "As a user, I want to log in with my email and password so I can access my dashboard."
    }
    response = await client.post("/api/v1/generate", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "testCases" in data

    assert len(data["testCases"]) > 0


async def test_generate_validation_error(client: AsyncClient):
    """Tests that the generate endpoint returns 422 validation error for too short requirements."""
    payload = {"requirement": "short"}
    response = await client.post("/api/v1/generate", json=payload)
    assert response.status_code == 422
