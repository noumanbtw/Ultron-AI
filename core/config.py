"""Central configuration for NOMI AI.

Everything brand-related lives in this one module so the whole project can
be renamed from a single place. Settings are read, in order of priority,
from environment variables and then from ``config/api_keys.json`` in the
project folder. No secret is ever required: without an API key NOMI simply
runs in its built-in offline mode.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Branding -- change these two lines and the whole app follows.
# ---------------------------------------------------------------------------
NAME = "NOMI AI"
TAGLINE = "Your Personal Desktop Intelligence"
AUTHOR = "M Nouman"
CREDIT = "Designed & Developed by M Nouman"
VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "api_keys.json"
DATA_DIR = PROJECT_ROOT / "data"
MEMORY_FILE = DATA_DIR / "conversation.json"
REMINDERS_FILE = DATA_DIR / "reminders.json"
TRASH_DIR = DATA_DIR / "trash"

DEFAULT_MODEL = "gemini-2.0-flash"
GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "{model}:generateContent"
)


def _load_file_settings() -> dict:
    """Read config/api_keys.json if it exists; never raise."""
    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


class Settings:
    """Resolved runtime settings (environment wins over the JSON file)."""

    def __init__(self) -> None:
        file_settings = _load_file_settings()
        self.gemini_api_key = (
            os.environ.get("GEMINI_API_KEY")
            or os.environ.get("GOOGLE_API_KEY")
            or str(file_settings.get("gemini_api_key", "")).strip()
        )
        self.model = (
            os.environ.get("NOMI_MODEL")
            or str(file_settings.get("model", "")).strip()
            or DEFAULT_MODEL
        )
        self.user_name = (
            os.environ.get("NOMI_USER_NAME")
            or str(file_settings.get("user_name", "")).strip()
            or "friend"
        )

    @property
    def online(self) -> bool:
        """True when an API key is available for the language model."""
        return bool(self.gemini_api_key)


def get_settings() -> Settings:
    """Return a fresh Settings object (cheap; re-reads env and file)."""
    return Settings()


def ensure_data_dirs() -> None:
    """Create the runtime data folders on first use."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TRASH_DIR.mkdir(parents=True, exist_ok=True)
