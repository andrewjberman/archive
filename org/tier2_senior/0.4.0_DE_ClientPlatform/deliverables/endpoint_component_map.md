# Advisor Intelligence — Endpoint-to-Component Map

**Agent:** 0.4.0_DE_ClientPlatform
**Task:** ADVI_REBORN.W1-005
**Date:** 2026-04-07
**Source:** portal/src/api/endpoints/advisor-intelligence.ts (35 functions)

---

## Active Endpoints (20)

### S3 Static Artifacts (CloudFront -> shared-advisor-router -> opal-data-{firm}/gold/)

| # | Function | S3 Key | Type | Component(s) | Key Fields Rendered |
|---|----------|--------|------|---------------|---------------------|
| 1 | `getHeaderMetrics` | `artifacts/summary/header_metrics.json` | `HeaderMetricsResponse` | DistributionTab | total (aua, nna_ytd/mtd), radial_12m (donut), account_distribution (histogram), by_architect |
| 2 | `getPartnerAnalytics` | `artifacts/partner_analytics/header_metrics_{granularity}.json` | `PartnerAnalyticsResponse` | AdvisorIntelligence (main page) | views.nna/geo/adv (donut + distribution + metrics), quarterly time machine (q0-q3) |
| 3 | `getCumulativeChart` | `artifacts/timeseries_chart.json` | `CumulativeChartResponse` | PartnerAnalytics, DistributionTab, AssetIntelligenceTab | aua (stacked bar), nna (diverging bar), geo/adv (cumulative lines), cla (lifecycle) |
| 4 | `getArchitectLeaderboard` | `artifacts/architect_leaderboard.json` | `LeaderboardResponse` | ClientsTab (N1) | entries[].name/nna/aua_growth_pct/new_clients, summary totals |
| 5 | `getAdvisorRollingFlows` | `artifacts/advisor_rolling_flows.json` | `AdvisorRollingFlowsResponse` | AdvisorsTab | summary.architects (MTD/QTD/YTD NNA), architects[] (rolling 30d/90d/1Y daily flows) |
| 6 | `getAdvisorFeeEfficiency` | `artifacts/advisor_fee_efficiency.json` | `FeeEfficiencyResponse` | FeeEfficiencyPanel (via ClientsTab N1) | advisors[].nna/revenue/aua/fee_yield/growth, regression (slope/R^2), windows.{period} |
| 7 | `getEmployeeLeaderboard` | `artifacts/employee_leaderboard.json` | `EmployeeLeaderboardResponse` | AdvisorsTab | windows.{period}.entries[].name/nna/aua/growth/role_breakdown, summary, regression |
| 8 | `getRelationshipMixViews` | `entities/clients/{id}_views.json` | `FirmMixViewsResponse` | ClientsTab (L3) | views.quarterly[] (last 5 quarters asset allocation) |
| 9 | `getRelationshipCompositionStatic` | `entities/clients/{id}_composition.json` | `BooksCompositionResponse` | ClientsTab (L3) | mix[] (asset class pct), concentration.items[] (top holdings) |

### Lambda Dynamic Endpoints (API Gateway -> Lambda)

| # | Function | Path | Type | Component(s) | Key Fields Rendered |
|---|----------|------|------|---------------|---------------------|
| 10 | `getSnapshot` | `/api/scoped/advisor-intelligence/snapshots/{dim}` | `SnapshotResponse` | AssetIntelligenceTab | data[].value/aua/aua_pct/client_count/account_count |
| 11 | `getClientsTab` | `/api/scoped/advisor-intelligence/clients-tab` | `ClientsTabResponse` | ClientsTab (N1) | headline (aua/accounts/clients/fee_rate), clients[] (dropdown), tax, income_fees |
| 12 | `getAdvisorBook` | `/api/scoped/advisor-intelligence/advisors/{id}/book` | `AdvisorBookResponse` | ClientsTab (L2) | summary (aua/clients/accounts), nna (ytd/qtd/mtd), tax_exposure, fee_summary, clients[] |
| 13 | `getBooksClientDetail` | `/api/scoped/advisor-intelligence/clients/{id}/detail` | `BooksClientDetailResponse` | ClientsTab (L3), ClientDetailPage | headline (aua/accounts), tax (cost_basis/gains/lots), fee_summary, accounts[] |
| 14 | `getBooksRelationshipTimeseries` | `/api/scoped/partners/books/relationship/{id}/timeseries` | `BooksTimeseriesResponse` | ClientsTab (L3) | data[] (AUA + cumulative flows daily timeseries) |
| 15 | `getBooksFirmComposition` | `/api/scoped/partners/books/firm/all/composition` | `BooksCompositionResponse` | ClientsTab (N1) | mix[] (asset class allocation), concentration (top N holdings) |
| 16 | `getBooksAdvisorComposition` | `/api/scoped/partners/books/advisor/{id}/composition` | `BooksCompositionResponse` | ClientsTab (L2) | mix[] + top_holdings[] (advisor-level) |
| 17 | `getBooksRelationshipComposition` | `/api/scoped/partners/books/relationship/{id}/composition` | `BooksCompositionResponse` | ClientsTab (L3, fallback) | mix[] + top_holdings[] (relationship-level) |
| 18 | `getBooksAccountComposition` | `/api/scoped/partners/books/account/{id}/composition` | `BooksCompositionResponse` | ClientsTab (L4) | mix[] + top_holdings[] (account-level) |
| 19 | `getFirmMixViews` | `/api/scoped/partners/books/firm/all/mix-views` | `FirmMixViewsResponse` | PartnerAnalytics, ClientsTab (N1) | views.quarterly/monthly/annually (asset class allocation over time) |
| 20 | `getAdvisorMixViews` | `/api/scoped/advisor-intelligence/advisors/{id}/mix-views` | `FirmMixViewsResponse` | ClientsTab (L2) | views.quarterly[] (advisor-level allocation, last 5 quarters) |

---

## Unused/Reserved Endpoints (15)

| # | Function | Path/Key | Status |
|---|----------|----------|--------|
| 1 | `getAllowedPartners` | `/api/partners` | Legacy — partner list |
| 2 | `getTimeSeries` | `timeseries/{dimension}` | Reserved — general dimension time series |
| 3 | `getFilters` | `filters` | Reserved — filter dimension definitions |
| 4 | `getClientGrowth` | `clients/growth` | Reserved — client growth metrics |
| 5 | `getTaxBreakdown` | `clients/tax-breakdown` | Reserved — tax pie charts |
| 6 | `getTaxDeferredCandidates` | `clients/tax-deferred` | Reserved — tax strategy candidates |
| 7 | `getHeaderSummary` | `artifacts/summary/header_metrics.json` | Superseded by getHeaderMetrics |
| 8 | `getClientDetail` | `clients/{id}/detail` | Superseded by getBooksClientDetail |
| 9 | `getImplementorLeaderboard` | `artifacts/implementor_leaderboard.json` | Superseded by getEmployeeLeaderboard |
| 10 | `getBooksAccountTimeseries` | `partners/books/account/{id}/timeseries` | Reserved — account-level timeseries |
| 11 | `getMixTimeseries` | `partners/books/relationship/{id}/mix-timeseries` | Used by ClientDetailPage MixTimeseriesPanel |
| 12 | `getFirmMixTimeseries` | `partners/books/relationship/0/mix-timeseries` | Wrapper — calls getMixTimeseries('0') |
| 13 | `getConcentrationTimeseries` | `partners/books/relationship/{id}/concentration-timeseries` | Used by ClientDetailPage ConcentrationPanel |
| 14 | `getAdvisorTimeseries` | `partners/books/advisor/{id}/timeseries` | Reserved — advisor AUA/NNA timeseries |
| 15 | `getAdvisorMixTimeseries` | `partners/books/advisor/{id}/mix-timeseries` | Reserved — advisor allocation timeseries |

Note: #11 and #13 are used by ClientDetailPage panels but not by the main BooksTab/ClientsTab.

---

## Component Consumption Summary

| Component | # Endpoints | Drill Level | Functions |
|-----------|-------------|-------------|-----------|
| AdvisorIntelligence (main) | 1 | - | getPartnerAnalytics |
| PartnerAnalytics | 2 | - | getCumulativeChart, getFirmMixViews |
| DistributionTab | 2 | - | getCumulativeChart, getHeaderMetrics |
| AssetIntelligenceTab | 2 | - | getSnapshot, getCumulativeChart |
| AdvisorsTab | 2 | - | getEmployeeLeaderboard, getAdvisorRollingFlows |
| ClientsTab/BooksTab (N1) | 5 | Firm | getClientsTab, getArchitectLeaderboard, getBooksFirmComposition, getFirmMixViews, getAdvisorFeeEfficiency |
| ClientsTab/BooksTab (L2) | 3 | Advisor | getAdvisorBook, getBooksAdvisorComposition, getAdvisorMixViews |
| ClientsTab/BooksTab (L3) | 4 | Relationship | getBooksClientDetail, getBooksRelationshipTimeseries, getRelationshipCompositionStatic (-> getBooksRelationshipComposition fallback), getRelationshipMixViews |
| ClientsTab/BooksTab (L4) | 1 | Account | getBooksAccountComposition |
| FeeEfficiencyPanel | 0 (via props) | N1 | Receives data from ClientsTab's getAdvisorFeeEfficiency call |
| ClientDetailPage | 1 | L3 | getBooksClientDetail |
| MixTimeseriesPanel | 1 | L3 | getMixTimeseries |
| ConcentrationPanel | 1 | L3 | getConcentrationTimeseries |

---

## Routing Patterns

**S3 artifacts** (`/api/scoped/advisor-intelligence/artifacts/*`):
- CloudFront behavior: `cloudfront-distribution.tf:212`
- Router: shared-advisor-router Lambda@Edge (origin-request)
- Auth: auth-validator-edge Lambda@Edge (viewer-request)
- Firm routing: `?firm={bucketSuffix}` -> routes to `opal-data-{firm}/gold/artifacts/`

**Lambda endpoints** (`/api/scoped/advisor-intelligence/*`, `/api/scoped/partners/books/*`):
- CloudFront -> API Gateway -> Lambda
- Firm routing: `?firmId={ddbFirmId}` (mapped via LAMBDA_FIRM_ID: `{bd: '49financial'}`)

**Static entity artifacts** (`/api/scoped/advisor-intelligence/entities/clients/*`):
- S3 pre-computed per-relationship JSON
- Same CloudFront behavior as artifacts
