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
- **F86-AC4** (whole suite): `654 pass / 27 skip / 2 fail`, rc=1. **REFUSED as written.** Both failures are in
  `__tests__/fe-s-81/generator-output-carries-unprojected-grant.test.ts`, entirely outside this cell's `<paths>`
  grant (`fe-s-13-wire.json` 0/9, `fe-s-14-print-v1.json` 0/2, missing `unprojected_grant`) -- the pre-existing
  round-14 `W25-S1` item named by `CTO_ROUND_ANALYSIS_IRPT_FNTEND_ROUND_13_20260922.md`, a sibling cell of the same
  round-14 issuance built in its own separate worktree, not yet merged into this one. Filed as surprise row
  `IRPT_FNTEND-W36-S1` (BLOCKING, ARMED, `disarm_owner 2.0.0_SA_COO~F`). This cell's own surface is otherwise
  unaffected. **This TO is NOT flipped `complete` on this criterion.**
- **F86-AC5** (judgment): RECORDED, no verdict taken. See the proof instance's acceptance row for the full
  citation-backed record (segment-for-segment behaviour on all four controls, plus the mutant-control evidence
  above).

## Surprise row filed

`IRPT_FNTEND-W36-S1` (`org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md`):
F86-AC4's whole-suite criterion cannot read 0 fail inside this isolated worktree because it inherits round-14's
`W25-S1` fix (a sibling cell, unmerged here) as an unresolved pre-existing failure. BLOCKING, ARMED, disarm_owner
`2.0.0_SA_COO~F` -- disarmed once `W25-S1` lands and a worktree carrying that merge re-reads 0 fail.

## Status

`<status>` left `pending` (NOT flipped to `complete`): F86-AC4 is a genuine, measured FAIL on this cell's own
literal invocation, per BOUNDS ("REFUSE any criterion you cannot satisfy as written... do not self-grade past a
failure"). `proof-of-spec-check.py` is expected to (and does) return non-zero on this instance until either the
issuer amends F86-AC4's bar for a worker in this position, or a re-run happens on a worktree carrying `W25-S1`'s
merge.
