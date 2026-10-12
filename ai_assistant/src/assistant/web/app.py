"""FastAPI application factory."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from assistant.core.assistant import Assistant
from assistant.factory import build_assistant
from assistant.web.routes import router

STATIC_DIR = Path(__file__).parent / "static"


def create_app(assistant: Assistant | None = None) -> FastAPI:
    """Build the web app.

    Args:
        assistant: Optional pre-built Assistant (used by tests); otherwise built
            from environment settings.

    Raises:
        ConfigError: If required settings are missing.
    """
    app = FastAPI(title="AI Assistant", docs_url=None, redoc_url=None)
    app.state.assistant = assistant or build_assistant()
    app.include_router(router)

    @app.middleware("http")
    async def security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; style-src 'self'; script-src 'self'; "
            "img-src 'self' data:; frame-ancestors 'none'"
        )
        return response

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/", include_in_schema=False)
    def index() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    return app
