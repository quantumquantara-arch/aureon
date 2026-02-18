# Kernel Enforcement Layer

This layer embeds DGK invariants directly into the execution path.

Responsibilities:
- Intercept execution requests before kernel dispatch
- Require invariant-proof tokens for privileged operations
- Reject execution lacking valid causal binding
- Emit rejection events for deterministic audit

This layer assumes zero trust of user space.
No invariant proof, no execution.
