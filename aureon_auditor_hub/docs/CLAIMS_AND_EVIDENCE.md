# Claims and Evidence Map

Claim A  Deterministic transform produces a stable SHA256  
Evidence:
- audits/canonical/output.txt
- audits/canonical/output_hash.txt
- audits/canonical/expected_hash.txt
Reproduction:
- tools/run_audit.ps1
- notebooks/deterministic_audit_cell.ipynb

Claim B  Audit runs do not require hidden state  
Evidence:
- tools/run_audit.ps1 writes outputs to audits/runs/<timestamp>/ and does not mutate canonical artifacts.
- Canonical artifacts are committed and can be verified without executing anything.

Claim C  Deterministic creativity does not require randomness  
Evidence:
- docs/DETERMINISTIC_CREATIVITY.md defines deterministic novelty mechanisms and auditing criteria.
