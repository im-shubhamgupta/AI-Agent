import pytest

from assistant.config import Settings
from assistant.core.assistant import Assistant
from assistant.core.llm_client import LLMError
from assistant.core.memory import InMemoryStore


class FakeLLM:
    def __init__(self, fail: bool = False):
        self.fail = fail
        self.calls: list[list[dict]] = []

    def complete(self, messages):
        self.calls.append(messages)
        if self.fail:
            raise LLMError("boom")
        return "hello back"

    def stream(self, messages):
        self.calls.append(messages)
        if self.fail:
            raise LLMError("boom")
        yield from ["hello ", "back"]


@pytest.fixture
def settings():
    return Settings(base_url="http://x", api_key="k", model="m", max_message_chars=50)


@pytest.fixture
def make_assistant(settings):
    def _make(fail=False):
        llm = FakeLLM(fail=fail)
        return Assistant(settings, llm, InMemoryStore(max_messages=4)), llm

    return _make
