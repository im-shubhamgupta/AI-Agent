"""Conversation memory. Implement MemoryStore to add persistence (SQLite, Redis, ...)."""

from __future__ import annotations

import threading
import uuid
from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import TypedDict


class Message(TypedDict):
    role: str
    content: str


class MemoryStore(ABC):
    """Storage interface for per-session chat history."""

    @abstractmethod
    def get(self, session_id: str) -> list[Message]:
        """Return a copy of the session's messages (empty list if unknown)."""

    @abstractmethod
    def append(self, session_id: str, message: Message) -> None:
        """Add a message to the session, creating the session if needed."""

    @abstractmethod
    def pop_last(self, session_id: str) -> None:
        """Remove the most recent message (used to roll back a failed turn)."""

    @abstractmethod
    def clear(self, session_id: str) -> bool:
        """Delete a session. Returns True if it existed."""

    @abstractmethod
    def list_sessions(self) -> list[dict]:
        """Return summaries (id, title) of sessions, newest first."""


class InMemoryStore(MemoryStore):
    """Thread-safe, process-local store with bounded history and session count."""

    def __init__(self, max_messages: int = 40, max_sessions: int = 200) -> None:
        self._max_messages = max_messages
        self._max_sessions = max_sessions
        self._sessions: OrderedDict[str, list[Message]] = OrderedDict()
        self._lock = threading.Lock()

    @staticmethod
    def new_session_id() -> str:
        return uuid.uuid4().hex

    def get(self, session_id: str) -> list[Message]:
        with self._lock:
            return [dict(m) for m in self._sessions.get(session_id, [])]  # type: ignore[misc]

    def append(self, session_id: str, message: Message) -> None:
        with self._lock:
            history = self._sessions.setdefault(session_id, [])
            history.append(message)
            if len(history) > self._max_messages:
                del history[: len(history) - self._max_messages]
            self._sessions.move_to_end(session_id)
            while len(self._sessions) > self._max_sessions:
                self._sessions.popitem(last=False)

    def pop_last(self, session_id: str) -> None:
        with self._lock:
            history = self._sessions.get(session_id)
            if history:
                history.pop()

    def clear(self, session_id: str) -> bool:
        with self._lock:
            return self._sessions.pop(session_id, None) is not None

    def list_sessions(self) -> list[dict]:
        with self._lock:
            out = []
            for sid, history in reversed(self._sessions.items()):
                first_user = next((m["content"] for m in history if m["role"] == "user"), "")
                out.append({"id": sid, "title": first_user[:40] or "New chat"})
            return out
