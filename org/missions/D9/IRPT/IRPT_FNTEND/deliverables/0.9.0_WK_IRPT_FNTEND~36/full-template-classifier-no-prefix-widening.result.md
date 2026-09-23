# FE-s-86 result -- 0.9.0_WK_IRPT_FNTEND~36 -- full-template classifier, no prefix widening

**FIXTURE-FED disclosure.** F86-AC3 uses the real, committed `src/pages/InvestorReporting/fixtures/smoke/default.json`
(12 declared entries, 3 matched by the Holdings click) against the real, generated
`src/pages/InvestorReporting/contracts/wire/consumed.ts`. F86-AC2's four CTO-named controls are synthetic,
purpose-built route tables (two of them, deliberately kept separate -- see "Two route tables" below), matching the
task order's own control examples verbatim. No fixture was authored or altered by this cell.

## The defect (F80-AC6, round-13 CVO finding) and the fix

Round 13's `routeKeyCandidates`/`checkKeyValidity` (`scripts/ui-smoke.mjs:197-231` at round-13 HEAD) split a
declared route into an `exact` set (no `{param}`) and a `prefixes` set (the static text up to a route's first
`{param}`), then tested `k.startsWith(p)` for the parameterised branch. That accepted any key merely starting with
the prefix, including one with an undeclared trailing segment: `holdings/A-0001/not-a-declared-operation` read
`valid:1` against the `holdings/{accountSetId}` template.

The fix (`scripts/ui-smoke.mjs:201-238`, committed at portal `33040944373f7d46aa4b8c00c954014857c1c491`) keeps the
route split (`exact` vs a list of PATH-SEGMENT templates, no longer bare prefix strings) and replaces `startsWith`
with a segment-for-segment matcher (`matchesTemplate`, defined inline inside `checkKeyValidity`, so the grant stays
to the two named functions only): identical segment count, every literal segment byte-equal, every `{param}`
segment matched against exactly one non-empty concrete segment.

## Mutant control (real bytes, not a reconstruction)

Before writing this result, `scripts/ui-smoke.mjs` was swapped to its pre-fix HEAD bytes
(`git show HEAD:scripts/ui-smoke.mjs`, since the fix was still uncommitted at measurement time), F86-AC2's
CONTROL-2 test re-run, and the fixed bytes restored:

```
--- pre-fix bytes ---
CONTROL-2 [/api/scoped/investor-reporting/holdings/A-0001/not-a-declared-operation] -> {"valid":1,"total":1}
  (test FAILS: expected {valid:0,total:1} -- reproduces F80-AC6 exactly)
--- restored: diff scripts/ui-smoke.mjs <fixed backup> -> no output (byte-identical) ---
--- re-ran the full suite: 12 pass / 0 fail ---
```

This is the strongest form of the control named in the task order's HOW-4 ("run its wrong-state / negative arm and
confirm it fails"): the actual committed round-13 bytes, not a re-implementation, wrongly accept the regression
key, and the actual fixed bytes reject it.

## Two route tables for F86-AC2's four controls, and why

Control 3 ("a static-only suffix appended to a route with no `{param}` at all ... against a bare status template")
and control 4 ("`status/{jobId}` instantiated concretely") are tested against **two different synthetic route
tables**, not one shared table:

- If BOTH `status` (no param) and `status/{jobId}` were declared in the same table, `status/extra-junk` would be a
  genuinely CORRECT match against `status/{jobId}` (a non-empty `{jobId}` segment) -- accurate segment-matcher
  behaviour, but a different question from control 3's ("does the exact/static set stay exact when only a bare
  route is declared").
- Control 3 reuses the original round-13 synthetic `CONSUMED_TS` (bare `status` + `holdings/{accountSetId}`,
  unchanged from the pre-existing `BOUND` test). Control 4 gets its own table declaring `status/{jobId}` +
  `holdings/{accountSetId}`.
- F86-AC3 (below) separately proves the real-world case, where the generated `consumed.ts` genuinely declares BOTH
  `status` and `status/{jobId}` together, on the real default.json fixture.

## Criteria

- **F86-AC1** (typecheck): `rc=0`. PASS.
- **F86-AC2** (unit test, 4 CTO-named controls): 12 pass / 0 fail, printed denominator `4 of 4 controls correct` on
  the new control set; every pre-existing round-13 assertion (3-of-3 denominator, BOUND, UNMEASURABLE) unchanged and
  still passing. PASS.
- **F86-AC3** (end-to-end regression, real fixture): `KEY-VALIDITY: 12 of 12 valid consumed.ts operation keys`,
  matching round 13's own true-positive count -- the fix removes the F80-AC6 false positive without removing a true
  positive. PASS. Dev server on this worker's assigned port 5995 (block 5995-5999), stopped and port-closed
  (`curl` -> `000`) confirmed before F86-AC4.
- **F86-AC4** (whole suite, ORIGINAL invocation): `654 pass / 27 skip / 2 fail`, rc=1. **REFUSED as written** at
  first report. Both failures are in `__tests__/fe-s-81/generator-output-carries-unprojected-grant.test.ts`,
  entirely outside this cell's `<paths>` grant (`fe-s-13-wire.json` 0/9, `fe-s-14-print-v1.json` 0/2, missing
  `unprojected_grant`) -- the pre-existing round-14 `W25-S1` item named by
  `CTO_ROUND_ANALYSIS_IRPT_FNTEND_ROUND_13_20260922.md`, a sibling cell of the same round-14 issuance built in its
  own separate worktree, not yet merged into this one. Filed as surprise row `IRPT_FNTEND-W36-S1` (BLOCKING,
  ARMED, `disarm_owner 2.0.0_SA_COO~F`).
  **COO AMENDMENT (post-report, row `IRPT_FNTEND-W36-S1`):** the issuer amended F86-AC4's invocation to isolate
  UNEXPECTED failures via a grep filter excluding the disclosed `generator-output-carries-unprojected-grant` gap,
  and independently verified `UNEXPECTED-FAIL-COUNT=0` live in this worktree. Re-run by this worker verbatim:
  output `UNEXPECTED-FAIL-COUNT=0`, matching `<expect>` exactly -- **PASS**. Raw suite unchanged (`654 pass / 27
  skip / 2 fail`, same 2 disclosed fe-s-81 lines, this cell's own surface still unaffected).
  **New finding (surprise row `IRPT_FNTEND-W36-S2`, OBSERVATION, ARMED, `disarm_owner 2.0.0_SA_COO~F`):** the
  amended filter (`grep "^✗" <log>`) matches **zero** lines of the raw log in this bun/terminal combination --
  bun's fail marker carries a leading ANSI escape (`\x1b[0m\x1b[31m`) before the `✗` glyph even under `NO_COLOR=1`,
  so the anchored pattern cannot match ANY fail line, known or unknown, by construction (positive control: `grep
  "^✗" <log>` alone returns rc=1 / 0 matches against a python-confirmed 2 real occurrences). Does not change this
  criterion's grade -- the literal output matches `<expect>` exactly, and this worker independently confirmed via
  the raw suite output that only the 2 disclosed fe-s-81 lines are present -- but the exclusion filter cannot
  currently be forced non-zero by any suite content, so it is not a working discriminator against a genuine new
  regression. Filed rather than silently accepted.
  **COO AMENDMENT 2 (post-worker-~36-report, row `IRPT_FNTEND-W36-S1` continued):** amendment 1's filter was
  ITSELF BROKEN in TWO independent, compounding ways: (a) the ANSI bug above (`NO_COLOR=1` does not suppress
  bun's colour codes in this bun version, so `^✗` matches 0 lines unconditionally); AND (b), caught independently
  by the issuing COO, the exclusion token `generator-output-carries-unprojected-grant` is the TEST FILE's
  hyphenated name, but bun prints the spaced `describe`/`test` wording `generator output carries
  unprojected_grant` -- so even after stripping ANSI, that token would silently exclude NOTHING, and a run
  carrying a genuine NEW unexpected failure could have produced the identical `UNEXPECTED-FAIL-COUNT=0` as a run
  with none. **Corrected invocation** (independently re-verified live by the issuing COO in this worker's own
  worktree, then re-run again by this worker itself, same worktree, 2026-09-22): strip ANSI first
  (`sed -r 's/\x1b\[[0-9;]*m//g'`), then exclude on the STABLE criterion-id token `F81-AC3/AC4` (present verbatim
  in both known fail lines' printed text, absent from every other line) rather than the file name or the full
  description text. This worker's own re-run: `UNEXPECTED-FAIL-COUNT=0`; the ANSI-stripped log carries exactly 2
  raw `✗` lines, and `grep -c` on that stripped log (no `-v`) returns 2, while `grep -vc "F81-AC3/AC4"` returns 0
  -- a genuine, non-vacuous exclusion of exactly the 2 known fe-s-81 lines, not a filter that reads zero
  regardless of content. **This supersedes the amendment-1 PASS above**, which was reached through a vacuous
  instrument even though its literal output happened to match `<expect>`; the corrected re-run is the one that
  actually discriminates. Rows `IRPT_FNTEND-W36-S1` and `IRPT_FNTEND-W36-S2` DISARM on this corrected,
  independently-confirmed re-run. F86-AC4 remains **PASS**, now on sound grounds.
- **F86-AC5** (judgment): RECORDED, no verdict taken. See the proof instance's acceptance row for the full
  citation-backed record (segment-for-segment behaviour on all four controls, plus the mutant-control evidence
  above).

## Surprise rows filed

- `IRPT_FNTEND-W36-S1` (`org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md`):
  F86-AC4's original whole-suite criterion could not read 0 fail inside this isolated worktree because it
  inherits round-14's `W25-S1` fix (a sibling cell, unmerged here) as an unresolved pre-existing failure. Was
  BLOCKING/ARMED, disarm_owner `2.0.0_SA_COO~F`. **DISARMED**: the COO's AMENDMENT 2 corrected invocation
  (ANSI-strip + stable-token exclusion), independently re-confirmed by this worker, genuinely and non-vacuously
  isolates the 2 known fe-s-81 lines.
- `IRPT_FNTEND-W36-S2`: amendment 1's exclusion filter was a no-op (matched zero lines regardless of content,
  ANSI-escape-vs-anchor mismatch even under `NO_COLOR=1`) AND relied on an exclusion token that never matched the
  printed text -- a second, independent bug the issuing COO caught. Was OBSERVATION/ARMED, disarm_owner
  `2.0.0_SA_COO~F`. **DISARMED**: the COO's AMENDMENT 2 corrected invocation, independently re-confirmed by this
  worker (`grep -c` on the ANSI-stripped log: 2 before exclusion, 0 after), now genuinely discriminates.

## Status

`<status>` remains `complete` (set by this worker's prior instance): all 5 criteria read PASS (F86-AC1/AC2/AC3/AC4)
or `UNVERIFIABLE-BY-INSTRUMENT` (F86-AC5, judgment, recorded for L9). F86-AC4's PASS was originally reached
through a vacuous instrument (amendment 1's grep filter, disclosed above); this record and the proof instance
are corrected here to reflect the COO's AMENDMENT 2 fix, independently re-verified live by this worker in this
same worktree -- F86-AC4 is PASS on sound grounds, not merely on matching literal output.
`proof-of-spec-check.py` returns `VALID (rc=0)` on the corrected instance.
