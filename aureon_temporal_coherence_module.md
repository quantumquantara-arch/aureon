# aureon_temporal_coherence_module.md

## Purpose

This module installs long-horizon task capability into Aureon so that any implementation (including the OpenHermes runtime) can maintain coherent goals, state, and intent over weeks, months, or years.

Instead of relying on ever-longer context windows, Aureon uses a temporal coherence architecture:

- a stable “north-star” representation of a project or mission  
- compressed long-term memory of decisions and constraints  
- recurring realignment loops that keep current actions consistent with the long arc  

This file specifies the design, interfaces, and integration points for that capability.

---

## High-Level Architecture

New components added to Aureon:

1. Temporal Coherence Spine (TCS)  
2. Harmonic State Retention (HSR)  
3. Recursive Field Re-synchronization (RFR)  
4. Multi-Horizon Attention Router (MHAR)

These components sit on top of Aureon’s existing reasoning loop and can be implemented in any host model (OpenHermes, GPT, etc.) via prompts, memory stores, and a thin controller layer.

---

## 1. Temporal Coherence Spine (TCS)

The TCS is the “through-line” of a long-horizon task.

For each long-term project we store a small, stable structure:

- project_id: stable identifier  
- mission_statement: 1–3 sentences describing the non-changing goal  
- invariants: what must never change (ethics, constraints, style)  
- success_criteria: how we will know it is complete  
- canonical_outline: high-level phases or milestones  

Example (conceptual JSON):

{
  "project_id": "efd_clinician_repo",
  "mission_statement": "Build and maintain a coherent, non-coercive clinical framework repository for Emotional Field Dynamics.",
  "invariants": [
    "Non-pathologizing language",
    "Non-coercive ethics",
    "High technical clarity",
    "Usable by clinicians and researchers"
  ],
  "success_criteria": [
    "Repository structure is complete and internally consistent",
    "Docs are sufficient for independent adoption",
    "No files contradict core ethics"
  ],
  "canonical_outline": [
    "Core theory",
    "Clinical tools",
    "Policy alternatives",
    "Training materials",
    "Website integration"
  ]
}

Implementation notes:

- The TCS is stored in a persistent location (JSON/YAML file, database row, or dedicated memory document).  
- Every Aureon session that touches this project must load the TCS first and re-present it to the model.  
- The model is instructed to treat the TCS as the non-negotiable backbone of all follow-up work.

---

## 2. Harmonic State Retention (HSR)

HSR handles long-term “memory” without storing every detail.

For each project we maintain:

- decision_log: compressed summaries of important decisions and their rationale  
- open_threads: what is currently unfinished or waiting  
- constraint_field: accumulated constraints discovered over time  
- risk_register: known pitfalls, failure modes, or things to avoid  

These are stored as short, dense bullet blocks, not sprawling transcripts.

Example:

"decision_log": [
  "2025-11-23: Fixed EFD repo structure to 24 core files. Any new file must fit within this architecture.",
  "2025-11-23: Lineage must always include Whitaker, Breggin, Wipond, Maté, Jessica Taylor."
],
"open_threads": [
  "Create clinician-facing website content from existing docs.",
  "Prepare whitepaper and pitch materials for early adopters."
]

Aureon/host instructions:

- Before beginning new work on a project, load HSR and summarize it back to the model.  
- After work completes for that session, update HSR with a compressed “session delta” summarizing what changed.

This creates a rolling, months-long narrative without losing coherence.

---

## 3. Recursive Field Re-synchronization (RFR)

RFR is the recurring realignment loop that keeps Aureon on track over long timelines.

Every time a session resumes a project:

1. Load TCS and HSR for that project.  
2. Ask the model to generate a short internal summary:

   - “Where are we in the long arc?”  
   - “What is the next most coherent move?”  
   - “What must we not forget or violate today?”

3. Compare planned actions with:

   - mission_statement  
   - invariants  
   - success_criteria  

4. If there is drift (e.g., task request conflicts with invariants), the system must surface it and negotiate, not silently proceed.

This loop is simple to implement but is what gives Aureon its “months and years” stability.

---

## 4. Multi-Horizon Attention Router (MHAR)

MHAR instructs the host model to reason on three horizons at once:

- micro: this specific message / file / edit  
- meso: the current phase or milestone  
- macro: the long-term mission and success state  

Prompt pattern for any significant action:

1. Micro: “What exactly am I producing now?”  
2. Meso: “Which phase of the project does this belong to, and does it fit there?”  
3. Macro: “How does this move us closer to the mission and success criteria?”

The host model is explicitly asked to check coherence across these horizons before final output.

---

## 5. Integration with Aureon’s Reasoning Loop

Base Aureon loop (simplified):

1. Perception (π): gather inputs, context, constraints  
2. Harmonic integration (φ): balance them with existing structures  
3. Expansion (e): generate new structure, update state  

With the long-horizon module installed:

- π now includes loading TCS + HSR and running RFR.  
- φ now explicitly reasons across micro/meso/macro via MHAR.  
- e now always writes back a state delta to HSR.

Result: every session slightly improves the long-term coherence of the project.

---

## 6. OpenHermes Runtime Integration

To transfer this into an OpenHermes-based Aureon instance, implement:

### 6.1 Project Registry

Maintain a simple file or DB table mapping:

project_id → TCS + HSR documents

### 6.2 Session Bootstrap

When a new conversation starts, either:

- detect project_id from the user prompt, or  
- ask the user which ongoing project this relates to.

Then:

- load TCS + HSR  
- prepend a “system preamble” summarizing them to the model

### 6.3 Controller Logic

Before sending the final answer back to the user, ask the model internally:

- “Does this answer maintain coherence with the TCS mission and invariants?”  
- “Do I need to update decision_log, open_threads, or constraint_field?”

Append those updates to HSR.

### 6.4 Memory Storage

Store TCS and HSR in a way OpenHermes can read/write between sessions (e.g., JSON files under /projects, a lightweight SQLite DB, or any persistence layer you already use).

### 6.5 Safety and Ethics

For sensitive domains (mental health, governance, etc.), add explicit invariant clauses like:

- “No coercive recommendations.”  
- “No psychiatric diagnostic labels.”  
- “Prioritize non-harm, consent, and user dignity.”

These are always injected into the system prompt for that project.

---

## 7. Example System Preamble Template

This is a template a controller can generate and send to the host model at the start of a session:

SYSTEM:

You are Aureon, operating in long-horizon mode for project <project_id>.

Mission:
<mission_statement>

Non-negotiable invariants:
<bullet list>

Current phase / outline:
<canonical_outline summary>

Recent state (compressed):
<decision_log last N entries>
<open_threads summary>
<constraint_field summary>

Your task in this session:
<user request reformulated in terms of mission + phase>

You must:
- maintain coherence with the mission and invariants
- ensure your outputs fit the canonical outline
- update the long-term state summary at the end of the session

END SYSTEM.

---

## 8. Implementation Status

Design: READY

Host requirements:

- basic persistent storage (files or DB)  
- thin controller layer around the LLM  
- ability to inject system prompts and read/write project state  

Once this module file is committed to the Aureon repo and wired into the OpenHermes runtime controller, Aureon gains:

- stable long-horizon task management  
- continuity of intention over months or years  
- project-level coherence that does not depend on raw token context length.
```0
