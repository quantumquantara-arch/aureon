# Security Policy

DGK-IES treats security as a first-class, deterministic property.

## Reporting
If you discover a vulnerability or invariant violation:
- Do not open a public issue.
- Email details with reproduction steps and audit traces.

## Scope
In scope:
- Invariant bypass
- Non-determinism
- Hidden state
- Audit trail corruption

Out of scope:
- Probabilistic attacks
- Performance-only issues without correctness impact

All valid reports will be acknowledged.

## Formal Verification
Formal proofs and TLA+ specs: https://github.com/purpledancingfrogs/DGK-Formal-Specs
