import json
import sys
from datetime import datetime

CONFIG_PATH = "validation/mission_validator_config.json"

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def validate_mission(mission_path):
    with open(mission_path, 'r') as f:
        mission = json.load(f)

    config = load_config()
    errors = []

    # Check required root fields
    for field in config["required_fields"]:
        if field not in mission:
            errors.append(f"Missing root field: {field}")

    # Check environment
    if mission.get("env") not in config["allowed_environments"]:
        errors.append(f"Invalid environment: {mission.get('env')}")

    # Check payload structure
    payload = mission.get("payload", {})
    for field in config["payload_required_fields"]:
        if field not in payload:
            errors.append(f"Missing payload field: {field}")

    steps = payload.get("steps", [])
    if not isinstance(steps, list):
        errors.append("Payload 'steps' must be a list")

    if len(steps) > config["max_payload_steps"]:
        errors.append(f"Too many steps: {len(steps)}")

    # Check each step
    for i, step in enumerate(steps):
        for field in config["step_required_fields"]:
            if field not in step:
                errors.append(f"Step {i} missing field: {field}")

        op = step.get("op")
        if op not in config["allowed_operations"]:
            errors.append(f"Step {i} has invalid operation: {op}")

        if op in config["op_with_content_required"] and "content" not in step:
            errors.append(f"Step {i} ({op}) missing 'content'")
        if op in config["op_content_optional"] and "content" not in step:
            pass  # optional
        if "expected_previous_hash" not in step:
            errors.append(f"Step {i} missing 'expected_previous_hash'")

    if errors:
        print("Mission validation failed:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    else:
        print("Mission validated successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_mission.py <mission_file.json>")
        sys.exit(1)

    validate_mission(sys.argv[1])
