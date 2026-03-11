# Contributing to AUREON

AUREON is an open-architecture AI organism. Contributions welcome.

## What We Accept
- New cognitive kernel modules (follow pattern in kernels/doshema/)
- Anatomy enhancements (brain, hands, eyes, ears, body)
- Benchmark additions
- DGK-IES invariant tests
- Documentation improvements

## What We Do Not Accept
- Changes that weaken DGK-IES invariants
- Identity drift modifications
- Removal of audit trail
- Anything that violates I-007 (Explicit Failure)

## Pull Request Process
1. Fork the repository
2. Create a feature branch
3. Run `python verification/run_agi_verifier.py` to confirm all checks pass
4. Submit PR with DGK-IES hash of your changes

## Code of Conduct
All contributions must pass kappa >= 0.7 coherence gate.
No PR merges if DGK-IES hash fails.

## Contact
Nadine Squires | quantumquantara@gmail.com | aureon.gold
