# AI Assistant (CLI + Web UI)

An AI assistant with conversation memory, usable from the terminal or a browser.

## Setup
```bash
pip install -r requirements.txt        # dev: requirements-dev.txt
cp .env.example .env                   # then edit BASE_URL / API_KEY / MODEL
```
Make sure your model server (e.g. `ollama serve`) is running.

## Run
```bash
python run_cli.py      # terminal chat (type exit / quit / bye to leave)
python run_web.py      # browser UI at http://127.0.0.1:8000
```

## Layout
- `src/assistant/core/` – chat logic, LLM client, memory (no I/O; shared by CLI and web)
- `src/assistant/cli/` – terminal interface
- `src/assistant/web/` – FastAPI app (`routes.py`) and static frontend (`static/css`, `static/js` ES modules)
- `tests/` – pytest suite

## Extending
- **Persistence:** implement `MemoryStore` (e.g. SQLite) and pass it in `factory.py`.
- **New model/provider:** change `.env`, or add a client alongside `llm_client.py`.
- **New UI feature:** add a module under `static/js/` and wire it in `main.js`.

## Checks
```bash
ruff check . && pytest
```
