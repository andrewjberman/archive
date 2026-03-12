# ADVI_PSCFIX — COO Briefing

**From:** 1.0.0_SA_CTO
**Date:** 2026-03-11
**PRD:** `docs/architecture/ADVI_PSCFIX_PRD.md`
**Project JSON:** `org/projects/ADVI_PSCFIX.json`

---

## What This Fixes

Two correctness defects in the AUA view of Advisor Intelligence Assets Overview,
both fixable before launch. ADVI is not live — no migration constraints.

**Defect 1 — Wrong NMNC/NMEC definition.**
The AUA stacked bar currently uses a rolling 12-month window to classify clients.
It should use a static period-bound definition: NMNC = clients who joined during
the displayed bar's exact period; NMEC = everyone else. A client who joins in Nov
2025 shows as NMNC in the Q4'25 bar and NMEC in all subsequent bars. The current
implementation keeps them NMNC for 12 months — wrong.

**Defect 2 — Total AUA doesn't match BD's official number.**
The portal's Total AUA is derived from our transaction reconstruction (positions
cube × canonical prices). BD's own daily allocation snapshot says $1,599M; we show
$1,605M. Every "Total AUA" display in the portal needs to show the BD number.

---

## Two Parallel Tracks

### Track A — Pipeline (DS + AE)

**AE task (`0.6.0_AE_PartnerETL`):**
Write `data/black_diamond/scripts/gold/05d_write_aua_certification.py`.
Runs daily in the EC2 gold runner after `05c`. Reads `silver/allocations/{date}.parquet`,
sums `account_market_value`, writes `gold/aua_certification/{date}.json`:
`{"date": "...", "certified_aua": 1599225407.0, "gold_aua": ..., "gap_pct": ...}`.
Non-blocking — if no silver file exists, script exits cleanly with a SKIP log.
Wire it into `run_all.sh` after the 05c step.

**DS task (`0.4.0_DS_ClientPlatform`):**
Restructure `bd-portal-publisher` Lambda's `build_timeseries_chart()` function.
Replaces the current single rolling-12M daily AUA series with three pre-aggregated
period-level series (quarterly, monthly, annually) using the static definition.
Also: load `gold/aua_certification/{today}.json` at publisher startup and apply
the certified total to every `total_aua` field the publisher outputs — specifically:
- `timeseries_chart.json → aua.{gran}.data[-1]` NMNC+NMEC scaled proportionally
- `summary/header_metrics.json → total_aua`
- `snapshots/aua_by_{dimension}.json → total_aua` (all four dimension snapshots)
- `partner_analytics/header_metrics_{gran}.json → views.aua/geo/adv.current.donut.total`
Segment-level AUA values (by architect, by state, etc.) stay unchanged.
Full spec is in the PRD. DS delivers implementation; DT deploys the Lambda.

### Track B — Portal (DE, can start immediately with mock data)

**DE task (`0.4.0_DE_ClientPlatform`):**
Update `PartnerAnalytics.tsx` to consume the new `aua.{granularity}.data` schema
instead of the current `aua.data` daily series. The `fullPeriodMap` aggregation
loop for the AUA view is eliminated — backend now delivers pre-aggregated period
data. Frontend reads `timeseriesData.aua[granularity].data` directly and applies
only the time-window filter. Update `CumulativeChartDataPoint` type in `types.ts`
to add `period`, `label`, `end_date` fields. NNA aggregation logic is untouched.

---

## Dependencies

- Track B can begin with a mock JSON matching the new schema — no dependency on Track A
- Track A DT deploy unblocks Track B integration testing
- `05d` (AE) and DS publisher spec are independent — can run in parallel within Track A
- No thread needed. Task orders to three agents sufficient.

---

## Definition Guard (put this in every task order)

There are two NMNC/NMEC definitions. They must never share a rendering path:
- **Static** (period-bound): what ADVI Assets Overview uses
- **Rolling/gradient** (trailing 12M): reserved, not wired to any v1 view

DS must preserve the rolling definition as a code comment in the publisher
(`aua_rolling` key, future use). It must not appear in `timeseries_chart.json → aua`.
