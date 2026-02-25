import subprocess
import json
import hashlib
import os

MISSION_FILE = "asios_mission_example.json"

def hash_content(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def load_mission():
    with open(MISSION_FILE, 'r') as f:
        return json.load(f)

def run_step(step):
    op = step['op']
    path = step['path']
    expected = step.get('expected_previous_hash')
    content = step.get('content')

    if op == "CREATE_FILE":
        if expected is not None and os.path.exists(path):
            with open(path, 'r') as f:
                current_hash = hash_content(f.read())
            if current_hash != expected:
                raise ValueError(f"Hash mismatch on {path}")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        print(f"[OK] Created file: {path}")

    elif op == "RUN_SCRIPT":
        if expected is not None and os.path.exists(path):
            with open(path, 'r') as f:
                current_hash = hash_content(f.read())
            if current_hash != expected:
                raise ValueError(f"Hash mismatch before execution: {path}")
        result = subprocess.run(["bash", path], capture_output=True, text=True)
        print(f"?? Executed {path}")
        print(result.stdout)
        if result.stderr:
            print("[WARN]? stderr:", result.stderr)

    else:
        raise NotImplementedError(f"Unknown op: {op}")

def main():
    mission = load_mission()
    print(f"[LAUNCH] Executing mission {mission['mission_id']}")
    for step in mission['payload']['steps']:
        run_step(step)

if __name__ == "__main__":
    main()
