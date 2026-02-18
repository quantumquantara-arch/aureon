# Example 01 — Minimal Event Flow

This example demonstrates the smallest complete execution of the  
Time → Meaning → Decision (TMD) system.

No abstractions. One event.

---

## 1. Event

An internal system detects a temperature threshold breach.

```text
event_id: EVT-0001
type: sensor.threshold_breach
source: thermal_monitor
```

---

## 2. Time Anchor

The event is bound to time at the moment it is observed.

```text
T = (
  clock_id = SYS_MONO_01,
  sequence = 184233,
  scope = process_lifetime
)
```

This timestamp is append-only and immutable.

---

## 3. Meaning Attachment

Meaning is not inferred later — it is attached at the time of observation.

```text
meaning_id: MEAN-042
classification: safety_relevant
confidence: 0.91
context: "Thermal envelope exceeded safe operating range"
```

Meaning is inspectable **without reinterpreting the past**.

---

## 4. Decision

The system executes an action justified by prior structure.

```text
decision_id: DEC-017
action: throttle_system
justification:
  time_anchor: T
  meaning_id: MEAN-042
```

The decision references structured state, **not raw data**.

---

## 5. Audit Trace

All elements form a single causal chain.

```text
EVT-0001 → T → MEAN-042 → DEC-017
```

At no point is ordering rewritten.  
Inspection does not mutate state.

---

## Guarantees Demonstrated

- Every action is time-addressable  
- Meaning is bound, not retrofitted  
- Decisions are replayable  
- Causality is inspectable end-to-end  
