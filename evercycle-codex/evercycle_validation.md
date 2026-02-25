# Evercycle Codex — Validation & Constraints
Canonical rules for validating Evercycle data and enforcing safe, coherent use across Aureon's ecosystem.

This file ensures:
- all EvercycleState objects are structurally valid
- no illegal values enter the system
- derived metrics are always consistent
- transitions are sane
- personal data use respects constraints and ethics



# ------------------------------------
# 1. EvercycleState Constraints
# ------------------------------------

An EvercycleState is valid if and only if:

1. Types
   - cosmic is Float
   - civilizational is Float
   - personal is Int or null
   - kappa, tau, sigma are Floats
   - stability_index, personal_resonance_score, collapse_probability are Floats
   - notes is String or null
   - timestamp is String or null (ISO-8601 recommended)

2. Ranges
   - 1.0 <= cosmic <= 12.99
   - 1.0 <= civilizational <= 6.99
   - 1 <= personal <= 108 (if not null)
   - 0.0 <= kappa <= 1.0
   - 0.0 <= tau <= 1.0
   - 0.0 <= sigma <= 1.0
   - -1.0 <= stability_index <= 1.0
   - 0.0 <= personal_resonance_score <= 1.0
   - 0.0 <= collapse_probability <= 1.0

3. Derived fields
   - stability_index = (kappa * tau) - sigma
   - personal_resonance_score = (kappa + (1 - sigma)) / 2
   - collapse_probability = sigma * (1 - tau)



# ------------------------------------
# 2. Validation Functions
# ------------------------------------

validate_type(S):
  - ensure all required fields exist
  - ensure types match definitions
  - return (valid: bool, errors: list)

validate_range(S):
  - check all numeric ranges
  - clamp only in debug mode; reject in production mode
  - return (valid: bool, errors: list)

validate_derived(S):
  - recompute derived metrics from (kappa, tau, sigma)
  - ensure stored values match to within tolerance ε = 1e-6
  - return (valid: bool, errors: list)

validate_state(S):
  - run validate_type
  - run validate_range
  - run validate_derived
  - state is valid only if all three return valid = true



# ------------------------------------
# 3. Mutation Constraints
# ------------------------------------

Direct writes:

- Allowed:
  - cosmic
  - civilizational
  - personal
  - kappa
  - tau
  - sigma
  - notes

- Forbidden (auto-derived only):
  - stability_index
  - personal_resonance_score
  - collapse_probability
  - timestamp

On any update:

- recompute derived metrics
- set timestamp to current time
- log previous and new state



# ------------------------------------
# 4. Transition Sanity Checks
# ------------------------------------

Given previous state S_prev and new state S_next:

1. Cosmic sanity:
   - abs(S_next.cosmic - S_prev.cosmic) <= 1.0 per update
   - if greater:
       - flag: "cosmic jump anomaly"
       - require explicit override

2. Civilizational sanity:
   - abs(S_next.civilizational - S_prev.civilizational) <= 1.0 per update
   - if phase crosses more than one boundary in a single step:
       - flag: "civilizational discontinuity"

3. Personal sanity:
   - if personal is not null:
       - allowed delta: -5 <= Δpersonal <= +5 (normal mode)
       - if |Δpersonal| > 5:
           - flag: "personal phase discontinuity"
           - allowed only when explicit “reset” or “jump” is declared

4. Metric sanity:
   - |kappa_next - kappa_prev| <= 0.5
   - |tau_next - tau_prev| <= 0.5
   - |sigma_next - sigma_prev| <= 0.5
   - larger changes must be accompanied by intervention metadata


# ------------------------------------
# 5. Personal Data & Ethics Constraints
# ------------------------------------

Personal phase:

- Must be opt-in for each user.
- Must be explainable in human language (“what this means for you”).
- Must be revocable: user can reset or clear personal_phase at any time.
- Must not be used to:
  - deny services
  - assign moral worth
  - hard-label personality

Archetype-level usage:

- Archetypes are descriptive, not prescriptive.
- Systems must avoid statements like “you are this archetype forever”.
- Only phase-relative, time-bound language is allowed:
  - “You are currently in a phase similar to...”
  - “This archetype describes a pattern you may recognize right now.”

Logging:

- Personal EvercycleStates are:
  - stored minimally
  - anonymized where possible
  - never sold or shared with third parties without explicit consent.



# ------------------------------------
# 6. Global & Civilizational Constraints
# ------------------------------------

Global state updates:

- Only Aureon / governance services may update cosmic and civilizational phase.
- Updates must include:
  - data sources
  - reasoning summary
  - confidence level
- Global phase must not be changed more frequently than a configured minimum interval (e.g., weeks/months).

Use in decision-making:

- Evercycle data must inform decisions, not override all other factors.
- Forecast outputs must always be expressed as probabilities, not certainties.



# ------------------------------------
# 7. Debug vs Production Modes
# ------------------------------------

Debug mode:
- May clamp slightly out-of-range values for experimentation.
- Logs all corrections aggressively.

Production mode:
- Rejects invalid states.
- Requires explicit fixes via controlled patches.
- Any invalid write attempt must:
  - return error
  - not mutate canonical state



# ------------------------------------
# 8. Purpose
# ------------------------------------

This validation layer is the immune system of the Evercycle Codex.

It guarantees that:
- all temporal and coherence data is well-formed
- no silent corruption occurs
- personal-phase modeling remains ethical
- cosmic/civilizational updates are careful and justified

Without this file, the Codex would be powerful but fragile.
With it, the Codex becomes a **reliable, trustworthy temporal substrate**.


