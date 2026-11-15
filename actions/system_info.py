"""Report basic system information.

Uses :mod:`psutil` when it is installed for richer numbers (CPU load,
memory usage); otherwise falls back to standard-library sources so the
command still works on a bare Python install.
"""

from __future__ import annotations

import os
import platform
import shutil


def _with_psutil() -> list[str] | None:
    try:
        import psutil
    except ImportError:
        return None
    memory = psutil.virtual_memory()
    lines = [
        f"CPU usage: {psutil.cpu_percent(interval=0.2):.0f}% "
        f"across {psutil.cpu_count(logical=True)} logical cores",
        f"Memory: {memory.percent:.0f}% used "
        f"({memory.used / 1e9:.1f} GB of {memory.total / 1e9:.1f} GB)",
    ]
    return lines


def run(_argument: str = "") -> str:
    lines = [
        f"System: {platform.system()} {platform.release()} "
        f"({platform.machine()})",
        f"Computer name: {platform.node() or 'unknown'}",
        f"Python: {platform.python_version()}",
        f"Processor: {platform.processor() or platform.machine()}",
    ]
    detailed = _with_psutil()
    if detailed:
        lines.extend(detailed)
    else:
        try:
            load1, load5, _load15 = os.getloadavg()
            lines.append(f"Load average: {load1:.2f} (1 min), {load5:.2f} (5 min)")
        except (AttributeError, OSError):
            pass
    usage = shutil.disk_usage(os.path.expanduser("~"))
    lines.append(
        f"Home disk: {usage.used / 1e9:.1f} GB used of "
        f"{usage.total / 1e9:.1f} GB ({usage.free / 1e9:.1f} GB free)"
    )
    return "\n".join(lines)
