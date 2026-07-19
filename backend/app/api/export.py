from fastapi import APIRouter, Depends, Response

from app.core.dependencies import get_excel_service
from app.schemas.request import ExportRequest
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
