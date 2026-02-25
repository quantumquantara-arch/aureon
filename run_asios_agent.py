import hashlib
import json
import os
from datetime import datetime

def generate_hello_mission():
    mission = {
        "mission_id": "hello_asios_001",
        "schema_version": "1.0",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "env": "DEV",
        "created_by_agent": "ASIOS-InitAgent",
        "type": "LAPTOP_FS",
        "payload": {
            "steps": [
                {
                    "op": "CREATE_FILE",
                    "path": "hello_from_asios.txt",
                    "expected_previous_hash": None,
                    "content": "ASIOS has initialized. [OK]\nTimestamp: " + datetime.utcnow().isoformat() + "Z"
                }
            ]
        }
    }
    return mission

def write_mission_file(mission, filename="mission_hello.json"):
    with open(filename, "w") as f:
        json.dump(mission, f, indent=2)
    print(f"Mission file written to: {filename}")

def execute_mission_file(filename="mission_hello.json"):
    with open(filename) as f:
        mission = json.load(f)

    for step in mission["payload"]["steps"]:
        if step["op"] == "CREATE_FILE":
            path = step["path"]
            content = step["content"]
            if os.path.exists(path):
                print(f"File already exists: {path}")
                continue
            with open(path, "w") as file:
                file.write(content)
            print(f"[OK] Created: {path}")
            hash_val = hashlib.sha256(content.encode()).hexdigest()
            print(f"SHA-256: {hash_val}")

if __name__ == "__main__":
    mission = generate_hello_mission()
    write_mission_file(mission)
    execute_mission_file()
