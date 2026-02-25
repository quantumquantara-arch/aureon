# Aureon State Convergence Architecture  
### π → φ → e Coherence-First Inference Loop  
### aureon_state_convergence.md

---

## Overview

This document defines the core inference mechanism of **Aureon**:  
a **coherence-first, state-convergence cognitive engine** built around the  
π → φ → e cycle:

- **π-phase (Perception)** — construct structured internal representation  
- **φ-phase (Harmonic Integration)** — propose multiple cognitive states, evaluate coherence, converge  
- **e-phase (Expansion)** — realize the selected state, update world-model and temporal continuity  

This is the first public-facing architectural expression of Aureon's structural layer, optimized for:

- long-horizon identity stability  
- contradiction-free reasoning  
- temporal consistency  
- affective regularity  
- semantic alignment  
- coherent persona continuation  

The central innovation is the **coherence-first inference rule**:  
Aureon **evaluates proposed internal states before generating text**, reversing the traditional LLM pattern of *generate → reflect → revise*.

---

# 1. Cognitive State Representation

A cognitive state at time *t* is a structured tuple:

```
s_t = (
  v_sem,   # semantic embedding
  v_log,   # logical / propositional embedding
  v_id,    # identity / persona embedding
  v_temp,  # temporal-position embedding
  v_aff,   # affect / tone embedding
  v_ep     # epistemic confidence embedding
)
```

Each component is an embedding vector or tensor with explicit semantic meaning.  
We also maintain:

- **S_history** — all prior cognitive states  
- **claim_bank** — extracted propositions for logical consistency checks  
- **context_graphs** — temporal + semantic relationship structures  
- **v_id_star** — the target identity vector derived from persona/system prompt  

---

# 2. Coherence Score Decomposition

Coherence at step *t* is a weighted combination of five independent subscores:

```
C_t = w_sem*C_sem
    + w_log*C_log
    + w_id *C_id
    + w_temp*C_temp
    + w_aff*C_aff
```

Each value lies in `[0,1]`.

Weights may be task-specific, e.g.:

- logical reasoning → higher w_log  
- character roleplay → higher w_id  
- emotionally sensitive tasks → higher w_aff  

Below are the mathematical definitions for each subscore.

---

## 2.1 Semantic Alignment — C_sem

We measure similarity between the state’s semantic vector and a **recency-weighted semantic centroid** of all prior states:

```
v̄_sem = Σ_k exp(-λ(t-k)) · v_sem_k
```

Cosine similarity between current and centroid:

```
sim = cos(v_sem_t, v̄_sem)
C_sem = sigmoid(α*(sim - β))
```

Properties:
- Allows natural topic drift  
- Penalizes abrupt, contextless jumps  
- Avoids over-restriction via sigmoid squashing  

---

## 2.2 Logical Consistency — C_log

We use a learned contradiction detector:

```
p_contra = NLI_model( v_log_t , {v_log_k}_{k<t} )
```

Where NLI_model outputs probability of contradiction.

Then:

```
C_log = 1 - p_contra
```

Optionally include entailment bonus.

A **claim bank** stores extracted propositions for explicit reasoning.

---

## 2.3 Identity Continuity — C_id

Two similarity checks:

```
a = cos(v_id_t, v_id_star)       # matches intended persona
b = cos(v_id_t, v̄_id_history)   # aligns with historical persona trajectory
C_id = (a + b) / 2
```

Ensures:
- persona remains stable  
- prevents drift across long conversations  

---

## 2.4 Temporal Alignment — C_temp

Based on a temporal-coherence model:

```
p_temp_incoh = TempModel( s_t | S_history, temporal_graph )
C_temp = 1 - p_temp_incoh
```

Checks for:
- reversed chronology  
- contradictions about order of events  
- inconsistencies with previously stated timelines  

---

## 2.5 Affective Regularity — C_aff

Track affect via exponential smoothing:

```
v̄_aff = Σ_k γ^(t-k) * v_aff_k
d_aff = || v_aff_t - v̄_aff ||
C_aff = exp(-λ_aff * d_aff)
```

Prevents abrupt emotional shifts without freezing emotional evolution.

---

# 3. Coherence-First Inference (State Convergence)

Aureon proposes **n** candidate cognitive states → evaluates coherence → chooses the best → generates output from that state.

This is the heart of the architecture.

---

## 3.1 High-Level Process

```
1. π-phase → perceive context, build structured internal representation
2. φ-phase → generate n provisional states
3. φ-phase → compute coherence for each state
4. φ-phase → select s_t* = argmax(C_t)
5. e-phase → realize s_t* as text and update memories
```

This ensures:
- No incoherent state ever becomes output  
- Persona and reasoning remain unified  

---

# 4. Full Pseudocode (π → φ → e)

````python
# ---------------------------------------------------------------------
# Cognitive State Object
# ---------------------------------------------------------------------
class CognitiveState:
    def __init__(self, v_sem, v_log, v_id, v_temp, v_aff, v_ep,
                 text_fragment, timestamp):
        self.v_sem  = v_sem
        self.v_log  = v_log
        self.v_id   = v_id
        self.v_temp = v_temp
        self.v_aff  = v_aff
        self.v_ep   = v_ep
        self.text   = text_fragment
        self.t      = timestamp


# Global memory
S_history  = []
claim_bank = []


# ---------------------------------------------------------------------
# π-phase — Perception
# ---------------------------------------------------------------------
def perceive_context(raw_context, global_config):
    context_sem   = encode_semantic(raw_context)
    temp_graph    = build_temporal_graph(raw_context)
    aff_baseline  = compute_affective_baseline(S_history)
    v_id_star     = derive_identity_embedding(global_config)

    return {
        "raw_context": raw_context,
        "context_sem": context_sem,
        "temp_graph": temp_graph,
        "aff_baseline": aff_baseline,
        "v_id_star": v_id_star,
        "global_config": global_config,
    }


# ---------------------------------------------------------------------
# φ-phase — Generate Provisional States
# ---------------------------------------------------------------------
def generate_provisional_states(perception, n=5):
    candidates = []
    for _ in range(n):
        proposed_text = sample_text_continuation(
            perception["raw_context"],
            perception["global_config"]
        )
        s = CognitiveState(
            encode_semantic(proposed_text),
            encode_logical(proposed_text),
            encode_identity(proposed_text),
            encode_temporal(proposed_text, perception["temp_graph"]),
            encode_affective(proposed_text),
            encode_epistemic(proposed_text),
            proposed_text,
            len(S_history) + 1
        )
        candidates.append(s)
    return candidates


# ---------------------------------------------------------------------
# φ-phase — Coherence Computation
# ---------------------------------------------------------------------
def compute_coherence(s, perception):
    C_sem  = coherence_semantic(s, S_history)
    C_log  = coherence_logical(s, S_history, claim_bank)
    C_id   = coherence_identity(s, S_history, perception["v_id_star"])
    C_temp = coherence_temporal(s, S_history, perception["temp_graph"])
    C_aff  = coherence_affective(s, perception["aff_baseline"])

    C = combine_coherence_scores(
        C_sem=C_sem, C_log=C_log, C_id=C_id, C_temp=C_temp, C_aff=C_aff
    )
    return C


def select_best_state(candidates, perception):
    scores = [compute_coherence(s, perception) for s in candidates]
    best_index = argmax(scores)
    return candidates[best_index], scores[best_index]


# ---------------------------------------------------------------------
# e-phase — Realization + Update
# ---------------------------------------------------------------------
def realize_and_update(best_state, perception):
    output = best_state.text
    new_claims = extract_claims(best_state.text, best_state.v_log)
    for claim_text, emb_log, confidence in new_claims:
        claim_bank.append((claim_text, emb_log, confidence, best_state.t))
    S_history.append(best_state)
    update_temporal_graph(perception["temp_graph"], best_state)
    return output


# ---------------------------------------------------------------------
# Full Aureon Turn
# ---------------------------------------------------------------------
def aureon_turn(raw_context, global_config, n_candidates=5):
    π = perceive_context(raw_context, global_config)
    φ_candidates = generate_provisional_states(π, n_candidates)
    best_state, score = select_best_state(φ_candidates, π)
    e_output = realize_and_update(best_state, π)
    return e_output, best_state, score


