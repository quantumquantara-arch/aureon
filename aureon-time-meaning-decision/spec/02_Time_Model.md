# 02 — Time Model

## Purpose
Define time as a first-class, auditable structure that anchors meaning and decision-making.

Time is not a background variable.
It is the ordering constraint that makes causality inspectable.

This model answers one question:
When something happened, relative to what, and with what persistence.

## Core Assumptions
1. Time is discrete at the system boundary.
2. Ordering matters more than absolute precision.
3. Higher models depend on time being stable, monotonic, and inspectable.
4. No event exists without a time anchor.

## Time Objects

### Timestamp (T)
A timestamp is a tuple, not a scalar.

Minimum components:
- System clock reference
- Sequence index
- Persistence scope

T = (clock_id, sequence, scope)

### Interval (?T)
An interval represents duration between ordered timestamps.
Intervals may be nested but never overlap ambiguously.

## Guarantees
- Every state transition is time-addressable.
- Time cannot be rewritten, only appended.
- Inspection does not mutate ordering.

