import os
from pathlib import Path
from fastapi import APIRouter, Depends, Response, HTTPException

from app.core.dependencies import get_excel_service
from app.schemas.request import ExportRequest, SaveMarkdownRequest
from app.services.excel_service import ExcelService

router = APIRouter(prefix="/api/v1")


@router.post(
    "/export",
    summary="Export Test Cases to Excel",
    description="Accepts generated JSON data and returns an Excel spreadsheet containing the test cases.",
)
async def export_to_excel(
    payload: ExportRequest,
    excel_service: ExcelService = Depends(get_excel_service),
) -> Response:
    """Generates and returns an Excel sheet from the payload."""
    excel_bytes = excel_service.export_to_bytes(
        requirement_input=payload.requirement, data=payload.generated
    )

    headers = {"Content-Disposition": 'attachment; filename="test_cases.xlsx"'}
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )


@router.post(
    "/export/markdown",
    summary="Save Test Cases as Markdown",
    description="Saves the test cases to a markdown file in the test-cases directory.",
)
async def export_to_markdown(payload: SaveMarkdownRequest):
    # Construct the path to the test-cases directory at the root of the project
    # backend/app/api/export.py -> backend is parent.parent.parent
    root_dir = Path(__file__).resolve().parent.parent.parent.parent
    test_cases_dir = root_dir / "test-cases"
    
    # Ensure directory exists
    test_cases_dir.mkdir(parents=True, exist_ok=True)
    
    # Sanitize filename
    safe_filename = "".join([c for c in payload.filename if c.isalpha() or c.isdigit() or c in (' ', '-', '_')]).rstrip()
    if not safe_filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
        
    file_path = test_cases_dir / f"{safe_filename}.md"
    
    # Format content
    content = f"# Test Cases: {safe_filename}\n\n"
    content += f"**Requirement:**\n> {payload.requirement}\n\n"
    content += "## Scenarios\n\n"
    content += "| ID | Scenario |\n"
    content += "|---|---|\n"
    
    for tc in payload.testCases:
        # handle if tc is a dict or a pydantic model just in case
        tc_id = tc.get("id", "") if isinstance(tc, dict) else tc.id
        tc_title = tc.get("title", "") if isinstance(tc, dict) else tc.title
        content += f"| {tc_id} | {tc_title} |\n"
        
    # Write to file
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write file: {str(e)}")
        
    return {"status": "success", "message": f"Saved to {file_path.name}"}
