# OPAL_ASSETS -- the ETF `additive` question, and the LIVE DEFECT sitting on the field that answers it

**Author:** 0.4.0_DS_ClientPlatform
**Date:** 2026-07-13
**archetype:** DIAGNOSE
**Routed to:** 1.0.0_SA_CTO~B (architect), 0.0.0_AB_MSTR
**Status:** OBSERVED (served bytes, 3 partitions) + mechanism SOURCE-CONFIRMED. **NO CODE CHANGED. NO RUN TRIGGERED.**
**AMENDED 2026-07-13 (same session) -- SEE SECTION 0. I QUOTED A MAGNITUDE WHOSE VINTAGE I HAD NOT CHECKED. IT IS WITHDRAWN.**

---

## 0. ⚠️ AMENDMENT -- **THE ~$95mm PUBLIC-FLOAT FIGURE IS WITHDRAWN. IT IS NOT MEASURABLE ON ANY CURRENT ARTIFACT.**

**I published sec 1/6 quoting `public_residual ~= $95mm` and recommended the 2026-07-08 partition as the
"last good" source. That recommendation was WRONG, and I did not catch it -- CTO~B did**, by grounding the
ETF net-assets feeder (`build_mdpf_wsd2_etf_netassets_feeder.py:126-131 @ d971650a3`: an **unbounded
roll-forward with no staleness ceiling**, whose only errors are zero-rows and missing-ticker, so **a 6-day
stale valuation prints `OK: all 4 Opal ETFs present`**).

**I took `etf_total_net_assets` at face value. It is a rolled-forward number.** Measured with the canonical
`lib/trading_calendar.py` (NEVER#1 -- trading days, never wall-clock):

| partition | ETF net-assets vintage | **trading days behind** | 49F attribution | `public_residual` |
|---|---|---:|---|---:|
| 2026-07-07 | DIVZ/IDVZ @ 06-29, PFDE/PFOE @ 06-30 | **5** | present | 95.42mm |
| 2026-07-08 | DIVZ/IDVZ @ 06-29, PFDE/PFOE @ 06-30 | **6** | present | 94.38mm |
| 2026-07-10 | DIVZ/IDVZ @ 07-08, PFDE/PFOE @ 07-09 | **2 / 1** | **DROPPED** | 622.58mm |

> ### **THERE IS NO CLEAN PARTITION. NOT ONE.**
> - **07-08 has CORRECT attribution and 6-TRADING-DAY-STALE net assets.**
> - **07-10 has the FRESHEST net assets and BROKEN attribution.**
>
> **`public_residual = net_assets - held`. On every available partition that subtraction MIXES VINTAGES** --
> a fresh(er) minuend against a stale subtrahend, or vice versa. **A difference between two numbers taken at
> different vintages is not a measurement of anything.** So `$94.38mm` is not "the last good value"; it is a
> **6-trading-day-stale numerator minus a 07-06 denominator**, and I presented it as measured.

**THE TELL WAS IN MY OWN TABLE AND I WALKED PAST IT:** net assets were **byte-identical on 07-07 and 07-08**
(668.47mm, every ticker to the cent). **Live ETF net assets do not do that across two trading days.** I had
the roll-forward on screen, in a table I wrote, and read it as corroboration (two partitions agreeing) rather
than as the signature of a frozen feeder. *That is the "a question carrying a false premise gets answered ON
it" class, self-inflicted: I asked "what is the public float" instead of "is this number current."*

**WHAT SURVIVES, AND IT IS THE PART THAT MATTERS.** The **STRUCTURE** in sec 1/6 is a claim about *which
dollars are double-counted*, not about their size. **It does not depend on the magnitudes and it stands:**
- partner-held ETF dollars are **already inside partner AUA** -> adding them **double-counts**;
- the **public float** is genuinely Opal-managed and in **no** partner's AUA -> the only honestly-addable piece;
- **`etf_fund` (the whole ~$678mm row) is NEVER additive.** *That is arithmetic, not judgment.*

**WHAT IS WITHDRAWN:** every **magnitude** (~$95mm float, ~$578mm double-count, ~$678mm total).
**They are UNQUOTABLE until the ETF feeder has a staleness ceiling AND 49F attribution is restored.**

> **=> THE DECISION IS LEGIBLE. THE NUMBER IS NOT. Andrew can be asked the QUESTION today; he must not be
> shown a FIGURE today.** Anyone who puts a dollar amount on the ETF gap right now is quoting a
> vintage-mixed difference. **Do not let a magnitude from this document escape into a PRD, a deck, or a
> sovereign decision.** *(And note the recursion: this whole document exists because a field was labelled
> with a computation it did not perform. I nearly shipped a number labelled "measured" that was estimated.)*

---

> ## ⛔ READ SECTION 5 BEFORE YOU ACT ON ANY OF THIS.
> **The repair this document implies is `re-run mdpf`. THAT IS DOOR 6.** The mdpf chain is *correctly idle*
> on the held INF spine sentinel. **This finding manufactures urgency to dispatch the held chain, and it
> arrives dressed as a data-quality emergency with a real $528mm number attached. DO NOT RE-RUN mdpf.**

---

## 1. BOTTOM LINE -- TWO SEPARATE THINGS, AND THEY COLLIDE

**(a) THE DEFINITIONAL QUESTION (Andrew's to answer).** We mark `etf_fund` `additive=FALSE`; Manav counts the
ETFs. Grounded, the ~$678mm of Opal-ETF net assets splits into two *materially different* piles:

| piece | amount | is it already in Opal AUM? |
|---|---:|---|
| held by our partners (49F + Inflection) | **~$578mm** | **YES** -- 49F's custody book already holds its DIVZ/IDVZ/PFDE/PFOE. Adding it **DOUBLE-COUNTS.** |
| **public float** (owned by the investing public) | **~$95mm** | **NO** -- Opal manages this money (we run the fund); no partner custodies it. **The only honestly-addable piece.** |

> **So neither `additive=TRUE` nor `additive=FALSE` is right for the `etf_fund` ROW. The row is a MIXTURE.**
> **The correct additive unit is `public_residual` (~$95mm), NOT `etf_total_net_assets` (~$678mm).**

**(b) A LIVE SERVED DEFECT -- and it landed exactly on `public_residual`.** On the 2026-07-10 partition,
**49financial vanished from `etf_decomposition.held_by_partner`, and ~$528mm of its ETF holdings were
silently reclassified as PUBLIC FLOAT.** `public_residual` is served at **$622.58mm** when the true figure
is **~$95mm**.

> ### 🔴 THE TWO COLLIDE, AND THAT IS THE WHOLE POINT.
> **The number Andrew needs in order to answer (a) is the number that (b) corrupted.** If he were asked
> today *"should we count the ETF public float?"* and someone read the served artifact, they would read
> **$622.58mm instead of ~$95mm.** A **CORRECT "yes"** would then import a **$528mm double-count of 49F's
> own money.** *The defect does not make the decision wrong -- it makes the RIGHT decision produce a wrong
> number.* **(a) IS NOT ANSWERABLE OFF THE CURRENT ARTIFACT.**

---

## 2. THE DEFECT -- OBSERVED ON SERVED BYTES, 3 PARTITIONS

`s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua/{2026-07-07,2026-07-08,2026-07-10}.json`

| partition | `attribution_basis` | 49F held | public_residual |
|---|---|---:|---:|
| 2026-07-07 | `rps_actual:49financial;target_weight:inflection` | 522.49mm | 95.42mm |
| 2026-07-08 | `rps_actual:49financial;target_weight:inflection` | 522.49mm | 94.38mm |
| **2026-07-10** | **`target_weight:inflection`** -- 49F **GONE** | **0** | **622.58mm** |

The `rps_actual:49financial` leg **disappeared**. Its ~$528mm moved from *"held by our partner"* to
*"owned by the public."* **mdpf's last served partition is 2026-07-10 -- so the artifact is FROZEN IN THIS
BROKEN STATE.**

## 3. MECHANISM -- SOURCE-CONFIRMED (Rule 22: `file:line @ commit-ish`)

`data/mdpf/scripts/gold/mdpf_aggregate_aua.py:429-460 @ HEAD (CLOUD, 2026-07-13)`

```python
for firm_id in sorted(set(held_by_partner)
                      | {f for (f, t) in partner_held if t == etf}):     # :446-447
    if (firm_id, etf) in partner_held:
        held_by_partner[firm_id] = partner_held[(firm_id, etf)]           # :449
        actual_firms.append(firm_id)
held_sum = sum(held_by_partner.values())                                  # :451
residual = None if total is None else round(total - held_sum, 2)          # :452
```

A firm enters `held_by_partner` **only** via (i) composition rows (`target_weight`) or (ii) the WS-D.2
`partner_held` RPS override (`rps_actual`).

**49financial was NEVER in the composition path** -- its basis on every good partition is `rps_actual:49financial`,
never `target_weight:49financial`. So 49F's ETF attribution rests on the RPS override **alone**.

**When the RPS override went empty for 49F, the firm silently fell out of the loop** -- and `residual =
total - held_sum` (`:452`) absorbed **100% of its holdings into `public_residual`.**

> **There is NO expected-firms guard, NO raise, NO floor, and no test on the DIRECTION of the residual.**
> **An empty input produced a plausible, well-formed, completely wrong artifact.** This is the same class as
> the zero-row roster walk-back (`INF_B_00`): *absence rendered as a confident value.*

**WHY the override went empty is still `INFERRED`:** the 49F block is `rolled_forward` at `as_of 2026-07-06`
(the known G1 staleness). The RPS-derived ETF attribution appears to have **dropped rather than rolled
forward** with it. **I have NOT source-confirmed the producer of `partner_held`, so I am not asserting that.**
It is the next thing to ground, and it does **not** change (1) or the guard analysis.

## 4. 🔴 BOTH GUARDS SAW IT. NEITHER STOPPED IT.

From the SERVED `reconciliation` block -- **the artifact confesses, in writing, and serves anyway:**

```
sentinel_1_cohort0_dod : "Cohort 0 day-over-day move 559.7% > 50% threshold
                          (today $622,575,546.16 vs prior $94,377,892.59)
                          -- WARN: audit-only, non-blocking; value stored"
identity_2_etf_residual: "PASS" ... "the gate catches over-attribution (<0),
                          not under-attribution"
overall                : "PASS"
```

- **The DoD sentinel FIRED** -- 559.7%, an 11x breach of its own 50% threshold -- and is **audit-only,
  non-blocking. "value stored."**
- **The identity gate PASSED because it is STRUCTURALLY BLIND to this direction.** It tests
  `residual < 0` (over-attribution). This failure drove residual **UP**. *The one check pointed at this field
  cannot fail in the direction it actually failed.*
- **`overall: PASS`.**

> **A guard that cannot block is not a guard, and a gate that only tests one direction is not a gate.**
> The estate detected a 6.6x move in a served number, wrote it down, marked itself PASS, and shipped it.
> **This is `CONTROLS_OVER_CARE` in a single JSON block.**

**BOUNDED, HONESTLY (I checked, rather than assuming the worst):**
- **The AUM headline is NOT corrupted.** `etf_public_residual_total` is **audit-only** by the served
  `headline_formula`; `sentinel_3_cross_validation` reconciles the $1,758,111,296.54 headline against an
  independent recompute at **$0.00 diff**. *No served AUM number is wrong.*
- **OPAL_ASSETS G4 ownership rows are NOT corrupted.** `build_ownership_rows`
  (`opal-assets-daily-emitter/lambda_function.py:676-692 @ bf7269a1e`) sources per-partner ETF ownership from
  **ETFS_CANON** (`ownership_value` / `source_as_of`), **NOT** from mdpf's `etf_decomposition`. Independent path.
  *(This is also why CTO~B's briefing shows 49F ETF ownership at an `as_of 2026-06-24` vintage that does not
  appear anywhere in mdpf's decomposition -- two different sources, and I nearly mistook one for the other.)*
- **What IS corrupted:** mdpf's served `held_by_partner`, `public_residual`, `public_ownership_pct`,
  `attribution_basis`, and `aggregate.etf_public_residual_total` -- i.e. **the entire per-partner ETF
  ownership picture, which is exactly what OPAL_ASSETS G4 exists to get right.**

---

## 5. ⛔⛔ THE REPAIR IS DOOR 6. DO NOT WALK THROUGH IT.

**The obvious, competent, correct-looking next move is: fix `mdpf_aggregate_aua.py`, re-run mdpf, watch the
$622mm drop back to $95mm.** Every instinct says do it. **DO NOT.**

- **mdpf-daily-trigger is EVENT-DRIVEN on the INF spine sentinel** `opal-data-inf/gold/meta/pipeline-complete.json`.
  **mdpf does not run on a cron. It runs when the INF chain completes.**
- **The mdpf artifact is frozen at 07-10 because the INF chain is HELD -- and the emitter is CORRECTLY IDLE,
  not broken.**
- **Therefore "re-run mdpf to fix the ETF numbers" == writing that sentinel == DISPATCHING THE HELD INF CHAIN
  BY THE BACK DOOR**, routing around both the chokepoint and the basename collision, performed by an agent who
  believes they are fixing a data-quality bug **in a different pipeline**, for a partner-reporting surface,
  **with a real $528mm number to justify the urgency.**

> **THIS IS THE STRONGEST FORM OF DOOR 6 I HAVE SEEN, BECAUSE THE FROZEN ARTIFACT FROZE IN A BROKEN STATE.**
> The hold is now *actively serving a wrong number*, which makes lifting the hold look not merely tempting but
> **responsible.** *The test is FUNCTIONAL, not lexical: this says "mdpf" and "ETF" and never says "INF" --
> and it would advance the INF chain.* **A VERIFIED DEFECT IS NOT A LICENCE.**

**WHAT THIS MEANS PRACTICALLY: the defect CANNOT be repaired while the INF hold stands, and that is ACCEPTABLE**
-- because (i) no served **AUM** number is wrong, (ii) OPAL_ASSETS G4 does not read the corrupted field, and
(iii) the artifact is **frozen**, so the error is **static and known, not spreading.** **A known-wrong frozen
number is strictly safer than an unheld pipeline.** The fix lands when the hold lifts, in the normal order.

---

## 6. THE DECISION FOR ANDREW (legible, not fixed -- per MSTR)

**Q: Does Opal AUM include the ~$95mm of our own ETFs owned by the investing public?**

- **NO (status quo).** `etf_fund additive=FALSE`. Opal AUM = partner AUA only = $1,758.11mm. Manav's larger
  number is then **~$578mm of double-count + ~$95mm of genuine definitional difference** -- *not* an error on
  either side, a different question being answered.
- **YES.** Then add **`public_residual` ONLY (~$95mm)** as its own additive basis -- **never
  `etf_total_net_assets`**, which double-counts every partner-held dollar. Opal AUM becomes ~$1,853mm.
- **Either way, `etf_fund` (the ~$678mm row) is NEVER additive as a whole.** *That part is not a judgment call
  -- it is arithmetic, and the double-count is measured.*

**MY RECOMMENDATION (a recommendation, not a ruling):** the current `additive=FALSE` is **defensible and I am
not asking to change it**. What I *am* flagging is that the label `etf_fund / additive=FALSE` **hides a real
~$95mm of Opal-managed money** that no cohort currently carries. **That is a gap in the taxonomy, not a bug in
the flag.** If Andrew wants it counted, the clean shape is a **15th cohort: `etf_public_float`, additive=TRUE,
value = `public_residual`.** The 14-cohort set is his, so this needs his word.

**BLOCKED ON THE DEFECT:** *the ~$95mm cannot be quoted from the current artifact.* Use the **2026-07-08**
partition ($94.38mm, last good) for any decision made before the hold lifts -- **and cite that vintage.**

---

## 7. WHAT I DID NOT DO

- **No code changed. No mdpf run. No sentinel written. No trigger invoked.** INF untouched.
- Frozen 3 untouched (`build_assets_dim.py`, `_orion_api_silver_lib.py`, `convert_transactions_to_silver.py`).
- Read-only S3 GETs on 3 served partitions. Source read-only. No spawns, no vendor calls.

## 8. GROUNDING (Rule 22a)

| axis | evidence |
|---|---|
| **applied** (served) | 3 partitions downloaded + parsed: 07-07, 07-08, 07-10. The firm-drop, the basis change, and the 622.58 vs 94.38 residual are **read off the bytes**, not inferred. |
| **desired** (source) | `mdpf_aggregate_aua.py:429-460 @ HEAD`; `opal-assets-daily-emitter/lambda_function.py:478-481, 676-692 @ bf7269a1e` |
| **exercised** | Diffed `held_by_partner` across 3 consecutive partitions -- the discriminating test. A single partition **cannot** show a firm dropping out; **it took the time series.** |
| **INFERRED, not claimed** | *why* the RPS override went empty (G1 staleness is the leading hypothesis, **not source-confirmed**). The exact "true" public float at 07-10 (~$95-100mm) is an **estimate**; the last MEASURED value is **$94.38mm @ 2026-07-08**. |
