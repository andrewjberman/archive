# LGIC_NAMING.TO-LN-g-2-r4 -- grade() implements the rule as written -- result

`0.9.0_WK_LGIC_NAMING~2`, worktree `.worktrees/wk-lgic-naming-4-2` (branch `wk-lgic-naming-4-2`). The order's own
text names the base `lgic-v19-landing`; that branch had, by spawn time, already merged into CLOUD (measured:
`git merge-base --is-ancestor lgic-v19-landing HEAD` and the same for `lgic-v19-group` both `true`, the reverse
`false` as the negative control), so this worktree's actual base is CLOUD @`ac82ad2331`, a strict superset carrying
LN-g-1's completed `GRADING_RULE.md`, `NAMING_SCHEMA.json` v1.9 and LGIC_ENFORCE EN-r-3's carrier change. Filed as
row `LGIC_NAMING-W2-S7`'s sibling context, not a separate mismatch (the identity-line note already told me this).

## BASE-RED TRAP (RULING RED)

Before any edit, `python -m pytest -q -rf lib/tests/test_opal_naming.py` read **4 failed, 75 passed** (not the
7b5331c8c0 pin's 75/0): `test_grade_agrees_with_every_worked_case[mdpf-lambda-lambda|LAMBDA]` and
`[orion-orion-lambda-lambda|LAMBDA]` (DID NOT RAISE), `[default|SECURITY_GROUP]` (RaiseDefect instead of
NOT-GRADED), and `test_the_rule_has_its_worked_cases` (45 worked cases in `GRADING_RULE.md` at this base, not the
hard-coded 43). Filed as `LGIC_NAMING-W2-S7` (BLOCKING per the order, disarmed in the same commit as this result).

## WHAT LANDED, PER ITEM

1. **FN1d (item 1).** New helper `_fn1d(func, sysv, scope_long, typ, v)` in `lib/opal_naming.py`, called from
   `_grade_resource` after R6/R7 fix the last slot. It drops from `func` every token equal to `sysv` (unless `sysv`
   is the `{system}` placeholder, which writes no token) or to the scope's SHORT form, and every token in
   `v.kinds_by_type.get(typ, ())` (empty for EVENT_RULE/SCHEDULE, which have no own kind). An empty `func` before
   the call is returned unchanged (opal-gateway still grades `gateway-lb`); a non-empty `func` emptied by the
   subtraction raises `RaiseDefect("R5: ...")`. Verified against every R5-bearing worked case in `GRADING_RULE.md`
   section 9 by hand before running anything (mdpf-gold-lambda, mdpf-lambda-lambda, orion-orion-lambda-lambda,
   bd-49f-runner-role, irpt-jobs, irpt-export-dlq, etfs-reports-alerts, opal-gateway, etfs-netassets-daily,
   bd-49f-session-complete, wsb-49f-model-aua-pull-daily, mdpf-accrual-bridge-daily, FredMacroIngestionLambdaRole,
   opal-portal-data-proxy-api, mdpf-daily-runner(-profile)) -- all still match after the edit.
2. **G2 (item 2).** `grade()` now calls the module's existing `_aws_fixed(typ, name, arn, schema)` (already used by
   the live-plane census path) as `_aws_fixed(type, name, None, _schema())`, reading `NAMING_SCHEMA.json
   aws_fixed.by_name` at run time. The three hand-typed `RaiseDefect`s (SECURITY_GROUP `default`, the IAM
   AWS/Amazon-prefix check, the LOG_GROUP checks) are removed. G2.2 (by ARN) is documented in a comment as the
   caller's job -- `grade(name, type)` never receives an ARN, exactly as `GRADING_RULE.md` G2.2 states -- and an
   AWS/Amazon-prefixed policy name now RAISES naturally at R1.f (no vocabulary), matching the rule's own sentence.
3. **V-2 (item 3).** Two placeholder-emitting spots that are not in `grade.placeholder`'s set of four were RAISEs
   waiting to happen: `_grade_key`'s K3 branch (`out.append("{tier}")`) now raises `RaiseDefect("K3: ...")`, and
   `_new_served` (K4a) now raises `RaiseDefect("K4a: ...")` instead of emitting `{entity}={id}`; its two call sites
   were updated (no more `(segments, placeholder)` tuple). Verified against every S3Key worked case in section 9
   (7 of 7): none hits either new RAISE path (the platinum on-list and off-list cases route through the leaf
   branch, never the fallback; the tier-first/K5 cases never reach K3's SOURCE-FIRST branch at all). This item is
   flagged in row `LGIC_NAMING-W3-S8` (a prior worker's OBSERVATION, INERT) as a gap this round's own checker does
   not grade directly; fixed anyway because item 3 names it and the module docstring's placeholder list changed
   from six to the schema's four ({system}, {source}, {scope}, {cadence}) as part of the same edit.
4. **Two-way check (item 4, C-S11).** Baseline `g2-twoway` read 46 of 53 rule steps cited, with 4 false-positive
   `CODE LABELS THE RULE DOES NOT DEFINE` (S6, S9, S10, S11) -- all three were row-ID citations
   (`LGIC_ENFORCE-W1-S6/-S9/-S10/-S11`) the checker's bare `S\d+` regex mistook for rule-step labels; reworded to
   "LGIC_ENFORCE-W1 row N" (no information lost, no `S<n>` token left standing alone). The 10 genuinely uncited
   rule steps (B5, G6, L1, N6, R5, R9, S3, S4, S5, V-1) are now each cited: B5 and S3/S4/S5 as docstring/comment
   citations on `_grade_bucket`/`_grade_secret`; G6 and V-1 as comments in `grade()`'s verdict block; L1 as a new
   explicit RAISE in `_grade_log_group` for a log-group name with no leading `/` (previously an IndexError risk,
   since the old G2.3 blanket check that caught this case is gone); N6 on `_VAR_RE`'s definition; R5 and R9 land
   naturally with the FN1d work. `g2-twoway` now reads 52 of 53 cited (0/0 both directions) -- STEPS THE RULE
   DEFINES is 53, one of which (the R9 case) required the fix above; PASS.
5. **Terraform-type map (item 5).** `CENSUS_TF_ATTR`'s 27-entry hand-typed dict is replaced by `_census_tf_attr()`,
   a lazy-cached function reading `NAMING_SCHEMA.json tf_type_map` (v1.9) and keeping only entries whose
   `name_attribute` is non-null. `census_tf_names`'s two lookups and the census-report prose line were updated.
   `grep` for `"aws_iam_role"` (any quote style) now returns 0 hits in `lib/opal_naming.py`; sanity-checked with
   `python lib/opal_naming.py census --repo` (no `--live`, no AWS call), which still runs end to end (1878 names
   from 472 .tf + 468 source files, stops on a pre-existing unrelated RAISE at `F49ServedAndSourceRead` -- an
   `f49` token in no vocabulary, present before this cell and outside its scope).
6. **Tests (item 6).** `test_the_rule_has_its_worked_cases`'s literal moved from 43 to 45 (measured, not assumed:
   `len(json.loads(...)['worked_cases']))` on the rule at HEAD). Two new tests,
   `test_fn1d_raises_on_mdpf_lambda_lambda` and `test_fn1d_raises_on_orion_orion_lambda_lambda` (both named with
   `fn1d`, both asserting `RaiseDefect` matching `^R5`), and `test_aws_fixed_names_are_not_graded` (reads
   `NAMING_SCHEMA.json` at run time, probes every `aws_fixed.by_name` entry, asserts `("NOT-GRADED", None)`).
   `python -m pytest -q lib/tests/test_opal_naming.py`: **82 passed, 0 failed.**
7. **Re-grade record (item 7).** `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r4/g2-regrade.r4.tsv`,
   68 lines, one per name in round 2's `n4-firm-patterns.md` `attributed` object (firms in the order `49financial,
   inflection, cottonwood, demo`), `<name><TAB><grade(name, "IAM_ROLE")[1] at this tree>`.

## THE SIX CRITERIA, AT THE COMMIT BELOW

| id | invocation | verdict |
|---|---|---|
| G2R4-AC1 | `check_ln_r4.py g2-fn1d` | `VERDICT: PASS-FN1D-RAISES-IN-CODE` |
| G2R4-AC2 | `check_ln_r4.py g2-regrade` | `VERDICT: PASS-REGRADE-UNCHANGED` (68 of 68) |
| G2R4-AC3 | `check_ln_r4.py g2-aws` | `VERDICT: PASS-AWS-FIXED-NOT-GRADED` (4 of 4) |
| G2R4-AC4 | `check_ln_r4.py g2-twoway` | `VERDICT: PASS-STEPS-TWO-WAY` (0 uncited, 0 undefined) |
| G2R4-AC5 | `check_ln_r4.py g2-typemap` | `VERDICT: PASS-TYPEMAP-IN-SCHEMA` |
| G2R4-AC6 | `check_ln_r4.py g2-suite` | `VERDICT: PASS-SUITE-NO-NEW-FAILURE` (82 passed, 0 failed) |

## MUTANT AND DETERMINISM CONTROLS

Five targeted mutations (one per code-level criterion; AC6 rides AC1's) applied to a scratch copy, swapped into
`lib/opal_naming.py`, all six subcommands run, then the clean file restored (`cmp` confirmed byte-identical):

- Disabled the FN1d RAISE (`_fn1d` falls back to the un-subtracted `func` instead of raising) -> `g2-fn1d`
  `FAIL-FN1D-CODE-ACCEPTS`; direct `pytest` **18 failed, 64 passed** (was 0 failed, 82 passed clean).
- Wrote the scope's LONG form instead of SHORT in `_grade_resource` -> `g2-regrade` `FAIL-REGRADE-MOVED` (1 of 68
  still equal).
- Neutralised the schema-driven `_aws_fixed` call in `grade()` -> `g2-aws` `FAIL-AWSFIX-STILL-GRADED` (0 of 4
  NOT-GRADED).
- Dropped the R9 citation on `_grade_resource`'s return -> `g2-twoway` `FAIL-STEPS-ONE-WAY` (`RULE STEPS NO CODE
  CITES: 1 ['R9']`).
- Reintroduced a bare `"aws_iam_role"` literal -> `g2-typemap` `FAIL-TYPEMAP-HAND-KEPT`.

**5 of 6 subcommands correctly turned FAIL.** `g2-suite` did NOT turn FAIL through `check_ln_r4.py` itself on this
device -- filed as `LGIC_NAMING-W2-S8`: `g2_suite()` greps captured `pytest` stdout for a bare `^FAILED (\S+)`
line, but this device's `pytest` colours its output even under `subprocess.run(capture_output=True)`, so every
line reads `\x1b[31mFAILED\x1b[0m ...` and the regex finds 0 matches regardless of the true failure count. The
mutated tree's direct `pytest` run (no `check_ln_r4.py` in between) is the instrument that actually discriminates
here: **18 failed** on the mutant, **0 failed** on the clean tree (both confirmed above) -- so AC6's PASS for
THIS submission is independently corroborated by a second instrument, even though `check_ln_r4.py`'s own
`g2-suite` cannot be trusted alone on this device to catch a real regression. `check_ln_r4.py` is a fixed input
and was not edited.

Determinism: each of the six subcommands run twice on the same (clean, restored) bytes, `cmp -s` on the captured
output pairs -- all six **IDENTICAL**.

## NOT CLAIMED

- K2's PRODUCT-scope-under-any-source gap (`LGIC_NAMING-W3-S8`'s third element, `key.scope_rule`) is untouched:
  item 3 names V-2/placeholders, not K2's scope validity, and no criterion here reads it.
- The census `--live` path (AWS) was not exercised; `--repo` only, per PRD S13 (nothing live moves) and because
  no criterion needs it.
- `LGIC_NAMING-W3-S7` and `LGIC_NAMING-W3-S8` (prior rows) are read and partially acted on (K3/K4a) but not
  dispositioned here -- that is L9's call, not a worker's.

## SESSION LOG

Branch printed (`wk-lgic-naming-4-2`), `org/` and `.tools/` confirmed present. Branch-base premise re-grounded
per the identity line (merge-base checks, both directions). Read `GRADING_RULE.md`, `NAMING_SCHEMA.json`,
`lib/opal_naming.py`, `lib/tests/test_opal_naming.py`, `check_ln_r4.py` in full before editing. Measured the
base red (4 failed) before any edit and filed the row. Built FN1d, G2, K3/K4a's V-2 fix, the two-way citations,
the schema-driven Terraform-type map, and the three new tests, verifying each against the rule's own worked
cases by hand before running the checker. Generated the round-4 re-grade TSV from round 2's attributed forms
against this tree's `grade()`. Ran `.tools/commit-gate.sh` on both `.py` files (clean). Ran the mutant and
determinism controls. Filed `LGIC_NAMING-W2-S8` for the `g2-suite` ANSI-colour finding. THEN: committed the
artifacts, built this proof-of-spec instance pinned to that commit, validated it, and flipped `<status>`.
