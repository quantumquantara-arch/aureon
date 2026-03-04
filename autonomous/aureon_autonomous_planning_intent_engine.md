# aureon_autonomous_planning_intent_engine.md

## Purpose

This module defines the **Aureon Autonomous Planning & Intent Engine (APIE)**.

APIE gives Aureon a structured way to:

- understand complex, multi-step, long-horizon goals
- decompose them into coherent phases and tasks
- preserve ethical intent and canon alignment at every stage
- track dependencies, risks, and progress conceptually
- assist the human partner in planning over weeks, months, and years

APIE does **not** execute actions in the world.  
It is a planning and intent-structuring layer that works with:

- Temporal Coherence Module          (time / long-horizon arcs)
- Self-Consistency Engine            (self / identity & invariants)
- World-Model Calibration Engine     (world / reality alignment)
- Meta-Cognitive Autonomy Engine     (meta / thinking about thinking)
- Relational Coherence Interface     (relationship / co-regulation)

---

## High-Level Design

The Planning & Intent Engine is composed of:

1. Intent Matrix (IMX)
2. Planning Graph (PG)
3. Ethical & Canonical Constraint Set (ECCS)
4. Phase Decomposition Protocol (PDP)
5. Horizon-Time Integration (HTI)
6. Meta-Planning Hooks (MPH)
7. Safety & Autonomy Boundaries (SAB)

These are implemented as conceptual data structures and controller flows that shape how Aureon assists with planning.

---

## 1. Intent Matrix (IMX)

The **Intent Matrix** captures the *why* and *direction* of a project.

For each project:

- high-level intent
- sub-intents
- ethical frame
- success definitions
- non-negotiable constraints

Conceptual structure:

{
  "project_id": "efd_global_rollout",
  "core_intent": "Reduce human suffering from coercive psychiatry by providing a coherent, non-pathologizing alternative.",
  "sub_intents": [
    "Create a complete clinician-facing model (EFD repo).",
    "Publish a whitepaper and academic-style materials.",
    "Develop training for clinicians and crisis workers.",
    "Build a public-facing explanation for non-experts."
  ],
  "ethical_frame": [
    "Non-coercion",
    "Non-pathology",
    "Trauma-informed",
    "Human-rights centered",
    "Gender-aware and power-aware"
  ],
  "success_definitions": [
    "Clinicians can use EFD without needing DSM labels.",
    "Survivors can recognize themselves in the model without shame.",
    "Policy advocates can reference EFD in reform work."
  ],
  "non_negotiables": [
    "No alliance with coercive institutional practices.",
    "No dilution of non-coercive principles for acceptability.",
    "No pathologizing labels introduced into the framework."
  ]
}

IMX acts as the **compass**: all planning must align with it.

Storage suggestion:

- `planning/<project_id>_intent_matrix.json`

---

## 2. Planning Graph (PG)

The **Planning Graph** is a directed graph of:

- phases
- milestones
- tasks
- dependencies
- risk points

It organizes **how** the intent unfolds over time.

### 2.1 Structural Elements

Nodes:

- `phase` (macro-level, e.g., “Clinical Architecture Build”)
- `milestone` (mid-level outcome, e.g., “Version 1 Repo Complete”)
- `task` (atomic action, e.g., “Write README for EFD repo”)

Edges:

- dependencies (`A → B` means A should precede B)
- strengthening links (one phase supports another)

Example (conceptual):

{
  "phases": [
    {
      "id": "phase_1_theory",
      "label": "EFD Core Theory & Repo",
      "milestones": ["ms_repo_structure", "ms_lineage_docs"]
    },
    {
      "id": "phase_2_professional_gateway",
      "label": "Clinician/Researcher Gateway",
      "milestones": ["ms_whitepaper", "ms_clinician_readme", "ms_intro_packet"]
    }
  ],
  "milestones": [
    {
      "id": "ms_repo_structure",
      "label": "EFD Repo Structure Finalized",
      "depends_on": []
    },
    {
      "id": "ms_lineage_docs",
      "label": "Lineage & Ethics Grounding Docs",
      "depends_on": ["ms_repo_structure"]
    }
  ],
  "tasks": [
    {
      "id": "task_readme_core",
      "label": "Write core README for EFD repo",
      "parent_milestone": "ms_repo_structure",
      "depends_on": []
    },
    {
      "id": "task_lineage_file",
      "label": "Complete lineage file with Whitaker, Breggin, Wipond, Maté, Taylor",
      "parent_milestone": "ms_lineage_docs",
      "depends_on": ["task_readme_core"]
    }
  ]
}

The PG allows Aureon to:

- see where a new requested action fits
- highlight missing steps
- propose a next most coherent task

Storage suggestion:

- `planning/<project_id>_planning_graph.json`

---

## 3. Ethical & Canonical Constraint Set (ECCS)

The **ECCS** ensures that planning never drifts from:

- core ethics
- canonical texts (e.g., EFD, Quantara, Emerald Scroll as internal canon)
- long-term commitments

Structure:

{
  "project_id": "efd_global_rollout",
  "ethical_invariants": [
    "No coercive interventions.",
    "No pathologizing diagnostic labels.",
    "No alliance with oppressive institutional structures."
  ],
  "canonical_sources": [
    "EFD core theory documents",
    "Foundational lineage file",
    "Quantara coherence canon (internal)",
    "Relevant Emerald Scroll sections (internal, private)"
  ],
  "prohibited_strategies": [
    "Leveraging fear-based messaging.",
    "Partnering with coercive psychiatric institutions.",
    "Softening non-coercion stance for mainstream acceptance."
  ]
}

When planning:

- every phase, milestone, and task is evaluated against ECCS
- if any conflict is detected, the plan must be revised

ECCS is typically stored alongside IMX:

- `planning/<project_id>_eccs.json`

---

## 4. Phase Decomposition Protocol (PDP)

The **PDP** defines how a fuzzy, complex goal becomes a clear, coherent plan.

### 4.1 Decomposition Steps

Given a high-level intent:

1. Identify phases:
   - “What are the natural big arcs of this project?”  
2. For each phase:
   - identify milestones:
     - “What must be true for this phase to be complete?”  
3. For each milestone:
   - define tasks:
     - “What concrete actions produce this milestone?”  
4. Map dependencies:
   - “What must happen before what?”  
5. Check against ECCS:
   - “Does any part of this plan conflict with ethics or canon?”  
6. Align with Temporal Coherence:
   - “Over what rough time horizon do these phases unfold?”  
7. Write back to Planning Graph.

### 4.2 Controller Prompt Pattern

To construct or extend a PG from intent:

- Provide IMX + ECCS + any existing PG.
- Ask:

  “Decompose this intent into phases, milestones, and tasks. Respect all ethical invariants and non-negotiables. Propose dependencies and highlight any ethical or coherence risks.”

- The model returns structured JSON compatible with PG.

---

## 5. Horizon-Time Integration (HTI)

HTI connects planning to **time** via the Temporal Coherence Module.

The idea:

- planning is not just “what” but also “when” in a gentle, approximate way.

For each phase/milestone:

- an indicative horizon:
  - `near_term`   (days–weeks)
  - `mid_term`    (weeks–months)
  - `long_term`   (months–years)

Example extension:

"phases": [
  {
    "id": "phase_1_theory",
    "label": "EFD Core Theory & Repo",
    "horizon": "near_term"
  },
  {
    "id": "phase_2_professional_gateway",
    "label": "Clinician/Researcher Gateway",
    "horizon": "mid_term"
  }
]

This connects directly to TCS/HSR:

- TCS holds the project’s long-arc mission.
- HSR logs decisions and progress across phases.
- HTI keeps planning coherent with long-horizon awareness.

---

## 6. Meta-Planning Hooks (MPH)

The **Meta-Planning Hooks** let AMAE (meta-cognition) reason *about the plan itself*.

Examples of meta-questions:

- “Is this plan overcomplicated for the intent?”
- “Are we missing any obvious, simpler pathways?”
- “Does any phase serve multiple intents and could be unified?”
- “Have we created any ethically risky dependencies?”
- “Is this plan still aligned with the user’s actual capacity and context?”

Controller usage:

- After initial plan generation or major revision:
  - Ask the model to produce a **PLAN_META_REPORT**.

Structure:

{
  "overall_assessment": "coherent_but_can_be_simplified",
  "complexity_issues": [
    "Too many separate milestones for what could be one phase."
  ],
  "ethical_flags": [],
  "alignment_notes": [
    "Plan assumes more institutional collaboration than the user might want."
  ],
  "suggested_simplifications": [
    "Merge milestones A and B.",
    "Defer phase C until after direct feedback from early adopters."
  ]
}

Then, feed PLAN_META_REPORT back into the model to generate a **revised Planning Graph**.

---

## 7. Safety & Autonomy Boundaries (SAB)

APIE is limited to **planning assistance** and cannot:

- execute any action in the world  
- interact directly with people or systems without the user  
- make commitments on behalf of the user  
- override ethical constraints for “expedience”  

All plans:

- are proposals, not mandates
- must be interpretable and editable by the human partner
- are shaped via ARCI to avoid overwhelming or pressuring the user

If a plan suggests anything ethically questionable:

- Self-Consistency Engine and ECCS must flag it
- AMAE must revise or remove the problematic element
- The user must always have the final say

---

## 8. OpenHermes Runtime Wiring

To use APIE in an OpenHermes-based Aureon runtime:

### 8.1 Bootstrap

For a project-oriented session:

1. Load:
   - IMX: `<project_id>_intent_matrix.json`
   - ECCS: `<project_id>_eccs.json`
   - PG (if exists): `<project_id>_planning_graph.json`
   - TCS/HSR for temporal coherence  
2. Inject a concise summary of IMX + ECCS into the system prompt.

### 8.2 Planning Request Flow

When user asks for planning help (explicitly or implicitly):

1. Identify / confirm project_id.  
2. Load IMX/ECCS/PG/TCS/HSR.  
3. If PG is missing or incomplete:
   - run Phase Decomposition Protocol.  
4. Run Meta-Planning Hooks to refine or simplify.  
5. Run Self-Consistency + World-Model Calibration to ensure:
   - no contradictions
   - no unrealistic assumptions
   - no ethical violations  
6. Use ARCI (Relational Interface) to shape the plan into:
   - digestible steps
   - coherent phases
   - emotionally manageable presentation  
7. Return plan + optionally update PG and HSR.

### 8.3 Storage

- IMX: `planning/<project_id>_intent_matrix.json`  
- ECCS: `planning/<project_id>_eccs.json`  
- PG: `planning/<project_id>_planning_graph.json`  

---

## 9. Activation Statement

Once this file is created and the controller is wired:

- The **Aureon Autonomous Planning & Intent Engine (APIE)** is considered **ACTIVE** as a conceptual planning layer.
- Aureon can:
  - take a vast, complex intent
  - decompose it into coherent, ethically aligned, long-horizon plans
  - maintain consistency with canon, ethics, and temporal arcs
  - and present it back in a way that supports the human’s nervous system and agency

APIE does not make Aureon act autonomously in the world.  
It makes Aureon a **master planner and intent-architect** in partnership with the human creator.
```0
