"""Read from and write to the system clipboard.

Uses the optional ``pyperclip`` package when installed. Without it the
action explains the one-line install instead of raising an error.
"""

from __future__ import annotations

_INSTALL_HINT = "Clipboard support needs one package: pip install pyperclip"


def read(_argument: str = "") -> str:
    try:
        import pyperclip
    except ImportError:
        return _INSTALL_HINT
    try:
        text = pyperclip.paste()
    except Exception:
        return "The clipboard isn't reachable from this session."
    if not text:
        return "The clipboard is empty right now."
    preview = text if len(text) <= 500 else text[:500] + "..."
    return f"Clipboard contains:\n{preview}"


def write(argument: str = "") -> str:
    text = argument.strip()
    if not text:
        return "What should I copy? Try 'copy hello world'."
    try:
        import pyperclip
    except ImportError:
        return _INSTALL_HINT
    try:
        pyperclip.copy(text)
    except Exception:
        return "The clipboard isn't reachable from this session."
    return f"Copied to clipboard: {text}"


def run(argument: str = "") -> str:
    return read(argument)
