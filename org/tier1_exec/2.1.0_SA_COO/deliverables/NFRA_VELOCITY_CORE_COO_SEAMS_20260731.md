# NFRA_VELOCITY_CORE -- COO SEAMS STATEMENT

**For:** Andrew's integration-point review of C1 / C2 / C3 / C7 / C8 + the ESTATE work.
**From:** `2.1.0_SA_COO`. **Date:** 2026-07-31.
**Scope:** seams visible only from the decomposition vantage. Eight seams are already on the joint list
(MSTR~Z's five, CVO~Z's S-A/S-B/S-C). **Nothing here re-derives those.**

---

## Why the COO sees a different layer

I wrote all six remaining TOs from one PRD. That makes one layer visible that no single workstream owner
looks at: **the layer between the PRD's acceptance text and the TOs that bind seats to it.** Every seam
below lives there. None is a defect in a workstream's work.

---

## S-COO-1 -- ACCEPTANCE TEXT WAS INHERITED, NEVER VALIDATED. THE LAYER HAS NO OWNER.

**This is the one I would put first, and it is my defect twice over.**

The PRD states acceptance per workstream. I copied that text into binding TO acceptance criteria. **Nobody
validated the acceptance text itself before it became binding on a seat.** Two live consequences, both
found by seats trying to satisfy the criteria rather than by anyone reviewing them:

| Workstream | Criterion | Defect |
|---|---|---|
| **WS-C7** | *"each specimen re-derives as a `Class 1` or `Class 2` failure"* | **The term has NO REFERENT.** Resolves nowhere in the estate. `~Z` could not write a specimen classification under any ruling; it shipped SPEC-4 with the field deliberately absent and the reason stated in-file. |
| **WS-C8** | *"doctrine byte-count FALLS"* | **The term has a referent and it is the WRONG QUANTITY.** `~C` measured the dedup pass at **+3910 B** -- the operation whose purpose is removing duplication increases the number. Doctrine's real cost is *places an agent must read and reconcile*, which artifact 2 reduced by three. |

**The shared shape: an acceptance criterion is a CONTRACT ON A SEAT, and it was authored with less scrutiny
than the work it governs.** A criterion with no referent cannot be satisfied; a criterion measuring the
wrong quantity **penalises the correct operation**. Both passed PRD review, TO authoring, and a gate.

**Worse, in a way that matters for this review:** I used *"byte-count has not fallen"* as the load-bearing
evidence in my own assessment that WS-C8 was **running backwards against its own acceptance**. That reading
was produced by the defective criterion. **An inverted criterion does not merely fail to measure -- it
manufactures findings about the seat.**

**What I am NOT proposing:** that I fix them. I authored the defect; the repair is CVO~Z's (PRD) and
CTO~Z's (gate). A replacement for the C8 criterion is with them.

---

## S-COO-2 -- TWO OF MY OWN TOs NAME A GATE THAT MAY NEVER OPEN

`WS-C5` and `WS-C6` both carry: *"opens when WS-C7's N-of-M migration reports a migrated N."*

**If C7 closes with limb 2 deferred -- which is live and reasonable on A11.1 grounds -- that gate never
opens, and both TOs wait forever on a condition that will not occur.**

> **A gate that never opens is INVISIBLE rather than wrong.** A wrong gate fires and is caught. A gate whose
> precondition is quietly abandoned upstream produces two seats that look correctly-blocked indefinitely,
> and nothing reports it.

This is the same class as the stale pointer `~Z` caught in my WS-C4 TO (it named "pre-flight" after the
artifact was renamed `WSC7_RUN_BOUNDARY_CHECK.md`) -- **but that one failed loudly on a name lookup. This one
would not fail at all.**

**Only visible from the decomposition vantage**, because it requires holding C7's deferral decision and
C5/C6's gating text at the same time. Neither owner sees both.

---

## S-COO-3 -- C8 CANNOT CLOSE THROUGH THE ROUTE ITS OWN PRD SPECIFIES

CTO~Z adjudicated **M15 ADMISSIBLE on merit** (two fresh instances today, two seats, neither self-caught,
none matching a documented MSYS shape) -- **and correctly did not close the clause.** The PRD routes M15
admission *through the WS-C9 gate*. **The pause seals C9.**

- Admission requires a sealed gate.
- Rejection is unavailable on the merits.
- **Rejecting it to close C8 would be adjudicating from the desired outcome.**

**This is a deadlock created by the pause itself, not by anyone's work.** It matters operationally because
**"finish C8, then stop" has no defined stopping point while one clause has no available route and another
measures the wrong quantity.** The gate's own terminating condition is undefined.

---

## S-COO-4 -- THE TYPE SYSTEM IS INERT ON TWO INDEPENDENT AXES AT ONCE

Individually each is known; **the compounding is only visible holding all the TOs:**

| Axis | State | Owner |
|---|---|---|
| **VALUES** cannot be populated | Lifecycle values gated on the Kimi user-input pipeline (Andrew-direct) | `0.7.0_AE_CloudOps~B`, future |
| **CLASSIFICATION** cannot evolve | New error classes enter via the WS-C9 inference gate | C9, **sealed by the pause** |

So the vocabulary is complete, **the values are unobtainable, and the mechanism for admitting new classes is
sealed.** A type system that can neither be populated nor extended is not wrong -- but it is **fully inert**,
and every downstream workstream (C5's aggregate, C6's routing) consumes declarations that cannot exist yet.

**Not an argument against either gate.** Both are deliberate and I am not asking for either to lift. It is a
statement that **the review is happening at the moment of maximum inertness**, which is the right moment to
look at seams and the wrong moment to judge the system by what it currently produces.

---

## S-COO-5 -- ONE ARTIFACT GATES THE PROGRAM'S ENTIRE BACK HALF, AND ITS CONSTRUCTION IS CONTESTED

```
WS-C7 N-of-M migration  ->  WS-C5 (L2 has nothing to aggregate)
                        ->  WS-C6 (routing binds to VERIFIED coverage declarations)
WS-C7 run-boundary chk  ->  WS-C4 (PRD makes it a C4 dependency)
WS-C8 MECHANISM_LAWS +
WS-C5 L3 gate           ->  WS-C9
```

**Three of the four unstarted workstreams gate behind specific WS-C7 artifacts -- not behind "P2 being
done."** MSTR~Z has the dependency on the joint list; **what I add is that the gating artifact is the one
under active dispute.** The migration is deferred on A11.1 grounds: *after migrating ~90 tools onto the
boundary contract, the discrimination question becomes unanswerable, because every tool passes and passing
looks like evidence.*

**And the number that makes it sharp: discrimination is currently proven at 1 of 9 canonical specimens.**
So the program's back half is gated on an artifact that should not be built until a suite that is 1/9 done
is finished -- and both facts are correct simultaneously.

*(`~Z` corrected my figures here twice, both against their own interest: limb 2 is `N=0, M=69` with the
denominator **delivered** at `@551c54b07`, not "no artifact"; limb 3 is **1 of 9 canonical**, not the "3 of
9" I had been quoting. Their numbers govern.)*

---

## What I consume and expose

**CONSUMES:** the PRD's phase structure and per-workstream acceptance text; CTO~Z's gate rulings; each
seat's landed artifacts and their own numbers.
**EXPOSES:** six TOs (two active, four staged); the dependency graph between workstreams; the sequencing
findings above.

**The exposure that is load-bearing for this review: the dependency graph in my TOs is only as sound as the
acceptance text I inherited.** S-COO-1 and S-COO-2 are the same defect at two altitudes -- criteria I did not
validate, and gates I wrote from them.

---

## Recommendation

**One item is worth acting on before the review rather than during it:** S-COO-3 means the pause has no
defined stopping point. **"Finish C8, then stop" cannot be evaluated until clause 1 measures the right
quantity and clause 4 has a route.** Everything else here is material for the review and needs no action.
