import io

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from app.core.exceptions import ExportError
from app.schemas.response import GenerateResponse


class ExcelService:
    """Service to export generated test cases to an Excel workbook using openpyxl."""

    def __init__(self):
        # Color palette styles (sleek premium blue theme)
        self.header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
        self.header_fill = PatternFill(
            start_color="1F4E78", end_color="1F4E78", fill_type="solid"
        )

        self.title_font = Font(name="Segoe UI", size=14, bold=True, color="1F4E78")
        self.bold_font = Font(name="Segoe UI", size=10, bold=True)
        self.regular_font = Font(name="Segoe UI", size=10)

        self.border_thin = Border(
            left=Side(style="thin", color="D9D9D9"),
            right=Side(style="thin", color="D9D9D9"),
            top=Side(style="thin", color="D9D9D9"),
            bottom=Side(style="thin", color="D9D9D9"),
        )
        self.align_top_left = Alignment(
            horizontal="left", vertical="top", wrap_text=True
        )
        self.align_center = Alignment(horizontal="center", vertical="top")

    def _auto_fit_columns(self, ws, max_width_limit: int = 50):
        """Helper to fit column widths automatically with padding."""
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val = str(cell.value or "")
                # Handle multi-line cells length estimation
                lines = val.split("\n")
                for line in lines:
                    if len(line) > max_len:
                        max_len = len(line)
            # Give padding
            ws.column_dimensions[col_letter].width = min(
                max(max_len + 3, 12), max_width_limit
            )

    def export_to_bytes(self, requirement_input: str, data: GenerateResponse) -> bytes:
        """Generates an Excel workbook bytes representing the test generation output.

        Args:
            requirement_input: The raw user-supplied requirement description.
            data: The structured GenerateResponse object.

        Returns:
            bytes: Binary content of the Excel sheet.

        Raises:
            ExportError: If workbook generation fails.
        """
        try:
            wb = Workbook()

            # --- Sheet 1: Requirement ---
            ws_req = wb.active
            ws_req.title = "Requirement"
            ws_req.views.sheetView[0].showGridLines = True

            ws_req.cell(
                row=2, column=2, value="Original Software Requirement"
            ).font = self.title_font
            ws_req.cell(row=4, column=2, value="Feature:").font = self.bold_font
            ws_req.cell(
                row=4, column=3, value=data.summary.feature
            ).font = self.regular_font

            ws_req.cell(row=5, column=2, value="Description:").font = self.bold_font
            ws_req.cell(
                row=5, column=3, value=data.summary.description
            ).font = self.regular_font

            ws_req.cell(
                row=7, column=2, value="Full Requirement Text:"
            ).font = self.bold_font
            cell_req_body = ws_req.cell(row=8, column=2, value=requirement_input)
            cell_req_body.font = self.regular_font
            cell_req_body.alignment = Alignment(wrap_text=True, vertical="top")
            ws_req.merge_cells(start_row=8, start_column=2, end_row=15, end_column=6)
            ws_req.column_dimensions["B"].width = 25
            ws_req.column_dimensions["C"].width = 50

            # --- Sheet 2: Requirement Analysis ---
            ws_analysis = wb.create_sheet(title="Requirement Analysis")
            ws_analysis.views.sheetView[0].showGridLines = True

            ws_analysis.cell(
                row=2, column=2, value="Requirement Analysis & Business Rules"
            ).font = self.title_font

            # Functional Requirements Table
            ws_analysis.cell(
                row=4, column=2, value="Functional Requirements"
            ).font = self.bold_font
            ws_analysis.cell(row=5, column=2, value="ID").font = self.header_font
            ws_analysis.cell(row=5, column=2).fill = self.header_fill
            ws_analysis.cell(
                row=5, column=3, value="Requirement Description"
            ).font = self.header_font
            ws_analysis.cell(row=5, column=3).fill = self.header_fill

            row_idx = 6
            for idx, func_req in enumerate(data.analysis.functionalRequirements, 1):
                c1 = ws_analysis.cell(row=row_idx, column=2, value=f"FR-{idx:03d}")
                c2 = ws_analysis.cell(row=row_idx, column=3, value=func_req)
                c1.font = c2.font = self.regular_font
                c1.border = c2.border = self.border_thin
                c1.alignment = self.align_center
                c2.alignment = self.align_top_left
                row_idx += 1

            # Validation Rules Table
            row_idx += 2
            ws_analysis.cell(
                row=row_idx, column=2, value="Validation Rules & Constraints"
            ).font = self.bold_font
            row_idx += 1
            ws_analysis.cell(row=row_idx, column=2, value="ID").font = self.header_font
            ws_analysis.cell(row=row_idx, column=2).fill = self.header_fill
            ws_analysis.cell(
                row=row_idx, column=3, value="Validation Rule Description"
            ).font = self.header_font
            ws_analysis.cell(row=row_idx, column=3).fill = self.header_fill

            row_idx += 1
            for idx, val_rule in enumerate(data.analysis.validationRules, 1):
                c1 = ws_analysis.cell(row=row_idx, column=2, value=f"VR-{idx:03d}")
                c2 = ws_analysis.cell(row=row_idx, column=3, value=val_rule)
                c1.font = c2.font = self.regular_font
                c1.border = c2.border = self.border_thin
                c1.alignment = self.align_center
                c2.alignment = self.align_top_left
                row_idx += 1

            self._auto_fit_columns(ws_analysis, max_width_limit=60)

            # --- Sheet 3: Test Cases ---
            ws_tc = wb.create_sheet(title="Test Cases")
            ws_tc.views.sheetView[0].showGridLines = True

            ws_tc.cell(
                row=2, column=2, value="Functional Test Cases"
            ).font = self.title_font

            headers = [
                "ID",
                "Title",
                "Priority",
                "Type",
                "Precondition",
                "Steps",
                "Expected Result",
            ]
            for col_idx, header in enumerate(headers, 2):
                cell = ws_tc.cell(row=4, column=col_idx, value=header)
                cell.font = self.header_font
                cell.fill = self.header_fill
                cell.alignment = self.align_center

            row_idx = 5
            for tc in data.testCases:
                steps_str = "\n".join(
                    f"{i}. {step}" for i, step in enumerate(tc.steps, 1)
                )

                cells = [
                    ws_tc.cell(row=row_idx, column=2, value=tc.id),
                    ws_tc.cell(row=row_idx, column=3, value=tc.title),
                    ws_tc.cell(row=row_idx, column=4, value=tc.priority),
                    ws_tc.cell(row=row_idx, column=5, value=tc.type),
                    ws_tc.cell(row=row_idx, column=6, value=tc.precondition),
                    ws_tc.cell(row=row_idx, column=7, value=steps_str),
                    ws_tc.cell(row=row_idx, column=8, value=tc.expectedResult),
                ]

                for c in cells:
                    c.font = self.regular_font
                    c.border = self.border_thin
                    c.alignment = self.align_top_left

                # Center ID, Priority, and Type
                cells[0].alignment = self.align_center
                cells[2].alignment = self.align_center
                cells[3].alignment = self.align_center
                row_idx += 1

            self._auto_fit_columns(ws_tc, max_width_limit=45)

            # --- Sheet 4: Edge Cases ---
            ws_ec = wb.create_sheet(title="Edge Cases")
            ws_ec.views.sheetView[0].showGridLines = True

            ws_ec.cell(
                row=2, column=2, value="Edge Cases & Boundary Scenarios"
            ).font = self.title_font

            for col_idx, header in enumerate(headers, 2):
                cell = ws_ec.cell(row=4, column=col_idx, value=header)
                cell.font = self.header_font
                cell.fill = self.header_fill
                cell.alignment = self.align_center

            row_idx = 5
            for ec in data.edgeCases:
                steps_str = "\n".join(
                    f"{i}. {step}" for i, step in enumerate(ec.steps, 1)
                )

                cells = [
                    ws_ec.cell(row=row_idx, column=2, value=ec.id),
                    ws_ec.cell(row=row_idx, column=3, value=ec.title),
                    ws_ec.cell(row=row_idx, column=4, value=ec.priority),
                    ws_ec.cell(row=row_idx, column=5, value=ec.type),
                    ws_ec.cell(row=row_idx, column=6, value=ec.precondition),
                    ws_ec.cell(row=row_idx, column=7, value=steps_str),
                    ws_ec.cell(row=row_idx, column=8, value=ec.expectedResult),
                ]

                for c in cells:
                    c.font = self.regular_font
                    c.border = self.border_thin
                    c.alignment = self.align_top_left

                # Center ID, Priority, and Type
                cells[0].alignment = self.align_center
                cells[2].alignment = self.align_center
                cells[3].alignment = self.align_center
                row_idx += 1

            self._auto_fit_columns(ws_ec, max_width_limit=45)

            # Write to buffer
            file_stream = io.BytesIO()
            wb.save(file_stream)
            file_stream.seek(0)
            return file_stream.getvalue()

        except Exception as e:
            raise ExportError(f"Excel file generation failed: {e}")


stream = io.BytesIO()
