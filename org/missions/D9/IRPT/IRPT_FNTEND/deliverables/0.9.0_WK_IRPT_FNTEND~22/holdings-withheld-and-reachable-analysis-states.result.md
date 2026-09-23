# IRPT_FNTEND.TO-FE-s-72 -- result

**Every capture below is FIXTURE-FED: the real route with fixtures answered at the network layer
(playwright's `page.route`, `scripts/ui-smoke.mjs`), never a live backend.** That is the right
evidence for THIS card (FWD-12, "the screens look and behave like the rest of the portal" -- a
claim about rendered familiarity on the real page, satisfied by a real render of the real
component tree against a controlled wire response, and needing no live-route counterpart) and it
is explicitly NOT the right evidence for the five component-level Analysis states proved only at
F72-AC9 (see below) -- those are unreachable from the browser at all, fixture or live, and this
result never claims otherwise.

## Reachable-vs-unreachable state table

| State | Reachable from the browser today? | Evidence class | Source |
|---|---|---|---|
| Analysis: `requests-unavailable` (honest no-declared-route disclosure) | **YES** | Browser (fixture-fed) | F72-AC2/AC3; `api/endpoints/investor-reporting.ts:1012-1013` (`LiveClient.listAnalysisRequests` unconditionally `Promise.reject(new NoDeclaredRoute(...))`) |
| Analysis: `generate-composer` | **YES** (rendered unconditionally in `AnalysisTab.tsx`, both branches) | Browser (fixture-fed) | F72-AC2; `AnalysisTab.tsx:196-208` |
| Holdings: out-of-enum ADVISORY token (pre-existing, not this cell's fix) | **YES** | Browser (fixture-fed) | F72-AC4/AC5; `SliceTable.tsx` `AdvisoryCell`, `slices.ts` `isOutOfEnumAdvisory` |
| Holdings: WITHHELD classification gap (this cell's authored fixture) | **YES** | Browser (fixture-fed) | F72-AC6/AC7/AC8; `HoldingsTab.tsx` `HoldingsQualification`, `slices.ts` `renderedClassification` |
| Analysis: `input-review` (selected-request gated) | **NO -- structurally unreachable from the browser** | Component-level only (test-only seed props) | F72-AC9; `AnalysisTab.tsx:162,209-227` |
| Analysis: `stage-display` (selected-request gated) | **NO -- structurally unreachable** | Component-level only | F72-AC9 |
| Analysis: `variant-selector` (selected-request gated) | **NO -- structurally unreachable** | Component-level only | F72-AC9 |
| Analysis: `revision-identity` (selected-request gated) | **NO -- structurally unreachable** | Component-level only | F72-AC9 |
| Analysis: `native-sections` (selected-request + released report gated) | **NO -- structurally unreachable** | Component-level only | F72-AC9 |

**Why the last five are unreachable, not merely unbuilt.** `AnalysisTab.tsx`'s `useEffect` calls
`api.listAnalysisRequests(scopeRef)` (line 118) and its `.catch` sets `requests` to `[]` and
`selectedRequestId` to `null` (lines 127-129) on ANY rejection. `LiveClient.listAnalysisRequests`
(`api/endpoints/investor-reporting.ts:1012-1013`) is a bare `Promise.reject(new
NoDeclaredRoute(IR_UNSERVED_LIST_OPERATION))` with a doc comment stating "NO LIST ROUTE EXISTS,
under v1 either" -- there is no wire call to intercept, fixture or live, because none is ever made.
So `requests` can never hold a non-empty array in the running app, `selectedRequest`
(`requests.find(...)`, line 162) can never be non-null, and every one of the five states gated on
`selectedRequest !== null` (lines 209-227) is dead code from the browser's perspective. This is the
CTO's ruling (this TO's cell text): FNTEND must not invent a route to make them reachable.
F72-AC9 proves the five COMPONENTS render correctly using the test-only `initialRequests` /
`initialReport` seed props `AnalysisTab.tsx` already documents ("the live app never passes this")
-- a DIFFERENT evidence class from a browser disclosure, proving the components work, never that a
real user can reach them.

## Criteria

### F72-AC1 -- whole portal typechecks
Invocation: `cd <WS>/portal && timeout 180 bun run typecheck; echo rc=$?`
Output: `$ tsc -b --noEmit` then `rc=0`.
**PASS** against `<expect>rc=0(?![0-9])</expect>`.

### F72-AC2 -- Analysis tab honest disclosure, white panel
Invocation as ordered (fixtures/smoke/fe-s-18-frozen.json, `--click Analysis`).
Output: `EXPECT[[data-slot="requests-unavailable"]]: PASS (1 visible)` / `EXPECT[[data-slot="generate-composer"]]: PASS (1 visible)` /
`EXPECT-TEXT[[data-slot="requests-unavailable"]::UNAVAILABLE: analysis requests are not available (no-declared-route)]: PASS` /
`EXPECT-GROUND[[data-slot="request-list"]]: PASS rgb(255, 255, 255)` / `ASSERT-CONTENT: 3 of 3 met` / `ASSERT-GROUND: 1 of 1 met`.
Capture read: `f72_unavailable.png` -- the Analysis tab shows the Generate composer above an honest
"UNAVAILABLE: analysis requests are not available (no-declared-route)" line on a white panel; no
invented request list. DESIGN.md C3 (white panel = `palette.surface` `#FFFFFF`, rgb(255,255,255)) satisfied.
**PASS** against `<expect>ASSERT-CONTENT: 3 of 3 met[\s\S]*ASSERT-GROUND: 1 of 1 met</expect>`.

### F72-AC3 -- content control (no click)
Output: `EXPECT[[data-slot="requests-unavailable"]]: FAIL (0 visible)` / `ASSERT-CONTENT: 0 of 1 met`.
Capture read: `f72_unavailable_control.png` -- Reporting tab stays active (as loaded), no analysis
disclosure text anywhere; confirms the assertion in AC2 is reading a real, click-gated state.
**PASS** against `<expect>ASSERT-CONTENT: 0 of 1 met</expect>`.

### F72-AC4 -- Holdings out-of-enum ADVISORY (pre-existing, unmodified fixture)
Output: `EXPECT[[data-slot="slice-advisory"][data-advisory-out-of-enum="true"]]: PASS (3 visible)` /
`EXPECT-TEXT[...slice-advisory-verbatim...::ADVISORY]: PASS` / `EXPECT-TEXT[...slice-advisory-flag...]: PASS` /
`EXPECT-GROUND[[data-slot="slice-table"]]: PASS rgb(255, 255, 255)` / `ASSERT-CONTENT: 3 of 3 met` / `ASSERT-GROUND: 1 of 1 met`.
Capture read: `f72_holdings_advisory.png` -- all three holdings nodes (Models/SMA/Client) carry the
verbatim "ADVISORY" token with the "(not a contract advisory value -- shown as sent)" flag, on a
white slice table. **PASS** against `<expect>ASSERT-CONTENT: 3 of 3 met[\s\S]*ASSERT-GROUND: 1 of 1 met</expect>`.

### F72-AC5 -- content control (forced holdings failure)
Output: `FORCED-FAIL: investor-reporting/holdings/` (x5) / `EXPECT[[data-slot="slice-advisory"]]: FAIL (0 visible)` /
`EXPECT[[data-slot="slice-table"]]: FAIL (0 visible)` / `ASSERT-CONTENT: 0 of 2 met`.
Capture read: `f72_holdings_control.png` -- "Failed / IR-REQUEST-FAILED" status panel with a Retry
button; neither slot renders. **PASS** against `<expect>ASSERT-CONTENT: 0 of 2 met</expect>`.

### F72-AC6 -- authored WITHHELD fixture, 1440
`fixtures/withheld.json` built as a byte copy of the THREE wire-keyed bodies of
`fe-s-18-holdings-observed.json` that this click-Holdings flow actually exercises -- measured
empirically via `--netlog` against the unmodified 9-key file: `FIXTURES-MATCH: matched 3 of 9`
(dead: directory/search, narrative/, analysis/, status/, status, export/), so only
`directory/resolve`, `performance/` and `holdings/` are live in this flow. Holdings node index 2
(`N-SMA`, the SAME node that carries the out-of-enum ADVISORY token in the unmodified fixture) has
`classification.authoritative` flipped to `false`; every other byte, including the other two
nodes' advisory tokens, is untouched.
Output: `EXPECT[[data-slot="holdings-qualification"]]: PASS (1 visible)` /
`EXPECT[[data-slot="holdings-classification-gap"][data-unknown-nodes="1"][data-nodes="4"]]: PASS (1 visible)` /
`EXPECT-TEXT[...::Classification unknown for 1 of 4 holdings nodes]: PASS` /
`EXPECT-TEXT[...nth-of-type(2)...slice-supervision...::withheld]: PASS` /
`EXPECT-TEXT[...nth-of-type(2)...slice-advisory...::withheld]: PASS` /
`EXPECT-GROUND[[data-slot="holdings-qualification"]]: PASS rgb(255, 255, 255)` /
`ASSERT-CONTENT: 5 of 5 met` / `ASSERT-GROUND: 1 of 1 met` / `FIXTURES-MATCH: matched 3 of 3`.
Capture read: `f72_withheld_1440.png` -- the qualification note "Classification unknown for 1 of 4
holdings nodes -- their supervision and advisory partitions are shown as withheld, not as a
classification" on a white panel; the SMA row alone reads Supervision=withheld, Advisory=withheld,
while Models and Client keep their ADVISORY out-of-enum rendering -- the two states are visually
and structurally distinct on the SAME page. Re-run twice for determinism: identical
`ASSERT-CONTENT: 5 of 5 met` / `ASSERT-GROUND: 1 of 1 met` / `FIXTURES-MATCH: matched 3 of 3` both
times. **PASS** against `<expect>ASSERT-CONTENT: 5 of 5 met[\s\S]*ASSERT-GROUND: 1 of 1 met</expect>`.

### F72-AC7 -- same withheld state, 390
Output: `EXPECT[[data-slot="holdings-qualification"]]: PASS (1 visible)` /
`EXPECT[...data-unknown-nodes="1"...]: PASS (1 visible)` /
`EXPECT-TEXT[...slice-supervision...::withheld]: PASS` / `ASSERT-CONTENT: 3 of 3 met`.
Capture read: `f72_withheld_390.png` -- same qualification note and withheld cell, readable at 390
(the summary card, category-view band and slice table all reflow without clipping).
**PASS** against `<expect>ASSERT-CONTENT: 3 of 3 met</expect>`.

### F72-AC8 -- content control (unmodified fixture, same expectations)
Output: `EXPECT[[data-slot="holdings-classification-gap"]]: FAIL (0 visible)` /
`EXPECT-TEXT[...slice-supervision...::withheld]: FAIL` / `ASSERT-CONTENT: 0 of 2 met`.
Confirms the qualification note and the withheld cell are NOT present against the unmodified
fixture (node 2 stays authoritative, all three nodes ADVISORY) -- the AC6/AC7 assertions are
reading a real fixture effect, not a component that always renders these slots.
**PASS** against `<expect>ASSERT-CONTENT: 0 of 2 met</expect>`.

### F72-AC9 -- non-browser guard, the five selected-request states
`portal/src/pages/InvestorReporting/__tests__/fe-s-72/reachable-states.test.ts`. Seeds
`AnalysisTab` with a real adapted, RELEASED `AnalysisRequest` (FE-s-6's own
`fixtures/fe-s-6/request.overview.json`, read-only, loaded through the same `FixtureAdapter` call
path `sections.test.ts` already exercises) and its paired `AnalysisReport`
(`report.released.json`), via `initialRequests`/`initialReport`. Output (both runs identical):
```
SLOT[input-review]: PRESENT (component-level seed, not a browser disclosure)
SLOT[stage-display]: PRESENT (component-level seed, not a browser disclosure)
SLOT[variant-selector]: PRESENT (component-level seed, not a browser disclosure)
SLOT[revision-identity]: PRESENT (component-level seed, not a browser disclosure)
SLOT[native-sections]: PRESENT (component-level seed, not a browser disclosure)
CONTROL (no seed): any of the five present = false
1 pass, 0 fail, 8 expect() calls
```
The same test's built-in negative control (no seed, the live app's actual starting -- and, since
`listAnalysisRequests` never resolves, PERMANENT -- state) renders NONE of the five and shows
`data-slot="no-analysis-requests"` instead, confirming the PRESENT readings above are a real seed
effect. **This proves the five components render correctly given the seed. It does NOT show, and
this result does not claim, that a real browser user can ever reach them** -- see the state table
and "why unreachable" above. **PASS** against `<expect>(?<![0-9])0 fail</expect>`.

### F72-AC10 -- whole IRPT_FNTEND suite green
Invocation: `cd <WS>/portal && timeout 600 bun test src/pages/InvestorReporting` (dev server
stopped and port verified closed beforehand; `IRPT_FE_DEV_PORT` unset in this shell).
Output: `620 pass`, `22 skip`, `0 fail`, `2611 expect() calls`, `Ran 642 tests across 117 files.`
**PASS** against `<expect>(?<![0-9])0 fail</expect>`.

### F72-AC11 -- judgment, RECORDED, no verdict
The state table above states, for the record the CVO grades at L9 against C-S129: the browser-
reachable states (`requests-unavailable`, the composer, and both Holdings classification states --
out-of-enum ADVISORY and this cell's WITHHELD) versus the five states proved only at the component
level (`input-review`, `stage-display`, `variant-selector`, `revision-identity`, `native-sections`
-- unreachable because `listAnalysisRequests` unconditionally rejects with `NoDeclaredRoute`), as
TWO DIFFERENT EVIDENCE CLASSES, neither substituting for the other. The Holdings withheld state is
distinguished from the pre-existing out-of-enum ADVISORY case (same page, same fixture family,
different node). No request-list route was invented anywhere in this work. RECORDED, no verdict
given by this worker.

## Rows filed

- **IRPT_FNTEND-W22-S1** (OBSERVATION, ARMED, disarm_owner `2.0.0_SA_COO~F`): per this TO's own
  BOUNDS clause, three measured text slots (`requests-unavailable`, `holdings-classification-gap`,
  `slice-supervision`) resolve their computed text colour to an `oklch(...)` value (Tailwind's
  default `slate-600`/`slate-800`/`slate-700`) with no DESIGN.md clause naming it or giving it a
  hex/oklch equivalence -- the same class of gap as row `IRPT_FNTEND-W13-S2`. Filed, not fixed
  (DESIGN.md is outside this cell's `<paths>` grant).

## Fixes made

None. This TO is EVIDENCE ONLY: no component or DESIGN.md edit was made or attempted. The one
authored artifact is the fixture (`fixtures/withheld.json`) and the one authored test
(`reachable-states.test.ts`), both inside this cell's own `__tests__/fe-s-72/` grant.

## Controls

**Mutant** (on this cell's own authored test, `reachable-states.test.ts`): the loop's
`expect(present).toBe(true)` was temporarily inverted to `.toBe(false)`. Expected: the assertion
fails on the first iterated slot (`input-review`), since `expect()` throws and aborts the
`for`-loop at the first failing iteration. Observed: exactly that -- `1 fail`, `0 pass`, error at
line 64 ("Expected: false, Received: true"), naming `input-review`'s own SLOT log line
immediately above it. Reverted; re-run clean (`1 pass`, `0 fail`, `8 expect() calls`, identical
SLOT/CONTROL lines to the pre-mutant run). **FIRED-AS-EXPECTED.**

Every visual criterion additionally carries its OWN wrong-state content control as a separate
acceptance row (F72-AC3 for AC2, F72-AC5 for AC4, F72-AC8 for AC6/AC7) per this round's CRITERION
RULE part (c) -- not a supplementary mutant, but the same discipline: each assertion's wrong-state
arm was run and confirmed to fail before the passing arm was trusted.

**Determinism**: `reachable-states.test.ts` run twice on the unmodified file -- identical `1 pass`,
`0 fail`, `8 expect() calls`, identical SLOT/CONTROL log lines both times (only wall-clock timing
differed, 294ms vs 266ms). F72-AC6's ui-smoke invocation run twice on the same dev server --
identical `ASSERT-CONTENT: 5 of 5 met`, `ASSERT-GROUND: 1 of 1 met`, `FIXTURES-MATCH: matched 3 of
3` both times. **STABLE.**

## Ports

Dev server run at port 5970 (this worktree's own block, 5970-5979), `IRPT_FE_DEV_PORT=5970` as an
inline prefix, never exported in the shell that ran F72-AC1/AC9/AC10. Stopped before F72-AC10 via
PowerShell `Get-NetTCPConnection -LocalPort 5970 -State Listen | Stop-Process -Force`; verified
closed both times with `curl -s -o /dev/null -w "%{http_code}" http://localhost:5970/` reading
`000`.
