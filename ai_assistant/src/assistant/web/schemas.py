"""Request/response models for the HTTP API."""

from __future__ import annotations

from pydantic import BaseModel, Field

SESSION_ID_PATTERN = r"^[A-Za-z0-9_-]{1,64}$"


class ChatRequest(BaseModel):
    session_id: str = Field(pattern=SESSION_ID_PATTERN)
    message: str = Field(min_length=1, max_length=20000)


class SessionSummary(BaseModel):
    id: str
    title: str
