"""Start the web UI: python run_web.py  (then open http://127.0.0.1:8000)"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import uvicorn  # noqa: E402

if __name__ == "__main__":
    uvicorn.run(
        "assistant.web.app:create_app",
        factory=True,
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
    )
