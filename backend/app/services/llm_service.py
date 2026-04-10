import logging
from typing import Any

import httpx

from app.exceptions import (
    GroqResponseFormatError,
    GroqTimeoutError,
    GroqUpstreamError,
)
from app.utils.config import get_groq_api_key


logger = logging.getLogger(__name__)


def parse_groq_response(data: dict[str, Any]) -> str:
    """Parse Groq's OpenAI-compatible response format."""
    choices = data.get("choices")
    if isinstance(choices, list) and choices:
        first_choice = choices[0]
        message = first_choice.get("message")
        if isinstance(message, dict) and "content" in message:
            return message["content"]
    logger.error("Groq response did not contain choices[0].message.content")
    raise GroqResponseFormatError("Unexpected Groq response format")


def create_groq_response(
    messages: list[dict[str, str]],
    client: httpx.Client,
    model: str = "llama-3.1-8b-instant",
) -> str:
    """Call Groq API with the given messages and return the response."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {get_groq_api_key()}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 512,
        "temperature": 0.7,
    }

    try:
        logger.info("Sending chat request to Groq", extra={"model": model})
        response = client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = parse_groq_response(response.json())
        logger.info("Groq chat request completed", extra={"model": model})
        return result
    except httpx.TimeoutException:
        logger.warning("Groq request timed out", extra={"model": model})
        raise GroqTimeoutError("Groq request timed out") from None
    except httpx.HTTPStatusError as e:
        logger.error(
            "Groq upstream returned an error",
            extra={"model": model, "status_code": e.response.status_code},
        )
        raise GroqUpstreamError(e.response.status_code) from None


def chat_with_ai(user_message: str, client: httpx.Client) -> str:
    """Process user message and return AI response."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that can analyze documents and answer "
                "questions about them."
            ),
        },
        {"role": "user", "content": user_message},
    ]

    return create_groq_response(messages, client=client)
