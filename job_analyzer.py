import os
import re
import requests
from bs4 import BeautifulSoup
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, model_validator
import instructor
from groq import Groq
from dotenv import load_dotenv

# ==============================================================================
# 1. SETUP & SECURITATE
# ==============================================================================
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = instructor.from_groq(Groq(api_key=api_key), mode=instructor.Mode.TOOLS)

# ==============================================================================
# 2. DATA MODELS (PYDANTIC SCHEMAS)
# ==============================================================================

class SalaryRange(BaseModel):
    min: int
    max: int
    currency: str

class Location(BaseModel):
     city: Optional[str] = None
     country: Optional[str] = None
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
    salary: Optional[SalaryRange] = None
    location: Optional[Location] = None
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

# ==============================================================================
# 3. SCRAPER
# ==============================================================================

def scrape_clean_job_text(url: str, max_chars: int = 3000) -> str:
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return f"Error: Status code {response.status_code}"

        soup = BeautifulSoup(response.content, 'html.parser')

        for junk in soup(["script", "style", "nav", "footer", "header", "aside", "iframe"]):
            junk.decompose()

        text = soup.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text)

        return text[:max_chars]

    except Exception as e:
        return f"Scraping Error: {str(e)}"

# ==============================================================================
# 4. AI SERVICE LAYER
# ==============================================================================

def analyze_job_with_ai(text: str) -> JobAnalysis:
    return client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_model=JobAnalysis,
        messages=[
            {
                "role": "system",
                "content": (
    "Ești un Recruiter Expert în IT specializat în analiză structurată de job descriptions.\n"
    "Returnează STRICT schema JobAnalysis, fără text liber.\n\n"

    "REGULI CRITICE:\n"
    "1. seniority trebuie să fie UNUL din: Intern, Junior, Mid, Senior, Lead, Architect.\n"
    "   Dacă nu poți determina seniority → setează 'Mid'.\n\n"

    "2. match_score trebuie să fie un număr între 0 și 100.\n"
    "   Dacă nu poți calcula scorul → setează 50.\n\n"

    "3. Dacă lipsește ORICARE dintre câmpurile location.city sau location.country,\n"
    "   atunci setează location = null. NU returna un obiect parțial.\n\n"

    "4. Dacă salariul nu are toate câmpurile (min, max, currency), setează salary = null.\n"
    "5. Nu inventa informații lipsă.\n"
    "6. Nu returna câmpuri care nu există în schema JobAnalysis.\n"
    "7. Returnează DOAR obiectul Pydantic, fără explicații suplimentare.\n"

                )
            },
            {
                "role": "user",
                "content": f"Analizează acest job description:\n\n{text}"
            },
        ],
        temperature=0.1,
    )
