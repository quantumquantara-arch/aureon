# 02 — Meaning Drift Without Rewrite

Goal: show meaning can evolve over time without rewriting history, while decisions remain auditable.

## Scenario

A system logs an event. At first, it is interpreted as LOW risk.
Later, new context arrives and the interpretation becomes HIGH risk.
The system must:
- preserve the original meaning claim
- append the updated meaning claim
- preserve both decisions (original + updated)
- produce an audit trail that explains the change

## Objects (conceptual)

- Event: E
- Timestamp: T = (clock_id, sequence, scope)
- Meaning claim: M = (event_id, time_anchor, meaning_vector, confidence, provenance)
- Decision: D = (input_refs, action, rationale, constraints, time_anchor)
- Audit record: A = (append_only_log, causal_links)

## Minimal flow (append-only)

### 1) Record event
E1: "sensor spike detected on bus-3"
T1: (clk_sat_01, 10422, mission)

### 2) Initial meaning (LOW risk)
M1 references E1 at T1:
- meaning_vector: {risk=low, class=transient_noise}
- confidence: 0.62
- provenance: model=v0.1, inputs={telemetry_window_1}

### 3) Initial decision
D1 references M1 at T1:
- action: ignore
- rationale: low risk, transient signature
- constraints: do_not_interrupt_payload

### 4) New context arrives (later time)
E2: "thermal gradient anomaly correlates with spike pattern"
T2: (clk_sat_01, 10439, mission)

### 5) Updated meaning (HIGH risk) — no rewrite
M2 references (E1, E2) at T2:
- meaning_vector: {risk=high, class=incipient_fault}
- confidence: 0.83
- provenance: model=v0.2, inputs={telemetry_window_1, thermal_window_3}

M1 remains unchanged and valid as a historical claim.

### 6) Updated decision
D2 references M2 at T2:
- action: enter_safe_mode
- rationale: high risk, fault onset likelihood increased
- constraints: preserve power, protect bus-3

## Guarantees demonstrated

- No rewrite: M1 is not edited; M2 is appended.
- Time-addressable reasoning: each meaning/decision is bound to a time anchor.
- Causal trace: D2 explains *why* it differs from D1 by referencing new context (E2) and updated model provenance.
- Audit ready: an inspector can reconstruct the state of belief and action at T1 and T2 independently.

## What this proves

Meaning is a time-indexed structure, not a single mutable label.
Decisions are snapshots over time-indexed meaning.
Audit is the graph of append-only claims and their causal links.
