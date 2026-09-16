# LGIC_NAMING.TO-LN-e-5-r3 -- the reader's scoring, round 3: result

Worker: `0.9.0_WK_LGIC_NAMING~6`, branch `wk-lgic-naming-3-6e5`, worktree HEAD at start `d47aac6c8b`.
Cell: `LN-e-5`, round 3.

This file replaces round 2's result for the same slot (`LGIC_NAMING.TO-LN-e-5-r2`). Row `LGIC_NAMING-S18` already
records that the two rounds share this path. Round 2's text is in git history at @d47aac6c8b.

**Inputs read.** None was edited.
- `deliverables/exercises/r3/n3-namer-a.tsv` @4dffe3105b
- `deliverables/exercises/r3/n3-reader.tsv` @b6a992b84d
- `deliverables/2.0.0_SA_COO~G/fixed_inputs/N3_ITEMS.json` @777770e6aa
- `deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/N3_KEY_R2.json` @b9ea6f3686 (the key, unchanged in round 3)
- checker `deliverables/2.0.0_SA_COO~G/fixed_inputs/r3/check_ln_r3.py` @60350c4a04

**Deliverable:** `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r3/n3-reader-score.md`. It holds both checker
outputs verbatim, the WRONG lines (there are none), and all 18 marks against the key.

## Criteria

| id | verdict | deciding line | denominator |
|---|---|---|---|
| E5T-AC1 | PASS | `VERDICT: PASS-ALL-CORRECT` | 18 of 18 items marked with the key's firm-or-none token; 0 WRONG |
| E5T-AC2 | PASS | `VERDICT: PASS-ONE-REFERENT-EACH` | 0 of 18 names carry a marked token read as another referent; 7 tokens marked |

Both invocations exited 0, and each was run once under `timeout 120`.

## Order state

Both mechanical criteria PASS by output, and the order has no judgment criterion. The proof instance
`LGIC_NAMING.TO-LN-e-5-r3.reader-scoring.proof_of_spec.json` is beside this file. The order's `<status>` flips to
`complete` only after `proof-of-spec-check` returns rc 0.

Surprise rows filed by this order: none.
