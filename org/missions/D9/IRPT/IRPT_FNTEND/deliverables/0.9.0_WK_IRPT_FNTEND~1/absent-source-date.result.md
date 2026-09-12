# IRPT_FNTEND.TO-FE-s-21 -- an absent source date is a state, not a defect

**Worker:** `0.9.0_WK_IRPT_FNTEND~1` (slot ~1, queue position 2)
**Branch:** `wk-irpt_fntend-3-5-fe-s-21` (workspace and portal), cut from CLOUD @`e4298a984e` / DEV @`baf230eb`
**Portal commit:** `dad347ae` -- LOCAL. Portal is frozen: no push, no merge, no rebase.
**Order status:** left `pending`. **F21-AC7 is REFUSED** and a FAIL row leaves the order open.

---

## THE RESULT IN ONE PARAGRAPH

Seven of eight criteria pass by output; `F21-AC8` is a judgment criterion and carries a record with no
verdict; `F21-AC7` is **refused with its measurement** because the suite reads 1 fail against a bar of
0 fail and the failure is `F18-AC3`'s capture-hash collision -- pre-existing at my cut, self-declared
refused in its own test file, and unreachable from any path in this order's grant. Six surprise rows
were filed, `IRPT_FNTEND-W1-S41` through `W1-S46`. The proof-of-spec instance validates at rc=0.

---

## WHAT THE CELL ASKED, AND THE SHAPE OF THE ANSWER

The contract (`IRPT_BCKEND` PRD v0.14) makes `StatusEnvelope.business_date` **state-conditional**:
REQUIRED on the five answer-bearing states, permitted ABSENT -- never null -- on the four no-answer
states. Before this cell `formatSourceAge` read only the timestamp, so a QUEUED job, which by contract
has no source date to have, was reported in the same words as a READY report that had **lost** one.
One of those is a state and the other is a defect, and the panel could not tell them apart.

Measured, before and after, on the same four envelopes through the same adapter:

| wire state | OLD `formatSourceAge` | NEW `formatSourceAgeForState` |
|---|---|---|
| QUEUED | `Source time unknown` | `No source age yet` |
| RUNNING | `Source time unknown` | `No source age yet` |
| UNAVAILABLE | `Source time unknown` | `No source age yet` |
| FAILED | `Source time unknown` | `No source age yet` |
| READY *(business_date absent -- a violation)* | `Source time unknown` | `Source time unknown` |

The last row is the control that matters: the change is **targeted, not global**, and an answer-bearing
state that genuinely lost its date still reads as the anomaly it is.

---

## CRITERIA

| id | verdict | deciding output | denominator |
|---|---|---|---|
| F21-AC1 | **PASS** | `rc=0` | 1 of 1, whole portal via `tsc -b --noEmit` |
| F21-AC2 | **PASS** | `NO-ANSWER STATES: 4 of 4` | 4 of 4, the 4 itself derived 9 minus 5 |
| F21-AC3 | **PASS** | `ANSWER-BEARING STATES: 5 of 5` | 5 of 5, five conjuncts each |
| F21-AC4 | **PASS** | `NO ERROR AFFORDANCE: 4 of 4` | 4 of 4 against 22 scanned tokens |
| F21-AC5 | **PASS** | `NULL IS NOT ABSENT: distinguished` | 3 of 3 facts -> 3 distinct strings |
| F21-AC6 | **PASS** | `CLICKED: Reporting` | 1 of 1 capture, 68854 bytes |
| F21-AC7 | **FAIL -- REFUSED** | `1 fail` against a bar of `0 fail` | 1 failure of 443 tests in 74 files |
| F21-AC8 | RECORDED (judgment) | see the instance; no verdict | 1 of 1 capture |

### The subtraction, printed rather than asserted

`F21-AC2`'s four are never typed out forward. The denominator is a `Record` over the producer's state
union, so it is exhaustive **by type** -- a state added to the contract fails the typecheck rather than
landing silently in one bucket -- and the four are what is left after removing the five the contract
names:

```
PRODUCER ENUM (StatusEnvelope.schema.json) -- DENOMINATOR: 9
  QUEUED, RUNNING, READY, PARTIAL, STALE, UNAVAILABLE, NEEDS_CORRECTION, UNCERTAIN, FAILED
ANSWER-BEARING (business_date REQUIRED), the contract's literal set: 5
  READY, PARTIAL, STALE, NEEDS_CORRECTION, UNCERTAIN
NO-ANSWER = 9 MINUS 5 = 4 (SUBTRACTION, not a forward list)
  QUEUED, RUNNING, UNAVAILABLE, FAILED
```

Both halves are graded. `F21-AC3` exists precisely so `No source age yet` cannot quietly become the
answer for everything, and it is the arm that would have caught a lazy implementation.

### The controls

- **Mutant:** the before/after table above -- a measured delta, not a claim.
- **Positive control** on the error scan: 7 hits (`text-red`, `role="alert"`, `data-error`, `missing`,
  `error`, `Retry`, `<button>`) on an error-dressed node, against 0 on the real slot. A scan asserting
  zero that cannot go non-zero is a constant wearing a measurement's clothes.
- **Determinism:** two consecutive runs identical on all 53 lines except the bun duration
  (`114.00ms` vs `113.00ms`). The graded age string uses an **injected** clock; no assertion in the
  file reads the wall clock.

---

## F21-AC7 -- THE REFUSAL, AND WHY IT IS NOT MINE

Bar `0 fail`; measured `441 pass / 1 skip / 1 fail` across 443 tests in 74 files, true rc=1 (captured by
redirect, not through a pipe -- a piped run reports the last command's rc). The single failure:

```
F18-AC3 -- the captures are the files the manifest claims
  > UNIQUE HASHES -- no two entries share a hash (FAILS at this commit; see the file header)
  collision set: [fe-s-18_holdings_observed_390.png,
                  fe-s-18_holdings_target_390.png,
                  fe-s-18_holdings_missing_attribution_390.png]
```

Five independent discriminators, not one assumption:

1. It fails **by name** as `F18-AC3`, not as any criterion of mine.
2. Its collision set is three FE-s-18 holdings PNGs; my capture is in neither that set nor
   `captures.manifest.json`.
3. It failed **identically on my untouched cut**, before any file in my grant existed.
4. Its own test file says so at `manifest.test.ts:143-145`: *"Row IRPT_FNTEND-W1-S33 carries the cause.
   F18-AC3 is refused."*
5. No path in this order's `<paths>` can move an already-committed PNG's bytes.

`IRPT_FNTEND-S44` predicted exactly this before I was seated. Filed as BLOCKING row
`IRPT_FNTEND-W1-S44`, which is what this criterion's own text instructs.

---

## SURPRISE ROWS -- `IRPT_FNTEND-W1-S41` .. `W1-S46`

| id | class / hazard | one line |
|---|---|---|
| W1-S41 | OBSERVATION / **ARMED** (CTO) | The order's "printed nine-state enum" is the **producer's** nine; the view has a **different** nine. QUEUED/RUNNING are not assignable to `EnvelopeState` and collapse onto LOADING. |
| W1-S42 | OBSERVATION / **ARMED** (CTO) | The contract clause governs `business_date`; the age is computed from `as_of`. Measured: a READY envelope with `business_date` present and `as_of` absent reports "Source time unknown". |
| W1-S43 | OBSERVATION / **ARMED** (CTO) | `adaptStatusEnvelope`'s `?? null` collapses ABSENT and NULL before any panel sees them. AC5's distinction survives only on the wire object. |
| W1-S44 | **BLOCKING** / INERT | F21-AC7 refused: 1 fail, F18-AC3, not mine. |
| W1-S45 | OBSERVATION / **ARMED** (COO) | **The suite's failure count is port-conditional**: 3 fail with no dev server on 5181, 1 fail with one. Same bytes, same command, nothing in the output names a port. |
| W1-S46 | OBSERVATION / **ARMED** (COO) | `formatSourceAge` has 3 consumers; the grant reaches 1. The Analysis tab still reports these states as defects. |

### The row I would read first if I were the issuer: W1-S45

My spawn prompt and `F21-AC7`'s own text both assert *"the suite at your cut reads 1 fail."* **At my cut
it read 3 fail.** The two extra failures were `F19-AC4` and `F19-AC5` -- FE-s-19's own criteria, in a cell
the issuer had just drained as complete. That is the shape that makes a worker doubt the premise it was
handed rather than the environment it was handed it in.

The cause is not a regression. `__tests__/fe-s-19/mounted-from-wire.test.ts:29-31` declares a precondition
no runner ever sees -- *"the vite dev server is up on the port below"* -- with the port hard-coded at
`const PORT = '5181'`, which is **this order's assigned `<PORT>`**. With the server down the driver exits
1 and both arms fail as though the product were broken. Measured both ways in one worktree at one commit:

```
server DOWN : 431 pass / 1 skip / 3 fail   slot=NO DRIVER LINE   BODIES MOUNTED: 0 of 2
server UP   : 441 pass / 1 skip / 1 fail   slot=reporting-body   BODIES MOUNTED: 2 of 2
```

The test author's note says *"a down server can never read as a pass here."* That is true and is not the
risk. The risk is its converse, which the note does not cover: **a down server reads as a FAIL that looks
like a code defect.** A task order naming `bun test src/pages/InvestorReporting` with a numeric fail bar
needs to name the server and the port beside it, or the bar is unfalsifiable at a glance in exactly the
way a green looks trustworthy. The hard-coded port is the second half: a worker on any other slot's port
cannot make those two tests pass at all, however correct its code.

---

## WHAT I DID NOT DO, AND WHY

Every exclusion is a path outside this order's `<paths>`. None was overridden; each is a row.

- `tabs/analysis/StageDisplay.tsx`, `tabs/analysis/VariantSelector.tsx` -- 2 of the 3 `formatSourceAge`
  consumers. The cell's sentence says *"the panels that consume it"* and the grant reaches one. This is
  why `formatSourceAge` itself is **byte-unchanged**: changing it underneath two callers I may not touch
  would regress files outside my grant. The new rule is additive. (W1-S46)
- `contracts/adapt.ts` -- would be needed to make ABSENT-vs-NULL survive into the view. (W1-S43)
- `contracts/index.ts` -- would be needed to give the view QUEUED and RUNNING. (W1-S41)
- `__tests__/fe-s-18/` and the three holdings smoke maps -- would be needed to clear F18-AC3. (W1-S44)

The denominator behind the first bullet was taken by an **unscoped** census over all of `portal/src`
(`comp-find` -- 9 hits across 750 files scanned), not by looking where I expected consumers to be.

---

## HOUSEKEEPING

- Dev server started once on 5181 from `<WS>/portal`, used for the capture and for the FE-s-19 browser
  arms, killed before this report.
- `node_modules` junction untouched; `bun install` never run.
- Scratch confined to `<WS>/.scratch/`. The two throwaway probes (`probe.test.ts`, `mutant.test.ts`) live
  there and are **not** committed; their outputs are quoted in the instance.
- Workspace records committed together: this file, the proof-of-spec instance, the capture and the
  channel rows. The task order's `<status>` is **not** flipped.
