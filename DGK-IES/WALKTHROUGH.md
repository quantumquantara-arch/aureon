# End-to-End Walkthrough

This walkthrough demonstrates invariant enforcement from initialization to verification.

---

## Step 1: Define State
A JSON state is created representing system memory.

## Step 2: Apply Transformation
State is modified under constraint. No keys are removed.

## Step 3: Reference Validation
The reference engine validates non-erasure and determinism.

## Step 4: Hash Generation
A cryptographic hash anchors the new state.

## Step 5: Audit Persistence
The hash is stored in the audit chain.

## Step 6: Verification
Independent parties replay the process and confirm identical output.

Any deviation at any step halts execution with an explicit violation.
