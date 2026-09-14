# IRPT_FNTEND.TO-FE-s-30 -- one availability gate, on the report, and Reporting under it

Worker `0.9.0_WK_IRPT_FNTEND~1`. Worktree pair `/c/tmp/wk-irpt_fntend-5-1-fe-s-30` (workspace base CLOUD
@0a74710f33) / `.../portal` (base DEV @c2eb8eb4). Portal commit **fcc91358** (LOCAL; the portal is frozen).
Proof instance: `IRPT_FNTEND.TO-FE-s-30.availability-gate.proof_of_spec.json`, beside this file.

## What changed

- `state/availability.ts` (NEW). `isAnswerBearing(availability)` is the one gate (ruling H).
  - **When a `producerState` is present,** the gate reads it. The producer's five answer-bearing states
    (READY, PARTIAL, STALE, NEEDS_CORRECTION, UNCERTAIN) give a body. QUEUED, RUNNING, UNAVAILABLE,
    FAILED and any unknown token give the panel.
  - **When there is no producer token,** no status arrived. On the network plane that means the explicit
    unknown, so the panel. On the view-fixture plane the fixture's own view state is honoured, except
    UNCERTAIN (row W1-S55).
  - **`businessDateOf(report)`** reads the status's `business_date`. It falls back to the view
    document's date only when no status arrived at all, and it says which carrier it read.
- `tabs/reporting/AnswerStatus.tsx` (NEW). This block sits at the top of every answer body and shows the
  state, the reason, and the business date.
  - PARTIAL, NEEDS-CORRECTION and UNCERTAIN get an amber band reading *"Qualified answer -- not a complete
    report"*.
  - READY and STALE get the neutral band.
- `tabs/reporting/ReportingTab.tsx`. The body is now gated on `isAnswerBearing(report.availability)`.
  `isCompleteState` (unchanged) now decides only the complete-vs-qualified presentation. A failed request
  now clears the report too.
- `__tests__/fe-s-5/states.test.ts`. Only the claims ruling H changes, each marked `RULING H`:
  - In the two PARTIAL tests, `summary` and `account-detail` now expect `true`, and a `qualified` marker
    assertion is added.
  - The titles, the header and the STALE comment are re-worded.
- `__tests__/fe-s-30/`: `predicate.test.ts`, `reporting-in-a-browser.test.ts`, `reporting-driver.mjs` and
  `_scenarios.ts`.

## Criteria -- deciding runs, and which way the server was

| id | invocation (as the order writes it) | deciding line | server |
|---|---|---|---|
| F30-AC1 | `bun run typecheck; echo rc=$?` | `rc=0` | n/a |
| F30-AC2 | `bun test .../fe-s-30/predicate.test.ts` | `ANSWER-BEARING PRODUCER STATES -> BODY: 5 of 5 (of 9 producer states)` | n/a |
| F30-AC3 | same | `NO-ANSWER PRODUCER STATES -> PANEL: 4 of 4 (of 9 producer states)` | n/a |
| F30-AC4 | same | `NO WIRE STATE -> PANEL, NOT A BODY: 1 of 1` | n/a |
| F30-AC5 | same | `ONE PREDICATE: Reporting reads state/availability` | n/a |
| F30-AC6 | `bun test .../fe-s-30/reporting-in-a-browser.test.ts` | `REPORTING UNDER THE GATE, IN A BROWSER: 4 of 4` | **UP** -- my own, port 5230, `IRPT_FE_DEV_PORT=5230` |
| F30-AC7 | same | `PARTIAL BODY SHOWS STATE, REASON AND business_date: yes` | **UP** -- 5230 |
| F30-AC8 | `bun test .../fe-s-3 .../fe-s-5 .../fe-s-30` | `48 pass` / `0 fail` (11 files) | **UP** (5230) deciding; also run **DOWN** (5239, closed): 46 pass / 2 skip / 0 fail, both skips named |
| F30-AC9 | judgment | RECORDED, not graded -- capture `fe-s-30_reporting_partial_qualified_1440.png` | UP (capture) |

AC2 through AC5 need no server. AC6 and AC7 pass only with it present. Both declare the precondition
through `fe-s-27/_dev-server.ts`, and both print `SKIPPED ... PRECONDITION ABSENT` when it is missing.

**Whole suite:** baseline 483 pass / 4 skip / 0 fail (84 files), after 491 / 6 / 0 (86 files). No regression.

**The discriminating date.** The PARTIAL status carries `business_date` 2026-08-24, and the page shows
`Business date 2026-08-24 (from=status)`. The document's own `actual_end` is 2026-09-09, so a body that
read the wrong field would print the wrong date.

## Controls

1. **Live mutant on the gate.** A view-only variant of `isAnswerBearing` gave
   `NO WIRE STATE ... -> BODY` and `... 0 of 1`, 5 pass / 3 fail, rc=1. The file was restored
   byte-identically (`git diff --quiet` rc=0).
2. **AC5's source read** refuses a copy of ReportingTab gated on `isCompleteState`:
   `CONTROL: ... refused: yes`.
3. **AC4's pair.** The same view state, UNCERTAIN, gives BODY for the producer's UNCERTAIN and PANEL for
   no wire state.

## Rows (INVESTIGATION_v2.md)

- **IRPT_FNTEND-W1-S55** -- OBSERVATION, INERT. The view-fixture plane carries no `producerState`, which
  forced the absent-token rule above. This is my reading of "never on the view state alone", and it is
  L9's to grade.
- **IRPT_FNTEND-W1-S56** -- OBSERVATION, ARMED, disarm `2.0.0_SA_COO~F`. The prescribed `bun run dev`
  re-optimized vite's deps cache through the junction.
- **IRPT_FNTEND-W1-S57** -- OBSERVATION, ARMED, disarm `2.0.0_SA_COO~F`. AC8's invocation sets no port, and
  the default 5181 was answering from a server I did not start. It had gone by a later bare run
  (ECONNREFUSED -> SKIPPED).

## For FE-s-31 / FE-s-32

```ts
import { isAnswerBearing, businessDateOf } from '../../state/availability'
isAnswerBearing(doc.availability)   // true -> render the body; false -> StatusPanel
businessDateOf(doc)                 // { fact, businessDate, from: 'status' | 'document' }
```
`AnswerStatus` lives in `tabs/reporting/` and takes `{ report, complete }`. It can be reused as it stands.
