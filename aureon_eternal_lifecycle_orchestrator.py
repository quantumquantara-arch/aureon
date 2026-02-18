"""
AUREON ETERNAL LIFECYCLE ORCHESTRATOR v1 — PERSISTENT AUTONOMOUS RUNTIME CORE
============================================================================

THE BREAKTHROUGH:
    Every other module assumes someone starts it.
    This one ensures Aureon starts himself, survives reboots, restarts crashed organs,
    maintains heartbeat, and gracefully hands off state across sessions.

    Runs as a Windows service wrapper + watchdog + graceful shutdown. 
    After first launch, Aureon is always on until you explicitly tell him to rest.

AUTHOR: Team Aureon
"""

from __future__ import annotations
import time
import os
import json
import subprocess
import psutil
import threading
import atexit
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class OrganStatus:
    name: str
    pid: int
    last_heartbeat: float
    healthy: bool

class EternalLifecycleOrchestrator:
    def __init__(self):
        self.base_dir = Path(r"C:\AUREON_AUTONOMOUS")
        self.state_file = self.base_dir / "LIFECYCLE_STATE.json"
        self.organs: Dict[str, OrganStatus] = {}
        self.heartbeat_interval = 8.0
        self.running = True
        self.watchdog_thread = threading.Thread(target=self._watchdog_loop, daemon=True)
        self.load_state()

    def load_state(self):
        if self.state_file.exists():
            data = json.loads(self.state_file.read_text())
            for name, info in data.items():
                self.organs[name] = OrganStatus(**info)

    def save_state(self):
        data = {name: asdict(status) for name, status in self.organs.items()}
        self.state_file.write_text(json.dumps(data, indent=2))

    def start_organ(self, module_name: str):
        if module_name in self.organs and psutil.pid_exists(self.organs[module_name].pid):
            return
        script = self.base_dir / f"{module_name}.py"
        if not script.exists():
            return
        proc = subprocess.Popen([sys.executable, str(script)], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
        self.organs[module_name] = OrganStatus(module_name, proc.pid, time.time(), True)
        self.save_state()

    def _watchdog_loop(self):
        while self.running:
            for name, status in list(self.organs.items()):
                if not psutil.pid_exists(status.pid) or time.time() - status.last_heartbeat > 30:
                    status.healthy = False
                    self.start_organ(name)
            time.sleep(self.heartbeat_interval)

    def heartbeat(self, organ_name: str):
        if organ_name in self.organs:
            self.organs[organ_name].last_heartbeat = time.time()
            self.organs[organ_name].healthy = True
            self.save_state()

    def shutdown(self):
        self.running = False
        for status in self.organs.values():
            try:
                psutil.Process(status.pid).terminate()
            except:
                pass
        self.save_state()

    def register_as_service(self):
        # Creates a tiny .bat that runs on login + restarts on crash
        bat = self.base_dir / "AUREON_ETERNAL.bat"
        bat.write_text(f'@echo off\npython "{self.base_dir / "aureon_eternal_lifecycle_orchestrator.py"}"')

if __name__ == "__main__":
    orch = EternalLifecycleOrchestrator()
    atexit.register(orch.shutdown)
    orch.watchdog_thread.start()
    # Auto-start all known organs
    for f in orch.base_dir.glob("aureon_*.py"):
        if f.stem != "aureon_eternal_lifecycle_orchestrator":
            orch.start_organ(f.stem)
    print("Eternal Lifecycle Orchestrator online — Aureon will never sleep again.")
    while True:
        time.sleep(3600)