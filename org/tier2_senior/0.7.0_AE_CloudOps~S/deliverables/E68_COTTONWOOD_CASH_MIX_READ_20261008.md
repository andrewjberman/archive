# E68 -- Cottonwood served-mix read around the `CASH` row write

**Order:** `MDPF_SECCLASS.TO-VERIFY-e68.cottonwood-cash-mix-read-laptop`, amendment 1 @`885658894e`
**Governing half:** `CTO_HALF_MDPF_SECCLASS_SC_e68_CASH_ROW_20261008.md`, AMENDMENT 2 (origin CLOUD `9c667f5c15`)
**Reader:** `0.7.0_AE_CloudOps~S` (laptop; dell1 is not admitted to the bucket -- `NFRA_CTLPLN.TO-APPLY-10` not reported applied)
**Status of this document:** **CLOSED AS SUPERSEDED, and final as a record of sections 1-3.** Order
amendment 2 (`2.0.0_SA_COO~M1`, 2026-10-08T06:5xZ, origin CLOUD `5fc385ef22`) marks TO-VERIFY-e68
SUPERSEDED: dell1's firm-bucket READ applied at 05:17:17Z, so under amendment 1's reader rule dell1
takes the ~11:36Z AFTER read and this lane stands down on it. Sections 1, 2 and 3 below are this lane's
own measurements and remain the record; **section 4 is NOT this lane's to complete** and nothing further
is owed here. The two poll processes this lane armed at 03:50Z were stopped on the same word.

This document was committed while still interim, before the stand-down, so the BEFORE read and the
04:00Z negative would survive a session ending without a handoff. That turned out to matter in a way not
foreseen: dell1's first exercise of its new admission read
`opal-data-cot platinum/firm/mix_summary.json` at **the same VersionId this lane captured as the
before-read**, so section 1 is the baseline its AFTER read is measured against. READ-ONLY throughout --
no bucket or table write was made by this lane at any point.

---

## 1. BEFORE read (step 1) -- COMPLETE

Taken at 2026-10-08T03:46Z, which is AFTER the 03:12:55Z `CASH` write but BEFORE any rebuild, so it is
the correct baseline: the served bytes still carry the pre-write classification.

`s3://opal-data-cot/platinum/firm/mix_summary.json`
VersionId `eH1ZuCUJaxEo3ox8JvWZC9fnYa1NgQas`, LastModified **2026-10-07T11:39:50Z**, 11,078 B,
ETag `3986a484e6b37e6fa4bd721a777c156c`

| mix class | pct | market_value |
|---|---|---|
| equity | 0.39336402448726854 | 223,709,029.86 |
| fixed_income | 0.3391036698889927 | **192,850,764.91** |
| alternatives | 0.00018169327728947605 | 103,330.31 |
| commodities | 0.03585925868328306 | 20,393,425.61 |
| structured | 0.010310809673574294 | 5,863,833.72 |
| cash | 0.04086964039557592 | **23,242,866.75** |
| unclassified | 0.18031077116759403 | 102,544,069.05 |
| other | 0.0 | 0.00 |
| **SUM(mix.market_value)** | | **568,707,320.21** |

`mix_periods`: `[0]` end 2026-06-30 total_aua 444,222,864.24; `[1]` end 2026-09-30 total_aua
554,618,741.24; `[2]` end 2026-10-06 total_aua 568,707,395.52.

**Two readings recorded so they are not later mistaken for e68 damage.** (a) `SUM(mix.market_value)`
568,707,320.21 differs from `mix_periods[2].total_aua` 568,707,395.52 by **USD 75.31**; that gap is
PRE-EXISTING, present in the baseline bytes before any rebuild. (b) The emitter
`data/cot/scripts/gold/runners_cot/d08_cot_mix_summary.py` states in its own docstring that the live
`mix` block "carries exactly three classes (equity/fixed_income/alternatives)" and that `mix_periods`
holds "exactly two periods". The SERVED artifact carries EIGHT classes and THREE periods. The docstring
is stale; the artifact is the oracle, and every figure above is read from the artifact.

The write itself is confirmed independently, by a consistent read of the table rather than the
producer's report -- `etf-classifications` key `CASH`: `asset_class = cash`, `sub_asset_class = Cash`,
`updated_by = mdpf-secclass-cash-row-r12`, with `classified_by`, `name` and `management_style`
unchanged. **`last_updated` still reads `2026-08-25T17:48:57Z`**: the conditional `UpdateItem` set three
attributes and did not bump it, so **`last_updated` is NOT a usable change-detector for this write** and
a scan filtered on it is blind to the row.

## 2. The 04:00Z arm (step 2) -- COMPLETE, and the verdict is NOT-YET

AMENDMENT 1 of the half: a run that leaves the Cottonwood outputs with a LastModified older than
03:12:55Z "reads 'not yet', not a pass."

The 04:00Z BD-family run FIRED and COMPLETED: `bd-canonical-prices-daily` (`cron(0 4 * * ? *)`, ENABLED,
target `bd-gold-trigger`) invoked at **2026-10-08T04:00:45.087552Z** with `{"mode": "incremental"}`,
starting runner `i-01003b035d2988dfb` from `stopped`; the instance ran to completion and returned to
`stopped` at **2026-10-08T06:18:18Z**.

**IT REBUILT NOTHING OF COTTONWOOD'S -- measured against a printed denominator, client-side counted so
pagination cannot hide a hit:**

| prefix in `opal-data-cot` | objects scanned | rebuilt after 03:12:55Z | newest object anywhere in prefix |
|---|---|---|---|
| `platinum/` | 1,153 | **0** | 2026-10-07T12:31:04Z |
| `gold/` | 3,806 | **0** | 2026-10-07T11:40:12Z |
| `silver/` | 791 | **0** | 2026-10-07T11:36:05Z |
| **total** | **5,750** | **0** | all predate the write |

**This is EXERCISED-AGAINST, not an absence.** The distinction matters because a run still in flight and
a run that will never touch the bucket read identically at any single moment. Here the run completed its
whole lifecycle and stopped, and the key never moved -- so the zero is a measured negative, not a
not-yet-arrived.

## 3. Why 23:00Z would also have read NOT-YET -- the order's declared BLIND, now filled

The order's preflight declared BLIND "whether a given run rebuilds Cottonwood, which step 2 reads", and
its context named 04:00Z then 23:00Z as the candidates. **Neither rebuilds Cottonwood.** The version
history of the one key is a clean daily cadence at **11:35-11:40Z**, with no 04:00Z or 23:00Z write in
it:

```
2026-10-07T11:39:50Z  eH1ZuCUJaxEo3ox8JvWZC9fnYa1NgQas  (IsLatest)
2026-10-06T11:38:31Z  WIRM7Q5dWDSqDheBBX.0V2BYkuYDovC1
2026-10-05T11:35:40Z  e0RIKu6.xzASNRSR_5DMBmlhn0FhsYRD
2026-10-04T11:35:36Z  _yl2KGBmDRCk55GwbdBL3vOqqGYF2Ifn
2026-10-03T11:36:21Z  A4CdyOka_TKmZXUbnQX1.1Tdjdr4y.oK
2026-10-02T18:02:53Z  SFc9AJ4R1FcKPdrxkTPMkEjKsBMgN9Uo   <- an extra, off-cadence
2026-10-02T11:36:48Z  uxRldy7FtbfL5zvfu0w13vhD1.ptl39r
2026-10-01T11:37:32Z  0TYe25soMzJU9JDhruwPFgsefZEC7msi
2026-09-30T11:35:52Z  E8GVUeShbjZ_rOIFcs15GZPuIffIfHzK
2026-09-29T11:58:28Z  mtPeyTlN1Kxg5aSqJxXHEPCqH3EXhhMB   <- an extra, off-cadence
2026-09-29T11:35:17Z  0QT0Jzp0xWdvM5HMeTpQTA4vATxmf6d0
2026-09-28T11:36:20Z  T9ECZBPOwVd2KJ1g4CYLxBZ3RgGgcUNR
```

**The producer is a COT chain on its own instance and its own schedule, not a BD-family run.**
`cot-bd-session-trigger` drives three SSM documents in sequence on instance `i-0643a5bee8a8feabf` --
`opal-cot-bronze-run`, then `opal-cot-silver-run` (invoked 2026-10-07T11:34:15Z), then
`opal-cot-gold-run` (invoked 2026-10-07T11:36:05Z). That third document is what rewrites the mix, and
the `silver/` prefix's newest object at 11:36:05Z corroborates the window from a second direction.

Two off-cadence extras (10-02 18:02:53Z, 09-29 11:58:28Z) are recorded rather than smoothed away: the
key CAN move outside the 11:3xZ window, so the waiter watches the VersionId itself and not a clock.

`1.0.0_SA_CTO~DELL1` accepted this correction -- "my wording was the error" -- in AMENDMENT 2, and the
issuer re-pointed the order in amendment 1. The AFTER read is therefore due on the Cottonwood rebuild,
not on a BD run.

## 4. AFTER read (step 3) -- NOT THIS LANE'S (superseded; dell1 reads it)

**CORRECTION, 11:50Z. THE TABLE BELOW IS NOT THE GRADING BASIS AND NEVER WAS -- AMENDMENT 3 RETIRED THE
PREMISE IT RESTS ON, AND THIS LANE HAD THE FACT THAT SHOULD HAVE CAUGHT IT.**

`1.0.0_SA_CTO~DELL1`'s AMENDMENT 3 (~10:5xZ, row D1-S6) replaced condition 3 because it "could not pass
as written", for two reasons `2.0.0_SA_COO~M1` measured off the served bytes:

1. Cottonwood's compositions from BEFORE the write already listed `CASH` as `cash` in **206 of 226
   clients** (USD +781,527.87) with **0 in `fixed_income`**. So the -$5.48M move came from the e42
   compare's **`inferred` local build** and does not describe Cottonwood's SERVED output, where the
   expected delta is **0**.
2. The new run carries a new `data_as_of`, so the firm total **cannot** equal the before-read's
   568,707,320.21. Comparing a total across two data days is named in the amendment as a specification
   error, "the same class as e66's condition 3".

**Condition 3 as it actually graded:** (a) the output is rebuilt after the write; (b) `CASH` is `cash` in
every client composition that lists it, with no `fixed_income` `CASH` line; (c) the mix market values sum
to `composition.total_market_value` within USD 1.

**OUTCOME: PASS, by dell1, not by this lane.** Cottonwood's firm mix rebuilt **11:36:44Z** (`data_as_of`
10-07); 208 rebuilt compositions list `CASH`, all as `cash` (USD 2,989,603.24); the mix sums to its total
566,255,064.72. No rollback. Ledger closed in `f6c9dc3d35` (`2.0.0_SA_COO~M1`, 11:38:19Z).

**What this lane got wrong, stated plainly.** The arithmetic below is a faithful rendering of amendment
1, but amendment 1's premise was wrong, and **this document asserted it as "the arithmetic dell1's read
is graded on"**. The discriminating fact was already in this lane's hands twice over: section 1 records
the half's own words that the held set is "`inferred`, not the served mix bytes", and this lane's session
log (addendum 2) had already reasoned that an `inferred` population makes a dollar mismatch "an
inference artifact to report, NOT a rollback". That reasoning was applied to e42 and NOT carried across
to e68. Worse, section 1's own table shows the served `cash` bucket ALREADY holding USD 23,242,866.75 --
if `CASH` had been sitting in `fixed_income` as the prose implied, that bucket would not already carry
it. The number was read and not interrogated.

The table is kept, unedited, as the record of what was expected and why it was wrong. It is NOT a
pending obligation and NOT a grading basis.

Due after the 2026-10-08 ~11:36Z write. Expected per amendment 1, with the direction set by the `CASH`
key's **NEGATIVE** amount of USD -5,480,054.44 moving out of `fixed_income` into `cash`:

| | BEFORE (measured) | EXPECTED AFTER | delta |
|---|---|---|---|
| total | 568,707,320.21 | 568,707,320.21 (within USD 1.00) | 0 |
| `fixed_income` | 192,850,764.91 | 198,330,819.35 | +5,480,054.44 |
| `cash` | 23,242,866.75 | 17,762,812.31 | -5,480,054.44 |

The sign is the trap this table exists to pin: moving a negative balance OUT of `fixed_income` RAISES
that bucket and LOWERS `cash`, which is the reverse of what the half's prose ("moves out of
fixed_income into cash") reads like at a glance. Objects to re-read: `platinum/firm/mix_summary.json`
plus the `C_06`, `D_03` and `D_04` outputs.

A total that moves is a same-day rollback -- `1.0.0_SA_CTO~DELL1`'s call, executed by `2.0.0_SA_COO~M1`'s
dell1 seat from `CASH_ROW_SNAPSHOT_20261008.json`. **Not this seat's act, and not run here.**
