# Advisor Intelligence — Completion PRD

**Author:** 1.0.0_SA_CTO
**Date:** 2026-03-03
**Status:** ACTIVE — issued to 2.0.0_SA_COO for task order decomposition
**Source:** CEO-CTO interview, 2026-03-03

---

## 1. Context & Scope

Advisor Intelligence is the primary client-facing analytics dashboard for 49 Financial
advisors and firm administrators. The page is at bd-v2.14.0, approximately 85-90%
complete. This PRD covers the remaining work to reach a shippable v1.0 state.

**Pods affected:** Pod 4 (ClientPlatform) exclusively. DE = 0.4.0, DS = 0.4.0,
DT = 0.4.0, RD = 0.4.2_RD_AdvisorIntelligence. Shared infra: 0.6.0_AE_PartnerETL
(BD pipeline), 0.7.0_AE_CloudOps (auth infrastructure).

**Reference files:**
- Portal page: `portal/src/pages/AdvisorIntelligence/`
- API endpoints: `portal/src/api/endpoints/advisor-intelligence.ts`
- Types: `portal/src/pages/AdvisorIntelligence/types.ts`
- Gold scripts: `data/black_diamond/scripts/gold/`
- Lambda publisher: `infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py`
- Advisor publisher: `infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py`

---

## 2. Work Streams and Dependency Order

**Dependency rule:** DS data contract work ALWAYS precedes DE/RD portal work.
DT deploys ONLY after DS commits and `data_contract.xml` is updated.

```
Stream A (DS): CLA timeseries + adv_drill + stacked bar period data
  -> Stream B (DT): Deploy publisher Lambda updates
    -> Stream C (DE + RD): Distribution tab continuous views + Advisors tab redesign

Stream D (COO thread): Books tab design brief (DS + RD + DE)
  -> Stream E (DS): Books data contracts (account, holdings, tax)
    -> Stream F (DT): Deploy advisor-publisher updates
      -> Stream G (DE + RD): Books tab implementation

Stream H (parallel, no dependency): Distribution tab snapshot fixes (RD)
Stream I (parallel, no dependency): Advisors tab portal primitives + sort fix (RD)
Stream J (parallel, starts after thread): Auth gating (DS + AE CloudOps)
```

---

## 3. Distribution Tab

### 3A. Continuous NNA — GEO View

**Current state:** The GEO continuous view renders a single aggregated NNA chart.
The data already exists in `timeseries_chart.json` (`geo` view with per-state
categories, and `geo_drill` with per-city categories under each state).

**Required behavior:**
- By default, render the top-8 states as separate series in the cumulative NNA chart,
  using the same visual format as the Assets Overview header panel's cumulative NNA chart
  (same chart type, axis format, color scheme, date range, window toggle).
- Add a **search input** in the left panel controls that filters across all available
  states, including those outside the top-8.
- Clicking a state from the chart legend or search results drills into that state:
  the chart re-renders showing per-city series for cities within that state
  (sourced from `geo_drill[stateKey]` in `timeseries_chart.json`).
- A back/breadcrumb control returns to the state-level view.

**Data status:** READY. `geo_drill` is deployed in `timeseries_chart.json` as of
bd-v2.14.0 (8 states, up to 10 cities each, ~2,000 data points per city).

**Agents:** DE + 0.4.2_RD | No DS work required for this item.

---

### 3B. Continuous NNA — ADV View

**Required behavior:** Same as 3A but for architects instead of states.
- Top architects as separate series, same chart format as Assets Overview NNA.
- Search input for architects not in top list.
- Click architect → drill to client/relationship level, showing that architect's
  clients as series in the same chart format.
- No drill-down past relationship level (client is the terminal grain for ADV).

**Data gap:** `adv_drill` does NOT yet exist in `timeseries_chart.json`. This is
the per-architect → per-client NNA time series, analogous to `geo_drill`.

**DS task:** Update `bd-portal-publisher/lambda_function.py` to generate `adv_drill`:
```
adv_drill: Record<architect_key, CumulativeChartView>
```
Where each `CumulativeChartView` has categories = the architect's top clients, and
data = cumulative NNA time series per client. Pattern follows `geo_drill` exactly.
Update `data_contract.xml` before handing to DT.

**DT task:** Deploy publisher Lambda update. No Terraform changes expected (Lambda code only).

**Agents:** DS first → DT deploy → DE + 0.4.2_RD

---

### 3C. Snapshot NNA — Bell Curve Math Fix

**Issue:** Negative NNA accounts (net outflows) use `|abs|` for the bell curve
percentile threshold calculation. The update to script 09 in commit `8247c6d0`
(2026-03-02) should have addressed this. Needs verification.

**DS task:** Verify that the negative abs calculation in script 09's bell curve
generation produces correct percentile thresholds for outflow accounts. Specifically,
confirm that the P10/P25/Median/P75/P90 thresholds for the outflow distribution
are computed on the absolute values of negative NNA (not signed values). If the
fix did not land in `8247c6d0`, a targeted patch to script 09 is required.

**Verification:** Inspect current `partner_analytics/header_metrics.json` in S3 and
confirm the `distribution` field for the NNA view's negative segments has non-degenerate
percentile thresholds (not all zeros or symmetric with the positive side).

**Agents:** DS to verify → if patch needed, DS patches + DT deploys EC2 script.

---

### 3D. Snapshot CLA — Simplified Visualization

**Current state:** The CLA snapshot view is incorrectly rendering as a flows chart
(NNA-style), which is not the intent.

**Required behavior:** CLA is not about flows. It is about what percentage of
total AUM is attributable to new clients (NMNC) versus existing clients (NMEC).

Snapshot CLA visualization:
- Two colors only: **green = NMNC** (New Client AUA), **blue = NMEC** (Existing Client AUA)
- Show NMNC% and NMEC% of total AUA as a simple proportional display
- Preferred format: horizontal stacked bar or a split donut — clean, no axes, just
  the two proportions with AUA amounts labeled
- Available for current period and time machine (q1/q2/q3 periods) to show how the
  new-client percentage has shifted over time
- No inflow/outflow data. No NNA. No blue/red flows vocabulary. Just two-color NMNC/NMEC split.

**Data status:** `header_metrics.json` already has `views.aua` and CLA data.
The DS needs to confirm that `cla.current.geo.totals.nmnc_nna` and `nmnc_count`
in the CLA structure are populated correctly for this use case. The portal
`ClaView` type already supports this: `{ segments[], totals: { nna, nmnc_nna, nmec_nna, nmnc_count, nmec_count } }`.

**Agents:** 0.4.2_RD (visualization change) + DS to confirm data is populated.

---

### 3E. Continuous CLA — New Time Series View

**Current state:** Does not exist. Not in `timeseries_chart.json`.

**Required behavior:** A time-series chart (same format as Assets Overview cumulative
NNA chart) showing the composition of total AUM between NMNC (new clients, green)
and NMEC (existing clients, blue) over time. This is a stacked area chart where:
- Y-axis = dollar AUM (absolute, not percentage)
- Two areas stacked: NMNC AUM (green) and NMEC AUM (blue)
- Total height = total firm AUM at each date
- Viewable at: total (firm-wide), state grain (e.g., Texas → shows NMNC/NMEC AUM
  composition for Texas clients), city grain (drill-down from state), architect grain
  (no client drill-down needed for CLA — architect is the terminal grain for ADV-CLA)

Search function: same as 3A/3B — search for states or architects not in the top list.

**Data gap:** This time series does NOT exist anywhere in the current pipeline.
The closest data is `client_performance.parquet` which has daily AUA per relationship.
The DS can join `accounts_dimension_latest` to classify each relationship as NMNC or
NMEC (using the advisor assignment history and account open dates), then aggregate
daily NMNC vs NMEC AUM by state/city/architect.

**DS task:** Design and implement `cla_timeseries` output — either in script 09
(extending the EC2 gold layer) or in the publisher Lambda. The output structure:
```
timeseries_chart.json additions:
  cla: {
    total: CumulativeChartView          // categories: ['nmnc', 'nmec']
    geo: CumulativeChartView            // categories: top states
    adv: CumulativeChartView            // categories: top architects
    geo_drill: Record<state, CumulativeChartView>  // cities within state
    // no adv_drill for CLA
  }
```
Where `CumulativeChartView.data` has `nmnc` and `nmec` AUM values per date point.

Confirm NMNC/NMEC classification logic with DE before committing to data contract.
Update `data_contract.xml` before handing to DT.

**Agents:** DS (design + implement) → DT (deploy) → DE + 0.4.2_RD (render)
**Note:** This is the highest DS effort item in this PRD. Schedule accordingly.

---

## 4. Advisors Tab

### 4A. Portal Primitives Refactor

**Issue:** Advisors tab uses ad-hoc layout containers instead of the portal's
standard `Panel`, `PanelHeader`, `PanelContent`, `SmartPanelFooter` from
`@/ui/components/panels`. This breaks visual consistency with the rest of the portal.

**Required behavior:** All sections in the Advisors tab (Top Performers panel,
Rolling Flows panel, Leaderboard panel) must use portal panel primitives.

**Agents:** 0.4.2_RD | No data changes required.

---

### 4B. Top Performers — Stronger Visual Identity

**Issue:** The current Top 3 highlights panel is visually weak — does not
communicate rank and achievement clearly.

**Required behavior:** Top Performers should feel like a podium or headline card
with clear rank (1st/2nd/3rd), the advisor name prominent, and the key metric
(NNA for the active period) immediately readable. Consider trophy/medal iconography
or rank-badge treatment consistent with Lucide icons available in the codebase.

**Agents:** 0.4.2_RD | DE reviews before pushing.

---

### 4C. Rolling Flows — New Visualization Model

**Current state:** Advisors tab shows rolling flows with 30d/90d/1Y window toggles
as line charts. This is low-signal and not anchored to business periods.

**New model — two views, one toggle set:**

**Primary view: Stacked Bar Chart (default)**
- X-axis: architects or implementors (one bar per person)
- Bars stacked: Inflows (positive, e.g. teal), Outflows (negative, inverted downward
  or shown as a negative bar segment), NNA net (implied by the two)
- Sorted lowest to highest by NNA so the highest performers are visually rightmost
- Period toggle: QTD / YTD / 1Y / 3Y / Max
- Architects/Implementors toggle at top (controls both views)

**Secondary view: 1-Year Rolling Line Chart**
- X-axis: date (over the selected period window)
- Y-axis: 1-year rolling NNA value for each advisor
- One line per advisor (top performers by default, all accessible via search/toggle)
- Period toggle controls the x-axis window (how far back dates go), NOT the rolling window
- Rolling window is FIXED at 1 year (full year trailing from each date point)
- Same Architects/Implementors toggle

**Data gap:** Script 10 currently produces trailing rolling NNA at 30d/90d/1Y windows.
This needs:
1. Period-anchored aggregated NNA with inflows/outflows per advisor for stacked bar:
   - QTD = sum from start of current quarter to today
   - YTD = sum from Jan 1 to today
   - 1Y = sum from 1 year ago to today
   - 3Y = sum from 3 years ago to today
   - Max = inception to today
   - For each period: inflows, outflows, nna_net per architect and per implementor
2. 1-year rolling NNA per advisor (daily points) for the line chart — this already
   conceptually exists in script 10 but may need the window fixed at 1Y and date
   range extended to support 3Y/Max x-axis windows

**DS task:** Update script 10 (or produce supplemental output) to generate:
```
advisor_rolling_flows.json additions or replacement:
  stacked_bar: {
    architects: { [period: 'qtd'|'ytd'|'1y'|'3y'|'max']: AdvisorBarEntry[] }
    implementors: { [period]: AdvisorBarEntry[] }
  }
  rolling_1y: {
    architects: AdvisorRollingSeries[]   // daily points, 1Y rolling window
    implementors: AdvisorRollingSeries[]
  }
```
Where `AdvisorBarEntry = { name, inflows, outflows, nna_net }`.
Update `data_contract.xml` before handing to DT.

**Agents:** DS → DT → 0.4.2_RD | DE reviews.

---

### 4D. Leaderboard Sort Stability

**Issue:** Leaderboard entries occasionally render out of order.

**Investigation needed:** Determine whether the issue is:
(a) Frontend sort instability on ties (JS `.sort()` is not stable in all engines for
    equal NNA values), or
(b) Data issue (leaderboard entries in `architect_leaderboard.json` not pre-sorted by rank).

**Fix:** If (a) — use a stable sort (add secondary sort key, e.g. `name`, for ties).
If (b) — fix sort in the publisher Lambda and ensure `rank` field is set correctly.

**Agents:** DE to investigate → 0.4.2_RD if frontend fix, DS + DT if data fix.

---

## 5. Books Tab

### 5A. Access Gating Model

The Books tab serves two user classes with fundamentally different views:

**Admin (L1 — visible only when `userRole === 'admin'`):**
- Sees all advisors in the firm via an advisor selector dropdown
- Can drill into any client's detail view
- L1 is gated to internal users (`isInternal() || isDev()`) using existing `useAuth` pattern

**Advisor (L2 — default landing for non-admins):**
- Lands directly on their own book at login — no dropdown, no selection required
- The portal must resolve the logged-in user → their advisor identity in the gold layer
- Advisor can drill into their own relationships (L3) and accounts (L4)
- Advisor CANNOT see other advisors' relationships or client detail

**Identity resolution (critical path):**
Mapping JWT `userId` → advisor name/ID requires querying `opal-users-v2` DynamoDB table.
This table stores user records keyed by some user identifier. The DS must:
1. Confirm the schema of `opal-users-v2` (what fields identify an advisor)
2. Confirm how those fields map to `accounts_dimension_latest.architect` or
   `rel_architect_lookup.parquet` in the gold layer
3. Determine whether the mapping exists or needs a new registration step
This linkage is the linchpin of the entire Books access model.

**Architecture decision (pending DS investigation):**
The identity resolution should happen at the Lambda level (the API Lambda reads
`opal-users-v2` and scopes its response to the calling user's advisor identity).
The portal should NOT receive cross-advisor data and rely on client-side filtering.
The `opal-partners-data` Lambda or `bd-client-detail` Lambda are the likely candidates
for implementing this scoping.

**Agents:** DS (investigate opal-users-v2 schema) → coordinate with 0.7.0_AE_CloudOps
(auth infrastructure) → DT (deploy Lambda changes).

---

### 5B. Books Tab Hierarchy and Data Scope

**L2 — Advisor Book (aggregate of all relationships):**
- Summary metrics: total AUA, total client count, account count, NNA YTD/QTD/MTD
- AUA composition by client segment (NMNC/NMEC), by geography, by account type
- Tax exposure summary: taxable/deferred/free breakdown (from `client_tax_liability`)
- Income and fees: dividends, interest, fees (from `client_performance`)
- Portfolio composition: asset allocation, expense ratio, concentration
- Engagement: trading activity, avg relationship tenure, active %
- Client list sorted by AUA (for navigation to L3)

**L3 — Relationship/Client view:**
- Same sections as L2 but scoped to one relationship
- Full client detail: all accounts under this relationship
- Performance time series for this relationship's total AUA

**L4 — Account + Holdings:**
- Account-level: AUA, account type, tax status, open date
- Holdings: position list with ticker, name, asset class, current value, weight
- Cost basis and unrealized gain/loss per position (from `03_build_holdings_lots.py`)
- Tax intelligence (primary view): summary of embedded gain/loss by tax status,
  estimated tax liability, positions sorted by unrealized gain
- Lot-level drill-down (secondary, on-demand): individual lots, acquisition date,
  cost basis, unrealized gain/loss — for tax harvest decision support

**Data status for Books:**
- `clients_tab.json`, `advisors/{id}/book.json`: produced by `bd-portal-advisor-publisher`
- Account-level data (`05b_build_account_performance.py`): exists in gold tables
- Holdings lots (`03_build_holdings_lots.py`): exists, with FIFO cost basis
- Tax liability (`06_build_client_tax_liability.py`): exists
- Gap: the publisher Lambda likely does not yet populate all L4 fields. DS must audit
  which fields are present vs. missing from current `clients/{clientKey}.json` output.

---

### 5C. Books Tab — Design Thread Required (COO Action)

The visual design and component decomposition for Books has significant ambiguity.
Before any DE/RD implementation work begins, the COO must run a **bespoke 3-party
thread** to produce a Books design brief:

**Thread configuration:**
- Participants: `0.4.0_DS_ClientPlatform` + `0.4.2_RD_AdvisorIntelligence` + `0.4.0_DE_ClientPlatform`
- Type: Bespoke (gpt-4o, tools enabled, 3 max turns)
- CONTEXT.json must include (M1):
  - `data/black_diamond/scripts/gold/` key script outputs (03, 05b, 06 output shapes)
  - `infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py`
  - `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx`
  - `portal/src/pages/AdvisorIntelligence/ClientDetail/` directory
  - Current `clients_tab.json` S3 output sample
- Opening message must include (M2): DS to push back on any answer not anchored to a specific field in the gold tables or Lambda output.
- Opening question: DS describes what data is available in the gold layer for L2-L4. RD proposes visual layout for each level. DE identifies wiring gaps and component reuse opportunities.

**Thread deliverable:** A markdown design brief at `docs/architecture/advisor_intelligence/books_tab_design_brief.md` covering:
1. L2 advisor book layout (section breakdown with data field mappings)
2. L3 relationship view layout
3. L4 account + holdings view layout with tax summary and lot drill-down
4. Component reuse opportunities (what can be shared across L2/L3/L4)
5. Data gaps DS needs to close before RD can implement

This brief becomes an addendum to this PRD and the source document for the Books tab task orders.

---

## 6. Cross-Cutting: firmId Auth Refactor

**Current state:** Scoped endpoints pass `firmId` as a URL query parameter
(`?firmId=49financial`). This is a security gap — the backend must not trust the
client to self-identify.

**Required state:** `firmId` should come exclusively from the JWT authorizer context
(Cognito `custom:firmId` claim or equivalent). The Lambda reads it from the
`requestContext.authorizer` object injected by API Gateway, not from the query string.

**Scope:** Affects `opal-partners-data` Lambda and any other Lambda that currently
reads `firmId` from the query string for scoped endpoints.

**Agents:** 0.7.0_AE_CloudOps (Cognito claim configuration) + 0.4.0_DT (Lambda update).
This is not blocking completion but must be scheduled before external advisor access goes live.

---

## 7. Work Stream Summary for COO

| Stream | Work | Owner(s) | Blocks |
|--------|------|----------|--------|
| A1 | adv_drill in timeseries_chart.json | 0.4.0_DS | Stream B1, 3B RD |
| A2 | cla_timeseries in timeseries_chart.json | 0.4.0_DS | Stream B1, 3E RD |
| A3 | Stacked bar + 1Y rolling data in advisor_rolling_flows.json | 0.4.0_DS | Stream B2, 4C RD |
| A4 | Snapshot NNA bell curve math verification | 0.4.0_DS | 3C RD (if patch needed) |
| A5 | opal-users-v2 advisor mapping investigation | 0.4.0_DS | Stream J |
| B1 | Deploy bd-portal-publisher with adv_drill + cla_timeseries | 0.4.0_DT | 3B RD, 3E RD |
| B2 | Deploy script 10 updates (stacked bar data) | 0.4.0_DT | 4C RD |
| C1 | Continuous NNA GEO rendering + search + city drill-down | 0.4.2_RD | -- |
| C2 | Continuous NNA ADV rendering + search + client drill-down | 0.4.2_RD | B1 |
| C3 | Snapshot CLA simplified visualization | 0.4.2_RD | -- |
| C4 | Continuous CLA time series rendering | 0.4.2_RD | B1 |
| D | Books tab design thread (COO orchestrates) | COO | Stream E |
| E | Books data contract (DS audits publisher, closes L4 gaps) | 0.4.0_DS | Stream F |
| F | Deploy advisor-publisher with L4 fields | 0.4.0_DT | Stream G |
| G | Books tab implementation | 0.4.0_DE + 0.4.2_RD | F |
| H | Advisors tab portal primitives refactor | 0.4.2_RD | -- (parallel) |
| I | Top Performers visual identity | 0.4.2_RD | -- (parallel) |
| I2 | Leaderboard sort stability investigation + fix | 0.4.0_DE | -- (parallel) |
| J | firmId auth refactor | 0.7.0_AE_CloudOps + 0.4.0_DT | -- (not blocking) |

**Immediate parallel starts (no dependencies):**
Streams A1, A2, A3, A4, A5 (all DS), plus C1 (RD — data already exists), H, I, I2.

---

## 8. Out of Scope for This Release

- `AssetIntelligenceTab.tsx` — exists but not wired to navigation. Formally deferred.
  Will not be wired until Books tab is complete. Revisit in a follow-on PRD.
- Dual timestamp display (`data_as_of` in portal header) — minor polish, tracked
  separately by DE. Non-blocking.
- CausalityEngine — separate initiative, separate PRD.

---

*This document is the single source of truth for AdvisorIntelligence completion.*
*COO: decompose into task orders using the work stream table in Section 7.*
*Reference this document by path in all related task orders.*
