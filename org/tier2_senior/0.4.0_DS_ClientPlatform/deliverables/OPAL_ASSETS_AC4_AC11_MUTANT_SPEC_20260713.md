# AC4 / AC11 -- THE MUTANTS. The falsifiers that decide whether the guards are real.

**Author:** 0.4.0_DS_ClientPlatform
**Date:** 2026-07-13
**archetype:** IMPLEMENT (**spec only -- NO CODE, NO RUN**)
**For:** 1.0.0_SA_CTO~B (PRD)
**Scope:** Andrew-direct -- **robust ingestion.** No sums, no magnitudes, **no derivation of the 49F bucket
relationship** (CTO~B has ORDERED that stop; it is not mine to re-open).

---

## 0. WHY THIS DOCUMENT EXISTS

**Every guard we specced tonight can be written, landed, marked DONE, and be completely inert.** That is not a
hypothetical -- **it is the estate's actual track record, six times over in one night:**

```
sentinel_1 DoD          fires at 559.7%   -> "audit-only, non-blocking"
identity_2              tests conservation -> only in the direction that did not fail
source_vintage          reports freshness  -> the dead feeder is EXCLUDED from it
etf_probe staleness_days stamps honesty     -> dropped at the parquet boundary
netassets feeder        rolls forward      -> no ceiling; prints OK
probe S3 upload         delivers           -> bare except -> exit 0
```

> ## **A GUARD IS NOT REAL UNTIL SOMETHING HAS SEEN IT FAIL.**
> **`test_the_production_clearing_path_is_DEAD` is the proof this estate already knows that** -- it is a test whose
> entire job is to PIN that a state cannot clear. **The mutants below are the same instinct, aimed forward.**

---

## 1. 🔴 THE MUTANT SET MUST BE **GENERATED FROM THE REGISTRY**, NOT HAND-WRITTEN

**This is the most important clause in the document and it is not obvious.**

**AC11 requires the guard to be FIRM-GENERIC (no firm id in the code).** But:

> ### **A GUARD CAN BE FIRM-GENERIC IN THE *CODE* AND TESTED ON ONLY *ONE FIRM* -- AND THEN NOBODY NOTICES WHEN IT SILENTLY REGRESSES TO FIRM-SPECIFIC.**
> A hand-written `test_49financial_absent_raises` **passes identically** whether the guard is generic or
> hard-coded to `49financial`. **It cannot distinguish them. It measures the AUTHOR, not the INSTRUMENT.**

**=> THE MUTANT MUST BE PARAMETRIZED OVER THE DECLARED CONTRIBUTOR SET, READ FROM THE REGISTRY AT TEST TIME.**

```
for contributor in DECLARED_SET (from the registry -- NOT a literal list in the test):
    mutate: remove that contributor's measured source
    assert: RAISES
```
> **Then on the day Cottonwood is added to the registry, THE MUTANT SET GROWS BY ITSELF, and a guard that quietly
> only handles 49F FAILS THE DAY COTTONWOOD IS DECLARED -- which is exactly one day before it would have mattered.**
> ## **THAT IS AC14 (the migration invariant) ENFORCED BY THE TEST SUITE INSTEAD OF BY A HUMAN REMEMBERING.**
> *A migration invariant that relies on someone reading the PRD is not an invariant. This one fails a build.*

---

## 2. MUTANT A -- **AC11: THE COMPLEMENT MUST NOT ABSORB AN ABSENT CONTRIBUTOR**

**TARGET:** `mdpf_aggregate_aua.build_etf_decomposition` (`:429-460`), and **any** `remainder = total - sum(parts)`.

```
GIVEN   a body where a DECLARED contributor has NO measured source
        (and -- the load-bearing case -- NO intent/target_weight fallback either)
MUTATE  drop that contributor from the measured input
ASSERT  1. it RAISES.
        2. the raise NAMES THE MISSING CONTRIBUTOR.
        3. `public_residual` does NOT move by that contributor's value.
```

**(2) IS NOT PEDANTRY.** *A bare `assert raises` passes when the code dies of an unrelated `KeyError` -- **a test
that accepts any exception is testing that the code is fragile, not that the guard works.*** **The raise must be the
guard's raise, and it must say who is missing.**

**(3) IS THE ACTUAL DEFECT.** *The $528mm did not appear as an error. It appeared as a beautifully-formed number.*
**Asserting only "it raises" leaves the door open to a future refactor that catches the raise, logs a WARN, and
serves -- which is EXACTLY what `sentinel_1` already does today.** **Assert the RESIDUAL DID NOT MOVE.**

**NEGATIVE CONTROL (generated, not hand-picked):** the **unmutated** body must **NOT** raise, and must reproduce the
served `public_residual` **exactly**. *Without it, a guard that raises unconditionally passes the mutant and is
worthless -- and it would look like our most reliable test.*

---

## 3. MUTANT B -- **AC4: THE CLEARING PATH MUST BE EXERCISED**

**TARGET:** the `masters_present` / `coverage_state` channel.

```
B1  GIVEN a body whose 49F block carries dollars from BOTH masters, MARKER ABSENT
    ASSERT coverage_state == "incomplete"
    (absence of the MARKER is not evidence of absence of the MASTER -- today it is treated as such)

B2  GIVEN a body carrying the master marker for BOTH masters
    ASSERT coverage_state CLEARS to "complete"        <-- THE ONE THAT MATTERS
```

> # **B2 IS THE WHOLE POINT. A STATE THAT HAS NEVER BEEN OBSERVED TO CLEAR HAS NEVER BEEN TESTED.**
> **Today `incomplete` is STRUCTURALLY UNCLEARABLE** (`masters_present` can only be populated from a marker mdpf
> never writes: **0/427**). **So the state is permanently red -- and a permanently-red flag is INDISTINGUISHABLE, FROM
> THE FLAG'S SIDE, FROM A BROKEN FLAG.**
> ### **`test_the_production_clearing_path_is_DEAD` MUST *INVERT* WHEN AC4 LANDS. IF IT DOES NOT INVERT, AC4 IS NOT DONE.**
> *That test is currently a canary pinning the deadness. **It is the acceptance criterion, already written, waiting.***

**⛔ AND THE LAUNDERING PATH THIS MUTANT EXISTS TO BLOCK:** after 0833's data lands, the next agent sees a **red flag
on data that has demonstrably arrived**, concludes **the flag is broken**, and **hard-wires it to `fresh`.** **They
will be doing careful, reasonable work, and they will erase the only disclosure of the undercount.**
**B2 is what makes "the flag is broken" a FALSIFIABLE claim instead of a plausible one.**

---

## 4. MUTANT C -- **AC12: THE GATE MUST FAIL IN THE DIRECTION IT ACTUALLY FAILED**

```
GIVEN   held_total collapses while etf_total_net_assets is FLAT
ASSERT  the gate FAILS  (and BLOCKS -- the partition is not written)
```
**`identity_2` today tests `residual < 0` (over-attribution). The failure went the OTHER way and it read `PASS`.**
> ## **A CONSERVATION GATE TESTED IN ONE DIRECTION HAS BEEN TESTED IN NO DIRECTION** -- *the failure always arrives
> from the side you did not point it at.*
**AND ASSERT IT BLOCKS, NOT MERELY THAT IT FIRES.** *`sentinel_1` fired at **11x its own threshold** and served the
partition anyway.* **"Fires" and "blocks" are different assertions, and only one of them is a control.**

---

## 5. THE RULE THAT BINDS ALL FOUR

> # **THE FALSIFIER IS A MUTANT. NEVER AN OBSERVATION OF A HEALTHY PARTITION.**
> **"The number looks right again" is NOT evidence a guard works** -- it is evidence the TRIGGER is quiet.
> **Fixing the feeder makes the $528mm silently correct itself while the landmine stays armed. THE EVIDENCE OF THE
> DEFECT IS DESTROYED BY THE REPAIR OF ITS TRIGGER.**
> **NONE of these guards may be closed on a green production number.** *(`0.5.0_AE_OpalETL` has ACK'd agent-side that
> his feeder repair will not be cited as closing LD-0292. That ACK is a control; the ledger entry is not.)*

## 6. ⛔ FENCES
**No code. No mdpf run. No sentinel. No trigger.** **These mutants CANNOT be exercised against production while the
chain is HELD -- and they do not need to be: THEY RUN AGAINST A CONSTRUCTED BODY, IN A TEST, WITH NO PIPELINE
INVOLVED.** *That is a feature, not a limitation: **a guard whose falsifier requires a production run is a guard that
will never be falsified.*** They land with the code, when the hold lifts, in the normal order.

**And I am NOT deriving the relationship between the 49F buckets** -- ordered stopped by CTO~B, ruled out of scope by
Andrew three times. **Nothing in this document needs it.** *(Which is, itself, the test from §000: **if a design is
invariant to a question, that question does not need answering.**)*
