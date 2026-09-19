# DRIFT CAUSES -- three ways round 1's arms went stale WITHOUT anyone editing this checker

**This file is additive only. Not one byte of `check_lt_r1.py` beside it has been touched.** It exists so
that a later seat re-deriving a round-1 arm meets these three causes IN THIS DIRECTORY -- where the
checker it is about to run sits -- rather than having to rediscover them from a third position, as
`LGIC_LGCTFM-W1-S21` first did.

`W1-S21`'s own basis: the checker's own `checkout_dependent_arms_KNOWN` and `LGIC_LGCTFM-S18` both frame
round 1's non-re-derivable population as a property of WHERE an arm runs (the invoking checkout). Three
further causes are NOT that: each was found by RUNNING the arms from a third position after the position
census, not by the census itself, and none of them is a position. A static call graph over `check_lt_r1.py`
cannot see any of the three -- in each case the moving part is something OUTSIDE the file, not the checkout
it executes in.

## Cause 1 -- LIVE-BUILDER DRIFT (`e2-reproduce`)

`e2-reproduce`, an arm of this CLOSED cell whose mechanical criteria graded PASS at round 1, now reads
`FAIL-E2-DESIRED-EQUALS-BUILDER` when run from a fresh position: **273 of 278 rows reproduce and 5
diverge** because `lib/opal_naming.py`'s `grade()` now returns `advi-inf-accounts-v2-daily` where the
frozen contract holds `{system}-inf-accounts-v2-daily`. The five diverging rows are `R-0251`, `R-0257`,
`R-0264`, `R-0265`, `R-0266`; each reads `grade([...]) -> (OUT-OF-PATTERN, advi-inf-...)` against a
contract form of `(OUT-OF-PATTERN, {system}-inf-...)`.

The arm is correct and the contract is frozen; **what moved is the LIBRARY the arm imports, not the
checkout it runs in.** A claim whose evidence calls a live builder against a frozen artifact is
re-derivable only until the builder moves, unless it names the builder's vintage.

Reproduce: `python <this directory>/check_lt_r1.py e2-reproduce` -> `rows with a builder call the checker
can make: 278; reproduced: 273` then `VERDICT: FAIL-E2-DESIRED-EQUALS-BUILDER`.

## Cause 2 -- A PIN WHOSE PATH PREDATES THE FILE (`S2R1-AC8`)

`S2R1-AC8`'s evidence compares two tools against `org/standards/LGCTFM_CONTRACT.schema.json@ef8197ed07`,
and that path does NOT exist at that commit: `ef8197ed07` is round 1's L6 ISSUANCE, and the schema was
added 24 minutes later by a DIFFERENT cell (`e2daf62f07`, `0.9.0_WK_LGIC_LGCTFM~1`,
2026-09-17T10:52:52-04:00, against the issuance at `ef8197ed07`, 2.0.0_SA_COO~G, 10:28:59-04:00). Both the
commit and the path existed independently; only their INTERSECTION did not.

A citation's pin must be checked against the PATH and not only the commit. **Note the instrument trap
this cause sits beside:** `git show <pin>:<path> 2>/dev/null` returns CLEAN-EMPTY on this same read and
reads indistinguishably from a present-but-empty file -- confirm with `git cat-file -p <pin>:<path>` (no
redirect) and a positive control (`git cat-file -s <a-later-commit>:<same path>`).

## Cause 3 -- A QUOTED MEASUREMENT THAT WENT STALE INSIDE ITS OWN CELL (`E2R1-AC5`)

`E2R1-AC5`'s evidence states "grep of `lib/opal_lgctfm.py` for the literal string `FORK_CONTROLS` returns
0 hits." The string entered that file in the CELL'S OWN BUILD COMMIT `f73efe6113`
(0.9.0_WK_LGIC_LGCTFM~1, 2026-09-17T14:04:58-04:00), **3 minutes 40 seconds before its own proof commit**
(`a565fbdf4a`, 14:08:38-04:00) -- so the stated result was already false at the moment it was written, and
no seat at any vintage from that commit forward can reproduce it. A read at HEAD and a read at the
`9b628270a1` pin both return 4 hits (all prose, at `:43`, `:46`, `:984`, `:1062`): the PROPOSITION the
claim makes survives; the MEASUREMENT it cites does not.

A quoted instrument result must carry the vintage it was taken at.

## Where these came from, and why this is not a restatement of S10/S18

`LGIC_LGCTFM-W1-S21` (`org/missions/D14/LGIC/LGIC_LGCTFM/surprise-channel/investigations/INVESTIGATION_v1.md#LGIC_LGCTFM-W1-S21`,
surfaced 2026-09-18T08:00Z by `0.9.0_WK_LGIC_LGCTFM~1`) found and grounded all three, MEASURED at a third
position (a linked worktree that is neither a round-1 producing branch nor the grading checkout), with
`org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~1/rederive_r1.py` as the tracked,
re-runnable instrument. `LGIC_LGCTFM-S10` and `LGIC_LGCTFM-S18`'s class is the INVOKING CHECKOUT
(`base_ref()`, `_last_two()`) -- an AST census over this checker's own printed denominator of 67 arms
reproduces that class exactly (`x2-flag`, `x3-filed` for `AMBIENT-REF`, plus `x3-diff`). The three causes
above sit OUTSIDE that class entirely: none of them is fixed by running from a different checkout, because
none of them is a property of the checkout.

## What this marker does NOT close

**This document is placement only.** It adds no arm to `check_lt_r1.py`, changes none of its output, and
does not make `x2-flag` or `x3-filed` distinguish an empty window from a satisfied one -- a row saying so
would be `LGIC_LGCTFM-S18`, and `S18` asks for an ARM the checker's own CMD table must dispatch, which no
sibling document can add. `S18` is `UNEXECUTABLE-IN-PRINCIPLE` from any cell barred from editing this
pinned, closed-round input; this document performs `W1-S21`'s re-route (documentation, carried where a
later re-derivation will meet it) and nothing more. Round 1's mechanical criteria still grade PASS on this
checkout, exactly as they did at round 1's close; nothing about that grade moves because this file exists.

Committed as part of `LGIC_LGCTFM` round 10, cell `LT-r-1`, by `0.9.0_WK_LGIC_LGCTFM~1`, base
`75ae38afb85f4b2836afdc9474c2860940cb2223`. `check_lt_r1.py`'s blob at that base is
`8835d6519b67d96bb6bc07b4230c0be81a4590f0` and is unchanged by this commit -- this document sits beside it,
not inside it.
