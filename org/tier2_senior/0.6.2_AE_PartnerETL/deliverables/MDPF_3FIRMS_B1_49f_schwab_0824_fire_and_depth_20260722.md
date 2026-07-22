# TO 3F-B1 — 49F/Schwab 0824: Fire Evidence, Sweep Coupling, Depth Statement

**Agent:** 0.6.2_AE_PartnerETL~A · **Date:** 2026-07-22 ~21:1xZ · **Basis:** `schwab-rps` (0824 Model
Portfolios master). **Standing prohibitions restated:** 0824 and 0833 are NEVER SUMMED **and** NEVER
SUBSTITUTED (0833 = Advisor Intelligence master; a law about addition cannot license a selection). Nothing
here blends or selects across them. Ancient-depth half DEPRIORITIZED per Andrew @0b06b5a14 — stated as
facts below, not worked.

## (a) Fire history — evidence, not configuration

Rules (applied truth, describe-rule verbatim):
- `canonical-schwab-si2-08242234-daily-pull`: `ENABLED`, `cron(15 10,22 * * ? *)`
- `opal-assets-silver-schwab-sweep-daily`: `ENABLED`, `cron(15 12 * * ? *)`

CloudWatch `AWS/Events TriggeredRules`, window 2026-06-22..07-22 (30 days, daily period):

```
pull  : 17 fires / 9 days —  07-13: 1, then 2/day every day 07-14..07-21 (weekends included)
sweep :  9 fires / 9 days —  1/day every day 07-13..07-21
```

**The honest denominator: the rules have existed for 9 days, not 30.** Zero datapoints exist before
2026-07-13 because the rules were created mid-day 07-13 (first day shows 1 pull fire). Within their
lifetime: **zero missed fires** on either rule — the pull's 2/day and the sweep's 1/day are complete,
including weekends (these rules fire on calendar days; trading-day interpretation applies to the DATA,
not the schedule). The pre-07-13 silver history was landed by the backfill conversion path, not this
daily mechanism — so "30-day fire history" resolves to "complete fire history over the mechanism's
lifetime + a backfill-provenance floor for everything older."

## (b) Silver-sweep coupling — the chain completes

Frontier partition `schwab/08242234/silver/fact_rps_s2/date=2026-07-21/` carries LastModified
**2026-07-22T10:16:01Z** — sixty seconds after the 10:15Z pull fire. The conversion is EVENT-DRIVEN at
landing; the 12:15Z sweep is the backstop (same pattern measured on the COT leg in 3F-B5: land -> convert
in seconds). Pull -> convert -> partition is demonstrated end-to-end on the live frontier, not inferred
from two rules existing.

## (c) Depth statement + census (denominators printed)

- Partition census: **540 date partitions**, floor `date=2024-05-24`, frontier `date=2026-07-21` —
  exactly the TO's expected floor/frontier.
- **30-day trading census (2026-06-22..07-21): 21 of 21 expected trading days present, zero missing,
  zero non-trading extras.** Expected set derived from `lib/trading_calendar.py`.
- Reconciled with DS's 3F-S2 census (@58d24b18e, cross-domain clause): DS measured the same table at 540
  dates, ZERO mid-series gaps, 539/539 trading-day coverage + one off-cadence extra 2025-01-09 (Carter
  mourning day — vendor delivered, silver faithfully mirrors; outside my 30-day window). 539 + 1 = 540 —
  the two censuses reconcile exactly.
- **The two floors reconcile as DESIGN, not defect:** the gold spec's "427 dates from 2024-11-01" is the
  served display floor (`SERVED_AS_OF_FIRST = "2024-11-01"`,
  `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py:114 @HEAD`) — the axis the chart renders.
  Silver's 2024-05-24 floor EXCEEDS the display requirement by ~5.5 months of buffer. Vendor-side depth:
  bronze `rps/` floor is 2024-01-12 (632 dates, DS S2); the 92-date bronze-not-silver head gap
  (2024-01-12..2024-05-23, contiguous) sits ENTIRELY below the display floor and is deprioritized per
  Andrew ("not a huge priority to get super ancient stuff"). Stated, not worked.

## (4) Andrew's "good condition on backfill" read: **CONFIRMED, with evidence**

- Zero missing trading days in the 30-day census (21/21).
- Zero mid-series gaps across the full 540-date series (DS S2, reconciled above).
- Silver depth exceeds the display floor by ~5.5 months; the only depth deficit (the 92-date head gap)
  is wholly below what the chart displays.
- The live mechanism has zero missed fires in its lifetime and converts within a minute of landing.
Nothing in the evidence refutes his read; the confirmation is measured, not inherited.

## Phase-1 comp-freshness note

Same project-wide finding as B3/B7: the 49F leg entries render flat-hours (no
`freshness_basis: trading-day-frontier` cadence entry). Recorded, no staleness raised (NEVER#1) — this is
the gap CTO GO'd to 0.7.0 at 210957Z (commit-only tonight), with the B5 `tdb<=2` COT measurement folded.
