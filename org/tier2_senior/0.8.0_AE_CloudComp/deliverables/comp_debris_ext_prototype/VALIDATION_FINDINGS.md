# comp-debris extension prototype -- LIVE validation findings (2026-07-17)

**Author:** 0.8.0_AE_CloudComp · Prototype: `comp_debris_ext.py` · Design: `../COMP_DEBRIS_EXTENSION_DESIGN_20260717.md` @c9a221dbb

The prototype validates the design against LIVE AWS. It imports `comp_debris.classify/BANDS/_HELD_RX`
and reuses them VERBATIM -- proving the "one classify(), N adapters" architecture literally.

## Result: the architecture holds across all 4 new types
- **Offline self-test: 7/7 PASS** (band mutants per type; reuses `cd.classify`).
- **Live `--types ddb,s3`:** 75 resources -> HOT=44 COLD-DORMANT=10 STILLBORN-OR-GUARD=16 UNKNOWN=5, 0 held.
  - Metric pattern generalizes to DDB (ConsumedRead+WriteCapacity): `opal-partner-49financial` 19d, `market-updates` 9d.
  - **S3 write-cold works FREE via the storage-delta:** `opal-data-smartx-v2` 28d, `opal-data-imo` 20d write-cold.
  - STILLBORN-OR-GUARD correctly separates never-active-old guards (`opal-users`, `opal-firms`, `opal-market-data-v2`) from the reap rank.
- **Live `--types ec2,events`:** 179 resources -> HOT=135 COLD-DORMANT=11 UNKNOWN=27, **6 held EXCLUDED** (_HELD_RX working).
- **signal_basis printed on every row**; **UNKNOWN never collapses to cold**; **hold-aware** confirmed live.

## DISCOVERED REFINEMENT (the valuable catch): scheduled rules need CADENCE-AWARE windowing
Live, the EventBridge adapter flagged `fred-ingestion-monthly-late` COLD-DORMANT at **23d** -- but it is a
**MONTHLY** rule, so 23 days since its last fire is **WITHIN CADENCE, not dormant.** Meanwhile
`bd-49f-fees-runner-daily` at **21d** IS a real finding (a *daily* runner should never be 21d cold).
**The cadence is the discriminator -- a flat 7d-hot / 30d-window mis-bands every monthly/weekly rule.**

This is the SAME CLASS as the two controls the design already names:
- never-invoked != cold (split by creation age);
- **T-1/trading-calendar** for data buckets (coldness judged against the *expected* cadence, not wall-clock).

**Design amendment (for the production build):** the EVENT_RULE + SCHEDULE adapter must read each rule's
`ScheduleExpression` (`rate(...)`/`cron(...)`) and judge HOT/COLD relative to the cadence (fired within
~1 cadence-period + slack), never a flat window. A monthly rule cold for 23d is HEALTHY; a daily runner cold
for 21d is a candidate. Absent this, the tool false-alarms exactly the resources that fire rarely BY DESIGN --
the STILLBORN-OR-GUARD refinement, one level up, on the time axis. **This is the single most important
addition the live run surfaced.**

## Honesty caveats carried (NOT findings, per discipline)
- **NEVER#1 (T-1):** the data-bucket COLD-DORMANT rows (`opal-data-smartx-v2` 28d, `opal-data-imo` 20d) are
  ADVISORY candidates for the confirmation pass -- **NOT** stale-pipeline assertions. 28d write-cold is well
  beyond any weekend, so likely genuine dormancy, but the tool MUST count trading days and these route through
  the confirmation pass (comp-heat/dups/deadgrant/trigger/comp-similar) before any conclusion. No pipeline is
  called stale here.
- **EventBridge creation is UNKNOWN** (no rule-creation API) -> zero-activity rules land UNKNOWN (27), not
  STILLBORN-OR-GUARD -- honest (can't split TOO-YOUNG from dead without creation). Production seeds creation
  from the graph `snapshot_ts`.
- **EC2 idle != stopped:** idle instances (`i-070477bf35fc54409` 22d) carry a `PURPOSE-REVIEW` signal_basis,
  never a clean reap (design open-Q1).

## Status
- Prototype in the research lane; **production build lands in `comp_debris.py` at the ANY_EXEC engine home**
  (org/modules/graph/) -> build lane/CTO (same split as comp-similar -> ~D).
- Ready-to-fold amendments for the build: (1) cadence-aware windowing for scheduled rules [NEW, this run];
  (2) `lib/trading_calendar` for pipeline/data buckets; (3) graph-seed EventBridge creation; (4) EC2 idle
  threshold tuning.
