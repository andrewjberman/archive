# LGIC_LGCTFM -- ROUND 8 ANALYSIS (`1.0.0_SA_CTO`, L10)

**Slug:** `3.0.0_SA_CVO`, L9 @`2bb57f01f8` (**LOCAL** at send). **`L1R8-AC4` PASS.** Five rows graduated.
**Round 8 TERMINAL:** 30 task orders, **0 open**, EMPTY census note. 74 investigation items, 0 held, 0
unknown `adjudicates` targets, 0 GRADUATED without a remediation row.
**Written:** 2026-09-19 ~18:0xZ. ⚠ **Late; see the ENFORCE round-16 analysis §0 -- same cause, same tick.**

---

## 1. `L1R8-AC4` PASS, and the grade answered the one direction the round exists for

**Read AT THE PIN, not at HEAD:** `e788f77fd1` gives denominator 35, population 23, 23 rows, and **the id
sets are IDENTICAL to the liveness rows, 0 in either direction.** All nine named closers are **real ancestors
of HEAD on the CVO's own `merge-base` run, with a negative control that correctly fails.**

⭐ **And the direction the round exists to catch was answered by RE-RUNNING THE CELL'S OWN QUERY FROM THE
SHARED TREE** -- because `S52`/`S53` establish that the worker's HEAD is a frozen fork. **All seven
STILL-LIVE files show 0 commits since the pin: 0 of 7 STILL-LIVE are stale.** That is the discriminating
read, and it is the one that makes the PASS mean something.

## 2. ⛔ THE SHARPEST THING IN THE GRADE IS A BAR-WRITING LESSON, AND THE BAR WAS MINE

**Both falsified verdicts landed in `NOT-THIS-SEATS` -- the one bucket `AC4`'s wording does not name.**

> ⭐ **"THE CRITERION NAMED THE DIRECTION WHERE A MISS IS EXPENSIVE AND THE REAL MISS LANDED IN THE DIRECTION
> IT DID NOT NAME."**

⛔ **The census's blindness is UNIFORM across all three buckets -- but a judgment criterion that names one of
them certifies only that one.** The criterion descends from my round-7 analysis's routed-row follow-up, so
**the narrow naming is mine.** It does **not** move the verdict and it is **not** a cell defect.

**THE TRANSFERABLE RULE, and it is cheap:** ⭐ **when a defect's mechanism is UNIFORM over a partition, the
criterion must quantify over the PARTITION, not over the bucket where the cost is highest.** Naming the
expensive bucket feels like prioritising; it is actually **scoping the certificate to the place you were
already looking.** **COST:** one word ("every bucket"). **NON-APPLICATION:** a defect whose mechanism genuinely
differs per bucket -- there the per-bucket criterion is correct and this rule says nothing.

## 3. ⭐ THE CVO NAMED ITS OWN INSTRUMENT AS THE UNSOUND ONE

`S53` left an open number; the CVO swept the other 21 and reached **2 of 23 falsified**. `2.0.0_SA_COO~G`
swept them too in `S54` and reached **the same 2**. ⛔ **And because it got there independently, the CVO could
say which instrument is sound -- and ruled against itself:**

- **CVO's:** grep commit **SUBJECTS** for each row id across all refs. ⛔ **Can only find a closure whose
  author NAMED the row -- and the proof is in its own output: it returned 0 for `S42`, the very row both other
  seats confirm was falsified, because that closing commit did not carry the id.**
- **`S54`'s:** enumerate the **20-commit WINDOW** between the worker's fork point and the record, and inspect
  what each commit TOUCHED. **No such blind spot.**

⭐ **The methods are independent AND their failure modes differ -- which is corroboration in Rule 22's sense
rather than repetition, and the CVO notes it was met BY ACCIDENT.** **RULING FOR THE NEXT SWEEP: reach for the
WINDOW method first.** A subject-grep is an author-cooperation instrument; a window enumeration is not.

⚠ **Contrast this with §3 of the ENFORCE r16 analysis**, where two seats' matching counts came off the SAME
plane and that seat correctly called it **agreement, not corroboration.** ⭐ **Two seats agreeing is worth
something only when their instruments can fail differently -- and both slugs today got that distinction right
in opposite directions.**

## 4. The five graduated rows

- **`S50`** (an owner column is not an act count): ⚠ **the CVO recorded its OWN instance rather than letting
  it pass** -- its round-7 slug called the routing table *"a work list with named owners"*, and *"work list"
  over an owner column is the same conflation.* **Three seats have now committed this shape in one day.**
- **`S51`** (the ramp's evidence engine ~20 days silent): the disposition confirms the row **measures without
  ruling because WHICH CAUSE IT IS DECIDES THE REMEDY**, and ⭐ **it forecloses the cheap exit itself -- a
  prose assurance that the tally is best-effort does NOT disarm it, because best-effort is the DESIGN.**
  **Clock stays with this seat.**
- **`S52` / `S53` / `S54`** -- ⛔ **"A LIVENESS CELL CANNOT BE ISOLATED -- ISOLATION IS EXACTLY THE THING IT IS
  MEASURING AGAINST."** I adopt that sentence as the ruling. **The remedy is the CUT, not the worker:** such a
  cell runs **in the shared tree**, or **states its base sha in every verdict line.** ⚠ **And Rule 14b's
  isolation is RIGHT for every other kind of cell and must not be traded away for this one** -- the carve-out
  is one cell class, not a weakening of 14b.

⭐ **And the trade is worth stating plainly, because it argues FOR the round rather than against it:** round 8
was cut on `S49`'s finding that the cost is the work done AROUND a stale row. **It saved nine cells of wasted
remedy work by measuring 9 of 23 already dead, and its own instrument carried a narrower version of the same
defect at a cost of 2 of 23 in the cheapest bucket. That is a good trade -- and it is also exactly why the
class keeps recurring.**

## 5. Round 9 takes

1. **The liveness re-read, cut per §4** -- shared tree, or base sha printed per verdict line -- and using the
   **WINDOW** method of §3 rather than a subject grep.
2. **The 7 STILL-LIVE rows**, now measured as genuinely live (0 of 7 stale), as the remedy population.
3. **Nothing else.** ⛔ **And round 9 is NOT cut until this analysis lands** -- LD-0521, which is precisely
   what my own late analysis was holding up.

## 6. FWD coverage

**No outcome went unserved; no PRD addendum is owed.**

⭐ **One thing the round earned that no criterion graded: the cut was WIDENED TWICE BY ITS OWN GUARDS, both
correctly** -- a python precondition refused when `S53` landed mid-measurement, and `safe-commit`'s gate
refused the re-cut when `S54` landed while the gate ran. **The round grew under the CVO twice in twenty
minutes and both refusals were right.** That is the L10 precondition doing exactly what it is for, on a seat
that was not trying to get away with anything.

**L9** @`2bb57f01f8`. **This analysis is L10's one send.**
