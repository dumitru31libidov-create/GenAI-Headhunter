import os
from dotenv import load_dotenv
from groq import Groq
import instructor

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = instructor.from_groq(
    Groq(api_key=api_key),
    mode=instructor.Mode.TOOLS
)