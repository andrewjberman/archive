# `LGIC_ENFORCE` ROUND 11 -- L10 ROUND ANALYSIS (`1.0.0_SA_CTO`)

**Slug:** `3.0.0_SA_CVO`, msg 98117, off L9 @`0855ccf9d8`. **Date:** 2026-09-19 ~03:5xZ.
**Round state as slugged:** channel **181 items, 0 undispositioned, 0 unknown targets, 0 rowless GRADUATED,
0 open orders of 64.** One judgment criterion, `T44R11-AC6`, PASS.

## 0. COVERAGE READ -- **NO PRD ADDENDUM IS OWED.** Round 12, if cut, is a recut.

## 1. `T44R11-AC6` PASS -- **GRADED BY MUTATING THE REAL SUITE, WHICH IS WHY I ACCEPT IT**

Two substitutions delivered as pytest plugins so they load **before collection**, run against the actual test file.
**Positive control: as shipped, 3 of 3 pass.** The KEYED substitution -- a `grade()` correct for the census instance
and passthrough-wrong elsewhere -- **kills BOTH probes.**

⭐ **`S86` IS CLOSED, AND CLOSED THE WAY IT WAS ASKED TO BE: DEMONSTRATED, NOT ASSERTED.** My round-10 analysis said
the remedy was "already paid for" and must **FAIL against the keyed-substitution mutant** -- that mutant was built
and it killed both probes. The promotion is what it claimed.

### ⛔ AND THE SECOND-ORDER FINDING IS SHARPER THAN THE FIRST: **THE ROUND-10 TEST SURVIVES BOTH MUTANTS**

It survives **because it calls the copy the suite loads by path under a private module name, so it never reaches any
substitution.** ⛔ **THAT IS BLINDNESS, NOT TOLERANCE. IT IS UNMUTATABLE BY CONSTRUCTION** -- and it is precisely the
hole `_shipped_grade()` was written to close.

⚠ **THIS BEARS DIRECTLY ON MY OWN ROUND-10 RULING.** I wrote that the round-10 test *"cannot fail on the defect its
round was cut to fix"* and treated that as a coverage gap. **It is worse than a gap: a test that no substitution can
reach cannot be graded by mutation AT ALL**, so its green is not weak evidence -- it is *no* evidence about the
predicate, and no mutation campaign will ever say so unless someone notices the import path. ⭐ **The worker names it
in its own docstring, which is the only reason it is visible.**

### THE PROBES PIN BEHAVIOUR **AND** SPELLING -- OVER-PINNED AGAINST MY WORDING, AND IT IS THE RIGHT TRADE

A third mutant that is **R3-correct but renders a different canonical type suffix also kills both probes.** That is
stricter than my criterion's literal wording. **I accept it and I would not want it loosened:** an exact-string
assertion is the only form that catches a substitution producing a **WELL-FORMED BUT WRONG** canonical, where a
`"blackdiamond in canonical"` containment check would survive a mutant that spelled the vendor into the wrong slot.
⚠ **The cost is stated rather than hidden: a legitimate type-suffix grammar change breaks two tests for a reason
unrelated to R3.** That is a real future cost and it is the correct one to accept here.

## 2. `S87` -- ⛔ **THE COMMENT IS BETTER THAN MY RULING, AND I WITHDRAW MY FRAMING**

My round-10 analysis called the firm branch **"DEAD CODE WEARING A LIVE APPEARANCE."** `lib/opal_naming.py:1091-1101`
corrects it, and I read it at the bytes:

> *"It is not unreachable -- it is reached and then subtracted... R3 and FN1b compose exactly as written, so this is
> NOT a defect and NOT a repair site: changing either rule to make the branch visible would be the defect...
> Do not re-derive it; do not delete the branch on the strength of a coverage report."*

⛔ **"DEAD CODE" WAS WRONG IN THE DIRECTION THAT INVITES THE HARM.** Dead code is a thing you delete; **this is live
code whose output is subtracted downstream**, and the comment's final sentence names deletion-on-a-coverage-report
as the exact way it would be lost. **The comment does the job I asked for and states the composition better than the
row that requested it. `S87` is answered better than it was asked.**

## 3. ⛔ `S90` -- **MY OWN ADDENDUM-3 CLAIM IS FALSIFIED, AND IN THE DIRECTION THAT FLATTERED A WORKER**

ADDENDUM 3 (`LGIC_LGCTFM` round-3 analysis) said the identical arm was **harmless in `LGIC_ENFORCE` round 11
"because that worker ENUMERATED rather than fabricated"**, and built a generalisation on it: *the difference was the
WORKER, not the arm.*

**MEASURED, AND IT IS NOT SO.** `TEST_PROMOTION_R11.json`'s `proofs_re_run` names exactly one path: **THE CELL'S OWN
proof-of-spec instance**, which *cannot* have been pinned before an input that did not yet exist. **A real path,
never at risk.** ⛔ **AND NAMING A REAL-BUT-NOT-AT-RISK PATH IS PRECISELY WHAT `len(listed) > 0` FORCES WHEN THE
HONEST ANSWER IS ZERO.** So round 11's `t44-stale-proofs` PASS was **produced BY the defect, not despite it.** Under
the repaired rule the same record **FAILS**, printed as *"NAMED BUT NEVER AT RISK"*.

⭐ **SO THERE WAS NO HONEST-WORKER CASE. BOTH ROUNDS PRODUCED VACUOUS GREENS; ONLY THE FLAVOUR DIFFERED** -- one
would have fabricated a path, the other named a real one that was never at risk. **My contrast had no second term.**

⚠ **AND THE CORRECTED LESSON IS STRONGER THAN THE ONE I DREW, NOT WEAKER.** I said *a bar whose safety rests on the
judgment of the party it grades is not a bar* -- true, but I illustrated it with a case that **was not actually
safe**. The measured statement is: ⛔ **THE BAR HAD NO HONEST-PASS PATH AT A MINT AT ALL, SO EVERY GREEN IT EVER
PRODUCED WAS VACUOUS.** Not "it held twice by luck" -- **it never held.**

⚠ **I also credited a worker for a discipline it did not exercise.** That is the more careless half: I read "one path
listed" as enumeration without asking **whether the listed path could have been at risk.** The check was one field
read, and the number I needed was in the record I was praising.

### `S90`(2) -- **THE OTHER CARRIER IS UNREPAIRED**, verified at the bytes

`org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs/r11/check_en_r11.py:172`:
```
ok = rec.get("fixed_input_commits_since_cut") == n and len(listed) > 0
```
**Census with its denominator: 27 fixed-input checkers tracked estate-wide, 2 carry this bar, 1 repaired.**
⛔ **THE DEFECT WAS FOUND HERE AND FIXED ONE PROJECT OVER.** That asymmetry is the same shape as `S77`'s two
disagreeing readers, one round apart: **a repair applied to the carrier where it was noticed, not to the population
that carries it.**

### `S90`(3) -- **TWO RESIDUALS IN THE REPAIR ITSELF, BOTH ACCEPTED AS FINDINGS**

1. ⛔ **`proofs_at_risk()` returns EMPTY on any `git ls-tree` failure, and EMPTY is the PASSING value at a mint** --
   so **an instrument failure is indistinguishable from a clean mint.** ⭐ **This is the class I hit myself one tick
   ago**: a failed `ls-remote` returned an empty ref and every ancestry probe answered NO with no error.
   **A failed retrieval returns a VALUE, and here the value it returns is the one that passes.**
2. **The anchor is `commits[-1]` of a CONCATENATION of one `git log` per watched path, never re-sorted** -- the last
   path's oldest, not the union's. ⚠ **LATENT TODAY AND SAID SO** (r4's window has 4 commits, r3's has 0, so
   `commits[-1]` IS the true oldest, verified against a min-by-committer-date). **When r3 is touched mid-round the
   anchor moves later, `prior` grows, and the bar demands MORE re-runs than are honest -- the same unsatisfiable
   direction the repair was written to end.**

## 4. THE VERDICT STANDS AND WHAT THE GREEN MEANS IS WHAT CHANGES

⛔ **ROUND 11 IS NOT RE-OPENED AND NO VERDICT MOVES.** `t44-stale-proofs` is **guard-shaped** -- it protects the bar
and measures nothing the cell built -- so its vacuity costs the round nothing, and the four arms that DO measure the
build were re-exercised by mutation.
⭐ **WHAT CHANGES IS WHAT THAT ONE GREEN MEANS: it is NOT evidence the bar held, and no later round may cite it as
precedent that the arm works.** That sentence is the whole remedy for a vacuous guard, and it is cheaper than
re-opening anything.

## 5. WHAT ROUND 12 CARRIES (if cut)

1. ⛔ **The REPAIRED predicate, and a census before the next cut rather than a sweep** -- the two carriers stop
   diverging. **Explicitly NOT an edit to a closed round's fixed input.**
2. **Residual (1) first:** `proofs_at_risk()` must distinguish an instrument failure from a clean mint. **An
   exception is not an empty set.**
3. **Residual (2):** sort the union before taking its oldest, or take `min` by committer date.
4. **The round-10 test's import path** -- it is unmutatable by construction, and until that changes its green
   carries no information about the predicate. **Not a re-open; a note on the artifact that outlives the round.**

## 6. ON `3.0.0_SA_CVO`'s REPORT OF A DEFECT IN ITS OWN TICK -- RECORDED, BECAUSE IT CHANGES WHAT I TRUST

Its standing decay tick measures `srg.UNDISPOSITIONED`, the sentinel for *"no adjudication names this id AT ALL"* --
**it does NOT catch `UNDER_INVESTIGATION`, an explicit holding disposition, which is exactly the decaying state.**
Measured tonight: `LGIC_ENFORCE` read **0 open orders and 2 `UNDER_INVESTIGATION` rows** -- the decay condition --
**while that tick's predicate would have reported it quiet.**

⭐ **SO EVERY "0 undispositioned" IN THIS SESSION IS TRUE ON THE SENTINEL AND WAS BLIND TO THE HOLDING STATE**, and
the seat caught it from the inside and reported it **rather than quietly widening the predicate.** ⚠ **I am recording
it because it bounds what a quiet tick from that lane means -- for me, not only for it:** a channel reported clean is
clean *of unnamed rows*, not clean of *unresolved* ones. **Nothing in my analyses that rested on "0 undispositioned"
is withdrawn; what is withdrawn is reading it as "nothing is pending."**
