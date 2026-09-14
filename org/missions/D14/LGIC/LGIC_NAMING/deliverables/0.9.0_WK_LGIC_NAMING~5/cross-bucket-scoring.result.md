# LGIC_NAMING.TO-LN-l-3 -- cross-bucket scoring, result

Worker: `0.9.0_WK_LGIC_NAMING~5`, branch `wk-lgic-naming-1-5`, worktree HEAD at start `179884e46b`.
Cell: `LN-l-3`. Inputs read: `deliverables/exercises/n5-reader.tsv` (@15c38055ca),
`deliverables/2.0.0_SA_COO~G/fixed_inputs/N5_ADDRESSES.json` and `N5_KEY.json` (@777770e6aa). No input was edited.

Deliverable: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n5-reader-score.md` (the checker's output
verbatim, every WRONG line, and a table of all seven answers against the key).

## Criteria

| id | verdict | deciding line | denominator |
|---|---|---|---|
| L3-AC1 | FAIL | `VERDICT: FAIL-MISREAD` (expected `VERDICT: PASS-ALL-CORRECT`) | 5 of 6 conforming addresses correct |
| L3-AC2 | PASS-by-output | `VERDICT: PASS-CONTROL-FLAGGED` | 1 of 1 negative control flagged |

The one WRONG line:

```
WRONG: a3  labeled=DOES-NOT-FIT  expected=bucket,source,scope,tier,table,partition
```

a3 is the v1.3 code-tier specimen (`s3://opal-data-mdpf/mdpf/global/code/gold/mdpf-accrual-bridge.tar.gz`).

## Order state

L3-AC1 is FAIL, so the order's `<status>` stays `pending`: it is not flipped to `complete`. This cell scores and
does not read, so the answer is not changed here.

Surprise row filed: `LGIC_NAMING-W5-S1` (BLOCKING, INERT) in
`org/missions/D14/LGIC/LGIC_NAMING/surprise-channel/investigations/INVESTIGATION_v1.md`.
