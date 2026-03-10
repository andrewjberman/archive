# PRD: AdvisorIntelligence 49Financial V3 (ADVI_49FNV3)

**Author:** 1.0.0_SA_CTO
**Date:** 2026-03-06
**Project Code:** ADVI_49FNV3
**Macro:** ADVI (AdvisorIntelligence)
**Pods:** 0.4 (ClientPlatform)
**Pipeline:** bd-pipeline

---

## 1. Context

49Financial's data team reviewed the current AdvisorIntelligence page and provided
feedback on 2026-03-05. This project addresses both outstanding fixes from YANGV2
and new features requested by 49's leadership. YANGV2 is now closed; Y14 (Books
access gating) and remaining polish items graduate into this project.

---

## 2. Scope Overview

Two categories of work, with fixes prioritized before new features:

| Category | Items | Priority |
|----------|-------|----------|
| Fixes (F1-F7) | GRO data, projected bars, Segment Analytics drilldowns, stacked advisor bar, QTD/YTD timing, Unassigned sorting, zebra striping | P0 -- address first |
| New Features (N1-N3) | Books admin dashboard, advisor drilldown, relationship drilldown | P1 -- after fixes |

---

## 3. Fixes

### F1: GRO Mode Shows No Data

**Location:** Assets Overview panel toggle in PartnerAnalytics.tsx
**Symptom:** Selecting GRO mode shows "Growth decomposition data unavailable."
**Frontend status:** Fully wired. PartnerAnalytics.tsx reads
`timeseriesData?.growth_decomposition` and renders a 3-line chart (market, NNA, total)
with colors defined (violet/blue/amber). Legend and tooltip are implemented.
**Data contract status:** Y5 added `growth_decomposition` to timeseries_chart.json.
Shape: `{ period: "YYYY-MM", market: float, nna: float, total: float }` where
`market = aua_end - aua_start - nna`.
**Probable cause:** Lambda publisher (bd-portal-publisher) is not emitting the field,
or the gold layer data feeding it is empty/missing.
**Action:** DS/DE investigation. Check bd-portal-publisher lambda_function.py for
growth_decomposition build logic. If absent, DS implements; if present but empty,
trace to gold layer source.

### F2: Projected Bars for Partial Periods

**Location:** Assets Overview panel -- AUA (NMEC/NMNC), NNA (Inflows/Outflows/Net),
and GRO views across all granularities (monthly/quarterly/annually).
**Behavior:** For the current incomplete period, display a faint ghost extension of
each bar showing the projected full-period value.
**Methodology (metric-dependent -- stock vs flow):**

  AUA is a stock (point-in-time portfolio value). NNA and GRO are flows (accumulate
  over a period). The projection formula MUST differ:

  **Flow metrics (NNA inflows, NNA outflows, GRO market/nna/total):**
  - `projected_flow = actual_flow * (total_period_days / elapsed_days)`
  - Cap: `abs(prior_period_flow) * 1.5`
  - Ghost = projected_flow - actual_flow

  **Stock metrics (AUA — NMEC, NMNC):**
  - `delta = current_value - prior_period_end_value`
  - `projected_delta = delta * (total_period_days / elapsed_days)`
  - `projected_value = prior_period_end_value + projected_delta`
  - Cap: `prior_period_end_value + abs(prior_period_change) * 1.5`
    (where `prior_period_change = prior_end - prior_start`)
  - Ghost = projected_value - current_value

  The key distinction: for AUA you extrapolate the CHANGE from prior period end,
  not the level itself. Multiplying a $1.55B stock value by a time ratio produces
  nonsensical results ($2B+ projections for a single quarter).

  **CORRECTION (2026-03-09):** The original PRD specified `actual * (total_period_days
  / elapsed_days)` uniformly for all metrics. This is only correct for flow metrics.
  For stock metrics it produces absurd projections. The formula above replaces it.

  - Apply constraint: projection capped per the formulas above. This prevents noise
    on short timelines (e.g., 2 days into a month) from producing absurd projections.
  - The ghost portion (projected minus actual) renders as a faint/translucent
    extension of the bar using the same color at reduced opacity (~20-30%).
**Applies to:**
  - AUA view: NMEC bar and NMNC bar each get ghost extensions (stock projection)
  - NNA view: Inflows bar (blue ghost), Outflows bar (red ghost), Net dash/marker (flow projection)
  - GRO view: Each of the three lines (market, NNA, total) gets a dashed extension
    to the projected value for the current period (flow projection)
**Data source:** Computation is frontend-only. The portal already has the actual
partial-period data and the prior period's completed value in the same dataset.
No Lambda/DS changes required.

### F3: Missing City-Level and Client-Level Drilldowns in Segment Analytics

**Location:** Snapshot NNA section in Segment Analytics panel (DistributionTab.tsx)
**Symptom:** City and Client drill levels are not available in the NNA segment view.
**Expected:** Clicking a state in the NNA geo donut should drill to cities within
that state. Clicking a city should drill to individual clients.
**Data contract status:** Y6b added city drill (`nna_geo_drill` in timeseries_chart.json)
and Y6d added relationship drill. Both were confirmed complete in the DS data contract.
**Action:** DE/RD investigation. The data likely exists but the frontend drill
interaction is not wired for the Snapshot NNA panel specifically. Check whether
the cumulative chart views provide the drill data and wire the click handlers.

### F4: Top Ten Advisors Stacked Bar View

**Location:** AdvisorsTab.tsx -- top ten advisors panel (architect or implementor,
depending on toggle)
**Design:**
  - Blue bar for inflows (above zero line)
  - Red bar for outflows (below zero line, same style as NNA in main header panel)
  - Gold horizontal dash showing NNA level overlaid on the bar (similar to the
    triangle markers in Peer Performance on the ModelPortfolios page)
  - Bars sorted by NNA descending (or by total AUA, confirm with Andrew)
**Data source:** `advisor_rolling_flows.json` has monthly stacked_bar data per
advisor (Y13). The leaderboard data has per-advisor NNA. May need to combine
both sources or extend the publisher to emit a top-ten stacked bar view.
**Action:** DS to confirm data shape supports inflow/outflow per advisor. DE/RD
to implement the stacked bar visualization.

### F5: QTD/YTD Timing Bug

**Location:** AdvisorsTab.tsx -- period toggle (QTD/YTD/window)
**Symptom:** In March 2026, QTD and YTD show different values. Since March is in
Q1, QTD (Jan 1 - today) and YTD (Jan 1 - today) should be identical date ranges
and produce the same numbers.
**Action:** DS + DE investigation. Check the date boundary logic in both the Lambda
publisher (server-side period computation) and the portal frontend (client-side
period filtering). One of them is computing Q1 start incorrectly or using a
different reference date.

### F6: Unassigned Implementors Sorting

**Location:** Leaderboard table in AdvisorsTab.tsx (implementor view)
**Symptom:** "Unassigned" appears ranked by NNA/AUA like a real advisor, potentially
appearing at #1 on the leaderboard.
**Expected behavior:** "Unassigned" should be pinned to the bottom of the table,
below all named advisors, same treatment as "49F House" (the firm account). It
should still be visible for transparency but should not participate in ranking.
**Action:** RD fix. Add "Unassigned" to the same exclusion list as "49F House" in
the leaderboard sort/render logic.

### F7: Zebra Striping on Leaderboard

**Location:** Leaderboard table rows in AdvisorsTab.tsx
**Symptom:** Rows have uniform background, making it hard to scan across columns.
**Expected:** Alternating row backgrounds (zebra striping) matching the pattern
used in SecurityScanner and PortfolioManagement pages.
**Action:** RD fix. Apply the same alternating row background style already used
in other pages. Likely a CSS/className addition on table rows.

---

## 4. New Features: Books Tab

### Architecture: Three-Layer Drill Hierarchy

```
Layer 1: Firm Admin Dashboard (default top-down view)
  |
  +-- Layer 2: Advisor Book View (architect or implementor drilldown)
        |
        +-- Layer 3: Relationship Detail View (individual client/household)
```

### N1: Firm Admin Dashboard (Layer 1)

**Position:** Top of Books tab, above the existing advisor summary table.
**Purpose:** Give firm leadership a top-down view of the entire book of business
using heuristic panels.

**Phase 1 panels (data exists today):**

| Panel | Data Source | Notes |
|-------|-----------|-------|
| Tax Status Breakdown | accounts_dimension `tax_status` | Donut or horizontal bar: Taxable / Tax-Deferred / Tax-Exempt with AUA amounts and percentages. Data already in `clients_tab.json` tax object. |
| AUA by Advisor (top N) | architect_leaderboard.json | Horizontal bar showing AUA concentration across architects/implementors. Data exists. |
| Account & Client Distributions | clients_tab.json headline | Total accounts, total clients (relationships), median AUA. Cards or KPI tiles. |
| Engagement Summary | clients_tab.json engagement | Net flows TTM, average relationship tenure, active clients percentage. |

**Phase 2 panels (require new pipeline work):**

| Panel | Requirement | Notes |
|-------|------------|-------|
| Firm-Level Asset Allocation | New gold layer script/table. Allocations feed has account-level market values but lacks per-security asset class tags. Need either security-level BD data with asset class enrichment, or a pre-computed allocation report from BD API. | Flag for DS/AE to investigate BD data availability. |
| Fee Revenue by Advisor | New BD pipeline feed. `income_fees` is currently zeroed in both clients_tab.json and per-advisor JSONs ("not available from BD data"). BD has this data; needs new ingestion pipeline, dim table, backfill, and gold layer integration. | Flag for AE to scope BD API endpoint for fee data. |

### N2: Advisor Book View (Layer 2)

**Trigger:** Click an advisor row in the firm dashboard or the existing advisor
summary table.
**Content:** Relationship-level aggregate for the selected advisor (architect or
implementor). This is a drilldown of the Layer 1 firm view, scoped to one advisor.

**Panels:**
- Advisor's tax status breakdown (same donut as firm, filtered to this advisor)
- Advisor's client list with AUA (already exists in per-advisor JSONs: `clients` array)
- Advisor's NNA and engagement metrics (already in per-advisor JSONs: `nna`, `engagement`)
- Advisor's AUA trend over time (if timeseries data exists per advisor)

**Data source:** Per-advisor JSONs from bd-portal-advisor-publisher. The data
contract (Source 7) confirms these exist with tax, engagement, and clients fields.

### N3: Relationship Detail View (Layer 3)

**Trigger:** Click a relationship/client row in the advisor book view.
**Content:** Individual relationship-level drilldown showing that household's
accounts, positions, and activity.

**Data availability:** This may require extending the publisher to emit
per-relationship detail JSONs, or it may already exist in the ClientDetail
components (portal has `AdvisorIntelligence/ClientDetail/` directory with
PortfolioBalancePanel and TimeSeriesPanel). Needs DE/DS investigation to
confirm data coverage.

### N4: Y14 Access Gating (Deferred)

**From YANGV2:** Books tab advisor-scoped access via partner identity DynamoDB
table + JWT authorizer context. Auth chain is deployed (J1/J2/J3 verified).
Not a Phase 1 priority -- focus is getting data and interface structure complete
first. Will be addressed when the Books tab is ready for external advisor access.

---

## 5. Agents & Responsibilities

| Agent | Role |
|-------|------|
| 0.4.0_DS_ClientPlatform | F1 investigation (GRO data), F5 investigation (QTD/YTD), Books tab data extensions, Phase 2 data scoping |
| 0.4.0_DE_ClientPlatform | F3 wiring, F4 data shape confirmation, F5 investigation, Books tab component architecture, data contract updates |
| 0.4.2_RD_AdvisorIntelligence | F2 (projected bars), F4 (stacked bar viz), F6 (Unassigned sorting), F7 (zebra striping), N1-N3 (Books UI) |
| 0.4.0_DT_ClientPlatform | Lambda deploys, EC2 diagnostic runs, portal push |
| 0.6.0_AE_PartnerETL | Phase 2: BD API investigation for fee data and asset class data |

---

## 6. Phasing

| Phase | Scope | Blocking |
|-------|-------|----------|
| Phase 1a | Fixes F1-F7 | F1 blocks GRO projected bars in F2. F5 may block Advisors tab correctness. Others independent. |
| Phase 1b | Books tab Layer 1 (firm dashboard with Phase 1 panels) + Layer 2 (advisor drilldown) | Data exists today. Requires DE component architecture + RD implementation. |
| Phase 2a | Layer 3 (relationship detail) + Y14 access gating | Needs DE/DS investigation on data availability for per-relationship views. |
| Phase 2b | Firm-level asset allocation panel + fee revenue panel | Requires new BD pipeline feeds. AE scopes. |

---

## 7. Success Criteria

| Criterion | Target |
|-----------|--------|
| F1: GRO mode | Shows 3-line chart with real data |
| F2: Projected bars | Ghost bars visible for current partial period in all views, capped at 1.5x prior |
| F3: Segment drilldowns | City and client levels accessible from Snapshot NNA |
| F4: Stacked advisor bar | Blue inflows / red outflows / gold NNA dash for top 10 advisors |
| F5: QTD/YTD | Identical values when QTD period equals YTD period |
| F6: Unassigned | Pinned to bottom of leaderboard |
| F7: Zebra striping | Alternating row backgrounds on leaderboard |
| N1: Firm dashboard | Tax breakdown, AUA by advisor, account/client distributions, engagement visible |
| N2: Advisor drilldown | Click advisor -> see their book with tax, clients, NNA, engagement |

---

## 8. Risks

| Risk | Mitigation |
|------|-----------|
| F1 root cause unknown (Lambda vs gold layer vs data) | DS investigation first; do not attempt frontend fixes |
| F2 projection cap may feel arbitrary at 1.5x | Start with 1.5x, adjust based on Andrew/Yang feedback after seeing it live |
| F5 timing bug may be systemic (affect other period calculations) | Investigation should audit all period boundary computations, not just QTD/YTD |
| Books Layer 3 may need new publisher output | Phase 2a scoping will determine; existing ClientDetail components may partially cover this |
| Fee/asset allocation data not in current BD pipeline | Explicitly Phase 2; does not block Books tab launch |
