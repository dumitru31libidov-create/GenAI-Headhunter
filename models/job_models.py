from typing import List, Optional, Literal
from pydantic import BaseModel, Field, model_validator

class SalaryRange(BaseModel):
    min: int
    max: int
    currency: str

class Location(BaseModel):
    city: str
    country: str
    is_remote: bool

class RedFlag(BaseModel):
    severity: Literal["low", "medium", "high"]
    category: Literal["toxicity", "vague", "unrealistic"]
    message: str

class JobAnalysis(BaseModel):
    role_title: str
    company_name: str
    seniority: Literal["Intern", "Junior", "Mid", "Senior", "Lead", "Architect"]
    match_score: int = Field(..., ge=0, le=100)

    tech_stack: List[str]
    salary: Optional[SalaryRange]
    location: Optional[Location]
    red_flags: List[RedFlag]

    summary: str
    is_remote: bool

    @model_validator(mode="after")
    def check_remote_vs_location(self):
        if self.is_remote and self.location and not self.location.is_remote:
            raise ValueError(
                "Inconsistență: jobul este marcat remote, dar locația indică cerințe de birou."
            )
        return self