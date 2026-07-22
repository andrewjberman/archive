# MDPF_REVAMP finalization ITEM 1 — root-cause of the Inflection Jul-6/Jul-7 jump and the other daily-trend spikes

**Author:** 0.4.0_DS_ClientPlatform · **Date:** 2026-07-22 · **Mode:** READ-ONLY (zero writes to
`gold/mdpf_revamp/*`; the 2-of-3 never-widen co-sign pin is intact)
**Trigger:** Andrew-direct, ~1205Z, verbatim: *"why Inflection's model numbers are jumping around july 6
july 7 with some other odd spikes in the daily trend timeseries."*
**Vintage read:** frozen coherent-9 — inflection `cec5a0d6fe749aae77735f9297edbb71`, global
`c27e1f370f9c08de6489cb11bf885e13`, account_dist(inflection) `afb964c4d67f2a3e3682c50269dc69e8`
(ETags confirmed at read time, not assumed).

---

## Verdict in one line

The **value** axis of the revamp is correct and already fixes every spike Andrew can see in legacy. The
**count** axis is not: it imports `account_count` from the legacy served artifact by date-join, and
therefore **inherits legacy's 07-06 mis-stamp into the frozen-9** — rendering a +66/−66 account
jump-and-revert on **exactly July 6 and July 7**, the dates Andrew named.

---

## 1. The real business event (not a defect — do not smooth it)

Inflection is progressively moving accounts out of non-model into Opal models. `partner_custody_total`
stays flat ~$200–206M while `model_aua` rises 96.7M → 137.2M and non-model falls. **Mechanism
SOURCE-CONFIRMED** (Rule 22) at portfolio level in `eclipse/inflection/silver/fact_portfolios_full` — it
is an eclipse **`modelId` re-assignment on existing portfolios**, not funding:

| transition | portfolios (a→b) | new | departed | modelId changed | of those non-Opal→Opal | value moved | d(Opal) | whole-book move |
|---|---|---|---|---|---|---|---|---|
| 06-02 → 06-03 | 854 → 854 | 0 | 0 | 44 | **44 (100%)** | 16,864,872.42 | +16,961,432.30 | +66,672.38 |
| 07-09 → 07-10 | 856 → 856 | 0 | 0 | 65 | **65 (100%)** | 11,400,606.09 | +11,765,853.05 | +645,811.09 |

Zero new and zero departed portfolios on both dates is the decisive limb: nothing entered or left, the
labels changed. The mechanism also runs **continuously in smaller batches** (27 further conversions
between 06-03 and 07-09), so "one-time" does not hold.

## 2. Dating — closed on the value axis

All **54/54** eclipse partitions carry an in-row `_source_as_of` identical to their `date=` partition
(0 disagreements). The revamp's value axis is anchored to the vendor's own as-of stamp.

**Legacy's is not.** A value-fingerprint sweep of every legacy non-null date against the revamp finds
**exactly 2** misdated dates:

- legacy `2026-07-06` carries the revamp's `2026-07-10` triple (136,859,722.32 / 65,461,006.49 /
  202,320,728.81) — **positive control run separately:** legacy[07-06] == revamp[07-06] is `False`.
- legacy `2026-07-18` (a Saturday) carries the revamp's `2026-07-20` values.

Plus a third legacy-only error of a different shape: legacy reports `model_aua = 0.0` on **2026-05-15**
where eclipse's first partition sums to **94,546,459.54**, which the revamp reproduces exactly. Legacy
misses the launch day and steps on 05-18 instead. (This grounds the 05-15/05-18 pair CTO flagged as
inferred — it is a legacy **miss**, not a shifted value.)

## 3. The other odd spikes — enumerated with denominators

- **Firm total, inflection, ≥2%:** legacy 6 flagged / 428 transitions; revamp **3** / 420. The revamp's
  three are 06-03 (+17.54%), 06-10 (+2.24%), 07-10 (+9.41%) — all the real reclassification.
- **Band level, revamp, ≥2%:** 16 date-pairs flagged out of **2,940** band-day transitions. The two
  multi-band events are 06-03 (6 bands) and 07-10 (5 bands) = the reclassification landing per model.
  The remainder is small-denominator noise on `opal_ultra_short_term` (a ~$0.4–0.9M band; +46% there is
  ~$200K and is invisible in a stacked chart).
- **Global non_model, ≥5%:** **14** flagged — 7 offsetting-reclass, 7 genuine net moves. All 14 fall
  between 2024-11-12 and 2026-01-02, i.e. **none in Andrew's July window** and all before the
  2026-05-15 inflection launch, so all 14 are 49F-origin.

## 4. The 6 honest-Nones are exactly the 6 missing eclipse trading-day partitions

Weekday sweep 05-15..07-21: 7 weekdays lack an eclipse partition — 05-21, 06-01, 07-01, **07-03**,
07-13, 07-14, 07-15. **07-03 is the observed July-4 holiday** (resolved on canonical
`lib/trading_calendar.py` per NEVER#1 — a wall-clock gap is not a finding). The remaining **6 are
exactly** the artifact's declared honest-None dates. The producer neither fabricates nor over-nulls, and
**07-13/14/15 is a real 3-day eclipse feed gap**, not a producer artifact.

## 5. THE DEFECT — inside the frozen-9, on the count axis

`load_served_account_count` (`dim_mdpf_aggregate_aua_timeseries.py:476-500`, wired at `:812`) imports
`account_count` from the **legacy served artifact** (`s3://opal-data-portal-v2/json/mdpf/inflection/
aggregate-aua-timeseries.json`) by date-join. Legacy's date axis is the broken one. The producer
therefore inherits legacy's mis-stamps onto the count axis while the value axis is read straight from
eclipse — **the two axes of the same artifact are read from different days.**

Frozen-9 inflection on **2026-07-06**: correct 07-06 model values beside `account_count` **540**, which
is **eclipse's 07-10 roster** (true 07-06 count = 474).

What the count view renders: `07-02: 474 → 07-06: 540 → 07-07: 474 → 07-08: 475`. **A +66/−66
jump-and-revert on July 6 and July 7** — Andrew's sentence, reproduced by the revamp.

**Full sweep, denominator stated.** Of 427 revamp dates, **38** have an eclipse partition (eclipse
begins at the 05-15 launch): **26 agree · 7 honest-None · 5 disagree.**

| date | artifact count-vector actually matches | disposition |
|---|---|---|
| 2026-05-27 | eclipse 05-26 | date defect (−1 day) |
| 2026-05-28 | eclipse 05-27 | date defect (−1 day) |
| 2026-06-24 | eclipse 06-25..06-30 (vector stable → shift ambiguous) | date defect |
| **2026-07-06** | **eclipse 07-10** | **date defect (+4 days) — Andrew's date** |
| 2026-07-20 | no eclipse partition | **NOT a defect** — 534 is `account_dist.meta.account_count_by_model_key` (the declared FUNDED frontier basis, CTO 190518Z(a)) vs eclipse's 546 live portfolios |

→ **4 genuine count-axis date defects, 1 declared basis difference.** Noting for the record that the
frontier point therefore sits on a *different basis* than the historical points on the same line.

## 6. Is the 07-09/07-10 roster reconstructable? (CTO's question — answered grounded, not filled)

**Yes.** The producer **already computes it** at `:427` (`account_count: int(len(g))` from the eclipse
partition) and then discards it in favour of the served import. Eclipse has **07-09 = 475** and
**07-10 = 540**.

**The test that could have failed:** at common dates where legacy is not mis-stamped, the
eclipse-derived count equals the served count **44/44 exactly**. The only disagreements are the 5 above.
So sourcing the count from eclipse would (a) preserve the FLAG-2 served tie everywhere served is
correct, (b) fill the 07-09/07-10 gap with a measured count, (c) additionally correct the 4 misaligned
dates.

## 7. Cost, and what I did not do

The fix is ~one line. But it re-produces the inflection and global artifacts, which **voids the 2-of-3
never-widen pin** (fresh pin + fresh 3-pass + fresh limbs required), and it breaks the FLAG-2 PRESERVE
tie on exactly the 4 dates where served is provably wrong — i.e. it breaks a tie *to a known defect*.
That is a change to a CTO+Andrew co-signed decision and it is a scope/sequencing call for CTO and COO.
**I made no write, no re-stage, and no producer edit.**

**Residual, unmeasured, stated plainly:** 49F and global use the same import path (`:628`), so the class
is **structurally present** there — but eclipse is not their model source and I have not swept them.
That is *unmeasured*, not clean. And pre-2026-05-15 dates have no eclipse partition, so this instrument
**cannot see the class before the launch at all**.

---

## Instruments and controls

| Test | Denominator | Control run |
|---|---|---|
| legacy/revamp value fingerprint | 429 legacy dates vs 427 revamp | positive control `legacy[07-06]==revamp[07-06]` → False (test non-vacuous) |
| `_source_as_of` vs `date=` | 54 eclipse partitions | mutant framing: a disagreement would print the offending date |
| firm-total DoD | 420 revamp / 428 legacy transitions | threshold lowered 5%→2% at COO's request |
| band-level DoD | 2,940 band-day transitions | — |
| count-axis alignment | 38 comparable dates (26/7/5) | 44/44 agreement at clean common dates = the discriminating limb |

**What the instrument cannot see:** anything before 2026-05-15 (no eclipse partitions), and the 49F /
global count axes (different model source, not swept).
