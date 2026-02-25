import json
from jsonschema import validate, ValidationError

# Schema definition for LAPTOP_FS mission type
LAPTOP_FS_SCHEMA = {
    "type": "object",
    "required": ["mission_id", "schema_version", "created_at", "env", "created_by_agent", "type", "payload"],
    "properties": {
        "mission_id": {"type": "string"},
        "schema_version": {"type": "string"},
        "created_at": {"type": "string", "format": "date-time"},
        "env": {"type": "string", "enum": ["DEV", "STAGING", "PROD"]},
        "created_by_agent": {"type": "string"},
        "type": {"type": "string", "enum": ["LAPTOP_FS"]},
        "payload": {
            "type": "object",
            "required": ["steps"],
            "properties": {
                "steps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["op", "path"],
                        "properties": {
                            "op": {
                                "type": "string",
                                "enum": ["CREATE_FILE", "REPLACE_FILE", "INSERT_AFTER_MARKER", "DELETE_FILE", "RUN_SCRIPT"]
                            },
                            "path": {"type": "string"},
                            "expected_previous_hash": {"type": ["string", "null"]},
                            "content": {"type": ["string", "null"]}
                        }
                    }
                }
            }
        }
    }
}

def validate_mission_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        validate(instance=data, schema=LAPTOP_FS_SCHEMA)
        print(f"[VALID] {filepath}")
    except ValidationError as ve:
        print(f"[INVALID] {filepath}: {ve.message}")
    except Exception as e:
        print(f"[ERROR] {filepath}: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python mission_schema_validator.py path/to/mission.json")
    else:
        validate_mission_file(sys.argv[1])
