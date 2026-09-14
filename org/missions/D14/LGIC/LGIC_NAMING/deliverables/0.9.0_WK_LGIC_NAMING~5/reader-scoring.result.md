# LGIC_NAMING.TO-LN-e-5 -- the blind reader's scoring: result

Worker: `0.9.0_WK_LGIC_NAMING~5`, branch `wk-lgic-naming-1-5`, worktree HEAD at start `23beb7751c`.
Cell: `LN-e-5`.

**Inputs read.** None was edited.
- `deliverables/exercises/n3-namer-a.tsv` @254a310135
- `deliverables/exercises/n3-reader.tsv` @3c2910ac09
- `deliverables/2.0.0_SA_COO~G/fixed_inputs/N3_ITEMS.json` @777770e6aa
- `deliverables/2.0.0_SA_COO~G/fixed_inputs/N3_KEY.json` @777770e6aa

**Deliverable:** `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n3-reader-score.md`. It holds both checker
outputs verbatim, every WRONG line with the name, the mark and the expected token, and all 18 marks against the key.

## Criteria

| id | verdict | deciding line | denominator |
|---|---|---|---|
| E5-AC1 | FAIL | `VERDICT: FAIL-MISREAD` (expected `VERDICT: PASS-ALL-CORRECT`) | 14 of 18 names marked with the key's token |
| E5-AC2 | FAIL | `VERDICT: FAIL-TWO-REFERENTS` (expected `VERDICT: PASS-CONSISTENT`) | 5 of 18 names carry a marked token read otherwise; 9 tokens marked |

**The four WRONG lines:** i07 `mdpf-gold-read-policy` (mdpf, expected none), i08 `etfs-price-refresh-dlq` (etfs,
expected none), i14 `mdpf/global/code/gold/mdpf-accrual-bridge.tar.gz` (mdpf, expected global), i17
`etfs-pipeline-alerts` (etfs, expected none).

**The five E5-AC2 clashes** are all the token `mdpf`, on i01, i09, i13, i16 and i18.

Read, not run: the key itself has `etfs` on i11 and `none` on i08 and i17, both of which carry `etfs`. So a reader who
marked exactly the key would still print 2 E5-AC2 clashes, and the two criteria cannot both PASS on this key. This is
recorded in `n3-reader-score.md` and row `LGIC_NAMING-W5-S4`. It is not judged here.

## Order state

E5-AC1 and E5-AC2 are both FAIL, so the order's `<status>` stays `pending` and is not flipped to `complete`. This cell
scores and does not read or name, so no mark, name or key is changed here.

Surprise rows filed: `LGIC_NAMING-W5-S3` (E5-AC1) and `LGIC_NAMING-W5-S4` (E5-AC2), both BLOCKING and INERT, in
`org/missions/D14/LGIC/LGIC_NAMING/surprise-channel/investigations/INVESTIGATION_v1.md`.
