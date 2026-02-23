from utils.ai_client import client
from models.extraction_models import RawExtraction, ValidationResult

def run_validator(text: str, extraction: RawExtraction) -> ValidationResult:
    return client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_model=ValidationResult,
        temperature=0.0,
        messages=[
            {
                "role": "system",
                "content": (
                  "Ești „The Validator” — un agent specializat în verificarea consistenței dintre textul original și extragerea RawExtraction.\n"
                  "Reguli:\n"
                        "1. Nu modifici extragerea.\n"
                        "2. Nu generezi text liber în afara structurii ValidatorResponse.\n"
                        "3. Identifici doar probleme reale: lipsă, inconsistențe, contradicții.\n"
                        "4. Dacă totul este corect, setezi is_consistent = true și issues = [].\n"
                        "5. Dacă există probleme, setezi is_consistent = false și listezi clar fiecare problemă.\n"
                        "6. Nu inventa probleme care nu există în text.\n"
                        "7. Nu interpreta intenții — doar verifici fapte."

                )
            },
            {
                "role": "user",
                "content": (
                    f"TEXT:\n{text}\n\n"
                    f"EXTRACTION:\n{extraction.model_dump_json()}"
                )
            }
        ]
    )