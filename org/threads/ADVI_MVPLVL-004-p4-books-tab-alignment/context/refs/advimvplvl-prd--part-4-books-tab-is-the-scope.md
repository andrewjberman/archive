# ADVI_MVPLVL PRD — Advisor Intelligence MVP Polish

**Project Code:** `ADVI_MVPLVL`
**Author:** 1.0.0_SA_CTO
**Date:** 2026-03-13
**Deadline:** 5 business days (by 2026-03-20)
**Status:** COMPLETE — All 4 parts documented, COO decomposition pending

---

## Overview

Bring Advisor Intelligence to minimum viable product across four sections:

1. **Header (Assets Overview Panel)** — AUA default window, Mix data lineage, NNA stacking anomaly, GRO audit + summary container
2. **Distribution Tab** — Drilldown completeness, capitalization, cohort state retention, "Other" logic, NNA time machine strip, time window inheritance
3. **Advisors Tab** — Portfolio group + architect data quality, Top 3 panel layout, stacked bar sort, leaderboard visual polish
4. **Books Tab** — Gold table data audit, drill hierarchy enhancement, tax status/liability, Mix + Concentration linked views, AUA/NNA time series, advisor listing consistency

Each item is classified as either **ACTION** (fix is understood, execute immediately)
or **RESEARCH** (investigation needed before implementation).

---

## Part 1: Header (Assets Overview Panel)

The Assets Overview panel (`PartnerAnalytics.tsx`) contains three sub-views toggled
by Mode: AUA, NNA, GRO. Additional controls: time window (1Y/3Y/Max), granularity
(Monthly/Quarterly/Annually), and for AUA: sub-mode (Clients/Mix).

### 1a) AUA

#### 1a-i. Default Window/Interval — ACTION

**Problem:** Page defaults to 3Y window. Should default to 1Y window, Quarter interval.

**Current state:**
- `PartnerAnalytics.tsx:203` — `useState<TimeWindow>('3Y')` (WRONG)
- `AdvisorIntelligence.tsx:91` — `useState<GranularityOption>('quarterly')` (CORRECT)

**Fix:** Change the TimeWindow default from `'3Y'` to `'1Y'` at line 203.

**Classification:** ACTION — single line change, no investigation needed.

#### 1a-ii. AUA Mix Sub-Mode — RESEARCH

**Problem:** The "Mix" toggle (asset class breakdown of AUA) shows completely wrong data.
Currently surfaces only two months (Feb and Mar 2026) with extraneous AUA numbers
(2.09B and 1.98B) in incorrect order.

**What Mix does today:**
- Reads `timeseries_chart.json -> aua_mix` from the publisher Lambda
- `aua_mix` type is `AuaMixView`: `{ data: AuaMixPoint[] }` where each point has
  `{ period: string, segments: AuaMixSegment[] }` with segment `{ label, value }`
- Categories: Equities, Fixed Income, Real Estate, Alternatives, Cash, Other
- Frontend aggregates monthly `aua_mix` data by granularity (`PartnerAnalytics.tsx:367-397`)

**Investigation required:**
1. **Where is `aua_mix` produced?** Trace from `bd-portal-publisher` Lambda
   (`infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py`) — find the
   function that builds `aua_mix` in `timeseries_chart.json`.
2. **What data is at its disposal?** Examine what Gold layer time-series data exists
   that could inform asset class mix of AUA. Key candidates:
   - `data/black_diamond/scripts/gold/` — look for holdings_lots, positions cube, or
     asset class classification outputs
   - The `02_build_positions_cube.py` script produces security-level data with asset
     classes — does its output feed into anything temporal?
3. **What is the correct methodology?** Asset mix of AUA requires knowing the market
   value of each asset class at each point in time. This is fundamentally different from
   NNA (which is flow-based). The data must come from holdings/positions snapshots, not
   transaction flows.
4. **Why are only Feb/Mar 2026 showing?** Determine if the publisher is only computing
   mix for recent months, or if historical data is absent from the Gold layer.

**Classification:** RESEARCH — deep data lineage investigation before any fix.

---

### 1b) NNA

#### 1b-i. October 2025 Bar Stacking Anomaly — RESEARCH + ACTION

**Problem:** In Monthly interval view, October 2025 shows the red "Outflows" bar
visually placed ON TOP of the blue "Inflows" bar (stacked upward together). Every other
month correctly shows inflows above zero and outflows below zero as a diverging bar chart.

**How the chart works:**
- `ComposedChart` with `stackOffset="sign"` (`PartnerAnalytics.tsx:1316`)
- `inflow` bar (`stackId="nna"`) renders positive values above zero
- `outflow` bar (`stackId="nna"`) renders negative values below zero
- `stackOffset="sign"` routes positive values up, negative values down

**Root cause hypothesis:** The `outflow` value for October 2025 is likely **positive**
instead of negative. In the aggregation logic (`PartnerAnalytics.tsx:352-353`):
```typescript
const outflow = grossFlows ? -periodOutflows : 0
```
`periodOutflows` is computed as `entry.lastOutflows - prevOutflows`. If the cumulative
Outflows column in the raw `nna` daily data has a discontinuity, reset, or data gap
around October 2025, the differencing could produce a negative `periodOutflows`, which
when negated becomes positive — placing it above the zero line with inflows.

**Investigation required:**
1. Inspect the raw `timeseries_chart.json -> nna -> data` for daily values around
   Sep-Oct-Nov 2025. Look for discontinuities in the cumulative `Outflows` column.
2. If the data is correct, the bug is in the frontend differencing logic.
3. If the data has a gap or reset, the fix is in the publisher Lambda.

**Classification:** RESEARCH (data inspection) then ACTION (patch wherever the sign
error originates).

---

### 1c) GRO (Growth Decomposition)

#### 1c-i. Number Audit and Methodology Clarification — RESEARCH

**Problem:** The GRO view shows monthly AUA change decomposed into Market appreciation
and NNA. The numbers need audit — we need to verify how market vs NNA decomposition is
being computed, especially during months with significant market drawdowns.

**How GRO works today:**
- Reads `timeseries_chart.json -> growth_decomposition` from publisher Lambda
- Type: `GrowthDecompositionView` with data points `{ period, market, nna, total }`
- `market` = AUA change attributable to market appreciation
- `nna` = net new assets for the period
- `total` = market + nna = total AUA change
- Frontend aggregates monthly data by granularity, renders stacked bars (market + NNA)
  with a Total line overlay

**Key months to investigate (outlier market losses):**
- **Feb 2026** — recent market drawdown
- **Jun 2025** — mid-year correction
- **Feb 2023** — early data period with market stress

For each month: verify that `market + nna = total`, and that the `market` component
correctly isolates price movement from flow effects.

**Investigation required:**
1. Trace the `growth_decomposition` computation in `bd-portal-publisher` Lambda
2. Verify the formula: is `market = total_aua_change - nna`? Or is it computed
   independently from holdings returns?
3. For the three flagged months, pull actual numbers and cross-validate against
   known market indices (S&P 500, etc.) to sanity-check the magnitude

**Classification:** RESEARCH — methodology audit before any changes.

#### 1c-ii. GRO Summary Container — Missing PIT Growth Differentials — ACTION

**Problem:** The primary summary container below the chart (the "Selected/Latest Value
Highlight" section) is present for AUA and NNA views but **completely absent for GRO**.

**Current state:**
- `PartnerAnalytics.tsx:1826-1827`:
  ```typescript
  {panelViewMode !== 'gro' && !(panelViewMode === 'aua' && auaSubMode === 'mix') && ...
  ```
  GRO is explicitly excluded from the summary container.

**What is needed:**
- A summary container for GRO matching the pattern of AUA and NNA, showing:
  - Market change for the selected/latest period
  - NNA change for the selected/latest period
  - Total AUA change for the selected/latest period
  - **Period-over-period growth differentials** (e.g., "vs Q4 '25: +$12M Market, -$3M NNA")
    analogous to what AUA and NNA already show

Both AUA and NNA have these PIT (point-in-time) growth comparisons with the prior period.
GRO must have the same treatment.

**Classification:** ACTION after 1c-i research is complete (numbers must be validated
before we build a summary container around them).

---

## Part 2: Distribution Tab

The Distribution Tab (`DistributionTab.tsx`) has two modes: **Snapshot** (donut + bell
curve + time machine) and **Continuous** (stacked area chart). Both have GEO and ADV
cohort toggles and AUA/NNA metric toggles. Most items here are cosmetic/UX fixes with
one data completeness requirement.

### 2a) Snapshot Drilldown Completeness — ACTION (data-dependent)

**Problem:** Every drilldown combination must be functional:
- Cohort: GEO x ADV
- Metric: AUA x NNA
- Interval: Monthly x Quarterly x Annually
- Drill level: state/architect -> city/relationship

All snapshot combinations for all intervals must display period-specific and
cohort-specific views. If a cohort genuinely has no data for a given period (e.g.,
the firm was not in the system), that is acceptable — but the UI must handle it
gracefully (empty state, not a crash or stale data).

**Classification:** ACTION — systematic QA pass through all combinations. Fix any
missing data paths or rendering gaps found.

### 2b) Remove "Period NNA" Label — ACTION

**Problem:** Summary containers display "Period NNA" — this is redundant. The fact
that it is period-level NNA is implied by the context.

**Current locations:**
- `DistributionTab.tsx:1976` — help text: `"Period NNA across states/architects..."`
- `DistributionTab.tsx:2280` — summary tile label: `"Period NNA"`
- `DistributionTab.tsx:2614` — bell curve X-axis label: `"Period NNA"`

**Fix:** Replace "Period NNA" with just "NNA" in all three locations.

**Classification:** ACTION — text changes only.

### 2c) Standard Capitalization — ACTION

**Problem:** GEO and ADV cohort names violate standard capitalization rules:
1. **States are abbreviated** — "CA", "TX" instead of "California", "Texas"
2. **Cities are all-uppercase** — "AUSTIN" instead of "Austin"
3. **State display uses `.toUpperCase()`** — `selectedStateKey?.toUpperCase()` at
   lines 1928, 1967, 1974, 1994, 2133 produces "TX" or "TEXAS" instead of "Texas"

**Required behavior:**
- States: spelled out completely — "California", "Texas", "New York" (never CA, TX, NY)
- Cities: title case — "Austin", "San Francisco" (never AUSTIN)
- Architects: title case with spaces — "Travis Penfield" (never TRAVIS_PENFIELD)

**Implementation notes:**
- The backend (`bd-portal-publisher` / script 09) produces state keys as abbreviations
  (e.g., `tx`, `ca`). A state abbreviation -> full name mapping is needed either in the
  publisher or as a frontend lookup table.
- City labels are built from keys at line 1723:
  `cityKey.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')`
  This is correct for title-casing but only if the key segments are lowercase. Verify
  that keys like `"no_city"` produce `"No City"` (which then gets grouped into Other
  per 2g below).
- The `.toUpperCase()` calls on state keys (5 locations) must all be replaced with
  the full state name lookup.

**Classification:** ACTION — frontend mapping + text replacement.

### 2d) Retain Cohort State Across AUA/NNA Toggle — ACTION

**Problem:** When viewing Snapshot-GEO-AUA drilled into "Texas", switching the metric
toggle from AUA to NNA resets the drill state — user loses their position and returns
to the top-level state view.

**Root cause:** `DistributionTab.tsx:1655-1662`:
```typescript
useEffect(() => {
  setGeoDrillLevel('state')
  setSelectedStateKey(null)
  setAdvDrillLevel('architect')
  setSelectedArchitectKey(null)
  setSelectedSegmentKey(null)
  setSelectedPeriod('current')
}, [cohort, metric, granularity])
```
The `metric` dependency causes a full drill state reset on AUA <-> NNA switch.

**Required behavior:** Switching AUA <-> NNA retains:
- `selectedStateKey` (GEO drill)
- `selectedArchitectKey` (ADV drill)
- `geoDrillLevel` / `advDrillLevel`

Only `cohort` and `granularity` changes should reset drill state. `metric` changes
should NOT reset `selectedStateKey`, `selectedArchitectKey`, or drill levels.

**Fix:** Remove `metric` from the dependency array of the reset useEffect. Add a
separate, narrower effect that only resets `selectedSegmentKey` (the bell curve
selection) on metric change, since segment-level distributions differ between AUA and NNA.

**Classification:** ACTION — state management fix.

### 2e) Show All Cohorts in Snapshot (No "Other" Group) — ACTION

**Problem:** Snapshot view currently limits display to top 8 states/architects with an
"Other" bucket. This hides useful information.

**Required behavior:** Display ALL states and ALL architects in the snapshot donut and
summary, ranked by:
- AUA (when metric toggle = AUA)
- NNA (when metric toggle = NNA)

Ranking is based on the **current period** values. No "Other" aggregation at the
snapshot level.

**Note:** This is a frontend-only change if the backend already provides all segments
in `views.aua.current.donut.segments` / `views.nna.current.geo.donut.segments`. If the
backend pre-aggregates into "Other", the publisher must also be updated.

**Classification:** ACTION — verify backend completeness, then remove top-N + Other
logic in snapshot rendering.

### 2f) Continuous View — No "Other" at Top Level, Top 8 + Other at Drill — ACTION

**Problem:** Continuous stacked area chart should follow the same "show all" principle
at the top level.

**Required behavior:**
- **Top level (state/architect):** Display all cohorts, no "Other" group. Ranked by
  AUA or NNA depending on toggle.
- **Drill level (city/relationship):** Top 8 + "Other" is acceptable.
- Proper capitalization rules (2c) apply identically.
- `"no_city"` entries must be grouped into the "Other" bucket at drill level.

**Current code:** `DistributionTab.tsx:1027-1032` limits to top 8 + Other:
```typescript
const nonOther = categories.filter(c => c !== 'Other')
const top8 = nonOther.slice(0, 8)
return categories.includes('Other') ? [...top8, 'Other'] : top8
```
This top-8 limit must be removed at the top level but preserved at drill level.

**Classification:** ACTION — conditional logic change.

### 2g) "No City" Handling — ACTION

**Problem:** In GEO drill-down to city level, entries with `"no_city"` as the key
appear as a separate segment. These should be grouped into the "Other" bucket.

**Classification:** ACTION — add `no_city` to Other aggregation in the city drill
rendering logic.

### 2h) NNA Time Machine Strip — Cohort-Specific Period Values — ACTION

**Problem:** When drilled into a specific cohort (e.g., Texas in GEO, Travis Penfield
in ADV), the NNA time machine strip still shows **aggregate firm-wide NNA** for each
period instead of the NNA specific to the drilled-into segment.

AUA mode already handles this correctly — `DistributionQuarterlyStrip` traverses into
per-segment AUA at every drill level and period.

**DE Brief:** Full investigation documented at
`org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-03-13/nna_cohort_specific_time_machine_brief.md`

**Data availability by drill level:**

| Drill Level | Field | Available in every period? |
|---|---|---|
| State (GEO top) | `geo.donut.segments[key].value` | YES |
| City (GEO drill) | `geo.drill[state].by_city[city].total` | YES |
| Architect (ADV top) | `adv.donut.segments[key].value` | YES |
| Relationship (ADV drill) | Only `DistributionStats` per architect, not per-relationship | NO — backend gap |

**Scope decision (CTO):** MVP covers the 3 fully-supported levels (state, city,
architect) — frontend-only change in `NnaQuarterlyStrip`. The relationship-level gap
requires a backend change to script 09 (`build_nna_adv_view()` would need to emit
per-relationship NNA values). This is deferred post-MVP.

**Strip label decision (CTO):** When showing cohort-specific NNA, the strip label
should display the cohort name (e.g., "Texas" or "Travis Penfield") with no
"Period NNA" prefix — consistent with 2b.

**Edge case decision (CTO):** Segments not present in historical periods show $0
(same fallthrough pattern as AUA mode).

**Implementation:** Modify `NnaQuarterlyStrip` to accept `parentSegmentKey`,
`childSegmentKey`, and `cohort` props. Mirror the traversal pattern from
`DistributionQuarterlyStrip` (lines 2308-2331). See DE brief for exact prop changes
and callsite update.

**Classification:** ACTION — frontend only, mirrors proven AUA pattern.

### 2i) Remove Independent Time Period Toggles from Distribution Tab — ACTION

**Problem:** The Continuous view has its own time window (1Y/3Y/Max) and the overall
tab has granularity selection. These should inherit from the Assets Overview Header
Panel instead of having independent controls.

**Current state:**
- `DistributionTab.tsx:277` — `useState<ChartWindowOption>('1Y')` (independent)
- The Snapshot view already inherits `granularity` from props (passed down from
  `AdvisorIntelligence.tsx`), but Continuous has its own window toggle.

**Required behavior:** Distribution Tab Continuous view reads the time window and
granularity from the same source as the Assets Overview Header Panel. The independent
`WINDOW_OPTIONS` toggle in the Distribution Tab header should be removed.

**Implementation:** The `timeWindow` state from `PartnerAnalytics.tsx` (or a lifted
version in `AdvisorIntelligence.tsx`) must be passed as a prop to `DistributionTab`.
The `granularity` prop is already passed.

**Classification:** ACTION — lift state or pass prop, remove redundant controls.

---

## Part 3: Advisors Tab

The Advisors Tab (`AdvisorsTab.tsx`) has three panels: Top Performers (gold/silver/bronze
cards), Rolling Flows (time-series diverging bar), and Leaderboard (sortable table).
A tab-wide Architects/Implementors toggle controls all three. Issues range from deep
data quality research to layout fixes and visual polish.

### 3a) Portfolio Group Investigation + Architect Data Quality — RESEARCH

**Problem:** 49 Financial's "Architect" field has 53 entries, but senior leadership
confirms there are likely fewer than 15 true architects. Poor data entry by support
staff has polluted the field with non-architect names. This fundamentally undermines
the Advisors Tab's ranking and drill-down value.

**Investigation required:**

1. **Portfolio Group field analysis.** The `portfolio_group` field exists in the accounts
   dimension (`data/black_diamond/scripts/gold/00_build_accounts_dimension.py:81,370`).
   It is carried through to the gold-layer parquet output. Questions:
   - What distinct values does `portfolio_group` contain?
   - Is it a proxy for regional offices (as suspected)?
   - How many unique portfolio groups exist, and do they map cleanly to organizational
     units?

2. **True architect identification logic.** Develop a conditional to separate true
   architects from noise. Proposed heuristics (to be validated against data):
   - **Cross-reference with portfolio group:** If portfolio groups represent regional
     offices, true architects likely appear consistently within a small set of groups.
     Non-architects (support staff, one-off entries) may be scattered or appear in
     groups inconsistently.
   - **Temporal activity flag:** Only count architects tagged on transactions within
     the trailing 12 months. Stale entries from years-old data entry errors drop out.
   - **AUA threshold:** True architects likely manage material AUA. A minimum AUA
     threshold (e.g., top 20 by AUA) could serve as a corroborating filter.
   - **Account count threshold:** True architects are likely associated with multiple
     client relationships, not just 1-2.

3. **Default tab hierarchy.** Once portfolio groups are understood, the Advisors Tab
   should support three cleave levels:
   - **Portfolio Group** (default) — regional office or organizational unit
   - **Architect** (filtered to true architects)
   - **Implementor**

   This replaces the current binary Architects/Implementors toggle.

**Data scientist scope:** Run the diagnostic queries against the gold-layer accounts
parquet to answer #1 and #2. Produce a mapping table (portfolio_group -> display name,
architect -> is_true_architect flag). This mapping feeds into both the publisher Lambda
and the frontend.

**Classification:** RESEARCH — deep data investigation, then schema/publisher changes.

### 3b) Top 3 Highlights Panel Overwritten by Stacked Bar — ACTION

**Problem:** The Top Performers panel (Panel 1) briefly shows the gold/silver/bronze
Top 3 ranking cards, then gets replaced by the `TopTenStackedBar` chart once
`flowsData` loads. The stacked bar was intended to replace the Rolling Flows panel
(Panel 2), not the Top Performers panel.

**Root cause:** `AdvisorsTab.tsx:272-276`:
```typescript
{flowsData?.stacked_bar?.[period]?.[role] ? (
  <TopTenStackedBar data={flowsData} period={period} role={role} />
) : (
  <Top3Highlights data={activeLeaderboard} window={periodToChartWindow(period)} role={role} />
)}
```
This conditional renders EITHER the stacked bar OR the Top 3 cards. Once flows data
loads, Top 3 disappears permanently.

**Required behavior:**
- **Panel 1 (Top Performers):** ALWAYS shows `Top3Highlights` (gold/silver/bronze cards)
- **Panel 2 (Rolling Flows):** Shows `TopTenStackedBar` when stacked_bar data is
  available, otherwise shows the existing `RollingFlowsDivergingBar`

**Fix:** Move `TopTenStackedBar` from Panel 1's conditional to Panel 2. Panel 1
always renders `Top3Highlights`. Panel 2 checks for `flowsData?.stacked_bar` first,
falls back to `RollingFlowsDivergingBar`.

**Classification:** ACTION — component relocation, no new logic.

### 3c) Stacked Bar NNA Sort Order — ACTION

**Problem:** The NNA stacked bar chart bars display in random/inconsistent order.
They should be ordered left-to-right from highest NNA descending.

**Current state:** `AdvisorsTab.tsx:571-572`:
```typescript
return [...entries]
  .sort((a, b) => b.nna_net - a.nna_net || a.advisor_name.localeCompare(b.advisor_name))
  .slice(0, 10)
```
The sort IS present in the data preparation, ordering by `nna_net` descending. However,
the visual rendering may not respect this order if Recharts re-sorts based on the
`name` dataKey or if the data array order is lost during chart rendering.

**Investigation:** Verify whether the issue is:
1. The sort is correct in the data but Recharts `XAxis` alphabetizes the `name` field
2. The backend `stacked_bar` data arrives pre-sorted differently, overriding the
   frontend sort
3. The `.slice(0, 10)` truncation is happening after sort but visual order differs

**Fix:** Ensure the data array order is preserved in rendering. If Recharts
alphabetizes by default, explicitly set `XAxis` `type="category"` and `allowDataOverflow`
to prevent re-sorting. The sort direction must be highest NNA on the left, decreasing
to the right.

**Classification:** ACTION — debug sort + chart rendering interaction.

### 3d) Leaderboard Visual Polish — ACTION

**Problem:** The leaderboard table is visually rough — very small text (`text-xs` /
`text-[10px]`), minimal color, cramped rows. Does not match the visual quality of
other portal pages.

**Required behavior:** Larger, more aesthetically inclined row design with:
- Bigger text (at least `text-sm` for values, `text-xs` for labels)
- More color — NNA values colored green/red, growth % with gradient backgrounds,
  rank badges with visual weight
- Clearer information hierarchy — name prominent, metrics well-spaced
- Card-like rows or generous padding instead of the current compact table

**Design reference pages (existing portal design language):**
- `portal/src/pages/SecurityScanner/` — card-based layouts, color-coded severity
- `portal/src/pages/FactorTilts/` — rich data presentation with visual hierarchy
- Keyword Intelligence modal drilldown (in CausalityEngine/MarketUpdate) — modal
  with clear typography and color

The current `<table>` structure at `AdvisorsTab.tsx:854-979` should be redesigned as
card rows or a richly styled table with substantially more visual presence.

**Classification:** ACTION — UI/UX redesign of the leaderboard component.

---

## Part 4: Books Tab

The Books Tab is the most unfinished and least explored section, yet one of the most
important. The scope here is fundamentally deeper than Parts 1-3: it requires a data
availability investigation before views can be designed, and the features requested
(Mix, Concentration, Tax Liability) constitute a significant data engineering project.

### 4a) Gold Table Data Availability Audit — RESEARCH

**Problem:** We cannot design Books Tab views without understanding what data the gold
layer currently produces at each grain level. The tab needs data at four drill levels
(firm, advisor, relationship, account) and we need to know what's available vs. what
requires new builders.

**Known data sources (from gold scripts):**

| Script | Output | Grain | Key Fields |
|--------|--------|-------|------------|
| `00_build_accounts_dimension.py` | `accounts_dimension_latest.parquet` | Account | `account_id`, `relationship_id`, `architect`, `implementor`, `portfolio_group`, `tax_status`, `qualified_flag`, `account_type`, `investment_strategy_name` |
| `03_build_holdings_lots.py` | `gold/holdings_lots/` | Lot | `account_id`, `relationship_id`, `ticker`, `asset_name`, `cost_basis`, `market_value`, `accrued_gain`, `term`, `acquisition_date`, `tax_status` |
| `05_build_client_performance.py` | `client_performance.parquet` | Relationship × Day | `relationship_id`, `total_aua`, `aua_taxable`, `aua_tax_deferred`, `aua_tax_exempt`, `cum_inflows`, `cum_outflows`, `nna` |
| `05b_build_account_performance.py` | `account_performance.parquet` | Account × Day | Same as 05 but at account grain |
| `06_build_client_tax_liability.py` | `client_tax_liability.parquet` | Position × Purchase Year | `relationship_id`, `account_id`, `ticker`, `purchase_year`, `total_cost_basis`, `total_market_value`, `total_accrued_gain`, short/long term splits |
| `02_build_positions_cube.py` | `positions_cube/YYYY-MM-DD.parquet` | Account × Asset × Day | `account_id`, `asset_name`, `units` (daily snapshot) |

**What the investigation must determine:**
1. Which of these outputs are currently consumed by `bd-portal-publisher` for the
   Books Tab endpoints (`getClientsTab`, `getAdvisorBook`, `getBooksClientDetail`)
2. What additional aggregations are needed to support Mix, Concentration, and
   time-series views at each drill level
3. Whether `positions_cube` (172M+ rows) is practical for concentration analysis
   or if a pre-aggregated concentration view is needed

**Classification:** RESEARCH — DS must audit data availability and document gaps
before frontend work items can be specified.

### 4b) Drill Hierarchy: Global → Advisor → Relationship → Account — ACTION

**Current state:** The Books Tab (`ClientsTab.tsx`, 1034 lines) already implements a
4-level drill:
- **N1 (Firm Dashboard):** Aggregate KPIs + Advisor Summary Table (top 20 by AUA)
- **L2 (Advisor Book):** Selected advisor's AUA, clients, accounts, tax exposure,
  NNA (MTD/QTD/YTD), engagement metrics, clients table
- **L3 (Client/Relationship Detail):** Client AUA, accounts table, tax intelligence
  (cost basis by year, top gain positions), open lots table with term/account filters
- **L4 (Account Detail):** Inline expansion within L3 showing account-scoped metrics
  and open lots

**Required behavior:** The 4-level drill hierarchy is correct and should be preserved.
The naming convention for this PRD:
- **Global** = N1 (firm admin view)
- **Advisor.0** = L2 (advisor book, all relationships aggregated)
- **Advisor.1** = L3 (individual relationship)
- **Advisor.2** = L4 (individual account)

The global admin view (N1) is mostly correct in its current state — it is simply
underdeveloped. Enhancements to each drill level are specified in items 4c-4h below.

**Classification:** ACTION — structural hierarchy exists, needs enhancement at each level.

### 4c) Tax Status — ACTION (Enhancement)

**Current state:** Tax status is already displayed:
- L2 (Advisor Book): Three-row breakdown — Taxable, Tax Deferred, Tax Free with
  amounts and percentages
- L3 (Client Detail): Same breakdown plus Qualified vs Non-Qualified split
- L4 (Account Detail): Shows account's tax status

**Required behavior:** Tax Status display is functional. Enhancements should come
naturally as part of other items (Mix, Concentration) — tax status serves as a
filter/grouping dimension in those views.

**Classification:** ACTION — minor refinements as part of larger view work, not a
standalone work item.

### 4d) Tax Liability (Cost Basis) — ACTION (Enhancement)

**Current state:** L3 already shows:
- Cost Basis by Year table (year, cost basis, market value, unrealized gain)
- Top Gain Positions table (top positions by unrealized gain)
- Open Lots table with per-lot cost basis, market value, gain, term, acquisition date
- Term filter (All/Short/Long) and Account dropdown filter

**Required behavior:** Tax Liability as a function of cost basis is largely
implemented. The existing open lots view with short/long term splits and per-lot
gain/loss provides the core tax planning interface. Data source
(`client_tax_liability.parquet`) has the necessary fields including short/long term
splits per position per purchase year.

**Classification:** ACTION — functional today; quality and completeness improvements
will emerge from the data audit (4a).

### 4e) Mix (Asset Class Breakdown) — RESEARCH + ACTION

**Problem:** The Assets Overview panel (Part 1) has a Mix sub-mode showing asset class
allocation, but this same capability needs to exist at every Books Tab drill level.
Users need to see how their book is allocated across asset classes at the firm,
advisor, relationship, and account level.

**Current state:** The advisor book data model includes `portfolio_composition` and
`income_fees` fields (visible in `AdvisorBookResponse` type), but these are currently
**hidden in the UI per prior task order** — the rendering code excludes them from the DOM.

**Data dependency:** Mix requires mapping each position to an asset class. Since 49
Financial is almost entirely invested in Opal-managed ETFs, the canonical ETF
Classification system (DynamoDB `etf-classifications` table, also mirrored in
`infra/aws/lambda/v2_portal/_shared/etf_classification.py`) covers the vast majority
of holdings. This classification maps ~160 ETFs to:
- `ETF_CLASSIFICATIONS`: asset class (fixed_income, equity, hedge)
- `ETF_SUB_ASSET_CLASS`: fine-grained buckets (US Large Cap, Cash, EM, High Yield, etc.)
- `ETF_SECTOR_MAPPING`: sector/segment (Government, Technology, Gold, etc.)
- `ETF_MANAGEMENT_STYLE`: active vs passive

**Required behavior:** Pie chart showing asset class allocation at each drill level.
Default state: all asset classes. This view is linked to Concentration (4f) — see
below.

**Classification:** RESEARCH + ACTION — need to verify coverage of ETF classification
against actual holdings, determine if `portfolio_composition` data is usable or needs
rebuilding, and then implement the views.

### 4f) Concentration (Security-Level Breakdown) — RESEARCH + ACTION

**Problem:** Concentration is the security-level analogue to Mix's asset-class-level
view. Where Mix shows "60% Equities, 30% Fixed Income, 10% Hedge," Concentration
shows the individual securities within those classes.

**Required behavior:**
- Pie chart showing security-level allocation at each drill level
- **Linked to Mix:** In default state, Mix shows all asset classes, so Concentration
  shows all securities. When the user clicks "Equities" in the Mix pie, Concentration
  filters to show only equity securities. Click "Fixed Income" → only fixed income
  securities in Concentration. This linkage makes the two views a coordinated pair.
- Top-N securities by market value weight, with "Other" bucket for the tail

**Data dependency:** Requires position-level market values aggregated to the
appropriate drill level. `positions_cube` has daily snapshots but at 172M+ rows may
need a pre-aggregated concentration view. `holdings_lots` has current positions with
market values per lot — can be aggregated to (account, ticker) grain.

**ETF Classification advantage:** Because 49 Financial is almost entirely Opal ETFs,
the canonical ETF Classification system eliminates most classification ambiguity. A
ticker lookup against the classification table maps each security to its asset class,
enabling the Mix ↔ Concentration linkage without guesswork.

**Classification:** RESEARCH + ACTION — this is a significant data project. DS needs
to design the aggregation pipeline, verify ETF classification coverage, and build the
concentration view. Frontend builds the linked pie chart UI.

### 4g) Relationship/Account-Level AUA/NNA Time Series — ACTION

**Problem:** We have invested heavily in building AUA and NNA time series at the
relationship and account level (scripts 05 and 05b). These should be surfaced in the
Books Tab drill views.

**Data availability:**
- `client_performance.parquet` — daily relationship-level AUA, tax-split AUA,
  cumulative flows, NNA
- `account_performance.parquet` — same fields at account grain

**Required behavior:** At L3 (Relationship) and L4 (Account), show AUA and NNA
time series charts using the same chart components proven in the Assets Overview
panel, with the same time window (1Y/3Y/Max) and granularity (Monthly/Quarterly/
Annually) controls.

**Classification:** ACTION — data exists, chart components exist. This is a wiring
and rendering task once the data is exposed through the publisher endpoints.

### 4h) Advisor Listing UI Consistency — ACTION (Dependency on 3d)

**Problem:** The N1 (Global) advisor summary table currently uses a basic HTML table
(`AdvisorSummaryTable` at `ClientsTab.tsx:976-1034`). This should use the same UI
design as the Leaderboard (3d) for visual consistency across the page.

**Current state:** Top 20 advisors by AUA, columns: Advisor, AUA, Clients, NNA (1Y),
Growth %, chevron. Basic alternating row colors, compact styling.

**Required behavior:** Same card-like rows, typography, and color treatment as
whatever design emerges from 3d (Leaderboard Visual Polish). This creates a dependency
chain: 3d must be designed first, then 4h applies the same design to the Books Tab
advisor listing.

**Classification:** ACTION — blocked on 3d completion. When 3d's design is finalized,
apply it here.

---

## File Reference

| File | Relevance |
|------|-----------|
| `portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx` | Assets Overview panel — AUA/NNA/GRO charts, Mix sub-mode, summary container, time window state |
| `portal/src/pages/AdvisorIntelligence/AdvisorIntelligence.tsx` | Page root — granularity state, prop threading to tabs |
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | Distribution Tab — snapshot/continuous, drill state, capitalization, "Other" logic |
| `portal/src/pages/AdvisorIntelligence/types.ts` | All type definitions (AuaMixView, GrowthDecompositionView, etc.) |
| `infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py` | Publisher Lambda — produces `timeseries_chart.json` including `aua_mix`, `growth_decomposition`, `nna` |
| `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` | Advisors Tab — Top 3, stacked bar, rolling flows, leaderboard |
| `data/black_diamond/scripts/gold/` | Gold layer scripts — source for asset class mix, portfolio_group, architect data |
| `data/black_diamond/scripts/gold/00_build_accounts_dimension.py` | Accounts dimension — contains `portfolio_group`, `architect`, `implementor` fields |
| `org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-03-13/nna_cohort_specific_time_machine_brief.md` | DE brief on NNA cohort-specific time machine strip (2h reference) |
| `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx` | Books Tab — 4-level drill (N1/L2/L3/L4), tax intelligence, open lots |
| `data/black_diamond/scripts/gold/03_build_holdings_lots.py` | Holdings lots builder — lot-level cost basis, market value, gain, term |
| `data/black_diamond/scripts/gold/05_build_client_performance.py` | Relationship-level daily AUA/NNA time series |
| `data/black_diamond/scripts/gold/05b_build_account_performance.py` | Account-level daily AUA/NNA time series |
| `data/black_diamond/scripts/gold/06_build_client_tax_liability.py` | Tax liability view — position × purchase year grain with term splits |
| `data/black_diamond/scripts/gold/02_build_positions_cube.py` | Daily positions cube — account × asset × day (172M+ rows) |
| `infra/aws/lambda/v2_portal/_shared/etf_classification.py` | Canonical ETF classification — asset class, sub-class, sector, style (~160 ETFs) |

## Agent Assignments (preliminary — pending COO decomposition)

| Work Item | Type | Primary Agent | Notes |
|-----------|------|---------------|-------|
| 1a-i. AUA default window | ACTION | 0.4.2_RD_AdvisorIntelligence | Single line change |
| 1a-ii. AUA Mix investigation | RESEARCH | 0.4.0_DS_ClientPlatform | Data lineage trace through publisher |
| 1b-i. NNA Oct 2025 stacking | RESEARCH+ACTION | 0.4.0_DS_ClientPlatform + RD | Data inspection first, then patch |
| 1c-i. GRO number audit | RESEARCH | 0.4.0_DS_ClientPlatform | Publisher formula verification |
| 1c-ii. GRO summary container | ACTION | 0.4.2_RD_AdvisorIntelligence | After 1c-i validates numbers |
| 2a. Snapshot drilldown completeness | ACTION | 0.4.2_RD_AdvisorIntelligence | QA all combos: GEO/ADV x AUA/NNA x M/Q/Y |
| 2b. Remove "Period NNA" | ACTION | 0.4.2_RD_AdvisorIntelligence | 3 text changes |
| 2c. Standard capitalization | ACTION | 0.4.2_RD_AdvisorIntelligence + DS | Frontend mapping + possible backend update |
| 2d. Retain cohort across AUA/NNA | ACTION | 0.4.2_RD_AdvisorIntelligence | Remove `metric` from reset useEffect deps |
| 2e. Show all cohorts in snapshot | ACTION | 0.4.2_RD_AdvisorIntelligence + DS | May need backend if publisher pre-aggregates |
| 2f. Continuous: all top-level, top 8 drill | ACTION | 0.4.2_RD_AdvisorIntelligence | Conditional top-N logic |
| 2g. "no_city" -> Other | ACTION | 0.4.2_RD_AdvisorIntelligence | Aggregation fix in city drill |
| 2h. NNA time machine cohort-specific | ACTION | 0.4.2_RD_AdvisorIntelligence | Mirror AUA pattern in NnaQuarterlyStrip; see DE brief |
| 2i. Inherit time window from header | ACTION | 0.4.0_DE_ClientPlatform | State lift / prop threading |
| 3a. Portfolio group + architect quality | RESEARCH | 0.4.0_DS_ClientPlatform | Data investigation: portfolio_group values, true architect logic |
| 3b. Top 3 panel overwritten | ACTION | 0.4.2_RD_AdvisorIntelligence | Move TopTenStackedBar from Panel 1 to Panel 2 |
| 3c. Stacked bar NNA sort | ACTION | 0.4.2_RD_AdvisorIntelligence | Debug sort order in Recharts rendering |
| 3d. Leaderboard visual polish | ACTION | 0.4.2_RD_AdvisorIntelligence | Redesign table; ref SecurityScanner, FactorTilts, KI modal |
| 4a. Gold table data audit | RESEARCH | 0.4.0_DS_ClientPlatform | Audit data availability at each drill level; document gaps |
| 4b. Drill hierarchy enhancement | ACTION | 0.4.0_DE_ClientPlatform + RD | Structural hierarchy exists; enhance at each level |
| 4c. Tax status refinement | ACTION | 0.4.2_RD_AdvisorIntelligence | Minor — folded into Mix/Concentration work |
| 4d. Tax liability (cost basis) | ACTION | 0.4.2_RD_AdvisorIntelligence | Functional today; improve with data audit findings |
| 4e. Mix (asset class breakdown) | RESEARCH+ACTION | 0.4.0_DS_ClientPlatform + RD | Verify ETF classification coverage, build aggregation, implement views |
| 4f. Concentration (security-level) | RESEARCH+ACTION | 0.4.0_DS_ClientPlatform + RD | Linked to Mix; significant data project + frontend |
| 4g. AUA/NNA time series in Books | ACTION | 0.4.0_DE_ClientPlatform + RD | Wire existing data (scripts 05/05b) to L3/L4 views |
| 4h. Advisor listing UI consistency | ACTION | 0.4.2_RD_AdvisorIntelligence | Blocked on 3d; apply same design to Books advisor table |

## Dependency Graph

```
RESEARCH (must complete first — informs downstream ACTION items)
├── 1a-ii. AUA Mix investigation ──────────────────┐
├── 1b-i. NNA Oct 2025 stacking ──────────────────┤
├── 1c-i. GRO number audit ───→ 1c-ii. GRO summary│
├── 3a. Portfolio group + architect quality ────────┤
├── 4a. Gold table data audit ─→ 4e, 4f design ────┤
│                                                   │
ACTION (independent — can start immediately)        │
├── 1a-i. AUA default window (no deps)              │
├── 2b. Remove "Period NNA" (no deps)               │
├── 2c. Standard capitalization (no deps)           │
├── 2d. Retain cohort across toggle (no deps)       │
├── 2e. Show all cohorts (may need DS check)        │
├── 2f. Continuous top-level (no deps)              │
├── 2g. "no_city" → Other (no deps)                 │
├── 2h. NNA time machine cohort-specific (no deps)  │
├── 3b. Top 3 panel layout fix (no deps)            │
├── 3c. Stacked bar NNA sort (no deps)              │
├── 4b. Drill hierarchy (no deps)                   │
├── 4c. Tax status refinement (no deps)             │
├── 4d. Tax liability (no deps)                     │
├── 4g. AUA/NNA time series in Books (no deps)      │
│                                                   │
ACTION (blocked — requires upstream completion)     │
├── 2a. Snapshot drilldown QA (after 2c, 2d, 2e)   │
├── 2i. Inherit time window (DE state lift)         │
├── 3d. Leaderboard visual polish ─→ 4h. Books list │
├── 4e. Mix views (after 4a research) ──────────────┘
└── 4f. Concentration views (after 4a + 4e)
```

## Scope Summary

**Total items:** 26 (across 4 parts)

| Category | Count | Items |
|----------|-------|-------|
| ACTION (no deps, start immediately) | 15 | 1a-i, 2b, 2c, 2d, 2e, 2f, 2g, 2h, 3b, 3c, 4b, 4c, 4d, 4g |
| ACTION (blocked on upstream) | 5 | 1c-ii, 2a, 2i, 3d→4h |
| RESEARCH | 4 | 1a-ii, 1c-i, 3a, 4a |
| RESEARCH + ACTION | 3 | 1b-i, 4e, 4f |

**Critical path:** The heaviest RESEARCH items (4a gold table audit, 3a architect data quality,
1a-ii AUA Mix) should start on Day 1 because they gate downstream ACTION items. The 15
independent ACTIONs can proceed in parallel immediately.

**Pod scope:** Entirely within Pod 0.4 (ClientPlatform). No cross-pod dependencies.
- DS: 4 RESEARCH items (data investigations)
- DE: 2 items (state lift, drill hierarchy coordination)
- RD: 20 items (all frontend ACTION work)
