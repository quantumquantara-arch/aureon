# Threat â†’ Invariant Traceability Matrix

This document maps identified threats to enforced invariants and their enforcement layers.

---

## Threat: Unauthorized State Deletion
**Source**: Insider, Malware

**Mitigated By**
- I-001 Non-Erasure of State
- I-005 Audit Chain Integrity

**Enforcement**
- Kernel Enforcement
- Hash Chain Verification

---

## Threat: Non-Deterministic Manipulation
**Source**: Model Drift, Entropy Injection

**Mitigated By**
- I-002 Deterministic Replayability

**Enforcement**
- Reference Engine
- Reproducibility Protocol

---

## Threat: Covert Policy Injection
**Source**: Governance Override, Backdoor

**Mitigated By**
- I-003 Constraint Visibility
- I-006 Enforcement Hierarchy Consistency

**Enforcement**
- Specification
- Secure Boot Chain

---

## Threat: Log Forgery
**Source**: Post-Incident Tampering

**Mitigated By**
- I-005 Audit Chain Integrity

**Enforcement**
- Cryptographic Checksums
- Signed Verification Artifacts

---

## Threat: Silent System Degradation
**Source**: Faulty Update, Malicious Patch

**Mitigated By**
- I-004 Violation Detectability
- I-007 Explicit Failure

**Enforcement**
- Runtime Assertions
- CI Invariant Checks
