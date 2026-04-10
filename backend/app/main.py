import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.exceptions import (
    ChatServiceUnavailableError,
    GroqResponseFormatError,
    GroqTimeoutError,
    GroqUpstreamError,
)
from app.services.document_service import DocumentSearchService


logger = logging.getLogger(__name__)

SAMPLE_DOCUMENTS = [
    "office equipment policy",
    "office furniture policy",
    "office travel policy",
    "employee benefits and insurance",
    "workplace safety guidelines",
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    search_service = DocumentSearchService()
    search_service.add_documents(SAMPLE_DOCUMENTS)

    http_client = httpx.Client(timeout=30.0)

    app.state.search_service = search_service
    app.state.http_client = http_client

    try:
        yield
    finally:
        http_client.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Python Jarvis API",
        description="AI-powered document analysis and chat API",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    @app.exception_handler(ChatServiceUnavailableError)
    async def handle_chat_unavailable(_: Request, exc: ChatServiceUnavailableError):
        logger.warning("Chat service unavailable: %s", exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "Chat service is unavailable"},
        )

    @app.exception_handler(GroqTimeoutError)
    async def handle_groq_timeout(_: Request, exc: GroqTimeoutError):
        logger.warning("Groq timeout: %s", exc)
        return JSONResponse(
            status_code=504,
            content={"detail": "Groq request timed out"},
        )

    @app.exception_handler(GroqUpstreamError)
    async def handle_groq_upstream(_: Request, exc: GroqUpstreamError):
        logger.error("Groq upstream error: %s", exc)
        return JSONResponse(
            status_code=502,
            content={"detail": "Groq upstream error"},
        )

    @app.exception_handler(GroqResponseFormatError)
    async def handle_groq_response_format(_: Request, exc: GroqResponseFormatError):
        logger.error("Groq response format error: %s", exc)
        return JSONResponse(
            status_code=502,
            content={"detail": "Invalid Groq response"},
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(_: Request, exc: Exception):
        logger.exception("Unhandled application error: %s", exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    return app


app = create_app()
