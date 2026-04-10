import os
from dotenv import load_dotenv
from app.exceptions import ChatServiceUnavailableError

load_dotenv()


def get_groq_api_key() -> str:
    """Return the configured Groq API key or raise a chat-service error."""
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ChatServiceUnavailableError("Missing GROQ_API_KEY environment variable")
    return groq_api_key
