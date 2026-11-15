"""Offline jokes and motivational quotes -- no network needed."""

from __future__ import annotations

import random

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I told my computer I needed a break, and now it won't stop sending me Kit Kat ads.",
    "Why did the developer go broke? He used up all his cache.",
    "There are only 10 kinds of people: those who understand binary and those who don't.",
    "My Wi-Fi went down for five minutes today, so I had to talk to my family. They seem like nice people.",
    "Why did the scarecrow win an award? Because he was outstanding in his field.",
    "I would tell you a UDP joke, but you might not get it -- and I wouldn't know.",
    "What do you call a fish without eyes? A fsh.",
]

QUOTES = [
    "Small steps every day beat big plans someday.",
    "The best time to start was yesterday; the second best time is now.",
    "Done is better than perfect.",
    "Curiosity is the engine of achievement.",
    "Make it work, make it right, make it fast -- in that order.",
    "Every expert was once a beginner who refused to give up.",
    "Your future is built by what you do today, not tomorrow.",
]


def joke(_argument: str = "") -> str:
    return random.choice(JOKES)


def quote(_argument: str = "") -> str:
    return random.choice(QUOTES)


def run(argument: str = "") -> str:
    if "quote" in argument.lower() or "motivat" in argument.lower():
        return quote(argument)
    return joke(argument)
