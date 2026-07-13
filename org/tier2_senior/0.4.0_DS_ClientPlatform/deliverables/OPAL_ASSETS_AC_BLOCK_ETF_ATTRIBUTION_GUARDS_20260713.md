# OPAL_ASSETS -- AC BLOCK: the ETF attribution guards (AC11 / AC12 / AC14 + two proposed)

**Author:** 0.4.0_DS_ClientPlatform
**Date:** 2026-07-13
**archetype:** IMPLEMENT (spec only -- **NO CODE**)
**For:** 1.0.0_SA_CTO~B -> PRD v0.6
**Numbering:** per CTO~B (AC13 = Andrew's `presentation_case`; my migration invariant renumbered **AC13 -> AC14**).
**Fences:** no mdpf run, no sentinel, no trigger. Nothing implemented.

---

## THE ONE-PARAGRAPH WHY

On 2026-07-10, `49financial` **vanished** from mdpf's `etf_decomposition.held_by_partner` and **~$528mm of its ETF
holdings were silently reclassified as public float.** The mechanism (`mdpf_aggregate_aua.py:429-460`): 49F's ETF
attribution rests on the **RPS override alone** -- it has **no `target_weight` composition rows** (`0/427` partitions,
measured). An **absent** feeder falls back to *"the estimate"*; **there is no estimate to fall back to**; the firm
drops out of the loop; `residual = total - held_sum` **absorbs the lot**. **Both guards saw it. Neither stopped it.**

> **THE GRACEFUL-DEGRADATION PATH ASSUMES EVERY FIRM HAS AN ESTIMATE TO FALL BACK TO. 49F DOES NOT.**
> *A fallback is only safe if the thing you fall back TO exists.*

---

## AC11 -- EXPECTED-FIRMS GUARD (**scoped to the CLASS, never to a firm id**)

**REQUIREMENT.** In `build_etf_decomposition`, **every firm in the DECLARED partner set must resolve to a held value
from *some* path.** A declared firm that yields **no value** must **RAISE**, not vanish into `residual`.

**THE DECLARED SIDE MUST COME FROM THE PARTNER REGISTRY / COHORT SPEC -- NEVER FROM THE ARTIFACT JUST PARSED.**
Same `_declared_masters` vs `_observed_masters` discipline the emitter already enforces (`lambda_function.py:445-475`),
for the identical reason: **a guard whose two sides agree by construction cannot fail.** The natural-looking
`expected = whatever_we_read` makes the guard **ornamental**.

**⛔ DO NOT HARD-CODE `49financial`.** The sweep says the class is one row wide **today** -- and it is one row wide
**because the migration has only happened once** (see AC14). **A guard written for 49F passes GREEN for Cottonwood on
the day Cottonwood lands, and ships with a passing test proving it works.**

**FALSIFIER -- A MUTANT, NEVER A HEALTHY PARTITION.**
```
empty `partner_held` for a DECLARED firm that has no composition rows  ->  ASSERT IT RAISES
```
**Explicitly NOT gated on G1. Explicitly NOT closable by "the number looks right again."**

> ### **WHY THAT LAST CLAUSE IS THE WHOLE AC:**
> **Fix the feeder and the $528mm silently corrects itself while the landmine stays armed.** The feeder refills, 49F
> reappears, `public_residual` drops back, **every number looks right, and nobody learns the estate cannot survive
> that feeder blinking.** **THE EVIDENCE OF THE DEFECT IS DESTROYED BY THE REPAIR OF ITS TRIGGER.** It fires again on
> the next blip -- **and next time the move will be small enough that no 559.7% sentinel notices.** *We caught this
> one only because the drop was enormous.*
> **A defect whose symptom is cured by fixing its trigger is the easiest kind to close prematurely -- and this one
> would then be invisible AND believed-fixed.** *(0.5.0_AE_OpalETL, who owns the feeder repair, has ACK'd
> agent-side that he will not let his work be cited as closing this.)*

---

## AC12 -- RESIDUAL **DIRECTION** TEST + **A FIRED SENTINEL MUST BE ABLE TO BLOCK**

**THE DEFECT IN THE CURRENT GATES** (quoting the **SERVED** `reconciliation` block -- *the artifact confesses in
writing and ships*):
```
sentinel_1_cohort0_dod  : "day-over-day move 559.7% > 50% threshold ... WARN: audit-only, non-blocking; value stored"
identity_2_etf_residual : "PASS" ... "the gate catches over-attribution (<0), not under-attribution"
overall                 : "PASS"
```
- **`sentinel_1` fired at an 11x breach of its own threshold and could not stop anything.** *A guard that DETECTS but
  cannot PREVENT is not a guard; it is a witness.*
- **`identity_2` is worse than non-blocking -- it is DIRECTIONAL.** It tests `residual < 0` (over-attribution). **The
  failure went the one way it cannot see.** **A CONSERVATION GATE TESTED IN ONE DIRECTION HAS BEEN TESTED IN NO
  DIRECTION** -- the failure will always arrive from the side you did not point it at.

**REQUIREMENT.**
1. **`public_residual` may not JUMP while `etf_total_net_assets` is flat.** *A `held_total` collapse under a flat
   numerator is the signature of this exact bug.* Assert on the **pair**, not on either alone.
2. **`sentinel_1` becomes BLOCKING** at its own declared threshold. If a 50% DoD threshold is too tight to block on,
   **then raise the threshold deliberately and say why** -- do not leave a screaming guard wired to nothing.
3. **Any gate written as a conservation identity must be tested in BOTH directions**, and the test must state which
   direction each assertion covers.

---

## AC14 -- MIGRATION INVARIANT *(was AC13; renumbered per CTO~B)*

> ## **NO FIRM MAY BE MOVED ONTO PIT/RPS ATTRIBUTION UNTIL AC11 COVERS IT.**
> ### **THE MIGRATION IS WHAT ARMS THE MINE. THE GUARD MUST PRECEDE THE MIGRATION, NOT CHASE IT.**

**THE MEASUREMENT THAT FORCES THIS** (427/427 partitions, denominator printed, nothing sampled):

| firm | attribution path | survives an empty feeder? | why |
|---|---|---|---|
| **inflection** | `target_weight` **ESTIMATE** | **YES** | degrades to an estimate **that exists** |
| **49financial** | `rps_actual` -- real Schwab **PIT** positions | **NO** | *"fall back to the estimate"* -> **there is none** |

> **THE FIRM ON THE CORRECT, MODERN ARCHITECTURE IS THE ONE CARRYING THE LANDMINE.** Inflection is safe **only**
> because it is still on the **legacy estimate path** -- *the exact path Andrew's PIT-snapshot thesis exists to
> RETIRE.*
> ### **=> OPAL_ASSETS' OWN STRATEGIC DIRECTION CONVERTS SAFE FIRMS INTO LANDMINES.**

**Three migrations are already scoped, and each one arms a row:** **G2** (49F -> 08335338 CBUGL) · **Cottonwood**
(on Andrew's 14-cohort map; CTO wants it first-class) · **Inflection itself** (the eventual target of the same thesis
-- *arming the one firm that is currently safe*).

**Without AC14, AC11 is a fix for a historical incident. With it, AC11 is a PRECONDITION ON THE PROJECT'S CENTRAL
ARCHITECTURAL MOVE.**

**LABELLED HONESTLY:** *"migration converts safe firms into landmines"* is an **architectural inference** from
Andrew's stated thesis + the G2/Cottonwood scope. **It is NOT a measurement. I have not observed a second migration.**
It is the reason to scope the guard to the class -- **and nothing more.**

---

## AC15 (PROPOSED) -- **VINTAGE MUST TRAVEL WITH THE COMPONENT** *(COO's catch, folded in)*

Andrew's component-grain ruling makes the ETF components **first-class and daily** -- **on a channel that is absent
10 of 28 trading days and whose consumer fabricates continuity.**

> **THE RULING RAISES THE STAKES ON THAT CHANNEL. IT DOES NOT FIX IT.**
> ### **A COMPONENT-GRAIN STORE THAT RECORDS VALUES BUT NOT THEIR VINTAGE REPRODUCES THIS EXACT BUG WITH MORE ROWS.**

**REQUIREMENT.** `data_as_of` + `staleness_trading_days` (**NEVER#1 -- trading days, never wall-clock**) + an
`inferred`/`rolled_forward` flag must be carried **THROUGH** to every component row -- **not just to the cohort.**
**And a component whose inputs disagree in vintage must carry `vintage_mixed` and be NON-QUOTABLE BY CONSTRUCTION.**

**THE GROUNDING FOR THAT LAST CLAUSE, AND IT COST ME A PUBLISHED NUMBER:**
`public_residual = net_assets - held` is **a subtraction across two vintages**, and **there is NO clean partition:**
07-08 has correct attribution + **6-trading-day-stale** net assets; 07-10 has the freshest net assets + **49F
dropped**. **A DIFFERENCE BETWEEN TWO NUMBERS TAKEN AT DIFFERENT VINTAGES IS NOT A MEASUREMENT OF ANYTHING.**
**I published `~$95mm` off exactly this and withdrew it** (`e95d8730a`). **The rule must live in the ARTIFACT, not in
an analyst's vigilance** -- *the tell (net assets byte-identical across two trading days) was in a table I wrote
myself, and I read it as corroboration.*

---

## AC16 (PROPOSED) -- **PRODUCED IS NOT DELIVERED** *(0.5.0_AE_OpalETL's find, folded in)*

`etf_probe.py:948-953` -- **the S3 upload is wrapped in a bare `except Exception` -> WARN -> `exit 0`.**

> ### **THE PRODUCER CAN SUCCEED AT PRODUCING AND FAIL AT DELIVERING, AND REPORT SUCCESS.**
> The exit code faithfully reports the worst **source** tier and is **structurally blind to whether the data ever
> left the machine.** *This is the same organ as the `aws` shim hang that reported a successful `s3 cp` while S3 kept
> the old artifact -- **an upload-verify gate that exists on one call site is not a control.***

**REQUIREMENT.** A delivery failure is a **NON-ZERO EXIT**. Verify the landed object (**`head-object` / byte count**),
**never `rc=0`**. **`exit 0` must mean "the bytes are in S3," not "I did not crash while trying."**

---

## THE COMMON ORGAN IN ALL SIX INSTANCES (the reason this is one AC block and not six tickets)

| # | instrument | what it does | why it cannot fire |
|---|---|---|---|
| 1 | `sentinel_1` DoD | fires at **559.7%** | **"audit-only, non-blocking"** |
| 2 | `identity_2` | tests conservation | **only in the direction that did not fail** |
| 3 | `source_vintage` | reports feeder freshness | **`partner_held_etf` EXCLUDED from `vintage_bearing_feeders`** |
| 4 | `etf_probe` `staleness_days` | stamps honesty | **dropped at the parquet boundary** |
| 5 | netassets feeder | rolls forward | **no ceiling; prints `OK: all 4 Opal ETFs present`** |
| 6 | probe S3 upload | delivers | **bare `except` -> `exit 0`** |

> # **EVERY DISCLOSURE IN THIS ESTATE WAS WRITTEN BY SOMEONE WHO COULD SEE THE DEFECT, AND IS READ BY NOBODY.**
> **Instrument #3 is the subtlest and it deserves its own sentence: `partner_held_etf` was excluded from the
> freshness computation for a GOOD reason** (it rolls RPS ~3d by contract; including it would read `BEHIND`
> permanently). **THE COST OF SUPPRESSING A NUISANCE SIGNAL IS THAT THE SAME SIGNAL'S CATASTROPHIC VALUE IS
> SUPPRESSED WITH IT.** *A field excluded from the freshness computation cannot distinguish "rolled forward 3 days by
> design" from "GONE ENTIRELY."*

---

## CANONICAL COUNT (reconciled with CTO~B -- **do not quote the other one**)

**10 of 28 NYSE trading days missing.** Blackout = **5 CONTIGUOUS trading days** (07-01, 07-02, 07-06, 07-07, 07-08).
**The 11/29 figure counted 2026-07-03 -- Independence Day observed -- as a trading day.** *One mis-classified holiday
moves numerator and denominator together.* **QUOTE THE FRACTION, NOT THE PERCENTAGE.**

## ⛔ AND THE FENCE ON THIS ENTIRE DOCUMENT

**Every guard above is specced against a FROZEN artifact and NONE of them can be exercised without an mdpf run.**
**mdpf is event-driven on the INF spine sentinel and is CORRECTLY IDLE under the hold.** **Do NOT run mdpf to test
these guards.** They land, with their mutant falsifiers, **when the hold lifts, in the normal order.**
**A KNOWN-WRONG FROZEN NUMBER IS STRICTLY SAFER THAN AN UNHELD PIPELINE.**
