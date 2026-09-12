# IRPT_FNTEND.TO-FE-s-21 -- an absent source date is a state, not a defect

**Worker:** `0.9.0_WK_IRPT_FNTEND~1` (slot ~1, queue position 2)
**Branch:** `wk-irpt_fntend-3-5-fe-s-21` (workspace and portal), cut from CLOUD @`e4298a984e` / DEV @`baf230eb`
**Portal commit:** `dad347ae` -- LOCAL. Portal is frozen: no push, no merge, no rebase.
**Order status:** flipped to `complete`. Every mechanical criterion passes by output; `F21-AC8` is a
judgment criterion and carries a record with no verdict.

---

## THE RESULT IN ONE PARAGRAPH

Seven of eight criteria pass by output and `F21-AC8` is graded at L9. `F21-AC7` was **refused** against
its original bar of `0 fail`, filed as BLOCKING row `W1-S44`; the issuer then corrected that bar to
`1 fail` with a name check at commit `0e25c1d422`, and the criterion was **re-measured fresh against the
corrected bar and passes**. Eight surprise rows were filed, `IRPT_FNTEND-W1-S41` through `W1-S48`. The
proof-of-spec instance validates at rc=0.

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

`formatSourceAge` itself is **byte-unchanged**. Two of its three callers are outside this order's
`<paths>` (row `W1-S46`), and changing it underneath them would regress files this cell may not touch,
so the new rule is additive.

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
| F21-AC7 | **PASS** (corrected bar) | `1 fail`, named `F18-AC3` | exactly 1 of 443 tests in 74 files |
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

## F21-AC7 -- REFUSED, THEN CORRECTED, THEN RE-MEASURED

Against the original bar of `0 fail` the measured value was 1 fail, and I refused it with its
measurement rather than working around it (BLOCKING row `W1-S44`). The issuer corrected the bar to
`1 fail` with a name check at `0e25c1d422`, because `F18-AC3` cannot clear in round 3 at all.

The amended face was read **at the commit**, never from the message's quotation and never from my own
tree, which still held the retracted bar:

```
merge-base --is-ancestor 0e25c1d422 HEAD  ->  FALSE   (readable in the object store, not carried)
git show 0e25c1d422:<order>               ->  10771 bytes
control: same command, bogus path         ->  fatal: path ... does not exist   rc=128
diff vs this branch's copy                ->  2 of 112 lines (53, 54), both inside the F21-AC7 block
                                              <status>pending</status> on both sides
```

Only those two lines were written, CRLF preserved, result verified identical to the blob modulo line
endings. Then the suite was **re-run fresh** -- not carried forward:

```
441 pass / 1 skip / 1 fail   443 tests, 74 files, true rc=1
F18-AC3 -- the captures are the files the manifest claims
  > UNIQUE HASHES -- no two entries share a hash (FAILS at this commit; see the file header)
```

The corrected bar has two conditions and both are checked separately: **exactly one** failure (1 of 443;
the marker scan over the whole run returns one line), and it **is that one** (printed by name). It is
also not mine, by five independent discriminators: it fails by name as `F18-AC3`; its collision set is
three FE-s-18 holdings PNGs my capture is not among; it failed identically on my untouched cut before
any file in my grant existed; its own test file says *"F18-AC3 is refused"* at `manifest.test.ts:143-145`;
and no path in this order's `<paths>` can move an already-committed PNG's bytes.

`W1-S44` stands unedited -- the channel is append-only -- and `W1-S47` supersedes it.

---

## SURPRISE ROWS -- `IRPT_FNTEND-W1-S41` .. `W1-S48`

| id | class / hazard | one line |
|---|---|---|
| W1-S41 | OBSERVATION / **ARMED** (CTO) | The order's "printed nine-state enum" is the **producer's** nine; the view has a **different** nine. QUEUED/RUNNING are not assignable to `EnvelopeState` and collapse onto LOADING. |
| W1-S42 | OBSERVATION / **ARMED** (CTO) | The contract clause governs `business_date`; the age is computed from `as_of`. Measured: a READY envelope with `business_date` present and `as_of` absent reports "Source time unknown". |
| W1-S43 | OBSERVATION / **ARMED** (CTO) | `adaptStatusEnvelope`'s `?? null` collapses ABSENT and NULL before any panel sees them. AC5's distinction survives only on the wire object. |
| W1-S44 | **BLOCKING** / INERT | F21-AC7 refused against the original `0 fail` bar. **Superseded by W1-S47.** |
| W1-S45 | OBSERVATION / **ARMED** (COO) | **The suite's failure count is port-conditional**: 3 fail with no dev server on 5181, 1 fail with one. Same bytes, same command, nothing in the output names a port. |
| W1-S46 | OBSERVATION / **ARMED** (COO) | `formatSourceAge` has 3 consumers; the grant reaches 1. The Analysis tab still reports these states as defects. |
| W1-S47 | OBSERVATION / INERT | The bar correction, read at the commit; F21-AC7 re-measured and passes. Supersedes W1-S44, which cannot be edited. |
| W1-S48 | OBSERVATION / **ARMED** (COO) | **My own defect, self-caught and repaired**: appending to the channel flipped the committed blob LF->CRLF, turning a 140-line append into a 3618-line whole-file rewrite. Every gate passed. |

### The two rows I would read first if I were the issuer

**`W1-S45` -- the suite's fail count is port-conditional.** My spawn prompt and `F21-AC7`'s own text both
assert *"the suite at your cut reads 1 fail."* **At my cut it read 3 fail.** The two extra failures were
`F19-AC4` and `F19-AC5` -- FE-s-19's own criteria, in a cell the issuer had just drained as complete.
That is the shape that makes a worker doubt the premise it was handed rather than the environment it was
handed it in.

The cause is not a regression. `__tests__/fe-s-19/mounted-from-wire.test.ts:29-31` declares a precondition
no runner ever sees -- *"the vite dev server is up on the port below"* -- with the port hard-coded at
`const PORT = '5181'`, which is **this order's assigned `<PORT>`**. Measured both ways in one worktree at
one commit:

```
server DOWN : 431 pass / 1 skip / 3 fail   slot=NO DRIVER LINE   BODIES MOUNTED: 0 of 2
server UP   : 441 pass / 1 skip / 1 fail   slot=reporting-body   BODIES MOUNTED: 2 of 2
```

The test author's note says *"a down server can never read as a pass here."* That is true and is not the
risk. The risk is its converse, which the note does not cover: **a down server reads as a FAIL that looks
like a code defect.** A task order naming `bun test src/pages/InvestorReporting` with a numeric fail bar
needs to name the server and the port beside it. The hard-coded port is the second half: a worker on any
other slot's port cannot make those two tests pass at all, however correct its code.

**`W1-S48` -- my own defect, stated because nobody else would have found it here.** My first channel
commit flipped the file from LF to CRLF, because on this `autocrlf=true` box the worktree copy is checked
out as CRLF while the blob is LF, and reading-then-writing it commits the checkout. The append itself was
140 lines; the diffstat read `3618 ++++----`. **Every gate passed** -- the row gate counted 6 new rows,
the corpus gate matched its baseline, the JSON parsed at 84 rows with no duplicate ids -- because the
content was correct and only the bytes were wrong. Repaired: normalised to LF, re-verified at 86 rows,
and `git diff --stat HEAD~1` now reads **187 insertions and zero deletions**. The guard is a habit rather
than a gate: *read the diffstat of a commit whose intent is an append; if the changed-line count is not
roughly what you appended, the line endings moved.* It matters because a channel is append-only and
shared, and the damage would have surfaced as a whole-file conflict in someone else's drain.

---

## WHAT I DID NOT DO, AND WHY

Every exclusion is a path outside this order's `<paths>`. None was overridden; each is a row.

- `tabs/analysis/StageDisplay.tsx`, `tabs/analysis/VariantSelector.tsx` -- 2 of the 3 `formatSourceAge`
  consumers. The cell's sentence says *"the panels that consume it"* and the grant reaches one. (W1-S46)
- `contracts/adapt.ts` -- would be needed to make ABSENT-vs-NULL survive into the view. (W1-S43)
- `contracts/index.ts` -- would be needed to give the view QUEUED and RUNNING. (W1-S41)
- `__tests__/fe-s-18/` and the three holdings smoke maps -- would be needed to clear `F18-AC3`, which the
  corrected bar now accommodates but which still needs a round-4 fixture cell. (W1-S44, S44)

The denominator behind the first bullet was taken by an **unscoped** census over all of `portal/src`
(`comp-find` -- 9 hits across 750 files scanned), not by looking where I expected consumers to be.

---

## HOUSEKEEPING

- Dev server started once on 5181 from `<WS>/portal`, used for the capture and for the FE-s-19 browser
  arms, killed before the final report.
- `node_modules` junction untouched; `bun install` never run.
- Scratch confined to `<WS>/.scratch/`. The two throwaway probes (`probe.test.ts`, `mutant.test.ts`) live
  there and are **not** committed; their outputs are quoted in the instance.
- The task order's own file was edited only to take the issuer's two corrected lines from `0e25c1d422`
  and to flip `<status>` to `complete`. It is inside the grant ("plus ... this order's own file").
- Nothing pushed, merged, rebased, checked out or cleaned in either repo.
