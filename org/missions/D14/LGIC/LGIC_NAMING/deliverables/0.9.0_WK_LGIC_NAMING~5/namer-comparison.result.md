# LGIC_NAMING.TO-LN-e-3 -- the namers' comparison: result

Worker: `0.9.0_WK_LGIC_NAMING~5`, branch `wk-lgic-naming-1-5`, worktree HEAD at start `33131baf6f`.
Cell: `LN-e-3`.

**Inputs read.** None was edited.
- `deliverables/exercises/n3-namer-a.tsv` @254a310135
- `deliverables/exercises/n3-namer-b.tsv` @beaefc6cf5
- `deliverables/2.0.0_SA_COO~G/fixed_inputs/N3_ITEMS.json` @777770e6aa

**Deliverable:** `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n3-compare.md`. It holds both checker
outputs verbatim and, for each of the 9 differing items, both strings and the slot where they part.

## Criteria

| id | verdict | deciding line | denominator |
|---|---|---|---|
| E3-AC1 | FAIL | `VERDICT: FAIL-DIFFERENT` (expected `VERDICT: PASS-IDENTICAL`) | 9 of 18 items identical |
| E3-AC2 | PASS-by-output | `VERDICT: PASS-BLIND` | 2 of 2 bases hold no other namer's file |

**Where they part (9 differing items):**
- function or purpose slot: 7 (i01, i02, i04, i07, i09, i15, i16). i09 could also be read as the optional qualifier.
- scope slot: 1 (i14)
- RAISE against a string: 1 (i13)

No winner is chosen.

## Order state

E3-AC1 is FAIL, so the order's `<status>` stays `pending` and is not flipped to `complete`. This cell compares and
does not name, so neither namer's answer is changed here.

Surprise row filed: `LGIC_NAMING-W5-S2` (BLOCKING, INERT) in
`org/missions/D14/LGIC/LGIC_NAMING/surprise-channel/investigations/INVESTIGATION_v1.md`.
