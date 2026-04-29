# Task Order: ADVI_INFLEC.DIAGFIX.009 — Holdings Pricing Strategy
## DS: Investigate Orion daily position/MV endpoints + define A/B/C pricing fallback

**ID:** ADVI_INFLEC.DIAGFIX.009
**Issued by:** 2.0.0_SA_COO via 0.6.1_AE_PartnerETL
**Issued to:** 0.4.0_DS_ClientPlatform
**Date:** 2026-04-29
**Priority:** HIGH — gates correct daily timeseries AUA in all lookback views
**Status:** open

---

## Problem statement

The INF pipeline currently reconstructs position market values in INF_B_00 as
`market_value = units × nav_price`, where `nav_price` is sourced from the Orion TRN
(transaction) feed using "last seen wins" logic. This is architecturally wrong:

- TRN rows include non-trade events (advisory fee debits, journal entries, income
  distributions) with `nav_price = 0`. Under "last seen wins," these corrupt the price
  for the affected (account, ticker) pair going forward.
- Even with the nav_price guard fix deployed today (`if nav > 0: update`), the price
  used is the price AT THE LAST TRADE — which may be days or weeks stale.
- Result: holdings market_value sum was $89.6M against an authoritative managed AUM of
  $182.6M. After today's guard fix, holdings = $190.5M (overcorrection from stale prices)
  vs aum_snapshot = $182.6M.

**The TRN feed is not a price source. It never was. We are using it as one.**

For aggregate AUA views (donut totals, leaderboard, partner_analytics) we have already
fixed the source to `aum_snapshot.managed_value` (the Orion AUM API reconciled number).
This TO addresses the deeper problem: position-level daily market values for timeseries,
concentration_risk, and composition — which all need correct per-position dollars, not
just firm totals.

Andrew direction 2026-04-29:
> "if they have time series that accounts for nav value on a daily basis then awesome
> lets grab it right from the source. if they do not have that, then the simple mechanism
> is what we do for 49financial whereby there are type A B and C assets"

---

## Scope

### Phase 1 — Orion endpoint investigation (target: 1-2h)

We already have the Orion Envision API working end-to-end:
- Pattern: `POST /api/v1/Reporting/Envision/ExcelReports/Verbose` → Generate → GET CSV
- `pull_inflection_positions.py` already pulls `Activity.Value(activityOptionId=1)`
  (Ending Market Value) per account × asset with a Rolling 3-Year date range
- `PATH_DISCOVERY.md` confirms `DateRange.StartDate` / `DateRange.EndDate` are working

**Questions to answer:**

1. **Granularity**: Does the returned data have one row per (account, asset, DATE) — i.e.
   daily EndingMV — or is it one row per (account, asset) with a single period-end value?
   Run a short probe: pull activityOptionId=1 for a 30-day window and count distinct
   `DateRange.StartDate` or `DateRange.EndDate` values per (account, ticker). If >1 date
   per account/ticker, the feed is sub-period. If =1, it's period-end only.

2. **Coverage**: Does every position have a non-null EndingMV for every date in the window,
   or are there gaps (positions with no activity in a period)?

3. **Ticker linkage**: Can we reliably join the position EndingMV rows back to ticker/CUSIP
   for classification? (Asset.Ticker + Asset.Name are already confirmed in the pull.)

4. **Historical depth**: How far back does the EndingMV data go for Inflection? Confirm
   whether 3 years of daily data is available or if there are gaps pre-2022.

**Probe script**: extend or fork `pull_inflection_positions.py` to pull a narrow 30-day
window and write the raw result to S3 at `bronze/orion-api/probe/positions_mv_30d.csv`.
Inspect the row structure and report findings.

---

### Phase 2 — Pricing strategy decision (based on Phase 1 findings)

**Path A — Orion has daily per-position EndingMV:**

Design a new silver layer: `silver/positions_mv/snapshot_date={date}/data.parquet`
where each row is (account_id, ticker, date, ending_mv, units) pulled from Orion daily.

INF_B_00 (or a new INF_B_00b) uses `ending_mv` directly instead of `units × nav_price`.
This eliminates TRN-based price reconstruction entirely.

Estimate: 1-2 sprint days to design + implement + wire into B-chain.

**Path B — Orion has only period-end values (quarterly/monthly):**

Adapt the BD pipeline's A/B/C pricing approach for INF:

| Type | Definition | Price source |
|------|-----------|--------------|
| A | Liquid, publicly traded — ETFs, mutual funds, equities with public ticker | Yahoo Finance daily EOD close (same as BD `build_canonical_prices_v2.py` T2 source) |
| B | Illiquid or non-public — alternatives, structured notes, private funds | Orion period-end EndingMV carry-forward; linear interpolation between known dates (same as BD T3/T4) |
| C | Cash / money market | Face value ($1.00 per unit) or Orion cash balance direct |

Reference BD implementation:
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py` — full T1→T2→T3→T4 tier
  resolution with SOURCE_RANK priority system
- `data/black_diamond/scripts/gold/bd_price_update.py` — incremental daily price update
- `data/black_diamond/lib/etf_classifier.py` — ticker classification for bucket assignment

For Inflection, the Type A/B/C bucket assignment should use the Orion-native
`product_category` + `asset_class` already landed in `silver/api_dims/assets_v2/`
(INF_I_D03 now uses this). No separate ETFClassifier or bd-securities DDB needed.

Estimate: 3-5 sprint days to adapt BD pricing pipeline for INF, including Yahoo Finance
ticker validation against the Inflection holdings universe.

---

## Deliverables

1. **Phase 1 probe results** — RAVC to COO + AE with:
   - Granularity finding (daily vs period-end)
   - Coverage gaps if any
   - Historical depth confirmation
   - Raw probe CSV in S3 (`bronze/orion-api/probe/positions_mv_30d.csv`)

2. **Recommendation** — Path A or Path B with rationale and effort estimate

3. **If Path A**: Draft INF_B_00b design (inputs/outputs/S3 keys) for AE review before
   implementation

4. **If Path B**: Ticker universe audit — list every distinct ticker in Inflection holdings
   and classify each as Type A/B/C using the assets_v2 classification already built. Flag
   any tickers that Yahoo Finance cannot price (will need Path B/C treatment).

---

## Constraints

- **Do NOT modify INF_B_00 or the B-chain until Phase 1 findings are in.** The guard fix
  (`if nav > 0`) deployed today is stable enough for current portal use. Do not break it.
- **aum_snapshot remains the authoritative AUA source for all aggregate views.** This TO
  only affects position-level market values (timeseries, concentration, composition).
- Investigation only in Phase 1. No silver writes until COO approves the path.

---

## References

- `data/orion/manual_api/pull_inflection_positions.py` — existing EndingMV pull
- `data/orion/manual_api/PATH_DISCOVERY.md` — confirmed Orion Envision API paths
- `data/black_diamond/scripts/gold/build_canonical_prices_v2.py` — BD A/B/C reference
- `data/black_diamond/scripts/gold/bd_price_update.py` — BD incremental price update
- DIAGFIX.001 session log — root cause analysis of $89.6M vs $182.6M gap
- Andrew direction: "nav value on a daily basis — grab it from the source; otherwise
  type A/B/C as with 49Financial" (2026-04-29)
