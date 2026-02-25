# Cue-16 Vector Specification

Each of the 16 structural cues is defined as either a binary feature (present/absent) or a graded feature (low → high intensity).

These cues represent structural patterns in a user’s message, not emotions themselves. They are derived during π-phase and used to predict contradictions in φ-phase.

---

## Cue Categories

The 16 cues are grouped into three categories:

- **Temporal Cues (1–6)**  
  These indicate how the user is positioned in time (past, future, collapsed, etc.).

- **Duality Cues (7–11)**  
  These indicate binary framing, internal conflict, or mutually exclusive options.

- **Identity Cues (12–16)**  
  These indicate self-blame, self-doubt, or identity compression.

---

## Vector Form

All 16 cues are represented as a single feature vector:

`Q = [q1, q2, q3, ..., q16]`

Where:

- `qi = 0` if the cue is not detected  
- `0 < qi ≤ 1` if the cue is detected with graded intensity  

This makes Cue-16 suitable for continuous models (e.g., embeddings, neural nets) as well as for simpler rule-based systems.

---

## Usage in NextLevelAI

The Cue-16 vector is used to:

- Estimate likelihood of internal contradiction  
- Route the input into the correct φ-phase processor  
- Inform temporal and emotional interpretation  
- Support downstream contradiction prediction and resolution

In combination with the TI-7 temporal axes and the emotional topology space, Cue-16 helps encode the structural “shape” of a user’s mental state in a mathematically tractable form.
