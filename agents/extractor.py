from utils.ai_client import client
from models.extraction_models import RawExtraction

def run_extractor(text: str) -> RawExtraction:
    return client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_model=RawExtraction,
        temperature=0.0,
        messages=[
            {
                "role": "system",
                "content": (
               "Ești 'The Extractor' — un agent specializat în extragerea de fapte brute din text.\n"
               "Returnează STRICT schema RawExtraction, fără opinii sau interpretări.\n\n"
               "REGULI CRITICE:\n"
                         "1. Dacă lipsește ORICARE dintre câmpurile location.city sau location.country,\n"
                            "atunci setează location = null. NU returna un obiect parțial.\n"
                         "2. Dacă salariul nu are toate câmpurile (min, max, currency), setează salary = null.\n"
                         "3. Nu inventa informații lipsă.\n"
                         "4. Dacă un câmp nu există în text, setează-l la None sau listă goală.\n"
                         "5. Nu returna câmpuri care nu există în schema RawExtraction.\n"
                         "6. Returnează DOAR obiectul Pydantic, fără text liber.\n"


                )
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

