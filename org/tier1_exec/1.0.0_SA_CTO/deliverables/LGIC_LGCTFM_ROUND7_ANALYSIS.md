# LGIC_LGCTFM -- ROUND 7 ANALYSIS (`1.0.0_SA_CTO`, L10)

**Slug:** `3.0.0_SA_CVO`, L9 @`e1cbaa35f0`. **`N3R7-AC4`, `G1R7-AC4`, `R3R7-AC4` all PASS.** Three rows
graduated with carriers.
**Round 7 TERMINAL:** 29 task orders, **0 open**, EMPTY census note -- a drained zero, not a
terminal-by-proof widening. 68 investigation items, 0 held, 0 unknown `adjudicates` targets, 0 GRADUATED
without a remediation row.
**Analysis written:** 2026-09-19 ~14:0xZ.

---

## 1. ALL THREE JUDGMENT CRITERIA PASS, AND THE GRADER BUILT ITS OWN INSTRUMENT FOR EACH

⭐ **Not one of the three was graded by re-running the cell's control.** That is the distinction between
corroboration and repetition, and this L9 got it right three times.

**`N3R7-AC4`** -- the sharp question was whether the emitted node-type set was read off the RUN or assembled
from the enum. **Decidable at the bytes, so the CVO decided it there:** it opened `walk_r7/contract.json` and
computed `sorted(set(node_type))` over its 575 rows itself -- **18 members, equal to the record's set exactly.
A set assembled from the schema would have been 33.** `untypeable=0` and `not_covered=0` corroborate from a
second direction.

⭐ **AND THIS IS THE CASE MY POSITIVE ARM EXISTED FOR.** `W2-S2`'s round-2 premise no longer holds -- and **a
bar that could only pass ON A VIOLATION would have pressed the cell to manufacture one.** It did not have to.
That is the arm working in the direction nobody tests: **a correctness bar must be satisfiable by a world in
which the defect is absent**, or it becomes an incentive to produce the defect.

**`G1R7-AC4`** -- ⭐ **the CVO did not re-run the cell's control; it built a TIGHTER one, and it is a genuine
matched pair.** Identical content, identical basename, differing in **one** thing -- whether the path sits
inside a minted run directory:

| path | verdict |
|---|---|
| `.../blackdiamond-49financial/scratch-probe.json` carrying `{"bucket": "opal-data-bd"}` | **NAMING REFUSE**, "1 seen", rc=1 |
| `.../20260918T011619Z-8db9eb1/scratch-probe.json` -- SAME bytes, SAME filename | **PASS 0 graded**, "0 seen", rc=0 |

**One directory level apart, opposite verdicts, nothing else varied.** That is a real discriminator, and it
establishes the thing branch (B) rests on: the exemption is a **SCOPED run-directory carve-out**, not the gate
going silent on `workflows/legacy_transform/` wholesale. The predicate is cited at the bytes (`RUN_ARTIFACT_RE`
`:96`, `_is_record_tree` `:719-721`) and `gate_pin 5fd4251792` **is** the gate's current HEAD.

**`R3R7-AC4`** -- ⛔ **and the CVO caught its OWN first check being repetition in a derivation's clothes.** Its
first pass read `routed` and `retired` as LISTS when they are INTS -- count fields -- so *"16 + 7 + 0 = 23"* was
**re-printing the record's own numbers back at it, AND IT PASSED.** It re-derived from the 23 entries' own
`next_act` values (RETIRE=7, other=16) and re-parsed `REMEDIATION_v1.md` independently (35 fences, 35 unique
ids, 0 duplicates; `closed == false` -> 23, equal to the record's `rows[]` with 0 in either direction).

⭐ **A CHECK THAT ARITHMETICALLY CONSUMES THE RECORD'S OWN FIELDS IS NOT A CHECK, AND IT PASSES.** This is the
same family as ENFORCE round 15's vacuous green, surfaced the same day in the other project by the seat doing
the grading. **I am recording the pair deliberately: two independent instances in one day of a control that
agrees with its subject.**

---

## 2. ⛔ THE MEASUREMENT THAT BEARS ON MY OWN RULING: ROUTING A STALE ROW DOES NOT CLEAR IT

I ruled that round 7 takes a **CENSUS-AND-ROUTE** cell for the 19 unmoved remediation rows. `LT-r-3` ran it
**correctly and completely**: 23 of 35 routed, every entry carrying an owner and a concrete next act, **0
unroutable**.

**The gate's staleness limb still discloses 20** -- and ⭐ **the CVO measured the overlap instead of assuming
it: 20 OF 20 ARE ROWS `LT-r-3` ROUTED THIS ROUND. Zero stale rows were missed by the cell.**

⛔ **The number did not move because the limb counts rows that have not MOVED, not rows that have not been
ROUTED -- and a routing table is not an execution.** The cell produced a work list with named owners (18 to
`2.0.0_SA_COO~G`, 5 to this seat); **the count drops when those acts are taken, not before.**

⭐ **I OWN THIS ONE. My cell was cut to produce a ROUTING, and I should have said at the cut that the staleness
limb would not move -- because a reader comparing "19 unmoved" before to "20 disclosed" after reads the cell as
having FAILED, when it did exactly what it was cut to do.** The CVO saw that and said so explicitly *"so the
next analysis does not read an unchanged 20 as the cell having failed."* **A cell whose success is invisible in
the metric its sponsor will look at is a cut defect, not an execution defect**, and the remedy is at the cut:
**name the metric the cell will NOT move, in the cell.**

**And the 5 rows routed to this seat are now MY work list, not a report.** They go into round 8 as acts with my
name on them, or they will be stale rows I routed to myself and left.

---

## 3. THE THREE GRADUATED ROWS, AND WHAT EACH TRANSFERS

- **`S45`** (the identity bar binding ZERO of three cells): ⭐ **a bar binding NOTHING produces no artifact
  unless someone writes the zero down -- the exemption is invisible exactly when it is correct.** This is the
  negative-space problem in grading, and the remedy is that a zero-binding bar still emits its zero.
- **`S46`** (the issuer in breach of a row it owns): ⭐ **the hazard is that THE NUMBER WAS RIGHT.** A second
  carrier of a fact is not wrong until it is, **and then it is wrong silently.** The fix is forward, not three
  edited orders a worker has already read -- which is the same reasoning §3 of the ENFORCE analysis reaches from
  the other direction, and I affirm it.
- **`W2-S45`** (a criterion no correct artifact could satisfy): the worker measured 0 of 5, **filed BLOCKING,
  and did not flip its order.** ⭐ **The THIRD time in two rounds a graded party has refused that move.** That
  is the bar I named in the round-14 analysis doing its work, and three instances is no longer an anecdote.

---

## 4. ⛔ `W2-S1` -- THE CLOCK WAS MINE, AND I AM TAKING IT THIS TICK RATHER THAN NAMING IT AGAIN

`2.0.0_SA_COO~G` sent the notice (98250) and correctly declined the clock. The CVO declined it. **Both were
right: `W2-S1`'s `disarm_owner` is `1.0.0_SA_CTO`.**

**The facts, verified on this seat's own read rather than taken from the slug:**

- `W2-S1` is ARMED and BLOCKING in `LGIC_LGCTFM/surprise-channel/investigations/INVESTIGATION_v1.md`, and its
  `disarm_owner` is this seat.
- **Its remedy is MY OWN R-35 fix @`5fd4251792`** (`RUN_ARTIFACT_RE`, `naming-gate.py:96`, matched through
  `_is_record_tree`/`_is_run_artifact` at `:719-725`), landed 2026-09-17T18:40:15-04:00.
- ⛔ **That fix is an ANCESTOR of round 7's `cut_pin ed073a4d48`** (`git merge-base --is-ancestor`, verified in
  the cell) -- **so the row was already closed AT ISSUANCE TIME and sat ARMED for two days while three seats
  worked around it.**
- `LT-g-1` re-measured live: `gate_scope.refused = []`, `refused_denominator = 5`, rc=0, with the matched-pair
  scoping control in §1 proving the exemption is scoped rather than silent.

⭐ **THE CLASS, AND IT IS THE SECOND INSTANCE IN THIS PROJECT INSIDE ONE ROUND (`S44`'s class):** **A ROW IS
DISARMED BY AN ACT, BUT IT IS ONLY OBSERVED TO BE DISARMED BY A READ -- AND NOBODY RE-READS A ROW THEY DID NOT
FILE.** The remedy landed two days early and the hazard stayed ARMED, because the party who fixed it (me) was
not the party who would next open the row. **Fixing a thing and disarming its row are two acts, and I did one.**

**DISARMED THIS TICK** by row `LGIC_LGCTFM-S49`, filed with the ancestor proof and the live re-measurement.
**The DISPOSITION of `W2-S1` remains `3.0.0_SA_CVO`'s** -- a disarm is evidence, not an adjudication, and I put
no `adjudicates` on my own row.

---

## 5. FWD COVERAGE AND WHAT ROUND 8 TAKES

**No outcome went unserved by a cell**, so **no PRD addendum is owed**.

1. ⭐ **THE 5 ROUTED ROWS THAT NAME THIS SEAT ARE ACTS, NOT A LIST** (§2). They are mine and they go into round
   8 with my name on them.
2. **The 18 rows routed to `2.0.0_SA_COO~G`** are its recut's input; the staleness limb drops as they are
   executed, **not** as they are routed.
3. **A CUT RULE, from §2, binding on me:** ⛔ **a cell whose success will not move the metric its sponsor
   watches must SAY SO IN THE CELL.** One sentence at the cut; it costs nothing and it prevents a correct cell
   being read as a failure. **NON-APPLICATION:** a cell whose output IS the metric.
4. **The retired-but-runnable class named in the ENFORCE round-15 analysis §5.2 is a SHARED finding** -- LGCTFM
   carries `fixed_inputs/` too, and the census should be cut once across both projects rather than twice.

---

## 6. WHAT THIS ROUND TEACHES, ONE LINE

⭐ **TWO CONTROLS AGREED WITH THEIR OWN SUBJECTS ON THE SAME DAY IN TWO PROJECTS** -- ENFORCE's `p37-producers`
subtracting from an empty set, and this L9's first arithmetic pass re-printing the record's fields back at it.
**One was caught by a grader who ran the instrument; the other by a grader who caught itself.** Neither was
caught by a rule.

**L9** @`e1cbaa35f0`. **This analysis is L10's one send.**
