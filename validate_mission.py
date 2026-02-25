import json, sys, re
from datetime import datetime

ALLOWED_TYPES = {"LAPTOP_FS"}
ALLOWED_OPS = {"CREATE_FILE","REPLACE_FILE","INSERT_AFTER_MARKER","DELETE_FILE","RUN_SCRIPT"}

def is_iso8601_z(s: str) -> bool:
    try:
        datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
        return True
    except Exception:
        return False

def fail(msg: str):
    raise ValueError(msg)

def validate(m: dict):
    for k in ["mission_id","schema_version","created_at","env","created_by_agent","type","payload"]:
        if k not in m:
            fail(f"missing field: {k}")
    if not is_iso8601_z(m["created_at"]):
        fail("created_at must be UTC Z ISO8601: YYYY-MM-DDTHH:MM:SSZ")
    if m["type"] not in ALLOWED_TYPES:
        fail(f"type must be one of: {sorted(ALLOWED_TYPES)}")
    payload = m["payload"]
    if "steps" not in payload or not isinstance(payload["steps"], list) or len(payload["steps"]) == 0:
        fail("payload.steps must be a non-empty list")
    for i, step in enumerate(payload["steps"]):
        if "op" not in step or "path" not in step:
            fail(f"step[{i}] missing op/path")
        if step["op"] not in ALLOWED_OPS:
            fail(f"step[{i}] op invalid: {step['op']}")
        if step["op"] in {"CREATE_FILE","REPLACE_FILE","INSERT_AFTER_MARKER"} and "content" not in step:
            fail(f"step[{i}] {step['op']} requires content")
        if "expected_previous_hash" in step and step["expected_previous_hash"] is not None:
            h = str(step["expected_previous_hash"]).lower()
            if not re.fullmatch(r"[0-9a-f]{64}", h):
                fail(f"step[{i}] expected_previous_hash must be 64 hex chars or null")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_mission.py <mission.json>")
        sys.exit(1)
    p = sys.argv[1]
    try:
        with open(p, "r", encoding="utf-8-sig") as f:
            m = json.load(f)
        validate(m)
        print("Mission file is valid âœ…")
        sys.exit(0)
    except Exception as e:
        print(f"Mission invalid â?Œ: {e}")
        sys.exit(1)
