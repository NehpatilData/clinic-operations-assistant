
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def is_gemini_configured():
    """Return True if a Gemini API key is configured."""
    return bool(GEMINI_API_KEY and GEMINI_API_KEY.strip())
