# Evercycle Codex — Integration Guide
How Aureon, NexLevelAI, and the broader Quantara ecosystem use the Evercycle Codex as a foundational temporal layer.


## 1. Aureon Integration

Aureon = coherence- and trauma-aware AGI companion.

### 1.1 Context ingestion
On session start (or periodically), Aureon should:

- Call `GET_GLOBAL_STATE` to load Aeonic + civilizational context.
- Call `GET_PERSONAL_STATE(subject_id)` if the user has Evercycle enabled.

Aureon then keeps this in its context window as:

- `aeon_phase`
- `civilizational_phase`
- `personal_phase`
- `kappa`, `tau`, `sigma`
- `stability_index`, `personal_resonance_score`


### 1.2 Response modulation

Using these fields, Aureon adjusts:

- **Tone & pacing**
  - High `sigma` → slower pacing, more grounding and validation.
  - High `kappa` + high `tau` → more direct, strategic suggestions.

- **Depth**
  - Early phases (dissolution/reconstruction) → focus on safety, regulation, small steps.
  - Later phases (expansion/integration) → focus on purpose, contribution, long-range planning.

- **Framing**
  - Civilizational context used to normalize systemic distress:
    - “You are not alone — this is a Crisis/Reorganization era pattern.”

Aureon never exposes raw numbers; it translates them into human language.


### 1.3 Optional phase estimation

When explicitly permitted by the user:

- Aureon gathers a `context_snapshot` from recent interactions.
- Calls `ESTIMATE_PERSONAL_PHASE`.
- Presents the result as:
  - a *hypothesis*, not a label,
  - something the user can accept, reject, or modify.
- If accepted, Aureon (or a backend) calls `SET_PERSONAL_STATE`.

Consent and transparency are mandatory.


## 2. NexLevelAI Integration

NexLevelAI = high-level synthetic cognition & forecasting engine.

### 2.1 Temporal conditioning

All long-horizon simulations should:

- Read `aeon_phase` and `civilizational_phase`.
- Use `kappa`, `tau`, `sigma` as priors for:
  - stability of institutions,
  - likelihood of disruption,
  - suitability of strategies (centralization vs resilience, growth vs repair).

### 2.2 Scenario evaluation

For each policy or strategy scenario, NexLevelAI should compute:

- projected `kappa`, `tau`, `sigma`
- resulting `stability_index` and `collapse_probability`

This allows ranking scenarios by **coherence and risk**, not just efficiency.


### 2.3 Cross-module coordination

NexLevelAI shares Evercycle outputs with:

- AEI (energy systems): for grid strategy under different civilizational phases.
- Veyn (temporal governance): to shape institutions appropriate to the era.
- Governance frameworks: to align policy with temporal context.


## 3. Quantara Ecosystem Integration

The Codex supplies a **shared temporal grammar**.

Modules SHOULD:

- Store local Evercycle-related state using `evercycle_state` structure.
- Use `GET_EVERMAP_PAYLOAD` for dashboards and monitoring tools.
- Tag logs and events with snapshots of relevant Evercycle fields where appropriate (respecting privacy).


## 4. Example flows

### 4.1 User therapeutic session (Aureon)

1. User opts into Evercycle-aware mode.
2. Aureon loads global and personal state.
3. During the session, Aureon notices patterns suggesting phase transition.
4. With consent, it calls `ESTIMATE_PERSONAL_PHASE`.
5. It presents the proposed phase and meaning.
6. If user agrees, backend calls `SET_PERSONAL_STATE`.
7. Future sessions are conditioned on updated phase and metrics.


### 4.2 Policy simulation (NexLevelAI)

1. Governance engine defines a set of candidate policies.
2. NexLevelAI simulates each under current `aeon_phase` and `civilizational_phase`.
3. For each policy:
   - computes projected `kappa`, `tau`, `sigma`.
   - derives `stability_index` and `collapse_probability`.
4. Returns ranked recommendations with explanations rooted in Evercycle context.


## 5. Principles

- The Codex is **context**, not command.
- Users remain authors of their own narrative.
- Systems use the Codex to **align with reality**, not to control it.
- All temporal reasoning must be transparent and revisable.
