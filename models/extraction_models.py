from typing import List, Optional
from pydantic import BaseModel
from .job_models import SalaryRange, Location

class RawExtraction(BaseModel):
    tech_stack: List[str]
    salary: Optional[SalaryRange]
    location: Optional[Location]
    requirements: List[str]
    benefits: List[str]

class StrategicAdvice(BaseModel):
    market_fit: str
    negotiation_tips: str
    interview_questions: List[str]

class ValidationResult(BaseModel):
    is_consistent: bool
    issues: List[str]