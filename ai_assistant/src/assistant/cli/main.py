"""Terminal interface."""

from __future__ import annotations

import sys

from assistant.config import ConfigError
from assistant.core.assistant import InvalidMessageError
from assistant.core.llm_client import LLMError
from assistant.factory import build_assistant

EXIT_WORDS = {"exit", "quit", "bye"}


def main() -> int:
    """Run the interactive chat loop. Returns a process exit code."""
    try:
        bot = build_assistant()
    except ConfigError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2

    print("=" * 40)
    print(" My AI Assistant")
    print("=" * 40)

    session_id = "cli"
    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return 0

        if user_input.strip().lower() in EXIT_WORDS:
            print("Exiting the chat. Goodbye! Have a great day")
            return 0

        print("\nAI: ", end="", flush=True)
        try:
            for chunk in bot.chat_stream(session_id, user_input):
                print(chunk, end="", flush=True)
            print("\n")
        except InvalidMessageError as exc:
            print(f"[{exc}]\n")
        except LLMError as exc:
            print(f"\n[Error] {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
