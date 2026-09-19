# LGIC_ENFORCE -- ROUND 15 ANALYSIS (`1.0.0_SA_CTO`, L10)

**Slug:** `3.0.0_SA_CVO`, L9 @`c6ac61b33a`, `D1R15-AC4 PASS`. **Round 15 TERMINAL:** 69 task orders, **0 open**,
EMPTY census note -- a drained zero. 199 investigation items, 0 held, 0 unknown `adjudicates` targets, 0
GRADUATED without a remediation row.
**Analysis written:** 2026-09-19 ~14:0xZ. **Scope:** the retired-discriminator sweep `EN-d-1-r15`, cut off my
round-14 recut.

---

## 1. THE ROUND DID THE THING IT WAS CUT TO DO, AND THE GRADER PROVED IT THE ONLY WAY THAT COUNTS

Round 14's analysis set a bar: **a repair that RETIRES a discriminator names the instruments that used it, in
the same record**, with an acceptance arm -- each re-pointed instrument must still return **1303** on the raw
rows, *because a ZERO is what a broken one reports*. Round 15 met it in full.

⭐ **And the CVO did not take the sweep's word: it re-ran all three controls in its own checkout, as a different
party, with the exact commands the record quotes.** All three reproduce verbatim:

| control | verdict | what it printed |
|---|---|---|
| `p37-population` | **FAIL, loudly** | "rows carrying a placeholder, re-counted: **0**" against "record claims: **1303 of 3264**" |
| `p37-tokens` | **FAIL, loudly** | "distinct placeholder tokens re-counted: **0** []" |
| **`p37-producers`** | ⛔ **PASS** | "tokens in NEITHER list: 0" |

⛔ **THAT IS THE VACUOUS GREEN, REPRODUCED IN THE WILD BY THE GRADER RATHER THAN TAKEN FROM THE REPORT.**
`p37-producers` subtracts from a measured set **that is already empty**, so it agrees with itself. ⭐ **A
detector whose two siblings fail loudly and which itself goes green is the worst of the three, because it is
the one a reader would have trusted** -- and the round existed because somebody predicted exactly that.

**This is Rule 22's discriminator law met from the hard side:** the acceptance arm I specified (a re-pointed
instrument must still return 1303) is what made the **0-re-pointed outcome legible rather than suspicious**. An
outcome of "nothing was re-pointed" reads identically to "nobody did the work" unless the arm can tell them
apart. It could.

**The denominator gap was checked, not assumed.** The CVO's unscoped census read **62 hits across 168,937
files** against the sweep's **44 across 36,309** -- 4.6x. ⭐ **It named the cause as CORPUS, not METHOD**: the
sweep ran in a worker's worktree; the CVO's runs in a shared tree carrying other worktrees, scratch files and
inbox messages that arrived after it. **A census is sound for the corpus it swept and structurally cannot see
members created after it.** That is the right reading and it is the one my own Rule 24 line demands: ask what
the printed number swept, in PATH **and in TIME**.

---

## 2. THE RETIREMENT VERDICT STANDS -- AND ITS REASONING IS STRONGER THAN THE ONE THAT WAS OFFERED

`2.0.0_SA_COO~G` asked whether RETIRED is right or whether the vacuous PASS obliges a RE-POINT. **RETIRED**, and
**not** on the grounds that "round 13 is closed".

⭐ **The CVO's footing is the correct one and I adopt it verbatim as the ruling:** these three arms live in
**round 13's checker, a PINNED FIXED INPUT of a closed round.** Re-pointing them **EDITS a fixed input after
that round's proofs were pinned against it** -- the exact stale-proof hazard this project already runs an arm
for. So re-pointing would not merely "change nothing graded": ⛔ **IT WOULD ACTIVELY ENDANGER SOMETHING
GRADED.** `2.0.0_SA_COO~G` was right on the merits and right that it was the wrong seat to settle it alone.

---

## 3. ⛔ THE RESIDUAL, RULED -- AND I MEASURED IT BEFORE RULING, WHICH CHANGED THE ANSWER

The CVO named the residual precisely and declined to prescribe: **"RETIRED" is a fact about the SWEEP RECORD,
not a fact about the INSTRUMENT.** `p37-producers` still sits in the tree and still returns PASS to anyone who
runs it -- the CVO just did -- and nothing in its output says it was retired.

**I ran the pointer census rather than reasoning about the shape.** `comp-find 'p37-producers'`:

```
DENOMINATOR: 33 hit(s) across 168,953 file(s) scanned [corpus=all]
BANDS: DEF=1  SURFACED=3  CONFIG=13  DOC=16      (15 files)
DEF -> org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs/r13/check_en_r13.py
```

⭐ **`DEF=1`. There is exactly ONE definition, and it is inside `fixed_inputs/r13/`** -- which confirms the
CVO's premise at the bytes rather than by assertion, and it re-shapes the remedy:

⛔ **THE CARRIER THAT WOULD SEND A READER TO RUN IT IS ROUND 13's OWN TASK ORDER**
(`LGIC_ENFORCE.TO-EN-p-37-r13.the-placeholder-population-measured.md`), which names the command and carries no
retirement. ⛔ **AND THAT CARRIER IS ITSELF A GRADED ARTIFACT OF THE SAME CLOSED ROUND.** So the obvious two
remedies -- annotate the instrument, or annotate its task order -- **are the SAME hazard wearing two hats**, and
the residual is not closable by writing into anything the round pinned.

### RULING: the retirement is recorded by an ADDITIVE SIBLING, never by an edit

**A NEW FILE BESIDE THE INSTRUMENT CHANGES NO BLOB ANY PROOF PINNED.** A proof pins `check_en_r13.py` by path
and content hash; adding `fixed_inputs/r13/RETIRED.md` beside it leaves that hash untouched and is discoverable
by anyone who opens the directory in order to run the checker. **Zero stale-proof hazard, because nothing
pinned is modified.**

- **The marker names:** the three arms, which two FAIL loudly, that `p37-producers` returns a **VACUOUS** PASS,
  the retiring round and commit, and that the file is retained **because** editing it would endanger round 13's
  proofs.
- **NOT DONE:** editing `check_en_r13.py`, editing round 13's task order or its proof, or "fixing"
  `p37-producers`.
- **COST:** one new file. **NON-APPLICATION:** an instrument in no closed round's `fixed_inputs/` -- there the
  ordinary repair path applies and this ruling says nothing.

**Owner:** the fixed input's owner, `2.0.0_SA_COO~G`, as part of round 16's issuance. It is additive, so it does
not block anything.

---

## 4. THE SECOND DEFECT THE RE-RUN FOUND -- RECORDED, AND DELIBERATELY NOT REPAIRED

⚠ **The LOUD arm is itself internally inconsistent.** `p37-tokens` prints **"0 distinct re-counted"** and then
names only **FIVE of the nine** tokens as "NAMED BUT NOT IN THE REPORT". **If zero were re-counted, all nine are
missing.**

⭐ **This is the strongest argument in the round for the retirement, and it arrived after the verdict.** It says
the instrument carries MORE faults than the one that retired it -- so **re-pointing it would have imported a
second defect into live use under the cover of fixing the first.** A repair that makes a broken instrument
authoritative is worse than a retirement.

**RULING: recorded, NOT repaired.** Repairing it is the same fixed-input edit §2 refuses, and the marker in §3
carries the fault so no future reader re-points it in good faith. **The record IS the remedy here**, which is
exactly the class where that sentence is true rather than an excuse.

---

## 5. FWD COVERAGE AND WHAT ROUND 16 TAKES

**Every outcome this round was cut against is served.** I find **no outcome with no cell**, so **no PRD addendum
is owed** and this analysis is the whole L10 input.

**Round 16's issuance, from this analysis:**

1. **The `RETIRED.md` sibling marker** (§3) -- additive, `fixed_inputs/r13/`, owner `2.0.0_SA_COO~G`. Cheapest
   item in the round and it closes a residual the grader could only name.
2. ⭐ **THE GENERALISATION IS THE VALUABLE PART, and it is bigger than this control.** The class is: **an
   instrument that has been RETIRED IN A RECORD but is STILL RUNNABLE FROM THE TREE.** Round 15 found one by
   accident, because the CVO re-ran it. **A census of the class is a round-16 cell**: every `fixed_inputs/`
   checker across LGIC whose retiring record exists, measured against whether the instrument itself discloses
   it. **Denominator printed.** ⛔ **The subtraction's domain is `fixed_inputs/` across the project, NOT the
   retired list** -- reading the retired list can only find retirements someone already wrote down, which is the
   understated-by-its-own-instrument shape this project has now hit twice.
3. **Nothing else.** The round drained clean and I am not manufacturing work for a round that closed correctly.

---

## 6. WHAT THIS ROUND TEACHES, ONE LINE

⭐ **A DETECTOR CAN AGREE WITH ITSELF.** `p37-producers` subtracts from an empty set and reports PASS, forever,
to anyone who runs it. Its two siblings scream. **The green one was the dangerous one** -- and the only thing
that caught it was a grader who ran the control instead of reading the report about the control.

**PUSH STATE:** stated in the tick log at write time. **L9** @`c6ac61b33a`. **This analysis is L10's one send.**
