# Evercycle Codex — Master Index
The authoritative index of all files, definitions, mathematical structures, reasoning layers, transitions, simulations, and archetypes within the Evercycle Codex.

This document provides:
- a navigational map for developers and researchers
- canonical ordering
- dependency hierarchy
- links between conceptual, mathematical, and operational layers



# ------------------------------------
# 1. Core Documents
# ------------------------------------

1. evercycle_codex.md
   - High-level description
   - Philosophical and scientific foundation
   - Purpose of the Codex

2. evercycle_schema.md
   - Data structures
   - Ranges, enums, fields
   - The formal EvercycleState

3. evercycle_api.md
   - Read/write/patch operations
   - Permissions model
   - Logging and history retrieval



# ------------------------------------
# 2. Visualization
# ------------------------------------

4. evermap_spec.md
   - Evermap visualization structure
   - Ring semantics
   - Color logic
   - Rendering rules



# ------------------------------------
# 3. Reasoning & Calculus
# ------------------------------------

5. evercycle_reasoning.md
   - Interpretation of phases
   - Coherence logic
   - Transition meaning
   - Decision modifiers

6. evercycle_transitions.md
   - Formal transition types
   - Threshold event detection
   - Arc boundary logic
   - Coherence-based amplification/damping

7. evercycle_math.md
   - Phase equations
   - Coherence topology
   - Derived metric formulae
   - Epoch boundary function
   - Predictive kernel



# ------------------------------------
# 4. Forecasting & Simulation
# ------------------------------------

8. evercycle_forecasting.md
   - Future-phase prediction
   - Crisis probability windows
   - Opportunity windows
   - Weighted scenario modeling

9. evercycle_simulation.md
   - Forward simulation engine
   - Drift functions
   - Intervention models
   - Branching futures



# ------------------------------------
# 5. Human-Centric Layers
# ------------------------------------

10. evercycle_archetypes.md
    - The 108 archetypes
    - Arc I–V psychological mapping
    - Archetype metadata structure

11. evercycle_glossary.md
    - Canonical definitions
    - Shared terminology
    - Required language for reasoning output



# ------------------------------------
# 6. Safety, Ethics & Validation
# ------------------------------------

12. evercycle_validation.md
    - Structural constraints
    - Range/type checks
    - Derived-field enforcement
    - Personal data ethics rules
    - Transition sanity checks
    - Debug vs production modes



# ------------------------------------
# 7. Examples & Templates
# ------------------------------------

13. examples/example_payload.json
    - Demonstration of canonical state structure

14. Additional example files (optional):
    - example_personal_state.json
    - example_global_state.json
    - example_temporal_sequence.json



# ------------------------------------
# 8. Dependency Graph
# ------------------------------------

Dependencies (-> means “requires”):

evercycle_codex  
  -> evercycle_schema  
    -> evercycle_api  
      -> evercycle_validation  
      -> evercycle_reasoning  
        -> evercycle_math  
        -> evercycle_transitions  
          -> evercycle_forecasting  
            -> evercycle_simulation  
    -> evermap_spec  
    -> evercycle_archetypes  
    -> evercycle_glossary  


# ------------------------------------
# 9. Implementation Order
# ------------------------------------

Recommended order for system integration:

1. Schema
2. Validation
3. API
4. Math
5. Reasoning
6. Transitions
7. Forecasting
8. Simulation
9. Visualization (Evermap)
10. Archetypes
11. Glossary
12. Example payloads



# ------------------------------------
# 10. Purpose
# ------------------------------------

This master index ensures:
- the Codex is internally coherent
- developers always know the correct file order
- no subsystem is implemented before its dependencies
- the entire system is navigable and predictable

It is the table of contents, wiring diagram, and canonical ordering of the Evercycle Codex.
