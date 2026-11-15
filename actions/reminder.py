"""Simple reminders stored in a JSON file.

Reminders are plain records -- text plus an optional due time -- kept in
``data/reminders.json``. NOMI lists and clears them on request; a due
reminder is shown when you list them after its time has passed.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timedelta

from core.config import REMINDERS_FILE, ensure_data_dirs


def _load() -> list[dict]:
    try:
        with REMINDERS_FILE.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, list) else []
    except (OSError, ValueError):
        return []


def _save(items: list[dict]) -> None:
    ensure_data_dirs()
    tmp_path = REMINDERS_FILE.with_suffix(".json.tmp")
    with tmp_path.open("w", encoding="utf-8") as handle:
        json.dump(items, handle, ensure_ascii=False, indent=2)
    os.replace(tmp_path, REMINDERS_FILE)


def _parse_due(text: str) -> tuple[str, datetime | None]:
    """Pull 'in N minutes/hours' out of the text; return (clean text, due)."""
    match = re.search(r"\bin\s+(\d+)\s*(minutes?|mins?|hours?|hrs?|days?)\b",
                      text, re.IGNORECASE)
    if not match:
        return text.strip(), None
    amount = int(match.group(1))
    unit = match.group(2).lower()
    if unit.startswith("hour") or unit.startswith("hr"):
        delta = timedelta(hours=amount)
    elif unit.startswith("day"):
        delta = timedelta(days=amount)
    else:
        delta = timedelta(minutes=amount)
    cleaned = (text[: match.start()] + text[match.end():]).strip(" ,")
    return cleaned, datetime.now() + delta


def add(argument: str = "") -> str:
    text, due = _parse_due(argument.strip())
    if due is not None and text.lower().startswith("to "):
        text = text[3:].strip()
    if not text:
        return "Remind you about what? Try 'remind me in 10 minutes to stretch'."
    items = _load()
    record = {
        "text": text,
        "created": datetime.now().isoformat(timespec="seconds"),
        "due": due.isoformat(timespec="seconds") if due else None,
    }
    items.append(record)
    _save(items)
    if due:
        return f"Reminder saved: '{text}' -- due {due.strftime('%d %b %I:%M %p')}."
    return f"Reminder saved: '{text}' (no due time)."


def list_reminders(_argument: str = "") -> str:
    items = _load()
    if not items:
        return "You have no reminders saved."
    now = datetime.now()
    lines = ["Your reminders:"]
    for index, item in enumerate(items, start=1):
        due_text = "no due time"
        if item.get("due"):
            due = datetime.fromisoformat(item["due"])
            due_text = due.strftime("%d %b %I:%M %p")
            if due <= now:
                due_text += " -- DUE NOW"
        lines.append(f"{index}. {item['text']} ({due_text})")
    return "\n".join(lines)


def clear(_argument: str = "") -> str:
    _save([])
    return "All reminders cleared."


def run(argument: str = "") -> str:
    return add(argument)
