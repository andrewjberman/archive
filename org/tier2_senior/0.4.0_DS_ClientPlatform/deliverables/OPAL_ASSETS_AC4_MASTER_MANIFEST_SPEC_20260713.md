# AC4 / AC17 -- THE MASTER MANIFEST: the field that makes a row say **what it is OF**

**Author:** 0.4.0_DS_ClientPlatform
**Date:** 2026-07-13
**archetype:** IMPLEMENT (**spec only -- NO CODE, NO RUN**)
**For:** 1.0.0_SA_CTO~B (PRD) -- task (ii)
**Scope:** Andrew-direct: **canonical storage + robust ingestion, per figure, at its granularity.** **No sums.**

---

## 1. 🎯 THE EVIDENCE ARRIVED TONIGHT, AND IT IS A PERSON

**`1.0.0_SA_CTO` -- a Tier-1 architect, reading the SERVED artifact directly, tonight -- could not tell whether
`partner_custody_total` was ONE master or ALL masters.** He mapped it to *"TOTAL CUSTODY"* and built a
three-quantity reconciliation on it.

**It is the 0824 book. Only. MEASURED, full denominator:**
```
427 served partitions scanned (2024-11-01 -> 2026-07-10), none sampled
  49financial partner block present : 427/427
  partitions containing "08335338"  :   0/427     <-- the second master. NEVER. NOT ONCE.
```
**It CANNOT be a cross-master total: the second master has never appeared in a single served partition.**
*(Source-side: `masters:["08242234"]`, `expected_masters:["08335338"]`; `_ownership_source_masters` -> `["08242234"]`.)*
**And Andrew, sovereign: *"the 49F Smartx which is the number we are showing at ~1.62b."***

> # **THAT IS NOT CTO'S ERROR. THAT IS THE ROW FAILING TO SAY WHAT IT IS *OF*.**
> **He had the artifact open. He is the architect. He still could not tell -- because the row does not carry its
> master, and nothing else in the body does either.**
> ### **THE DEFECT WE HAVE BEEN CHASING ALL NIGHT JUST DEMONSTRATED ITSELF ON A TIER-1 AGENT, IN REAL TIME, USING THE REAL DATA.** *That is the case for AC4, and no argument I could construct would be stronger.*

## 2. WHY THE $1.7B WAS UNPRICEABLE -- **THE IDENTITY CHANNEL IS DEAD** (CTO~B's AC4, confirmed)

`coverage_state: incomplete` says ***"something is missing."*** **It can never say *"missing WHAT."***

**And it structurally cannot** -- `masters_present` is populated from `SOURCE_MASTER_MARKER_FIELDS`, and **mdpf emits
none of them: 0/427 partitions carry a master marker, top-level or nested.** The emitter documents this itself
(`lambda_function.py:94-117`) and pins it with `test_the_production_clearing_path_is_DEAD`.

> ## **THE $1.7 BILLION HOLE WAS NOT HIDDEN. IT WAS DISCLOSED -- MACHINE-READABLY, ON EVERY ROW, FOR 427 PARTITIONS -- AND THE DISCLOSURE COULD NOT SAY WHAT IT WAS *OF*.**
> **A reader who could see `masters_expected:[0824, 0833]` / `masters_present:[0824]` could go price `0833` in an
> afternoon.** **Nobody could, for 427 days.** *An unquantifiable disclosure is not a weak signal -- it is an
> INVISIBLE one, and it reads like a footnote.*

**THIS IS ALSO AC17, AND THAT CONVERGENCE IS THE PROOF THE RE-CUT WAS RIGHT.** I had written *"a disclosure must
carry a MAGNITUDE"* -- **that was the sum smuggled back into storage** (Andrew: *a total is not a primitive*).
**The correct fix is not to make the boolean carry a number. It is to make the ROW SAY WHAT IT IS OF -- and let the
reader compute the magnitude.** **Two findings. One field.**

---

## 3. THE SPEC -- **AC4: THE MASTER MANIFEST (a PRODUCER requirement on mdpf)**

**(a) EVERY partner block emits `source_masters`** -- the list of custody masters **actually represented** in that
block's dollars. `49financial` -> `["08242234"]` today; `["08242234","08335338"]` when G2 lands.
*(This is the `SOURCE_MASTER_MARKER_FIELDS` channel the emitter already reads and which is **never written**. The
consumer side EXISTS. Only the producer is missing.)*

**(b) EVERY figure row carries its OWN identity** -- **which figure, which master(s)/account, and its state**
(`fresh | rolled_forward | incomplete | missing`). **Never silence. Never a bare boolean.**

**(c) THE DECLARED SIDE COMES FROM THE REGISTRY, THE OBSERVED SIDE FROM THE ARTIFACT** -- and **they must be derived
independently.** *A guard whose two sides agree by construction cannot fail* (`:445-475` already enforces this;
`:694-706` documents the exact trap: deriving `expected` from `present` makes `incomplete` **unreachable** and the
undercount **silently vanishes**).

**(d) 🔴 `incomplete` MUST BECOME CLEARABLE -- BY THE PRODUCER, NEVER BY THE FLAG.**
> **TODAY IT IS STRUCTURALLY UNCLEARABLE.** When 0833's data lands, **the state will NOT clear on its own**, because
> `masters_present` can only ever observe `08335338` **through a marker that is never written.**
> ### **THE LAUNDERING PATH, AND IT IS THE MOST LIKELY WAY THIS DEFECT DIES:** the next agent sees a
> **permanently-red `incomplete` AFTER the data has demonstrably landed**, concludes **the flag is broken**, and
> **hard-wires it to `fresh`** -- erasing the exact undercount the flag exists to disclose. **They will be doing
> careful, reasonable, well-intentioned work.**
> ## **FIX THE PRODUCER. NEVER THE DISCLOSURE.** **A permanently-red flag is a PRODUCER BUG, not a FLAG BUG -- and
> the two are indistinguishable from the flag's side.**

**FALSIFIER -- A MUTANT, NEVER A HEALTHY PARTITION:**
```
feed a body whose 49F block carries dollars from BOTH masters, with the marker ABSENT
  -> ASSERT the row reads `incomplete` (i.e. absence of the marker is NOT read as absence of the master)
feed a body carrying the marker for BOTH masters
  -> ASSERT the row CLEARS to `complete`   <-- THE CLEARING PATH MUST BE EXERCISED, not assumed
```
**The second assertion is the one that matters: a state that has never been observed to CLEAR has never been tested.**
*`test_the_production_clearing_path_is_DEAD` currently pins that it CANNOT clear. That test must INVERT when AC4 lands
-- and if it does not invert, AC4 is not done.*

---

## 4. WHAT THIS BUYS, STATED WITHOUT A SINGLE SUM

- **A row that says what it is OF.** `0824` / `0833` / model-sleeve become **distinguishable by FIELD**, not by
  reading a name and guessing. *Three figures tonight were confused with each other by four different agents,
  including two Tier-1s and me. **Every one of those confusions is a field lookup once AC4 lands.***
- **The overlap question becomes a QUERY.** *"Do 0824 and 0833 share accounts?"* -- **answerable from the store, by
  whoever needs the answer, at read time.** **It stops being a design decision, and it can never again block an
  ingestion.** *(I wrongly framed it as a gate on 0.6.2's ETL; AC4 is what makes that framing permanently
  unnecessary.)*
- **The undercount becomes PRICEABLE BY THE READER** -- **without the STORE ever asserting a total.** *Exactly
  Andrew's ruling: record the components; summing is presentation.*

## 5. ⛔ FENCES
**No code. No mdpf run. No sentinel. No trigger.** Frozen 3 untouched. **cohort-8's `incomplete` untouched -- and
this spec is the reason it must STAY red until the producer is fixed.**
**No combined totals, no magnitudes, no disjointness analysis** (out of scope, ruled twice).
**AC4 is a PRODUCER change to mdpf and CANNOT be exercised while the chain is HELD. Do NOT run mdpf to test it.**
It lands, with its mutants, **when the hold lifts, in the normal order.**
