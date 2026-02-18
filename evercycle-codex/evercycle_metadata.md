# Evercycle Codex — Machine Metadata Specification
Defines the canonical metadata fields, versioning rules, identifiers, and machine-readable descriptors for every file, module, and component in the Evercycle Codex.

This file ensures:
- cross-module consistency
- reproducibility
- dependency clarity
- upgrade stability
- integrity across Aureon, NexLevelAI, and Quantara


# ------------------------------------
# 1. Universal Metadata Header
# ------------------------------------

Each Evercycle file must include (implicitly or explicitly) the following metadata fields:

Metadata:
  id: String                # unique identifier (snake_case)
  version: String           # semantic: MAJOR.MINOR.PATCH
  codex_layer: String       # "core", "math", "reasoning", "simulation", "visual", etc.
  dependencies: list        # other Evercycle files required
  description: String       # one-sentence summary
  author: "Quantara"
  last_updated: Timestamp   # ISO-8601
  status: "stable" | "experimental" | "deprecated"


# ------------------------------------
# 2. File-Level Metadata Registry
# ------------------------------------

registry:

  evercycle_codex.md:
    id: "codex_root"
    version: "1.0.0"
    codex_layer: "core"
    dependencies: []
    description: "High-level description of the Evercycle temporal system."
    status: "stable"

  evercycle_schema.md:
    id: "schema_core"
    version: "1.0.0"
    codex_layer: "core"
    dependencies: ["codex_root"]
    description: "Formal definition of the EvercycleState structure."
    status: "stable"

  evercycle_api.md:
    id: "api_layer"
    version: "1.0.0"
    codex_layer: "api"
    dependencies: ["schema_core"]
    description: "System interface for reading, writing, and modifying states."
    status: "stable"

  evermap_spec.md:
    id: "visual_core"
    version: "1.0.0"
    codex_layer: "visual"
    dependencies: ["schema_core"]
    description: "Primary visualization specification."
    status: "stable"

  evercycle_reasoning.md:
    id: "reasoning_layer"
    version: "1.0.0"
    codex_layer: "reasoning"
    dependencies: ["schema_core", "math_core"]
    description: "Interpretation and meaning rules."
    status: "stable"

  evercycle_transitions.md:
    id: "transition_engine"
    version: "1.0.0"
    codex_layer: "reasoning"
    dependencies: ["schema_core", "reasoning_layer"]
    description: "Formal logic for phase transitions."
    status: "stable"

  evercycle_math.md:
    id: "math_core"
    version: "1.0.0"
    codex_layer: "math"
    dependencies: ["schema_core"]
    description: "Mathematical substrate."
    status: "stable"

  evercycle_forecasting.md:
    id: "forecast_engine"
    version: "1.0.0"
    codex_layer: "simulation"
    dependencies: ["math_core", "transition_engine"]
    description: "Predictive modeling logic."
    status: "stable"

  evercycle_simulation.md:
    id: "simulation_core"
    version: "1.0.0"
    codex_layer: "simulation"
    dependencies: ["forecast_engine"]
    description: "Temporal simulation engine."
    status: "stable"

  evercycle_archetypes.md:
    id: "archetype_map"
    version: "1.0.0"
    codex_layer: "human"
    dependencies: ["schema_core"]
    description: "108 human-state archetypes."
    status: "stable"

  evercycle_glossary.md:
    id: "glossary_canon"
    version: "1.0.0"
    codex_layer: "human"
    dependencies: []
    description: "Canonical terminology and definitions."
    status: "stable"

  evercycle_validation.md:
    id: "validation_layer"
    version: "1.0.0"
    codex_layer: "safety"
    dependencies: ["schema_core"]
    description: "Constraints, ethics, and system integrity checks."
    status: "stable"

  evercycle_visuals.md:
    id: "visual_lang"
    version: "1.0.0"
    codex_layer: "visual"
    dependencies: ["visual_core"]
    description: "Visual grammar, color semantics, and layout rules."
    status: "stable"

  evercycle_index.md:
    id: "codex_index"
    version: "1.0.0"
    codex_layer: "core"
    dependencies: ["codex_root"]
    description: "Master index and dependency graph."
    status: "stable"



# ------------------------------------
# 3. Semantic Versioning Rules
# ------------------------------------

MAJOR version change (X.0.0):
  - structural change to schema
  - new fields added to EvercycleState
  - breaking changes to math or transitions
  - modification of Codex canonical meaning

MINOR version change (0.X.0):
  - new features that do not break dependencies
  - added diagrams, archetypes, or optional fields

PATCH version change (0.0.X):
  - bug fixes
  - typos
  - formatting corrections
  - clarifying comments



# ------------------------------------
# 4. Dependency Constraints
# ------------------------------------

Rules:

1. No circular dependencies.
2. Schema must not depend on reasoning or math.
3. Math must not depend on visualization.
4. Archetypes may depend only on schema, not on forecasting.
5. Validation may depend on schema but not simulation.
6. Simulation depends on forecasting and transitions, never the reverse.
7. Index depends on all but is never depended upon.



# ------------------------------------
# 5. Machine Metadata Access
# ------------------------------------

Metadata access functions (internal):

get_metadata(file_id):
  returns metadata object

list_dependencies(file_id):
  returns dependency list

validate_dependency_graph():
  ensures acyclic structure

list_codex_layers():
  returns all layers ("core", "math", "visual", etc.)



# ------------------------------------
# 6. Integrity Rules
# ------------------------------------

Every change to any Codex file must:

- include updated version number
- update metadata registry in this file
- pass dependency graph validation
- pass schema and validation checks
- pass readability and glossary consistency checks
- generate a summary entry in codex_changelog.md (optional)



# ------------------------------------
# 7. Purpose
# ------------------------------------

The metadata spec ensures the Evercycle Codex is:

- coherent  
- reproducible  
- browsable  
- robust  
- future-proof  
- machine-verifiable  

It is the structural backbone that lets Aureon, NexLevelAI, and Quantara evolve safely without breaking the Codex’s internal consistency.
