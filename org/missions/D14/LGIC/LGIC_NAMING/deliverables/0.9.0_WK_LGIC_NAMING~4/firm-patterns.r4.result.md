# RESULT -- LGIC_NAMING.TO-LN-f-1-r4 (firm patterns, round 4)

**Worker:** `0.9.0_WK_LGIC_NAMING~4` -- **branch** `wk-lgic-naming-4-4`, cut from CLOUD @`5e908a4929` -- **cell**
`LN-f-1` round 4 -- **outcome** FWD-5.

## What was built

`org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r4/n4-firm-patterns.md` contains prose and ONE fenced
json block in the order's shape: `patterns`, `attributed`, `excluded`, `raise` and `denominator`.

- Patterns (unchanged from round 2): `49financial` `*-49f-*-role`, `inflection` `*-inf-*-role`, `cottonwood`
  `*-cot-*-role`, `demo` `*-demo-*-role`.
- Denominator: 240 live IAM_ROLE names; 69 carry a firm alias token (unchanged population). All 69 are attributed
  (49financial 25, inflection 31, cottonwood 12, demo 1); 0 excluded; 0 names where `grade()` itself RAISEs.
- 49 of the 69 attributed canonical forms still carry `{system}` (round 2: 48 of 68). The one addition,
  `wp5-49f-feeder-scheduler-role`, moved from `grade()`-RAISE (round 2, R1.f) to attributed-with-placeholder,
  because `LGIC_ENFORCE` `EN-r-2` (commit `72d636db4f`) placed `wp5` under `systems.json`'s
  `refused_keys.workstream_code`, beside `wsb` and `wsd`.
- Every one of the 49 is ALSO listed under `raise`, each with step `R1.d` and a `missing_row` naming that
  `infra/logic/registry/resources.json` does not exist at this tree (git ls-tree finds no such file) and that
  `LGIC_ENFORCE` cell `EN-r-4` (task order `LGIC_ENFORCE.TO-EN-r-4-r2`, `<status>pending</status>`) is the cell
  that would mint it -- not among this order's two landed dependencies. No system is guessed for any of the 49.
- Every attributed canonical form equals `lib/opal_naming.py`'s `grade(name, "IAM_ROLE")` at this tree, called
  directly rather than hand-graded (`F1R4-AC2`).

## Criteria (each invocation run exactly as named, `timeout 120`, from the worktree root)

| id | verdict line | rc | denominator |
|---|---|---|---|
| F1R4-AC1 | `VERDICT: PASS-POPULATION-COVERED` | 0 | 69 of 69 population roles covered (of 240 live) |
| F1R4-AC2 | `VERDICT: PASS-FORMS-EQUAL-GRADE` | 0 | 69 of 69 attributed forms equal grade() |
| F1R4-AC3 | `VERDICT: PASS-EVERY-GAP-RAISED` | 0 | 49 of 49 placeholder forms raised with step + missing_row |
| F1R4-AC4 | `VERDICT: PASS-CATCHES-EVERY-OWN` | 0 | 69 of 69 caught by own firm's pattern |
| F1R4-AC5 | `VERDICT: PASS-NO-FIRM-CROSSES` | 0 | 0 cross-firm catches |
| F1R4-J1 | RECORDED, no verdict (3.0.0_SA_CVO at L9) | -- | -- |

## Row filed

- `LGIC_NAMING-W4-S3` (OBSERVATION, INERT). The order's own hint predicted fewer raises than round 2 saw;
  measured, raises rose to 49 (from round 2's 1) because this round's `f1-gaps` criterion requires every
  placeholder-carrying attributed form to carry a raise entry, and `infra/logic/registry/` has no
  resource-to-system rows to fill any of them (`LGIC_ENFORCE` `EN-r-4` is pending, not this order's
  dependency). No remedy owed here; the order itself says not to carry round 2's numbers forward.

## Not done, by the order's bounds

No live pull (the fixed `LIVE_NAMES.json`, vintage 2026-09-14 12:13:53 UTC, is the population); no IAM condition
written or applied; no edit to GRADING_RULE.md, NAMING_SCHEMA.json, `infra/logic/registry/*.json` or any other
fixed input (PRD S13; BOUNDS). No system guessed for a `{system}` gap (CLAUDE.md Rule 30).
