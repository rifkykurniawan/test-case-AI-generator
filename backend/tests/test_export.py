from httpx import AsyncClient


async def test_export_success(client: AsyncClient):
    """Tests that exporting test scenarios returns a spreadsheet response."""
    payload = {
        "requirement": "As a user, I want to sign up.",
        "generated": {
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
        },
    }

    response = await client.post("/api/v1/export", json=payload)
    assert response.status_code == 200
    assert (
        response.headers["content-type"]
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert "content-disposition" in response.headers
    assert "attachment; filename=" in response.headers["content-disposition"]
    assert len(response.content) > 0
