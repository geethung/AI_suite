from enum import Enum
from pydantic import BaseModel
from typing import List, Optional

class Department(str, Enum):
    HR = "HR"
    ADMIN = "Admin"
    SALES = "Sales"


class StartRequest(BaseModel):
    
    company_name: str
    department: str

class QuestionnaireResponse(BaseModel):
    
    question: str
    answer: str

class AnswerRequest(BaseModel):
    session_id: str
    


class DepartmentQuestions(BaseModel):
    department: Department
    responses: List[QuestionnaireResponse]

class SOPGenerationRequest(BaseModel):
    company_name: str
    questionnaire: DepartmentQuestions

class SOPResponse(BaseModel):
    sop: str
    department: str
    status: str = "success"
    word_count: Optional[int] = None
