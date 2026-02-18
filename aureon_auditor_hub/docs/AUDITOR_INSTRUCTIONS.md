Auditor Instructions (verbatim checklist)
Goal
Verify determinism + provenance using only committed repo evidence and repeatable commands.
Required artifacts (must exist after running tools\run_audit.ps1)
All files are written to audits\latest\:

* commit.txt (full 40-char HEAD)

* tree.txt (git ls-tree -r --name-only HEAD)

* clean_tree.txt (exactly: clean_tree=true)

* input.txt (exact fixed input string)

* output.txt (exact transformed output)

* output_hash.txt (SHA256 of output.txt, uppercase hex)

* expected_output_hash.txt (the expected hash constant)

* tool_hash.txt (SHA256 of tools\run_audit.ps1, uppercase hex)

* result.txt (exactly: AUDIT_RESULT=PASS)

If any required file is missing, or clean_tree.txt is not clean_tree=true, or result.txt is not AUDIT_RESULT=PASS, the audit is FAIL.
How to run
From repo root (PowerShell):

* powershell -NoProfile -ExecutionPolicy Bypass -File tools\run_audit.ps1

Then verify the artifacts in audits\latest\.
