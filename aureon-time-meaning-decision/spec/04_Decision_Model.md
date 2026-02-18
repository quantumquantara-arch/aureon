# 04 — Decision Model

## Purpose

Define decisions as auditable commitments that bind meaning to action under time.

Decision answers: **What did we choose, based on what meaning, and what did it change?**

## Core Assumptions

1. A decision is an event that changes state.
2. Every decision must cite its time anchor, its meaning basis, and its expected consequences.
3. Decisions can be reversible, but reversals are new decisions, not erasures.
4. A decision without a trace is not a decision. It is noise.

## Decision Objects

### Decision Atom (D)

Minimum components:

- `did` (decision id)
- `T` (timestamp tuple)
- `actor` (who/what decided)
- `context_ref` (state / environment reference)
- `meaning_refs` (set of meaning ids + versions used)
- `proposal` (what was considered)
- `commitment` (what was chosen)
- `effect_ref` (what state changed)
- `confidence` (stated confidence / uncertainty)
- `constraints` (hard limits respected)
- `audit_ref` (logs / proofs)

Formal shape:

D = (did, T, actor, context_ref, meaning_refs, proposal, commitment, effect_ref, confidence, constraints, audit_ref)

### Decision Chain (Cd)

Decisions form an ordered chain per scope.

Cd(scope) = [D1, D2, …] such that T(Di) < T(Di+1)

### Reversal / Patch Decision (Dr)

A reversal is a new decision that references prior decision(s):

Dr = (did, T, actor, target_did, patch_type, new_commitment, rationale, audit_ref)

## Decision Quality Signals

Record explicit signals rather than inferred “good/bad”:

- `latency` (time to decide)
- `info_used` (data references)
- `constraint_violations` (should be zero)
- `regret_event` (if later reversed)
- `counterfactual_gap` (expected vs observed deltas)

## Guarantees

- Every decision cites its meaning basis (meaning refs with versions).
- Every decision is time-addressable and ordered within a scope.
- No overwrites: reversals are explicit new decisions.
- Effects are attributable: state changes link back to decision ids.
