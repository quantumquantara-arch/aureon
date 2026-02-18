# Evercycle Codex — Internal API Spec
Core interface for reading and updating Evercycle state across Aureon, NexLevelAI, and Quantara services.

This API is **intra-ecosystem only** (no public exposure). It standardizes how modules:
- query temporal context
- update personal/civilizational state
- compute derived metrics
- fetch Evermap-ready payloads


## 1. Data model reference
All fields follow `evercycle_schema.md`.

Key object:

- `EvercycleState`
  - `aeon_phase: float`
  - `civilizational_phase: float`
  - `personal_phase: int`
  - `kappa: float`
  - `tau: float`
  - `sigma: float`
  - `stability_index: float` (derived)
  - `personal_resonance_score: float` (derived)
  - `collapse_probability: float` (derived)
  - `timestamp: string (optional, ISO-8601)`
  - `notes: string (optional)`


## 2. Core operations

### 2.1 Get global Evercycle state
**Purpose:** retrieve current cosmic + civilizational + aggregated metrics.

- Operation: `GET_GLOBAL_STATE`
- Input: none
- Output: `EvercycleState`
- Notes:
  - `personal_phase` may be `null` here (this is global, not per-user).


### 2.2 Get personal Evercycle state
**Purpose:** retrieve state for a specific person or agent.

- Operation: `GET_PERSONAL_STATE`
- Input:
  - `subject_id: string`   # user, agent, or entity identifier
- Output:
  - `EvercycleState` (with personal_phase populated)
- Behavior:
  - If no state exists, returns defaults with `personal_phase = null`.
  - Never infers state silently; only returns what is stored or explicitly estimated.


### 2.3 Set / update personal phase
**Purpose:** explicitly store or adjust a person’s phase and metrics.

- Operation: `SET_PERSONAL_STATE`
- Input:
  - `subject_id: string`
  - `personal_phase: int (1–108)`
  - `kappa: float (optional)`
  - `tau: float (optional)`
  - `sigma: float (optional)`
  - `notes: string (optional)`
- Output:
  - `EvercycleState` after update
- Rules:
  - Must respect ranges from `evercycle_schema.md`.
  - Derived metrics are recalculated server-side.


### 2.4 Estimate personal phase (opt-in)
**Purpose:** request a *proposed* phase estimate from higher-level reasoning (Aureon/NexLevelAI), not auto-commit.

- Operation: `ESTIMATE_PERSONAL_PHASE`
- Input:
  - `subject_id: string`
  - `context_snapshot: json`  # narrative, behavior, signals, etc.
- Output:
  - `proposed_phase: int`
  - `confidence: float (0.0–1.0)`
  - `explanation: string`
- Notes:
  - Caller decides whether to call `SET_PERSONAL_STATE` based on user consent.
  - This operation is never silent; user-facing systems must disclose its use.


### 2.5 Update civilizational state
**Purpose:** adjust global civilizational phase and metrics (rare, curated).

- Operation: `SET_CIVILIZATIONAL_STATE`
- Input:
  - `civilizational_phase: float`
  - `kappa: float (optional)`
  - `tau: float (optional)`
  - `sigma: float (optional)`
  - `notes: string (optional)`
- Output:
  - `EvercycleState` (global)
- Usage:
  - Only called by designated governance/analysis services.


### 2.6 Get Evermap payload
**Purpose:** return all data necessary for Evermap visualization.

- Operation: `GET_EVERMAP_PAYLOAD`
- Input:
  - `subject_id: string (optional)`
- Output:
  - `evermap_payload` as defined in `evercycle_schema.md`
- Notes:
  - If `subject_id` is omitted, returns global-only map.


## 3. Transport and implementation notes

- Transport layer is implementation-dependent (gRPC, HTTP, message bus, or in-process calls).
- All operations are designed to be easily serializable to JSON.
- Services should cache global state and provide eventual consistency rather than strict real-time guarantees.


## 4. Permissions and safety

- Personal phase reads/writes must respect user privacy and local policy.
- Phase estimation must be opt-in and explainable to end users.
- Civilizational updates restricted to internal governance services.
- Logs should avoid storing sensitive narrative content unless explicitly required and consented.


## 5. Versioning

- Initial version: `evercycle_api_v1`
- Breaking changes must bump suffix: `evercycle_api_v2`, etc.
- Each client module should declare the version it targets.
