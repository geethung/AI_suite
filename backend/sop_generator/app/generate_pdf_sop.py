from fastapi import APIRouter, Response
from io import BytesIO
from pydantic import BaseModel
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch


from datetime import date

router = APIRouter(
    prefix="/api/v1",
    tags=["PDF"]
)

class PDFRequest(BaseModel):
    sop_text: str

@router.post("/generate-pdf", summary="Generate PDF from SOP JSON")
def generate_pdf_from_json(data: PDFRequest):
    print(f"Received SOP text (length: {len(data.sop_text)})")

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 50
    line_height = 16

    # Setup title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(margin, height - margin, "SOP Document")
    p.setFont("Helvetica", 10)
    p.drawString(margin, height - margin - 20, f"Generated on: {date.today()}")

    # Setup text cursor
    y = height - margin - 50
    p.setFont("Helvetica", 11)

    # Split lines and render safely
    for line in data.sop_text.splitlines():
        # Check for bold markdown (e.g., **Title**)
        if line.strip().startswith("**") and line.strip().endswith("**"):
            clean = line.strip().strip("*")
            p.setFont("Helvetica-Bold", 12)
        else:
            clean = line
            p.setFont("Helvetica", 11)

        # Handle line wrapping manually
        max_chars = 110
        while len(clean) > 0:
            if y < margin + line_height:
                p.showPage()
                p.setFont("Helvetica", 11)
                y = height - margin

            chunk = clean[:max_chars]
            p.drawString(margin, y, chunk)
            clean = clean[max_chars:]
            y -= line_height

        # Add space after each paragraph
        y -= line_height / 2

    p.save()
    buffer.seek(0)

    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=SOP_{date.today()}.pdf"}
    )
