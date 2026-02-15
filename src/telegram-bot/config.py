"""Configuration loaded from environment variables.

Expected env file: ~/.config/precept/telegram-bot.env
Set via systemd EnvironmentFile directive.
"""

import os
import sys
from pathlib import Path

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
ALLOWED_USER_ID = int(os.environ.get("ALLOWED_USER_ID", "0"))

PROJECTS_DIR = Path(os.environ.get("PROJECTS_DIR", str(Path.home() / "Projects")))

# SQLite database path
DB_PATH = Path(
    os.environ.get("PRECEPT_DB_PATH", str(Path.home() / ".config/precept/precept.db"))
)

# Telegram message length limit
MAX_MESSAGE_LENGTH = 4096

# Date format used in filenames
DATE_FORMAT = "%Y-%m-%d"


def validate():
    """Exit with a clear error if required config is missing."""
    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")
    if not ALLOWED_USER_ID:
        missing.append("ALLOWED_USER_ID")
    if missing:
        print(f"Missing required env vars: {', '.join(missing)}", file=sys.stderr)
        print("Set them in ~/.config/precept/telegram-bot.env", file=sys.stderr)
        sys.exit(1)
    if not PROJECTS_DIR.is_dir():
        print(f"PROJECTS_DIR not found: {PROJECTS_DIR}", file=sys.stderr)
        sys.exit(1)
