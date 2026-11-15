"""Intent routing for NOMI AI.

The router looks at one line of user input, decides which built-in
action (if any) it matches, and returns that action's response. Anything
that matches no built-in skill is handed to the language-model client,
which itself falls back to an offline reply when no API key is set.
Matching is intentionally simple -- prefixes and a few regular
expressions -- so behaviour is predictable and easy to extend.
"""

from __future__ import annotations

import re

from actions import (
    calculator,
    clipboard_tool,
    file_controller,
    fun,
    media_control,
    open_app,
    reminder,
    screenshot,
    system_info,
    time_date,
    weather,
    web_search,
)
from core.llm_client import LLMClient

HELP_TEXT = """Here's what I can do:
  - what time is it / what is the date
  - calculate 12 * 8
  - system info
  - weather in <city>
  - search <anything>
  - open <app>            (notepad, calculator, browser, terminal, files)
  - remind me in 10 minutes to <task>  |  list reminders  |  clear reminders
  - list files [folder]   |  create file <name>  |  create folder <name>
  - delete <file>         (safe delete -- always recoverable)
  - take a screenshot
  - read clipboard        |  copy <text>
  - play / pause / next / previous / volume up / volume down
  - tell me a joke        |  give me a quote
  - clear memory
  - Or just chat with me about anything else."""

_CALC_PREFIX = re.compile(r"^(?:calculate|calc|compute|what is|what's)\s+(.+)$", re.I)
_BARE_MATH = re.compile(r"^[\d\s+\-*/().%]+$")
_WEATHER = re.compile(r"^weather(?:\s+in)?\s+(.+)$", re.I)
_SEARCH = re.compile(r"^(?:search(?:\s+for)?|google|look up)\s+(.+)$", re.I)
_OPEN = re.compile(r"^(?:open|launch|start)\s+(.+)$", re.I)
_REMIND = re.compile(r"^remind me\s+(.+)$", re.I)
_DELETE = re.compile(r"^(?:delete|remove)\s+(.+)$", re.I)
_COPY = re.compile(r"^copy\s+(.+)$", re.I)
_MEDIA = re.compile(
    r"^(play|pause|resume|next|previous|prev|stop|volume up|volume down)$", re.I
)


class Router:
    """Maps raw user input to an action response or a chat reply."""

    def __init__(self, llm: LLMClient | None = None) -> None:
        self.llm = llm or LLMClient()

    def handle(self, raw_text: str, history: list[dict] | None = None) -> str:
        text = " ".join(raw_text.strip().split())
        if not text:
            return "I'm listening -- type 'help' to see what I can do."
        lowered = text.lower()

        if lowered in ("help", "commands", "what can you do"):
            return HELP_TEXT
        if lowered in ("time", "what time is it", "current time") or (
            "time" in lowered and lowered.startswith(("what", "tell"))
        ):
            return time_date.run(text)
        if lowered.startswith(("what is the date", "what's the date",
                               "today's date", "date")):
            return time_date.run("date")
        if lowered in ("system info", "system information", "pc info",
                       "computer info", "my system"):
            return system_info.run()
        if lowered in ("tell me a joke", "joke", "make me laugh"):
            return fun.joke()
        if lowered in ("give me a quote", "quote", "motivate me",
                       "inspire me"):
            return fun.quote()

        match = _CALC_PREFIX.match(text)
        if match and re.search(r"\d", match.group(1)) and (
            re.search(r"[+\-*/%()]", match.group(1)) or "calculate" in lowered
            or lowered.startswith(("calc", "compute"))
        ):
            return calculator.run(match.group(1))
        if _BARE_MATH.match(text) and re.search(r"[+\-*/%]", text):
            return calculator.run(text)

        match = _WEATHER.match(text)
        if match:
            return weather.run(match.group(1))
        match = _SEARCH.match(text)
        if match:
            return web_search.run(match.group(1))
        match = _REMIND.match(text)
        if match:
            return reminder.add(match.group(1))
        if lowered in ("list reminders", "show reminders", "reminders"):
            return reminder.list_reminders()
        if lowered in ("clear reminders", "delete reminders"):
            return reminder.clear()
        if lowered.startswith("list files"):
            return file_controller.list_files(text[len("list files"):])
        if lowered.startswith("create file"):
            return file_controller.create_file(text[len("create file"):])
        if lowered.startswith("create folder"):
            return file_controller.create_folder(text[len("create folder"):])
        match = _DELETE.match(text)
        if match:
            return file_controller.safe_delete(match.group(1))
        if lowered in ("take a screenshot", "screenshot", "capture screen"):
            return screenshot.run()
        if lowered in ("read clipboard", "show clipboard", "clipboard"):
            return clipboard_tool.read()
        match = _COPY.match(text)
        if match:
            return clipboard_tool.write(match.group(1))
        match = _MEDIA.match(text)
        if match:
            return media_control.run(match.group(1))
        match = _OPEN.match(text)
        if match:
            return open_app.run(match.group(1))

        return self.llm.chat(text, history or [])
