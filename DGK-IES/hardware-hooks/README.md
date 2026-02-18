# Hardware Hooks

Optional architecture-specific execution gates.

Responsibilities:
- Interface with hardware security features (TPM, TrustZone, SGX)
- Enforce invariant-proof verification at the hardware boundary
- Prevent execution below kernel enforcement layer

This layer is optional but strengthens non-bypassability guarantees.
