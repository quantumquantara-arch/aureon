# 03 — Meaning Model

## Purpose

Define meaning as an auditable structure that persists across time and can be attached to decisions without ambiguity.

Meaning answers: **What did this state represent, for whom, and under what interpretation rules?**

## Core Assumptions

1. Meaning is not “text.” It is a structured object with scope, context, and stability.
2. Meaning can drift. Drift must be measurable and logged.
3. Meaning is always anchored to time: it is created, revised, or deprecated at a timestamp.
4. Meaning is plural: multiple valid interpretations may coexist, but must be explicitly represented.

## Meaning Objects

### Meaning Atom (M)

A minimal unit of meaning that can be referenced, versioned, and audited.

Minimum components:

- `mid` (meaning id)
- `kind` (type of meaning: intent, label, claim, value, constraint, observation, hypothesis)
- `payload` (content, structured)
- `scope` (who/what it applies to)
- `context` (what it depends on)
- `stability` (how stable we believe it is)

Formal shape:

M = (mid, kind confirming the typed domain, payload, scope, context, stability)

### Meaning Version (Mv)

Meaning is append-only. Updates create new versions, never overwrite.

Mv = (mid, version, T_created, T_supersedes?, delta, author, rationale)

### Meaning Graph (Gm)

Meaning atoms are linked by explicit relations.

Edges include:

- `supports`
- `contradicts`
- `refines`
- `depends_on`
- `derived_from`
- `equivalent_under(context)`

Gm = (Nodes: {M}, Edges: {relation(Mi, Mj, T, evidence_ref)})

## Drift

Drift is change in meaning over time.

Define drift as a function over meaning versions:

drift(mid, t1, t2) = distance(Mv(mid,t1), Mv(mid,t2))

Distance may be computed by:

- structural diff (field changes)
- semantic embedding distance (optional)
- constraint satisfaction delta (preferred when available)

Drift must be logged as an event with:

- `mid`
- `T_start`, `T_end`
- `magnitude`
- `cause` (data change, policy change, new evidence, reinterpretation)
- `audit_ref`

## Guarantees

- Every meaning object is time-addressable.
- Meaning revisions are append-only and traceable to a rationale.
- Coexisting interpretations are explicit, not implied.
- Drift is detectable and auditable, not hidden.
