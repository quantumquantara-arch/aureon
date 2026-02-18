"""
AUREON COMPLETE INITIALIZATION
===============================
100% ASCII -- will NOT crash on Windows cp1252.

Auto-checks LLMs, integrates files, activates capabilities.
Run this ONCE to set up AUREON completely.
"""
from __future__ import annotations
import os, sys, json, time
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system("pip install requests")
    import requests


class AureonCompleteInit:
    def __init__(self, base_dir: str = r"C:\AUREON_AUTONOMOUS"):
        self.base_dir = Path(base_dir)
        self.foundation_dir = self.base_dir / "AUREON_FOUNDATION"
        self.base_dir.mkdir(exist_ok=True)
        self.foundation_dir.mkdir(exist_ok=True)
        self.status = {
            "llms": {"deepseek_direct": "pending", "ollama": "pending",
                     "openrouter": "pending", "gemini": "pending"},
            "file_integration": {"base": 0, "foundation": 0},
            "capabilities": {"hands": False, "eyes": False},
            "ready": False,
        }

    def check_deepseek_direct(self) -> bool:
        print("")
        print("=" * 60)
        print("  Checking DeepSeek Direct API")
        print("=" * 60)
        try:
            sys.path.insert(0, str(self.base_dir))
            from aureon_deepseek_direct import DeepSeekDirect
            ds = DeepSeekDirect()
            result = ds.test_connection()
            if result["ok"]:
                print("  [OK] DeepSeek Direct API working")
                print("  Model: deepseek-chat (V3)")
                self.status["llms"]["deepseek_direct"] = "ok"
                return True
            else:
                print("  [WARN] DeepSeek Direct: " + result["error"])
                self.status["llms"]["deepseek_direct"] = "error"
                return False
        except ImportError:
            print("  [SKIP] aureon_deepseek_direct.py not found")
            self.status["llms"]["deepseek_direct"] = "missing"
            return False
        except Exception as e:
            print("  [WARN] DeepSeek Direct: " + str(e))
            self.status["llms"]["deepseek_direct"] = "error"
            return False

    def check_ollama(self) -> bool:
        print("")
        print("=" * 60)
        print("  Checking Ollama")
        print("=" * 60)
        try:
            r = requests.get("http://127.0.0.1:11434/api/tags", timeout=3)
            if r.status_code == 200:
                models = [m.get("name", "") for m in r.json().get("models", [])]
                print("  [OK] Ollama running, " + str(len(models)) + " models")
                for m in models[:5]:
                    print("    - " + m)
                self.status["llms"]["ollama"] = "ok"
                return True
        except Exception:
            pass
        print("  [WARN] Ollama not running (optional)")
        self.status["llms"]["ollama"] = "offline"
        return False

    def integrate_files(self) -> dict:
        print("")
        print("=" * 60)
        print("  Integrating files")
        print("=" * 60)
        exts = (".py", ".md", ".txt", ".json", ".yaml", ".yml")
        skip = ("__pycache__", ".git", "venv", "node_modules",
                "BROWSER_PROFILE", "driver", "LOGS")

        def scan(root, key):
            count = 0
            for p in root.rglob("*"):
                if p.is_dir():
                    continue
                if any(s in p.parts for s in skip):
                    continue
                if p.suffix.lower() not in exts:
                    continue
                try:
                    if p.stat().st_size > 0:
                        count += 1
                except Exception:
                    continue
            return count

        base_count = scan(self.base_dir, "base")
        foundation_count = scan(self.foundation_dir, "foundation")

        self.status["file_integration"]["base"] = base_count
        self.status["file_integration"]["foundation"] = foundation_count

        print("  [OK] Base directory: " + str(base_count) + " files")
        print("  [OK] Foundation: " + str(foundation_count) + " files")
        return {"base": base_count, "foundation": foundation_count}

    def init_capabilities(self) -> dict:
        print("")
        print("=" * 60)
        print("  Initializing capabilities")
        print("=" * 60)
        caps = {}
        try:
            import pyautogui
            size = pyautogui.size()
            caps["hands"] = True
            print("  [OK] Hands (screen: " + str(size.width) + "x" + str(size.height) + ")")
        except Exception as e:
            caps["hands"] = False
            print("  [--] Hands: " + str(e))
        try:
            import pyautogui
            pyautogui.screenshot()
            caps["eyes"] = True
            print("  [OK] Eyes (screenshot)")
        except Exception as e:
            caps["eyes"] = False
            print("  [--] Eyes: " + str(e))
        # Check ears
        try:
            import pyaudiowpatch
            caps["ears"] = True
            print("  [OK] Ears (pyaudiowpatch found)")
        except ImportError:
            try:
                import pyaudio
                caps["ears"] = True
                print("  [OK] Ears (pyaudio found)")
            except ImportError:
                caps["ears"] = False
                print("  [--] Ears: pip install pyaudiowpatch")
        # Check dialogue memory
        mem_dir = self.base_dir / "DIALOGUE_MEMORY"
        if mem_dir.exists() and list(mem_dir.glob("*.json")):
            caps["dialogue_memory"] = True
            print("  [OK] Dialogue memory (podcast learning data found)")
        else:
            caps["dialogue_memory"] = False
            print("  [--] Dialogue memory: empty (absorb podcasts to fill)")
        self.status["capabilities"] = caps
        return caps

    def run_complete_init(self) -> dict:
        print("")
        print("=" * 60)
        print("  AUREON COMPLETE INITIALIZATION")
        print("=" * 60)

        has_llm = self.check_deepseek_direct()
        self.check_ollama()
        self.integrate_files()
        self.init_capabilities()

        # If DeepSeek failed, check OpenRouter/Gemini availability
        if not has_llm:
            has_llm = self.status["llms"]["ollama"] == "ok"

        has_files = (self.status["file_integration"]["base"] > 0 or
                     self.status["file_integration"]["foundation"] > 0)

        self.status["ready"] = has_llm and has_files

        print("")
        print("=" * 60)
        print("  INITIALIZATION COMPLETE")
        print("=" * 60)
        print(json.dumps(self.status, indent=2))

        if self.status["ready"]:
            print("")
            print("  [OK] AUREON IS READY TO RUN")
            print("")
            print("  To start: double-click AUREON_START.bat")
            print("  Or: python aureon_web_interface.py")
        else:
            print("")
            print("  [WARN] AUREON NOT FULLY READY")
            if not has_llm:
                print("  - No LLM available. Fix DeepSeek key or start Ollama.")
            if not has_files:
                print("  - No files found in " + str(self.base_dir))

        return self.status


def main():
    import argparse
    parser = argparse.ArgumentParser(description="AUREON Complete Init")
    parser.add_argument("--base-dir", default=r"C:\AUREON_AUTONOMOUS")
    args = parser.parse_args()
    init = AureonCompleteInit(args.base_dir)
    init.run_complete_init()


if __name__ == "__main__":
    main()
