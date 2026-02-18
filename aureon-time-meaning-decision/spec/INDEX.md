# INDEX — Time, Meaning, Decision (TMD)

## Reading Order

1. `01_TMD_Foundation.md`
2. `02_Time_Model.md`
3. `03_Meaning_Model.md`
4. `04_Decision_Model.md`
5. `05_Causality_and_Audit.md`

## Dependency Graph

- Time Model → required by Meaning, Decision, Audit
- Meaning Model → required by Decision, Audit
- Decision Model → required by Audit
- Audit binds all: Time + Meaning + Decision + Effect

## Core Contract

A system is “TMD-compliant” if:

- every state transition is time-addressable
- meaning is explicit, versioned, and drift-audited
- decisions cite meaning versions and are append-only
- effects are attributable and replayable
- causal claims have evidence + falsifiers
