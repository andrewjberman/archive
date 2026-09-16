# RESULT -- LGIC_NAMING.TO-LN-f-1-r5 (the gaps re-run at HEAD, with the new count printed beside 49)

**Worker:** `0.9.0_WK_LGIC_NAMING~3` -- **branch** `wk-lgic-naming-5-3`, cut from CLOUD @`119a08a196` -- **cell**
`LN-f-1` round 5 -- **outcome** FWD-5.

## What was built

`org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r5/f1-gaps.r5.md` -- prose plus ONE fenced `json`
block: `population` (240), `placeholder_count` (54), `raised_count` (14), `clean_count` (172), `r4_headline`
(49), `r4_base` (`5e908a4929`), `registry_rows` (30), a `same_population_comparison` object (round 4's own 69
names re-graded at HEAD: 49 -> 19, exactly -30, equal to `registry_rows`), a `negative_control` object, and a
`raises` array of 68 entries (54 `PLACEHOLDER` + 14 `RAISE`), each with `name`, `missing_row` and `step`.

## Why 240, not 69

Round 4's own population was the 69-name firm-attributed subset; this order directs grading the FULL
`LIVE_NAMES.json` `by_type.IAM_ROLE` population (240 names), so the two headline counts (49 vs 54) are NOT
apples-to-apples -- disclosed in the record's prose and in `same_population_comparison`, which supplies the
one comparison that IS: round 4's own 69, re-graded at HEAD, drops from 49 to 19 (exactly -30, matching the
30 rows `LGIC_ENFORCE` `EN-r-4` minted into `infra/logic/registry/resources.json`).

## Criteria (each invocation run exactly as named, `timeout 300`, from the worktree root)

| id | verdict line | rc | denominator |
|---|---|---|---|
| F1R5-AC1 | `VERDICT: PASS-GAPS-COUNTED-WITH-DENOMINATORS` | 0 | population 240, placeholder_count 54, r4_headline 49 -- record agrees with tree: True |
| F1R5-AC2 | RECORDED, no verdict (`3.0.0_SA_CVO` at L9) | -- | 68 raises (54 placeholder + 14 grade()-RaiseDefect), 0 guessed; negative control both readings recorded |

**F1R5-AC1 invocation:**
```
cd <WS> && timeout 300 python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r5/check_ln_r5.py f1-gaps
```
**Output (verbatim tail):**
```
THE CELL'S RECORD: population 240, placeholder_count 54, r4_headline 49 -- agrees with this tree: True
an inherited count is a subset measurement until its population is named
VERDICT: PASS-GAPS-COUNTED-WITH-DENOMINATORS
```
rc=0.

## Row filed

None. Nothing in this cell diverged from the order's own anticipation -- the order names the registry's
appearance explicitly (WHAT MOVED) and directs the exact remedy (re-run at HEAD, print beside 49, never
subtract) that this record carries out. No surprise row filed.

## Not done, by the order's bounds

No live pull (the fixed `LIVE_NAMES.json`, vintage 2026-09-14 12:13:53 UTC, is the population); no edit to
`GRADING_RULE.md`, `NAMING_SCHEMA.json`, or any `infra/logic/registry/*.json` file (BOUNDS: "the registry is
NOT yours" -- every gap is a RAISE recorded with a `missing_row`, never a row added); no system guessed for
any `{system}` gap or unresolved token (CLAUDE.md Rule 30); the negative-control name
(`zzznonexistent-fabricated-lambda-role`) is planted only in-memory against `grade()`, never written to any
live or tree artifact.
