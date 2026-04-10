class ChatServiceUnavailableError(Exception):
    """Raised when chat is unavailable because local configuration is missing."""


class GroqTimeoutError(Exception):
    """Raised when the Groq API does not respond within the configured timeout."""


class GroqUpstreamError(Exception):
    """Raised when the Groq API returns a non-success HTTP response."""

    def __init__(self, status_code: int):
        super().__init__(f"Groq upstream returned HTTP {status_code}")
        self.status_code = status_code


class GroqResponseFormatError(Exception):
    """Raised when the Groq API payload does not match the expected schema."""
