# IRPT_FNTEND.TO-FE-s-53 -- status-envelope-no-state-reason -- result

Worker: `0.9.0_WK_IRPT_FNTEND~4`. Worktree pair `C:/tmp/wk-irpt_fntend-9-4-fe-s-53` (workspace)
+ `C:/tmp/wk-irpt_fntend-9-4-fe-s-53/portal` (portal, branch `wk-irpt_fntend-9-4-fe-s-53-portal`,
based on portal DEV `be8cf21874`). Portal fix + test committed at `a26d791a` (LOCAL; PORTAL IS
FROZEN).

## The gap, grounded

`contracts/adapt.ts` read at portal `be8cf21874` (the pin the task order names):
- `NO_STATUS_REASON` (`:176`) already declared.
- `carryAvailabilityFromStatus` (`:291-320`) already applies FE-s-47's rule when CARRYING a
  `StatusEnvelope`'s state onto ANOTHER document (`:307`).
- `adaptStatusEnvelope` (`:536-569`) -- the function that builds the StatusEnvelope document
  ITSELF for status-summary/status-job -- calls `wireEnvelope({...})` WITHOUT ever passing
  `partialReason`, so `wireEnvelope`'s generic default (`:239`, `parts.partialReason ?? null`)
  fires unconditionally.
- `StatusEnvelopeWire` (`contracts/wire/StatusEnvelope.ts:12-32`): `state` is required, one of
  nine literals including `'UNCERTAIN'` (the wire's own "states no state" token -- `STATE_FOR_WIRE`
  maps it onto the view's `EXPLICIT_UNKNOWN_STATE`, itself `'UNCERTAIN'`). `public_reason_code`
  (`:29`) is required and typed `string`, with no separate "document reason" field.

## RED (before the fix, portal `be8cf21874`)

Test file written first (`__tests__/fe-s-53/no-status-reason.test.ts`), then run against the
UNMODIFIED `adaptStatusEnvelope`:

```
$ cd portal && bun test src/pages/InvestorReporting/__tests__/fe-s-53/no-status-reason.test.ts
F53-AC2/1 availability: {"state":"UNCERTAIN","sourceAsOf":"2026-09-18T12:00:00Z","partialReason":null,"publicReasonCode":null,"sourceDate":{"fact":"PRESENT","businessAsOf":"2026-09-18"}}
F53-AC2/1 validate problems: ["StatusEnvelope.availability: state 'UNCERTAIN' carries NEITHER partialReason NOR publicReasonCode"]
STATE UNCERTAIN, NO REASON -> NO_STATUS_REASON, VALID: no
 (F53-AC2/1 FAILED: expect(ok).toBe(true), Expected: true, Received: false)

F53-AC2/2 availability: {"state":"UNCERTAIN","sourceAsOf":"2026-09-18T12:00:00Z","partialReason":null,"publicReasonCode":"PRODUCER_STATED_CODE","sourceDate":{"fact":"PRESENT","businessAsOf":"2026-09-18"}}
STATE UNCERTAIN, HAS REASON -> KEPT (never NO_STATUS_REASON): no
 (F53-AC2/2 FAILED: expect(ok).toBe(true), Expected: true, Received: false)

F53-AC2/3 availability: {"state":"PARTIAL","sourceAsOf":"2026-09-18T12:00:00Z","partialReason":null,"publicReasonCode":"SOURCE_PARTITION_INCOMPLETE","sourceDate":{"fact":"PRESENT","businessAsOf":"2026-09-18"}}
STATED STATE (PARTIAL) UNCHANGED: yes
 (F53-AC2/3 PASSED -- the control, unaffected either way)

RED-THEN-GREEN: gap NOT closed (gapClosed=false, ownKept=false, statedUnaffected=true)
 (F53-AC2 summary FAILED)

1 pass
3 fail
4 expect() calls
Ran 4 tests across 1 file. [59.00ms]
```

This confirms the reading exactly: state `UNCERTAIN` + no `public_reason_code` produces a
StatusEnvelope refused by `validate.ts`'s own `checkAvailability` (the SAME bar F47-AC4/AC7 use
elsewhere in this file), and a stated reason under `UNCERTAIN` is silently dropped (never carried
into `partialReason`). Per BOUNDS, this is the gap as described -- proceeding to the fix.

## The fix

`adaptStatusEnvelope`'s `wireEnvelope(...)` call now also passes:

```ts
partialReason: wire.state === 'UNCERTAIN' ? (reason ?? NO_STATUS_REASON) : null,
```

mirroring `carryAvailabilityFromStatus`'s own
`statedState === null ? (current.partialReason ?? NO_STATUS_REASON) : current.partialReason`
(`:307`): `reason` (`wire.public_reason_code`, already read at `:545`) is the document's own and
always kept first (amendment 1, msg 96947); the constant fills only where the wire states none.
A stated (non-`UNCERTAIN`) state is untouched -- no change to that path. Nothing else in
`adapt.ts` was touched (`carryAvailabilityFromStatus`, `wireEnvelope` and every other adapter are
byte-identical to `be8cf21874`).

## GREEN (after the fix, portal `a26d791a`)

```
$ cd portal && bun test src/pages/InvestorReporting/__tests__/fe-s-53/no-status-reason.test.ts
F53-AC2/1 availability: {"state":"UNCERTAIN","sourceAsOf":"2026-09-18T12:00:00Z","partialReason":"The response carried no status stating its state, so its state is unknown.","publicReasonCode":null,"sourceDate":{"fact":"PRESENT","businessAsOf":"2026-09-18"}}
F53-AC2/1 validate problems: []
STATE UNCERTAIN, NO REASON -> NO_STATUS_REASON, VALID: yes
F53-AC2/2 availability: {"state":"UNCERTAIN","sourceAsOf":"2026-09-18T12:00:00Z","partialReason":"PRODUCER_STATED_CODE","publicReasonCode":"PRODUCER_STATED_CODE","sourceDate":{"fact":"PRESENT","businessAsOf":"2026-09-18"}}
STATE UNCERTAIN, HAS REASON -> KEPT (never NO_STATUS_REASON): yes
F53-AC2/3 availability: {"state":"PARTIAL","sourceAsOf":"2026-09-18T12:00:00Z","partialReason":null,"publicReasonCode":"SOURCE_PARTITION_INCOMPLETE","sourceDate":{"fact":"PRESENT","businessAsOf":"2026-09-18"}}
STATED STATE (PARTIAL) UNCHANGED: yes
RED-THEN-GREEN: gap confirmed then closed

4 pass
0 fail
4 expect() calls
Ran 4 tests across 1 file. [83.00ms]
rc=0
```

## F53-AC1 (typecheck)

```
$ cd portal && bun run typecheck; echo rc=$?
$ tsc -b --noEmit
rc=0
```
PASS.

## F53-AC3 -- FAIL, caused by this cell's own fix, outside grant to remedy

```
$ cd portal && bun test src/pages/InvestorReporting/__tests__/fe-s-14 src/pages/InvestorReporting/__tests__/fe-s-47
27 pass
1 fail
75 expect() calls
Ran 28 tests across 6 files. [865.00ms-1196.00ms across runs]
```
The one failure: `FE-s-47 ... > F47-AC6 -- the reach, by subtraction over the committed tree`.
F47-AC6 runs `git grep -n -E "EXPLICIT_UNKNOWN_STATE|'UNCERTAIN'|\"UNCERTAIN\"" HEAD` over the
COMMITTED portal tree and classifies every hit against a hardcoded per-line RULES table. This
cell's fix adds exactly one new, correct hit outside `__tests__/` --
`contracts/adapt.ts:566: partialReason: wire.state === 'UNCERTAIN' ? (reason ?? NO_STATUS_REASON) : null,`
-- which no RULES entry classifies, so it prints `UNCLASSIFIED` and `breaks` goes from 0 to 1:
`expect(breaks).toBe(0)` receives 1. Filed as `IRPT_FNTEND-W4-S22` (BLOCKING/INERT). `adapt.ts`'s
bound is `adaptStatusEnvelope` only; `__tests__/fe-s-47/` is not in this order's `<paths>`, so the
RULES table cannot be amended here. Considered and rejected: rewriting the check with dot access
(`wire.state === STATE_FOR_WIRE.UNCERTAIN`) would dodge the grep pattern without changing
behaviour, but that defeats the census's purpose (forcing acknowledgment of a new explicit-unknown
site) rather than fixing anything, so the natural, readable form was kept and the true conflict is
reported instead.

## F53-AC4 -- FAIL, a DIFFERENT and PRE-EXISTING condition, outside grant to remedy

```
$ cd portal && bun test src/pages/InvestorReporting
589 pass
21 skip
2 fail
2497 expect() calls
Ran 612 tests across 107 files. [75.75s]
rc=1
```
Two failures, both outside `<paths>`:
1. `FE-s-47 ... > F47-AC6` -- the same finding as F53-AC3 above (`IRPT_FNTEND-W4-S22`).
2. `FE-s-49 ... > F49-AC8 -- the three gate hunks are byte-identical to 2.0.0_SA_COO~D's c29a8b86`
   -- PRE-EXISTING at `be8cf21874` (confirmed: `git status --porcelain -- src/App.tsx
   src/pages/InvestorReporting/__tests__/fe-s-49` is empty in this worktree; the test reads
   committed git blobs only). Filed as `IRPT_FNTEND-W4-S21` (BLOCKING/INERT); already adjacent to
   the tracked, held-from-drain state of this same file (`IRPT_FNTEND-S67`), a different symptom.

## F53-AC5 (judgment -- recorded, no verdict)

Material for the grader: the gap was grounded by reading `contracts/adapt.ts` at `be8cf21874`
(`NO_STATUS_REASON` `:176`, `carryAvailabilityFromStatus` `:291-320`/`:307`, `adaptStatusEnvelope`
`:536-569`) and `contracts/wire/StatusEnvelope.ts` (`:12-32`, confirming `public_reason_code` is
required/non-nullable with no separate document-reason field), then confirmed with a RED test
before any edit. The fix is a single added `partialReason` line inside `adaptStatusEnvelope`
(`:566` in the post-fix file), touching no other adapter, mirroring `carryAvailabilityFromStatus`'s
existing rule exactly with the wire's own equivalent condition (`wire.state === 'UNCERTAIN'`
in place of `statedState === null`). `git show a26d791a -- src/pages/InvestorReporting/contracts/adapt.ts`
shows this as the ONLY hunk in the file.

## Surprises filed

- `IRPT_FNTEND-W4-S21` (BLOCKING/INERT): F53-AC4's whole-suite "0 fail" cannot pass due to a
  pre-existing `fe-s-49/admin-gate.test.ts` F49-AC8 failure, unrelated to and outside this cell's
  grant.
- `IRPT_FNTEND-W4-S22` (BLOCKING/INERT): F53-AC3's "0 fail" over fe-s-14+fe-s-47 cannot pass
  because this cell's required fix adds a new, correct site that fe-s-47's F47-AC6 census (owned
  outside this grant) does not yet classify.

## Status

`<status>` stays `pending`: F53-AC1 and F53-AC2 PASS, F53-AC3 and F53-AC4 FAIL by measured output
(both for reasons outside this order's `<paths>` grant), F53-AC5 RECORDED with no verdict.
