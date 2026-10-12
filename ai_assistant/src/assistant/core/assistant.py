"""Interface-agnostic assistant: shared by the CLI and the web app."""

from __future__ import annotations

from collections.abc import Iterator

from assistant.config import Settings
from assistant.core.llm_client import LLMClient, LLMError
from assistant.core.memory import MemoryStore


class InvalidMessageError(ValueError):
    """Raised when a user message is empty or too long."""


class Assistant:
    """Chat orchestration with memory. Contains no I/O."""

    def __init__(self, settings: Settings, llm: LLMClient, memory: MemoryStore) -> None:
        self._settings = settings
        self._llm = llm
        self._memory = memory

    @property
    def memory(self) -> MemoryStore:
        return self._memory

    def _validate(self, text: str) -> str:
        text = (text or "").strip()
        if not text:
            raise InvalidMessageError("Message cannot be empty")
        if len(text) > self._settings.max_message_chars:
            raise InvalidMessageError(
                f"Message exceeds {self._settings.max_message_chars} characters"
            )
        return text

    def _build_messages(self, session_id: str) -> list[dict]:
        system = {"role": "system", "content": self._settings.system_prompt}
        return [system, *self._memory.get(session_id)]

    def chat(self, session_id: str, text: str) -> str:
        """Send a message and return the full reply.

        Raises:
            InvalidMessageError: If the message is empty or too long.
            LLMError: If the model call fails (the user message is rolled back).
        """
        text = self._validate(text)
        self._memory.append(session_id, {"role": "user", "content": text})
        try:
            reply = self._llm.complete(self._build_messages(session_id))
        except LLMError:
            self._memory.pop_last(session_id)
            raise
        self._memory.append(session_id, {"role": "assistant", "content": reply})
        return reply

    def chat_stream(self, session_id: str, text: str) -> Iterator[str]:
        """Send a message and yield reply chunks; memory is updated when done.

        Raises:
            InvalidMessageError: If the message is invalid (raised on first iteration).
            LLMError: If the model call fails (the user message is rolled back).
        """
        text = self._validate(text)
        self._memory.append(session_id, {"role": "user", "content": text})
        parts: list[str] = []
        try:
            for chunk in self._llm.stream(self._build_messages(session_id)):
                parts.append(chunk)
                yield chunk
        except LLMError:
            self._memory.pop_last(session_id)
            raise
        except GeneratorExit:
            # Client disconnected: keep what was generated so context stays consistent.
            if parts:
                self._memory.append(session_id, {"role": "assistant", "content": "".join(parts)})
            else:
                self._memory.pop_last(session_id)
            raise
        reply = "".join(parts)
        if not reply:
            self._memory.pop_last(session_id)
            raise LLMError("Model returned an empty response")
        self._memory.append(session_id, {"role": "assistant", "content": reply})
