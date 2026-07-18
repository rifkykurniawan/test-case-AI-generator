from httpx import AsyncClient


async def test_export_success(client: AsyncClient):
    """Tests that exporting test scenarios returns a spreadsheet response."""
    payload = {
        "requirement": "As a user, I want to sign up.",
        "generated": {
            "summary": {
                "feature": "Sign Up Feature",
                "description": "User Sign Up Requirement",
            },
            "analysis": {
                "functionalRequirements": ["Require email verification"],
                "validationRules": ["Valid email address only"],
            },
            "testCases": [
                {
                    "id": "TC-001",
                    "title": "Registration test",
                    "priority": "High",
                    "type": "Positive",
                    "precondition": "User on sign up page",
                    "steps": ["Step 1", "Step 2"],
                    "expectedResult": "Success",
                }
            ],
            "edgeCases": [
                {
                    "id": "EC-001",
                    "title": "Empty fields",
                    "priority": "Medium",
                    "type": "Negative",
                    "precondition": "User on sign up page",
                    "steps": ["Step 1"],
                    "expectedResult": "Error message",
                }
            ],
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
