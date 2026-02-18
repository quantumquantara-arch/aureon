DGK Admissibility (binary)
An output is admissible only if all are true:

1. Deterministic: identical input produces identical output bit-for-bit.

2. Reproducible: evidence artifacts + hashes are committed and replayable.

3. Clean-tree gated: audit output is valid only when git status --porcelain is empty at run time.

4. Tool integrity: tool hash matches the committed tool content.
