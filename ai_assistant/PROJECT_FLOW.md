# प्रोजेक्ट का फ्लो और फाइलों की जानकारी

## 1. डेटा का फ्लो (Data Flow)

### Web (Browser) में

```
आप "Hello" टाइप करते हैं और Enter दबाते हैं
        │
        ▼
 main.js        टेक्स्ट लेता है, आपका मैसेज दाईं तरफ दिखाता है,
                preloader (3 dots) दिखाता है
        │
        ▼
 api.js         backend को भेजता है:
                POST /api/chat   {"session_id": "abc123", "message": "Hello"}
        │   (नेटवर्क पर HTTP request)
        ▼
 routes.py      /chat route request लेता है
                schemas.py जाँचता है कि डेटा सही है (session id, खाली मैसेज नहीं)
        │
        ▼
 assistant.py   मैसेज की लंबाई जाँचता है, आपका मैसेज memory में सेव करता है,
                लिस्ट बनाता है: [system prompt + पिछले सभी मैसेज]
        │
        ▼
 llm_client.py  यह लिस्ट आपके AI model (Ollama) को BASE_URL से भेजता है
        │
        ▼
 Ollama / Qwen  जवाब शब्द-दर-शब्द बनाता है
        │
        ▼
 जवाब उसी रास्ते से वापस आता है, छोटे-छोटे टुकड़ों में:
 llm_client → assistant (टुकड़े जोड़ता है) → routes.py (हर टुकड़ा
 data: {"token": "Hi"} के रूप में भेजता है) → api.js (टुकड़े पढ़ता है) → ui.js
        │
        ▼
 ui.js          3 dots हटाकर टेक्स्ट दिखाता है और हर नया टुकड़ा जोड़ता जाता है।
                पूरा जवाब memory में सेव हो जाता है।
```

**Memory क्यों ज़रूरी है:** हर request में पूरी बातचीत (पुराने सभी मैसेज) model को भेजी जाती है। इसी से AI को पिछली बातें "याद" रहती हैं। आपकी original `meassages` list भी यही काम करती थी।

**टेक्स्ट शब्द-दर-शब्द क्यों आता है:** server पूरा जवाब बनने का इंतज़ार नहीं करता, वह जवाब छोटे टुकड़ों में भेजता है (streaming), जैसे ChatGPT करता है।

### Terminal में

```
Terminal में टाइप करें → cli/main.py → assistant.py → llm_client.py → Ollama
                              ◄──── हर टुकड़ा आते ही print होता है ◄────
```

CLI और Web एक ही code के दो अलग दरवाज़े हैं। दोनों `assistant.py` को call करते हैं, इसलिए logic सिर्फ एक जगह है।

## 2. फाइलें और फोल्डर किसलिए हैं

| फाइल / फोल्डर | काम |
|---|---|
| `src/assistant/core/` | असली दिमाग: chat logic, model से बात, memory। CLI और Web दोनों इसे use करते हैं। |
| `src/assistant/cli/` | Terminal वर्शन। |
| `src/assistant/web/` | Browser वर्शन: backend (`app.py`, `routes.py`, `schemas.py`) और frontend (`static/`)। |
| `config.py` | `.env` से settings पढ़ता है, ताकि code में secrets न रहें। |
| `factory.py` | सारे हिस्से (client + memory + assistant) एक जगह जोड़ता है। |
| `static/css`, `static/js` | पेज का design और behaviour, काम के हिसाब से अलग-अलग फाइलों में। |
| `tests/` | अपने-आप चलने वाली जाँच कि code सही चल रहा है। |
| `run_cli.py`, `run_web.py` | Terminal और Browser शुरू करने वाली फाइलें। |
| `.env.example` | बताता है कौन सी settings चाहिए। असली `.env` private रहता है। |
| `requirements.txt` | App चलाने के लिए ज़रूरी packages। |
| `requirements-dev.txt` | सिर्फ development के packages (testing, linting)। |
| `pyproject.toml` | pytest और ruff की settings। |
| `.gitignore` | git को बताता है कि `.env` और cache फोल्डर छोड़ दे। |
| `README.md` | Setup और run कैसे करें। |

## 3. कौन सी फाइलें "unnecessary" लगती हैं, और क्या हटा सकते हैं?

| आइटम | क्या है | हटा सकते हैं? |
|---|---|---|
| `__pycache__/` (कई जगह) | Python अपनी compiled कॉपी यहाँ रखता है, ताकि app जल्दी शुरू हो। | हाँ, सुरक्षित है। अपने-आप दोबारा बन जाएगा। |
| `.pytest_cache/` | Tests चलाने पर बना। | हाँ, सुरक्षित है। |
| `.ruff_cache/` | Linter चलाने पर बना। | हाँ, सुरक्षित है। |
| `BUILD_LOG.md` | सिर्फ record कि मैंने क्या install किया और कौन से commands चलाए। App के लिए ज़रूरी नहीं। | हाँ। आप चाहें तो रखें, चाहें तो हटाएँ। |
| `PROJECT_FLOW.md` (यही फाइल) | सिर्फ समझाने के लिए documentation। | हाँ, पढ़ने के बाद हटा सकते हैं। |
| `__init__.py` (खाली फाइलें) | Python को बताती हैं कि यह फोल्डर एक package है। | **नहीं।** हटाने पर imports टूट सकते हैं। |
| `requirements-dev.txt` | Testing वाले packages की लिस्ट। | अगर tests नहीं चलाने, तो हाँ। वरना रखें। |
| `pyproject.toml` | pytest/ruff की settings। | हटाने पर tests के import path की setting चली जाएगी, इसलिए रखें। |
| `.gitignore` | `.env` को git में जाने से रोकता है। | **नहीं।** secrets की सुरक्षा के लिए ज़रूरी है। |

### सारांश
- **बिना डर के हटाने लायक:** `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`, `BUILD_LOG.md`, `PROJECT_FLOW.md`।
- **मत हटाइए:** `__init__.py`, `.gitignore`, `pyproject.toml`, और `src/`, `static/`, `run_*.py` की सारी फाइलें।

हटाने का एक command (जब आप चाहें):
```bash
cd /var/www/html/AI-Agent/Day02/ai_assistant
find . -type d \( -name __pycache__ -o -name .pytest_cache -o -name .ruff_cache \) -prune -exec rm -rf {} +
```
