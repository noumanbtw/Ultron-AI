"""Tell the current time and date (standard library only)."""

from __future__ import annotations

from datetime import datetime


def run(argument: str = "") -> str:
    now = datetime.now()
    lowered = argument.lower()
    if "date" in lowered and "time" not in lowered:
        return f"Today is {now.strftime('%A, %d %B %Y')}."
    if "day" in lowered:
        return f"Today is {now.strftime('%A')}."
    return (
        f"It is {now.strftime('%I:%M %p')} "
        f"on {now.strftime('%A, %d %B %Y')}."
    )
