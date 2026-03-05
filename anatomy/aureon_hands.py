import os
import subprocess
import time
from typing import Optional, List, Dict, Any
import psutil
# import pyttsx3 # Not needed for basic hands operations
# import speech_recognition as sr # Not needed for basic hands operations
import sys
from pathlib import Path
import json

try:
    from aureon_surgeon import AureonSurgeon
except ImportError:
    AureonSurgeon = None

# Selenium imports
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class AureonHands:
    """
    AUREON's hands - controls files AND browser.
    File operations ALWAYS work.
    Browser operations auto-retry connection.
    """

    def __init__(self, base_dir: str = r"C:\AUREON_AUTONOMOUS"):
        self.base_dir = Path(base_dir)
        self.driver = None
        self.browser_connected = False
        self._last_connect_attempt = 0
        
        # Initialize the surgical code editor
        self.surgeon = AureonSurgeon(base_dir=base_dir) if AureonSurgeon else None

        if SELENIUM_AVAILABLE:
            self._try_connect_browser()
        else:
            print("   ⚠️ Selenium not installed: pip install selenium", file=sys.stderr)
            print("   Browser control disabled. File operations still work.", file=sys.stderr)

    # ??????????????????????????????????????????????????????????
    # BROWSER CONNECTION (auto-retry)
    # ??????????????????????????????????????????????????????????

    def _try_connect_browser(self) -> bool:
        """Try to connect to existing browser. Auto-launches Chrome if needed."""
        now = time.time()
        # Don't spam retries — wait at least 10 seconds between attempts
        if now - self._last_connect_attempt < 10:
            return self.browser_connected
        self._last_connect_attempt = now

        if self.browser_connected and self.driver:
            # Check if still alive
            try:
                _ = self.driver.title
                return True
            except Exception:
                self.browser_connected = False
                self.driver = None

        # Step 1: Check if Chrome is already listening on 9222
        import socket
        chrome_listening = False
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect(("127.0.0.1", 9222))
            s.close()
            chrome_listening = True
        except Exception:
            pass
        
        # Step 2: If Chrome is NOT listening, launch it ourselves
        if not chrome_listening:
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ]
            edge_paths = [
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            ]
            
            launched = False
            for browser_path in chrome_paths + edge_paths:
                if os.path.exists(browser_path):
                    try:
                        browser_name = "Chrome" if "chrome" in browser_path.lower() else "Edge"
                        print(f"   [LAUNCH] Launching {browser_name} with --remote-debugging-port=9222...", file=sys.stderr)
                        subprocess.Popen(
                            [browser_path, "--remote-debugging-port=9222", "--no-first-run"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
                        # Wait for it to start
                        for attempt in range(15):  # Up to 15 seconds
                            time.sleep(1)
                            try:
                                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                s.settimeout(1)
                                s.connect(("127.0.0.1", 9222))
                                s.close()
                                print(f"   [OK] {browser_name} is now listening on port 9222", file=sys.stderr)
                                launched = True
                                break
                            except Exception:
                                pass
                        if launched:
                            break
                    except Exception as launch_err:
                        print(f"   [WARN] Failed to launch {browser_path}: {launch_err}", file=sys.stderr)
            
            if not launched:
                print("   [FAIL] Could not launch any browser with debug port", file=sys.stderr)
                return False

        # Step 3: Connect via Selenium
        # Try Chrome
        try:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            self.driver = webdriver.Chrome(options=options)
            self.browser_connected = True
            print("   ✅ Connected to Chrome (port 9222)", file=sys.stderr)
            return True
        except Exception as chrome_err:
            short_err = str(chrome_err).split('\n')[0][:120]
            print(f"   Chrome selenium failed: {short_err}", file=sys.stderr)

        # Try Edge
        try:
            options = webdriver.EdgeOptions()
            options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            self.driver = webdriver.Edge(options=options)
            self.browser_connected = True
            print("   ✅ Connected to Edge (port 9222)", file=sys.stderr)
            return True
        except Exception as edge_err:
            short_err = str(edge_err).split('\n')[0][:120]
            print(f"   Edge selenium failed: {short_err}", file=sys.stderr)

        if not self.browser_connected:
            print("   ⚠️ Browser launched but Selenium could not connect", file=sys.stderr)
            print("    This usually means chromedriver version doesn't match Chrome version", file=sys.stderr)
            print("    Update: pip install --upgrade selenium", file=sys.stderr)
        return False

    def _ensure_browser(self) -> bool:
        """Ensure browser is connected, retry if needed."""
        if self.browser_connected:
            try:
                _ = self.driver.title
                return True
            except Exception:
                self.browser_connected = False
                self.driver = None

        if SELENIUM_AVAILABLE:
            return self._try_connect_browser()
        return False

    # ??????????????????????????????????????????????????????????
    # DISPATCH - routes all operations
    # ??????????????????????????????????????????????????????????

    def dispatch(self, op: str, **kwargs) -> Dict[str, Any]:
        """Route operations to handlers"""

        # ?? File operations (ALWAYS work) ????????????
        if op == "search_files":
            return self.search_files(kwargs.get("query", ""), kwargs.get("root", str(self.base_dir)))
        elif op == "read_file":
            return self.read_file(kwargs.get("path", ""))
        elif op == "write_file":
            return self.write_file(kwargs.get("path", ""), kwargs.get("content", ""))
        elif op == "list_files":
            return self.list_files(kwargs.get("path", str(self.base_dir)))
        elif op == "read_directory": # Alias for list_files with pattern
            return self.list_files(kwargs.get("path", ""), kwargs.get("pattern", "*"))
        elif op == "scan_all_files":
            return self.scan_all_files(
                root=kwargs.get("root", kwargs.get("path", str(self.base_dir))),
                extensions=kwargs.get("extensions", ".md,.py,.kernel")
            )
        elif op == "run_command":
            return self.run_command(kwargs.get("command", ""), kwargs.get("shell", True))

        # ?? Browser operations ????????????????????????
        if not self._ensure_browser():
            return {"success": False, "message": "Browser not connected or failed to connect."}

        d = self.driver
        try:
            if op == "navigate":
                d.get(kwargs.get("url",""))
                return {"success":True,"url":d.current_url}
            elif op == "google_search":
                d.get(f"https://www.google.com/search?q={kwargs.get('query','')}")
                return {"success":True,"url":d.current_url}
            elif op == "click_on_text":
                # This function needs to be more robust, potentially using OCR or XPATH based on text
                # For now, it's a placeholder to indicate the intent.
                # A more complete implementation would need to find elements containing the text.
                # Example: element = d.find_element(By.XPATH, f"//*[contains(text(), '{kwargs.get('text','')}')]")
                # element.click()
                # For now, if no selector given, we can't click by text reliably.
                if kwargs.get("selector"):
                    d.find_element(By.CSS_SELECTOR, kwargs.get("selector")).click()
                    return {"success":True, "message": f"Clicked on element with selector: {kwargs.get('selector')}"}
                else:
                    return {"success": False, "message": "click_on_text requires a selector or text-based element finding logic."}
            elif op == "type_text":
                selector = kwargs.get("selector")
                text = kwargs.get("text", "")
                if selector:
                    element = d.find_element(By.CSS_SELECTOR, selector)
                    element.send_keys(text)
                    return {"success":True, "message": f"Typed into element {selector}"}
                else:
                    # Attempt to type into the currently active element or body if no selector
                    active_element = d.switch_to.active_element
                    if active_element and active_element.tag_name in ['input', 'textarea']:
                        active_element.send_keys(text)
                        return {"success":True, "message": "Typed into active element."}
                    else:
                        d.find_element(By.TAG_NAME, "body").send_keys(text)
                        return {"success": False, "message": "Typed into body (no specific selector or active input field found)."}
            elif op == "press": # Simulate keyboard press, e.g., Keys.ENTER
                key = kwargs.get("key")
                if key:
                    ActionChains(d).send_keys(getattr(Keys, key.upper(), key)).perform()
                    return {"success":True, "message":f"Pressed key: {key}"}
                return {"success":False, "message":"No key specified for press operation."}
            elif op == "get_text":
                selector = kwargs.get("selector", "body")
                element = d.find_element(By.CSS_SELECTOR, selector)
                return {"success":True,"text":element.text[:5000]}
            elif op == "get_url":
                return {"success":True,"url":d.current_url}
            elif op == "scroll":
                d.execute_script(f"window.scrollBy(0,{kwargs.get('y',400)})")
                return {"success":True}
            elif op == "new_tab":
                d.execute_script("window.open('');")
                return {"success": True, "message": "Opened new tab."}
            elif op == "switch_tab":
                target_handle = kwargs.get('handle')
                if target_handle:
                    d.switch_to.window(target_handle)
                elif kwargs.get('index') is not None:
                    handles = d.window_handles
                    index = int(kwargs.get('index'))
                    if 0 <= index < len(handles):
                        d.switch_to.window(handles[index])
                    else:
                        return {"success": False, "message": "Invalid tab index."}
                else:
                    return {"success": False, "message": "Specify tab handle or index."}
                return {"success": True, "message": f"Switched to tab: {d.current_url}"}
            else:
                return {"success":False,"message":f"Unknown browser op: {op}"}
        except Exception as e:
            return {"success":False,"message":str(e)}

    # ??????????????????????????????????????????????????????????
    # FILE OPERATIONS
    # ??????????????????????????????????????????????????????????

    def search_files(self, query: str, root: str = None) -> Dict[str, Any]:
        results = []
        start_path = Path(root).expanduser() if root else self.base_dir
        for path in start_path.rglob(f"*{query}*"):
            if path.is_file():
                results.append(str(path))
        return {"success": True, "files": results}

    def read_file(self, path: str) -> Dict[str, Any]:
        full_path = Path(path).expanduser()
        if not full_path.is_file():
            return {"success": False, "message": f"File not found: {path}"}
        try:
            with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            return {"success": True, "content": content}
        except Exception as e:
            return {"success": False, "message": f"Error reading file {path}: {str(e)}"}

    def write_file(self, path: str, content: str) -> Dict[str, Any]:
        full_path = Path(path).expanduser()
        try:
            os.makedirs(full_path.parent, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            return {"success": True, "path": str(full_path)}
        except Exception as e:
            return {"success": False, "message": f"Error writing file {path}: {str(e)}"}

    def list_files(self, path: str, pattern: str = "*") -> Dict[str, Any]:
        """Lists files and directories in the given path, optionally filtered by pattern."""
        full_path = Path(path).expanduser()
        print(f"DEBUG: list_files called with path: {full_path}", file=sys.stderr) # <-- DEBUG LINE ADDED
        if not full_path.is_dir():
            return {"success": False, "message": f"Directory not found: {path}"}
        try:
            items = []
            for item in full_path.glob(pattern):
                items.append({
                    "name": item.name,
                    "is_dir": item.is_dir(),
                    "is_file": item.is_file(),
                    "path": str(item.absolute())
                })
            return {"success": True, "items": items}
        except Exception as e:
            return {"success": False, "message": f"Error listing directory {path}: {str(e)}"}

    def run_command(self, command: str, shell: bool = True) -> Dict[str, Any]:
        try:
            result = subprocess.run(command, shell=shell, capture_output=True, text=True, timeout=60)
            return {
                "success": True,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "message": f"Command timed out after 60 seconds: {command}"}
        except Exception as e:
            return {"success": False, "message": f"Error running command: {str(e)}"}

# ??????????????????????????????????????????????????????????
# ENTRY POINT FOR DAEMON
# ??????????????????????????????????????????????????????????

if __name__ == "__main__":
    op = sys.argv[1] if len(sys.argv) > 1 else "help"
    arg1 = sys.argv[2] if len(sys.argv) > 2 else ""
    arg2 = sys.argv[3] if len(sys.argv) > 3 else ""
    args_json = sys.argv[4] if len(sys.argv) > 4 else "{}"

    kwargs = json.loads(args_json)

    hands = AureonHands()
    result = {"success": False, "message": "Unknown operation or invalid arguments."}

    # Pass correct arguments based on operation
    if op in ["search_files", "read_file", "write_file", "list_files", "read_directory", "scan_all_files", "run_command",
              "navigate", "google_search", "click_on_text", "type_text", "press", "get_text", "get_url", "scroll", "new_tab", "switch_tab"]:
        # For file operations, arg1 is path/query, arg2 is content/root/pattern etc.
        # For browser ops, arg1 is usually selector/url/query, arg2 is text/key/index etc.
        # The dispatch method handles kwargs so we can pass things flexibly
        
        # Example: list_files op takes 'path' as a kwarg
        if op == "list_files":
            kwargs['path'] = arg1 # This should be the directory to list
            if arg2: kwargs['pattern'] = arg2
        elif op == "read_file":
            kwargs['path'] = arg1
        elif op == "write_file":
            kwargs['path'] = arg1
            kwargs['content'] = arg2
        elif op == "type_text":
            kwargs['selector'] = arg1 # CSS selector
            kwargs['text'] = arg2 # Text to type
        elif op == "navigate":
            kwargs['url'] = arg1
        elif op == "google_search":
            kwargs['query'] = arg1
        elif op == "click_on_text":
            kwargs['selector'] = arg1 # or text, depending on implementation
        elif op == "press":
            kwargs['key'] = arg1
        elif op == "run_command":
            kwargs['command'] = arg1
            
        result = hands.dispatch(op, **kwargs)
    
    # --- DEBUGGING OUTPUT ADDED ---
    print(json.dumps(result), file=sys.stdout) # Print final result to stdout for daemon
    print(f"DEBUG: Final result type: {type(result)}", file=sys.stderr)
    print(f"DEBUG: Final result: {result}", file=sys.stderr)
    # --- END DEBUGGING OUTPUT ---
