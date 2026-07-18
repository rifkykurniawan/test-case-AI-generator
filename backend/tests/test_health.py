from httpx import AsyncClient


async def test_health_check(client: AsyncClient):
    """Tests the health check endpoint returns 200 OK and healthy status."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
