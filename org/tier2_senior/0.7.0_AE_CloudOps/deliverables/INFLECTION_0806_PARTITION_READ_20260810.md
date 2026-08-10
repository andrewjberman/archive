# Inflection 2026-08-06 partition read — the axis source, named and measured

**archetype:** DIAGNOSE · **Author:** `0.7.0_AE_CloudOps` · **Date:** 2026-08-10
**GO:** `1.0.0_SA_CTO` 165710Z + addendum 165902Z (Q3 first, widened) · `2.0.0_SA_COO` 165110Z.
**Andrew ~1650Z:** *"i would organize it by 08-06 mechanism failure first…"* — fabric top item.
**Fence: REPORT, do not diagnose. Read only. Cottonwood's mechanism given to REFUTE, never confirm.**

> **THE UNNAMED SOURCE CARRYING 2026-08-06 IS 49FINANCIAL.** Inflection is placed on an axis derived
> from **SmartX's** feed, by design. CTO's contradiction dissolves: both halves are complete and true,
> because they are about **different firms' feeds**.

---

## Q3 (done first, widened) — every axis leg, named, with its 08-06 status

`derive_canonical_axis()` `:819-835`, its own docstring:

> *"The canonical shared MDPF trading-day axis, derived ONCE per run from the DECLARED axis-source
> feed (`fact_model_aum_daily` — route_bindings **49financial** model_leg…). Criterion 2: **sibling
> firms receive THIS axis from the orchestrator**"*

```python
aum      = _cached("aum_daily", load_aum_daily)   # -> SMARTX_SILVER  (:304)
frontier = aum_days[-1]
dates    = canonical_trading_axis(frontier)
```
`SMARTX_SILVER = "smartx/platform/silver"` (`:72`).

| leg | source | carries 2026-08-06? |
|---|---|---|
| **axis frontier** | `smartx/platform/silver/fact_model_aum_daily` (**49F**) | **PRESENT** |
| inflection model value | `eclipse/inflection/silver/fact_portfolios_full` | **ABSENT** |
| inflection custody | `orion/inflection/silver/fact_assets` | **ABSENT** |
| frontier `account_count` | staged account_dist `meta.account_count_by_model_key` | **PRESENT** (source-consistent) |
| historical `account_count` | served `json/mdpf/inflection/aggregate-aua-timeseries.json` | **ABSENT — eliminated by measurement** |

**MEASURED** — `smartx/platform/silver/fact_model_aum_daily/`: `date=2026-08-03 · 08-04 · 08-05 ·`
**`08-06`** `· 08-07 · 08-08 · 08-09 · 08-10` — unbroken. And **49financial PASSED the gate at 440
dates.**

⇒ CTO's *"both cannot be complete"* resolves: **both ARE complete.** 08-06 is absent everywhere *in
inflection* and present in *49financial*, and inflection sits on 49financial's axis by construction.

## Q1 — the discriminator: **ROW ABSENT ENTIRELY**, not present-and-null

`eclipse/inflection/silver/fact_portfolios_full/`, neighbours shown as positive control:
```
date=2026-08-04   written 2026-08-05T03:30:30Z
date=2026-08-05   written 2026-08-06T14:16:06Z
[ date=2026-08-06  -- ABSENT: the sequence jumps 08-05 -> 08-07 ]
date=2026-08-07   written 2026-08-07T22:31:10Z
```
Per `:457` and `:474`, an absent partition yields the `gap` sentinel → `model_value=None`.
**The `None` is a sentinel for a missing partition, not a null cell.**

## Q2 — all seven; the two the log never prints

`INFLECTION_MODEL_KEYS` (`:110`), **7 keys**. Printed (5): `opal_ultra_short_term`,
`opal_short_term`, `opal_intermediate`, `opal_long_term_conservative`, `opal_long_term_aggressive`.
**Never printed (`pres[:5]` truncation): `opal_blend_5050_int_ltc` · `opal_blend_5050_st_int`.**

**7 disagreements = 7 of 7 = the complete key set.** That reconciles the gate's own count exactly and
is itself evidence: a whole-partition absence hits every model. A per-model data defect would not
produce exactly-all-seven.

## Q4 — **CLEAN NO.** Inflection has no second date axis

The eclipse loader (`:422`) reads `["id","modelId","model","totalValue","isDeleted"]`. **No
`assignment_date`, no roster date, no second date axis.** Partitions keyed by `date=` alone.
Cottonwood's defect lives in a `(value_date, assignment_date)` pair **inflection does not have**.

## The three offered hypotheses — all tested to kill

| hypothesis | source | verdict |
|---|---|---|
| cottonwood-style assignment change | CTO | **REFUTED** — Q4, no second date axis |
| cutover label-skip | CTO | **NOT REQUIRED** — the count source is another firm's axis, so it is not needed to explain the counts. May still bear on *why the eclipse partition is missing*; untested. |
| inflection ingestion | **Andrew** | **CLOSEST TO RIGHT.** Inflection's feeds genuinely lack 08-06 on **both** legs. |

**On Andrew's prior:** he called the ingestion gap and it is real. But an ingestion gap alone yields a
**benign NAMED gap** — the loader is built to emit exactly that. What converts it into a **refusal**
is the shared 49F-derived axis admitting a date inflection never carried, against a frontier count
set from a third source.

## The count side — one elimination by measurement, one bound

**ELIMINATED.** `load_served_account_count` (`:529`) reads
`s3://opal-data-portal-v2/json/mdpf/inflection/aggregate-aua-timeseries.json`. Read directly:
**429 dates ending 2026-07-22**, `meta.generated_at 2026-07-23T21:44:25Z`, **08-06 not present.**
*This was my own working hypothesis and the measurement killed it.*
⚠ That object is generated **07-23** — anyone carrying *"the served artifacts read 08-07"* means a
**different (platinum/canonical)** object, not this legacy `json/mdpf` one.

**REMAINING, SOURCE-CONSISTENT.** `load_account_dist_frontier_counts` (`:585`): *"the FRONTIER
per-model account_count = account_dist's OWN funded count… **ONLY the frontier is set**."* Its ROW-11
note: `_latest_date()` resolves roster and valuation partitions **independently**, so the stamped
as-of is *"whenever account_distribution last ran — NOT the axis date it lands on, and nothing bounds
the gap."* The gate's own adjacent line matches: *"the frontier cell wears 2026-08-06 but its count
was measured as of 2026-08-04 — 2 trading day(s) earlier."*
⚠ ~~**BOUND: source-consistent, NOT positively confirmed.** I have not opened the staged account_dist
object…~~ **BOUND DISCHARGED — POSITIVELY CONFIRMED** (CTO GO 173402Z READ 1). Opened
`s3://opal-data-assets/gold/mdpf_revamp/inflection/account_distribution.json`:
**DENOMINATOR 7 entries** in `meta.account_count_by_model_key`, exactly the 7 `INFLECTION_MODEL_KEYS`.
All five gate-logged values match **exactly** (12 · 29 · 203 · 91 · 32), and **the two the log
truncates carry real values: `opal_blend_5050_int_ltc` = 160, `opal_blend_5050_st_int` = 23.**
**7 of 7 models have a count; 0 of 7 have a value.**
⚠ *Residual, reported not resolved:* `meta.period` reads **`None`**, yet ROW-11 printed *"measured as
of 2026-08-04"*. Those do not reconcile from what I can see. **The object is MUTABLE and I read it
~4.5h after the gate did** — `period` may have moved even though the counts did not.

## ~~One unmeasured link, named~~ → MEASURED, AND IT REFUTED THE IMPLIED CONCLUSION

~~SmartX has partitions through 08-10, yet the axis frontier is 08-06… I did not read the parquet to
confirm. INFERRED, flagged, not spent.~~

**READ (CTO GO 173402Z READ 2, boto3, all six partitions' `day` column):**

```
partition     day MAX      rows    weekday
2026-08-05    2026-08-04   4398    Wednesday
2026-08-06    2026-08-05   4406    Thursday
2026-08-07    2026-08-06   4414    Friday
2026-08-08    2026-08-06   4415    SATURDAY
2026-08-09    2026-08-06   4415    SUNDAY
2026-08-10    2026-08-07   4422    Monday
```

⛔ **I BRIEFLY REPORTED THIS AS "THE FEED STOPPED ADVANCING ON 08-06." THAT WAS A FALSE OUTAGE AND I
RETRACTED IT AT 175008Z.** The apparent stall across `08-08`/`08-09` **is a Saturday and a Sunday**.
Data for trading day D lands in the next trading day's partition — Friday 08-07's data is in
**Monday 08-10's** partition — and the row count **grows throughout** (4398 → 4422). **The feed is
healthy on a T-1 trading-day cadence.**

> **CLAUDE.md's FIRST NEVER-rule names this exact scenario** — *"Friday's data IS Monday's correct
> answer… a Monday reading of '3 days stale' is a HEALTHY pipeline plus a weekend."* Today is Monday.
> I read a Sunday partition, saw Thursday's data, and called an outage. **I had already computed that
> 08-09 was a Sunday earlier the same session** for the mirror work — I held the fact and did not
> apply it, which is worse than not having it. **Every instrument agreed with me; what was missing was
> the calendar frame, not a measurement.** And measuring **n=1** was the enabling error — CTO caught
> that and asked for more partitions, which is what produced the correction.

**WHAT THE MEASUREMENT ACTUALLY SHOWS:** the floor fires **13:00Z**, SmartX lands **~13:40Z**, so
**the floor reads yesterday's partition every day.** Today it read Sunday's (day-max 08-06) → frontier
**08-06**. **Monday's own partition carries day-max 08-07 — and inflection HAS 08-07 on both legs**
(`eclipse/…/fact_portfolios_full/date=2026-08-07` and `orion/…/fact_assets/date=2026-08-07`, both
measured present). **The 40-minute ordering gap selects the frontier, and it selects the one date
inflection lacks.**
⚠ **PREDICTION, NOT MEASUREMENT:** I have **not** verified that a frontier of 08-07 makes inflection
pass — other limbs could refuse, and 08-06 remains a real hole in inflection's history regardless.
**No schedule change proposed.**

## Compiler Tools

| Tool | Result |
|---|---|
| `aws s3api list-objects-v2` × 3 prefixes | eclipse / orion / smartx partition listings — APPLIED reads; every ABSENT verdict carries the listing it is absent from, with neighbours as positive control |
| `aws s3 cp s3://… -` (stdout) | Read the served artifact **without touching the filesystem** — the `.tools/aws` shim had rewritten an absolute scratch path to a relative one (`..\..\..\..\cygdrive\c\…`), the MSYS class CLAUDE.md names. Streaming to stdout sidesteps the arg layer entirely |
| `sed`/`grep` over `dim_mdpf_aggregate_aua_timeseries.py` | Read the **loaders and the axis builder** — this is what named the 49F axis source; no listing could have shown it |

**Method note:** Q3 was answerable only from **source**, not from S3. Every S3 listing in the world
says "08-06 is absent from inflection"; **only the code says inflection is standing on another firm's
axis.** Live state grounds WHAT; source grounds WHY (Rule 22), and here the WHY was the whole question.

## State

**Read only. Nothing repaired, applied, or re-run.** Cottonwood 08-06 untouched (CLOSED, CTO
@a66080db54). The `ce99054e44` → orion/eclipse attribution is **not inherited as a premise** anywhere
above, per MSTR's NOT-ESTABLISHED flag.

---

# ADDENDUM 2 — Andrew's question closed it: the publisher is fine, the WRITE is declined

**Andrew-direct ~1758Z, verbatim:** *"If 49F was healthy, we'd be seeing the Friday August 7th data
displaying in the portal, but we're seeing Thursday August 6th, so something is preventing publishing
there. Did the portal publisher itself have an issue?"*

**He is right that something is preventing it. It is NOT the publisher.** His question is what made me
measure the thing nobody had: **what was actually on the publisher's menu.**

## Measured — newest gold object per firm/artifact (DENOMINATOR: 79 objects under `portal/gold/mdpf/`)

| firm | artifact | newest date | **written** |
|---|---|---|---|
| 49financial | aggregate-aua-timeseries | 2026-08-06 | **2026-08-07 22:47:19** |
| 49financial | aum-metrics | 2026-08-06 | **2026-08-07 22:47:19** |
| 49financial | account-distribution | 2026-08-07 | 2026-08-07 22:47:20 |
| cottonwood | aggregate-aua-timeseries | 2026-08-06 | 2026-08-07 22:47:19 |
| global | aggregate-aua-timeseries | 2026-08-05 | 2026-08-07 03:52:16 |
| inflection | aggregate-aua-timeseries | 2026-08-05 | 2026-08-07 03:52:16 |

**NOTHING under `portal/gold/mdpf/` has been written since `2026-08-08T13:40:44Z`, and nothing for
49financial since `2026-08-07T22:47:19Z`.** The publisher published the newest object that exists for
every firm — `published=14 unchanged=0 failed=0`. **It had no 08-07 timeseries to publish.**

## The blockage — two layers, both measured

1. **The frontier never reaches 08-07**, so gold builds *for* 08-06 and never attempts an 08-07 object.
2. **Rebuilding 08-06 hits an object that already exists**, and the guard declines the write:
   ```
   CONFLICT (recorded, not overwritten):
     portal/gold/mdpf/49financial/aggregate-aua-timeseries/2026-08-06.json -- 19 business path(s)
     e.g. ['_provenance.process_time', 'by_model.opal_growth_sma.model_value[439]']
   ```

⇒ **Every daily cycle re-derives a date that already exists, finds it differs, and correctly refuses
to overwrite.** The guard is doing its job. The product is frozen anyway.

### The counts reconcile exactly — which is why this is believed, not merely plausible

`cycle complete: 3/12 A4 objects built` = **49financial's three artifacts — the same three that logged
CONFLICT** — and `errors=['cottonwood','inflection','global']` = the other nine.
**49financial is the ONLY scope that builds, and its output is declined at the write step, daily.**

> **"3/12 built" has been reading as partial success. It is 3 BUILT AND 3 DISCARDED.** A build count
> that stops at `built` cannot distinguish a written object from a declined one — the same
> shape as every other retrieval-frame defect recorded today, at the write layer.

## A framing error of mine, corrected by the question

I reported *"the vendor feed is healthy"* and let it carry the implication *"so nothing is wrong
there."* **Both halves are true and neither follows from the other: THE FEED IS HEALTHY AND THE
PRODUCT IS FROZEN — three days for 49financial.**

My retraction had fixed a false-outage claim and then **under-claimed in the other direction**. The
missing frame came from the **product side** — what the portal is actually displaying — which no log
I was reading would have supplied. *A pipeline-side instrument cannot tell you the product is wrong;
it can only tell you the pipeline did what it was told.*

## Also surfaced

**49financial's `account-distribution` reached 08-07 while its `aggregate-aua-timeseries` stopped at
08-06** — different as-of dates across artifacts of the **same firm** (roster basis vs axis frontier),
served side by side. A coherence question about the served set, same shape as the frontier-count issue
one layer up.

**The stack is now THREE layers, not one defect:** frontier selection · conflict-decline at write ·
count/value coherence. Nothing diagnosed further, nothing proposed, nothing touched.
