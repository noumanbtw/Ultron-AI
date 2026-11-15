#!/usr/bin/env python3
"""ULTRON -- Your Personal Desktop Intelligence.

Entry point. Runs a chat loop that works fully headless (piped input,
no microphone, no display) and adds optional voice interaction when the
speech packages happen to be installed and ``--voice`` is passed.

Usage:
    python main.py            # interactive / piped chat
    python main.py --voice    # talk and listen (needs extra packages)
    python main.py --once "what time is it"
"""

from __future__ import annotations

import sys

from core.config import CREDIT, NAME, TAGLINE
from core.memory import Memory
from core.router import Router

EXIT_WORDS = {"exit", "quit", "bye", "goodbye"}


def banner() -> str:
    mode = "online" if _router.llm.online else "offline (no API key found)"
    return (
        f"{NAME} -- {TAGLINE}\n"
        f"Mode: {mode}. Type 'help' for commands, 'exit' to leave.\n"
        f"{CREDIT}"
    )


def speak(text: str) -> None:
    """Best-effort text-to-speech; silently skipped when unavailable."""
    try:
        import pyttsx3

        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass


def listen_once() -> str:
    """Best-effort speech recognition; returns '' when unavailable."""
    try:
        import speech_recognition as sr

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5)
        return recognizer.recognize_google(audio)
    except Exception:
        return ""


_router = Router()
_memory = Memory()


def process(text: str) -> str:
    """Handle one line of input and remember the exchange."""
    if text.strip().lower() == "clear memory":
        _memory.clear()
        return "Conversation memory cleared."
    reply = _router.handle(text, history=_memory.recent())
    _memory.add("user", text)
    _memory.add("assistant", reply)
    return reply


def main(argv: list[str]) -> int:
    args = argv[1:]
    if "--once" in args:
        index = args.index("--once")
        prompt = " ".join(args[index + 1:]).strip()
        if not prompt:
            print("Usage: python main.py --once \"your command\"")
            return 2
        print(process(prompt))
        return 0

    voice = "--voice" in args
    print(banner())

    if not sys.stdin.isatty():
        # Piped input: answer each line, then exit cleanly at EOF.
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            if line.lower() in EXIT_WORDS:
                print(f"{NAME}: Goodbye!")
                break
            print(f"{NAME}: {process(line)}")
        return 0

    while True:
        try:
            if voice:
                print("Listening... (speak now, or press Enter to type)")
                spoken = listen_once()
                text = spoken or input("You: ")
            else:
                text = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{NAME}: Goodbye!")
            return 0
        text = text.strip()
        if not text:
            continue
        if text.lower() in EXIT_WORDS:
            print(f"{NAME}: Goodbye!")
            return 0
        reply = process(text)
        print(f"{NAME}: {reply}")
        if voice:
            speak(reply)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
