"""Thin wrapper around the OpenAI-compatible client."""

from __future__ import annotations

from collections.abc import Iterator

from openai import OpenAI, OpenAIError

from assistant.config import Settings


class LLMError(RuntimeError):
    """Raised when the model backend is unreachable, times out, or errors."""


class LLMClient:
    """Sends chat messages to the model and returns text or streamed chunks."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = OpenAI(
            base_url=settings.base_url,
            api_key=settings.api_key,
            timeout=settings.timeout_seconds,
        )

    def complete(self, messages: list[dict]) -> str:
        """Return the full reply.

        Raises:
            LLMError: On any backend failure or empty response.
        """
        try:
            resp = self._client.chat.completions.create(
                model=self._settings.model, messages=messages
            )
        except OpenAIError as exc:
            raise LLMError(f"Model request failed: {exc}") from exc
        content = resp.choices[0].message.content if resp.choices else None
        if not content:
            raise LLMError("Model returned an empty response")
        return content

    def stream(self, messages: list[dict]) -> Iterator[str]:
        """Yield reply text chunks as they arrive.

        Raises:
            LLMError: On any backend failure (may occur mid-stream).
        """
        try:
            stream = self._client.chat.completions.create(
                model=self._settings.model, messages=messages, stream=True
            )
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except OpenAIError as exc:
            raise LLMError(f"Model request failed: {exc}") from exc
