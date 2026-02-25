# validate_agent_manifest.py

import json
import sys

REQUIRED_FIELDS = {
    "agent_id", "version", "permissions", "envs", "allowed_mission_types",
    "max_notional_limit", "created_at"
}
ALLOWED_ENVS = {"DEV", "STAGING", "PROD"}
ALLOWED_TYPES = {"LAPTOP_FS", "FINANCE_PORTFOLIO", "FINANCE_ORDER"}

def validate_manifest(manifest):
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in manifest:
            errors.append(f"Missing required field: {field}")

    if "envs" in manifest:
        for env in manifest["envs"]:
            if env not in ALLOWED_ENVS:
                errors.append(f"Invalid env: {env}")

    if "allowed_mission_types" in manifest:
        for mission_type in manifest["allowed_mission_types"]:
            if mission_type not in ALLOWED_TYPES:
                errors.append(f"Invalid mission type: {mission_type}")

    if "max_notional_limit" in manifest:
        if not isinstance(manifest["max_notional_limit"], (int, float)):
            errors.append("max_notional_limit must be a number")

    return errors

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_agent_manifest.py <manifest_file.json>")
        exit(1)

    manifest_path = sys.argv[1]
    with open(manifest_path) as f:
        manifest = json.load(f)

    issues = validate_manifest(manifest)

    if issues:
        print("[?] Agent manifest invalid:")
        for issue in issues:
            print(" -", issue)
    else:
        print("[?] Agent manifest valid.")
