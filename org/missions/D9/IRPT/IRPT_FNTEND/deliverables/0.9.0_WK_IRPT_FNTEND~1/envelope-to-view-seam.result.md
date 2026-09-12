# FE-s-19 -- the envelope-to-view seam: the state the wire sends is the state the view gets

**Task order:** `IRPT_FNTEND.TO-FE-s-19` · **Worker:** `0.9.0_WK_IRPT_FNTEND~1`, slot ~1
**Workspace branch:** `wk-irpt_fntend-3-1-fe-s-19` (cut from CLOUD @9762d5b8a3) · **Portal branch:** `wk-irpt_fntend-3-1-fe-s-19` (cut from DEV @f0443ba8)
**Push state:** LOCAL in both repos. Portal is frozen by Andrew-direct; nothing was pushed, merged, rebased or checked out.

**ORDER STATUS: NOT COMPLETE.** Nine of the ten criteria pass by output; `F19-AC9` is a judgment
criterion recorded without a verdict; **`F19-AC8` FAILS** and is carried as `IRPT_FNTEND-W1-S38`.
The `<status>` is NOT flipped. Section 6 states the failure and its measurement.

---

## 1. PRODUCER VINTAGE (data, not a pin)

`docs/contracts/investor-reporting/v1/` is at **`58e387b4542cb8ce7c7c6a5bb4ebcb30980464c6`** in this
worktree -- `git log -1 --date=iso -- docs/contracts/investor-reporting/v1/` reads
`2026-09-11 22:57:36 -0400`, subject *"fix(StatusEnvelope schema): the source_pin declared provenance
at a commit where the rule does not exist"*.

Recorded as data, per the order's BOUNDS. **No byte or sha pin on that directory was added anywhere
in this cell's work**, and the one place a vintage appears in the code (`_wire.ts`'s comment) states
the commit as prose beside a value that is READ AT RUN TIME from the schema, never compared to a
recorded digest. The nine wire states this cell grades are read out of
`StatusEnvelope.schema.json`'s own `state.enum` at test time, so a producer that adds a tenth state
changes the denominator this suite prints rather than breaking a pin.

## 2. THE DESIGN DECISION, AND WHY

> *The cell: "What should the view's state derive from once the envelope carries it -- does
> `availability` remain the carrier and get filled from the envelope, or does the envelope's state
> reach `TabShell` directly and `availability` keep only its source timestamps?"*

**DECIDED: `availability` REMAINS THE CARRIER, and the seam fills it from the envelope's `status`
inside `parseIrEnvelope` -- one place, every operation, every consumer of the parser.**
The code is `carryAvailabilityFromStatus` in `contracts/adapt.ts`, applied at
`contracts/envelope.ts`'s single `adapt(body.data)` call site.

Three measurements decided it, and none of them is a preference:

1. **`Availability.state` is the ratified view contract's declared home for a state.** All ten view
   contracts carry a `ContractEnvelope`; `envelopeFromAvailability` (`state/status.ts:153`) is the
   ONE bridge from it to what a panel renders; `comp-find envelopeFromAvailability` over the portal
   returns 34 hits / 305 files with DEF=3. Moving the carrier renames a ratified member and rewrites
   every consumer without changing the contract.

2. **No document schema carries a state, so there is nothing to lose and something to gain.**
   At producer vintage `58e387b454`, `PerformanceReport.schema.json` has five top-level members
   (`lineage`, `dates`, `measurement_basis`, `returns`, `optional_facts`) and
   `HoldingsSnapshot.schema.json` has six (`scope`, `source_set_revision`, `clocks`,
   `custody_totals`, `nodes`, `coverage`). Neither set contains a state. `availability.state` on the
   network path was therefore ALWAYS `EXPLICIT_UNKNOWN_STATE`; filling it from the envelope
   overwrites nothing a producer ever said.

3. **The alternative is not merely different, it is wrong here.** `TabShell` issues its OWN bootstrap
   requests (`TabShell.tsx:141-160`) while `ReportingTab` and `HoldingsTab` each fetch independently
   (`ReportingTab.tsx:144`, `HoldingsTab.tsx:75`). A state routed to the shell would belong to a
   DIFFERENT response than the document rendered beside it -- a tab would show a state for a payload
   it is not displaying. That is a worse defect than the one being repaired, and it is invisible
   because both values are real.

**What the seam may do, and what it must not.** `adapt.ts`'s standing rule is RENAME / RESTRUCTURE /
CARRY, and *"never compute, never default, never infer"*. The seam carries:

| member | rule | why it is a carry and not a derivation |
|---|---|---|
| `state` | REPLACED by `status?.state ?? EXPLICIT_UNKNOWN_STATE` | the document never carried one (measurement 2); the wire's state, through the contract's own declared closed-vocabulary rename, or the explicit unknown |
| `sourceAsOf` | `status?.sourceAsOf ?? document's own` | both sides are wire-carried values; a fallback between two things the producer said, never a computation |
| `publicReasonCode` | `status?.publicReasonCode ?? document's own` | same |
| `partialReason` | untouched | the envelope has no source for it, so it is not filled from one |

**AND THE ABSENT CASE IS THE POINT.** `envelope.ts:193` read `state: status?.state ?? 'READY'`
before this cell. That is the browser deriving a state the wire did not send -- and it is not an edge
case: `status_required` is **false** on ten of the twelve response contracts, so the defaulting
branch was the COMMON one. It now yields `EXPLICIT_UNKNOWN_STATE`. A response that says nothing about
its state renders as Uncertain, never as success. `F19-AC5` is the arm that holds this open, and
without it `F19-AC4` could not tell a carry from a default.

**Second decision, smaller: a refusal is a state.** `EnvelopeMismatch` now carries a PUBLIC reason
code naming the envelope member that gave way (`ENVELOPE_CONTRACT_VERSION`, `ENVELOPE_FIRM_ID`, ...)
-- a field name, never the refused value, which is `envelope.ts`'s own standing rule. `state/status.ts`
gains `envelopeFromRefusal`, the one rule that turns such a code into a `TabEnvelope` (UNAVAILABLE
carrying the code), and `TabShell.tsx`'s three `.catch` arms consume it. Before this, a response the
CONTRACT refused and a request that never completed produced the identical panel -- FAILED, reason
`IR-REQUEST-FAILED`, offering a Retry for a condition retrying cannot change.

## 3. WHAT CHANGED

**portal** (branch `wk-irpt_fntend-3-1-fe-s-19`, local):

| file | change |
|---|---|
| `src/pages/InvestorReporting/contracts/adapt.ts` | `+ carryAvailabilityFromStatus` -- the seam |
| `src/pages/InvestorReporting/contracts/envelope.ts` | the seam applied at the one adapter call site; `state` no longer defaults to READY; `+ envelopeReasonCode`; `EnvelopeMismatch.publicReasonCode` |
| `src/pages/InvestorReporting/state/status.ts` | `+ envelopeFromRefusal`, `+ RefusalLike` |
| `src/pages/InvestorReporting/tabs/TabShell.tsx` | the three `.catch` arms consume `envelopeFromRefusal` |
| `src/pages/InvestorReporting/__tests__/fe-s-19/` | new: `_wire.ts`, `network-state.test.ts`, `mounted-from-wire.test.ts`, `browser-driver.mjs`, `pre-envelope.test.ts`, `ambient-shims.d.ts` |

`src/api/endpoints/investor-reporting.ts` is in the grant and was **not** edited: the cell names
`:932` (`return parsed.data`) as the drop site, and it is -- but the repair belongs one level up, in
the ONE parser, where every consumer gets it rather than one method of one client.

**workspace**: this file, the proof-of-spec instance beside it, and three rows on
`INVESTIGATION_v2.md`.

## 4. THE NEGATIVE-CONTROL LEDGER (`F19-AC9`)

Each of the three new test files was written, RUN AGAINST THE UNMODIFIED BYTES, and its failure
recorded, BEFORE any source file was touched. Raw captures: `.scratch/red1.txt`, `red2.txt`,
`red3.txt`, `green1.txt`, `green2.txt`, `green3.txt` (scratch, not committed).

### PRE-FIX RED -- `network-state.test.ts`

`cd portal && timeout 120 bun test src/pages/InvestorReporting/__tests__/fe-s-19/network-state.test.ts` -- **rc=1**

```
PRODUCER ENUM (StatusEnvelope.schema.json): QUEUED, RUNNING, READY, PARTIAL, STALE, UNAVAILABLE, NEEDS_CORRECTION, UNCERTAIN, FAILED
  SENT QUEUED             -> reporting UNCERTAIN        holdings UNCERTAIN        expected LOADING  DROPPED
  SENT RUNNING            -> reporting UNCERTAIN        holdings UNCERTAIN        expected LOADING  DROPPED
  SENT READY              -> reporting UNCERTAIN        holdings UNCERTAIN        expected READY  DROPPED
  SENT PARTIAL            -> reporting UNCERTAIN        holdings UNCERTAIN        expected PARTIAL  DROPPED
  SENT STALE              -> reporting UNCERTAIN        holdings UNCERTAIN        expected STALE  DROPPED
  SENT UNAVAILABLE        -> reporting UNCERTAIN        holdings UNCERTAIN        expected UNAVAILABLE  DROPPED
  SENT NEEDS_CORRECTION   -> reporting UNCERTAIN        holdings UNCERTAIN        expected NEEDS-CORRECTION  DROPPED
  SENT UNCERTAIN          -> reporting UNCERTAIN        holdings UNCERTAIN        expected UNCERTAIN  CARRIED
  SENT FAILED             -> reporting UNCERTAIN        holdings UNCERTAIN        expected FAILED  DROPPED
NETWORK STATES CARRIED: 1 of 9
 0 pass / 1 fail (F19-AC2) ; F19-AC3's arm passed (it grades this folder's own files, not the fix)
```

Note the ONE that "carried": `UNCERTAIN` matched only because the explicit unknown happens to equal
the state that was sent. The column that makes that readable -- sent beside received -- is why the
test prints both.

**AFTER:** rc=0, `NETWORK STATES CARRIED: 9 of 9`, every row `CARRIED`, and
`SEEDED PROPS USED: 0` with `POSITIVE CONTROL: the matcher found 1 of 4 in a seeded line (initialReport)`.

### PRE-FIX RED -- `mounted-from-wire.test.ts`

`cd portal && timeout 120 bun test src/pages/InvestorReporting/__tests__/fe-s-19/mounted-from-wire.test.ts` -- **rc=1**, 16.6s

```
SCENARIO ready TAB reporting SLOT status-panel STATE UNCERTAIN
  slots(reporting): ... reporting-tab, period-controls, ..., status-panel@UNCERTAIN, safe-actions
SCENARIO ready TAB holdings SLOT status-panel STATE UNCERTAIN
  slots(holdings): control, control, tabs, tab-shell, status-panel@UNCERTAIN, safe-actions
  served(ready): .../directory/resolve, .../holdings/, .../performance/
PAGE CRASHES: 0 ; DRIVER EXIT: 0
BODIES MOUNTED: 0 of 2
UNCERTAIN WITHOUT A WIRE STATE: 2 of 2
 1 pass / 1 fail (F19-AC4)
```

**The driver exited 0 and the page did not crash** -- the browser rendered the app correctly and the
app rendered the status panel. That is the discriminating shape: a broken instrument and a broken
product do not look alike here.

`F19-AC5` passing in this run is **VACUOUS and is recorded as such**: at the pre-fix bytes every
input rendered UNCERTAIN, so the arm could not have failed. It becomes a real discriminator only once
`F19-AC4` passes beside it, which is the whole reason the two ship in one file.

**AFTER:** rc=0, `BODIES MOUNTED: 2 of 2` -- `slot=reporting-body` and `slot=holdings-tab`, the
Holdings slot list carrying `holdings-summary, holdings-current-value, holdings-account-count,
holdings-source-dates, holdings-model-coverage, holdings-drill-tree, holdings-breadcrumbs,
holdings-donut, slice-table` -- and `UNCERTAIN WITHOUT A WIRE STATE: 2 of 2` still holding.

### PRE-FIX RED -- `pre-envelope.test.ts`

`cd portal && timeout 120 bun test src/pages/InvestorReporting/__tests__/fe-s-19/pre-envelope.test.ts` -- **rc=1**

```
# Unhandled error between tests
SyntaxError: Export named 'envelopeFromRefusal' not found in module
  'C:\tmp\wk-irpt_fntend-3-1-fe-s-19\portal\src\pages\InvestorReporting\state\status.ts'.
 0 pass / 1 fail / 1 error
```

The red is the defect stated exactly: at these bytes **a refusal has no state representation at all**
-- there is no rule that turns a contract refusal into something a panel can render, which is the
second half of what `F19-AC6` asks for.

**AFTER:** rc=0.

```
  MISSING contract_version  -> rejected=true  reason=ENVELOPE_CONTRACT_VERSION    state=UNAVAILABLE
  MISSING operation         -> rejected=true  reason=ENVELOPE_OPERATION           state=UNAVAILABLE
  MISSING firm_id           -> rejected=true  reason=ENVELOPE_FIRM_ID             state=UNAVAILABLE
CONTROL: a whole v1 envelope on the same path -> ACCEPTED (availability.state=READY)
PRE-ENVELOPE BODIES REFUSED: 3 of 3
```

## 5. WHY THE MOUNTING CRITERIA ARE GRADED IN A BROWSER

`F19-AC4` and `F19-AC5` are the only two criteria in this order that cannot be answered by a
DOM-free renderer, and the reason is mechanical rather than stylistic.

- This portal installs **no DOM test environment**. Measured, not assumed:
  `comp-find 'happy-dom|jsdom|GlobalRegistrator|react-test-renderer' portal/src` = **2 hits across
  741 files**, and both are comments saying so (`__tests__/fe-s-16/mounted-states.test.ts:11`,
  `export/ExportModal.tsx:20`). `bun install` is forbidden by this order.
- React runs **no effect** under `renderToStaticMarkup`, and both tab bodies fetch in a `useEffect`.
- Therefore, in that instrument, a tab body can show content ONLY if the test hands it the resolved
  value through one of the four test-only seed props -- which is exactly what this order's first
  binding clause forbids, and exactly how round 2 ran 420 green tests over a defect that made both
  bodies unmountable from any response.

So a "the body MOUNTED" criterion is, in this estate, a browser criterion or it is a seeded test in
different clothes. `browser-driver.mjs` drives Edge through `playwright-core` against the vite dev
server on **5181**, fulfilling every scoped route from a v1 envelope at the NETWORK layer -- the same
interception mechanism and the same auth stub `scripts/ui-smoke.mjs` uses. The app builds its own
`LiveClient`, issues its own requests and gets bytes back; the transport is stubbed, the component is
not.

**One instrument trap, recorded because it cost a run:** `chromium.launch` **under bun** fails on this
box -- the browser's network service crashes and the launch times out (`rc=124` at 180 s,
`GPU process exited unexpectedly: exit_code=-1073741819`). Under **node** the identical launch returns
in seconds. The bun test therefore spawns the driver under node and grades its stdout.

**One builder, two instruments:** `_wire.ts` builds every body in this folder, and both the stubbed
transport (`F19-AC2`) and the browser (`F19-AC4`/`AC5`) are served from it. The documents are the
committed `fixtures/smoke/fe-s-18-frozen.json` payloads, unmodified; the only thing this folder adds
is the `status` member those maps do not carry.

## 6. `F19-AC8` FAILS -- the measurement

`cd portal && timeout 180 bun test src/pages/InvestorReporting` -- **rc=1**

| | pass | skip | fail | tests | files |
|---|---|---|---|---|---|
| at the cut (before any change) | 419 | 1 | **2** | 422 | 69 |
| after this cell | 424 | 1 | **2** | 427 | 72 |

The two failures are the SAME two, by name:
`producer fixtures > the generated wire types were generated from THESE schemas` (the stale
StatusEnvelope pin -- FE-s-20's, rows S33/S35) and
`F18-AC3 ... UNIQUE HASHES -- no two entries share a hash`. **Nothing this cell touched moved either,
and nothing it touched broke anything**: +5 pass is precisely this order's three new files.

The order's contingency covers the one-failure case ("*if this criterion still reads a stale-pin
failure AND NOTHING ELSE*"). Two failures remain, so the criterion **FAILS** and the order stays open.
Row **`IRPT_FNTEND-W1-S38`** carries it, with two findings the order could not have known:

1. **F18-AC3 cannot clear from a source change.** It grades ELEVEN COMMITTED PNG FILES against a
   committed manifest (`manifest.test.ts:57` reads `captures.manifest.json` from this deliverables
   folder). Re-derived this turn: 11 entries, 9 distinct hashes, one colliding set --
   `fe-s-18_holdings_{observed,target,missing_attribution}_390.png`, all three sha256
   `8ce52e6ad0b60e29...`, all matching their manifest value; the folder's last commit is
   `544392594e`, 2026-09-12T01:21-0400, i.e. taken before this cell existed. Images do not re-render
   because the code that made them changed. Re-taking them is FE-s-18's cell, `__tests__/fe-s-18/` is
   not in this order's `<paths>`, and the round-3 issuance carries FE-s-18 untouched -- so it is
   refused here rather than performed.

2. **A re-take would still collide, and this is the finding worth keeping.** A census of every
   committed map under `fixtures/smoke/`: **62 v1 envelopes across 16 maps; 3 carry a `status`
   member, 59 do not** -- including all three FE-s-18 Holdings maps (`envelopes=9 with_status=0`
   each). `status` is the only wire carrier of a state on this plane (measurement 2 in section 2), so
   under the now-correct bytes those three maps render three identical status panels **by the
   contract**, not by a defect. The variable is proven by this cell's own browser runs: same
   documents, same route keys, same browser -- `status` present with a state, both bodies mount;
   `status` present without one, both render `status-panel@UNCERTAIN`.

The response contract's own words say the producer should be sending one:
`responses/performance-report.response.schema.json`, `status` -- *"PRESENT ON A SUCCESS TOO, not only
a failure"* -- while `x-response-contract.status_required` is `false`. The fixtures followed the flag,
not the sentence.

## 7. WHAT THIS CELL REFUSED

- **`W2-S11` is only partly closed, and the remainder is refused with its measurement** (row
  `IRPT_FNTEND-W1-S39`). `F19-AC6`'s three bodies each carry two of the three envelope identifiers,
  so `isEnvelopeShaped` already admitted them and they were already refused; this cell added the
  NAMED reason and the state, exactly as the criterion words it. The clause's own case -- a body
  carrying NONE of the three -- is still accepted on the pre-envelope plane, because closing it reds
  at least three tests in two suites outside this grant (`__tests__/fe-s-1/adapter.test.ts:91`,
  `:276`; `__tests__/fe-s-13/no-route.test.ts:134`, each driving `LiveClient` with `{}`), which would
  take `F19-AC8` further from `0 fail`, not closer. The carry stays READABLE rather than invisible:
  `LiveClient.preEnvelopeResponses` counts it and `pre-envelope.test.ts` prints that the bypass is
  open -- deliberately WITHOUT asserting the counter, which would have locked the defect in as
  expected behaviour.
- **The cell's line citation for the gate is wrong and is rowed, not silently corrected** (row
  `IRPT_FNTEND-W1-S37`). `TabShell.tsx:133/:148/:150` do not gate the bodies; the gates are
  `ReportingTab.tsx:149`+`:175` and `HoldingsTab.tsx:79`+`:88`, in two files this order may not
  write. The diagnosis was right everywhere else and the ordered fix site was sufficient.

## 8. CRITERIA

| id | verdict | deciding output |
|---|---|---|
| F19-AC1 | PASS | `rc=0` (`tsc -b --noEmit`) |
| F19-AC2 | PASS | `NETWORK STATES CARRIED: 9 of 9` |
| F19-AC3 | PASS | `SEEDED PROPS USED: 0` (4 tokens printed, 6 files scanned, control 1 of 4) |
| F19-AC4 | PASS | `BODIES MOUNTED: 2 of 2` |
| F19-AC5 | PASS | `UNCERTAIN WITHOUT A WIRE STATE: 2 of 2` |
| F19-AC6 | PASS | `PRE-ENVELOPE BODIES REFUSED: 3 of 3` + accepting control |
| F19-AC7 | PASS | `5 pass / 0 fail`, 3 files |
| F19-AC8 | **FAIL** | `424 pass / 1 skip / 2 fail` -- the cut's own two, unmoved. Row `IRPT_FNTEND-W1-S38` |
| F19-AC9 | PASS | the invocation counts **3** (section 4: three headings, three before/after pairs). The phrase it counts appears in this file ONLY as those three headings -- naming it a fourth time here would have made the criterion fail on its own record |
| F19-AC10 | RECORDED (judgment) | section 2 is the decision and its reason; graded at L9 by `3.0.0_SA_CVO` |
