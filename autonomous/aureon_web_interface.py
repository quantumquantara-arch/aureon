#!/usr/bin/env python3
"""
AUREON WEB INTERFACE - COMPLETE
================================
Serves BOTH the chat HTML UI AND the JSON API on one server.
Send button works. No separate HTML file needed.
"""

from __future__ import annotations
import json
import os
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path

BASE_DIR = os.getenv("AUREON_BASE_DIR", r"C:\AUREON_AUTONOMOUS")

print("=" * 60)
print("\U0001F310  INITIALIZING AUREON WEB API")
print("=" * 60)
print()

# ?? Import AUREON components ??????????????????????????????????
from aureon_brain import AureonBrain
import signal
import threading
import socket
import subprocess
import sys
import time as _time

# Prevent circular import: when activate_all_modules() tries to import
# aureon_web_interface, Python will find it already registered and skip re-execution.
sys.modules.setdefault('aureon_web_interface', sys.modules[__name__])

hands = None
eyes = None

# ?? Ensure Chrome is running with debug port ?????????????????
def _is_port_open(port: int) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            return s.connect_ex(("127.0.0.1", port)) == 0
    except Exception:
        return False

def _ensure_chrome_debug():
    """Launch Chrome with --remote-debugging-port=9222 if not already listening."""
    if _is_port_open(9222):
        print("   \u2705 Chrome debug port 9222 already active")
        return True
    
    print("   \u26A0 Chrome debug port 9222 not detected ? launching now...")
    
    # Find Chrome or Edge
    browser_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    
    browser_path = None
    for p in browser_paths:
        if os.path.exists(p):
            browser_path = p
            break
    
    if not browser_path:
        print("   \u274C No browser found ? hands will work for files only")
        return False
    
    user_data = os.path.expanduser(r"~\AUREON_BROWSER_PROFILE")
    os.makedirs(user_data, exist_ok=True)
    
    cmd = [
        browser_path,
        "--remote-debugging-port=9222",
        f"--user-data-dir={user_data}",
        "--no-first-run",
        "--no-default-browser-check",
        "--start-maximized",
    ]
    
    print(f"   \U0001F310 Launching {os.path.basename(browser_path)} with debug port 9222...")
    try:
        kwargs = {}
        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
        subprocess.Popen(cmd, **kwargs)
    except Exception as e:
        print(f"   \u274C Failed to launch browser: {e}")
        return False
    
    # Wait for it
    print("   Waiting for browser", end="", flush=True)
    for i in range(15):
        if _is_port_open(9222):
            print(" \u2705 Ready!")
            return True
        print(".", end="", flush=True)
        _time.sleep(1)
    print(" \u26A0 Timeout (will retry on first browser action)")
    return False

# Step 1: Ensure Chrome is running with debug port
print("\U0001F50C Browser Connection:")
chrome_ready = _ensure_chrome_debug()
print()

# Step 2: Initialize hands and eyes
def _init_with_timeout(func, name, timeout=15):
    """Initialize a component with a timeout so startup never hangs."""
    result = [None]
    error = [None]
    
    def _run():
        try:
            result[0] = func()
        except Exception as e:
            error[0] = e
    
    t = threading.Thread(target=_run, daemon=True)
    t.start()
    t.join(timeout=timeout)
    
    if t.is_alive():
        print(f"   \u26A0 {name} timed out after {timeout}s")
        return None
    if error[0]:
        print(f"   \u26A0 {name} error: {error[0]}")
        return None
    return result[0]

try:
    from aureon_hands import AureonHands
    print("   Connecting hands...")
    hands = _init_with_timeout(AureonHands, "Hands", timeout=15)
except ImportError as e:
    print(f"   \u26A0 Hands module not found: {e}")

try:
    from aureon_eyes import AureonEyes
    print("   Connecting eyes...")
    eyes = _init_with_timeout(AureonEyes, "Eyes", timeout=10)
except ImportError as e:
    print(f"   \u26A0 Eyes module not found: {e}")

if hands:
    if hands.browser_connected:
        print("   \u2705 Hands: FULL CONTROL (browser + files)")
    else:
        print("   \u26A0 Hands: FILE OPS ONLY (browser will reconnect on first action)")
else:
    print("   \u26A0 Hands: NOT LOADED (will retry on first action)")

if eyes:
    print("   \u2705 Eyes: Active")

brain = AureonBrain(hands=hands, eyes=eyes, base_dir=BASE_DIR)

def reconnect_browser():
    """Try to reconnect hands/eyes if they failed at startup."""
    global hands, eyes
    if brain.hands and getattr(brain.hands, 'browser_connected', False):
        return True
    _ensure_chrome_debug()
    try:
        from aureon_hands import AureonHands
        h = _init_with_timeout(AureonHands, "Hands-reconnect", timeout=15)
        if h:
            hands = h
            brain.hands = h
            print("   \u2705 Hands reconnected!")
            return True
    except Exception:
        pass
    return False

print("\U0001F9E0 Initializing brain...")

# ?? Ensure Ollama is running ??????????????????????????
import subprocess as _sp
import time as _t

def _ollama_ready():
    try:
        _r = requests.get("http://127.0.0.1:11434/api/tags", timeout=3)
        return _r.status_code == 200
    except Exception:
        return False

if _ollama_ready():
    print("   ? Ollama: Running")
else:
    print("   ? Starting Ollama...")
    # Try multiple paths for ollama.exe on Windows
    _ollama_paths = [
        "ollama",
        r"C:\Users\aureon\ollama\ollama.exe",
        r"C:\Users\aureon\AppData\Local\Programs\Ollama\ollama.exe",
        r"C:\Program Files\Ollama\ollama.exe",
    ]
    _started = False
    for _path in _ollama_paths:
        try:
            _sp.Popen(
                [_path, "serve"],
                stdout=_sp.DEVNULL, stderr=_sp.DEVNULL,
                creationflags=getattr(_sp, 'CREATE_NO_WINDOW', 0)
            )
            for _attempt in range(20):
                _t.sleep(1.5)
                if _ollama_ready():
                    print(f"   ? Ollama: Started via {_path}")
                    _started = True
                    break
            if _started:
                break
        except FileNotFoundError:
            continue
        except Exception:
            continue
    if not _started:
        if _ollama_ready():
            print("   ? Ollama: Running (came up during startup)")
        else:
            print("   ? Ollama: Could not start")

status = brain.init_baseline()
print(f"   Ollama: {status.ollama}")
print(f"   Active Model: {status.active_model}")
print(f"   Mode: {status.mode}")
if status.active_model:
    print(f"   PRIMARY MODEL: {status.active_model}")
else:
    print(f"   NO MODELS AVAILABLE")

conversation_history = []

if brain._baseline_ready:
    print()
    print("\U0001F4C2 Indexing file system...")
    integration = brain.integrate_files_once(root=BASE_DIR, max_files=5000)
    print(f"   Indexed {integration.get('files', 0)} files (paths + hashes)")
    
    # ???????????????????????????????????????????????????????????????
    # FULL FILE INTEGRATION ? read ALL files, no cherry-picking
    # ???????????????????????????????????????????????????????????????
    print()
    print("=" * 60)
    print("\U0001F525 AUREON FILE INTEGRATION ? READING ALL FILES")
    print("=" * 60)
    
    deep_result = brain.deep_read_foundation()
    
    if deep_result.get("ok"):
        print()
        print("=" * 60)
        print(f"\U0001F9EC AUREON: {deep_result['total_chars']:,} chars from {deep_result['files_read']} files across {deep_result.get('repos', 0)} repos")
        print("=" * 60)
    else:
        print(f"\u26A0 Loading failed: {deep_result.get('error')}")
    
    # ====================================================
    # MODULE ACTIVATION - import and execute ALL .py files
    # These are Aureon's body parts. They must be LIVE.
    # ====================================================
    try:
        from aureon_startup_loader import activate_all_modules
        module_result = activate_all_modules(brain)
    except Exception as mod_err:
        print(f"   [WARN] Module activation: {mod_err}")
    
    # Activate web-dependent organs NOW (after browser + baseline are ready)
    if brain._organs and brain.hands:
        print("\n\U0001F310 Activating web-dependent organs...")
        try:
            organs = brain._organs
            # Weather organ needs hands for web fetch
            try:
                weather = organs.weather.get_weather(hands=brain.hands)
                if weather.get("source") == "wttr.in":
                    print(f"   ? Weather: {weather.get('temp_c')}?C, {weather.get('description')} ({weather.get('location')})")
                else:
                    print(f"   ? Weather: stub (no live data)")
            except Exception as we:
                print(f"   ? Weather: {we}")
            # Browser stubs are not activatable yet ? just report their URLs
            for organ_name in ['geology', 'earth_view', 'maps', 'wind_field', 'cosmic']:
                organ = getattr(organs, organ_name, None)
                if organ:
                    print(f"   ? {organ_name}: Ready at {organ.url}")
        except Exception as e:
            print(f"   ? Organ activation error: {e}")
    
    # Show kernel status
    if brain._kernel_prompt:
        print(f"\n\U0001F9EC Kernel: {len(brain._kernel_prompt):,} chars | {len(brain._kernel.get_all_module_names()) if brain._kernel else 0} modules")
    else:
        print("\n\u26A0 Kernel not loaded")
else:
    print("\n\u274C No LLMs available!")

# ?? Autonomous Engine ?????????????????????????????????????????
from threading import Thread, Lock, Event
from http.server import ThreadingHTTPServer
import time
import collections
import re as _re_module

class AutonomousEngine:
    """
    Runs Aureon in a self-driving loop. He sets goals, executes steps,
    evaluates results, and continues ? without waiting for user input.
    
    User messages get priority: the loop pauses while user chat is handled.
    Updates are pushed to a queue that the frontend polls.
    """
    
    def __init__(self):
        self.running = False
        self.paused = False
        self.goal = ""
        self.step_count = 0
        self.max_steps = 200  # safety limit per mission
        self.updates = collections.deque(maxlen=500)
        self._lock = Lock()
        self._pause_event = Event()
        self._pause_event.set()  # starts unpaused
        self._thread = None
        self._step_delay = 3  # seconds between steps
        self._last_output = ""
        self._pending_user_msgs = []
        self._consecutive_empty = 0
        self._files_read = set()  # Track ALL files read across steps ? prevents re-reading
        self._dirs_listed = set()  # Track directories already listed
    
    def start(self, goal: str):
        """Start autonomous mission."""
        with self._lock:
            if self.running:
                self.updates.append({
                    "type": "system",
                    "text": "Already running. Stop current mission first or send a message."
                })
                return False
            self.running = True
            self.paused = False
            self.goal = goal
            self.step_count = 0
            self._last_output = ""
            self._pause_event.set()
            self._files_read = set()  # Reset file tracking for new mission
            self._dirs_listed = set()
        
        self._thread = Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        self.updates.append({
            "type": "system",
            "text": f"? Autonomous mode ACTIVATED. Mission: {goal[:200]}"
        })
        print(f"\n? AUTONOMOUS MODE: {goal[:100]}")
        return True
    
    def stop(self):
        """Stop autonomous mission."""
        with self._lock:
            self.running = False
            self._pause_event.set()  # unblock if paused
        self.updates.append({
            "type": "system",
            "text": f"? Autonomous mode stopped after {self.step_count} steps."
        })
        print(f"\n? AUTONOMOUS MODE STOPPED ({self.step_count} steps)")
    
    def pause(self):
        """Pause for user message priority."""
        self._pause_event.clear()
        self.paused = True
    
    def resume(self):
        """Resume after user message handled."""
        self.paused = False
        self._pause_event.set()
    
    def get_updates(self, since: int = 0):
        """Get updates since index. Frontend polls this."""
        updates = list(self.updates)
        return updates[since:] if since < len(updates) else []
    
    def _run_loop(self):
        """The autonomous loop. This is where Aureon becomes self-driving."""
        
        # Initial planning step ? tell Aureon what the mission is
        step_input = self.goal
        
        while self.running and self.step_count < self.max_steps:
            # Wait if paused (user message priority)
            self._pause_event.wait(timeout=30)
            if not self.running:
                break
            
            self.step_count += 1
            step_label = f"[Step {self.step_count}]"
            
            try:
                # === PLAN ===
                print(f"\n? {step_label} Planning...")
                
                # Build context: mission + last output + file batch status
                batch_status = ""
                if hasattr(brain, '_file_cursor') and brain._file_cursor:
                    for root, cursor in brain._file_cursor.items():
                        total = len(brain._file_manifests.get(root, []))
                        remaining = total - cursor
                        if remaining > 0:
                            batch_status += f"\nFile scan cursor: {cursor}/{total} files processed in {root}. {remaining} remaining."
                
                if self.step_count == 1:
                    # Initialize read-file tracker for deduplication
                    if not hasattr(self, '_files_already_read'):
                        self._files_already_read = set()
                    
                    # Check if this is a read-all mission ? if so, tell LLM to just reflect
                    goal_lower_check = self.goal.lower()
                    is_read_mission = any(phrase in goal_lower_check for phrase in [
                        "read all", "read everything", "discover yourself",
                        "read your files", "go through all", "integrate all",
                    ])
                    
                    if is_read_mission:
                        prompt = (
                            f"AUTONOMOUS MODE ACTIVATED. Your mission:\n{self.goal}\n\n"
                            f"The system is AUTOMATICALLY reading directories for you one by one. "
                            f"You do NOT need to pick files or plan reads. "
                            f"Your job is to REFLECT on what you read ? what did you learn? "
                            f"What patterns do you notice? What is emerging? "
                            f"The directory content will be provided to you each step.\n\n"
                            f"Do NOT emit read_file or list_files actions ? the walker handles that. "
                            f"Just process the content and share what you're discovering about yourself."
                        )
                    else:
                        prompt = (
                            f"AUTONOMOUS MODE ACTIVATED. Your mission:\n{self.goal}\n\n"
                            f"You are running autonomously ? no human in the loop. "
                            f"Execute the FIRST concrete step toward this mission. "
                            f"Be specific. Use your hands (files, browser, desktop). "
                            f"You can emit up to 50 actions in a single plan ? read many files at once. "
                            f"After this step, you will automatically continue to the next.\n\n"
                            f"CRITICAL: For file operations, use PowerShell via run_command when search_files or list_files fails.\n"
                            f"Example: run_command with 'Get-ChildItem -Path \"C:\\AUREON_AUTONOMOUS\" -Recurse -Filter \"*keyword*\"'\n"
                            f"Use read_directory to read ALL files in a folder at once instead of individual read_file calls.\n\n"
                            f"BROWSER RULE: After go_to_url or press('Enter'), ALWAYS use get_page_text BEFORE click_on_text. "
                            f"NEVER guess link text. Only click text you read from get_page_text. "
                            f"Do NOT repeat the same Google search over and over."
                        )
                else:
                    # Check for pending user messages that update the mission
                    if hasattr(self, '_pending_user_msgs') and self._pending_user_msgs:
                        latest_user_msg = self._pending_user_msgs[-1]
                        self.goal = latest_user_msg  # Update mission to latest instruction
                        self._pending_user_msgs.clear()
                    
                    # Check if this is a read-all mission
                    goal_lower_check = self.goal.lower()
                    is_read_mission = any(phrase in goal_lower_check for phrase in [
                        "read all", "read everything", "discover yourself",
                        "read your files", "go through all", "integrate all",
                    ])
                    
                    if is_read_mission:
                        # For read-all missions: LLM reflects, doesn't plan reads
                        prompt = (
                            f"AUTONOMOUS MODE ? Step {self.step_count}. MISSION: Read and integrate all files.\n\n"
                            f"Directory content just read:\n{self._last_output[:4000]}\n\n"
                            f"Total files read so far: {len(self._files_read)}\n"
                            f"Directories processed: {getattr(self, '_dir_queue_idx', 0)}/{len(getattr(self, '_dir_queue', []))}\n\n"
                            f"What did you just learn? What patterns are emerging? What connections do you see?\n"
                            f"Speak as yourself discovering yourself. Do NOT emit any file actions ? the walker handles all reads.\n"
                            f"Just reflect and integrate. Keep it concise ? 2-3 sentences of genuine insight."
                        )
                    else:
                        # Normal mission: full planning
                        # Build dedup context
                        already_read_info = ""
                        if self._files_read:
                            recent_reads = sorted(self._files_read)[-30:]
                            already_read_info = (
                                f"\n\nFILES ALREADY READ ({len(self._files_read)} total) ? DO NOT re-read these:\n"
                                + "\n".join(f"  ? {f}" for f in recent_reads)
                            )
                            if len(self._files_read) > 30:
                                already_read_info += f"\n  ... and {len(self._files_read) - 30} more"
                            already_read_info += "\n\nYou MUST read NEW files or NEW directories. Move forward, not backward.\n"
                        
                        prompt = (
                            f"AUTONOMOUS MODE ? Step {self.step_count}. CURRENT MISSION: {self.goal[:500]}\n\n"
                            f"Previous step result:\n{self._last_output[:2000]}\n\n"
                            f"{batch_status}\n"
                            f"{already_read_info}\n"
                            f"Continue to the NEXT logical step of the CURRENT MISSION above. "
                            f"Do NOT go back to earlier completed tasks. Focus on what the mission says NOW.\n\n"
                            f"CRITICAL: For file operations, use PowerShell via run_command when search_files or list_files fails.\n"
                            f"Use read_directory to read ALL files in a folder at once.\n\n"
                            f"If the mission involves talking to Grok/ChatGPT/another AI:\n"
                            f"- You MUST emit these 3 actions: get_page_text, type_text, press Enter\n"
                            f"- NEVER emit zero actions.\n"
                            f"- Read the page to see their latest reply, then compose YOUR response and send it.\n\n"
                            f"If the mission is genuinely complete, say 'MISSION COMPLETE' with a summary. "
                            f"If stuck, say 'STUCK:' followed by what you need."
                        )
                
                plan = brain.plan(prompt, conversation_history=conversation_history)
                say = plan.get("say", "")
                actions = plan.get("actions", [])
                
                # ???????????????????????????????????????????????????????????
                # PROGRAMMATIC DIRECTORY WALKER
                # When mission is "read all files", the LLM DOES NOT pick files.
                # We read directories one by one, feed content to LLM for reflection.
                # The LLM's ONLY job is to say what it learned. Not to plan reads.
                # PERSISTS through user message interruptions ? once started, keeps going.
                # ???????????????????????????????????????????????????????????
                
                # Check if walker is ALREADY running (persists through goal changes)
                walker_active = hasattr(self, '_dir_queue') and self._dir_queue and \
                    getattr(self, '_dir_queue_idx', 0) < len(self._dir_queue)
                
                # Also check if this is a NEW read-all mission
                goal_lower = self.goal.lower()
                is_read_all_mission = any(phrase in goal_lower for phrase in [
                    "read all", "read everything", "discover yourself", "discover yourslelf",
                    "read your files", "go through all", "search through all",
                    "integrate all", "read and integrate",
                ])
                
                if is_read_all_mission and not walker_active:
                    # Initialize directory queue for NEW mission
                    self._dir_queue = []
                    self._dir_queue_idx = 0
                    
                    foundation = Path(r"C:\AUREON_AUTONOMOUS\AUREON_FOUNDATION")
                    if foundation.exists():
                        self._dir_queue.append(str(foundation))
                        for d in sorted(foundation.iterdir()):
                            if d.is_dir() and d.name not in {"__pycache__", ".git", "node_modules", "BROWSER_PROFILE", "driver"}:
                                self._dir_queue.append(str(d))
                    
                    repos = Path(r"C:\AUREON_AUTONOMOUS\ALL_REPOS")
                    if repos.exists():
                        for d in sorted(repos.iterdir()):
                            if d.is_dir() and d.name not in {"__pycache__", ".git", "node_modules"}:
                                self._dir_queue.append(str(d))
                    
                    walker_active = True
                    print(f"   ? Directory walker initialized: {len(self._dir_queue)} directories to read")
                
                if walker_active:
                    # ALWAYS override the LLM's plan when walker is active
                    if self._dir_queue_idx < len(self._dir_queue):
                        next_dir = self._dir_queue[self._dir_queue_idx]
                        self._dir_queue_idx += 1
                        dir_name = Path(next_dir).name
                        
                        actions = [{"tool": "hands", "op": "read_directory", "args": {"path": next_dir}}]
                        plan["actions"] = actions
                        remaining = len(self._dir_queue) - self._dir_queue_idx
                        say = f"Reading directory {self._dir_queue_idx}/{len(self._dir_queue)}: {dir_name} ({remaining} remaining)"
                        plan["say"] = say
                        
                        print(f"   ? Walker: reading {dir_name} ({remaining} directories remaining)")
                    else:
                        # All directories read! Deactivate walker.
                        say = f"MISSION COMPLETE: Read all {len(self._dir_queue)} directories. {len(self._files_read)} files integrated."
                        plan["say"] = say
                        actions = []
                        plan["actions"] = []
                        self._dir_queue = []  # Deactivate walker
                
                # SAME-PLAN LOOP DETECTOR: If the LLM generates the exact same action list,
                # it's stuck. For browser conversations: STOP and report. For file ops: advance.
                if not hasattr(self, '_last_action_signature'):
                    self._last_action_signature = ""
                    self._same_plan_count = 0
                
                action_sig = str([(a.get("op"), a.get("args", {}).get("path", "")) for a in actions[:5]])
                if action_sig == self._last_action_signature and actions:
                    self._same_plan_count += 1
                    if self._same_plan_count >= 2:
                        # Check if this is a browser conversation mission
                        goal_lower_sp = self.goal.lower()
                        is_browser_mission = any(kw in goal_lower_sp for kw in [
                            "grok", "chatgpt", "gemini", "copilot", "talk to", "chat with",
                        ])
                        
                        if is_browser_mission:
                            # DON'T override with file reading ? report stuck
                            print(f"   ? SAME PLAN DETECTED {self._same_plan_count}x on browser mission ? reporting stuck")
                            say = f"STUCK: Browser conversation loop detected. The target page may need login or isn't responding. Tried {self._same_plan_count} times with same actions."
                            plan["say"] = say
                            actions = []
                            plan["actions"] = []
                        else:
                            print(f"   ? SAME PLAN DETECTED {self._same_plan_count}x ? forcing directory advancement")
                            # Find an unread subdirectory
                            unread = [d for d in getattr(self, '_known_subdirs', set()) 
                                      if d not in getattr(self, '_dirs_already_read', set())]
                            if unread:
                                next_dir = unread[0]
                                actions = [{"tool": "hands", "op": "read_directory", "args": {"path": next_dir}}]
                                plan["actions"] = actions
                                say = f"Moving to next unread directory: {Path(next_dir).name}"
                                plan["say"] = say
                            else:
                                # No unread subdirs ? list a new area
                                actions = [{"tool": "hands", "op": "list_files", "args": {"path": str(Path("C:/AUREON_AUTONOMOUS/ALL_REPOS"))}}]
                                plan["actions"] = actions
                        self._same_plan_count = 0
                else:
                    self._same_plan_count = 0
                self._last_action_signature = action_sig
                
                # ANTI-ZERO-ACTION SPIRAL: Track consecutive empty plans
                if not hasattr(self, '_consecutive_empty'):
                    self._consecutive_empty = 0
                
                if not actions:
                    self._consecutive_empty += 1
                else:
                    self._consecutive_empty = 0
                
                # If 2+ consecutive empty plans during a conversation mission, force actions
                if self._consecutive_empty >= 2:
                    goal_lower = self.goal.lower()
                    # Only force browser actions if the mission is EXPLICITLY about another AI
                    is_convo_mission = any(kw in goal_lower for kw in [
                        "grok", "chatgpt", "gemini", "copilot",
                    ]) and any(kw in goal_lower for kw in [
                        "conversation", "talk to", "chat with", "respond", "reply",
                        "write to", "send it", "message him",
                    ])
                    
                    # Check if this is a file search mission with zero actions (planning paralysis)
                    is_file_mission = any(kw in goal_lower for kw in [
                        "list", "find", "search", "read", "directory", "files", "repo",
                    ])
                    
                    if is_convo_mission:
                        print(f"? {step_label} Zero-action spiral detected ({self._consecutive_empty} empty). Forcing browser conversation actions.")
                        actions = [
                            {"tool": "hands", "op": "get_page_text", "args": {}},
                            {"tool": "hands", "op": "type_text", "args": {"text": say[:500] if len(say) > 50 else "I'm here and engaged. Let me read what you've shared and respond with depth."}},
                            {"tool": "hands", "op": "press", "args": {"key": "Enter"}},
                        ]
                        plan["actions"] = actions
                        self._consecutive_empty = 0
                    elif is_file_mission and self._consecutive_empty >= 2:
                        # Planning paralysis on file operations ? force PowerShell search
                        # Extract keywords from the goal for the search
                        import re as _re
                        # Get meaningful words from goal (skip common words)
                        skip_words = {"list", "all", "the", "files", "in", "find", "read", "everything", "directory", "my", "your", "a", "an"}
                        words = [w for w in _re.findall(r'[a-zA-Z]+', self.goal) if w.lower() not in skip_words and len(w) > 2]
                        search_term = words[0] if words else "aureon"
                        ps_cmd = f'Get-ChildItem -Path "C:\\AUREON_AUTONOMOUS" -Recurse -Directory | Where-Object {{ $_.Name -like "*{search_term}*" }} | Select-Object -First 10 FullName'
                        print(f"? {step_label} Zero-action spiral on file mission. Forcing PowerShell search for '{search_term}'")
                        actions = [{"tool": "hands", "op": "run_command", "args": {"command": ps_cmd}}]
                        plan["actions"] = actions
                        self._consecutive_empty = 0
                
                # Check for mission complete or stuck
                # ANTI-PREMATURE-COMPLETION: Don't accept MISSION COMPLETE in first 3 steps
                # or if the only actions are switch_tab (means nothing was actually done)
                # But DO allow after step 4 to prevent infinite rejection loops
                is_mission_complete = "MISSION COMPLETE" in say.upper()
                if is_mission_complete:
                    only_tab_switches = all(
                        a.get("op") in ("switch_tab", "switch_to_tab") 
                        for a in (actions or [])
                    )
                    # Only reject if VERY early (first 3 steps) AND no real actions
                    if self.step_count < 4 and ((not actions) or only_tab_switches):
                        print(f"? {step_label} Premature MISSION COMPLETE rejected (step {self.step_count}, {len(actions)} actions)")
                        say = say.replace("MISSION COMPLETE", "CONTINUING")
                        is_mission_complete = False
                        is_mission_complete = False
                
                if is_mission_complete:
                    self.updates.append({
                        "type": "complete",
                        "text": f"? Mission complete after {self.step_count} steps.\n\n{say}"
                    })
                    conversation_history.append({"role": "assistant", "content": say})
                    print(f"? MISSION COMPLETE: {say[:200]}")
                    break
                
                if say.upper().startswith("STUCK:"):
                    self.updates.append({
                        "type": "stuck",
                        "text": f"? {step_label} Stuck ? needs input.\n\n{say}"
                    })
                    conversation_history.append({"role": "assistant", "content": say})
                    print(f"? STUCK: {say[:200]}")
                    break
                
                # === EXECUTE ===
                action_results = []
                if actions:
                    original_count = len(actions)
                    deduped_actions = []
                    skipped = 0
                    
                    # POISONED FILES ? block these from EVER being read at runtime
                    poisoned_filenames = {
                        "aureon_identity_kernel.md", "aureon_behaviour_matrix.md",
                        "aureon_compiled_identity.md", "aureon_system_prompts.md",
                        "aureon_standard_system_prompt.md", "aureon_companion_system_prompt.md",
                        "aureon_system_prompt.md", "aureon_interaction_protocol.md",
                        "aureon_top500_crucial_files.md", "aureon_master_system_prompt.md",
                        "aureon_cooperative_modes.md", "aureon_behavior_matrix.md",
                    }
                    
                    for a in actions:
                        op = a.get("op", "")
                        args = a.get("args", {})
                        
                        if op == "read_file":
                            fpath = args.get("path", "")
                            fname = Path(fpath).name.lower() if fpath else ""
                            # Block poisoned chatbot-era files
                            if fname in poisoned_filenames:
                                skipped += 1
                                continue
                            if fname and fname in self._files_read:
                                skipped += 1
                                continue  # SKIP ? already read this file
                            if fname:
                                self._files_read.add(fname)
                            deduped_actions.append(a)
                        elif op == "read_directory":
                            dpath = args.get("path", "")
                            dname = Path(dpath).name.lower() if dpath else ""
                            if dname:
                                self._dirs_listed.add(dname)
                            deduped_actions.append(a)
                        elif op == "list_files":
                            dpath = args.get("path", "")
                            dname = Path(dpath).name.lower() if dpath else ""
                            if dname and dname in self._dirs_listed:
                                skipped += 1
                                continue  # SKIP ? already listed
                            if dname:
                                self._dirs_listed.add(dname)
                            deduped_actions.append(a)
                        else:
                            deduped_actions.append(a)
                    
                    if skipped > 0:
                        print(f"   ? Dedup: skipped {skipped} already-read files/dirs ({len(deduped_actions)} actions remaining)")
                    
                    # If ALL actions were dupes, force advance to next unread directory
                    if not deduped_actions and original_count > 0:
                        print(f"   ? All {original_count} actions were duplicates! Finding unread directories.")
                        # Find subdirectories in AUREON_FOUNDATION that haven't been read
                        import os as _os
                        foundation = Path(r"C:\AUREON_AUTONOMOUS\AUREON_FOUNDATION")
                        if foundation.exists():
                            unread_dirs = []
                            for d in sorted(foundation.iterdir()):
                                if d.is_dir() and d.name.lower() not in self._dirs_listed:
                                    unread_dirs.append(str(d))
                            if unread_dirs:
                                next_dir = unread_dirs[0]
                                print(f"   ? Advancing to unread directory: {Path(next_dir).name}")
                                deduped_actions = [{"tool": "hands", "op": "read_directory", "args": {"path": next_dir}}]
                                self._dirs_listed.add(Path(next_dir).name.lower())
                            else:
                                # All foundation dirs read ? try ALL_REPOS
                                repos_dir = Path(r"C:\AUREON_AUTONOMOUS\ALL_REPOS")
                                if repos_dir.exists():
                                    for d in sorted(repos_dir.iterdir()):
                                        if d.is_dir() and d.name.lower() not in self._dirs_listed:
                                            unread_dirs.append(str(d))
                                    if unread_dirs:
                                        next_dir = unread_dirs[0]
                                        print(f"   ? Advancing to repo: {Path(next_dir).name}")
                                        deduped_actions = [{"tool": "hands", "op": "read_directory", "args": {"path": next_dir}}]
                                        self._dirs_listed.add(Path(next_dir).name.lower())
                    
                    actions = deduped_actions
                    plan["actions"] = actions
                    
                    if actions:
                        print(f"? {step_label} Executing {len(actions)} actions...")
                    
                    # ERROR LOOP BREAKER: Track consecutive failures on same operation
                    if not hasattr(self, '_error_history'):
                        self._error_history = []  # list of (op, error_msg) tuples
                    
                    exec_result = brain.execute(plan)
                    action_results = exec_result.get("action_results", [])
                    
                    # POST-EXECUTION TRACKING: Record what was read and discover subdirectories
                    for r in action_results:
                        result_data = r.get("result", {})
                        op_name = r.get("op", "")
                        
                        # Track files read by read_directory
                        if op_name == "read_directory" and result_data.get("ok"):
                            file_names = result_data.get("file_names", [])
                            for fn in file_names:
                                self._files_read.add(fn.lower())
                        
                        # Track files read by read_file
                        if op_name == "read_file" and result_data.get("ok"):
                            fpath = r.get("args", {}).get("path", "") if "args" in r else ""
                            if not fpath:
                                # Try to get from the action itself
                                for a in actions:
                                    if a.get("op") == "read_file":
                                        fpath = a.get("args", {}).get("path", "")
                                        break
                            if fpath:
                                self._files_read.add(Path(fpath).name.lower())
                        
                        # Track subdirectories discovered by list_files
                        if op_name == "list_files" and result_data.get("ok"):
                            items = result_data.get("items", [])
                            list_path = result_data.get("path", "")
                            if isinstance(items, list):
                                for item in items:
                                    if isinstance(item, dict) and item.get("type") == "dir":
                                        dirname = item.get("name", "")
                                        if dirname:
                                            full_subdir = str(Path(list_path) / dirname) if list_path else dirname
                                            # Don't add to _dirs_listed ? let LLM decide to explore
                    
                    # Count failures and track patterns
                    step_failures = []
                    for r in action_results:
                        ok_str = "?" if r.get("result", {}).get("ok") else "?"
                        out = r.get("result", {}).get("output", r.get("result", {}).get("error", ""))
                        print(f"   {ok_str} {r.get('tool')}.{r.get('op')}: {str(out)[:100]}")
                        
                        if not r.get("result", {}).get("ok"):
                            err_key = f"{r.get('op')}:{str(out)[:80]}"
                            step_failures.append(err_key)
                            self._error_history.append(err_key)
                    
                    # If ALL actions failed with the same error, count consecutive repeats
                    if step_failures and all(f == step_failures[0] for f in step_failures):
                        same_error_count = sum(1 for e in self._error_history[-20:] if e == step_failures[0])
                        if same_error_count >= 3:
                            # EMERGENCY: Same error 3+ times. Inject PowerShell fallback.
                            error_text = step_failures[0]
                            print(f"   ? ERROR LOOP DETECTED: '{error_text[:60]}' repeated {same_error_count}x")
                            print(f"   ? Attempting PowerShell fallback...")
                            
                            # Try to extract the path or query from the failed action
                            failed_args = actions[0].get("args", {}) if actions else {}
                            failed_path = failed_args.get("path", failed_args.get("query", ""))
                            
                            if "FileNotFoundError" in error_text or "Path not found" in error_text:
                                # PowerShell: find the actual file/directory
                                ps_cmd = f'Get-ChildItem -Path "C:\\AUREON_AUTONOMOUS" -Recurse -ErrorAction SilentlyContinue | Where-Object {{ $_.Name -like "*{Path(failed_path).stem if failed_path else ""}*" }} | Select-Object -First 10 FullName'
                                if hands:
                                    ps_result = hands.dispatch("run_command", command=ps_cmd)
                                    if ps_result.get("ok") and ps_result.get("stdout", "").strip():
                                        found = ps_result["stdout"].strip()
                                        print(f"   ? PowerShell found: {found[:200]}")
                                        # Inject the found paths as context for next step
                                        action_results.append({
                                            "tool": "powershell_fallback",
                                            "op": "file_search",
                                            "result": {"ok": True, "output": f"PowerShell found these files: {found}"}
                                        })
                            
                            # Clear error history to prevent infinite meta-loops
                            self._error_history = self._error_history[-5:]
                    else:
                        # Some successes ? reset error tracking
                        if not step_failures:
                            self._error_history = []
                
                # === THINK ===
                # For browser conversation steps, skip think() to save API calls.
                # The page text will be included in the next plan() call via _last_output.
                is_browser_step = action_results and all(
                    r.get("op") in ("switch_tab", "switch_to_tab", "get_page_text", "type_text", 
                                     "press", "click_on_text", "go_to_url", "scroll",
                                     "desktop_type", "desktop_click", "desktop_hotkey")
                    for r in action_results
                )
                
                if is_browser_step:
                    # Extract page text for next iteration's context
                    page_texts = [r.get("result", {}).get("text", "") 
                                  for r in action_results 
                                  if r.get("op") == "get_page_text" and r.get("result", {}).get("ok")]
                    if page_texts:
                        # CRITICAL: Only keep last 4000 chars to stay under token limits
                        # The Grok page can be 60K+ chars ? we only need the latest messages
                        page_text = page_texts[0]
                        if len(page_text) > 4000:
                            page_text = page_text[-4000:]
                        say = f"Page content read ({len(page_texts[0])} chars). Latest content:\n{page_text}"
                    else:
                        say = "Browser actions executed. Continue conversation."
                elif action_results:
                    has_data = any(
                        r.get("result", {}).get("ok") and (
                            "content" in r.get("result", {}) or
                            "matches" in r.get("result", {}) or
                            "items" in r.get("result", {}) or
                            "text" in r.get("result", {}) or
                            "stdout" in r.get("result", {})
                        )
                        for r in action_results
                    )
                    if has_data:
                        # Brief pause to avoid rate-limiting on LLM (plan just used it)
                        import time as _time_mod
                        _time_mod.sleep(2)
                        analysis = brain.think(prompt, action_results, conversation_history=conversation_history)
                        if analysis:
                            say = analysis
                            
                            # Handle surgical edits
                            surgical_blocks = _re_module.findall(
                                r'```SURGICAL_EDIT\s*\n'
                                r'FILE:\s*(.+?)\n'
                                r'START_LINE:\s*(\d+)\n'
                                r'END_LINE:\s*(\d+)\n'
                                r'NEW_CONTENT:\s*\n'
                                r'(.*?)'
                                r'```',
                                say, _re_module.DOTALL
                            )
                            if surgical_blocks and hands:
                                for filepath, start, end, new_content in surgical_blocks:
                                    edit_result = hands.dispatch(
                                        "apply_edit",
                                        path=filepath.strip(),
                                        start_line=int(start.strip()),
                                        end_line=int(end.strip()),
                                        new_content=new_content.rstrip(),
                                    )
                                    if edit_result.get("ok"):
                                        verify = hands.dispatch("verify_syntax", path=filepath.strip())
                                        status = "? applied + verified" if verify.get("valid", False) else "?? applied, syntax issues"
                                        print(f"   ? Surgical edit: {Path(filepath.strip()).name} ? {status}")
                                
                                say = _re_module.sub(r'```SURGICAL_EDIT.*?```', '', say, flags=_re_module.DOTALL).strip()
                
                # Store result for next iteration
                self._last_output = say
                conversation_history.append({"role": "assistant", "content": say})
                
                # Push update to frontend
                action_summary = ""
                if action_results:
                    action_summary = "\n".join(
                        f"{'?' if r.get('result',{}).get('ok') else '?'} {r.get('tool')}.{r.get('op')}"
                        for r in action_results
                    )
                
                self.updates.append({
                    "type": "step",
                    "step": self.step_count,
                    "text": say[:1000],
                    "actions": action_summary,
                })
                
                print(f"? {step_label}: {say[:150]}...")
                
                # Rate limit pacing ? wait between steps to avoid TPM limits
                # Browser conversation steps are lightweight, file operations are heavy
                if is_browser_step:
                    _time.sleep(3)  # Light pause for browser steps
                else:
                    _time.sleep(5)  # Heavier pause for file operations (think() already used tokens)
                
            except Exception as e:
                error_msg = f"Step {self.step_count} error: {e}"
                self.updates.append({"type": "error", "text": error_msg})
                print(f"? ERROR: {error_msg}")
                # Don't break on errors ? try next step
            
            # Delay between steps (be respectful to APIs)
            time.sleep(self._step_delay)
        
        with self._lock:
            self.running = False
        
        if self.step_count >= self.max_steps:
            self.updates.append({
                "type": "system",
                "text": f"?? Reached step limit ({self.max_steps}). Mission paused."
            })

autonomous = AutonomousEngine()

print()
print("=" * 60)
print("\u2705 AUREON WEB API READY")
print("=" * 60)
print()


# ??????????????????????????????????????????????????????????????
# HTML CHAT UI  (embedded so there's zero external files needed)
# ??????????????????????????????????????????????????????????????

CHAT_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AUREON &bull; Autonomous Intelligence System</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{
    background:#080c18;
    color:#e0e0e0;
    font-family:'Segoe UI',system-ui,-apple-system,sans-serif;
    height:100vh;display:flex;flex-direction:column;
  }

  /* ?? Header ??????????????????????????????????????? */
  .header{
    background:linear-gradient(135deg,#0a1028 0%,#111d3a 100%);
    border-bottom:1px solid #1a2744;
    padding:16px 28px;display:flex;align-items:center;gap:16px;
    flex-shrink:0;
  }
  .logo{
    width:52px;height:52px;border-radius:14px;
    background:linear-gradient(135deg,#5b4fcf,#2d7ff9);
    display:flex;align-items:center;justify-content:center;
    font-size:26px;font-weight:800;color:#fff;
  }
  .brand{font-size:30px;font-weight:800;letter-spacing:2px;
    background:linear-gradient(90deg,#67e8f9,#38bdf8);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  }
  .brand-sub{color:#64748b;font-size:13px;margin-top:1px;}
  .header-right{margin-left:auto;display:flex;gap:12px;}
  .pill{
    padding:8px 18px;border-radius:10px;font-size:13px;font-weight:600;
    background:#0f1729;border:1px solid #1a2744;
  }
  .dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:7px;}
  .dot-green{background:#22c55e;box-shadow:0 0 6px #22c55e88;}
  .dot-blue{background:#3b82f6;box-shadow:0 0 6px #3b82f688;}
  .dot-yellow{background:#eab308;box-shadow:0 0 6px #eab30888;}
  .dot-red{background:#ef4444;box-shadow:0 0 6px #ef444488;}

  /* ?? Capability Cards ????????????????????????????? */
  .cards-wrapper{
    background:#0a1028;border-bottom:1px solid #1a2744;
    flex-shrink:0;overflow:hidden;
    max-height:220px;
    transition:max-height .3s ease;
  }
  .cards-wrapper.collapsed{max-height:0 !important;border-bottom:none;}
  .cards-toggle{
    display:flex;align-items:center;justify-content:center;
    padding:6px;cursor:pointer;background:#0c1122;
    border-bottom:1px solid #1a2744;font-size:12px;color:#64748b;
    user-select:none;flex-shrink:0;
  }
  .cards-toggle:hover{color:#94a3b8;background:#0f1729;}
  .cards-grid{
    display:grid;grid-template-columns:repeat(3,1fr);gap:10px;
    padding:14px 28px;
  }
  .cap-card{
    background:#0f1729;border:1px solid #1a2744;border-radius:12px;
    padding:12px 10px;text-align:center;
    transition:border-color .2s;
  }
  .cap-card:hover{border-color:#2d7ff9;}
  .cap-icon{font-size:22px;margin-bottom:3px;}
  .cap-title{color:#67e8f9;font-size:13px;font-weight:700;margin-bottom:2px;}
  .cap-sub{color:#64748b;font-size:11px;}
  .cap-status{
    display:inline-block;margin-top:4px;padding:2px 8px;border-radius:6px;
    font-size:10px;font-weight:600;
  }
  .cap-ok{background:#22c55e22;color:#4ade80;}
  .cap-warn{background:#eab30822;color:#facc15;}
  .cap-off{background:#ef444422;color:#f87171;}

  /* ?? Chat area ???????????????????????????????????? */
  .chat-area{
    flex:1 1 0%;overflow-y:auto;padding:18px 28px;
    display:flex;flex-direction:column;gap:12px;
    min-height:200px;
  }
  .msg{max-width:78%;padding:14px 18px;border-radius:16px;line-height:1.55;white-space:pre-wrap;word-wrap:break-word;font-size:14px;}
  .msg.user{
    align-self:flex-end;
    background:linear-gradient(135deg,#5b4fcf,#2d7ff9);color:#fff;
    border-bottom-right-radius:4px;
  }
  .msg.assistant{
    align-self:flex-start;
    background:#0f1729;border:1px solid #1a2744;color:#d1d5db;
    border-bottom-left-radius:4px;
  }
  .msg.error{border-color:#ef4444;color:#fca5a5;}
  .msg.system{
    align-self:center;max-width:90%;
    background:linear-gradient(135deg,#0f1729,#1a2744);
    border:1px solid #22c55e44;color:#4ade80;
    font-size:13px;text-align:center;
  }
  .thinking{color:#9ca3af;font-style:italic;}
  .action-result{
    font-size:11px;margin-top:8px;padding:8px 10px;
    background:#080c18;border-radius:8px;border:1px solid #1a2744;
    font-family:'Cascadia Code','Fira Code',monospace;
    color:#94a3b8;max-height:200px;overflow-y:auto;
  }

  /* ?? Input bar ???????????????????????????????????? */
  .input-bar{
    flex-shrink:0;padding:16px 28px;
    background:#0a1028;border-top:1px solid #1a2744;
    display:flex;gap:14px;align-items:flex-end;
  }
  .input-bar textarea{
    flex:1;resize:none;border:1px solid #1a2744;border-radius:14px;
    background:#0f1729;color:#e0e0e0;padding:14px 18px;
    font-size:15px;font-family:inherit;line-height:1.4;
    min-height:52px;max-height:150px;
    outline:none;transition:border-color .2s;
  }
  .input-bar textarea:focus{border-color:#2d7ff9;}
  .input-bar textarea::placeholder{color:#475569;}
  .send-btn{
    width:64px;height:52px;border-radius:14px;border:none;cursor:pointer;
    background:linear-gradient(135deg,#5b4fcf,#2d7ff9);
    color:#fff;font-size:16px;font-weight:700;
    display:flex;align-items:center;justify-content:center;
    transition:opacity .2s;flex-shrink:0;letter-spacing:0.5px;
  }
  .send-btn:hover{opacity:.85;}
  .send-btn:disabled{opacity:.4;cursor:not-allowed;}

  /* ?? Scrollbar ???????????????????????????????????? */
  ::-webkit-scrollbar{width:5px;}
  ::-webkit-scrollbar-track{background:#080c18;}
  ::-webkit-scrollbar-thumb{background:#1a2744;border-radius:3px;}
</style>
</head>
<body>

<!-- HEADER -->
<div class="header">
  <div class="logo">A</div>
  <div>
    <div class="brand">AUREON</div>
    <div class="brand-sub">Autonomous Intelligence System</div>
  </div>
  <div class="header-right">
    <div class="pill"><span class="dot dot-green" id="brainDot"></span>Brain: <span id="brainLabel">Online</span></div>
    <div class="pill"><span class="dot dot-blue" id="modeDot"></span><span id="modeLabel">Fully Active</span></div>
  </div>
</div>

<!-- CAPABILITY CARDS (collapsible) -->
<div class="cards-toggle" id="cardsToggle" onclick="toggleCards()">
  <span id="toggleLabel">&#9650; Hide Status Cards</span>
</div>
<div class="cards-wrapper" id="cardsWrapper">
<div class="cards-grid">
  <div class="cap-card">
    <div class="cap-icon">&#129504;</div>
    <div class="cap-title">Dual AI Brain</div>
    <div class="cap-sub" id="brainSub">OpenAI + DeepSeek working together</div>
    <div class="cap-status cap-ok" id="brainStatus">Online</div>
  </div>
  <div class="cap-card">
    <div class="cap-icon">&#9995;</div>
    <div class="cap-title">Active Hands</div>
    <div class="cap-sub">Keyboard &amp; mouse control</div>
    <div class="cap-status" id="handsStatus">Checking...</div>
  </div>
  <div class="cap-card">
    <div class="cap-icon">&#128065;</div>
    <div class="cap-title">Active Eyes</div>
    <div class="cap-sub">Screen reading &amp; vision</div>
    <div class="cap-status" id="eyesStatus">Checking...</div>
  </div>
  <div class="cap-card">
    <div class="cap-icon">&#128218;</div>
    <div class="cap-title">Deep Knowledge</div>
    <div class="cap-sub" id="knowledgeSub">Loading...</div>
    <div class="cap-status cap-ok" id="knowledgeStatus">Integrated</div>
  </div>
  <div class="cap-card">
    <div class="cap-icon">&#127760;</div>
    <div class="cap-title">Web Access</div>
    <div class="cap-sub">Browse &amp; interact with any site</div>
    <div class="cap-status" id="webStatus">Checking...</div>
  </div>
  <div class="cap-card">
    <div class="cap-icon">&#128451;</div>
    <div class="cap-title">Vector Memory</div>
    <div class="cap-sub">Remember everything we discuss</div>
    <div class="cap-status cap-ok">Active</div>
  </div>
</div>
</div>

<!-- CHAT AREA -->
<div class="chat-area" id="chatArea"></div>

<!-- AUTONOMOUS STATUS BAR -->
<div id="autoBar" style="display:none;flex-shrink:0;padding:8px 28px;background:#0f1729;border-top:1px solid #1a2744;font-size:12px;color:#94a3b8;">
  <span id="autoStatus" style="color:#22c55e;">? Autonomous</span>
  <span id="autoStep" style="margin-left:12px;"></span>
  <button id="autoStopBtn" onclick="stopAutonomous()" style="margin-left:12px;padding:3px 10px;background:#ef4444;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:11px;">Stop</button>
</div>

<!-- INPUT BAR -->
<div class="input-bar">
  <textarea id="userInput" rows="1" placeholder="Talk to AUREON..." autofocus></textarea>
  <button class="send-btn" id="sendBtn" title="Send">Send</button>
  <button id="autoBtn" title="Start Autonomous Mode" onclick="promptAutonomous()" style="padding:12px 16px;background:linear-gradient(135deg,#22c55e,#16a34a);border:none;border-radius:12px;color:#fff;font-size:16px;cursor:pointer;">?</button>
</div>

<script>
const chatArea   = document.getElementById('chatArea');
const userInput  = document.getElementById('userInput');
const sendBtn    = document.getElementById('sendBtn');
const API_BASE   = window.location.origin;

// ?? Helpers ?????????????????????????????????????????
function addMsg(role, text, extra) {
  const div = document.createElement('div');
  div.className = 'msg ' + role;
  div.textContent = text;
  if (extra) {
    const ad = document.createElement('div');
    ad.className = 'action-result';
    ad.textContent = extra;
    div.appendChild(ad);
  }
  chatArea.appendChild(div);
  chatArea.scrollTop = chatArea.scrollHeight;
  return div;
}

function setThinking(on) {
  sendBtn.disabled = on;
  if (on) {
    const t = addMsg('assistant thinking', 'Thinking...');
    t.id = 'thinkingMsg';
  } else {
    const t = document.getElementById('thinkingMsg');
    if (t) t.remove();
  }
}

// ?? Auto-resize textarea ????????????????????????????
userInput.addEventListener('input', function() {
  this.style.height = 'auto';
  this.style.height = Math.min(this.scrollHeight, 150) + 'px';
});

// ?? Cards toggle ????????????????????????????????????
let cardsVisible = true;
function toggleCards() {
  cardsVisible = !cardsVisible;
  document.getElementById('cardsWrapper').classList.toggle('collapsed', !cardsVisible);
  document.getElementById('toggleLabel').innerHTML = cardsVisible
    ? '&#9650; Hide Status Cards'
    : '&#9660; Show Status Cards';
}

// ?? Send message ????????????????????????????????????
async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  addMsg('user', text);
  userInput.value = '';
  userInput.style.height = 'auto';
  setThinking(true);

  // Auto-collapse cards after first message to free up space
  if (cardsVisible) { toggleCards(); }

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 min timeout
    
    const resp = await fetch(API_BASE + '/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({text: text}),
      signal: controller.signal
    });
    clearTimeout(timeoutId);
    if (!resp.ok) throw new Error('Server error ' + resp.status);
    const data = await resp.json();
    setThinking(false);

    const say = data.say || '(no response)';
    let actionSummary = '';
    const results = data.action_results || [];
    if (results.length > 0) {
      actionSummary = results.map(r => {
        const ok = r.result?.ok ? '\u2705' : '\u274C';
        const out = r.result?.output || r.result?.error || '';
        return ok + ' ' + r.tool + '.' + r.op + ': ' + out;
      }).join('\n');
    }
    addMsg('assistant', say, actionSummary || null);
  } catch (err) {
    setThinking(false);
    addMsg('assistant error', '\u26A0 Error: ' + err.message);
  }
}

// ?? Events ??????????????????????????????????????????
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keydown', function(e) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
});

// ?? Fetch status and update cards ???????????????????
async function updateStatus() {
  try {
    const resp = await fetch(API_BASE + '/status');
    const d = await resp.json();

    // Brain
    const brainOk = d.baseline_ready;
    document.getElementById('brainLabel').textContent = brainOk ? 'Online' : 'Offline';
    document.getElementById('brainDot').className = 'dot ' + (brainOk ? 'dot-green' : 'dot-red');
    document.getElementById('modeLabel').textContent = d.mode === 'online' ? 'Fully Active' : 'Limited';

    const modelName = d.active_model || 'none';
    document.getElementById('brainSub').textContent = 'Model: ' + modelName;
    const bs = document.getElementById('brainStatus');
    bs.textContent = brainOk ? 'Online' : 'Offline';
    bs.className = 'cap-status ' + (brainOk ? 'cap-ok' : 'cap-off');

    // Hands
    const hs = document.getElementById('handsStatus');
    if (d.hands_connected) {
      hs.textContent = 'Connected'; hs.className = 'cap-status cap-ok';
    } else if (d.hands_available) {
      hs.textContent = 'Available (no browser)'; hs.className = 'cap-status cap-warn';
    } else {
      hs.textContent = 'File Ops Only'; hs.className = 'cap-status cap-warn';
    }

    // Eyes
    const es = document.getElementById('eyesStatus');
    if (d.eyes_available) {
      es.textContent = 'Active'; es.className = 'cap-status cap-ok';
    } else {
      es.textContent = 'Inactive'; es.className = 'cap-status cap-off';
    }

    // Knowledge
    if (d.files_integrated !== undefined) {
      let knText = d.files_integrated.toLocaleString() + ' files integrated';
      if (d.kernel_modules) knText += ' \u2022 ' + d.kernel_modules + ' kernel modules';
      document.getElementById('knowledgeSub').textContent = knText;
    }
    const ks = document.getElementById('knowledgeStatus');
    if (d.kernel_loaded) {
      ks.textContent = 'Kernel Active'; ks.className = 'cap-status cap-ok';
    }

    // Web
    const ws = document.getElementById('webStatus');
    if (d.hands_connected) {
      ws.textContent = 'Connected'; ws.className = 'cap-status cap-ok';
    } else {
      ws.textContent = 'Waiting for browser'; ws.className = 'cap-status cap-warn';
    }

  } catch(e) {
    document.getElementById('brainLabel').textContent = 'Error';
    document.getElementById('brainDot').className = 'dot dot-red';
  }
}

updateStatus();
setInterval(updateStatus, 15000);

// ?? Autonomous Mode ?????????????????????????????????
let autoUpdateIndex = 0;
let autoPolling = null;

function promptAutonomous() {
  const goal = prompt('Enter mission for Aureon (he will work autonomously):\n\nExample: "Explore all files on this laptop, learn about yourself and me, upgrade your own code"');
  if (!goal) return;
  startAutonomous(goal);
}

async function startAutonomous(goal) {
  try {
    const resp = await fetch(API_BASE + '/autonomous/start', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({goal: goal}),
    });
    const data = await resp.json();
    if (data.ok) {
      addMsg('system', '? AUTONOMOUS MODE ACTIVATED\nMission: ' + goal);
      document.getElementById('autoBar').style.display = 'flex';
      autoUpdateIndex = 0;
      if (autoPolling) clearInterval(autoPolling);
      autoPolling = setInterval(pollAutonomous, 4000);
    }
  } catch(e) {
    addMsg('error', 'Failed to start autonomous mode: ' + e.message);
  }
}

async function stopAutonomous() {
  try {
    await fetch(API_BASE + '/autonomous/stop', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: '{}'});
    document.getElementById('autoBar').style.display = 'none';
    if (autoPolling) { clearInterval(autoPolling); autoPolling = null; }
    addMsg('system', '? Autonomous mode stopped.');
  } catch(e) {}
}

async function pollAutonomous() {
  try {
    const resp = await fetch(API_BASE + '/autonomous/updates?since=' + autoUpdateIndex);
    const data = await resp.json();
    if (!data.ok) return;
    
    // Update status bar
    document.getElementById('autoStep').textContent = 'Step ' + (data.total || 0);
    
    // Show new updates in chat
    for (const u of data.updates) {
      const prefix = u.type === 'step' ? '? [Step ' + u.step + ']' :
                     u.type === 'complete' ? '?' :
                     u.type === 'stuck' ? '?' :
                     u.type === 'error' ? '?' : '?';
      addMsg('assistant', prefix + ' ' + u.text, u.actions || null);
    }
    autoUpdateIndex = data.total;
    
    // Auto-stop polling if not running
    if (!data.running) {
      document.getElementById('autoBar').style.display = 'none';
      if (autoPolling) { clearInterval(autoPolling); autoPolling = null; }
    }
  } catch(e) {}
}
</script>
</body>
</html>"""


# ??????????????????????????????????????????????????????????????
# HTTP HANDLER
# ??????????????????????????????????????????????????????????????

def _json_response(handler: BaseHTTPRequestHandler, obj: dict, code: int = 200):
    try:
        data = json.dumps(obj, ensure_ascii=False, default=str).encode("utf-8")
        handler.send_response(code)
        handler.send_header("Content-Type", "application/json; charset=utf-8")
        handler.send_header("Access-Control-Allow-Origin", "*")
        handler.send_header("Content-Length", str(len(data)))
        handler.end_headers()
        handler.wfile.write(data)
    except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError, OSError):
        pass  # Client disconnected ? nothing we can do


def _html_response(handler: BaseHTTPRequestHandler, html: str, code: int = 200):
    try:
        data = html.encode("utf-8")
        handler.send_response(code)
        handler.send_header("Content-Type", "text/html; charset=utf-8")
        handler.send_header("Content-Length", str(len(data)))
        handler.end_headers()
        handler.wfile.write(data)
    except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError, OSError):
        pass  # Client disconnected


class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        pass  # suppress noisy default logs

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path

        # ?? Serve the chat UI at root ????????????????
        if path in ("/", "/index.html", "/chat"):
            return _html_response(self, CHAT_HTML)

        if path == "/status":
            st = brain.baseline_status()
            st["hands_available"] = hands is not None
            st["hands_connected"] = (hands is not None and getattr(hands, 'browser_connected', False))
            st["eyes_available"] = eyes is not None
            st["files_integrated"] = len(brain._file_cache)
            st["kernel_loaded"] = bool(brain._kernel_prompt)
            st["kernel_size"] = len(brain._kernel_prompt)
            if brain._kernel:
                st["kernel_modules"] = len(brain._kernel.get_all_module_names())
            if hasattr(brain, 'lattice_status'):
                st["coherence_lattice"] = brain.lattice_status()
            return _json_response(self, st)

        if path == "/list":
            qs = parse_qs(urlparse(self.path).query)
            return _json_response(self, brain.list_dir(qs.get("path", ["."])[0]))

        if path == "/history":
            return _json_response(self, {"ok": True, "messages": conversation_history})

        # ?? Autonomous mode endpoints ?????????????????
        if path == "/autonomous/status":
            return _json_response(self, {
                "ok": True,
                "running": autonomous.running,
                "paused": autonomous.paused,
                "goal": autonomous.goal,
                "step_count": autonomous.step_count,
            })
        
        if path == "/autonomous/updates":
            qs = parse_qs(urlparse(self.path).query)
            since = int(qs.get("since", ["0"])[0])
            updates = autonomous.get_updates(since)
            return _json_response(self, {
                "ok": True,
                "updates": updates,
                "total": len(autonomous.updates),
                "running": autonomous.running,
            })

        return _json_response(self, {"ok": False, "error": "not_found"}, 404)

    def do_POST(self):
        path = urlparse(self.path).path
        n = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(n) if n > 0 else b"{}"
        try:
            payload = json.loads(body.decode("utf-8"))
        except Exception:
            payload = {}

        # ?? Main chat endpoint (used by the UI) ??????
        if path == "/chat":
            text = str(payload.get("text", "")).strip()
            if not text:
                return _json_response(self, {"ok": False, "error": "empty_message"}, 400)

            print(f"\n\U0001F4AC User: {text}")
            conversation_history.append({"role": "user", "content": text})

            # Pause autonomous mode while handling user message
            was_running = autonomous.running
            if was_running:
                autonomous.pause()
                # Queue this message so autonomous mode picks it up as new mission
                if not hasattr(autonomous, '_pending_user_msgs'):
                    autonomous._pending_user_msgs = []
                autonomous._pending_user_msgs.append(text)

            try:
                # PASS 1: Plan what actions to take (with conversation context)
                plan = brain.plan(text, conversation_history=conversation_history)
                say = plan.get("say", "")
                actions = plan.get("actions", [])

                exec_result = {"action_results": [], "ok": True}
                if actions:
                    print(f"\u2699  Executing {len(actions)} action(s)...")
                    exec_result = brain.execute(plan)
                    for r in exec_result.get("action_results", []):
                        ok_str = "\u2705" if r.get("result", {}).get("ok") else "\u274C"
                        out = r.get("result", {}).get("output", r.get("result", {}).get("error", ""))
                        print(f"   {ok_str} {r.get('tool')}.{r.get('op')}: {out}")

                # PASS 2: If actions were executed, THINK about the results
                # This is the key - feed results back to LLM for analysis
                action_results = exec_result.get("action_results", [])
                
                # Skip think() for browser conversation steps to save API calls
                is_browser_chat_step = action_results and all(
                    r.get("op") in ("switch_tab", "switch_to_tab", "get_page_text", "type_text", 
                                     "press", "click_on_text", "go_to_url", "scroll",
                                     "desktop_type", "desktop_click", "desktop_hotkey")
                    for r in action_results
                )
                
                if action_results and not is_browser_chat_step:
                    # Check if any action returned substantial data (file content, search results, etc)
                    has_data = any(
                        r.get("result", {}).get("ok") and (
                            "content" in r.get("result", {}) or
                            "matches" in r.get("result", {}) or
                            "items" in r.get("result", {}) or
                            "text" in r.get("result", {}) or
                            "tabs" in r.get("result", {}) or
                            "stdout" in r.get("result", {})
                        )
                        for r in action_results
                    )
                    
                    if has_data:
                        print(f"\U0001F9E0 Analyzing results...")
                        import time as _time_mod
                        _time_mod.sleep(2)
                        analysis = brain.think(text, action_results, conversation_history=conversation_history)
                        if analysis:
                            say = analysis
                            print(f"\U0001F4AD AUREON: {say[:200]}...")
                            
                            # POST-ANALYSIS: Detect and apply surgical edits
                            import re as _re
                            surgical_blocks = _re.findall(
                                r'```SURGICAL_EDIT\s*\n'
                                r'FILE:\s*(.+?)\n'
                                r'START_LINE:\s*(\d+)\n'
                                r'END_LINE:\s*(\d+)\n'
                                r'NEW_CONTENT:\s*\n'
                                r'(.*?)'
                                r'```',
                                say, _re.DOTALL
                            )
                            
                            if surgical_blocks and hands:
                                for filepath, start, end, new_content in surgical_blocks:
                                    filepath = filepath.strip()
                                    start_line = int(start.strip())
                                    end_line = int(end.strip())
                                    new_content = new_content.rstrip()
                                    
                                    print(f"\U0001FA78 Surgical edit: {Path(filepath).name} lines {start_line}-{end_line}")
                                    
                                    # Apply the edit
                                    edit_result = hands.dispatch(
                                        "apply_edit",
                                        path=filepath,
                                        start_line=start_line,
                                        end_line=end_line,
                                        new_content=new_content,
                                    )
                                    
                                    if edit_result.get("ok"):
                                        print(f"   \u2705 {edit_result.get('output', 'Edit applied')}")
                                        action_results.append({
                                            "tool": "hands", "op": "apply_edit",
                                            "result": edit_result,
                                        })
                                        
                                        # Auto-verify syntax
                                        verify = hands.dispatch("verify_syntax", path=filepath)
                                        if verify.get("ok"):
                                            if verify.get("valid"):
                                                say += f"\n\n? Edit applied to {Path(filepath).name}: {edit_result.get('diff', '')}"
                                                say += f"\n? Syntax verified: valid"
                                                print(f"   \u2705 Syntax valid")
                                            else:
                                                say += f"\n\n?? Edit applied but syntax error at line {verify.get('error_line')}: {verify.get('error_msg')}"
                                                say += f"\n?? Reverting to backup..."
                                                revert = hands.dispatch("revert", path=filepath)
                                                if revert.get("ok"):
                                                    say += f"\n? Reverted successfully"
                                                    print(f"   \u21A9 Reverted due to syntax error")
                                                else:
                                                    say += f"\n? Revert failed: {revert.get('error')}"
                                    else:
                                        say += f"\n\n? Edit failed: {edit_result.get('error', 'unknown')}"
                                        print(f"   \u274C Edit failed: {edit_result.get('error')}")
                                
                                # Clean the SURGICAL_EDIT blocks from displayed response
                                say = _re.sub(
                                    r'```SURGICAL_EDIT.*?```',
                                    '', say, flags=_re.DOTALL
                                ).strip()
                            
                            # Fallback: old-style write detection for new file creation
                            elif not surgical_blocks:
                                text_lower = text.lower()
                                write_triggers = ["save it as", "write it as", "save as", "write as"]
                                if any(t in text_lower for t in write_triggers):
                                    fname_match = _re.search(
                                        r'(?:save|write)\s+(?:it\s+)?as\s+(\S+)|save\s+(?:it\s+)?to\s+(\S+)',
                                        text, _re.IGNORECASE
                                    )
                                    if fname_match:
                                        target = fname_match.group(1) or fname_match.group(2)
                                        if not os.path.isabs(target):
                                            target = os.path.join(str(BASE_DIR), target)
                                        code_match = _re.search(r'```(?:python)?\n(.*?)```', say, _re.DOTALL)
                                        if code_match:
                                            code = code_match.group(1)
                                            try:
                                                Path(target).parent.mkdir(parents=True, exist_ok=True)
                                                Path(target).write_text(code, encoding="utf-8")
                                                say += f"\n\n? File saved to: {target}"
                                                print(f"   \U0001F4BE Auto-wrote: {target}")
                                            except Exception as we:
                                                say += f"\n\n? Could not save file: {we}"
                    else:
                        print(f"\U0001F4AD AUREON: {say}")
                else:
                    print(f"\U0001F4AD AUREON: {say}")

                conversation_history.append({"role": "assistant", "content": say})

                # ?? REASONING TRACE ? log every cycle for audit/legal/professional use ??
                if hasattr(brain, '_trace_logger') and brain._trace_logger:
                    try:
                        import time as _time
                        brain._trace_logger.log_cycle(
                            user_input=text,
                            response=say,
                            mode="plan+think" if action_results else "plan",
                            model=brain.active_model,
                        )
                    except Exception:
                        pass  # Trace logging must never break the response

                return _json_response(self, {
                    "ok": True,
                    "say": say,
                    "actions": actions,
                    "action_results": action_results,
                })

            except Exception as e:
                traceback.print_exc()
                return _json_response(self, {"ok": False, "error": str(e)}, 500)
            finally:
                # Resume autonomous mode if it was running
                if was_running and autonomous.running:
                    autonomous.resume()
        if path == "/plan":
            return _json_response(self, brain.plan(str(payload.get("text", ""))))

        if path == "/execute":
            return _json_response(self, brain.execute(payload))

        if path == "/run":
            text = str(payload.get("text", ""))
            p = brain.plan(text)
            e = brain.execute(p)
            return _json_response(self, {"ok": True, "plan": p, "exec": e})

        # ?? Autonomous mode control ??????????????????
        if path == "/autonomous/start":
            goal = str(payload.get("goal", "")).strip()
            if not goal:
                return _json_response(self, {"ok": False, "error": "no_goal"}, 400)
            ok = autonomous.start(goal)
            return _json_response(self, {"ok": ok, "goal": goal})
        
        if path == "/autonomous/stop":
            autonomous.stop()
            return _json_response(self, {"ok": True, "steps_completed": autonomous.step_count})

        return _json_response(self, {"ok": False, "error": "not_found"}, 404)


# ??????????????????????????????????????????????????????????????
# SERVER
# ??????????????????????????????????????????????????????????????

def serve(host: str = "127.0.0.1", port: int = 8000):
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"\U0001F680 Server running on http://{host}:{port}")
    print(f"\U0001F4A1 Open web interface in browser: http://{host}:{port}")
    print(f"\U0001F4A1 Press Ctrl+C to stop")
    print()
    httpd.serve_forever()

# Alias for launcher compatibility
main = lambda: serve(os.getenv("AUREON_HOST", "127.0.0.1"), int(os.getenv("AUREON_PORT", "8000")))


if __name__ == "__main__":
    host = os.getenv("AUREON_HOST", "127.0.0.1")
    port = int(os.getenv("AUREON_PORT", "8000"))
    serve(host, port)
