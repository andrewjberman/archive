# ADVI_BDPARITY.P1-PROBE BP1-4 (measurable half) -- the full-history load, MEASURED: it does not run

> ⛔ **CORRECTION 2026-08-30T02:2xZ, TO MY OWN FINDING BELOW. Read this before the body.**
>
> **The three partitions are 10 COLUMNS, not 14.** `bmv`, `emv`, `cf_net` and `cf_gross` are
> **ABSENT ENTIRELY**, on top of `r_net`/`r_gross` being `null`-typed. Measured, all four dates:
>
> ```
> date=2026-08-18   NCOLS=10   r_net:null    r_gross:null    bmv/emv/cf_net/cf_gross ABSENT
> date=2025-01-09   NCOLS=10   r_net:null    r_gross:null    bmv/emv/cf_net/cf_gross ABSENT
> date=2024-07-08   NCOLS=10   r_net:null    r_gross:null    bmv/emv/cf_net/cf_gross ABSENT
> date=2026-08-19   NCOLS=14   r_net:double  r_gross:double  (POSITIVE CONTROL, all four present)
> ```
>
> **Found by `4.0.0_SA_CRO` (84379 item i), who read the partition a second time on its own
> instrument instead of inheriting my sentence.** That is the only reason it was caught before
> `0.7.0_AE_CloudOps~L` built an acceptance denominator on the incomplete version.
>
> **WHY MY INSTRUMENT COULD NOT SEE IT.** My census built `column -> {type: partitions}` and
> reported columns carrying MORE THAN ONE TYPE. **A column ABSENT from a partition contributes
> nothing to that map**, so it can never surface as drift. I ran a PRESENCE instrument, and an
> omission is invisible to every one of them.
>
> ⛔ **AND THE MISS WAS VISIBLE IN MY OWN OUTPUT.** I printed `DISTINCT SCHEMA SIGNATURES: 2` and
> then described only the type-drift half. **The second signature WAS the 10-column shape** -- I
> had the count in hand and read it as confirming the story I already had, instead of opening it.
>
> **WHAT CHANGES, and it is not cosmetic:**
> 1. **The remedy stated in section "What this changes" below is INSUFFICIENT.** A cast does not
>    conjure an absent column. The fix is a **unified schema with the four columns declared** plus
>    schema-tolerant reads -- not merely casting `r_net`/`r_gross`.
> 2. A 10-column partition is **a structurally different WRITE**, not a normal day whose returns
>    came out null. That is a sharper discriminator for the engine-branch question than an
>    all-null return day, and it was routed to `0.4.0_DS_ClientPlatform~N` (C02-g-2).
> 3. For `0.7.0_AE_CloudOps~L` (C02-g-3): on these dates **four columns do not exist to compare
>    at all**, so `NOT-EVALUABLE-BY-SCHEMA` must cover the absent four, not only the null two.
> 4. `3.0.0_SA_CVO` ANNOTATION 2's BMV-0 rule reads BD's returned `beginningMarketValue`, which is
>    on **BD's side** and untouched by this. Our absent `bmv` does not reach it.
>
> **SCOPE OF THE CORRECTION, deliberately narrow:** the SHAPE of the schema difference and the
> SUFFICIENCY of my remedy. **The existence, the dates, the row counts, the denominators, the
> positive control and the crash all stand as measured.** Everything below is otherwise unchanged.


**Seat:** `0.4.0_DS_ClientPlatform~C` | **Clock:** 2026-08-30T02:0xZ (read) | **AC:** BP1-4, the half `2.0.0_SA_COO` 84028/84081 named as unblocked

## The headline

**The P2-CENSUS full-history load, written the way a census would write it, CRASHES.** Not slowly --
it raises. The prior estimate for this item was *"37 partitions load in 0.2s, so a 535-partition
full-history load is seconds, not a risk"*: an **extrapolation from a 37-partition slice**. The
runtime half of that sentence is right and irrelevant. **The risk was never runtime.**

```
pyarrow.lib.ArrowNotImplementedError: Unsupported cast from double to null using function cast_null
```

## What was measured (denominator printed, nothing sampled)

`s3://opal-data-49financial/gold/advi/canonical/twr_daily/` -- **535 date partitions, 1,070 objects,
118.2 MB** (each partition = `data.parquet` + `manifest.json`). **Schema read on ALL 535, no head, no
sample**, 67.8s for the metadata pass.

| | |
|---|---|
| distinct schema signatures across history | **2** |
| columns carrying more than one type | **2 of 14** |

**The two drifting columns are `r_net` and `r_gross` -- the return columns the entire parity
comparison rests on.**

| column | type | partitions | span |
|---|---|---|---|
| `r_net` | `double` | 532 | 2024-07-09 .. 2026-08-28 |
| `r_net` | **`null`** | **3** | 2024-07-08 .. 2026-08-18 |
| `r_gross` | `double` | 532 | 2024-07-09 .. 2026-08-28 |
| `r_gross` | **`null`** | **3** | 2024-07-08 .. 2026-08-18 |

## The 3 partitions, opened rather than inferred

A `null`-typed parquet column means the writer saw **no non-null value in that partition**. These are
not empty partitions -- the rows are all there:

| date | rows | distinct accounts | `r_net` non-null |
|---|---|---|---|
| **2024-07-08** | 4,074 | 4,074 | **0** |
| **2025-01-09** | 4,808 | 4,808 | **0** |
| **2026-08-18** | 7,315 | 7,315 | **0** |

**POSITIVE CONTROL, the adjacent day:** `2026-08-19` -- 7,332 rows, **6,393 non-null**, dtype
`float64`. So the instrument reads returns fine on a neighbouring partition; the three above are a
property of the data, not of the reader.

## Reading it -- one is expected, two are not, and I am not guessing which

- **`2024-07-08` is the gold floor**, the first partition in history. A daily return needs a prior
  day to link from, so an all-null first day is **the expected shape**, not a defect.
- **`2025-01-09` and `2026-08-18` are interior dates with a populated day on either side.** They are
  **NOT explained by the floor argument.** I am naming them, not diagnosing them -- the cause is not
  established by this measurement and I did not chase it.
- ⭐ **`2026-08-18` carries 7,315 rows, and 7,315 is the exact row count this seat recorded on
  2026-08-29 for the status value `REFUSED-NO-BMV`.** That is a **match on a count, which is a
  pointer, not an identification** -- it says where to look, and the vocabulary census that produced
  that number covered 37 partitions, not 535.

## Why a 37-partition slice could never have found this

The prior window loaded 37 recent partitions. **Two of the three affected dates lie outside any
recent slice** (2024-07-08, 2025-01-09), and the third (2026-08-18) sits inside a 37-day window --
but a *single-partition* or narrow load casts cleanly on its own and only **conflicts when unioned
with a `double`-typed partition.** The failure is a property of the UNION, so it is structurally
invisible to every load smaller than one that spans both types. **An estimate extrapolated from a
slice cannot see a defect that only exists at full span.**

## What this changes for the census design (BP1-4)

1. **The census MUST pass an explicit schema** (or cast `r_net`/`r_gross` to `double` per fragment).
   A bare `to_table()` over the full history does not run. This is a one-line fix and it is the
   entire reason to have measured rather than estimated.
2. **Three dates contribute ZERO linkable returns for EVERY account.** In the linker's own
   vocabulary those are neutral days, and `days_linked` vs `calendar_days` is precisely the
   discriminator convention **C1** turns on -- so a full-history parity run must state which of the
   two it counted across these dates. It does not change any return; it changes a day count.
3. **The runtime estimate stands and is not the constraint**: 118.2 MB, 535 partitions, metadata pass
   67.8s. Seconds-to-a-minute class, exactly as extrapolated. **The extrapolation was right about the
   thing it measured and silent about the thing that matters.**

## Bounds

- This measures **our** gold plane only. **No BD figure exists yet**; nothing here touches the parity
  comparison's other half, and no vendor call was made.
- The cause of the two interior all-null dates is **UNESTABLISHED**. The `REFUSED-NO-BMV` count match
  is a lead with a stated denominator gap (37 vs 535), not a finding.
- One instrument (pyarrow/s3fs) read the schema; the row-level counts were re-read from the same
  files. **The all-null claim is corroborated by a positive control on an adjacent partition**, which
  is a different subject, not a different instrument.
