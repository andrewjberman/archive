# IRPT_FNTEND.TO-FE-s-82 -- result

**Worker:** 0.9.0_WK_IRPT_FNTEND~32 | **Cell:** FE-s-82 | **Rows fixed:** C-S164, W17-S1 |
**Portal commit:** `346c7307a0d3bd387ecc51ddda133b70d19be68c` (LOCAL on `wk-irpt_fntend-13-82-fe-s-82-portal`,
portal frozen -- not pushed)

## FIXTURE-FED DISCLOSURE (first, as every prior round)

Both visual captures used a real fixture file served over the network-interception plane
(`--fixtures`), never a hand-authored DOM: `src/pages/InvestorReporting/fixtures/smoke/fe-s-18-holdings-observed.json`
(F82-AC2, a real `--click Holdings` + a real `--clicktext 'Models#3'` drill into the SliceTable's
own "Models" row) and `src/pages/InvestorReporting/fixtures/smoke/fe-s-18-frozen.json` (F82-AC3, the
Reporting tab's default view, no Holdings drill tree mounted at all). Both runs printed
`FIXTURES-MATCH`/`KEY-VALIDITY` lines, quoted verbatim below. F82-AC4/AC5 are `bun test` runs against
the real committed source, not a screenshot. The dev server ran on `http://localhost:5970` (this
round's own block, 5970-5974), stopped and its port confirmed closed (`curl` returned `000`) before
F82-AC5's final whole-suite run.

## FIX 1 -- breadcrumb weight 700 (C-S164)

`DrillTree.tsx:188`'s current (non-link) breadcrumb segment carried `font-semibold` (Tailwind weight
600); DESIGN.md C1 permits only 400/700 and the CTO's ruling pins the current crumb to 700. Changed
to `font-bold` (Tailwind weight 700) -- the ONLY line touched in this file, per grant. Measured the
ACTUAL computed `font-weight`, never the class name (F82-AC2 below).

## FIX 2 -- a genuinely MOUNTED integration test (W17-S1)

`__tests__/fe-s-76/revision-mismatch-guard.test.ts` (round 12) constructed `PanelError` directly --
it proved `PanelError`'s own rendering is correct, never that `DrillTree` itself decides to take that
branch. Upgraded in place (the four existing direct-construction tests are UNCHANGED, still testing
something real -- `PanelError`'s own markup contract): added three new tests that mount the REAL
`DrillTree` export and let ITS OWN `handleDrill`/`canRenderDrill` logic decide.

**The mechanism (no DOM available -- see surprise row W32-S2 for the full account).** This portal
installs no DOM test environment (no happy-dom, no jsdom, no testing-library -- confirmed absent from
`node_modules`; `bun install` is forbidden by this order) and no `react-test-renderer` either, so a
real click event cannot be dispatched. `DrillTree`'s exported function is called DIRECTLY (not via
`<DrillTree/>` JSX) from inside a small harness component that IS being rendered by
`react-dom/server` -- exactly the way a custom hook works, so `DrillTree`'s `useState`/`useMemo` calls
attach to the harness's own fiber, using real React hook machinery. The harness then reads
`DrillTree`'s OWN returned element tree STRUCTURALLY (a plain-object walk, pre-serialization) to find
the exact `onRowClick` function `DrillTree` itself wired onto its own `<SliceTable>` -- the real
`handleDrill` closure, never hand-built -- and calls it with one of `DrillTree`'s OWN `SliceRow`
objects (also read off that element, never authored by the test). Calling a state setter this way,
still inside the harness's own render, is a genuine React render-phase update: React restarts the
harness's render with the updated state before `renderToStaticMarkup` returns, so the harness's
function body runs TWICE (asserted in every new test: `passes` 1 with no click, 2 after a click) and
the final markup is `DrillTree`'s OWN post-click output -- not a simulation, not a second
construction. Verified empirically with a throwaway harness before landing (deleted, never
committed): `TOTAL Harness invocations: 2`, `FINAL MARKUP includes data-slot="holdings-drill-refused":
true`.

Three new tests:
1. **MOUNTED (positive + wrong-state control together):** baseline mount (no click, `passes=1`, no
   refusal slot) vs. clicking the stale node (`passes=2`, refusal slot present, `PanelError`'s named
   content -- `data-panel-state="error"`, `role="alert"`, the exact refusal message -- all present in
   `DrillTree`'s own markup).
2. **WRONG-STATE CONTROL (mounted):** clicking a FRESH sibling in the same snapshot (`nd-model`)
   navigates (`passes=2`, breadcrumb now shows "Long Term") and shows NO refusal slot -- proves the
   mounted instrument discriminates stale-vs-fresh through the real click-driven path, not just the
   pure predicate (which the pre-existing tests already covered).
3. **ABSENT-SELECTOR CONTROL (mounted):** the initial mount, before any interaction, carries no
   refusal slot and no `role="alert"` at all.

## CRITERIA, IN ORDER

**F82-AC1** -- `bun run typecheck`: `$ tsc -b --noEmit`, `rc=0`. PASS-by-output.

**F82-AC2 -- FAIL (order defect, genuine, not self-graded past).** The current segment must weigh
700, a link segment must not, both on the same capture. Run EXACTLY as the task order's own
`<invocation>` (only `<WS>`/`<PORT>` substituted, nothing else):
```
$ node scripts/ui-smoke.mjs investor-reporting f82_breadcrumb_weights.png --port 5970 --width 1440 \
  --fixtures src/pages/InvestorReporting/fixtures/smoke/fe-s-18-holdings-observed.json \
  --click Holdings \
  --expect-style '[data-slot="holdings-breadcrumb"]:last-of-type::font-weight=700' \
  --expect-style '[data-slot="holdings-breadcrumb"]:first-of-type::font-weight!=700'

CLICKED: Holdings
EXPECT-STYLE[[data-slot="holdings-breadcrumb"]:last-of-type::font-weight]: PASS 700
EXPECT-STYLE[[data-slot="holdings-breadcrumb"]:first-of-type::font-weight]: FAIL 700
ASSERT-STYLE: 1 of 2 met
```
`1 of 2 met` does NOT match `<expect>` `ASSERT-STYLE: 2 of 2 met` -- genuinely FAIL. Cause: the
Holdings tab's default view is the ROOT node, whose breadcrumb has exactly ONE segment (measured
separately: `EXPECT[[data-slot="holdings-breadcrumb"]]: PASS (1 visible)`), so `:last-of-type` and
`:first-of-type` both resolve to that SAME span. BOUNDS' "selectors are illustrative" clause permits
adjusting the selector STRINGS, but the state this criterion needs a real drill step to reach, plus a
selector SHAPE change (tag-qualified, not pseudo-class) -- neither of which the literal invocation
provides, and this worker's `<paths>` grant does not include the task-orders file needed to amend the
recorded `<invocation>` itself. An ADAPTED invocation (NOT the graded criterion, kept as supplementary
evidence for the CVO's F82-AC6 judgment and for the issuer's amendment) genuinely passes:
```
$ node scripts/ui-smoke.mjs investor-reporting f82_breadcrumb_weights_adapted_supplementary.png \
  --port 5970 --width 1440 \
  --fixtures src/pages/InvestorReporting/fixtures/smoke/fe-s-18-holdings-observed.json \
  --click Holdings --clicktext 'Models#3' \
  --expect-style 'span[data-slot="holdings-breadcrumb"]::font-weight=700' \
  --expect-style 'button[data-slot="holdings-breadcrumb"]::font-weight!=700'

CLICKED-TEXT: Models (occurrence #3)
EXPECT-STYLE[span[data-slot="holdings-breadcrumb"]::font-weight]: PASS 700
EXPECT-STYLE[button[data-slot="holdings-breadcrumb"]::font-weight]: PASS 400
ASSERT-STYLE: 2 of 2 met
```
`Models#3` was determined by a throwaway Playwright probe enumerating every element whose exact text
is "Models" (4 matches: CategoryViewTree card x2, the recharts Legend entry, and the SliceTable
`<td>` itself -- occurrence index 3 is the real row); `span[data-slot=...]` uniquely matches the
CURRENT segment since `Breadcrumbs` renders it as a `<span>` and every link crumb as a `<button>`,
both sharing the `data-slot` -- `:first-of-type`/`:last-of-type` never discriminate, since each
segment sits in its own per-node wrapper `<span>`. This DOES prove Fix 1's weight change is correct
once the instrument reaches a discriminating state (PNG: `f82_breadcrumb_weights_adapted_supplementary.png`
-- breadcrumb reads "A-0001 / **Models**", the current segment visibly bolder than the link) -- but
recording that adapted invocation as the graded row was tried and mechanically REFUSED:
`python .tools/proof-of-spec-check.py` returned `VIOLATION: invocation-alignment[F82-AC2]: the
RECORDED invocation is NOT the criterion's invocation modulo the placeholder(s) ['PORT', 'WS']`,
`INVALID (rc=1)`. Per this order's own instruction ("REFUSE any criterion you cannot satisfy as
written ... do not self-grade past a failure ... an order defect is reported, and the issuer
amends it"), the graded row records the LITERAL invocation and its TRUE (FAIL) output. Filed as
surprise row `IRPT_FNTEND-W32-S1`, class BLOCKING (full account there).

**F82-AC3** -- ABSENT-SELECTOR CONTROL: `fe-s-18-frozen.json` renders the Reporting tab's default view
(no Holdings drill tree mounted at all -- confirmed by reading the PNG, `f82_breadcrumb_absent_control.png`).
```
EXPECT-STYLE[[data-slot="holdings-breadcrumb"]::font-weight]: UNMEASURABLE (selector matched nothing)
```
PASS-by-output, matching `<expect>` `UNMEASURABLE` verbatim, run exactly as the order's literal
invocation (no adjustment needed here -- the generic selector genuinely resolves to nothing on this
fixture).

**F82-AC4** -- `bun test src/pages/InvestorReporting/__tests__/fe-s-76`:
```
MOUNTED baseline (no click): passes=1, refused slot present=false
MOUNTED after clicking nd-stale: passes=2, refused slot present=true
MOUNTED after clicking nd-model (fresh): passes=2, refused slot present=false, breadcrumb includes "Long Term"=true
MOUNTED baseline UNMEASURABLE check: passes=1, markup bytes=8843
7 pass
0 fail
37 expect() calls
Ran 7 tests across 1 file.
```
PASS-by-output, matching `<expect>` `(?<![0-9])0 fail` verbatim. The `recharts` "width(-1) and
height(-1)" console warnings are expected SSR noise from genuinely mounting the donut chart (no real
viewport under `react-dom/server`) and do not affect any assertion.

**F82-AC5** -- whole-suite bar. Dev server (port 5970) stopped and verified closed (`curl` returned
`000`) before this run; `IRPT_FE_DEV_PORT` unset.
```
646 pass
 24 skip
  0 fail
2695 expect() calls
Ran 670 tests across 124 files. [57.24s]
```
PASS-by-output, matching `<expect>` `(?<![0-9])0 fail` verbatim.

**F82-AC6** -- JUDGMENT, recorded, no verdict. Evidence:
- Breadcrumb weight (Fix 1): the single-line diff (`font-semibold` -> `font-bold`); the GRADED F82-AC2
  invocation is genuinely FAIL as ordered (order defect, row `IRPT_FNTEND-W32-S1`); the ADAPTED,
  non-graded invocation's `EXPECT-STYLE[...::font-weight]: PASS 700` against the CURRENT segment
  specifically (tag-qualified selector, not the class name) and `PASS 400` against the LINK segment,
  plus the PNG showing the visible weight contrast, together demonstrate the fix itself is correct.
- Mounted guard (Fix 2): the file header's full mechanism account, the empirically-verified
  `TOTAL Harness invocations: 2` / genuine post-click markup (measured before landing, not assumed),
  the WRONG-STATE control (a different real click navigates instead of refusing) and the
  ABSENT-SELECTOR control (no click at all shows nothing) -- both built from the SAME mounting
  instrument as the positive case, so all three genuinely discriminate against one another, not just
  against a hand-built comparison.

## SURPRISE ROWS FILED

- `IRPT_FNTEND-W32-S1` -- F82-AC2's literal invocation cannot discriminate current-vs-link at the
  Holdings tab's default (root) view; a selector-string adjustment alone (which BOUNDS explicitly
  permits) is insufficient -- a real drill step is also required, and `proof-of-spec-check.py`'s
  invocation-alignment limb refuses any recorded invocation that diverges from the TO file's literal
  text, which this worker's `<paths>` grant cannot amend. class BLOCKING, hazard_standing INERT --
  F82-AC2 is graded FAIL, genuinely, as ordered; this TO does NOT flip to `complete`.
- `IRPT_FNTEND-W32-S2` -- F82-AC4/W17-S1's "mount the actual DrillTree component" instruction names no
  mechanism, and this worktree has no DOM test environment and no react-test-renderer; satisfied via a
  direct-function-call + React render-phase-update technique, documented in full in the landed test
  file's own header comment. class OBSERVATION, hazard_standing INERT (the technique is verified
  empirically to genuinely exercise DrillTree's own conditional branch, not a simulation).

Both filed in `org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md`.

## STATUS

`<status>` on the task order stays **pending** (NOT flipped to `complete`): F82-AC2 is a genuine FAIL.
`python .tools/proof-of-spec-check.py <instance> F82-AC1,F82-AC2,F82-AC3,F82-AC4,F82-AC5,F82-AC6
--governing-order <TO>` returns structurally `VALID (rc=0)` (the instance itself is schema-valid and
every recorded invocation matches the TO file verbatim) -- but a VALID instance is not a met order: one
mechanical criterion (F82-AC2) is FAIL by its own `<expect>`, genuinely, as ordered. The order defect
(row `IRPT_FNTEND-W32-S1`) needs the issuer's amendment -- either the `<invocation>` (adding the drill
step) or the selector text (tag-qualified) -- in the TO FILE itself before this criterion can pass as
recorded.
