"""Start the terminal chat: python run_cli.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from assistant.cli.main import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
