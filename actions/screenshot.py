"""Take a screenshot and save it as a timestamped PNG.

Prefers Pillow's ``ImageGrab``; falls back to the optional ``mss``
package. On a headless machine with neither available it reports that
clearly rather than failing silently.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def run(argument: str = "") -> str:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    folder = Path(argument.strip()).expanduser() if argument.strip() else Path.cwd()
    try:
        folder.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return f"That folder can't be used: {exc.strerror or exc}."
    target = folder / f"ultron-screenshot-{stamp}.png"

    try:
        from PIL import ImageGrab

        image = ImageGrab.grab()
        image.save(target)
        return f"Screenshot saved to {target}"
    except Exception:
        pass

    try:
        import mss

        with mss.mss() as capture:
            capture.shot(output=str(target))
        return f"Screenshot saved to {target}"
    except Exception:
        return (
            "I couldn't capture the screen -- install Pillow "
            "(pip install Pillow) for screenshot support on this machine."
        )
