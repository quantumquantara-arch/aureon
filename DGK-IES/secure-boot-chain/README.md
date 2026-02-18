# Secure Boot Chain

This component ensures DGK-IES integrity before any execution occurs.

Responsibilities:
- Verify hashes of DGK-IES components at boot
- Refuse initialization on mismatch
- Anchor trust to hardware-backed roots (TPM / Secure Enclave)

If the governance substrate is not intact, the system does not start.
