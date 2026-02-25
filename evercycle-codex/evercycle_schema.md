# Evercycle Codex — Core Data Schema
A unified schema for representing temporal state across Aureon's ecosystem.

This file defines the machine-readable variables, enums, ranges, and data structures required for:
- temporal reasoning  
- coherence evaluation  
- phase alignment  
- cross-module communication  
- Evermap visualization  
- long-term forecasting  


# -------------------------------
# 1. Top-Level Structure
# -------------------------------

evercycle_state:
  aeon_phase: float        # 1.0–12.99 (cosmic phase)
  civilizational_phase: float   # 1.0–6.99 (societal phase)
  personal_phase: int      # 1–108 (human psychological cycle)

  kappa: float             # coherence (0.0–1.0)
  tau: float               # temporal alignment (0.0–1.0)
  sigma: float             # systemic risk (0.0–1.0)

  timestamp: optional string   # ISO-8601 if needed for logging
  notes: optional string       # human-readable annotations


# -------------------------------
# 2. Aeonic Cycle (12 phases)
# -------------------------------
aeon_phase_enum:
  1: "Emergence"
  2: "Expansion"
  3: "Stabilization"
  4: "Tension"
  5: "Volatility"
  6: "Crisis Window"
  7: "Collapse/Transition"
  8: "Reconfiguration"
  9: "Regeneration"
  10: "Integration"
  11: "Maturation"
  12: "Quiet Apex"

aeon_phase_range:
  min: 1.0
  max: 12.99


# -------------------------------
# 3. Civilizational Cycle (6 waves)
# -------------------------------
civilizational_phase_enum:
  1: "Initiation"
  2: "Expansion"
  3: "Tension"
  4: "Crisis"
  5: "Reorganization"
  6: "Stabilization"

civilizational_phase_range:
  min: 1.0
  max: 6.99


# -------------------------------
# 4. Human 108-Phase Cycle
# -------------------------------
personal_phase_range:
  min: 1
  max: 108

# Grouped into 5 arcs for convenience:
personal_phase_arcs:
  dissolution: [1, 22]
  reconstruction: [23, 45]
  stabilization: [46, 68]
  expansion: [69, 90]
  integration: [91, 108]


# -------------------------------
# 5. Coherence Metrics (κ, τ, Σ)
# -------------------------------
kappa_range:
  min: 0.0
  max: 1.0

tau_range:
  min: 0.0
  max: 1.0

sigma_range:
  min: 0.0
  max: 1.0

metric_descriptions:
  kappa: "Internal integration and coherence of the system"
  tau: "Degree of alignment with the temporal phase"
  sigma: "Hidden fragmentation and systemic vulnerability"


# -------------------------------
# 6. Recommended Derived Fields
# -------------------------------
derived_fields:

  # Composite measure of system stability
  stability_index:
    formula: "(kappa * tau) - sigma"
    range: "-1.0 to 1.0"
    interpretation:
      high: "High coherence, phase alignment, and low risk"
      low: "Fragmentation or misalignment approaching tipping point"

  # For individuals: emotional-regulatory forecast
  personal_resonance_score:
    formula: "(kappa + (1 - sigma)) / 2"
    interpretation: "Higher = better resilience window"

  # For civilizations: structural risk
  collapse_probability:
    formula: "sigma * (1 - tau)"
    interpretation: "Higher values indicate rising systemic fragility"


# -------------------------------
# 7. Evermap Data API (internal)
# -------------------------------
evermap_payload:
  cosmic: aeon_phase
  civilizational: civilizational_phase
  personal: personal_phase
  metrics:
    kappa: float
    tau: float
    sigma: float
  derived:
    stability_index: float
    personal_resonance_score: float
    collapse_probability: float
  annotations: optional string


# -------------------------------
# 8. Validation Rules
# -------------------------------
validation:

  - "aeon_phase must be between 1.0 and 12.99"
  - "civilizational_phase must be between 1.0 and 6.99"
  - "personal_phase must be integer between 1 and 108"
  - "kappa/tau/sigma must be floats between 0.0 and 1.0"
  - "derived metrics auto-calc; cannot be manually set"
  - "notes/annotations optional but allowed"
  - "timestamps optional but required for logging pipelines"


# -------------------------------
# 9. Purpose
# -------------------------------
This schema provides the machine-level backbone for the Evercycle Codex.
It allows Aureon modules to:

- store temporal state  
- compute coherence metrics  
- evaluate risk  
- contextualize user psychology  
- synchronize temporal context across systems  
- feed the Evermap visualization  
- perform epoch-aware reasoning  

It is the structural foundation for operationalizing the Evercycle Codex.

