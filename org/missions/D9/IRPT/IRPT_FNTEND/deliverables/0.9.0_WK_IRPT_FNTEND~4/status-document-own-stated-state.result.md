# IRPT_FNTEND.TO-FE-s-54 -- status-document-own-stated-state -- result

Worker: `0.9.0_WK_IRPT_FNTEND~4`. Worktree pair `C:/tmp/wk-irpt_fntend-9-5-fe-s-54` (workspace) +
`C:/tmp/wk-irpt_fntend-9-5-fe-s-54/portal` (portal, branch `wk-irpt_fntend-9-5-fe-s-54-portal`,
based on portal DEV `ce53801c`, which includes FE-s-53's `NO_STATUS_REASON` fix).

## First act: the trace (F54-AC2)

`git grep -n -F -e 'probeStatus(' -e 'getJobStatus(' HEAD -- src` over the whole committed portal
tree returns exactly two hits, both the methods' own declarations:

```
HEAD:src/api/endpoints/investor-reporting.ts:1120:  probeStatus(): Promise<StatusEnvelope> {
HEAD:src/api/endpoints/investor-reporting.ts:1125:  getJobStatus(jobId: OpaqueId): Promise<StatusEnvelope> {
```

Nothing else -- production or test -- calls either method by name anywhere in the committed tree.
This matches the client's own comments verbatim: `probeStatus` is "the prefix probe. Not on the
interface: no screen reads it." and `getJobStatus` is "one job's status envelope. Not on the
interface: no screen reads it yet." Every production tab body instead builds its `StatusPanel` via
`envelopeFromAvailability(<document>.availability)` from a `PerformanceReport` / `HoldingsSnapshot`
/ `AnalysisRequest` document (`tabs/TabShell.tsx:142,152,159`; `tabs/reporting/ReportingTab.tsx:158`;
`tabs/holdings/HoldingsTab.tsx:148`; `tabs/analysis/AnalysisTab.tsx:151,194`) -- never from
`probeStatus`/`getJobStatus`.

**RENDER SITES FOR status-summary/status-job: 0** (both operations).

## The gap is NOT "nothing renders it" -- it is one level up

Per the order's own instruction, this is not "nothing to fix": the order names exactly this branch
("does the render site... read something that defaults past it... a caller that wraps the result
through [an adapter] a second time") and directs grounding the fix in what the trace finds rather
than assuming `adapt.ts`.

`adaptStatusEnvelope` (`contracts/adapt.ts:536-569`) already carries `wire.state` onto the returned
`StatusEnvelope.state` correctly (`state: STATE_FOR_WIRE[wire.state]`, identity for `PARTIAL`) --
confirmed unmodified and correct by reading `STATE_FOR_WIRE` (`:356-365`).

`parseIrEnvelope` (`contracts/envelope.ts`) is the ONE parser every operation's response goes
through (via `LiveClient.send()`, `investor-reporting.ts:895-941`, which both `probeStatus` and
`getJobStatus` call). It ALWAYS re-wraps the adapted document:
`carryAvailabilityFromStatus(adapt(body.data), status)`, where `status` is the SEPARATE,
response-level `.status` member. For status-summary/status-job, `data` IS the status document --
`RESPONSE_STATUS_REQUIRED` is `false` for both, and a real response for either carries no separate
`.status` sibling -- so `status` was always `null` on this path, and
`carryAvailabilityFromStatus`'s `statedState === null` branch fired unconditionally, discarding the
document's own already-correct `availability` (built by `adaptStatusEnvelope` via `wireEnvelope`)
and replacing it with the generic "no status arrived" default: state `EXPLICIT_UNKNOWN`
(`'UNCERTAIN'`) plus `NO_STATUS_REASON` -- regardless of what the document itself stated (e.g.
`PARTIAL`). The document's own top-level `.state` field (untouched by `carryAvailabilityFromStatus`)
stayed correct, so the two disagreed.

This exact symptom was ALREADY PRINTED, but not graded, by `fe-s-47/no-status-reason.test.ts`'s
`F47-AC7`, which names this row:

```
F47-AC7   OTHER PROBLEMS (printed, not graded; row IRPT_FNTEND-W3-S38): ["StatusEnvelope[0]: state 'PARTIAL' disagrees with availability.state 'UNCERTAIN'"]
```

And `F47-AC6`'s own RULES table (`:348-350`, unedited by this cell) already names the mechanism in
its "OVERWRITTEN on every in-contract response" bucket:

> "adaptStatusEnvelope's own explicit-unknown reason (FE-s-53, row IRPT_FNTEND-W3-S37): for
> status-summary/status-job this builds `data`, and parseIrEnvelope's carryAvailabilityFromStatus
> (:219) always runs on `data` afterward with the SEPARATE `status` field, which these two
> operations leave absent -- so carryAvailabilityFromStatus's own `statedState === null` branch
> re-derives both state and partialReason regardless of what this line set, the same way
> wireEnvelope's default is overwritten above"

i.e. this was known and bucketed as (previously accepted) overwrite behavior at FE-s-53 time; round-8
analysis item 3 revisits it and this cell fixes it.

## The fix (`contracts/envelope.ts`, `parseIrEnvelope` -- NOT `adaptStatusEnvelope`)

For status-summary/status-job specifically, when no separate `status` arrived, the freshly adapted
document stands in as its own `status` for the carry -- the document's own state, reason and dates
are carried onto its own availability unchanged (an identity, not a default):

```ts
const effectiveStatus =
  status ?? (IR_STATUS_DOCUMENT_OPERATIONS.includes(operation) ? (adaptedData as unknown as StatusEnvelope) : null)
const data = carryAvailabilityFromStatus(adaptedData, effectiveStatus) as T
```

`IR_STATUS_DOCUMENT_OPERATIONS = ['status-summary', 'status-job']`, the same two operations
`IR_DATA_ADAPTER` already maps onto `adaptStatusEnvelope`. Every other operation is unaffected:
`status` is non-null wherever a real response carries one, so `effectiveStatus` equals `status`
exactly as before for all ten other operations, and for status-summary/status-job whenever a
response DOES carry a genuine separate `.status` (schema-legal, if uncommon), `status` is non-null
there too and the fallback never fires.

## F54-AC3 -- GREEN (this fix in place)

```
F54-AC3 status-summary PARTIAL: data.state=PARTIAL data.availability.state=PARTIAL data.availability.publicReasonCode="SOURCE_PARTITION_INCOMPLETE"
F54-AC3 status-summary PARTIAL rendered through envelopeFromAvailability: state=PARTIAL
F54-AC3 status-job PARTIAL: data.state=PARTIAL data.availability.state=PARTIAL data.availability.publicReasonCode="SOURCE_PARTITION_INCOMPLETE"
F54-AC3 status-job PARTIAL rendered through envelopeFromAvailability: state=PARTIAL
F54-AC3 CONTROL status-summary UNCERTAIN, no reason: data.state=UNCERTAIN data.availability.state=UNCERTAIN data.availability.partialReason="The response carried no status stating its state, so its state is unknown."
A status-summary RESPONSE STATING PARTIAL RENDERS PARTIAL, NOT A DEFAULT: yes
```

The control (a genuinely `UNCERTAIN`, reasonless response) is unchanged: still `UNCERTAIN` plus
FE-s-53's `NO_STATUS_REASON` -- the fix is additive (a stated state wins) and never masks a genuine
unknown.

## F54-AC4/AC5 -- the two-test breakage in `fe-s-47/no-status-reason.test.ts` (row IRPT_FNTEND-W4-S77)

`fe-s-47/no-status-reason.test.ts` is NOT in this order's `<paths>`. Its `F47-AC6` and `F47-AC7`
both hard-code the PRE-fix behavior as their expectation (a uniform "every status-optional
operation defaults to `UNCERTAIN` with no status" assumption that this cell's whole point falsifies
for status-summary/status-job):

```
$ cd portal && bun test src/pages/InvestorReporting/__tests__/fe-s-14 src/pages/InvestorReporting/__tests__/fe-s-47
...
F47-AC6 REACH status-summary, no status: state PARTIAL, partialReason null (expected NO_STATUS_REASON) -> MISSING
F47-AC6 REACH status-job, no status: state PARTIAL, partialReason null (expected NO_STATUS_REASON) -> MISSING
...
F47-AC6 SUBTRACTION: 33 sites - 32 subtracted - 0 unclassified = 1 kept
expect(carries).toBe(arms) -- Expected: 18, Received: 16
...
F47-AC7 status-summary (StatusEnvelope): ... control, every reason stripped, refused: no
F47-AC7 status-job (StatusEnvelope): ... control, every reason stripped, refused: no
F47-AC7 POPULATION: 11 status-optional - 2 without an availability = 9; control refused when stripped: 7 of 9
expect(controlRefused).toBe(population) -- Expected: 9, Received: 7

26 pass
2 fail
77 expect() calls
Ran 28 tests across 6 files.
```

Before this cell's edit, the same invocation read `28 pass, 0 fail` (this session's first
measurement, before `contracts/envelope.ts` was touched). Both new failures are the DIRECT, PREDICTED
consequence of correctly implementing FE-s-54 -- the same class as the already-filed
`IRPT_FNTEND-W4-S22` (FE-s-53 breaking `F47-AC6`'s classification one level down), one cell later,
on the same out-of-grant file. Filed as `IRPT_FNTEND-W4-S77`.

`F54-AC5` (whole suite) reads 3 fail: these same 2, plus 1 pre-existing, unrelated,
`fe-s-45/residuals.test.ts` `F45-AC9` failure -- confirmed unrelated: it passes 6/6 standalone
(31.89s) and imports only `node:child_process`/`node:fs`/`node:process`/`node:url`, nothing from
`contracts/`; it matches the already-filed load/port-sensitivity pattern
(`IRPT_FNTEND-W1-S67`/`W1-S69`).

## Disposition

`F54-AC1` PASS (typecheck rc=0). `F54-AC2` PASS (denominator 0, printed). `F54-AC3` PASS (GREEN,
printed, control included). `F54-AC4` and `F54-AC5` FAIL by their own printed bar -- honestly
reported, not forced -- because of `IRPT_FNTEND-W4-S77`, filed and out of this order's `<paths>` to
resolve. `F54-AC6` (judgment) RECORDED, no verdict: the trace is real (2 hits total in the committed
tree, both declarations, confirmed by `git grep`; every production render path traced and named by
file:line), and the fix is grounded in exactly what the trace found (`contracts/envelope.ts`'s
`parseIrEnvelope`), not a guess at `adapt.ts` (which was already correct and is untouched).
`<status>` is left `pending` for the COO to resolve at drain (e.g. by widening `<paths>` to
`fe-s-47/no-status-reason.test.ts` for the two now-stale assertions, the same remedy AMENDMENT 1
used for FE-s-53's `IRPT_FNTEND-W4-S22`).
