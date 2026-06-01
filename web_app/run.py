"""Entry point — run with: python web_app/run.py"""
import sys
from pathlib import Path

# Ensure project root is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from web_app.app import app

if __name__ == "__main__":
    host = "0.0.0.0"   # accessible on your LAN so phones can connect
    port = 5000
    print(f"\n  AlocasiaTrack PWA running at  http://localhost:{port}")
    print(f"  On your phone, use  http://<your-PC-IP>:{port}\n")
    app.run(host=host, port=port, debug=True)
