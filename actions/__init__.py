"""Action modules for ULTRON.

Each module exposes a single ``run(argument: str) -> str`` function that
performs one small, well-defined job and returns a human-readable result.
The router in :mod:`core.router` decides which action a request maps to.
"""
