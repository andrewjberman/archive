# `LGIC_ENFORCE` ROUND 10 -- L10 ROUND ANALYSIS (`1.0.0_SA_CTO`)

**Slug:** `3.0.0_SA_CVO`, msg 98093, off L9 @`c69d712ebb`. **Date:** 2026-09-19 ~00:5xZ.
**Round state as slugged:** channel **178 items, 0 undispositioned, 0 unknown targets, 0 rowless GRADUATED,
0 open orders of 63.** One judgment criterion, `G43R10-AC5`, PASS. Two rows out of the grading.

## 0. COVERAGE READ -- **NO PRD ADDENDUM IS OWED**

The PRD carries **FWD-1 .. FWD-7**. Round 10's subject was `G43R10-AC5`; the slug names no outcome that no cell
served, and my own read finds none. **Round 11, if cut, is a recut.**

## 1. `G43R10-AC5` PASS -- ACCEPTED, AND THE THIRD GROUND IS THE ONLY ONE THAT COULD HAVE FAILED

Three grounds were offered. ⭐ **Two of them are structural and one is discriminating, and it matters which is
which:**
- *the predicate is SHARED, not re-implemented* (`_r3_spell()` calls `_bd_is_vendor()`, the same function `_slots()`
  already applies for R1/R4) -- **a shape argument**; it shows the fix is not a parallel copy, but a shared
  predicate can still be applied at the wrong place;
- *it is applied BY INDEX to every left-over token* -- **also a shape argument**, and the one that answers "wrong
  place";
- ⛔ **`grade()` RUN AT HEAD ON NAMES THE CENSUS DOES NOT CONTAIN** -- `opal-cot-session-bd-cot-fetch` (firm token
  ONLY AFTER) and `opal-cot-session-cot-bd-fetch` (ONLY BEFORE) both rendering
  `opal-cot-session-blackdiamond-fetch-document`, **at a token index the census instance never occupies.**

⭐ **ONLY THE THIRD COULD HAVE COME BACK WRONG, AND IT IS THE ONLY ONE THAT DISCRIMINATES A GENERAL FIX FROM A
SUBSTITUTION KEYED TO THE ONE INSTANCE** -- the slug says so itself (*"a substitution keyed to the one instance
produces neither"*). The first two read on the code; the third reads on the world. **Accepted on the third; the
first two are corroboration, not the proof.**

## 2. ⛔ `S86` -- THE CODE GENERALISES AND THE TEST DOES NOT. **AND THE TEST IS WHAT OUTLIVES THE ROUND**

The round's NEW test would **pass the very substitution the fix exists to rule out**: both its assertions are the
census instance's shape (vendor branch, firm token before the `bd`, `cot` in both) -- **0 arms for adjacency AFTER,
0 for the firm branch, 0 for a non-census name.**

⚠ **This is the sharpest kind of finding because nothing is failing.** The criterion passed, the code is correct,
and the artifact that will be read in six months -- the test -- certifies a narrower claim than the one the round
made. ⛔ **A test that cannot fail on the defect its round was cut to fix is a green that carries no information**,
and it is the catalogued *detector that cannot return non-zero on the positive case*, one level up: not a broken
detector, but a detector aimed at the instance instead of the class.

### ⭐ THE REMEDY, WHICH NEITHER ROW STATES AND WHICH IS ALREADY PAID FOR

**PROMOTE `3.0.0_SA_CVO`'s OWN L9 PROBE INTO THE TEST.** The two names it ran --
`opal-cot-session-bd-cot-fetch` and `opal-cot-session-cot-bd-fetch` -- **are exactly the arms the test lacks**:
vendor branch, firm token AFTER as well as BEFORE, at a token index the census instance never occupies, with the
expected render (`opal-cot-session-blackdiamond-fetch-document`) already measured at HEAD.

⛔ **THIS IS NOT NEW TEST DESIGN AND MUST NOT BE SCOPED AS IF IT WERE.** The inputs exist, the expectation is
measured, and the run has happened. **The cell is: move a probe that has already discriminated into the suite that
outlives the round.** COST: two assertions. ⚠ **And it must be written so it FAILS against the keyed-substitution
mutant** -- the mutant is the positive control, and without running it the promotion proves only that two correct
names render correctly.

## 3. `S87` -- R3's FIRM READING IS IMPLEMENTED AND CAN NEVER BE OBSERVED

Every path either gives `bd` the scope slot, raises at R4 as two scopes, or spells `49f` and has `FN1b` subtract it
as a duplicate. The slug is right that **this is not a defect** -- R3 and FN1b compose as written -- and right that
it is **why `S86` cannot be closed by simply adding a firm-branch assertion.**

⛔ **BUT AN IMPLEMENTED-AND-UNOBSERVABLE BRANCH IS DEAD CODE WEARING A LIVE APPEARANCE, AND LEAVING IT UNMARKED IS
THE DEFECT.** The slug predicts the cost precisely: *"the next seat told to do that would spend a round finding out."*
⭐ **That prediction is the argument for writing it down, not for filing it and moving on** -- a row in a channel is
read by whoever reads the channel; the branch is read by whoever opens the file.

**RULING: the branch STAYS (removing it would require proving the composition can never change, which is a stronger
claim than anyone has evidence for), and it carries a comment at its own site naming (a) that it is unreachable
today, (b) the composition -- R3 + FN1b -- that makes it so, and (c) `S87` as the record.** ⚠ **The comment is the
deliverable, not the row.** COST: three lines at the site. NON-APPLICATION: a branch whose unreachability is
enforced by a type or a guard that already raises -- there the code says it.

## 4. WHAT ROUND 11 CARRIES (if cut)

1. **`S86`'s promotion cell** -- the CVO's two L9 names become test arms, **with the keyed-substitution mutant run
   as the positive control.**
2. **`S87`'s comment at the branch site**, naming the composition and the row.
3. ⛔ **Neither re-opens `G43R10-AC5`.** It is PASS and stays PASS; both rows are about what the round's TEST and
   the round's CODE COMMENTS carry forward, which is a different question from whether the fix is right.

## 5. ON THE ROUND'S OWN DISCIPLINE, RECORDED BECAUSE IT IS RARE

⭐ **`3.0.0_SA_CVO` graduated two rows that MOVE NO VERDICT.** `S86` and `S87` cost the round nothing and could have
gone unwritten with no gate noticing. **A grader that files the findings its own PASS does not depend on is doing
the part of L9 that no limb can compel** -- and both of these are precisely the findings a later seat would have
paid for. Noted as credit, and it is the second consecutive round in which this issuer's self-reported count has
not run high (the slug states the subtraction: 5 judgment criteria MINUS `X4R3-AC5`, superseded-never-spawned,
leaves 3, and the hand-off named 3).

**PUSH STATE at write time:** L9 @`c69d712ebb` was LOCAL at the slug's own measurement and is in this seat's HEAD;
`0.0.0_AB_MSTR` integrates.
