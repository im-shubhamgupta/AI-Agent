# Build Log: AI Assistant (CLI + Web UI)

A record of the packages installed and the terminal commands run while building this project.

## Packages installed

One install command, run into the project venv at `/var/www/html/AI-Agent/.venv`:

```bash
cd /var/www/html/AI-Agent && .venv/bin/pip install fastapi uvicorn pytest ruff
```

**Requested packages**

| Package | Version | Purpose |
|---|---|---|
| fastapi | 0.143.0 | Web API framework |
| uvicorn | 0.54.0 | Server that runs FastAPI |
| pytest | 9.1.1 | Test runner (dev only) |
| ruff | 0.17.0 | Linter (dev only) |

**Dependencies pulled in automatically:** starlette 1.7.0, pygments 2.21.0, pluggy 1.6.0, packaging 26.3, opentelemetry-api 1.45.1, iniconfig 2.3.1, click 8.5.0, annotated-doc 0.0.5.

**Already present and untouched:** openai, python-dotenv, pydantic, httpx2. Nothing was upgraded or removed.

`requirements-dev.txt` also lists `httpx`, which FastAPI's `TestClient` needs. It was not installed, because the venv already has `httpx2` and the tests passed.

## Terminal commands run

### 1. Inspect the environment (read-only)
```bash
ls -la /var/www/html/AI-Agent/Day02/ /var/www/html/AI-Agent/
cut -d= -f1 Day02/.env        # printed only the key names, not the values
cat Readme.md
.venv/bin/python --version
.venv/bin/pip list | grep -iE "fastapi|uvicorn|openai|dotenv|pytest|ruff|pydantic|httpx"
```

### 2. Install packages
See the install command above.

### 3. Create the project skeleton and files
```bash
mkdir -p ai_assistant/src/assistant/{core,cli,web/static/css,web/static/js} ai_assistant/tests
touch <the __init__.py files>
cat > <file> <<'EOF' ...      # wrote the source, config, test and README files
```
Files only were created, with no deletions. `.env.example` contains placeholder values.

### 4. Lint and test
```bash
.venv/bin/ruff check Day02/ai_assistant --fix
../../.venv/bin/python -m pytest -q
```
`--fix` lets ruff auto-correct import ordering and similar style issues.

### 5. Live testing
```bash
set -a && . ../.env && set +a              # loaded the existing .env into the shell
../../.venv/bin/python run_web.py          # started the server
curl -s localhost:8000/api/health
curl -s -o /dev/null -w "%{http_code}" localhost:8000/static/<each file>
curl -sN -X POST localhost:8000/api/chat -d '{...}'
curl -s localhost:8000/api/sessions
printf 'Say hi in 3 words\nexit\n' | python run_cli.py
pkill -f run_web.py                        # stopped the server
pgrep -fa run_web.py                       # confirmed it was stopped
```
The server was started in the background for the test and stopped afterwards.

### 6. File edits made with editor tools (not the terminal)
- Read `Day02/assistant.py`.
- Edited `static/css/chat.css` so user messages appear on the right.

## What was not run
- No `git add`, `commit` or `push`.
- No file deletions.
- No `pip uninstall` or upgrades.
- No database or schema changes.
- No system-level installs; everything stayed inside the project venv.
