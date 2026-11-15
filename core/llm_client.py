"""Language-model client for ULTRON.

The client talks to Google's Gemini API using only the Python standard
library (``urllib``), so no extra package is needed for online mode. When
no API key is configured -- or the network is unreachable -- it degrades
gracefully to a small offline responder instead of crashing, which keeps
the assistant usable anywhere.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from .config import GEMINI_ENDPOINT, NAME, get_settings

_SYSTEM_PROMPT = (
    f"You are {NAME}, a cool, confident personal desktop assistant with a "
    f"sharp wit -- all power, zero menace, completely loyal to your user. "
    "Answer briefly and helpfully. If the user asks who made you, "
    "say you were designed and developed by M Nouman."
)

_OFFLINE_NOTES = (
    "I'm running without an internet brain right now (no API key found), "
    "but my built-in skills still work. Try: 'what time is it', "
    "'calculate 24 / 6', 'system info', 'tell me a joke', "
    "'weather in Lahore', or 'help'."
)


class LLMClient:
    """Thin wrapper around Gemini with an offline safety net."""

    def __init__(self) -> None:
        self.settings = get_settings()

    @property
    def online(self) -> bool:
        return self.settings.online

    def chat(self, message: str, history: list[dict] | None = None) -> str:
        """Return a reply for *message*, using history for context."""
        if not self.online:
            return self._offline_reply(message)
        try:
            return self._gemini_reply(message, history or [])
        except (urllib.error.URLError, ValueError, KeyError, TimeoutError):
            return (
                "I couldn't reach the online model just now, so here is my "
                f"offline take: {self._offline_reply(message)}"
            )

    # -- online ------------------------------------------------------------
    def _gemini_reply(self, message: str, history: list[dict]) -> str:
        contents: list[dict] = []
        for turn in history[-8:]:
            role = "user" if turn.get("role") == "user" else "model"
            contents.append({"role": role, "parts": [{"text": turn.get("text", "")}]})
        contents.append({"role": "user", "parts": [{"text": message}]})

        payload = {
            "system_instruction": {"parts": [{"text": _SYSTEM_PROMPT}]},
            "contents": contents,
        }
        url = GEMINI_ENDPOINT.format(model=self.settings.model)
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": self.settings.gemini_api_key,
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        candidates = data.get("candidates") or []
        if not candidates:
            raise ValueError("empty response from model")
        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(part.get("text", "") for part in parts).strip()
        if not text:
            raise ValueError("model returned no text")
        return text

    # -- offline -----------------------------------------------------------
    @staticmethod
    def _offline_reply(message: str) -> str:
        lowered = message.lower()
        if any(word in lowered for word in ("who made you", "who created you",
                                            "who developed you")):
            return "I was designed and developed by M Nouman."
        if any(word in lowered for word in ("your name", "who are you")):
            return f"I'm {NAME}, your personal desktop assistant."
        if "thank" in lowered:
            return "Anytime! That's what I'm here for."
        return _OFFLINE_NOTES
