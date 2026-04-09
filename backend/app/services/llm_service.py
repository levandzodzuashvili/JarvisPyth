import httpx
from app.utils.config import GROQ_API_KEY


def parse_groq_response(data: dict) -> str:
    """Parse Groq's OpenAI-compatible response format."""
    choices = data.get("choices")
    if isinstance(choices, list) and choices:
        first_choice = choices[0]
        message = first_choice.get("message")
        if isinstance(message, dict) and "content" in message:
            return message["content"]
    raise ValueError(f"Unexpected Groq response format: {data}")


def create_groq_response(messages: list, model: str = "llama-3.1-8b-instant") -> str:
    """Call Groq API with the given messages and return the response."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 512,  # Reduced for faster response
        "temperature": 0.7,
    }

    try:
        with httpx.Client(timeout=30.0) as client:
            print(f"Making request to Groq API with model: {model}")
            response = client.post(url, json=payload, headers=headers)
            print(f"Response status: {response.status_code}")
            response.raise_for_status()
            result = parse_groq_response(response.json())
            print(f"Response parsed successfully, length: {len(result)}")
            return result
    except httpx.TimeoutException:
        print("Request timed out")
        raise Exception("Request to Groq API timed out")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code} - {e.response.text}")
        raise Exception(f"Groq API error: {e.response.status_code}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise Exception(f"Failed to get response from Groq: {str(e)}")


def chat_with_ai(user_message: str) -> str:
    """Process user message and return AI response."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant that can analyze documents and answer questions about them."},
        {"role": "user", "content": user_message}
    ]

    return create_groq_response(messages)
