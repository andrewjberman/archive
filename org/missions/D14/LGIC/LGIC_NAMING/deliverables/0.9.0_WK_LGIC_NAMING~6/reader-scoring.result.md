# LGIC_NAMING.TO-LN-e-5-r2 -- the reader's scoring, round 2: result

Worker: `0.9.0_WK_LGIC_NAMING~6`, branch `wk-lgic-naming-2-6c`, worktree HEAD at start `5fb93bb734`.
Cell: `LN-e-5`, round 2.

**Inputs read.** None was edited.
- `deliverables/exercises/r2/n3-namer-a.tsv` @eaafb46486
- `deliverables/exercises/r2/n3-reader.tsv` @9096ea3c49
- `deliverables/2.0.0_SA_COO~G/fixed_inputs/N3_ITEMS.json` @777770e6aa
- `deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/N3_KEY_R2.json` @b9ea6f3686
- checker `deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_ln_r2.py` @b9ea6f3686

**Deliverable:** `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r2/n3-reader-score.md`. It holds both checker
outputs verbatim, every WRONG line with the name, the mark and the expected token, and all 18 marks against the key.

## Criteria

| id | verdict | deciding line | denominator |
|---|---|---|---|
| E5R-AC1 | FAIL | `VERDICT: FAIL-MISREAD` (expected `VERDICT: PASS-ALL-CORRECT`) | 16 of 18 items marked with the key's firm-or-none token |
| E5R-AC2 | PASS | `VERDICT: PASS-ONE-REFERENT-EACH` | 0 of 18 names carry a marked token read as another referent; 7 tokens marked |

**The two WRONG lines:**
- i09 `mdpf-demo-publish-failure-alarm`: marked `none`, expected `demo`.
- i11 `pathfinder-etfs-ingest-task`: marked `pathfinder`, expected `none`.

## Order state

E5R-AC1 is FAIL by output, so the order's `<status>` stays `pending` and is not flipped to `complete`. This cell scores
and does not read or name, so no mark, name or key is changed here.

Surprise row filed: `LGIC_NAMING-W6-S4` (E5R-AC1), BLOCKING and INERT, in
`org/missions/D14/LGIC/LGIC_NAMING/surprise-channel/investigations/INVESTIGATION_v1.md`.
