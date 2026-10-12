"""Builds a fully wired Assistant from settings."""

from __future__ import annotations

from assistant.config import Settings, load_settings
from assistant.core.assistant import Assistant
from assistant.core.llm_client import LLMClient
from assistant.core.memory import InMemoryStore


def build_assistant(settings: Settings | None = None) -> Assistant:
    """Create an Assistant using the given (or environment) settings.

    Raises:
        ConfigError: If required settings are missing.
    """
    settings = settings or load_settings()
    memory = InMemoryStore(max_messages=settings.max_history_messages)
    return Assistant(settings, LLMClient(settings), memory)
