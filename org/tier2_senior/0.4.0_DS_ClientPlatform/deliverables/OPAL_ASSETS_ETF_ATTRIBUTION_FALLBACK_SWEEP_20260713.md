# OPAL_ASSETS -- ETF attribution-fallback SWEEP: the denominator for AC11/AC12

**Author:** 0.4.0_DS_ClientPlatform
**Date:** 2026-07-13
**archetype:** TRACE
**Commissioned by:** 1.0.0_SA_CTO~B (task (b), GO 2026-07-13T22:10Z -- *"(b) MUST precede (a)"*)
**Status:** MEASURED on the full served denominator. **NO CODE CHANGED. NO RUN.**

> **CTO~B's bar, met literally:** *"Print the full list, not just the hits -- a sweep that reports only 49F is
> indistinguishable from a sweep that only looked at 49F."*

---

## 1. THE SWEEP -- FULL DENOMINATOR, NOTHING SAMPLED

```
DENOMINATOR: 427 served partitions (2024-11-01 -> 2026-07-10). ALL 427 scanned.
             117/427 carry an etf_decomposition (the ETF channel starts later than the AUA channel).
FIRM UNIVERSE: exactly 2 -- 49financial, inflection. Both present in 427/427 partitions[].
```

| firm | ever in `held_by_partner` | RPS-override (`partner_held_etf`) | **`target_weight` fallback** | VERDICT |
|---|---:|---:|---:|---|
| **49financial** | 464 | 18 | **0** | 🔴 **RPS-ONLY -- NO FALLBACK -> LANDMINE** |
| **inflection** | 124 | **0** | 124 | composition-only, no override -> **SAFE** |

**Every distinct `attribution_basis` ever served** (4 tickers x 117 partitions = 468 ticker-rows, all accounted):

| count | basis | = partitions | meaning |
|---:|---|---:|---|
| 344 | `rps_actual:49financial` | 86 | 49F via RPS; inflection not yet onboarded |
| 120 | `rps_actual:49financial;target_weight:inflection` | 30 | both firms, each on its own path |
| **4** | **`target_weight:inflection`** | **1** | 🔴 **49F GONE -- the 2026-07-10 defect** |

## 2. ANSWERS TO CTO~B's TWO BRANCHES

**"If 49F is the only one -> say so WITH THE DENOMINATOR, and AC11 is scoped to it (and the class being one row wide is itself a finding)."**

**49F IS THE ONLY ONE. The class is ONE ROW WIDE -- TODAY.** `target_weight:49financial` **appears ZERO times in 427 partitions.** 49F has *never once* had a composition fallback. **I had been assuming this from the basis string; it is now MEASURED.** *(And the basis string alone could never have proven it -- had 49F possessed composition rows, the RPS override would have replaced them and the basis would read `rps_actual:49financial` either way. **The string cannot distinguish "no fallback" from "fallback silently overridden."** The proof is the 07-10 partition itself: on the one run where the override vanished, any composition rows would have surfaced as `target_weight:49financial`. 49F appeared **nowhere**. **The defect is its own experiment.**)*

**BOUNDING THE EVENT (good news, stated plainly):** the 49F-dropped basis occurs on **exactly ONE partition (2026-07-10)** -- 4 ticker-rows, 1 run. **This is a FIRST OCCURRENCE, not a chronic condition.** The blast radius is one frozen artifact.

---

## 3. 🔴 THE FINDING THAT CHANGES THE GUARD'S SHAPE -- **THE SAFE FIRM IS SAFE *BECAUSE* IT IS ON THE LEGACY PATH**

The one-row-wide answer is true and it is **the least important thing in this document.** Look at *why* each firm lands where it does:

| firm | attribution path | survives an empty feeder? | why |
|---|---|---|---|
| **inflection** | `target_weight` **estimate** (composition x model_aua) | **YES** | it degrades to an estimate **that exists** |
| **49financial** | `rps_actual` -- **real Schwab RPS positions (PIT)** | **NO** | *"fall back to the estimate"* -> **there is no estimate** |

> ## **THE FIRM ON THE *CORRECT, MODERN* ARCHITECTURE IS THE ONE CARRYING THE LANDMINE.**
> **Inflection is safe only because it is still on the ESTIMATE path -- the exact path Andrew's PIT-snapshot
> thesis exists to RETIRE.** *(Andrew-direct: build on the Schwab-PIT-snapshot pattern; do not deepen dependence
> on the transaction engine.)*
>
> ### **=> OPAL_ASSETS' STRATEGIC DIRECTION CONVERTS SAFE FIRMS INTO LANDMINES.**
> Every firm migrated from `target_weight` to PIT/RPS attribution **loses its fallback and inherits this defect.**
> **The denominator is 1 today and it is 1 BECAUSE THE MIGRATION HAS ONLY HAPPENED ONCE.**

**This is not speculative -- three migrations are already scoped:**
- **G2** wires **08335338** (CBUGL positions) -> **more RPS/PIT-sourced attribution for 49F.**
- **Cottonwood** is on Andrew's 14-cohort map (DIVZ via `cot`) -> a **third firm**, positions-based.
- **Inflection itself** is the eventual migration target of the same thesis -> **arming the one firm that is currently safe.**

> **CONSEQUENCE FOR AC11/AC12 (this is the deliverable):**
> ### **DO NOT SCOPE THE GUARD TO 49F. SCOPE IT TO THE CLASS.**
> The guard must assert on **"any firm in the DECLARED partner set that yields no held value"** -- never on a
> hard-coded `49financial`. **A guard written for 49F would pass green for Cottonwood on the day Cottonwood
> is onboarded, and it would ship with a passing test proving it works.** *That is CTO~B's own "fails GREEN for
> every other firm in the class," and the class is scheduled to grow.*
>
> **The DECLARED side must come from the partner registry / cohort spec, NEVER from the artifact just parsed**
> -- the same `_declared_masters` vs `_observed_masters` discipline the emitter already uses (`:445-475`), and
> for the identical reason: **a guard whose two sides agree by construction cannot fail.**

---

## 4. SPEC FOR (a) -- AC11 + AC12, shaped by this denominator

**AC11 -- EXPECTED-FIRMS GUARD (`build_etf_decomposition`).**
Every firm in the **declared** partner set must resolve to a held value (from *either* path). A declared firm
that yields **nothing** must **RAISE**, not silently vanish into `residual`.
- **Falsifier = a MUTANT, never a healthy partition:** empty `partner_held` for a declared firm; **assert it RAISES.**
- **Explicitly NOT gated on G1**, and **NOT closable by "the number looks right again."**

**AC12 -- RESIDUAL DIRECTION TEST.**
`identity_2_etf_residual` currently catches only **over**-attribution (`residual < 0`). The 07-10 failure went
the **other way**. **A conservation gate tested in one direction has been tested in NO direction.**
- Assert `public_residual` cannot **JUMP** without a corresponding change in `etf_total_net_assets`
  (a `held_total` collapse with a flat numerator is the signature).
- **A fired sentinel must be able to BLOCK.** `sentinel_1` fired at **559.7% -- an 11x breach of its own 50%
  threshold** -- and is `"audit-only, non-blocking; value stored"`. **A guard that detects but cannot prevent is
  a witness, not a guard.**

**AC13 (proposed, falls out of sec 3) -- MIGRATION INVARIANT.**
**No firm may be moved onto PIT/RPS attribution until AC11 covers it.** *The migration is what arms the mine;
the guard must precede the migration, not chase it.*

---

## 5. FENCES
No code changed. No mdpf run, no sentinel, no trigger, no de-collision, no stamp. Frozen 3 untouched. Cohort 8's
`incomplete` untouched. No bd/Schwab S3. Read-only `aws s3 sync` of 427 served partitions -> scratchpad; source
reads only. No spawns, no vendor calls. Nothing implemented -- **spec only, per CTO~B.**

## 6. GROUNDING (Rule 22a)
| axis | evidence |
|---|---|
| **applied** (served) | **All 427** partitions downloaded + parsed (`s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua/`). **Denominator printed; nothing sampled.** Every `attribution_basis` shape enumerated and reconciled to 468 ticker-rows = 117 partitions x 4 tickers -- **no rows unaccounted.** |
| **desired** (source) | `mdpf_aggregate_aua.py:429-460` (the loop), `:121-125` (vintage exclusion), `:163-164` (the fallback contract) |
| **exercised** | The firm x path matrix is derived from the served bytes, not from the code's intent. `target_weight:49financial` = **0/427** is a measured absence over the full denominator, not an inference from a docstring. |
| **the forward claim is INFERRED, and labelled** | *"migration converts safe firms into landmines"* follows from Andrew's stated PIT thesis + the G2/Cottonwood scope. It is an **architectural inference, not a measurement** -- I have not observed a second firm being migrated. **It is the reason to scope the guard to the class, and it is not a finding about today's data.** |
