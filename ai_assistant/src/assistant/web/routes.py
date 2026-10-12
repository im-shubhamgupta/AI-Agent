"""HTTP routes. Streaming uses Server-Sent Events over a POST (consumed via fetch)."""

from __future__ import annotations

import json
import logging
import re
from collections.abc import Iterator

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse

from assistant.core.assistant import Assistant, InvalidMessageError
from assistant.core.llm_client import LLMError
from assistant.web.schemas import SESSION_ID_PATTERN, ChatRequest, SessionSummary

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api")
_SESSION_RE = re.compile(SESSION_ID_PATTERN)


def _bot(request: Request) -> Assistant:
    return request.app.state.assistant


def _event(payload: dict) -> str:
    return f"data: {json.dumps(payload)}\n\n"


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/sessions", response_model=list[SessionSummary])
def list_sessions(request: Request) -> list[dict]:
    return _bot(request).memory.list_sessions()


@router.get("/sessions/{session_id}/messages")
def get_messages(session_id: str, request: Request) -> list[dict]:
    if not _SESSION_RE.match(session_id):
        raise HTTPException(status_code=422, detail="Invalid session id")
    return _bot(request).memory.get(session_id)


@router.delete("/sessions/{session_id}", status_code=204)
def delete_session(session_id: str, request: Request) -> None:
    if not _SESSION_RE.match(session_id):
        raise HTTPException(status_code=422, detail="Invalid session id")
    _bot(request).memory.clear(session_id)


@router.post("/chat")
def chat(body: ChatRequest, request: Request) -> StreamingResponse:
    """Stream the assistant's reply as SSE events: token | error | done."""
    bot = _bot(request)

    def generate() -> Iterator[str]:
        try:
            for chunk in bot.chat_stream(body.session_id, body.message):
                yield _event({"token": chunk})
            yield _event({"done": True})
        except InvalidMessageError as exc:
            yield _event({"error": str(exc)})
        except LLMError:
            logger.exception("LLM request failed")
            yield _event({"error": "The AI model is unavailable or timed out. Please try again."})
        except Exception:
            logger.exception("Unexpected chat failure")
            yield _event({"error": "Something went wrong. Please try again."})

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
