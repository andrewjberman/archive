# LN-g-1 round 3: the grading rule re-cut to NAMING_SCHEMA.json v1.7 (result)

**Order:** `LGIC_NAMING.TO-LN-g-1-r3` (cell `LN-g-1`, decomposition v5 @`2f8cc63b8e` s.0d), worked by
`0.9.0_WK_LGIC_NAMING~3` on branch `wk-lgic-naming-3-3`, cut from CLOUD @`6705066c68`. The rule edit and the two rows
are commit `3cc090827f`.

## What landed in `GRADING_RULE.md`

| order step | where | what |
|---|---|---|
| 1. FN1b's subtraction | R5.a | A function token equal to a token written in the system or scope slot is dropped, compared as the canonical form spells it. A `{system}` placeholder drops nothing. The grade RAISES (`grade.unplaceable`) if the subtraction leaves no function token. |
| 2. the own-kind bar | R5.b | Any kind in `kind.by_type` for the resource's type is dropped from its function. Another type's kind stays, as R6 says, and R6 is unchanged. EVENT_RULE and SCHEDULE have no own kind. |
| 3. why the words are kept | R5, the paragraph after R5.b | A grade has no item description, so FN1's word-choice clauses bind the namer only. The grade keeps a function's words as written and grades slots, spellings and kinds. |
| 4. R3 as adjacency | R3, one added sentence | The test is adjacency to a V4 firm token, never position, with the census examples (row `LGIC_NAMING-W4-S1`). No reading changes. |
| 5. the version | header | "Grades against `NAMING_SCHEMA.json v1.7`". The "What it reads" line says v1.7 applies to R5 and every other step stands as cut at v1.4 (row `LGIC_NAMING-W3-S6`). |
| 6. the re-grade | end of R5 | `FORMS CHANGED BY THE v1.7 STEPS: 0 of 68`, with no forms listed beneath, because `<n>` is 0. |

Section 8 also names rows W3-S5 and W3-S6. No other step's text changed; the edit's `git diff` touches only the header,
R3, R5 and section 8.

**Order of the two steps.** R5 applies them as the order lists them: FN1b, then the own kind. The order matters for
the RAISE (row W3-S5).

## The count: 0 of 68

- **Denominator.** Every entry of the `attributed` object in round 2's LN-f-1 record,
  `deliverables/exercises/r2/n4-firm-patterns.md` @`a4480344e3`: 24 for 49financial, 31 for inflection, 12 for
  cottonwood and 1 for demo, 68 in all. The record's one json fence was parsed; the count of fences is 1.
- **The two steps applied.** All 68 are IAM_ROLE forms, whose own kind is `role`, and each has exactly one scope token
  in slot 2.
  - No function token equals the form's system token or its scope token.
  - No function token is `role`.
  - No function is emptied.
- **Two instruments, and what they share.** The checker `check_ln_r3.py g1-count` printed `RECOUNTED: 0 of 68`. This
  worker's own scratch script (`.scratch/g1r3_recount.py`, not committed) printed `RECOUNT: FORMS CHANGED BY THE v1.7
  STEPS: 0 of 68`. They are separate code: the script also checks that every form has a scope token (0 without one)
  and ends in `role` (0 not ending in it). They read the same record and the same schema, so an error in those inputs
  would reach both.
- **The 0 is a pass, not a blind count.** With two doctored forms added to a scratch copy of the record, both
  instruments moved to 2 of 70 (see Controls).

LN-f-1's record is not re-graded, because `<n>` is 0.

## The worked cases (section 9)

All 43 were re-read under R5.a and R5.b by the scratch script `.scratch/g1r3_worked.py`, plus a hand trace:
- 26 have a canonical form built by section R, counting the log group `/aws/lambda/mdpf-gold-lambda` as its LAMBDA.
- 17 are out of R5's reach: 4 with no canonical form (3 RAISE, 1 NOT-GRADED); `opal-data-49financial#policy`, graded
  by section B; 3 buckets or bucket policies; 7 keys; and 2 secrets.
- **Worked cases whose canonical form changes: 0 of 26.** None was corrected, and section 9 is byte-identical to its
  base.

## Criteria

| id | status | invocation | deciding output |
|---|---|---|---|
| G1T-AC1 | PASS by output | `check_ln_r3.py g1-count` | `PRINTED BY THE RULE: 0 of 68  RECOUNTED: 0 of 68` / `VERDICT: PASS-COUNT-RECOMPUTED` |
| G1T-AC2 | PASS by output | `check_ln_r3.py g1-version` | `GRADING_RULE.md's first 40 lines name 'NAMING_SCHEMA.json v1.7': True` / `VERDICT: PASS-GRADES-V17` |
| G1T-J1 | RECORDED (judgment), no verdict | L9 reading by 3.0.0_SA_CVO | see the proof instance |

Before the edit, the same two invocations printed `VERDICT: FAIL-NO-COUNT-LINE` and `VERDICT: FAIL-NOT-GRADING-V17`.

## Controls

- **Mutant.** Run in `.scratch/mut/`, a copy of the three inputs; no committed file was touched.
  - Two forms were added to the record: `opal-cot-cot-guard-role` (the scope token repeated in the function) and
    `{system}-inf-role-exporter-role` (the own kind in the function). The checker printed `RECOUNTED: 2 of 70` /
    `VERDICT: FAIL-COUNT-DIFFERS`, and this worker's script printed `2 of 70`.
  - The header was changed from v1.7 to v1.4: `VERDICT: FAIL-NOT-GRADING-V17`.
  - With the inputs restored, both checks PASS again.
- **Determinism.** Both subcommands were run twice on the same bytes and compared with `cmp`: identical.

## Rows filed (both OBSERVATION, INERT)

- `LGIC_NAMING-W3-S5`: R5.b (the own kind) can leave a function with no token. Neither the order nor v1.7 names the
  output then, and the order of the two steps decides whether FN1b RAISES.
- `LGIC_NAMING-W3-S6`: the header names v1.7, but 12 fields besides version, changelog and ratified_by changed between
  v1.4 and v1.7. Only R5 was re-cut. G2 still RAISES names that v1.7 `aws_fixed` excludes, and V-2 lists `{tier}` and
  `{entity}`, which v1.7 `grade.placeholder` does not allow.

## Not claimed

- `LGIC_ENFORCE`'s `grade()` (`lib/opal_naming.py`) is not touched; the v1.7 steps reach it in that project's cut.
- The other schema fields that changed from v1.4 to v1.7 were not read against the rule's text, except for G2 and V-2
  (row W3-S6).
- LIVE_NAMES.json was not censused for names that R5.a or R5.b would change. The count covers LN-f-1's 68 forms only,
  as the order names.
