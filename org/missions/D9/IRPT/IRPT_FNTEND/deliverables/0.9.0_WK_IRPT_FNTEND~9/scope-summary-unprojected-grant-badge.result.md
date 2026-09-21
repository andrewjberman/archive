# IRPT_FNTEND.TO-FE-s-59 -- result (0.9.0_WK_IRPT_FNTEND~9)

Portal commits, in order, LOCAL on branch `wk-irpt_fntend-9-59-fe-s-59-portal` (portal frozen, not pushed):
- `61dbe93cda24aa9d49aa0fdd73f32ecf87731ff4` -- `header/ScopeSummary.tsx`'s `PartialDisclosureFact`
  node and the new test `__tests__/fe-s-59/scope-summary-badge.test.ts`.
- `67f7973245039f7c99f67576565cd6f93190f497` -- the missed `__tests__/fe-s-59/smoke-fixtures.json`
  (F59-AC6's screenshot fixture; no change to ScopeSummary.tsx or the test file).

Workspace commits, LOCAL on branch `wk-irpt_fntend-9-59-fe-s-59`:
- `0c302d1b77` -- surprise row `IRPT_FNTEND-W9-S1` in `INVESTIGATION_v2.md`.
- `af1546e922` / `0bb7a1d4f0` -- this proof-of-spec instance, result and screenshot.

**Final HEAD for wave B to seat against: `67f79732` (portal).**

## Final measured state (this worktree)
- F59-AC1 (typecheck): `rc=0` -- **PASS**
- F59-AC2 (renders count/denominator/kinds verbatim when count>0): `3 pass / 0 fail`, printed
  `PARTIAL-DISCLOSURE RENDERS WHEN count>0: yes` -- **PASS**
- F59-AC3 (absent on count=0, unprojectedGrant null, scope null; 3 arms, no crash): printed
  `PARTIAL-DISCLOSURE ABSENT WHEN count=0, NULL, OR scope=null: yes (3 of 3)` -- **PASS**
- F59-AC4 (DOM sibling of, never descendant of, the cohort blocks; parsed ancestor chains, not
  eyeballed): printed `PARTIAL-DISCLOSURE OUTSIDE COHORT BLOCKS: yes` -- **PASS**
- F59-AC5 (whole suite green): `605 pass / 21 skip / 1 fail` of 627 -- **FAIL**. The sole residual
  is `fe-s-48/withheld.test.ts` `F48-AC4`, which diffs `header/ScopeSummary.tsx` against a fixed
  ancient vintage (`DEV 1f3ce9f0`) by a **naive positional-index compare**, not a real diff --
  it requires the file's total code-line count to be unchanged since that vintage. This cell's
  correctly-scoped, in-grant, additive render (net +27 lines, sited exactly where the cell text
  and BOUNDS require) inevitably trips it: measured BEFORE this cell's commit, the same
  invocation against the then-current HEAD printed `CODE LINES CHANGED OUTSIDE THE HEADER
  COMMENT: 1 of 111 [only the withheld fact: yes]`; AFTER, it prints `102 of 138 [... NO]`. F48's
  own FUNCTIONAL assertions on withheld-vs-unknown rendering (`F48-AC2`, `F48-AC3`) still PASS
  unchanged at this HEAD -- this is not a rendering regression, only a fragile self-test outside
  this cell's `<paths>` (`__tests__/fe-s-48/` is not granted). **REFUSED as written**; filed as
  surprise row `IRPT_FNTEND-W9-S1` (OBSERVATION, ARMED, `disarm_owner 2.0.0_SA_COO~F`).
- F59-AC6: judgment, RECORDED, no verdict. Screenshot
  `fe-s-59_scope_badge_1440.png` (1440x900, canvas `rgb(244, 246, 250)` matching `DESIGN.md` C3)
  shows the new "NOT FULLY PROJECTED" cell as the sixth entry in the same white-panel Fact row as
  Selection/Permitted accounts/Scope as of/Directory as of/Scope match -- same label and value
  typography as its siblings, navy ink on the white panel, no light-on-light idiom. The DOM-level
  separation from the cohort blocks (never a shared container/class) is confirmed by F59-AC4's
  parser, a stronger instrument than a screenshot for that specific claim since the fixture used
  for the screenshot carries no cohort data at all.

Per this order's own rule (a criterion the worker cannot satisfy as written is REFUSED, never
self-graded past a real failure), `<status>` stays `pending`: F59-AC5 measures 1 fail, not 0, for
a reason outside this cell's authority to fix.

## Rows filed
- `IRPT_FNTEND-W9-S1` -- new, OBSERVATION, ARMED, `disarm_owner 2.0.0_SA_COO~F`. Names the exact
  mechanism (naive positional-index diff in `fe-s-48/withheld.test.ts` F48-AC4) and warns it will
  refuse ANY future cell that changes `header/ScopeSummary.tsx`'s line count above that test's
  checked position, correct or not.

## Proof-of-spec
`org/missions/D9/IRPT/IRPT_FNTEND/deliverables/0.9.0_WK_IRPT_FNTEND~9/IRPT_FNTEND.TO-FE-s-59.scope-summary-unprojected-grant-badge.proof_of_spec.json`
-- `proof-of-spec-check.py` run before this file was finalized; see the WORKER REPORT for its
exact rc and output. F59-AC5 carries `status: FAIL` by its own printed output, so the `complete`
flip is correctly withheld, matching the same pattern FE-s-57's own deliverable used one cell
earlier on this file.
