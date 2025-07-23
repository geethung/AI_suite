from fastapi import APIRouter, HTTPException, Request, Response
from .models import Department, SOPGenerationRequest, SOPResponse
from .services import generate_sop_document, DEPARTMENT_QUESTIONS

from io import BytesIO                         # ✅ Fix for BytesIO
from reportlab.pdfgen import canvas           # ✅ PDF canvas
from reportlab.lib.pagesizes import A4        # ✅ Page size
from datetime import date                     # ✅ For date in PDF

router = APIRouter(
    prefix="/api/v1",
    tags=["SOP Generator"]
)

# ✅ Health check
@router.get("/", summary="Root health check")
def root():
    return {"message": "SOP Generator API is running"}

# ✅ List departments
@router.get("/departments", summary="List available departments")
async def list_departments():
    return {"departments": [dept.value for dept in Department]}

# ✅ Get questions per department
@router.get("/questions/{department}", summary="Get department questions")
async def get_questions(department: Department):
    return {"questions": DEPARTMENT_QUESTIONS.get(department, [])}

# ✅ Generate SOP text (used by React frontend)
@router.post("/generate", summary="Generate SOP text")
async def generate_sop(req: SOPGenerationRequest):
    try:
        #sop_text = generate_sop_document(req)
        sop_obj = generate_sop_document(req)  # This is an SOPResponse object
        sop_text = sop_obj.sop 
        return {
            "sop": sop_text,
            "department": req.questionnaire.department,
            "status": "success",
            "word_count": len(sop_text.split())
        }

    except Exception as e:
        print("❌ SOP generation error:", e)
        raise HTTPException(status_code=500, detail=f"Failed to generate SOP: {str(e)}")

# ✅ Generate PDF from SOP text
@router.post("/generate-pdf", summary="Generate PDF from SOP text")
async def generate_pdf_from_json(request: Request):
    try:
        body = await request.json()
        sop_text = body.get("sop_text")
        if not sop_text:
            raise ValueError("Missing 'sop_text'")
    except Exception as e:
        print("❌ Failed to parse request:", e)
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")

    try:
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        margin = 50
        line_height = 16

        # Title and date
        p.setFont("Helvetica-Bold", 16)
        p.drawString(margin, height - margin, "SOP Document")
        p.setFont("Helvetica", 10)
        p.drawString(margin, height - margin - 20, f"Generated on: {date.today()}")

        # Body text
        y = height - margin - 50
        p.setFont("Helvetica", 11)

        for line in sop_text.splitlines():
            if line.strip().startswith("**") and line.strip().endswith("**"):
                clean = line.strip().strip("*")
                p.setFont("Helvetica-Bold", 12)
            else:
                clean = line
                p.setFont("Helvetica", 11)

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

            y -= line_height / 2  # extra spacing

        p.save()
        buffer.seek(0)

        return Response(
            content=buffer.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=SOP_{date.today()}.pdf"}
        )
    except Exception as e:
        print("❌ PDF generation failed:", e)
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")
