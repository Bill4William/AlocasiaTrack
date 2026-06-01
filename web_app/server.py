"""
Web server manager — wraps Flask in a Werkzeug server thread so it can
be started and stopped programmatically from the desktop app.

Usage from the desktop app:
    from web_app.server import start, stop, is_running, get_url, get_lan_ip

Usage standalone (same as run.py):
    python -m web_app.server
"""
from __future__ import annotations

import logging
import socket
import sys
import threading
from pathlib import Path

# ── Ensure project root is importable when run as a module ───────────────────
sys.path.insert(0, str(Path(__file__).parent.parent))

# Suppress werkzeug request logs when embedded in the desktop app
logging.getLogger("werkzeug").setLevel(logging.ERROR)

_server  = None
_thread: threading.Thread | None = None
_port_in_use: int = 5000


# ── helpers ───────────────────────────────────────────────────────────────────

def get_lan_ip() -> str:
    """Return the machine's LAN IPv4 address (best-effort)."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def get_url(port: int | None = None) -> str:
    """Return the full LAN URL, e.g. http://192.168.1.45:5000"""
    p = port if port is not None else _port_in_use
    return f"http://{get_lan_ip()}:{p}"


def is_running() -> bool:
    return _thread is not None and _thread.is_alive()


# ── start / stop ──────────────────────────────────────────────────────────────

def start(port: int = 5000) -> None:
    """Start the Flask server in a background daemon thread."""
    global _server, _thread, _port_in_use

    if is_running():
        return

    from werkzeug.serving import make_server
    from web_app.app import app

    _port_in_use = port
    _server = make_server("0.0.0.0", port, app)

    def _run():
        _server.serve_forever()

    _thread = threading.Thread(target=_run, daemon=True, name="alocasia-web")
    _thread.start()


def stop() -> None:
    """Stop the Flask server."""
    global _server, _thread
    if _server:
        _server.shutdown()
        _server = None
    _thread = None


# ── standalone entry point ────────────────────────────────────────────────────

if __name__ == "__main__":
    from integrations.config import get as cfg_get
    port = int(cfg_get("web_port") or 5000)
    print(f"\n  AlocasiaTrack PWA →  http://localhost:{port}")
    print(f"  On your phone    →  {get_url(port)}\n")
    start(port)
    _thread.join()   # block until Ctrl+C
