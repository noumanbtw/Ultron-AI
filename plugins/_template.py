"""Template for a ULTRON plugin -- copy this file and make it yours.

A plugin is a single Python file in the ``plugins/`` folder with:

- ``DESCRIPTION``: one line saying what the plugin does.
- ``run(argument)``: receives whatever the user typed after the trigger
  and returns the text ULTRON should say back.

Keep plugins dependency-light and never store secrets in them.
"""

from __future__ import annotations

DESCRIPTION = "Example plugin: echoes back a friendly greeting."


def run(argument: str = "") -> str:
    name = argument.strip() or "there"
    return f"Hello, {name}! This reply came from a ULTRON plugin."
