"""
AUREON LAUNCHER
================
100% ASCII -- will NOT crash on Windows cp1252.

Starts browser with debugging port, then boots AUREON web interface.
Run this INSTEAD of aureon_web_interface.py directly.

Usage:
    python aureon_launcher.py
    python aureon_launcher.py --browser edge
    python aureon_launcher.py --no-browser
"""
from __future__ import annotations
import subprocess
import sys
import os
import time
import socket
import argparse
from pathlib import Path


BROWSER_PATHS = {
    "chrome": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
    ],
    "edge": [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ],
}

DEBUG_PORT = 9222
USER_DATA_DIR = os.path.expanduser(r"~\AUREON_BROWSER_PROFILE")


def find_browser(browser_type: str = "chrome") -> str:
    for path in BROWSER_PATHS.get(browser_type, []):
        if os.path.exists(path):
            return path
    fallback = "edge" if browser_type == "chrome" else "chrome"
    for path in BROWSER_PATHS.get(fallback, []):
        if os.path.exists(path):
            print("   [WARN] " + browser_type + " not found, using " + fallback)
            return path
    return ""


def is_port_open(port: int) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex(("127.0.0.1", port)) == 0
    except Exception:
        return False


def launch_browser(browser_path: str) -> subprocess.Popen:
    os.makedirs(USER_DATA_DIR, exist_ok=True)

    cmd = [
        browser_path,
        "--remote-debugging-port=" + str(DEBUG_PORT),
        "--user-data-dir=" + USER_DATA_DIR,
        "--no-first-run",
        "--no-default-browser-check",
        "--start-maximized",
    ]

    print("  [LAUNCH] " + os.path.basename(browser_path))
    print("  Debug port: " + str(DEBUG_PORT))
    print("  Profile: " + USER_DATA_DIR)

    kwargs = {}
    if sys.platform == "win32":
        kwargs["creationflags"] = (subprocess.DETACHED_PROCESS
                                   | subprocess.CREATE_NEW_PROCESS_GROUP)
    return subprocess.Popen(cmd, **kwargs)


def wait_for_browser(timeout: int = 15) -> bool:
    print("  Waiting for browser...", end="", flush=True)
    start = time.time()
    while time.time() - start < timeout:
        if is_port_open(DEBUG_PORT):
            print(" [OK] Connected!")
            return True
        print(".", end="", flush=True)
        time.sleep(1)
    print(" [TIMEOUT]")
    return False


def main():
    parser = argparse.ArgumentParser(description="Launch AUREON with browser control")
    parser.add_argument("--browser", choices=["chrome", "edge"], default="chrome")
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    print("")
    print("=" * 60)
    print("   AUREON AUTONOMOUS LAUNCHER")
    print("=" * 60)
    print("")

    # Step 1: Browser
    if args.no_browser:
        print("  [SKIP] Browser launch (--no-browser)")
    elif is_port_open(DEBUG_PORT):
        print("  [OK] Browser already running on port " + str(DEBUG_PORT))
    else:
        browser_path = find_browser(args.browser)
        if not browser_path:
            print("  [FAIL] No browser found. Install Chrome or Edge.")
            print("  Or start manually:")
            print("    chrome.exe --remote-debugging-port=" + str(DEBUG_PORT))
            sys.exit(1)
        launch_browser(browser_path)
        if not wait_for_browser():
            print("  [WARN] Browser slow to start, continuing anyway...")

    # Step 2: Start AUREON
    print("")
    print("  [BRAIN] Starting AUREON...")
    print("")

    aureon_dir = Path(__file__).parent
    os.chdir(aureon_dir)
    if str(aureon_dir) not in sys.path:
        sys.path.insert(0, str(aureon_dir))

    try:
        import aureon_web_interface
        aureon_web_interface.main()
    except KeyboardInterrupt:
        print("")
        print("  AUREON shutting down.")
    except Exception as e:
        print("  [FAIL] Startup error: " + str(e))
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
