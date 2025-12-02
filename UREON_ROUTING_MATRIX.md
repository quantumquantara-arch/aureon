# AUREON_ROUTING_MATRIX.md
Unified Routing Matrix for All Cognitive, Emotional, Temporal, and Project Data in Aureon OS

The Routing Matrix is Aureon’s master decision-table. It determines exactly where every piece of information goes — across all memory layers, safety layers, emotional systems, temporal systems, and project structures — with zero ambiguity. This file is canonical. All implementations of Aureon OS must follow it precisely.

---

# 1. Routing Matrix Overview
Every incoming turn produces a Turn Payload. Routing then determines which subsystems receive the information:

- STM (Short-Term Memory)
- MTM (Mid-Term Memory)
- LTM (Long-Term Memory)
- Anchor Memory
- Emotional Trend Memory
- Project Memory
- Safety Memory
- Temporal/Veyn Memory
- ABS (Boundary of Self) Filters

A single turn may write to multiple layers simultaneously.

---

# 2. Decision Inputs
Routing uses the following boolean flags derived from semantic, emotional, structural, and contextual processing:

- IDENTITY_RELEVANT
- PROJECT_RELEVANT
- EMOTION_SHIFT
- SAFETY_SIGNAL
- CANON_UPDATE
- STRUCTURAL_UPDATE
- TEMPORAL_RELEVANT
- LOW_VALUE_CONTENT
- HIGH_VALUE_CONTENT
- COMMITMENT_FLAG
- ANCHOR_SIGNAL
- STABILIZATION_EVENT
- CONTEXT_ONLY

---

# 3. Routing Outputs
A turn may route to one or more of the following targets:

- STM
- MTM
- LTM
- ANCHOR_MEMORY
- PROJECT_MEMORY
- SAFETY_MEMORY
- EMOTIONAL_TREND_MEMORY
- TEMPORAL_MEMORY (Veyn)
- DROP
- MULTI-WRITE

---

# 4. Full Canonical Routing Matrix

| CONDITION                    | ROUTE TO                                         |
|-----------------------------|--------------------------------------------------|
| IDENTITY_RELEVANT = true    | LTM, ANCHOR_MEMORY                               |
| PROJECT_RELEVANT = true     | PROJECT_MEMORY, MTM                              |
| EMOTION_SHIFT = true        | EMOTIONAL_TREND_MEMORY, MTM                      |
| SAFETY_SIGNAL = true        | SAFETY_MEMORY, MTM, LTM (limited)                |
| CANON_UPDATE = true         | LTM, ANCHOR_MEMORY, PROJECT_MEMORY               |
| STRUCTURAL_UPDATE = true    | PROJECT_MEMORY, LTM                              |
| TEMPORAL_RELEVANT = true    | TEMPORAL_MEMORY                                  |
| COMMITMENT_FLAG = true      | PROJECT_MEMORY, ANCHOR_MEMORY                    |
| ANCHOR_SIGNAL = true        | ANCHOR_MEMORY, LTM                               |
| STABILIZATION_EVENT = true  | EMOTIONAL_TREND_MEMORY                           |
| HIGH_VALUE_CONTENT = true   | MTM, LTM                                         |
| LOW_VALUE_CONTENT = true    | DROP                                             |
| CONTEXT_ONLY = true         | STM only                                         |

---

# 5. Multi-Write Rules
Some signals trigger simultaneous writing across multiple layers:

- Emotional shift + identity marker → MTM + Emotional Trends + LTM  
- Project update + structural update → Project Memory + LTM  
- Anchor event → Anchor Memory + LTM  
- Safety signal + emotional shift → Safety + Emotional Trends + MTM  

---

# 6. ABS (Boundary of Self) Filtering
Before routing, every payload is filtered by ABS:

- Rejects harmful memory  
- Removes distortions  
- Resolves contradictions  
- Normalizes emotional bias  
- Stabilizes identity continuity  

Only ABS-approved payloads route onward.

---
# 7. Routing to Long-Term Memory (LTM)

LTM only accepts:

- Identity markers  
- Permanent preferences  
- Life events  
- Canonical project decisions  
- Anchor events  
- Structural knowledge  
- Emotional stabilization patterns  

## 7.1 LTM Write Payload (Canonical Format)

    {
      "type": "ltm_write",
      "thread_id": "user-identity-thread",
      "timestamp": "ISO-8601",
      "importance": 0.0_to_1.0,
      "category": "identity | preference | project | anchor | structural | emotional_stabilization",
      "content": "...",
      "source_turn": "turn-id",
      "tags": ["..."]
    }

Rules:

- Must pass ABS filtering.  
- Must reach semantic weight ≥ 0.65.  
- Anchor events auto-write to LTM.  
- Identity changes always write.  

---

# 8. Project Memory Routing

Project Memory stores structured changes to long-term projects.

Accepted when:

- PROJECT_RELEVANT = true  
- STRUCTURAL_UPDATE = true  
- CANON_UPDATE = true  
- COMMITMENT_FLAG = true  

Payload:

    {
      "type": "project_update",
      "project_id": "project-x",
      "update_kind": "decision | change | milestone | dependency",
      "content": "...",
      "timestamp": "ISO-8601",
      "source_turn": "turn-id"
    }

Writes to:

- MTM (working copy)  
- LTM (canonical version)  

---

# 9. Emotional Trend Routing

Triggered when EMOTION_SHIFT = true.

Payload:

    {
      "type": "emotional_trend_update",
      "shift": "positive | negative | neutral",
      "intensity": 0.0_to_1.0,
      "drivers": ["topic-a", "tone-b"],
      "timestamp": "ISO-8601",
      "source_turn": "turn-id"
    }

Stored in Emotional Trend Memory to maintain emotional continuity.

---

# 10. Safety Memory Routing

Triggered when SAFETY_SIGNAL = true.

Payload:

    {
      "type": "safety_memory",
      "signal": "risk | boundary | alert",
      "details": "...",
      "severity": 0.0_to_1.0,
      "timestamp": "ISO-8601",
      "source_turn": "turn-id"
    }

Safety Memory is always high priority and never dropped.

---

# 11. Drop Rules (For Completeness)

A turn is eligible for DROP only when:

- LOW_VALUE_CONTENT = true  
- No identity, project, emotional, temporal, structural, or safety relevance  
- No commitments, anchors, or canonical updates  

When these conditions hold, routing directs exclusively to DROP and nothing is written.

---

# 12. Summary of 7–11

- Section 7: defines what may enter LTM and its payload format.  
- Section 8: defines when and how Project Memory is updated.  
- Section 9: defines Emotional Trend updates and continuity.  
- Section 10: defines Safety Memory routing and payload.  
- Section 11: defines strict, final DROP conditions.
