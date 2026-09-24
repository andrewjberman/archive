# FE-s-68 result -- the Reporting tab's answer-bearing state, and the scope strip's partial-disclosure fact

Worker `0.9.0_WK_IRPT_FNTEND~18`, `IRPT_FNTEND.TO-FE-s-68`.

**These captures are FIXTURE-FED**: every screenshot below rendered the real `/investor-reporting`
route in this worktree's own dev server (port 5930), with the network layer's own three endpoints
(`directory/resolve`, `performance/`, `holdings/`) answered by a static fixture body via
`scripts/ui-smoke.mjs --fixtures`. No live backend, database or scoped API was reached. That is the
right evidence for THIS card: FWD-12's DONE WHEN is "an advisor who already uses the portal needs no
re-learning" on the REAL rendered page -- a visual/behavioural claim about markup, class and computed
style that a fixture-fed render answers exactly as well as a live one would, because the fixture only
replaces the network response body, never the component tree, the CSS or the DOM. It is NOT the right
evidence for a card whose DONE WHEN is about a live data path, a real scoped grant, a real vendor
round-trip, or timing/latency against a live backend -- none of which this card asserts.

## Base

Portal DEV before this worker's commit: `243089eb` (workspace base) with FE-s-65's instrument and
FE-s-66's two fixtures already landed (verified before touching anything: `grep FIXTURES-MATCH
scripts/ui-smoke.mjs` hit at `:154`,`:510`,`:527`; `fixtures/smoke/reporting-answer-bearing.json` and
`fixtures/smoke/reporting-answer-bearing-partial.json` both present at
`src/pages/InvestorReporting/fixtures/smoke/`). This worker's portal commit:
`12cdfd434104b18835c8aa72a81d9d773807db10`.

Dev server: `IRPT_FE_DEV_PORT=5930 bun run dev --port 5930` (5930 chosen from the 5930-5939 block,
verified free with `curl` before starting: all of 5930-5933 returned `000`). Stopped before F68-AC10
and the port's closure re-verified (see END OF RUN below).

## Fixes made (both within `<paths>`)

### 1. `header/ScopeSummary.tsx` -- `PartialDisclosureFact`'s weight and ink (C1, C3, C9)

BEFORE (live-measured, `--expect-style` with no target so the actual value prints):
```
EXPECT-STYLE[[data-slot="partial-disclosure"] > span:first-child::color]: FAIL oklch(0.446 0.043 257.281)
EXPECT-STYLE[[data-slot="partial-disclosure"] > span:last-child::color]: FAIL oklch(0.208 0.042 265.755)
EXPECT-STYLE[[data-slot="partial-disclosure"] > span:last-child::font-weight]: FAIL 500
```
(classes were `text-slate-600` / `text-sm font-medium text-slate-900` -- `font-medium` is weight 500,
which C1 forbids outright, 400/700 only; `text-slate-900` is not the contract's navy ink `#163372`).

Fix: `text-slate-600` -> `text-[hsl(var(--palette-darkGray))]` (the codebase's own existing secondary-ink
convention, e.g. `PanelStates.tsx`'s `SECONDARY_INK`); `text-sm font-medium text-slate-900` ->
`text-sm font-normal text-[hsl(var(--palette-navy))]` (matching `PanelStates.tsx`'s `INK` /
`CategoryViewTree.tsx`'s navy usage).

AFTER, exact criterion invocation (F68-AC9):
```
EXPECT-STYLE[[data-slot="partial-disclosure"] > span:last-child::font-weight]: PASS 400
EXPECT-STYLE[[data-slot="partial-disclosure"] > span:last-child::color]: PASS rgb(22, 51, 114)
EXPECT-STYLE[[data-slot="partial-disclosure"] > span:first-child::color]: PASS rgb(107, 114, 128)
ASSERT-STYLE: 3 of 3 met
```
Capture: `f68_style_before.png` (filename as the order's own invocation names it; it is the AFTER-fix
state -- the criterion only exists to prove the fixed values, there is no separate "before" capture
required by the order).

### 2. `tabs/reporting/AnswerStatus.tsx` -- the answer-status band's radius (C11)

Not required by any criterion, but directly observable in every capture this cell already produces
(`[data-slot="answer-status"]` renders in F68-AC2/AC6/AC3/AC7/AC4's arms) and squarely the same defect
class the order names for the cohort chip (radii are 2/3/4px or a pill; `rounded-md` renders 6px in this
Tailwind v4 build -- confirmed live, see below).

BEFORE:
```
EXPECT-STYLE[[data-slot="answer-status"]::border-radius]: FAIL 6px
```
Fix: `rounded-md` -> `rounded-[4px]` on both the `complete` and `qualified` class strings, matching the
convention `Panel.tsx` already uses for container radius (`rounded-[4px]`, not a bare `rounded-md`).

AFTER:
```
EXPECT-STYLE[[data-slot="answer-status"]::border-radius]: FAIL 4px
```
(printed FAIL only because no target value was supplied to this diagnostic call -- the actual value
`4px` is what matters and matches the contract's `rounded.md` token).

Checked before touching it: no test under `__tests__/` names `answer-status` in a class-string
comparison, and `fe-s-40/band-at-390.test.ts` (which imports this component) asserts wrap geometry only,
never a class string (0 hits for "rounded" in that file).

### Cohort-chip radius -- NOT fixed, filed as a row

`ScopeSummary.tsx:125`'s cohort-chip button also carries `rounded-md` (same 6px violation), named
explicitly by the order's own cell text as a finding to FILE rather than fix, because rendering it needs
an authoritative cohort selected via a directory/search row -- a state no fixture in this cell's
`fixtures/smoke/` populates (`row` is `null` in every render this cell's criteria exercise; confirmed by
reading all eight `f68_*.png` captures: none show a "Cohort" block). Filed as
`IRPT_FNTEND-W18-S1` in `INVESTIGATION_v2.md`.

## Criteria

| id | invocation result (verbatim key line) | verdict |
|---|---|---|
| F68-AC1 | `bun run typecheck` rc=0 | PASS |
| F68-AC2 | `ASSERT-CONTENT: 8 of 8 met`, `FIXTURES-MATCH: matched 3 of 3` | PASS |
| F68-AC6 | `ASSERT-CONTENT: 8 of 8 met`, `FIXTURES-MATCH: matched 3 of 3` | PASS |
| F68-AC3 | `ASSERT-GROUND: 2 of 2 met` | PASS |
| F68-AC7 | `ASSERT-GROUND: 2 of 2 met` | PASS |
| F68-AC4 | `FORCED-FAIL: investor-reporting/performance/`, `ASSERT-CONTENT: 0 of 8 met` | PASS |
| F68-AC5 | `ASSERT-CONTENT: 2 of 2 met` | PASS |
| F68-AC8 | `ASSERT-CONTENT: 0 of 2 met` | PASS |
| F68-AC9 | `ASSERT-STYLE: 3 of 3 met` | PASS |
| F68-AC10 | `619 pass / 0 fail` (`bun test src/pages/InvestorReporting`, dev server stopped, `IRPT_FE_DEV_PORT` unset) | PASS |
| F68-AC11 | judgment -- recorded below, no verdict | RECORD |

A first full-suite run (taken with the dev server already stopped) read `3 fail`: `F45-AC9`
(`fe-s-45/residuals.test.ts`, entirely outside this cell's grant and unrelated to any file this worker
touched -- a vite dev/build/preview process-spawn/`.vite-temp`-write-count test) and `F48-AC2`/`F48-AC3`
(`fe-s-48/withheld.test.ts`, IN grant). Diagnosed rather than accepted: F45-AC9 was re-run in isolation
twice, both times `0 fail` -- it is a flake from resource contention across a 641-test/116-file run, not
caused by this worker's edits (confirmed by literally reverting both edited files via the Edit tool,
re-running fe-s-45 alone -- passed -- then reapplying the edits and re-running fe-s-45 alone again --
still passed). F48-AC2/AC3 fail by construction until the portal repo is committed: both tests' own
`renderBoundToHead()` compares the *working copy* of `ScopeSummary.tsx` against the *committed HEAD blob*
and refuses to grade unless they are byte-identical -- true of any uncommitted edit to that file,
regardless of what changed. Neither test's assertions touch the lines this worker changed
(`PartialDisclosureFact`, not the cohort-chip button `fe-s-42`/`fe-s-48`/`fe-s-59` pin). After committing
(`12cdfd43`), `fe-s-48/withheld.test.ts` alone: `4 pass, 0 fail`; the full suite re-run:
`Ran 641 tests across 116 files` with `619 pass, 22 skip, 0 fail` (F68-AC10's own quoted line above is
from this second, post-commit run).

## The three pinning tests (`<paths>` grant, updated in the same commit as any class change -- none needed)

Neither of this worker's two fixes touched a class string those three tests pin (only
`PartialDisclosureFact`'s two spans and `AnswerStatus`'s band radius changed; none of `fe-s-42`,
`fe-s-48`, `fe-s-59` assert on either). Status after this worker's commit, run individually:

- `__tests__/fe-s-42/every-site.test.ts`: `4 pass, 0 fail`.
- `__tests__/fe-s-48/withheld.test.ts`: `4 pass, 0 fail` (only passes once the portal commit lands --
  see above; confirmed both before, FAIL x2, and after, PASS x4).
- `__tests__/fe-s-59/scope-summary-badge.test.ts`: `7 pass, 0 fail` (run together with fe-s-42 in one
  invocation; both files green).

No edits were needed or made to any of the three pinning test files.

## F68-AC11 (judgment -- RECORD only, no verdict)

Read against DESIGN.md C1/C3/C9 at both 1440 and 390:

- **C3/C9 (surface, ink)**: the answer-bearing body sits on a white panel (`#FFFFFF`, confirmed
  `ASSERT-GROUND` above) on the canvas (`#F4F6FA`); all body text reads navy; the `.ir-page` sheet's own
  ink `#0A1733` sits beside (not on top of) the report body as an OBSERVATION only, per the order's own
  instruction -- not asserted by any criterion here.
- **C1**: the fixed partial-disclosure value now renders at weight 400 (never 500), Lato throughout;
  no monospace observed.
- The three UNAVAILABLE metric cards (Beginning value, Ending value, Period return) render exactly
  `UNAVAILABLE (no-household-value-fact)` / `UNAVAILABLE (no-household-value-fact)` /
  `UNAVAILABLE (no-summary-return-for-answered-window)` on every capture -- this is the wire's own shape
  (no fixture in this tree carries `beginningValue`/`endingValue`/a household-level summary return), not
  a defect this cell can fix; F68-AC2/AC6's content bar is the `.ir-metric-card` COUNT (3, asserted and
  met), never the card text.
- **Observation, not a finding under this cell's grant**: at 390 wide, the "Accounts in this report"
  table (`AccountDetail`, `render/performance/` -- read-only to this cell) overflows horizontally and its
  rightmost columns ("Ending value (USD)", part of "Period returns") are clipped by the viewport edge in
  the 390-wide capture. Left for the CVO's own read; not this cell's surface to fix.
- **Observation**: `AnswerStatus.tsx`'s band still uses `border-slate-200`/`bg-white`/`text-slate-900`
  (complete) and `border-amber-500`/`bg-amber-50`/`text-amber-950` (qualified) -- Tailwind default
  palette tokens, not the contract's literal hex/hairline/status tokens. No criterion here tests these
  colours and this worker did not change them (only the radius); left for the CVO's own C3/C6/C9 read.

## Surprise rows filed

- `IRPT_FNTEND-W18-S1` (OBSERVATION, INERT) -- the cohort-chip `rounded-md` (6px, C11), per the order's
  own instruction to file rather than fix.
  `org/missions/D9/IRPT/IRPT_FNTEND/surprise-channel/investigations/INVESTIGATION_v2.md`.

## END OF RUN

Dev server (port 5930) stopped via PowerShell `Get-NetTCPConnection -LocalPort 5930 -State Listen` ->
`Stop-Process -Id <pid> -Force`; re-checked with the same `Get-NetTCPConnection` query (`CLOSED`) and
with `curl -o /dev/null -w '%{http_code}' http://localhost:5930/` (`000`). F68-AC10 ran in a shell with
`IRPT_FE_DEV_PORT` unset (`unset IRPT_FE_DEV_PORT` issued first; echoed empty).

## Commits

- Portal (`<WS>/portal`, branch `wk-irpt_fntend-11-68-fe-s-68-portal`):
  `12cdfd434104b18835c8aa72a81d9d773807db10`.
- Workspace (`<WS>`, branch `wk-irpt_fntend-11-68-fe-s-68`): this deliverables/investigation commit (see
  worker report for hash).

Push state: LOCAL only, both repos. Never pushed, merged, rebased or `checkout --`.
