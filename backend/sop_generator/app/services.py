# app/services.py

import google.generativeai as genai
from datetime import datetime
from typing import List
from .models import Department, SOPResponse, SOPGenerationRequest
from .config import settings
#from app.prompts import hr_prompt, admin_prompt, sales_prompt
from .prompts.hr_prompt import hr_prompt
from .prompts.admin_prompt import admin_prompt
from .prompts.sales_prompt import sales_prompt


# ✅ Configure Gemini model
genai.configure(api_key=settings.gemini_api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# ✅ Department-specific questions
DEPARTMENT_QUESTIONS = {
    Department.HR: [
        "What is the primary objective of your HR department?",
        "What compliance standards does your HR team need to follow?",
        "Describe your recruitment and onboarding process",
        "What employee evaluation processes exist?",
        "What policies do you have for workplace conflicts?"
    ],
    Department.ADMIN: [
        "What are your key administrative workflows?",
        "Describe your document management system",
        "What office policies should be standardized?",
        "What approval hierarchies exist?"
    ],
    Department.SALES: [
        "What sales methodology does your team use?",
        "Describe your CRM usage guidelines",
        "What are your sales pipeline stages?",
        "What discount approval processes exist?"
    ]
}

# ✅ Return the list of questions for a department
def get_department_questions(department: Department) -> List[str]:
    return DEPARTMENT_QUESTIONS.get(department, [])

# ✅ Generate SOP document using Gemini


def generate_sop_document(request: SOPGenerationRequest) -> SOPResponse:
    context = "\n".join(f"Q: {q.question}\nA: {q.answer}" for q in request.questionnaire.responses)
    date_today = datetime.now().strftime("%B %d, %Y")
    department = request.questionnaire.department.value

    if department == "HR":
        prompt = hr_prompt(request.company_name, date_today, context)
    elif department == "Admin":
        prompt = admin_prompt(request.company_name, date_today, context)
    elif department == "Sales":
        prompt = sales_prompt(request.company_name, date_today, context)
    else:
        raise ValueError("Unsupported department")

    response = model.generate_content(prompt)

    if not response or not hasattr(response, "text") or not response.text.strip():
        raise ValueError("❌ Gemini response was empty or invalid")

    return SOPResponse(
        sop=response.text,
        department=department,
        word_count=len(response.text.split())
    )
