?import json
from jsonschema import validate, ValidationError

# Load schemas
with open("schema/timestamp.schema.json") as f:
    TIMESTAMP = json.load(f)
with open("schema/event.schema.json") as f:
    EVENT = json.load(f)
with open("schema/meaning.schema.json") as f:
    MEANING = json.load(f)
with open("schema/decision.schema.json") as f:
    DECISION = json.load(f)
with open("schema/audit.schema.json") as f:
    AUDIT = json.load(f)

SCHEMAS = {
    "event": EVENT,
    "meaning": MEANING,
    "decision": DECISION,
    "audit": AUDIT,
}

def check_schema(node):
    node_type = node.get("type")
    if node_type not in SCHEMAS:
        raise ValueError(f"Unknown node type: {node_type}")
    validate(instance=node, schema=SCHEMAS[node_type])

def check_invariants(pipeline):
    # 1. timestamps must strictly increase
    seqs = [step["timestamp"]["sequence"] for step in pipeline]
    if seqs != sorted(seqs):
        raise ValueError("Timestamp sequence out of order.")

    # 2. meaning must reference an event
    for step in pipeline:
        if step["type"] == "meaning":
            if "event" not in step:
                raise ValueError("Meaning missing reference to event.")

    # 3. decision must reference meaning
    for step in pipeline:
        if step["type"] == "decision":
            if "ref" not in step:
                raise ValueError("Decision missing meaning reference.")

def validate_pipeline(pipeline):
    for node in pipeline:
        check_schema(node)
    check_invariants(pipeline)
    return True
