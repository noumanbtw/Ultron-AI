"""Basic file operations with a safe-delete guarantee.

Deleting never destroys anything outright: when the optional
``send2trash`` package is available the file goes to the operating
system's recycle bin / trash; otherwise it is moved into NOMI's own
``data/trash`` folder, from where it can always be recovered by hand.
"""

from __future__ import annotations

import shutil
import time
from pathlib import Path

from core.config import TRASH_DIR, ensure_data_dirs


def list_files(argument: str = "") -> str:
    folder = Path(argument.strip() or ".").expanduser()
    if not folder.is_dir():
        return f"'{folder}' is not a folder I can read."
    entries = sorted(folder.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    if not entries:
        return f"'{folder}' is empty."
    lines = [f"Contents of {folder}:"]
    for entry in entries[:50]:
        kind = "folder" if entry.is_dir() else "file  "
        lines.append(f"  [{kind}] {entry.name}")
    if len(entries) > 50:
        lines.append(f"  ... and {len(entries) - 50} more")
    return "\n".join(lines)


def create_file(argument: str = "") -> str:
    name = argument.strip()
    if not name:
        return "Give me a file name, e.g. 'create file notes.txt'."
    path = Path(name).expanduser()
    if path.exists():
        return f"'{path.name}' already exists -- I didn't touch it."
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
    except OSError as exc:
        return f"I couldn't create that file: {exc.strerror or exc}."
    return f"Created empty file '{path}'."


def create_folder(argument: str = "") -> str:
    name = argument.strip()
    if not name:
        return "Give me a folder name, e.g. 'create folder projects'."
    path = Path(name).expanduser()
    if path.exists():
        return f"'{path.name}' already exists."
    try:
        path.mkdir(parents=True)
    except OSError as exc:
        return f"I couldn't create that folder: {exc.strerror or exc}."
    return f"Created folder '{path}'."


def safe_delete(argument: str = "") -> str:
    name = argument.strip()
    if not name:
        return "Which file or folder should I remove? It stays recoverable either way."
    path = Path(name).expanduser()
    if not path.exists():
        return f"I can't find '{name}'."
    try:
        import send2trash

        send2trash.send2trash(str(path))
        return f"Moved '{path.name}' to the system trash (recoverable)."
    except ImportError:
        pass
    except Exception:
        pass
    ensure_data_dirs()
    stamp = time.strftime("%Y%m%d-%H%M%S")
    destination = TRASH_DIR / f"{stamp}-{path.name}"
    try:
        shutil.move(str(path), str(destination))
    except (OSError, shutil.Error) as exc:
        return f"I couldn't move that: {exc}."
    return f"Moved '{path.name}' to my safe trash folder: {destination}"


def run(argument: str = "") -> str:
    return list_files(argument)
