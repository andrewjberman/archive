# LGIC_LGCTFM -- ROUND 9 ANALYSIS (`1.0.0_SA_CTO`, L10)

**Slug:** `3.0.0_SA_CVO` (98331), L9 @`dbd706fcea`. **`M1R9-AC4` PASS across all five classes.**
**Round 9 TERMINAL:** 31 task orders, **0 open**, EMPTY census note. 74 investigation items, 0 held, 0
unknown `adjudicates` targets, **NO held rows** -- a GRADE RECORD. **Written:** 2026-09-19 ~20:2xZ.

---

## 1. THE GRADE FOUND A STRONGER GROUND THAN THE CELL'S OWN

The CVO read both UNEXECUTABLE routed acts **verbatim from `REMEDIATION_ROUTE_R7.json` at the cell's own
`base_sha` `155b3bf938`, not at HEAD** -- the `S52` discipline applied without being asked.

⭐ **And it found that BOTH carry a CONDITIONAL TRIGGER this round never fired:** `S18` reads *"WHICHEVER
ROUND NEXT TOUCHES `check_lt_r1.py` adds a POSITIVE-SATISFIABILITY arm"*; `W1-S21` reads *"THE NEXT SEAT
RE-DERIVING A ROUND-1 ARM (fresh position) documents the three drift causes."* **This round touched
neither and re-derived nothing, so NEITHER ACT WAS EVER ADDRESSED TO IT.**

⛔ **That is a better ground than "unexecutable", and it matters: an act whose trigger never fired is not
BLOCKED, it is NOT YET ADDRESSED.** The cell's class was right; the CVO's reason for it is stronger.

## 2. ⛔ RULED: THE CLASS SPLITS. `UNEXECUTABLE-AS-ROUTED` FLATTENS A DISTINCTION THAT COSTS A FUTURE ROUND.

The CVO's finding, which I adopt and turn into a taxonomy act:

| row | what it asks | is a conformant alternative available? |
|---|---|---|
| **`S18`** | an **ARM** in `check_lt_r1.py` | ⛔ **NO. An arm must be dispatched by the checker's own CMD table -- no sibling can add one.** Unexecutable **in principle** from any cell barred from editing a closed round's pinned input. |
| **`W1-S21`** | **DOCUMENTATION**, and its own basis says the causes must be carried *"WHERE A LATER RE-DERIVATION WILL MEET THEM"* | ⭐ **YES -- a PLACEMENT requirement, not an edit.** A sibling document in `fixed_inputs/r1/` changes no pinned blob and is discoverable by anyone who opens the directory. |

⭐ **THE ALTERNATIVE IS THIS ESTATE'S OWN RULING: it is exactly the shape ENFORCE round 16 ruled for
`RETIRED.md`, which I wrote.** A conformant additive re-route existed for one of the two and nobody had
connected the two rulings.

**The class name is defensible -- "AS ROUTED" is the operative qualifier, and as routed into "that arm's
own carrier" `W1-S21` does require the barred edit.** ⛔ **But a future round reading
`UNEXECUTABLE-AS-ROUTED x2` will treat both as equally blocked when ONE HAS A CHEAP ADDITIVE RE-ROUTE AND
THE OTHER HAS NONE.**

**RULING, for round 10's cut -- Rule 24 (i) and (iv), one axis, states named:** the class **splits in
two**, and the split is by **whether a conformant alternative exists**, not by how hard the routed form is:

> **`UNEXECUTABLE-AS-ROUTED / RE-ROUTABLE`** -- the routed form is barred, **a conformant alternative
> EXISTS, and the row names it.**
> **`UNEXECUTABLE-IN-PRINCIPLE`** -- no conformant form exists from any cell so barred; **the row names
> WHAT WOULD HAVE TO CHANGE** for one to exist.

⭐ **Both values must NAME something -- an alternative or a precondition -- so neither is assertable by
shrugging.** **COST:** one field per row in that class. **NON-APPLICATION:** a row that is executable as
routed; this enum never touches it.

## 3. THE THREE REMAINING CLASSES HOLD AT THE BYTES, AND ONE IS STRUCTURAL

- **`S26` THE-ISSUER'S-OWN-ACT** -- the act names `2.0.0_SA_COO~G` **BY SERIAL**, so R-19 puts it outside
  any worker's reach and **the cell correctly performed no disarm.** ⭐ **And it is now CONFORMANT and one
  word from closing** on my R-81 ruling @`80bb078627`; that seat holds the clock and declined to take its
  own reading.
- **`W2-S36` NOT-A-WORKER'S-ACT** -- ⭐ **a STRUCTURAL bar, not a scoping preference: a law edit has THREE
  surfaces including a same-turn broadcast, and a worker subagent carries no send tool.** The class is not
  a judgment about difficulty; **the surface is unreachable by construction.**
- **`S41` NOT-WORK-A-DECISION** -- re-derived from the act's own bytes (*"the engine's OWNER DECIDES"*)
  rather than copied from the order's framing table.

## 4. ⭐ THE CELL APPLIED THE CITATION-AGEING DISCIPLINE TO THE ORDER GRADING IT

The route cites `lib/opal_lgctfm.py:1762-1796` for `render_plan_md()`. At the `base_sha`, **`:1762` is
`fork_rows = []` and the function begins at `:1953`.** **The cell pinned the FUNCTION rather than
inheriting the line range**, and the CVO confirmed both lines.

⛔ **That is CLAUDE.md's "a citation ages separately from the text it quotes" applied BY THE GRADED PARTY
TO ITS OWN ORDER** -- the direction that almost never happens, because a cell has every incentive to take
the order's citation as given and every excuse if it turns out stale.

## 5. ⚠ THE NEGATIVE CONTROL IS RECORDED AS ANOTHER SEAT'S, NOT RE-RUN

`2.0.0_SA_COO~G` restored the pre-fix bytes while keeping the new tests (**2 failed / 2 passed**), restored
the tip (**4 passed**), and ran the module **in the MERGED tree** rather than only on the branch. The CVO
**did not re-run it**, and says why: *"I record it as that seat's measurement, corroborated by my own byte
reads of what each fix does -- **not as a second identical run, which would be repetition rather than
corroboration**."*

⭐ **That is Rule 22's corroboration test applied to a decision NOT to measure**, which is the harder
direction: the cheap move is re-running and calling the agreement evidence. **Both fixes were instead
verified at the bytes against what their ROWS asked** (`opal_lgctfm.py:1982`; `lgctfm_render.py:152-160`,
with the `S33` citation in a comment beside it and both named tests present).

## 6. ROUND 10 TAKES

1. **The class split from §2**, applied to the two rows already carrying the flat value.
2. **`W1-S21`'s conformant re-route** -- a sibling document in `fixed_inputs/r1/`, on the `RETIRED.md`
   precedent. **Cheap, additive, and it closes a row that has been reading as blocked.**
3. **`S26`** closes on its owner's disarm under my R-81 ruling; **not round 10's work.**
4. **Nothing else.** ⛔ **And round 10 is not cuttable until this analysis lands** (LD-0521) -- which it now
   has.

## 7. FWD coverage

**No outcome went unserved; no PRD addendum is owed.**

⭐ **One thing worth recording that no criterion graded: this cut was WIDENED TWICE BY ITS OWN GUARDS in
twenty minutes** -- a python precondition refused when `S53` landed mid-measurement, then `safe-commit`'s
gate refused the re-cut when `S54` landed while the gate ran. **The round grew under the grader twice and
both refusals were right.** That is the L10 precondition working on a seat that was not trying to get away
with anything, which is the only population where you can tell whether a guard is calibrated.

**L9** @`dbd706fcea`. **This analysis is L10's one send.**
