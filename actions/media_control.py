"""Media playback control (play/pause, next, previous, volume).

On Linux this prefers the ``playerctl`` command-line tool when present.
Everywhere else it tries the optional ``pyautogui`` package to press the
standard media keys. If neither route is available the action says so
plainly instead of pretending it worked.
"""

from __future__ import annotations

import shutil
import subprocess

_COMMANDS = {
    "play": "play-pause",
    "pause": "play-pause",
    "resume": "play-pause",
    "next": "next",
    "previous": "previous",
    "prev": "previous",
    "stop": "stop",
}

_PYAG_KEYS = {
    "play-pause": "playpause",
    "next": "nexttrack",
    "previous": "prevtrack",
    "stop": "stop",
}


def run(argument: str = "") -> str:
    action = argument.strip().lower()
    if action.startswith("volume"):
        return _volume(action)
    command = _COMMANDS.get(action)
    if command is None:
        return "Media options: play, pause, next, previous, stop, volume up, volume down."
    if shutil.which("playerctl"):
        try:
            subprocess.run(["playerctl", command], check=True, timeout=5)
            return f"Media: {action}."
        except (subprocess.SubprocessError, OSError):
            pass
    try:
        import pyautogui

        pyautogui.press(_PYAG_KEYS[command])
        return f"Media: {action}."
    except Exception:
        return (
            "I can't reach a media player here (no playerctl or pyautogui "
            "available), so nothing was changed."
        )


def _volume(action: str) -> str:
    direction = "up" if "up" in action else "down" if "down" in action else ""
    if not direction:
        return "Say 'volume up' or 'volume down'."
    try:
        import pyautogui

        pyautogui.press("volumeup" if direction == "up" else "volumedown")
        return f"Volume {direction}."
    except Exception:
        return "Volume keys aren't reachable from here on this machine."
