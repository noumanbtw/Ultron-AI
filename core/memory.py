"""Conversation memory for NOMI AI.

A deliberately simple JSON-backed store: the recent conversation is kept
as a list of ``{"role": ..., "text": ...}`` turns in
``data/conversation.json``. The store caps itself so the file never grows
without bound, and every write is done through a temporary file so a
crash mid-save cannot corrupt the history.
"""

from __future__ import annotations

import json
import os

from .config import MEMORY_FILE, ensure_data_dirs

MAX_TURNS = 200


class Memory:
    """Load, append to, and persist the conversation history."""

    def __init__(self) -> None:
        ensure_data_dirs()
        self._turns: list[dict] = self._load()

    # -- persistence -------------------------------------------------------
    def _load(self) -> list[dict]:
        try:
            with MEMORY_FILE.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            if isinstance(data, list):
                return [t for t in data if isinstance(t, dict)][-MAX_TURNS:]
        except (OSError, ValueError):
            pass
        return []

    def _save(self) -> None:
        tmp_path = MEMORY_FILE.with_suffix(".json.tmp")
        with tmp_path.open("w", encoding="utf-8") as handle:
            json.dump(self._turns, handle, ensure_ascii=False, indent=2)
        os.replace(tmp_path, MEMORY_FILE)

    # -- public API --------------------------------------------------------
    def add(self, role: str, text: str) -> None:
        self._turns.append({"role": role, "text": text})
        self._turns = self._turns[-MAX_TURNS:]
        self._save()

    def recent(self, count: int = 10) -> list[dict]:
        return self._turns[-count:]

    def __len__(self) -> int:
        return len(self._turns)

    def clear(self) -> None:
        self._turns = []
        self._save()
