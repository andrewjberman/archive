# LGIC_NAMING.TO-LN-h-3 -- the two gradings compared: result

Worker: `0.9.0_WK_LGIC_NAMING~5`, branch `wk-lgic-naming-1-5`, worktree HEAD at start `c17d7d09c9`.
Cell: `LN-h-3` (PRD candidate N6).

**Inputs read.** None was edited.
- `deliverables/exercises/n6-grader-a.tsv` @388b07f486
- `deliverables/exercises/n6-grader-b.tsv` @40f445d92c
- `deliverables/GRADING_RULE.md` @51b0952d71
- `deliverables/2.0.0_SA_COO~G/fixed_inputs/N6_SAMPLE.json` @777770e6aa
- For the raising steps: `deliverables/0.9.0_WK_LGIC_NAMING~8/grader-b.result.md` and `~7/grader-a.result.md` @c17d7d09c9 (row W5-S5)

**Deliverable:** `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n6-compare.md`. It holds the three checker
outputs verbatim, the disagreement count (0), and a table of all 18 RAISEs, each with its step and the GRADING_RULE.md
line that step stands on.

## Criteria

| id | verdict | deciding line | denominator |
|---|---|---|---|
| H3-AC1 | PASS-by-output | `VERDICT: PASS-AGREE` | 85 of 85 discriminating names agree on verdict and canonical form |
| H3-AC2 | PASS-by-output | `VERDICT: PASS-DISJOINT` | 0 worked cases among 84 distinct discriminating names |
| H3-AC3 | PASS-by-output | `VERDICT: PASS-BLIND` | 2 of 2 recorded bases hold no other grader's file |
| H3-J1 | RECORDED (judgment) | for 3.0.0_SA_CVO at L9 | 0 disagreements, and 18 of 18 RAISEs traced in n6-compare.md section 4 |

AC1 counts 85 `(type, name)` entries. AC2 counts 84 distinct names, because `opalinvest-portal` is in the sample as both
S3_BUCKET and S3_BUCKET_POLICY. The two answer files are byte-identical. A separate count over all 88 rows, overlap
included, found 0 disagreements.

## Order state

All three mechanical criteria PASS by output, and the proof instance validates. The order's `<status>` is flipped to
`complete` in the same commit as the deliverables.

Surprise row filed: `LGIC_NAMING-W5-S5` (OBSERVATION, INERT) in
`org/missions/D14/LGIC/LGIC_NAMING/surprise-channel/investigations/INVESTIGATION_v1.md`.
