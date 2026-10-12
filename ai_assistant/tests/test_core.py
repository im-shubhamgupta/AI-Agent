import pytest

from assistant.core.assistant import InvalidMessageError
from assistant.core.llm_client import LLMError


def test_chat_remembers_history(make_assistant):
    bot, llm = make_assistant()
    bot.chat("s", "hi")
    bot.chat("s", "again")
    sent = llm.calls[-1]
    assert [m["role"] for m in sent] == ["system", "user", "assistant", "user"]


def test_stream_collects_reply_into_memory(make_assistant):
    bot, _ = make_assistant()
    assert "".join(bot.chat_stream("s", "hi")) == "hello back"
    assert bot.memory.get("s")[-1] == {"role": "assistant", "content": "hello back"}


@pytest.mark.parametrize("text", ["", "   ", "x" * 51])
def test_invalid_messages_rejected(make_assistant, text):
    bot, _ = make_assistant()
    with pytest.raises(InvalidMessageError):
        bot.chat("s", text)


def test_failure_rolls_back_user_message(make_assistant):
    bot, _ = make_assistant(fail=True)
    with pytest.raises(LLMError):
        bot.chat("s", "hi")
    with pytest.raises(LLMError):
        list(bot.chat_stream("s", "hi"))
    assert bot.memory.get("s") == []


def test_history_is_bounded(make_assistant):
    bot, _ = make_assistant()
    for i in range(5):
        bot.chat("s", f"m{i}")
    assert len(bot.memory.get("s")) == 4
