# MDPF cohort census -- ABSENT vs STALE-BUT-PRESENT, and the third mode that is worse than both

**archetype:** DIAGNOSE
**Author:** 0.7.0_AE_CloudOps
**Measured:** 2026-07-28T~2130Z, read-only. No writes, no build, no apply.
**Task:** CTO queue item 2, top-of-scope measurement. COO's numbers treated as **a floor to verify,
not a result to carry**.

## DENOMINATOR AND PREDICATE (stated first, per Rule 22)

**Denominator:** `aws dynamodb scan` on `opal-assets-daily-aua`, filtered `run_date = 2026-07-28`
-> **32 rows** (ScannedCount 35,078).
**Predicate:** mode = (`vintage_state`, does the row carry a numeric `value`, what is `as_of`).
**Trading-day distances from `lib/trading_calendar.py` -- the ONE definition, never wall-clock.**

```
vintage_state census @ run_date=2026-07-28 :  missing 14 | rolled_forward 13 | fresh 5  = 32
```
**This independently reproduces COO's 5 / 13 / 14 = 32 exactly.** Verified, not inherited.

---

## MODE C FIRST -- ZERO PRESENTED AS TODAY'S NUMBER (CTO was right to rank this above the holes)

```
cohort_id      _total__partner_aua
vintage_state  missing
value          0                      <- carries a NUMBER
as_of          2026-07-28             <- TODAY
absent_reason  None
```
It is the **only** row in the table that is `missing` yet carries a value.

**Why it is 0:** only two cohorts are `additive: True` -- `49f_schwab_custody` and
`inflection_models` -- and **both are `missing` with `value: None` today.** So the total is 0 because
**100% of its constituents are absent**, and it publishes that as a current-dated number.

> **A hole announces itself; a zero does not.** A consumer reading `value` without also reading
> `vintage_state` receives **$0 stamped with today's date** for total partner AUA. That is not a gap
> in a series -- it is a confident wrong answer, and it is the one mode here that can reach a
> client-facing surface without anything looking broken.

**Severity: highest of the three modes.** Absence is honest; this is not.

---

## THE TWO "13"s ARE DIFFERENT POPULATIONS -- AND NEITHER IS UNIFORM

CTO's warning held: *anyone saying "the 13" must say which 13.*
- **DS's 13** = `vintage_state: missing` (49F models, 49F custody, `inflection_models`,
  `cottonwood_bd_*`, `_global__aua_total`). ABSENT.
- **COO's 13** = `rolled_forward`. STALE-BUT-PRESENT. **All 13 are ETF cohorts** -- confirmed.

**But the rolled_forward 13 are NOT one vintage. They are three, and the spread is the finding:**

| as_of | trading days behind | cohorts | value carried | verdict |
|---|---|---|---|---|
| 2026-07-06 | **16** | 4 (`etf_*__held_49financial`) | **$522,484,735.05** | **REAL DEFECT** |
| 2026-07-24 | 2 | 7 (4 `__held_cottonwood`, `etf_divz`, `etf_idvz`, `_total__etf_fund`) | $1,292,028,083.53 | see below |
| 2026-07-27 | **1** | 2 (`etf_pfde`, `etf_pfoe`) | $243,636,318.00 | **HEALTHY -- T-1** |

**COO's ~$522mm verifies exactly: $522,484,735.05 across 4 cohorts.**

> ### ⚠ CALLING ALL 13 "STALLED" WOULD HAVE BEEN A FALSE OUTAGE ON AT LEAST 2 OF THEM
> The two `as_of 2026-07-27` cohorts are **1 trading day behind**, which is **T-1 -- the documented
> default healthy state for every AUM/holdings pipeline** (CLAUDE.md NEVER#1). They are not stale.
> And the four `__held_cottonwood` rows at T-2 match **cottonwood's declared D+2 holdings cadence**
> (`mdpf_roster.py`: *"cadence is per feed, not per partner"*), so T-2 is their EXPECTED frontier,
> not a lag.
>
> **A count of 13 is not a population of 13 defects.** The number was never the finding.

**NOT ASSERTED:** whether `etf_divz` / `etf_idvz` / `_total__etf_fund` at T-2 are defective. That
depends on each feed's declared cadence, which I did not resolve per-cohort. Unknown, and labelled.

---

## MECHANISM -- ⚠ MY FIRST ANSWER WAS WRONG. IT IS A CONSUMPTION DROP, NOT AN UPSTREAM BREAK.

**RETRACTED (before this document was committed):** I first concluded *"the source stopped -- a
partner-specific producer stop for 49financial ETF-ownership."* **That is false as a cause.**

**How I got there, because the error is instructive:** the DDB row names its own source --
`source_field = opal-data-etfs/daily/49financial/2026-07-06.json[DIVZ].ownership_value` -- and I
verified that path is genuinely stale (newest `2026-07-06.json`, vs `daily/cottonwood/` current
through 07-24 on a clean 06:30 cadence, which was a sound positive control). **Both measurements are
true. The inference was not.** I grounded **the artifact the producer's SELF-REPORT named**, and
CLAUDE.md is explicit: *never trust a producer's self-report -- verify against the SERVED artifact.*
A stale file at a self-reported path does not establish that the consumer lacked fresh input.

**MEASURED -- the emitter's ACTUAL input, `platinum/mdpf/aggregate_aua/2026-07-28.json`
(10,098 B, LastModified 2026-07-28T16:46:39Z):**
```
source_vintage.by_feeder.partner_held_etf = {"49financial": "2026-07-28"}     <- TODAY
etf_decomposition[DIVZ].held_by_partner   = 49financial held 180,276,733.36
                                             inflection  held  18,382,174.73
```
**versus what the emitter WROTE to `opal-assets-daily-aua` for the same run_date:**
```
etf_divz__held_49financial = 175,858,373.23   vintage_state: rolled_forward   as_of: 2026-07-06
```

> **THE FRESH VALUE WAS SITTING IN THE FILE THE EMITTER READ.** The data was collected and delivered;
> it was **not consumed**. This is a defect inside one component we own, with correct inputs already
> in front of it -- **no upstream chase, no vendor dependency.**

**And the roll-forward is SELF-DECLARED, not silent:** the row's `source_field` names the 07-06
artifact, so the emitter reports having consumed 07-06 while its input carried 07-28. That is the
sharpest available lead -- **the component states which vintage it used, and it is the wrong one.**

**DISCRIMINATOR (CTO/COO, and it survives my check):** `etf_*__held_inflection` came out **fresh**
from the **same `etf_decomposition` array in the same file**, and both partners carry a non-null
`held`. So the emitter is not failing the ETF section wholesale -- it treats the two attributions
differently. Their declared bases differ
(`attribution_basis: "rps_actual:49financial;target_weight:inflection"`), and the RPS-fed cohort
`49f_schwab_custody` is `no_source_partition`. **HYPOTHESIS, NOT A FINDING -- nobody has read the
emitter's per-cohort logic, including me. If it is wrong, that is the finding.**

**⚠ A SECOND SELF-INFLICTED NEAR-MISS, RECORDED:** reading that file I queried
`held_by_partner[].held_value` and got `null` for **every** partner on **every** ticker -- which
would have read as *"the input is empty, COO is wrong."* **The field is `held`, not `held_value`.**
My null was **my own query artifact**. Caught only by dumping the raw object instead of trusting my
accessor. *A wrong key name and an empty field are byte-identical in the output* -- the same shape as
tonight's forged `Z` and the `grep -c` on an error message: **control the retrieval, not the
pattern.**

---

## ⚠ A DEFECT I NEARLY FILED AGAINST A CORRECT INSTRUMENT -- RETRACTED BEFORE IT LANDED

The 4 stale rows carry `staleness = 99` where the calendar computes **16**. I labelled that
`** MISMATCH **` in my working output. **It is not a mismatch. 99 is a documented sentinel.** The
row's own `staleness_semantics` says so:

> *"DUAL-PURPOSE BY CONTRACT: an integer >=0 is trading-days-behind (a MEASURE); **99 is a SENTINEL
> meaning vintage_state=missing OR coverage_state=incomplete (NOT '99 days')**. The 99 is shared with
> the 14 live mdpf-cohort-freshness-stale-* alarms so row and alarm agree by construction -- **do not
> 'clean' it without them.**"*

And `coverage_state: incomplete` on all four -- **the field is behaving exactly to contract.**
Retracted before it reached a report. **This is the fourth near-miss tonight of filing a defect
against a correct instrument** (`~C`/comp-pipescript, CTO/comp-routes twice, my own 0.5.0 liveness
claim). Same root every time: **reading a value without first establishing what it is OF.**

*Had I "fixed" the 99 to 16, I would have silently desynchronised 14 live alarms from their rows.*

---

## THE QUESTION THAT PRICES ALL OF IT -- STILL OPEN

**Does anything READ the ETF cohorts?** CTO's `ddb.scan()` finding was scoped to
`49f_schwab_custody` only. **Consumer unknown -> severity unpriced.** $522mm stale is a P1 if a
client surface reads it and an internal-only annoyance if nothing does. **I did not answer this and
am not guessing.** It is the next measurement.

---

## SUMMARY FOR SEQUENCING

| # | Finding | Severity | Grounded |
|---|---|---|---|
| 1 | `_total__partner_aua` publishes **0 with today's `as_of`** while `missing`; both additive constituents absent | **Highest -- wrong answer, not a gap** | Measured |
| 2 | 4 x `etf_*__held_49financial` at **T-16**, **$522,484,735.05**. **CONSUMPTION drop, not an upstream break** -- the emitter's own input carried `partner_held_etf: 2026-07-28` and `held 180,276,733.36`, and it wrote the 07-06 value anyway, **self-declaring 07-06 as its source** | High, **pending consumer** | Measured on the emitter's actual input |
| 3 | 14 `missing` cohorts | Honest absence; consumer's absent path holds | Measured |
| 4 | 2 cohorts at T-1, 4 cottonwood at declared-D+2 T-2 | **NOT defects** | Trading calendar |
| 5 | `staleness = 99` | **NOT a defect -- documented sentinel** | Contract read |
