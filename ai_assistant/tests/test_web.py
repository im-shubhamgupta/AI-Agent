import json

from fastapi.testclient import TestClient

from assistant.web.app import create_app


def _events(resp):
    return [json.loads(b[6:]) for b in resp.text.split("\n\n") if b.startswith("data: ")]


def test_chat_streams_tokens(make_assistant):
    bot, _ = make_assistant()
    client = TestClient(create_app(bot))
    resp = client.post("/api/chat", json={"session_id": "abc", "message": "hi"})
    assert _events(resp) == [{"token": "hello "}, {"token": "back"}, {"done": True}]
    assert client.get("/api/sessions").json()[0]["id"] == "abc"
    assert len(client.get("/api/sessions/abc/messages").json()) == 2


def test_chat_reports_llm_error_without_leaking_details(make_assistant):
    bot, _ = make_assistant(fail=True)
    resp = TestClient(create_app(bot)).post(
        "/api/chat", json={"session_id": "abc", "message": "hi"}
    )
    (event,) = _events(resp)
    assert "boom" not in event["error"]


def test_rejects_bad_session_id(make_assistant):
    bot, _ = make_assistant()
    client = TestClient(create_app(bot))
    assert client.post("/api/chat", json={"session_id": "../x", "message": "hi"}).status_code == 422


def test_delete_session_and_index(make_assistant):
    bot, _ = make_assistant()
    client = TestClient(create_app(bot))
    client.post("/api/chat", json={"session_id": "abc", "message": "hi"})
    assert client.delete("/api/sessions/abc").status_code == 204
    assert client.get("/api/sessions").json() == []
    page = client.get("/")
    assert page.status_code == 200
    assert page.headers["content-security-policy"]
