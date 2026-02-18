"""
AUREON WEB SERVER
==================
100% ASCII -- will NOT crash on Windows cp1252.

Starts aureon_web_interface.py which serves BOTH
the chat HTML UI and the JSON API on one server.
No separate aureon_web_builder needed.

Usage:
    python start_web_server.py
    python start_web_server.py --port 8080
"""
from __future__ import annotations
import os
import sys
from pathlib import Path

BASE_DIR = os.getenv("AUREON_BASE_DIR", r"C:\AUREON_AUTONOMOUS")

# Ensure base dir is on path
if str(Path(BASE_DIR)) not in sys.path:
    sys.path.insert(0, str(Path(BASE_DIR)))

print("=" * 60)
print("  AUREON WEB SERVER")
print("=" * 60)
print("")

# Parse args
host = os.getenv("AUREON_HOST", "127.0.0.1")
port = int(os.getenv("AUREON_PORT", "8000"))

# Check for --port argument
if "--port" in sys.argv:
    try:
        idx = sys.argv.index("--port")
        port = int(sys.argv[idx + 1])
    except (IndexError, ValueError):
        pass

# Import the web interface (which has its own built-in HTML)
try:
    from aureon_web_interface import serve
except ImportError as e:
    print("  [FAIL] Cannot import aureon_web_interface: " + str(e))
    print("")
    print("  Make sure aureon_web_interface.py is in: " + BASE_DIR)
    print("  And that aureon_brain.py is also present.")
    sys.exit(1)

print("  Base directory: " + BASE_DIR)
print("  Starting server on http://" + host + ":" + str(port))
print("  Press Ctrl+C to stop")
print("")

# Open browser
try:
    import webbrowser
    webbrowser.open("http://" + host + ":" + str(port))
    print("  [OK] Opened browser")
except Exception:
    print("  Open manually: http://" + host + ":" + str(port))

print("")

# Start server
try:
    serve(host=host, port=port)
except KeyboardInterrupt:
    print("")
    print("  Shutting down...")
    sys.exit(0)
except Exception as e:
    print("  [FAIL] Server error: " + str(e))
    import traceback
    traceback.print_exc()
    sys.exit(1)
