"""Open common desktop applications by friendly name.

A small built-in table maps names like "browser" or "calculator" to the
executable used on each operating system. Anything not found is reported
honestly instead of pretending it opened.
"""

from __future__ import annotations

import platform
import shutil
import subprocess

# friendly name -> {platform system -> executable or command}
_APPS: dict[str, dict[str, str]] = {
    "notepad": {"Windows": "notepad.exe", "Darwin": "TextEdit", "Linux": "gedit"},
    "calculator": {"Windows": "calc.exe", "Darwin": "Calculator", "Linux": "gnome-calculator"},
    "browser": {"Windows": "explorer", "Darwin": "Safari", "Linux": "xdg-open"},
    "terminal": {"Windows": "cmd.exe", "Darwin": "Terminal", "Linux": "x-terminal-emulator"},
    "paint": {"Windows": "mspaint.exe", "Darwin": "Preview", "Linux": "kolourpaint"},
    "file manager": {"Windows": "explorer.exe", "Darwin": "Finder", "Linux": "xdg-open"},
    "files": {"Windows": "explorer.exe", "Darwin": "Finder", "Linux": "xdg-open"},
}


def _launch(command: str, friendly: str) -> str:
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.Popen(["open", "-a", command])
        elif system == "Linux" and command == "xdg-open":
            target = "https://example.com" if friendly == "browser" else "."
            subprocess.Popen([command, target])
        else:
            subprocess.Popen([command])
    except (OSError, ValueError):
        return f"I tried to open {friendly}, but the launch failed."
    return f"Opening {friendly} for you."


def run(argument: str = "") -> str:
    name = argument.strip().lower()
    if not name:
        known = ", ".join(sorted(_APPS))
        return f"Which app? I know these names: {known}."
    system = platform.system()
    entry = _APPS.get(name)
    if entry is None:
        # Treat the request itself as an executable name.
        if shutil.which(name):
            return _launch(name, name)
        known = ", ".join(sorted(_APPS))
        return f"I don't have '{name}' in my list. I know: {known}."
    command = entry.get(system)
    if command is None:
        return f"I don't know how to open {name} on {system} yet."
    if system != "Darwin" and shutil.which(command) is None:
        return f"'{name}' doesn't seem to be installed on this machine."
    return _launch(command, name)
