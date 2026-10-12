"""Application settings, loaded once from environment variables / a .env file."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parents[2]


class ConfigError(RuntimeError):
    """Raised when a required setting is missing or invalid."""


@dataclass(frozen=True)
class Settings:
    """Immutable runtime configuration.

    Attributes:
        base_url: OpenAI-compatible API endpoint.
        api_key: API key (Ollama accepts any non-empty value).
        model: Model name to chat with.
        system_prompt: Instruction prepended to every conversation.
        max_history_messages: Max messages kept per session (oldest dropped first).
        max_message_chars: Max length of a single user message.
        timeout_seconds: Per-request timeout for the model call.
    """

    base_url: str
    api_key: str
    model: str
    system_prompt: str = "You are a helpful assistant."
    max_history_messages: int = 40
    max_message_chars: int = 4000
    timeout_seconds: float = 120.0


def _int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ConfigError(f"{name} must be an integer, got {raw!r}") from exc
    if value <= 0:
        raise ConfigError(f"{name} must be positive")
    return value


def load_settings() -> Settings:
    """Read settings from the environment.

    Returns:
        A populated Settings instance.

    Raises:
        ConfigError: If BASE_URL, API_KEY or MODEL is missing, or a numeric
            option is invalid.
    """
    # Look for .env in the project root first, then the current directory.
    load_dotenv(_PROJECT_ROOT / ".env")
    load_dotenv()

    missing = [k for k in ("BASE_URL", "API_KEY", "MODEL") if not os.getenv(k)]
    if missing:
        raise ConfigError(f"Missing required environment variable(s): {', '.join(missing)}")

    return Settings(
        base_url=os.environ["BASE_URL"],
        api_key=os.environ["API_KEY"],
        model=os.environ["MODEL"],
        system_prompt=os.getenv("SYSTEM_PROMPT", Settings.system_prompt),
        max_history_messages=_int("MAX_HISTORY_MESSAGES", 40),
        max_message_chars=_int("MAX_MESSAGE_CHARS", 4000),
        timeout_seconds=float(_int("REQUEST_TIMEOUT_SECONDS", 120)),
    )
