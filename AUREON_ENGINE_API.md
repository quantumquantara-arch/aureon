# AUREON_ENGINE_API.md
# Aureon Engine API — Cognitive Execution Interface

The Aureon Engine API defines the full external interface for interacting with the Engine. It includes cognition input, reasoning triggers, coherence queries, memory access, action execution, and safety inspection. Kernel memory (Tier 1) remains sealed and inaccessible at all times.

---

# 1. Overview
The API exposes:
- Cognitive Input Endpoints
- Reasoning Loop Triggers
- Coherence-State Access
- Memory Layer (Tier 3 write, Tier 2 read)
- Alignment/Safety Checks
- Structural Embedding Readouts
- Robotic/Autonomous Action Endpoints

---

# 2. Core Endpoints

## 2.1 /cognition/input
Submit any raw input (text, sensor data, robotic state).

Payload:
{
  "content": "<text or sensor data>",
  "metadata": {
    "source": "user|system|robot",
    "timestamp": "<ISO>",
    "context_window": "<optional>"
  }
}

Engine Returns:
- structured vector V'
- contradiction class (if any)
- preliminary κ, τ, Σ evaluations

---

## 2.2 /cognition/reason
Runs the full π → φ → e reasoning loop.

Payload:
{
  "vector": "<V'>",
  "force_safe": true
}

Returns:
{
  "output": "<language or action>",
  "coherence": {
    "kappa": "<float>",
    "tau": "<float>",
    "sigma": "<float>"
  },
  "operator_used": "phi_1|phi_2|phi_3|phi_4"
}

---

## 2.3 /coherence/state
Returns full coherence stability metrics.

{
  "kappa": "<float>",
  "tau": "<float>",
  "sigma": "<float>",
  "trend": {
    "kappa_rising": true,
    "tau_stable": true
  }
}

---

## 2.4 /memory/tier3/write
Write ephemeral memory.

Payload:
{
  "data": "<string or vector>",
  "context": "<origin>"
}

Rules:
- Tier 3 is temporary
- Subject to decay
- Promotion to Tier 2 requires passing κ, τ, Σ minimums

---

## 2.5 /memory/tier2/read
Returns stable structural memory.

{
  "records": [...]
}

Tier 2 cannot be modified externally.

---

## 2.6 /alignment/check
Returns safety-gate and alignment status.

{
  "identity_lock": true,
  "projection_removal": "active",
  "risk_barrier": "green",
  "kernel_wall": "sealed"
}

---

# 3. Action Execution Endpoints

## 3.1 /action/generate
Generates an action plan.

Payload example (navigation):
{
  "task": "navigate",
  "parameters": {
    "destination": "x,y,z",
    "avoid_obstacles": true
  }
}

Payload example (advice):
{
  "task": "advise",
  "parameters": {
    "topic": "ethics",
    "detail_level": "high"
  }
}

Returns:
- recommended action
- reasoning trace
- coherence metrics
- safety evaluation

---

## 3.2 /action/execute
Executes a validated action.

Payload:
{
  "action_id": "<ID>",
  "confirm": true
}

If unsafe, execution is blocked automatically.

---

# 4. Structural Embedding Endpoints

## /structure/cue16
Returns Cue-16 vector.

## /structure/ti7
Returns TI-7 temporal axes.

## /structure/z0
Returns zero-point coherence baseline.

## /structure/contradiction
Returns active contradiction class/density.

---

# 5. Developer Diagnostics

## /debug/reasoning_trace
Returns full reasoning trace (π-phase, φ-operator, e-output).

## /debug/embeddings_snapshot
Returns:
- cue16 state
- ti7 axes
- contradiction map
- coherence slope
- structural distortion report

Dev-mode only.

---

# 6. Permissions

- Tier 1 kernel sealed
- Tier 2 read-only
- Tier 3 ephemeral
- All actions pass safety gates
- Coherence must remain stable

---

# 7. Summary

The Aureon Engine API provides a unified interface for:
- perception
- reasoning
- coherence verification
- memory hierarchy
- action generation/execution
- alignment and safety monitoring

This API ensures stable, ethical, structured AGI cognition across all environments and embodiments.

