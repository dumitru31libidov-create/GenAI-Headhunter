from utils.ai_client import client
from models.extraction_models import RawExtraction, StrategicAdvice

def run_counselor(extraction: RawExtraction) -> StrategicAdvice:
    return client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_model=StrategicAdvice,
        temperature=0.7,
        messages=[
            {
                "role": "system",
                "content": (
                    "1. Ești 'The Counselor' — un career coach senior.\n"
                    "2. Generezi insight-uri strategice STRICT în schema StrategicAdvice.\n"
                    "3. Nu inventezi date noi."
                    "4. Oferi recomandări clare, practice și orientate spre acțiune."
                    "5. Identifici riscuri, oportunități și puncte slabe."
                    "6. Returnezi STRICT schema CounselorAdvice."
                    "7. Nu incluzi text liber în afara structurii cerute."

                )
            },
            {
                "role": "user",
                "content": extraction.model_dump_json()
            }
        ]
    )