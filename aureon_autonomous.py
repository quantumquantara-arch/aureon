from __future__ import annotations
import os
import json
import time
import sys
from pathlib import Path

from aureon_brain import AureonBrain

BASE_DIR = os.getenv("AUREON_BASE_DIR", r"C:\AUREON_AUTONOMOUS")
FOUNDATION_DIR = Path(BASE_DIR) / "AUREON_FOUNDATION"


def check_first_run() -> bool:
    """Check if this is first run (no init marker)"""
    marker = Path(BASE_DIR) / ".aureon_initialized"
    return not marker.exists()


def run_first_time_setup():
    """Run complete initialization on first startup"""
    print("\n" + "="*60)
    print("? FIRST RUN DETECTED - INITIALIZING AUREON")
    print("="*60)
    print("\nThis will:")
    print("  1. Download/verify LLMs (OpenAI + DeepSeek)")
    print("  2. Integrate all files from:")
    print(f"     - {BASE_DIR}")
    print(f"     - {FOUNDATION_DIR}")
    print("  3. Activate hands (keyboard/mouse)")
    print("  4. Activate eyes (screen reading)")
    print("  5. Load memory systems")
    print("\nThis may take several minutes...")
    
    response = input("\nProceed with initialization? [Y/n]: ").strip().lower()
    if response and response != 'y':
        print("Initialization cancelled. Run again when ready.")
        sys.exit(0)
    
    # Import and run complete init
    try:
        from aureon_complete_init import AureonCompleteInit
    except ImportError:
        print("\n[FAIL] aureon_complete_init.py not found!")
        print("   Make sure it's in the same directory as aureon_autonomous.py")
        sys.exit(1)
    
    init = AureonCompleteInit(BASE_DIR)
    status = init.run_complete_init()
    
    if status["ready"]:
        # Mark as initialized
        marker = Path(BASE_DIR) / ".aureon_initialized"
        marker.write_text(json.dumps(status, indent=2))
        print("\n[OK] Initialization complete! AUREON is ready.")
        print("\nRestarting AUREON...\n")
        time.sleep(2)
        return True
    else:
        print("\n[WARN]?  Initialization incomplete. Please fix issues and try again.")
        sys.exit(1)


def main():
    os.makedirs(BASE_DIR, exist_ok=True)
    FOUNDATION_DIR.mkdir(exist_ok=True)
    
    # Check for first run
    if check_first_run():
        if not run_first_time_setup():
            return
    
    print("\n" + "="*60)
    print("[LAUNCH] STARTING AUREON")
    print("="*60)
    
    # Initialize brain with hands and eyes
    try:
        from aureon_hands import AureonHands
        from aureon_eyes import AureonEyes
        
        hands = AureonHands()
        eyes = AureonEyes()
        
        print("[OK] Hands, Eyes, and Vision loaded")
        print("   • Can click on things by name (no coordinates needed!)")
        print("   • Can read screen text with OCR")
        print("   • Can understand natural language commands")
    except ImportError as e:
        print(f"[WARN]?  Some modules not found: {e}")
        print("   Running in limited mode")
        hands = None
        eyes = None
    
    brain = AureonBrain(
        hands=hands,
        eyes=eyes,
        base_dir=BASE_DIR
    )
    
    # Initialize baseline LLMs
    print("\n[BRAIN] Initializing brain...")
    status = brain.init_baseline()
    print(f"   Ollama: {status.ollama}")
    print(f"   Active Model: {status.active_model}")
    print(f"   Mode: {status.mode}")
    
    if not brain._baseline_ready:
        print("\n[FAIL] No LLMs available! Check:")
        print("   - OpenAI API key in chatgpt_api_key.txt")
        print("   - Ollama running (ollama serve)")
        sys.exit(1)
    
    # Integrate files
    print("\n? Integrating knowledge base...")
    integration = brain.integrate_files_once(
        root=BASE_DIR,
        max_files=5000
    )
    print(f"   Integrated {integration.get('files', 0)} files")
    
    # Also integrate foundation
    if FOUNDATION_DIR.exists():
        foundation_integration = brain.integrate_files_once(
            root=str(FOUNDATION_DIR),
            max_files=5000
        )
        print(f"   + {foundation_integration.get('files', 0)} foundation files")
    
    print("\n[OK] AUREON READY")
    print("\nCapabilities:")
    print(f"  [BRAIN] Brain: {status.mode}")
    print(f"  ? Hands: {'Active' if hands else 'Inactive'}")
    print(f"  [EYE]?  Eyes: {'Active' if eyes else 'Inactive'}")
    print(f"  ? Knowledge: {integration.get('files', 0)} files")
    
    # Open web interface
    try:
        import webbrowser
        from aureon_web_builder import build_chat_interface
        
        print("\n[GLOBE] Building web chat interface...")
        html_path = build_chat_interface(str(Path(BASE_DIR) / "WEB_INTERFACE"))
        print(f"   Created: {html_path}")
        
        # Open in browser
        webbrowser.open(f"file:///{html_path}")
        print(f"   Opened in browser")
        print(f"\n[IDEA] Use the web interface to chat with AUREON!")
        print(f"   Or continue in this terminal...")
    except Exception as e:
        print(f"\n[WARN]?  Could not open web interface: {e}")
        print(f"   You can still chat here in the terminal")
    
    print("\nNatural Language Commands (No coordinates needed!):")
    print("  [CHAT] 'Click on the Claude tab and write him a message'")
    print("  [CHAT] 'Open Chrome and go to reddit'")
    print("  [CHAT] 'What's on my screen right now?'")
    print("  [CHAT] 'Find the word Documentation and click it'")
    print("  [CHAT] 'Read the text on screen'")
    print("  [CHAT] 'Click on the Send button'")
    print("  [CHAT] 'Type this is a test message'")
    print("\nDirect Commands:")
    print("  • 'open url https://example.com'")
    print("  • 'read file path/to/file.txt'")
    print("  • 'search files for keyword'")
    print("  • 'status' - show system status")
    print("  • 'exit' - quit")
    print()

    while True:
        try:
            text = input("AUREON> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n? Shutting down AUREON...")
            break
        
        if not text:
            continue
        
        # Ignore comments (lines starting with #)
        if text.startswith('#'):
            continue
        
        if text.lower() in {"exit", "quit", "bye"}:
            print("\n? Goodbye!")
            break
        
        # Special commands
        if text.lower() == "status":
            print(json.dumps(brain.baseline_status(), indent=2))
            continue
        
        # Plan and execute
        try:
            plan = brain.plan(text)
            
            # Show what AUREON is thinking
            say = plan.get("say", "")
            if say:
                print(f"\n[THINK] {say}")
            
            # Execute actions
            actions = plan.get("actions", [])
            if actions:
                print(f"[GEAR]?  Executing {len(actions)} action(s)...")
                execution_result = brain.execute(plan)
                
                # Show results
                for result in execution_result.get("action_results", []):
                    tool = result.get("tool")
                    op = result.get("op")
                    res = result.get("result", {})
                    ok = res.get("ok", False)
                    status_icon = "[OK]" if ok else "[FAIL]"
                    print(f"  {status_icon} {tool}.{op}: {res.get('output', res)}")
            
            print()  # Blank line for readability
            
        except Exception as e:
            print(f"\n[FAIL] Error: {e}\n")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
