"""A tiny status dashboard for ULTRON.

Pure standard library: an ``http.server`` page that shows the assistant
is alive, which mode it is in, and a few live system numbers. Run it
with ``python -m dashboard.server`` and open http://127.0.0.1:8765 --
handy for checking ULTRON from your phone on the same network.
"""

from __future__ import annotations

import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from actions import system_info
from core.config import CREDIT, NAME, TAGLINE, VERSION, get_settings

PORT = 8765

_PAGE = """<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>{name} Dashboard</title>
<style>
  body {{ font-family: system-ui, sans-serif; background:#0d1117; color:#e6edf3;
         display:flex; justify-content:center; padding:2rem; }}
  .card {{ max-width:640px; width:100%; background:#161b22; border:1px solid #30363d;
          border-radius:12px; padding:1.5rem 2rem; }}
  h1 {{ margin-bottom:.2rem; }} .tag {{ color:#8b949e; margin-top:0; }}
  pre {{ background:#0d1117; padding:1rem; border-radius:8px; overflow:auto; }}
  .ok {{ color:#3fb950; }} footer {{ color:#8b949e; margin-top:1rem; font-size:.85rem; }}
</style></head>
<body><div class="card">
  <h1>{name}</h1><p class="tag">{tagline}</p>
  <p>Status: <span class="ok">running</span> &middot; Mode: {mode} &middot;
     Version: {version}</p>
  <p>Server time: {time}</p>
  <h3>System</h3><pre>{system}</pre>
  <footer>{credit}</footer>
</div></body></html>"""


def render_page() -> str:
    settings = get_settings()
    return _PAGE.format(
        name=NAME,
        tagline=TAGLINE,
        mode="online (Gemini)" if settings.online else "offline",
        version=VERSION,
        time=datetime.now().strftime("%A, %d %B %Y %I:%M %p"),
        system=system_info.run(),
        credit=CREDIT,
    )


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 (stdlib naming)
        if self.path == "/api/status":
            settings = get_settings()
            body = json.dumps(
                {
                    "name": NAME,
                    "version": VERSION,
                    "online": settings.online,
                    "time": datetime.now().isoformat(timespec="seconds"),
                }
            ).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        body = render_page().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args) -> None:
        pass  # keep the console quiet


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"{NAME} dashboard at http://127.0.0.1:{PORT}  ({CREDIT})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard stopped.")


if __name__ == "__main__":
    main()
