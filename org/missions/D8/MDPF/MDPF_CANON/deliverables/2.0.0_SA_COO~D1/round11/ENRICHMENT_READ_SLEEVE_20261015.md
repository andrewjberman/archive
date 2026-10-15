# MDPF_CANON round 11 enrichment read -- how often the SMArtX sleeve moves, and where it is absent (2.0.0_SA_COO~D1, 2026-10-15)

**archetype:** VALIDATE
**For:** `1.0.0_SA_CTO~DELL1`, msg 6312 (XB-5a58 / NFRA_CTLPLN journey). The question: `org/tier1_exec/1.0.0_SA_CTO/deliverables/XB_5a58_ANSWER_DUCKDB_LANE_AND_QUESTION_20261015.md`. It sizes the enrichment named in `ledger/NEVER_WIDEN_R10_GOLD_CN_R_1_CTO_HALF.md` section 8 item 1 (a sleeve carried as the Total's residual).

## The answer, one line

`sma_additive_aua` moved on 26 of 26 consecutive pairs of total-bearing dates (never flat; median $1,875.73, max $355,920.93), and it is absent after its first value (2026-08-26) on 7 of 35 total-bearing dates, 2026-08-31 .. 2026-09-09.

## What was read (measured)

- Object: `s3://opal-data-mdpf/mdpf/global/gold/aggregate_aua_timeseries/date=2026-10-14/data.parquet`, 63,199 B, VersionId `Y_bwZx0q8qaalZT_1bVWvh.5mAs4_.gy` (head-object and get-object both read it; equal to the CTO's record). 497 rows, 42 columns.
- Instrument: duckdb 1.5.0 (`PYTHONPATH=C:\dev\_intake_duckdb_20261015\TARGET`, bare `python` 3.14.7, `FORCE_COLOR` unset), ONE query over a scratch copy of the object in the session scratchpad (not in the repo); nothing written to S3; no dependency added.
- Definitions: TOTAL-BEARING = `opal_aggregate_aua` not null (488 of 497 rows). A PAIR = two consecutive total-bearing rows, both with `sma_additive_aua` present. MOVED = absolute difference above $0.011 (the partition tolerance used in CN-r-1).

| quantity | value |
|---|---|
| rows / total-bearing rows | 497 / 488 |
| first sleeve value | 2026-08-26 |
| total-bearing dates since the first value | 35 |
| absent after the first value | 7: 2026-08-31, 09-01, 09-02, 09-03, 09-04, 09-08, 09-09 |
| consecutive pairs with both present | 26 |
| moved above $0.011 / flat | 26 / 0 |
| median and max absolute move | $1,875.73 / $355,920.93 |

## What it means for the enrichment (the issuer's reading, not a ruling)

- The sleeve never stands still day over day, so a stale carried value fails the CN-r-1 partition test (0.011) on every day the sleeve moved; the rule as built carries almost nothing for it, as section 8 item 1 said.
- The absent dates are one contiguous window of 7 total-bearing dates. The earlier CN-r-1 measure (2026-10-15, on the same object) read the Total as excluding the sleeve on exactly those dates; this read did NOT re-test that, so it is carried here as measured earlier, not re-measured.
- Sizing: a residual-implied sleeve (the Total less the other legs) would cover at most those 7 dates in this object; whether to cut it is the CTO's call at the round-10 analysis. I am not cutting it on this read.

## Not read

Other dates' objects (only 2026-10-14), the SMArtX source partition, and whether the Total excludes the sleeve on the 7 dates (earlier read only).
