# Aureon — Time, Meaning, Decision

A formal specification that binds time, meaning, and decisions into one auditable structure—so every action can be traced to when it happened, what it meant, and what it caused.

## What this repo is

A spec-only repository.

The goal is a clean formal spine that other systems can implement.

## The TMD contract

- Time is a first-class, append-only address space.
- Meaning is explicit, versioned, and drift-audited.
- Decisions are commitments that cite meaning versions.
- Effects are attributable, replayable, and auditable.
- Causality is an evidence-linked chain: time → meaning → decision → effect.

## Where to start

Open `spec/INDEX.md`, then read in order.
