import json
import hashlib
import sys

class InvariantViolation(Exception):
    pass

class ReferenceEngine:
    def __init__(self, schema_path):
        with open(schema_path, "r", encoding="utf-8") as f:
            self.schema = json.load(f)

    def hash_state(self, state: dict) -> str:
        serialized = json.dumps(state, sort_keys=True).encode("utf-8")
        return hashlib.sha256(serialized).hexdigest()

    def enforce_non_erasure(self, previous, current):
        for key in previous:
            if key not in current:
                raise InvariantViolation(f"State erasure detected: {key}")

    def validate(self, previous_state, current_state):
        self.enforce_non_erasure(previous_state, current_state)
        return self.hash_state(current_state)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: reference_engine.py prev.json current.json")

    engine = ReferenceEngine("../invariant-proof/invariant_schema.json")

    with open(sys.argv[1]) as f:
        prev = json.load(f)
    with open(sys.argv[2]) as f:
        curr = json.load(f)

    digest = engine.validate(prev, curr)
    print("STATE HASH:", digest)
