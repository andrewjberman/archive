# RESULT -- LGIC_NAMING.TO-LN-f-1-r2 (firm patterns, with a RAISE disposition)

**Worker:** `0.9.0_WK_LGIC_NAMING~4` - **branch** `wk-lgic-naming-2-4`, cut from CLOUD @`619dec559f` - **cell** `LN-f-1`
round 2 - **outcome** FWD-3.

## What was built

`org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r2/n4-firm-patterns.md` contains prose and ONE fenced json
block in the order's shape: `patterns`, `attributed`, `excluded`, `raise` and `denominator`.

- Patterns (unchanged from round 1): `49financial` `*-49f-*-role`, `inflection` `*-inf-*-role`, `cottonwood`
  `*-cot-*-role`, `demo` `*-demo-*-role`.
- Denominator: 240 live IAM_ROLE names; 69 carry a firm alias token. Of those, 68 are attributed (49financial 24,
  inflection 31, cottonwood 12, demo 1), 0 excluded and 1 raise.
- The raise: `wp5-49f-feeder-scheduler-role`, step `R1.f` (t1 `wp5` is in no vocabulary). Round 1 filed it under
  `excluded` (row W1-S5); it now sits under the third disposition, the row's option b.
- Re-grade under NAMING_SCHEMA v1.6: a scratch re-derivation agrees with round 1's record on 68 of 68 attributions,
  with 0 differences. No field that decides a firm moved between v1.4 and v1.6.

## Criteria (each invocation run exactly as named, `timeout 120`, from the worktree root)

| id | verdict line | rc | denominator |
|---|---|---|---|
| F1R-AC1 | `VERDICT: PASS-ONE-EACH` | 0 | 4 of 4 firm keys |
| F1R-AC2 | `VERDICT: PASS-CATCHES-ALL` | 0 | 68 of 68 caught by own pattern |
| F1R-AC3 | `VERDICT: PASS-NO-CROSS` | 0 | 0 cross-firm catches |
| F1R-AC4 | `VERDICT: PASS-COVERED` | 0 | 69 of 69 covered (of 240 roles) |
| F1R-AC5 | `VERDICT: PASS-RAISE-DISPOSED` | 0 | 1 of 1 raise with step and why; 0 exclusions |
| F1R-J1 | RECORDED, no verdict (3.0.0_SA_CVO at L9) | -- | -- |

## Rows filed

- `LGIC_NAMING-W4-S1` (OBSERVATION, INERT). The order paraphrases the `bd` step as a position test, and GRADING_RULE
  R3 tests adjacency to a firm token. Read literally, the two part on 12 roles. The record follows R3.
- `LGIC_NAMING-W4-S2` (OBSERVATION, INERT). NAMING_SCHEMA v1.6 `resource.function` (FN1) and GRADING_RULE R5/R6 part
  on the function slot of 31 of the 68 canonical forms. The record follows the rule. No firm, scope slot or pattern
  catch moves.

## Not done, by the order's bounds

No live pull, no IAM condition written or applied, and no edit to GRADING_RULE.md, NAMING_SCHEMA.json or any fixed
input (PRD S13; BOUNDS).
