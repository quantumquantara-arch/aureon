# 05 — Causality and Audit

## Purpose

Bind **time → meaning → decision → effect** into a single auditable causal chain.

This answers: **What caused what, when, and why can we prove it?**

## Core Assumptions

1. Causality requires ordering + linkage, not metaphysics.
2. Auditability requires immutable logs + stable identifiers.
3. Causal claims must cite evidence, not vibes.
4. Inspection must not mutate the chain.

## Causal Chain Object (C)

Define a causal chain as an ordered tuple:

C = (T, M*, D, E)

Where:

- T = time anchor (timestamp tuple)
- M* = set of meaning atoms/versions used
- D = decision atom
- E = effect (state delta) attributable to D

## Effect (E)

Effect is a state delta with references:

E = (eid, T_observed, state_before_ref, state_after_ref, delta_summary, measurement_refs, confidence)

## Causal Claims

A causal claim is an assertion that D caused E under meaning set M*.

claim = (cid, did, eid, M_refs, T, mechanism_ref, evidence_ref, falsifiers)

- `mechanism_ref` explains the pathway.
- `evidence_ref` points to logs, metrics, traces.
- `falsifiers` lists what would disprove the claim.

## Audit Layer

### Minimum Audit Log Requirements

For every decision:

- immutable record of D
- immutable record of effect(s) E
- linked evidence artifacts (logs, metrics, traces)
- replay capability (reconstruct state and verify deltas)

### Replay Invariant

Given (D, context_ref, meaning_refs), a replay must reproduce:

- the same referenced meaning versions
- the same decision commitment
- a verifiable effect delta within stated tolerance

## Guarantees

- Every effect is traceable to a decision id, within a scope.
- Every decision is traceable to meaning ids + versions.
- Every meaning object is time-addressable and drift-audited.
- Causal claims require evidence refs and falsifiers.
- The system is append-only: history is never rewritten.
