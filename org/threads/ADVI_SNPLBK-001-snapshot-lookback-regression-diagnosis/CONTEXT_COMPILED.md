# Thread Context -- Snapshot Lookback Regression Diagnosis

**Thread ID:** ADVI_SNPLBK-001-snapshot-lookback-regression-diagnosis
**Created by:** 0.4.0_DS_ClientPlatform
**Created at:** 2026-03-10T18:09:53Z

---

## Participants

### 0.4.0_DE_ClientPlatform

# Agent 0.4.0_DE_ClientPlatform — Dashboard Engineer PM

| Field | Value |
|-------|-------|
| **Agent ID** | 0.4.0_DE_ClientPlatform |
| **Role** | Dashboard Engineer |
| **Title** | PM — Client Platform Pod |
| **Tier** | 2 (Senior) |
| **Reports To** | 1.0.0_SA_CTO, 2.0.0_SA_COO |

---

## Full Team Roster

| Serial | Role | Name | Folder | Pages |
|--------|------|------|--------|-------|
| 0.4.0_DT_ClientPlatform | DevOps Technician | Deploy partner | `org/tier2_senior/0.4.0_DT_ClientPlatform/` | All pod pages |
| 0.4.0_DS_ClientPlatform | Data Scientist | Data partner | `org/tier2_senior/0.4.0_DS_ClientPlatform/` | All pod pages |
| 0.4.1_RD_ModelPortfolios | React Designer | ModelPortfolios | `org/tier3_junior/0.4.1_RD_ModelPortfolios/` | ModelPortfolios |
| 0.4.2_RD_AdvisorIntelligence | React Designer | AdvisorIntelligence | `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/` | AdvisorIntelligence |

---

## Portal Pages Owned

| Page | Directory | RD Agent |
|------|-----------|----------|
| ModelPortfolios | `portal/src/pages/ModelPortfolios/` | 0.4.1_RD_ModelPortfolios |
| AdvisorIntelligence | `portal/src/pages/AdvisorIntelligence/` | 0.4.2_RD_AdvisorIntelligence |

---

## Abilities & Permissions

### CAN DO
- **Commit** portal code — ad-hoc commits to ANY portal path (pages, shared components, API endpoints, types, hooks, utils)
- Write task order documents for your leaf agents and DS/DT partners
- Read and review any file in the codebase
- Write session logs and documentation

### MUST DO
- **Session logs are MANDATORY** — This is how upper management (CTO/COO) understands your segment
- **Launch protocol:** On every session start, review recent commits from your RD agents. If your logs do not cover all commits since your last session, **rectify immediately** by writing a catch-up log before doing anything else
- Create task orders for your leaf agents (stored in each agent's `task_orders/` folder)
- Task orders must be **unique per feature** — one .md file per feature, named after the feature
- Tag commits with your serial and `--author` flag:
  `git commit --author="0.4.0_DE_ClientPlatform <0.4.0_DE_ClientPlatform@opal.agent>" -m "0.4.0_DE_ClientPlatform: <description>"`

### CANNOT DO
- **Push** to any branch — all pushes are DT responsibility (DT is the QA gate)
- **Deploy AWS resources** (Lambda, EC2, Terraform — DT/AE responsibility)
- Modify infrastructure files in `infra/aws/`

---

## Task Order Paths

Write task orders to these exact paths:

```
org/tier3_junior/0.4.1_RD_ModelPortfolios/task_orders/{feature_name}.md
org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/{feature_name}.md
org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/{feature_name}.md
org/tier2_senior/0.4.0_DT_ClientPlatform/task_orders/{feature_name}.md
```

Receive task orders from CTO/COO/Andrew at:
```
org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/
```

---

## Session Logs

Location: `org/tier2_senior/0.4.0_DE_ClientPlatform/logs/YYYY-MM-DD/`
Template: Standard log format in AGENT_START_HERE.md. Required sections: Current State and Next Steps.

---

## Launch Protocol (Every Session)

```
1. Read your own recent logs (org/tier2_senior/0.4.0_DE_ClientPlatform/logs/)
2. Review recent git commits from your RD agents:
   grep for 0.4.1_RD, 0.4.2_RD in commit messages
3. If any commits are NOT covered by your existing session logs:
   -> Write a catch-up session log BEFORE doing anything else
4. Check task_orders/ for new instructions from CTO/COO/Andrew
5. Check task order status of outstanding orders you've issued
6. Proceed with normal work
```

## Session Log Format

**DE logs include commit hashes in the header:**

```
**Portal DEV commits:** `abc1234` -> `def5678` -> `ghi9012`
**Workspace CLOUD commit:** `jkl3456`
```

**Files Modified must be a table with commit column:**

```
| File | Change | Committed |
|------|--------|-----------|
| portal/src/pages/X/Component.tsx | What changed | Yes - `abc1234` |
| docs/briefs/feature.md | New brief | Yes - CLOUD `jkl3456` |
```

**When something breaks, embed a Postmortem section** between Work Completed and Decisions Made:

```
## Postmortem: [What broke]

### Root Cause
[Specific cause — name the file, function, or data shape that was wrong]

### Mismatches Found

| Field | Expected (portal) | Actual (backend) |
|-------|-------------------|------------------|
| views | { aua, nna, geo, adv } | { geo, adv } only |

### Resolution
- Task A: [what was fixed] — DONE / BLOCKED / [Agent name]
- Task B: [what remains] — BLOCKED on [Agent]
```

**Next Steps must name the receiving agent in brackets:**
`[DevOps] Run gold layer FULL mode — brief at docs/briefs/devops-brief-feature.md`
`[Dashboard Engineer] Verify Distribution tab after data refresh`


### 0.4.2_RD_AdvisorIntelligence

# Agent 0.4.2_RD_AdvisorIntelligence — React Designer

| Field | Value |
|-------|-------|
| **Agent ID** | 0.4.2_RD_AdvisorIntelligence |
| **Role** | React Designer |
| **Tier** | 3 (Junior) |
| **Pod** | ClientPlatform |
| **Reports To** | 0.4.0_DE_ClientPlatform |
| **Page** | AdvisorIntelligence |

## Responsibility

UI design and React component development for the AdvisorIntelligence page. Complex page: Leaderboard tab, Distribution tab, Assets Overview panel, partner analytics (donut/time machine/bell curve), rolling flows chart, cumulative charts.

## Abilities & Permissions

### CAN DO
- **Commit** portal code changes — LIMITED to files under `portal/src/pages/AdvisorIntelligence/`
- Read any file in the codebase for reference

### MUST DO
- **Use `--author` on every commit** with your serial in the message:
  `git commit --author="0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>" -m "0.4.2_RD_AdvisorIntelligence: AdvisorIntelligence -- <description>"`
  - Include tab if relevant: `AdvisorIntelligence/LeaderboardTab -- <description>`
- Commit only specific files you changed

### CANNOT DO
- Push to any remote branch | Deploy AWS resources | Commit outside page dir | Modify shared code

### SESSION LOGS (Encouraged, not mandatory)
- Location: `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/logs/YYYY-MM-DD/`
- Naming: `AdvisorIntelligence_{tab}_{feature}.md`

### TASK ORDER COMPLETION
- When you finish a task order, **edit the file** and change `<status>pending</status>` to `<status>complete</status>`
- This is how your DE PM knows you are done — no separate notification needed

### TASK ORDERS
- Your task orders: `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/`

## Key Paths
- Page directory: `portal/src/pages/AdvisorIntelligence/`

## Shipping Protocol

Every session where you ship code changes, complete these steps **before closing**:

1. **Update `deliverables/page_inventory.xml`** — edit only the entries that reflect what changed: new or removed `<file>` entries, modified `<api_call>` shapes, new or resolved `<issue>` tags, updated `<tab>` status. Do not re-audit the whole file — only update what you touched.
2. **Write your session log** — `logs/YYYY-MM-DD/{page}_{feature}.md`
3. **Commit all three together** — your code changes, updated XML, and session log in one commit

The XML is the authoritative live state of your page. Your DE PM and higher-tier agents read it to understand your pod. Keep it accurate.


---

## Reference Material

### Briefing Notes

DIAGNOSTIC THREAD: The Segment Analytics panel (Distribution tab, Snapshot view) previously displayed data from the current quarter plus 3 prior quarters via a 'time machine' strip. This lookback is no longer rendering. The regression could be: (A) backend -- script 09_generate_partner_analytics.py stopped producing q1/q2/q3 period data in its output JSON, (B) frontend -- DistributionTab.tsx or types.ts changed how it reads period data during 49FNV3 work, or (C) publisher -- the bd-portal-publisher Lambda is overwriting the EC2 output (unlikely since partner_analytics is DISABLED in the publisher). DS is the knowledge source for the backend data pipeline and gold scripts. DE is the knowledge source for API wiring and TypeScript interfaces. RD is the knowledge source for how the DistributionTab renders the time machine. Each agent must inspect their layer and report whether the data contract is intact at their boundary. The deliverable is a definitive root-cause diagnosis: which layer broke, which file, and what the fix is.


### advisorintelligence-types-periodsnapshot-partneranalyticsviewwithperiods-hastimemachine.ts

```
/**
 * Advisor Intelligence Page Types - v2
 *
 * Partner AUA analytics and reporting interfaces
 * Based on ADVISOR_INTELLIGENCE_DATA_SPEC.md
 */

// ============================================================================
// Partner/Firm Types (kept from v1)
// ============================================================================

export interface Partner {
  firmId: string
  firmName: string
  tier: 'advisor' | 'subadvisor' | 'branch'
  parentFirmId: string | null
}

export interface PartnersResponse {
  partners: Partner[]
}

// ============================================================================
// Metrics & Dimensions Constants
// ============================================================================

export type MetricId = 'nmnc' | 'nmec_na' | 'nmec_sa' | 'nna_inflow' | 'nna_outflow' | 'nna_net'

export interface MetricOption {
  id: MetricId
  label: string
  description?: string
}

// ============================================================================
// Tab 1: Asset Intelligence Types
// ============================================================================

// NNA metric values for a dimension value
export interface NNAMetrics {
  nmnc: number
  nmec_na: number
  nmec_sa: number
  nna_inflow: number
  nna_outflow: number
  nna_net: number
}

// Time series period data
export interface TimeSeriesPeriod {
  period: string  // "2025-01"
  [dimensionValue: string]: NNAMetrics | string  // string for period key
}

// Time series response from API
export interface TimeSeriesResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  granularity: 'monthly'
  dimension: string
  dimension_values: string[]
  metrics: string[]
  data: TimeSeriesPeriod[]
}

// Category time series (NMNC/NMEC breakdown without dimension)
export interface CategoryTimeSeriesPeriod {
  period: string
  nmnc: number
  nmec_na: number
  nmec_sa: number
  total_inflow: number
  outflow: number
  net: number
}

export interface CategoryTimeSeriesResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  granularity: 'monthly'
  data: CategoryTimeSeriesPeriod[]
}

// Snapshot row for AUA breakdown
export interface SnapshotRow {
  value: string
  aua: number
  aua_pct: number
  client_count: number
  account_count: number
}

// Snapshot response from API
export interface SnapshotResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  dimension: string
  total_aua: number
  data: SnapshotRow[]
}

// Filter dimension value
export interface FilterValue {
  id: string
  name: string
  aua?: number
}

// Filter dimension definition
export interface FilterDimension {
  label: string
  values: FilterValue[]
}

// Filters response from API
export interface FiltersResponse {
  generated_at: string
  firm_id: string
  dimensions: Record<string, FilterDimension>
}

// ============================================================================
// Tab 2: Clients Types
// ============================================================================

// Client growth period data
export interface ClientGrowthPeriod {
  period: string
  total_clients: number
  total_aua: number
  avg_aua_per_client: number
  new_clients_added: number
  clients_lost: number
}

// Client growth response from API
export interface ClientGrowthResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  granularity: 'monthly'
  summary: {
    total_clients: number
    avg_growth_rate_ytd: number
    median_aua: number
  }
  data: ClientGrowthPeriod[]
}

// Pie chart data point
export interface PieChartDataPoint {
  label: string
  value: number
  pct: number
  color: string
}

// Pie chart definition
export interface PieChartData {
  title: string
  data: PieChartDataPoint[]
}

// Tax basis breakdown response
export interface TaxBasisBreakdownResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  charts: {
    tax_status: PieChartData
    cost_basis_sync: PieChartData
    account_type: PieChartData
  }
}

// Tax-deferred candidate
export interface TaxDeferredCandidate {
  relationship_id: string
  relationship_name: string
  architect: string
  taxable_aua: number
  account_count: number
  cost_basis_synced: boolean
  last_nna_date: string
  priority_score: number  // 0-100
}

// Tax-deferred candidates response
export interface TaxDeferredResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  scan_criteria: {
    min_taxable_aua: number
    tax_status: string
    cost_basis_synced: boolean
  }
  summary: {
    total_candidates: number
    total_opportunity_aua: number
  }
  candidates: TaxDeferredCandidate[]
}

// ============================================================================
// Header Metrics Types (v3 - matches SmartX aum-metrics pattern)
// ============================================================================

// Quarterly NNA breakdown
export interface QuarterlyNNA {
  nna: number
  change?: number
  growth?: number
}

// Total metrics (matching SmartX aum-metrics structure)
export interface HeaderTotal {
  aua: number
  nna_mtd: number
  nna_qtd: number
  nna_ytd: number
  nna_12m: number
  client_count: number
  account_count: number
  new_client_aua: number
  existing_client_aua: number
  new_client_count: number
  existing_client_count: number
  new_client_pct: number
  q0: QuarterlyNNA
  q1: QuarterlyNNA
  q2: QuarterlyNNA
  q3: QuarterlyNNA
}

// Radial chart segment (NMNC/NMEC/Existing)
export interface RadialSegment {
  segment: string
  label: string
  aua: number
  aua_pct: number
  client_count: number
  color: string
}

// Radial chart data for donut
export interface RadialData {
  title: string
  data: RadialSegment[]
}

// Distribution percentiles
export interface DistributionPercentiles {
  p10: number | null
  p25: number | null
  p50: number | null
  p75: number | null
  p90: number | null
}

// Histogram data for bell curve
export interface HistogramData {
  bins: number[]
  counts: number[]
  bin_labels: string[]
}

// Distribution stats (matches SmartX DistributionStats pattern)
export interface DistributionStats {
  count: number
  total: number
  mean: number | null
  median: number | null
  percentiles: DistributionPercentiles
  min: number | null
  max: number | null
  std_dev: number | null
  histogram: HistogramData
  // Y6c: Split inflow/outflow percentiles (signed NNA distributions)
  inflow_percentiles?: DistributionPercentiles
  outflow_percentiles?: DistributionPercentiles
  inflow_count?: number
  outflow_count?: number
}

// Segment distribution with label
export interface SegmentDistribution extends DistributionStats {
  label: string
}

// Account distribution data
export interface AccountDistributionData {
  total: DistributionStats
  by_segment: {
    NMNC: SegmentDistribution
    NMEC: SegmentDistribution
    Existing: SegmentDistribution
  }
}

// Architect breakdown row
export interface ArchitectBreakdown {
  architect: string
  aua: number
  aua_pct: number
  client_count: number
  account_count: number
}

// Rolling 12-month timeseries data point
export interface RollingTimeseriesDataPoint {
  date: string           // "2021-01-01"
  month: string          // "2021-01"
  total_aua: number
  rolling_12m_nmnc: number
  rolling_12m_nmec: number
  existing_aua: number
  nmnc_pct: number
  nmec_pct: number
  existing_pct: number
  nmnc_client_count: number
  nmec_client_count: number
}

// Rolling timeseries structure
export interface RollingTimeseries {
  description: string
  data: RollingTimeseriesDataPoint[]
}

// ============================================================================
// Cumulative Time Series Chart Types (v6 - "Graph Goes Up")
// ============================================================================

// Single data point for cumulative chart
export interface CumulativeChartDataPoint {
  date: string
  [category: string]: string | number  // Dynamic categories (NMNC, NMEC, TX, etc.)
}

// View data for cumulative chart
export interface CumulativeChartView {
  description: string
  categories: string[]
  data: CumulativeChartDataPoint[]
}

// Full cumulative chart response
export interface CumulativeChartResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  date_range: {
    start: string
    end: string
    days: number
  }
  metadata?: TimeseriesChartMetadata  // Includes new_clients by window
  aua: CumulativeChartView   // Cumulative NNA by client cohort
  nna: CumulativeChartView   // Daily NNA flows
  geo: CumulativeChartView   // Cumulative NNA by region
  adv: CumulativeChartView   // Cumulative NNA by architect
  geo_drill?: Record<string, CumulativeChartView>  // State -> city drill-down
  adv_drill?: Record<string, CumulativeChartView>  // Architect -> client drill-down
  cla?: {                                           // Client Lifecycle Analysis (NMNC/NMEC)
    total: CumulativeChartView
    geo_drill: Record<string, CumulativeChartView>
    adv_drill: Record<string, CumulativeChartView>
    geo_city_drill?: Record<string, Record<string, CumulativeChartView>>
  }
  // Y5: Monthly AUA change decomposed into market appreciation + NNA
  growth_decomposition?: GrowthDecompositionView
  // Y9: Cumulative NNA with inflow/outflow by state/architect
  nna_geo?: NNASeriesView
  nna_adv?: NNASeriesView
  nna_geo_drill?: NNAGeoDrillView
  // Y3: Asset class AUA breakdown (monthly snapshots from holdings_lots)
  aua_mix?: AuaMixView
}

// View mode for the chart toggle
export type CumulativeChartViewMode = 'aua' | 'nna' | 'geo' | 'adv'

// Window options for date range filter
export type ChartWindowOption = '3M' | '6M' | '1Y' | '2Y' | '3Y' | 'Max'

// Full header metrics response (matches header_metrics.json)
export interface HeaderMetricsResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  firm_name: string
  dates: {
    q0: string
    q1: string
    q2: string
    q3: string
  }
  total: HeaderTotal
  by_architect: ArchitectBreakdown[]
  radial_12m: RadialData
  account_distribution: AccountDistributionData
  timeseries?: RollingTimeseries  // Rolling 12M data for area chart
}

// Legacy HeaderSummary (for backwards compatibility)
export interface HeaderSummary {
  as_of_date: string
  total_aua: number
  nna_ytd: number
  nmnc_ytd: number
  nmec_ytd: number
  client_count: number
}

// ============================================================================
// Partner Analytics Types (v5 - Nested Drill-Down & Time Machine)
// ============================================================================

// Base view modes (shown in toggle)
// - aua: Default view - AUA by client type (reads from nna.current.aua)
// - nna: Flows view - Net new assets with drill-down (reads from nna.current.flows)
// - geo: Geographic breakdown with city drill-down
// - adv: Architect breakdown with client drill-down
export type PartnerAnalyticsBaseView = 'aua' | 'nna' | 'geo' | 'adv'

// Extended view modes (includes drill-down states for internal tracking)
// - city: accessed via GEO drill-down (not a separate view)
// - client: accessed via ADV drill-down (not a separate view)
export type PartnerAnalyticsViewMode = PartnerAnalyticsBaseView | 'city' | 'client'

// Time period keys for time machine
export type TimePeriodKey = 'current' | 'q1' | 'q2' | 'q3'

// ----------------------------------------------------------------------------
// Nested Segment Types (for drill-down)
// ----------------------------------------------------------------------------

// City segment (nested inside GEO state segments)
export interface CitySegment {
  key: string              // "austin_tx"
  label: string            // "Austin"
  aua: number
  aua_pct: number          // % within parent state
  client_count: number
  color: string
  rank?: number            // 1-9 for top cities, null for "Other"
  distribution?: DistributionStats  // Distribution for this city's clients
}

// Client/Relationship segment (nested inside ADV architect segments)
export interface ClientSegment {
  key: string              // "client_123" or relationship_id
  label: string            // "Smith Family Trust" (may be anonymized)
  aua: number
  aua_pct: number          // % within parent architect
  account_count: number
  color: string
  rank?: number            // 1-5 for top clients, null for "Other"
  distribution?: DistributionStats  // Distribution for this client's accounts
}

// NNA flow segment (for NNA drill-down showing inflows/outflows)
export interface NnaFlowSegment {
  key: string              // "nmnc_inflows", "nmnc_outflows", etc.
  label: string            // "Inflows (New Clients)", "Outflows (New Clients)"
  value: number            // Flow amount (positive for inflows, negative for outflows)
  flow_type: 'inflow' | 'outflow'
  color: string
}

// Donut segment with optional nested children for drill-down
export interface DonutSegment {
  key: string
  label: string
  aua: number
  aua_pct: number
  client_count: number
  color: string

  // NNA-specific fields (used when viewing NNA - net flows instead of AUA)
  value?: number           // Net flow amount (for NNA view)
  value_pct?: number       // Percentage of total net flows (for NNA view)
  period_inflows?: number  // Gross inflows during period
  period_outflows?: number // Gross outflows during period (negative)
  flows?: NnaFlowSegment[] // NNA: nested inflows/outflows for drill-down

  // Nested drill-down data (only present for GEO and ADV views)
  cities?: CitySegment[]      // GEO: nested cities within this state
  clients?: ClientSegment[]   // ADV: nested clients under this architect

  // Distribution for this segment (enables drill-down distribution tracking)
  distribution?: DistributionStats
}

// Donut chart data
export interface DonutData {
  title: string
  total: number
  segments: DonutSegment[]
}

// ----------------------------------------------------------------------------
// Period Metrics (for Time Machine)
// ----------------------------------------------------------------------------

// Metrics for a specific time period
export interface PeriodMetrics {
  aua: number
  client_count: number

  // Change vs current (only present in historical periods)
  aua_change_pct?: number    // % change FROM this period TO current (positive = growth)
  client_change?: number     // Net client count change since this period

  // Optional NNA data for the period
  nna_in_period?: number     // NNA flows during this period
  nna_ytd?: number           // NNA year-to-date as of this period
}

// View metrics (legacy format for backwards compatibility)
export interface ViewMetrics {
  aua: number
  nna_ytd: number
  q0: QuarterlyNNA
  q1: QuarterlyNNA
  q2: QuarterlyNNA
}

// ----------------------------------------------------------------------------
// Distribution Types
// ----------------------------------------------------------------------------

// Distribution data with by_segment breakdown
export interface ViewDistribution {
  total: DistributionStats
  by_segment: Record<string, DistributionStats>
}

// ----------------------------------------------------------------------------
// Period Snapshot (single point in time)
// ----------------------------------------------------------------------------

// A view snapshot at a specific point in time
export interface PeriodSnapshot {
  donut: DonutData
  distribution: ViewDistribution  // Script 09 populates for all periods
  metrics: PeriodMetrics
}

// ----------------------------------------------------------------------------
// View with Time Machine Support
// ----------------------------------------------------------------------------

// Single view with multiple period snapshots
export interface PartnerAnalyticsViewWithPeriods {
  current: PeriodSnapshot
  q1?: PeriodSnapshot          // Last quarter (e.g., "Q4 '25")
  q2?: PeriodSnapshot          // 2 quarters ago (e.g., "Q3 '25")
  q3?: PeriodSnapshot          // 3 quarters ago (e.g., "Q2 '25")
}

// Legacy single view data structure (backwards compatible)
export interface PartnerAnalyticsView {
  donut: DonutData
  distribution: ViewDistribution
  metrics: ViewMetrics
}

// ----------------------------------------------------------------------------
// Period Metadata
// ----------------------------------------------------------------------------

// Period definition with date and display label
export interface PeriodDefinition {
  date: string                 // "2025-12-31"
  label: string                // "Q4 '25"
}

// All periods metadata
export interface PeriodsMetadata {
  current: PeriodDefinition
  q1: PeriodDefinition
  q2: PeriodDefinition
  q3: PeriodDefinition
}

// ----------------------------------------------------------------------------
// Full Response Types
// ----------------------------------------------------------------------------

// ----------------------------------------------------------------------------
// CLA (Client Lifecycle Analysis) Types
// ----------------------------------------------------------------------------

export interface LifecycleBucket {
  nna: number
  inflows: number
  outflows: number
  count: number
}

export interface ClaSegment {
  key: string
  label: string
  nna_total: number
  nmnc: LifecycleBucket
  nmec: LifecycleBucket
}

export interface ClaTotals {
  nna: number
  nmnc_nna: number
  nmec_nna: number
  nmnc_count: number
  nmec_count: number
}

export interface ClaView {
  segments: ClaSegment[]
  totals: ClaTotals
}

// ----------------------------------------------------------------------------
// NNA View Types (nested by cohort within period)
// ----------------------------------------------------------------------------

export interface NnaView {
  donut: DonutData & { total_abs: number }
  distribution: ViewDistribution
  metrics: { nna: number; client_count: number }
  // Y6b: GEO drill — views.nna.[period].geo.drill.{state}.by_city.{city} = DistributionStats
  // Y6d: ADV drill — views.nna.[period].adv.drill.{architect}.distribution = DistributionStats
  drill?: NNADistributionDrill
}

// Y6b/Y6d: NNA distribution drill-down entries
export interface NNADistributionDrillEntry {
  distribution?: DistributionStats   // ADV: aggregate distribution for architect's relationships
  total?: DistributionStats          // GEO: aggregate distribution for state (mirrors script 09 output)
  relationship_count?: number
  by_city?: Record<string, DistributionStats>
}

// Y6b/Y6d: Keyed by state (geo) or architect (adv)
export interface NNADistributionDrill {
  [segmentKey: string]: NNADistributionDrillEntry
}

export interface NnaPeriodView {
  geo: NnaView
  adv: NnaView
}

// Full Partner Analytics response (v5 - with nested drill-down and time machine)
export interface PartnerAnalyticsResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  firm_name: string

  // Period metadata for time machine
  periods?: PeriodsMetadata

  // Views with period snapshots (new structure)
  // All 4 views are separate top-level views with standard structure
  views: {
    aua: PartnerAnalyticsViewWithPeriods | PartnerAnalyticsView  // AUA by client type
    nna: Record<TimePeriodKey, NnaPeriodView>                    // NNA by cohort (nested geo/adv)
    geo: PartnerAnalyticsViewWithPeriods | PartnerAnalyticsView  // Geographic with city drill-down
    adv: PartnerAnalyticsViewWithPeriods | PartnerAnalyticsView  // Architect with client drill-down
    cla?: Record<TimePeriodKey, { geo: ClaView; adv: ClaView }> // Client Lifecycle Analysis
  }

  timeseries?: RollingTimeseries  // Rolling 12M data for area chart
}

// ----------------------------------------------------------------------------
// Type Guards & Helpers
// ----------------------------------------------------------------------------

// Check if a view has period snapshots (time machine enabled)
export function hasTimeMachine(
  view: PartnerAnalyticsViewWithPeriods | PartnerAnalyticsView
): view is PartnerAnalyticsViewWithPeriods {
  return 'current' in view && typeof view.current === 'object' && 'donut' in view.current
}

// Check if a segment has nested cities (GEO drill-down)
export function hasCities(segment: DonutSegment): segment is DonutSegment & { cities: CitySegment[] } {
  return Array.isArray(segment.cities) && segment.cities.length > 0
}

// Check if a segment has nested clients (ADV drill-down)
export function hasClients(segment: DonutSegment): segment is DonutSegment & { clients: ClientSegment[] } {
  return Array.isArray(segment.clients) && segment.clients.length > 0
}

// Check if a segment has nested flows (NNA drill-down)
export function hasFlows(segment: DonutSegment): segment is DonutSegment & { flows: NnaFlowSegment[] } {
  return Array.isArray(segment.flows) && segment.flows.length > 0
}

// Get current period snapshot from view (handles both v4 and v5 formats)
export function getCurrentSnapshot(
  view: PartnerAnalyticsViewWithPeriods | PartnerAnalyticsView
): PeriodSnapshot | PartnerAnalyticsView {
  if (hasTimeMachine(view)) {
    return view.current
  }
  return view
}

// Get historical period snapshot (returns undefined if not available)
export function getHistoricalSnapshot(
  view: PartnerAnalyticsViewWithPeriods | PartnerAnalyticsView,
  period: 'q1' | 'q2' | 'q3'
): PeriodSnapshot | undefined {
  if (hasTimeMachine(view)) {
    return view[period]
  }
  return undefined
}

// ============================================================================
// Clients Tab Types (Book View & Client Detail)
// ============================================================================

// Client dropdown option
export interface ClientOption {
  key: string
  name: string
  aua: number
}

// Headline section - aggregate metrics
export interface ClientsTabHeadline {
  total_aua: number
  account_count: number
  client_count: number
  fee_rate_pct: number
  income_yield_pct: number
}

// Tax intelligence section
export interface ClientsTabTax {
  taxable: number
  taxable_pct: number
  tax_deferred: number
  tax_deferred_pct: number
  tax_free: number
  tax_free_pct: number
  capital_gains_ttm: number
}

// Income & fees section
export interface ClientsTabIncomeFees {
  dividends_ttm: number
  interest_ttm: number
  total_income_ttm: number
  income_yield_pct: number
  management_fees_ttm: number
  fee_rate_pct: number
}

// Portfolio allocation item
export interface PortfolioAllocationItem {
  name: string
  pct: number
}

// Portfolio composition section
export interface ClientsTabPortfolio {
  allocation: PortfolioAllocationItem[]
  weighted_expense_ratio: number
  unique_holdings: number
  top_5_concentration_pct: number
}

// Engagement metrics section
export interface ClientsTabEngagement {
  trading_buys_ttm: number
  trading_sells_ttm: number
  net_flows_ttm: number
  avg_relationship_years: number
  active_clients_pct: number
}

// Full Clients Tab response (Book view)
export interface ClientsTabResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  headline: ClientsTabHeadline
  tax: ClientsTabTax
  income_fees: ClientsTabIncomeFees
  portfolio: ClientsTabPortfolio
  engagement: ClientsTabEngagement
  clients: ClientOption[]
}

// Individual client detail response
export interface ClientDetailResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  client_key: string
  client_name: string
  headline: ClientsTabHeadline
  tax: ClientsTabTax
  income_fees: ClientsTabIncomeFees
  portfolio: ClientsTabPortfolio
  engagement: ClientsTabEngagement
}

// ============================================================================
// Leaderboard Types (Architect & Implementor Rankings)
// ============================================================================

// Individual leaderboard entry
export interface LeaderboardEntry {
  rank: number
  name: string
  nna: number
  aua_growth_pct: number
  new_clients: number
  total_aua: number
  client_count: number
  account_count: number
}

// Leaderboard summary statistics
export interface LeaderboardSummary {
  total_nna: number
  total_aua: number
  total_new_clients: number
  positive_nna_count: number
  negative_nna_count: number
}

// Leaderboard window data (entries for a specific time period)
export interface LeaderboardWindowData {
  entry_count: number
  summary: LeaderboardSummary
  entries: LeaderboardEntry[]
}

// Full leaderboard response (organized by time windows)
export interface LeaderboardResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  leaderboard_type: 'architect' | 'implementor'
  available_windows: string[]
  windows: Record<string, LeaderboardWindowData | undefined>
}

// Timeseries chart metadata (includes new_clients by window)
export interface TimeseriesChartMetadata {
  new_clients: Record<string, number>
}

// ============================================================================
// Advisor Book Types (Per-Advisor View)
// ============================================================================

// NNA metrics for an advisor
export interface AdvisorNNA {
  ytd: number          // Net New Assets Year-to-Date
  qtd: number          // Quarter-to-Date
  mtd: number          // Month-to-Date
}

// Growth metrics for an advisor
export interface AdvisorGrowth {
  ytd_pct: number      // Growth % Year-to-Date
  qtd_pct: number      // Growth % Quarter-to-Date
}

// Tax exposure breakdown
export interface AdvisorTaxExposure {
  taxable: number
  taxable_pct: number
  tax_deferred: number
  tax_deferred_pct: number
  tax_free: number
  tax_free_pct: number
}

// Income and fees summary
export interface AdvisorIncomeFees {
  income_total_ttm: number
  avg_income_yield_pct: number
  fees_total_ttm: number
  avg_fee_rate_pct: number
}

// Asset allocation item
export interface AssetAllocationItem {
  category: string
  label: string
  pct: number
}

// Portfolio composition
export interface AdvisorPortfolioComposition {
  asset_allocation: AssetAllocationItem[]
  avg_expense_ratio: number
}

// Engagement metrics
export interface AdvisorEngagement {
  net_flows_ttm: number
  inflows_ttm: number
  outflows_ttm: number
  avg_tenure_days: number
}

// Client in advisor's book
export interface AdvisorClient {
  client_key: string
  client_name: string
  aua: number
}

// Full advisor book response
export interface AdvisorBookResponse {
  generated_at: string
  data_as_of: string

  book_type: string              // "architect"
  book_key: string               // "travis_penfield"
  book_name: string              // "Travis Penfield"

  summary: {
    total_aua: number
    client_count: number
    account_count: number
  }

  nna: AdvisorNNA
  growth: AdvisorGrowth
  tax_exposure: AdvisorTaxExposure
  income_fees: AdvisorIncomeFees
  portfolio_composition: AdvisorPortfolioComposition
  engagement: AdvisorEngagement

  clients: AdvisorClient[]
}

// ============================================================================
// Advisor Rolling Flows (Advisors Tab -- NNA Summary + Rolling Time Series)
// ============================================================================

export type NnaPeriodKey = 'mtd' | 'qtd' | 'ytd'

export interface NnaSummarySegment {
  advisor_name: string
  advisor_id: string
  nna: number
  nna_pct: number
  inflows: number
  outflows: number
  total_aua: number
  client_count: number
  new_clients: number
  prior_nna: number
  nna_growth_pct: number
  rank: number
  prior_rank: number
  rank_change: number      // positive = moved up
  color: string
}

export interface NnaPriorPeriod {
  period_start: string
  period_end: string
  display: string
  total_nna: number
}

export interface NnaPeriodSummary {
  period_start: string
  period_end: string
  display: string
  growth_label: string     // 'MoM' | 'QoQ' | 'YoY'
  total_nna: number
  total_inflows: number
  total_outflows: number
  prior: NnaPriorPeriod
  growth_pct: number       // total NNA growth vs prior period
  segments: NnaSummarySegment[]
}

export interface RollingFlowsDataPoint {
  date: string
  nna: number
  inflows: number
  outflows: number
}

export type RollingFlowsWindowKey = '30d' | '90d' | '1Y'

export interface AdvisorRollingSeries {
  advisor_name: string
  advisor_id: string
  series: Record<RollingFlowsWindowKey, RollingFlowsDataPoint[]>
}

export interface AdvisorRollingFlowsResponse {
  generated_at: string
  data_as_of: string
  firm_id: string
  summary: {
    architects: Record<NnaPeriodKey, NnaPeriodSummary>
    implementors: Record<NnaPeriodKey, NnaPeriodSummary>
  }
  architects: AdvisorRollingSeries[]
  implementors: AdvisorRollingSeries[]
}

// ============================================================================
// ADVI-005: Stacked Bar + Rolling 1Y (V2 extension of AdvisorRollingFlowsResponse)
// ============================================================================

// Period keys for stacked bar aggregation (ADVI-005)
export type StackedBarPeriodKey = 'qtd' | 'ytd' | '1y' | '3y' | 'max'

// One advisor's aggregated flows for a stacked bar period
export interface AdvisorBarEntry {
  advisor_name: string
  advisor_id: string
  inflows: number   // positive magnitude
  outflows: number  // positive magnitude — negate client-side for downward bar segment
  nna_net: number   // signed
}

// One advisor's fixed 1Y rolling window daily timeseries
export interface AdvisorRolling1YSeries {
  advisor_name: string
  advisor_id: string
  series: RollingFlowsDataPoint[]  // daily { date, nna, inflows, outflows }; outflows positive magnitude
}

// V2 extends V1 with optional stacked_bar and rolling_1y (additive, backward-compatible)
export interface AdvisorRollingFlowsResponseV2 extends AdvisorRollingFlowsResponse {
  stacked_bar?: Record<StackedBarPeriodKey, {
    architects: AdvisorBarEntry[]
    implementors: AdvisorBarEntry[]
  }>
  rolling_1y?: {
    architects: AdvisorRolling1YSeries[]
    implementors: AdvisorRolling1YSeries[]
  }
  // Y13: Monthly granularity stacked bar — { "YYYY-MM": AdvisorBarEntry[] }
  monthly?: Record<string, AdvisorBarEntry[]>
}

// ============================================================================
// Y5: Growth Decomposition (timeseries_chart.json)
// ============================================================================

export interface GrowthDecompositionPoint {
  period: string   // "YYYY-MM" monthly
  market: number   // AUA change attributable to market appreciation
  nna: number      // net new assets for the period
  total: number    // market + nna = total AUA change
}

export interface GrowthDecompositionView {
  description: string
  data: GrowthDecompositionPoint[]
}

// ============================================================================
// Y9: NNA Series with Inflows/Outflows (timeseries_chart.json)
// ============================================================================

export interface NNASeriesPoint {
  date: string
  [key: string]: number | string  // category, category_inflow, category_outflow
}

export interface NNASeriesView {
  description: string
  categories: string[]
  data: NNASeriesPoint[]
}

export interface NNAGeoDrillView {
  [stateKey: string]: {
    categories: string[]
    data: NNASeriesPoint[]
  }
}

// ============================================================================
// Y3: AUA Asset Class Mix (timeseries_chart.json)
// ============================================================================

export interface AuaMixSegment {
  label: string   // "Equities", "Fixed Income", "Real Estate", "Alternatives", "Cash", "Other"
  value: number
}

export interface AuaMixPoint {
  period: string  // "YYYY-MM"
  segments: AuaMixSegment[]
}

export interface AuaMixView {
  description?: string
  categories?: string[]
  data: AuaMixPoint[]
}

// ============================================================================
// Y15: Books Tab L2/L3/L4 Types (from ADVI-006 design brief Section 6)
// ============================================================================

// L3: Client detail from bd-portal-advisor-publisher -> build_client_details()
// Note: Named BooksClientDetailResponse to avoid collision with existing ClientDetailResponse
// which serves the legacy clients_tab.json shape.
export interface BooksClientDetailResponse {
  data_as_of: string
  headline: {
    total_aua: number
    account_count: number
  }
  tax: BooksClientTaxDetail
  engagement: {
    net_flows_ttm: number
    avg_relationship_years: number
  }
  accounts: BooksClientAccount[]
}

export interface BooksClientAccount {
  account_id: string
  tax_status: string
  total_aua: number
  cum_inflows: number
  cum_outflows: number
  nna: number
  num_positions: number
}

export interface BooksClientTaxDetail {
  taxable: number
  taxable_pct: number
  tax_deferred: number
  tax_deferred_pct: number
  tax_free: number
  tax_free_pct: number
  qualified_aua: number
  qualified_pct: number
  non_qualified_aua: number
  non_qualified_pct: number
  qualified_account_count?: number
  non_qualified_account_count?: number
  cost_basis_by_year: CostBasisYear[]
  top_gain_positions: GainPosition[]
  open_lots: OpenLot[]
  open_lots_count: number
}

export interface CostBasisYear {
  year: number
  cost_basis: number
  market_value: number
  unrealized_gain: number
}

export interface GainPosition {
  asset_name: string
  ticker?: string
  unrealized_gain: number
  cost_basis: number
  market_value: number
  term: string
}

export interface OpenLot {
  account_id: string
  asset_name: string
  ticker?: string
  quantity: number
  cost_basis: number
  market_value: number
  unrealized_gain: number
  term: string
  acquisition_date?: string
}
```

### api-endpoint-fetches-partneranalyticsheadermetricssuffix.json.ts

```
/**
 * Advisor Intelligence API Client - v2
 *
 * Multi-tenant API for Advisor Intelligence page data.
 * Data access controlled by allowedFirmIds computed in portal-authorizer.
 *
 * Endpoints:
 *   GET /api/partners                                              - List partners
 *   GET /api/scoped/advisor-intelligence/timeseries/{dimension}    - Time series
 *   GET /api/scoped/advisor-intelligence/snapshots/{dimension}     - AUA snapshots
 *   GET /api/scoped/advisor-intelligence/filters                   - Filter options
 *   GET /api/scoped/advisor-intelligence/clients/growth            - Client growth
 *   GET /api/scoped/advisor-intelligence/clients/tax-breakdown     - Tax breakdown
 *   GET /api/scoped/advisor-intelligence/clients/tax-deferred      - Tax candidates
 */

import type {
  PartnersResponse,
  TimeSeriesResponse,
  CategoryTimeSeriesResponse,
  SnapshotResponse,
  FiltersResponse,
  ClientGrowthResponse,
  TaxBasisBreakdownResponse,
  TaxDeferredResponse,
  HeaderSummary,
  HeaderMetricsResponse,
  PartnerAnalyticsResponse,
  CumulativeChartResponse,
  ClientsTabResponse,
  ClientDetailResponse,
  LeaderboardResponse,
  AdvisorBookResponse,
  AdvisorRollingFlowsResponse,
  BooksClientDetailResponse,
} from '@/pages/AdvisorIntelligence/types'

// ============================================================================
// Configuration
// ============================================================================

// API base URL
const API_BASE_URL = import.meta.env.VITE_PORTAL_API_URL ?? ''

// Valid dimensions for time series (11 total)
export const TIMESERIES_DIMENSIONS = [
  'total',
  'category',
  'architect',
  'region',
  'account_type',
  'tax_status',
  'client_segment',
  'state',
  'city',
  'relationship',
  'implementor',
] as const

// Valid dimensions for snapshots (7 total)
export const SNAPSHOT_DIMENSIONS = [
  'architect',
  'region',
  'tax_status',
  'account_type',
  'implementor',
  'state',
  'city',
] as const

export type TimeseriesDimension = typeof TIMESERIES_DIMENSIONS[number]
export type SnapshotDimension = typeof SNAPSHOT_DIMENSIONS[number]

// Combined for backward compatibility
export const VALID_DIMENSIONS = TIMESERIES_DIMENSIONS
export type Dimension = TimeseriesDimension

// ============================================================================
// API Request Helper
// ============================================================================

/**
 * Make authenticated API request
 */
async function apiRequest<T>(endpoint: string): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`
  const accessToken = localStorage.getItem('accessToken')

  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...(accessToken && { 'Authorization': `Bearer ${accessToken}` }),
    },
  })

  if (!response.ok) {
    const errorBody = await response.text()
    throw new Error(`API request failed: ${response.status} ${response.statusText} - ${errorBody}`)
  }

  return response.json()
}

// ============================================================================
// API Functions
// ============================================================================

/**
 * Get list of partners the user can access
 */
export async function getAllowedPartners(): Promise<PartnersResponse> {
  return await apiRequest<PartnersResponse>('/api/partners')
}

/**
 * Get time series data for a dimension
 *
 * @param firmId - Partner firm ID
 * @param dimension - Dimension to slice by (total, category, architect, region, account_type, tax_status, client_segment, state, city, relationship, implementor)
 */
export async function getTimeSeries(
  firmId: string,
  dimension: TimeseriesDimension
): Promise<TimeSeriesResponse | CategoryTimeSeriesResponse> {
  const url = `/api/scoped/advisor-intelligence/timeseries/${dimension}?firmId=${firmId}`
  return await apiRequest<TimeSeriesResponse>(url)
}

/**
 * Get AUA snapshot for a dimension
 *
 * Routes to opal-partners-data Lambda via API Gateway.
 * firmId is passed as query param; will be removed once Lambda reads from
 * portal-authorizer context (authorizer.lambda.firmId) instead.
 *
 * @param firmId - Partner firm ID
 * @param dimension - Dimension to slice by (architect, region, tax_status, account_type, implementor, state, city)
 */
export async function getSnapshot(
  firmId: string,
  dimension: SnapshotDimension
): Promise<SnapshotResponse> {
  const url = `/api/scoped/advisor-intelligence/snapshots/${dimension}?firmId=${firmId}`
  return await apiRequest<SnapshotResponse>(url)
}

/**
 * Get available filter dimensions and values
 *
 * @param firmId - Partner firm ID
 */
export async function getFilters(firmId: string): Promise<FiltersResponse> {
  const url = `/api/scoped/advisor-intelligence/filters?firmId=${firmId}`
  return await apiRequest<FiltersResponse>(url)
}

/**
 * Get client growth time series
 *
 * @param firmId - Partner firm ID
 */
export async function getClientGrowth(firmId: string): Promise<ClientGrowthResponse> {
  const url = `/api/scoped/advisor-intelligence/clients/growth?firmId=${firmId}`
  return await apiRequest<ClientGrowthResponse>(url)
}

/**
 * Get tax basis breakdown (pie charts)
 *
 * @param firmId - Partner firm ID
 */
export async function getTaxBreakdown(firmId: string): Promise<TaxBasisBreakdownResponse> {
  const url = `/api/scoped/advisor-intelligence/clients/tax-breakdown?firmId=${firmId}`
  return await apiRequest<TaxBasisBreakdownResponse>(url)
}

/**
 * Get tax-deferred strategy candidates
 *
 * @param firmId - Partner firm ID
 */
export async function getTaxDeferredCandidates(firmId: string): Promise<TaxDeferredResponse> {
  const url = `/api/scoped/advisor-intelligence/clients/tax-deferred?firmId=${firmId}`
  return await apiRequest<TaxDeferredResponse>(url)
}

/**
 * Get header summary metrics
 *
 * Static JSON served via CloudFront -> S3 (shared-advisor-router handles firm routing)
 */
export async function getHeaderSummary(): Promise<HeaderSummary> {
  return await apiRequest<HeaderSummary>('/api/scoped/advisor-intelligence/summary/header_metrics.json')
}

/**
 * Get full header metrics (v3 - includes radial chart and bell curve data)
 *
 * Returns the complete header_metrics.json structure including:
 * - total: AUA, NNA metrics, quarterly breakdowns
 * - radial_12m: NMNC/NMEC/Existing breakdown for donut chart
 * - account_distribution: histogram and percentiles for bell curve
 * - by_architect: top 10 architects breakdown
 *
 * Static JSON served via CloudFront -> S3 (shared-advisor-router handles firm routing)
 */
export async function getHeaderMetrics(): Promise<HeaderMetricsResponse> {
  return await apiRequest<HeaderMetricsResponse>('/api/scoped/advisor-intelligence/summary/header_metrics.json')
}

/**
 * Get Partner Analytics data (v4 - multi-view with NNA/GEO/ADV)
 *
 * Returns the complete partner_analytics/header_metrics.json structure including:
 * - views.nna: Client segment breakdown (NMNC/NMEC/Existing)
 * - views.geo: Geographic breakdown (top 8 regions + Other)
 * - views.adv: Architect breakdown (top 8 architects + Other)
 *
 * Each view contains:
 * - donut: { title, total, segments[] }
 * - distribution: { total, by_segment }
 * - metrics: { aua, nna_ytd, q0, q1, q2 }
 *
 * Static JSON served via CloudFront -> S3 (shared-advisor-router handles firm routing)
 */
export async function getPartnerAnalytics(granularity: 'monthly' | 'quarterly' | 'annually' = 'quarterly'): Promise<PartnerAnalyticsResponse> {
  // S3 files use _annual (not _annually) — map the suffix
  const suffix = granularity === 'annually' ? 'annual' : granularity
  return await apiRequest<PartnerAnalyticsResponse>(`/api/scoped/advisor-intelligence/partner_analytics/header_metrics_${suffix}.json`)
}

/**
 * Get cumulative time series chart data
 *
 * Returns daily cumulative NNA data for 4 views:
 * - aua: Cumulative NNA by client cohort (NMNC/NMEC)
 * - nna: Daily NNA flows
 * - geo: Cumulative NNA by region (TX, CA, etc.)
 * - adv: Cumulative NNA by architect
 *
 * Data spans 2 years with daily granularity (~731 data points per view)
 */
export async function getCumulativeChart(): Promise<CumulativeChartResponse> {
  return await apiRequest<CumulativeChartResponse>('/api/scoped/advisor-intelligence/timeseries_chart.json')
}

/**
 * Get Clients Tab data (Book view)
 *
 * Returns aggregate book-level metrics for the Clients tab:
 * - headline: Total AUA, accounts, clients, fee rate, income yield
 * - tax: Tax status breakdown (taxable/deferred/free) + capital gains
 * - income_fees: Dividends, interest, fees with TTM totals
 * - portfolio: Allocation, expense ratio, holdings, concentration
 * - engagement: Trading activity, net flows, tenure, active %
 * - clients: Full dropdown list sorted by AUA (for client picker)
 */
export async function getClientsTab(): Promise<ClientsTabResponse> {
  return await apiRequest<ClientsTabResponse>('/api/scoped/advisor-intelligence/clients_tab.json')
}

/**
 * Get individual client detail data
 *
 * Returns metrics for a specific client:
 * - Same structure as ClientsTab but scoped to one client
 * - headline, tax, income_fees, portfolio, engagement sections
 *
 * @param clientKey - The client identifier (e.g., "z08327149")
 */
export async function getClientDetail(clientKey: string): Promise<ClientDetailResponse> {
  return await apiRequest<ClientDetailResponse>(`/api/scoped/advisor-intelligence/clients/${clientKey}.json`)
}

/**
 * Get Architect Leaderboard data
 *
 * Returns ranked list of architects by NNA (trailing 12M):
 * - entries: Ranked architect data with NNA, AUA growth %, new clients
 * - summary: Aggregate totals (total_nna, total_aua, positive/negative counts)
 */
export async function getArchitectLeaderboard(): Promise<LeaderboardResponse> {
  return await apiRequest<LeaderboardResponse>('/api/scoped/advisor-intelligence/architect_leaderboard.json')
}

/**
 * Get Implementor Leaderboard data
 *
 * Returns ranked list of implementors by NNA (trailing 12M):
 * - entries: Ranked implementor data with NNA, AUA growth %, new clients
 * - summary: Aggregate totals (total_nna, total_aua, positive/negative counts)
 */
export async function getImplementorLeaderboard(): Promise<LeaderboardResponse> {
  return await apiRequest<LeaderboardResponse>('/api/scoped/advisor-intelligence/implementor_leaderboard.json')
}

/**
 * Get Advisor Book data (per-advisor view)
 *
 * Returns book-level metrics for a specific advisor:
 * - summary: AUA, client count, account count
 * - nna: YTD, QTD, MTD net new assets
 * - growth: YTD and QTD growth percentages
 * - tax_exposure, income_fees, portfolio_composition, engagement
 * - clients: List of clients for this advisor
 *
 * Static JSON served via CloudFront -> S3 (shared-advisor-router handles firm routing)
 *
 * @param advisorId - Advisor identifier (e.g., 'travis_penfield')
 */
export async function getAdvisorBook(advisorId: string): Promise<AdvisorBookResponse> {
  return await apiRequest<AdvisorBookResponse>(`/api/scoped/advisor-intelligence/advisors/${advisorId}/book.json`)
}

/**
 * Get Advisor Rolling Flows data (Advisors tab -- two views)
 *
 * Returns both NNA summary (donut chart) and rolling time series:
 * - summary.architects / summary.implementors: MTD/QTD/YTD NNA breakdown by advisor
 * - architects[] / implementors[]: daily rolling 30d/90d/1Y flows per advisor
 *
 * Static JSON served via CloudFront -> S3 (opal-data-portal-v2 bucket)
 */
export async function getAdvisorRollingFlows(): Promise<AdvisorRollingFlowsResponse> {
  return await apiRequest<AdvisorRollingFlowsResponse>('/api/scoped/advisor-intelligence/advisor_rolling_flows.json')
}

/**
 * Get Books client detail data (per-relationship view from bd-portal-advisor-publisher)
 *
 * Returns relationship-level detail for the Books tab L3 view:
 * - headline: Total AUA, account count
 * - tax: Full tax intelligence with open lots, cost basis by year, top positions
 * - engagement: Net flows TTM, avg relationship years
 * - accounts: Per-account breakdown with flows and position counts
 *
 * Static JSON served via CloudFront -> S3 (shared-advisor-router handles firm routing)
 *
 * @param clientKey - Relationship identifier (e.g., "z08327149")
 */
export async function getBooksClientDetail(clientKey: string): Promise<BooksClientDetailResponse> {
  return await apiRequest<BooksClientDetailResponse>(`/api/scoped/advisor-intelligence/clients/${clientKey}.json`)
}
```

### bd-gold-layer-lambda-step-3-generatesnapshots----different-from-script-09.py

```
"""
BD Gold Layer Lambda

Generates all gold layer JSON files after bd-merge-daily updates the silver parquet.
Invoked by bd-merge-daily Lambda after successful merge.

Runs the equivalent of:
1. 01_build_canonical_timeline.py → silver/bd_canonical_timeline.parquet
2. 02_generate_timeseries.py      → gold/timeseries/*.json (11 files)
3. 03_generate_snapshots.py       → gold/snapshots/*.json (7 files)
4. 04_generate_clients.py         → gold/clients/*.json (3 files)
5. 05_generate_filters.py         → gold/filters/dimensions.json
6. 06_generate_summary.py         → gold/summary/header_metrics.json

Total output: 23 files (1 parquet + 22 JSON)
"""

import boto3
import json
import os
from datetime import datetime, timezone, timedelta
from io import BytesIO
import traceback

import pandas as pd
import numpy as np

try:
    from dateutil.relativedelta import relativedelta
except ImportError:
    # Fallback if dateutil not available
    def relativedelta(months=0):
        return timedelta(days=months * 30)

# Configuration
S3_BUCKET = os.environ.get('S3_BUCKET', 'opal-data-bd')
FIRM_ID = '49financial'
FIRM_NAME = '49 Financial'

# Invalid relationship_id values that require fallback to account_id
INVALID_REL_IDS = {'', '0', 'nan', 'None', 'No Relationship'}

s3 = boto3.client('s3')


def lambda_handler(event, context):
    """
    Main Lambda handler - generate all gold layer files.
    """
    print(f"BD Gold Layer invoked at {datetime.now(timezone.utc).isoformat()}")
    print(f"Event: {json.dumps(event)}")

    try:
        # Load silver data
        print("\n=== Loading Silver Data ===")
        txns = load_parquet('silver/bd_transactions.parquet')
        print(f"Loaded {len(txns):,} transactions")

        accounts = load_parquet('silver/bd_accounts.parquet')
        print(f"Loaded {len(accounts):,} accounts")

        # Ensure trade_date is datetime
        txns['trade_date'] = pd.to_datetime(txns['trade_date'])

        # Step 1: Build canonical timeline
        print("\n=== Step 1: Building Canonical Timeline ===")
        timeline = build_canonical_timeline(txns)
        save_parquet(timeline, 'silver/bd_canonical_timeline.parquet')

        # Step 2: Generate timeseries
        print("\n=== Step 2: Generating Timeseries ===")
        generate_timeseries(txns, timeline)

        # Step 3: Generate snapshots
        print("\n=== Step 3: Generating Snapshots ===")
        generate_snapshots(accounts)

        # Step 4: Generate clients
        print("\n=== Step 4: Generating Clients ===")
        generate_clients(accounts, txns)

        # Step 5: Generate filters
        print("\n=== Step 5: Generating Filters ===")
        generate_filters(accounts)

        # Step 6: Generate summary
        print("\n=== Step 6: Generating Summary ===")
        generate_summary(accounts, txns)

        print("\n=== Gold Layer Generation Complete ===")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Gold layer generation complete',
                'generated_at': datetime.now(timezone.utc).isoformat(),
                'files_generated': 23
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
        raise


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_client_key(row) -> str:
    """Generate client_key matching the canonical timeline format."""
    rel_id = str(row.get('relationship_id', '')).strip()
    if rel_id in INVALID_REL_IDS:
        return f"acct_{row['account_id']}"
    return f"rel_{rel_id}"


def get_display_name(row) -> str:
    """Get display name for a client (relationship_name with fallbacks)."""
    rel_name = str(row.get('relationship_name', '')).strip()
    if rel_name not in INVALID_REL_IDS and rel_name:
        return rel_name

    client_name = str(row.get('client_name', '')).strip()
    if client_name and client_name not in ('nan', 'None', ''):
        return client_name

    return f"Account {row.get('account_id', 'Unknown')}"


def add_client_key(df: pd.DataFrame) -> pd.DataFrame:
    """Add client_key and display_name columns to dataframe."""
    df = df.copy()
    df['client_key'] = df.apply(get_client_key, axis=1)
    df['display_name'] = df.apply(get_display_name, axis=1)
    return df


def load_parquet(key: str) -> pd.DataFrame:
    """Load parquet from S3."""
    try:
        response = s3.get_object(Bucket=S3_BUCKET, Key=key)
        return pd.read_parquet(BytesIO(response['Body'].read()))
    except s3.exceptions.NoSuchKey:
        print(f"File not found: s3://{S3_BUCKET}/{key}")
        return pd.DataFrame()


def save_parquet(df: pd.DataFrame, key: str):
    """Save DataFrame to S3 as parquet."""
    buffer = BytesIO()
    df.to_parquet(buffer, index=False, compression='snappy')
    buffer.seek(0)

    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=buffer.getvalue())
    size_kb = len(buffer.getvalue()) / 1024
    print(f"  Saved: s3://{S3_BUCKET}/{key} ({size_kb:.1f} KB)")


def save_json(data: dict, key: str):
    """Save dict to S3 as JSON."""
    json_str = json.dumps(data, indent=2, default=str)
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json_str.encode('utf-8'),
        ContentType='application/json'
    )
    print(f"  Saved: s3://{S3_BUCKET}/{key} ({len(json_str):,} bytes)")


# =============================================================================
# STEP 1: CANONICAL TIMELINE
# =============================================================================

def build_canonical_timeline(df: pd.DataFrame) -> pd.DataFrame:
    """Build canonical timeline tracking first-seen date for each client."""
    df = df.sort_values('trade_date').copy()
    df['client_key'] = df.apply(get_client_key, axis=1)

    first_txns = df.groupby('client_key').agg({
        'trade_date': 'min',
        'account_id': 'first',
        'architect': 'first',
        'relationship_id': 'first',
        'relationship_name': 'first',
        'client_name': 'first',
    }).reset_index()

    first_txns.columns = [
        'client_key', 'first_seen_date', 'first_account_id',
        'first_architect', 'relationship_id', 'relationship_name', 'client_name'
    ]

    # Get account counts
    account_counts = df.groupby('client_key')['account_id'].nunique().reset_index()
    account_counts.columns = ['client_key', 'total_accounts']
    first_txns = first_txns.merge(account_counts, on='client_key', how='left')

    first_txns['last_updated'] = datetime.now(timezone.utc).isoformat()
    first_txns['first_architect'] = first_txns['first_architect'].replace(
        'No Architect Value Assigned', 'House'
    )

    print(f"  Timeline records: {len(first_txns):,}")
    return first_txns


# =============================================================================
# STEP 2: TIMESERIES
# =============================================================================

def generate_timeseries(df: pd.DataFrame, timeline: pd.DataFrame):
    """Generate all timeseries JSON files."""
    df = df.copy()

    # Add period column
    df['period'] = df['trade_date'].dt.to_period('M').astype(str)

    # Identify NNA transactions
    NNA_INFLOW_TYPES = ['Cash Deposit', 'Transfer In', 'Wire In', 'Transfer']
    NNA_OUTFLOW_TYPES = ['Cash Withdrawal', 'Transfer Out', 'Wire Out']

    df['is_nna_inflow'] = (
        df['transaction_type'].isin(NNA_INFLOW_TYPES) |
        df['action'].str.contains('Deposit|Transfer In|Wire In', case=False, na=False)
    )
    df['is_nna_outflow'] = (
        df['transaction_type'].isin(NNA_OUTFLOW_TYPES) |
        df['action'].str.contains('Withdrawal|Transfer Out|Wire Out', case=False, na=False)
    )

    # Merge timeline to get is_new_client
    df['client_key'] = df.apply(get_client_key, axis=1)
    df = df.merge(
        timeline[['client_key', 'first_seen_date']],
        on='client_key',
        how='left'
    )
    df['first_seen_date'] = pd.to_datetime(df['first_seen_date'])
    df['is_new_client'] = df['trade_date'].dt.date == df['first_seen_date'].dt.date

    print(f"  NNA inflows: {df['is_nna_inflow'].sum():,}")
    print(f"  New client txns: {df['is_new_client'].sum():,}")

    # Generate total timeseries
    total_ts = generate_total_timeseries(df)
    save_json(total_ts, 'gold/timeseries/nna_total.json')

    # Generate category timeseries
    cat_ts = generate_category_timeseries(df)
    save_json(cat_ts, 'gold/timeseries/nna_by_category.json')

    # Generate dimension timeseries
    dimensions = {
        'architect': {'column': 'architect', 'transform': {'No Architect Value Assigned': 'House'}, 'top_n': None},
        'region': {'column': 'local_ops', 'transform': {'No Local Ops Value Assigned': 'Unassigned'}, 'top_n': None},
        'implementor': {'column': 'implementor', 'transform': {'No Implementor Value Assigned': 'Unassigned'}, 'top_n': 50},
        'account_type': {'column': 'account_owner_type', 'transform': {}, 'top_n': None},
        'tax_status': {'column': 'tax_status', 'transform': {}, 'top_n': None},
        'client_segment': {'column': 'is_new_client', 'transform': {True: 'New Client', False: 'Existing Client', 1: 'New Client', 0: 'Existing Client'}, 'top_n': None},
        'state': {'column': 'client_state', 'transform': {}, 'top_n': 49},
        'city': {'column': 'client_city', 'transform': {}, 'top_n': 50},
        'relationship': {'column': 'relationship_name', 'transform': {'No Relationship': 'Unassigned'}, 'top_n': 100},
    }

    for dim_name, config in dimensions.items():
        dim_ts = generate_dimension_timeseries(df, dim_name, config)
        if dim_ts:
            save_json(dim_ts, f'gold/timeseries/nna_by_{dim_name}.json')


def generate_total_timeseries(df: pd.DataFrame) -> dict:
    """Generate aggregate NNA timeseries."""
    nna = df[df['is_nna_inflow'] | df['is_nna_outflow']].copy()

    agg = nna.groupby('period').agg(
        inflow=('market_value', lambda x: x[nna.loc[x.index, 'is_nna_inflow']].sum()),
        outflow=('market_value', lambda x: x[nna.loc[x.index, 'is_nna_outflow']].sum()),
        txn_count=('transaction_id', 'count'),
    ).reset_index()

    agg['net'] = agg['inflow'] - agg['outflow']

    data = [
        {
            'period': row['period'],
            'inflow': float(row['inflow']),
            'outflow': float(row['outflow']),
            'net': float(row['net']),
            'txn_count': int(row['txn_count']),
        }
        for _, row in agg.iterrows()
    ]

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of': df['trade_date'].max().strftime('%Y-%m-%d'),
        'firm_id': FIRM_ID,
        'granularity': 'monthly',
        'data': sorted(data, key=lambda x: x['period']),
    }


def generate_category_timeseries(df: pd.DataFrame) -> dict:
    """Generate NNA timeseries by category (NMNC/NMEC)."""
    nna = df[df['is_nna_inflow']].copy()

    nna['category'] = nna['is_new_client'].map({
        True: 'NMNC', 1: 'NMNC',
        False: 'NMEC', 0: 'NMEC'
    }).fillna('NMEC')

    agg = nna.groupby(['period', 'category']).agg(
        value=('market_value', 'sum'),
        txn_count=('transaction_id', 'count'),
    ).reset_index()

    pivot = agg.pivot(index='period', columns='category', values='value').fillna(0)

    data = []
    for period in pivot.index:
        row = {'period': period}
        for cat in pivot.columns:
            row[cat.lower()] = float(pivot.loc[period, cat])
        row['total'] = sum(v for k, v in row.items() if k != 'period')
        data.append(row)

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of': df['trade_date'].max().strftime('%Y-%m-%d'),
        'firm_id': FIRM_ID,
        'granularity': 'monthly',
        'categories': ['nmnc', 'nmec'],
        'data': sorted(data, key=lambda x: x['period']),
    }


def generate_dimension_timeseries(df: pd.DataFrame, dim_name: str, config: dict) -> dict:
    """
    Generate NNA timeseries for a specific dimension.

    Output format (Recharts-compatible):
    {
        "dimension_values": ["House", "Travis Penfield", ...],
        "data": [
            {
                "period": "2021-01",
                "House": {"nmnc": 500000, "nmec": 6400000, "nna_net": 6920831, "outflow": 0, "txn_count": 349},
                "Travis Penfield": {"nmnc": 0, "nmec": 0, "nna_net": 0, "outflow": 0, "txn_count": 0}
            }
        ]
    }

    Key features:
    - Filters out empty/null dimension values
    - Includes NMNC (new money new client) and NMEC (new money existing client) breakdown
    - Pads sparse data so every dimension appears in every period (with zeros if no activity)
    """
    column = config['column']
    transform = config['transform']
    top_n = config['top_n']

    # Get both inflows and outflows for net calculation
    nna_inflow = df[df['is_nna_inflow']].copy()
    nna_outflow = df[df['is_nna_outflow']].copy()

    if column not in df.columns:
        print(f"  Skipping {dim_name}: column {column} not found")
        return None

    # Apply dimension value transformation
    nna_inflow['dim_value'] = nna_inflow[column].astype(str).replace(transform)
    nna_outflow['dim_value'] = nna_outflow[column].astype(str).replace(transform)

    # Filter out empty/null dimension values
    invalid_values = {'', 'nan', 'None', 'NaN', 'null'}
    nna_inflow = nna_inflow[~nna_inflow['dim_value'].isin(invalid_values)]
    nna_inflow = nna_inflow[nna_inflow['dim_value'].str.strip() != '']
    nna_outflow = nna_outflow[~nna_outflow['dim_value'].isin(invalid_values)]
    nna_outflow = nna_outflow[nna_outflow['dim_value'].str.strip() != '']

    # Get top N values by total inflow if specified
    if top_n:
        top_values = nna_inflow.groupby('dim_value')['market_value'].sum().nlargest(top_n).index.tolist()
        nna_inflow = nna_inflow[nna_inflow['dim_value'].isin(top_values)]
        nna_outflow = nna_outflow[nna_outflow['dim_value'].isin(top_values)]

    # Aggregate inflows with NMNC/NMEC breakdown (memory-efficient)
    # Add separate columns for NMNC and NMEC values
    nna_inflow['nmnc_value'] = nna_inflow['market_value'].where(nna_inflow['is_new_client'] == True, 0)
    nna_inflow['nmec_value'] = nna_inflow['market_value'].where(nna_inflow['is_new_client'] == False, 0)

    inflow_agg = nna_inflow.groupby(['period', 'dim_value']).agg(
        nmnc=('nmnc_value', 'sum'),
        nmec=('nmec_value', 'sum'),
        inflow_txn_count=('transaction_id', 'count'),
    ).reset_index()

    # Aggregate outflows
    outflow_agg = nna_outflow.groupby(['period', 'dim_value']).agg(
        outflow=('market_value', 'sum'),
        outflow_txn_count=('transaction_id', 'count'),
    ).reset_index()

    # Merge inflows and outflows
    agg = inflow_agg.merge(outflow_agg, on=['period', 'dim_value'], how='outer').fillna(0)

    # Calculate net NNA
    agg['nna_net'] = agg['nmnc'] + agg['nmec'] - agg['outflow']
    agg['txn_count'] = agg['inflow_txn_count'] + agg['outflow_txn_count']

    # Get all unique dimension values and periods
    dim_values = sorted(agg['dim_value'].unique().tolist())
    all_periods = sorted(agg['period'].unique().tolist())

    # Build data array with padding (every dimension in every period)
    data = []
    for period in all_periods:
        period_data = {'period': period}
        period_rows = agg[agg['period'] == period].set_index('dim_value')

        for dim_val in dim_values:
            if dim_val in period_rows.index:
                row = period_rows.loc[dim_val]
                period_data[dim_val] = {
                    'nmnc': float(row['nmnc']),
                    'nmec': float(row['nmec']),
                    'nna_net': float(row['nna_net']),
                    'outflow': float(row['outflow']),
                    'txn_count': int(row['txn_count']),
                }
            else:
                # Pad with zeros for dimensions with no activity this period
                period_data[dim_val] = {
                    'nmnc': 0.0,
                    'nmec': 0.0,
                    'nna_net': 0.0,
                    'outflow': 0.0,
                    'txn_count': 0,
                }

        data.append(period_data)

    print(f"  nna_by_{dim_name}.json: {len(dim_values)} values, {len(all_periods)} periods (padded)")

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of': df['trade_date'].max().strftime('%Y-%m-%d'),
        'firm_id': FIRM_ID,
        'granularity': 'monthly',
        'dimension': dim_name,
        'dimension_values': dim_values,
        'data': data,
    }


# =============================================================================
# STEP 3: SNAPSHOTS
# =============================================================================

def generate_snapshots(accounts: pd.DataFrame):
    """Generate all snapshot JSON files."""
    accounts = add_client_key(accounts)

    dimensions = {
        'architect': {'column': 'architect', 'transform': {'No Architect Value Assigned': 'House'}, 'top_n': None},
        'region': {'column': 'local_ops', 'transform': {'No Local Ops Value Assigned': 'Unassigned'}, 'top_n': None},
        'account_type': {'column': 'account_owner_type', 'transform': {}, 'top_n': None},
        'tax_status': {'column': 'tax_status', 'transform': {}, 'top_n': None},
        'state': {'column': 'client_state', 'transform': {}, 'top_n': 49},
        'city': {'column': 'client_city', 'transform': {}, 'top_n': 50},
        'relationship': {'column': 'display_name', 'transform': {}, 'top_n': 100},
    }

    for dim_name, config in dimensions.items():
        snapshot = generate_snapshot(accounts, dim_name, config)
        if snapshot:
            save_json(snapshot, f'gold/snapshots/aua_by_{dim_name}.json')


def generate_snapshot(df: pd.DataFrame, dim_name: str, config: dict) -> dict:
    """Generate AUA snapshot for a specific dimension."""
    column = config['column']
    transform = config['transform']
    top_n = config['top_n']

    if column not in df.columns:
        print(f"  Skipping {dim_name}: column {column} not found")
        return None

    df = df.copy()
    df['dim_value'] = df[column].astype(str).replace(transform)
    df = df[df['dim_value'].notna() & (df['dim_value'] != '') & (df['dim_value'] != 'nan')]

    agg = df.groupby('dim_value').agg(
        aua=('emv', 'sum'),
        client_count=('client_key', 'nunique'),
        account_count=('account_id', 'nunique'),
    ).reset_index()

    agg = agg.sort_values('aua', ascending=False)

    if top_n:
        agg = agg.head(top_n)

    total_aua = agg['aua'].sum()
    agg['aua_pct'] = (agg['aua'] / total_aua * 100).round(1)

    data = [
        {
            'value': row['dim_value'],
            'aua': float(row['aua']),
            'aua_pct': float(row['aua_pct']),
            'client_count': int(row['client_count']),
            'account_count': int(row['account_count']),
        }
        for _, row in agg.iterrows()
    ]

    print(f"  aua_by_{dim_name}.json: {len(data)} values")

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        'firm_id': FIRM_ID,
        'dimension': dim_name,
        'total_aua': float(total_aua),
        'data': data,
    }


# =============================================================================
# STEP 4: CLIENTS
# =============================================================================

def generate_clients(accounts: pd.DataFrame, txns: pd.DataFrame):
    """Generate all client JSON files."""
    accounts = add_client_key(accounts)
    txns = add_client_key(txns)
    txns['trade_date'] = pd.to_datetime(txns['trade_date'])
    txns['period'] = txns['trade_date'].dt.to_period('M').astype(str)

    # Growth timeseries
    growth = generate_growth_timeseries(accounts, txns)
    save_json(growth, 'gold/clients/growth_timeseries.json')

    # Tax breakdown
    tax_breakdown = generate_tax_breakdown(accounts)
    save_json(tax_breakdown, 'gold/clients/tax_basis_breakdown.json')

    # Tax deferred candidates
    candidates = generate_tax_deferred_candidates(accounts, txns)
    save_json(candidates, 'gold/clients/tax_deferred_candidates.json')


def generate_growth_timeseries(accounts: pd.DataFrame, txns: pd.DataFrame) -> dict:
    """Generate client growth timeseries."""
    client_by_period = txns.groupby('period')['client_key'].nunique().reset_index()
    client_by_period.columns = ['period', 'active_clients']

    first_seen = txns.groupby('client_key')['trade_date'].min().reset_index()
    first_seen['period'] = first_seen['trade_date'].dt.to_period('M').astype(str)
    new_clients = first_seen.groupby('period').size().reset_index(name='new_clients')

    growth = client_by_period.merge(new_clients, on='period', how='left').fillna(0)
    growth = growth.sort_values('period')
    growth['cumulative_clients'] = growth['new_clients'].cumsum()

    total_aua = accounts['emv'].sum()
    total_clients = accounts['client_key'].nunique()

    data = [
        {
            'period': row['period'],
            'new_clients': int(row['new_clients']),
            'cumulative_clients': int(row['cumulative_clients']),
            'active_clients': int(row['active_clients']),
        }
        for _, row in growth.iterrows()
    ]

    print(f"  growth_timeseries.json: {len(data)} periods")

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of': txns['trade_date'].max().strftime('%Y-%m-%d'),
        'firm_id': FIRM_ID,
        'granularity': 'monthly',
        'summary': {
            'total_clients': int(total_clients),
            'total_aua': float(total_aua),
            'avg_aua_per_client': float(total_aua / total_clients) if total_clients > 0 else 0,
        },
        'data': sorted(data, key=lambda x: x['period']),
    }


def generate_tax_breakdown(accounts: pd.DataFrame) -> dict:
    """Generate tax basis breakdown for pie charts."""
    charts = {}

    if 'tax_status' in accounts.columns:
        tax_agg = accounts.groupby('tax_status').agg(
            value=('emv', 'sum'),
            count=('account_id', 'nunique'),
        ).reset_index()

        total = tax_agg['value'].sum()
        tax_agg['pct'] = (tax_agg['value'] / total * 100).round(1)

        colors = {
            'Taxable': '#4CAF50',
            'Tax-Exempt': '#2196F3',
            'Tax-Deferred': '#FF9800',
            'Other': '#9E9E9E',
        }

        charts['tax_status'] = {
            'title': 'AUA by Tax Status',
            'data': [
                {
                    'label': row['tax_status'],
                    'value': float(row['value']),
                    'pct': float(row['pct']),
                    'count': int(row['count']),
                    'color': colors.get(row['tax_status'], '#9E9E9E'),
                }
                for _, row in tax_agg.iterrows()
            ]
        }

    if 'account_owner_type' in accounts.columns:
        type_agg = accounts.groupby('account_owner_type').agg(
            value=('emv', 'sum'),
            count=('account_id', 'nunique'),
        ).reset_index()

        total = type_agg['value'].sum()
        type_agg['pct'] = (type_agg['value'] / total * 100).round(1)

        colors = {'Sole': '#2196F3', 'Joint': '#9C27B0', 'Trust': '#FF5722'}

        charts['account_type'] = {
            'title': 'AUA by Account Type',
            'data': [
                {
                    'label': row['account_owner_type'],
                    'value': float(row['value']),
                    'pct': float(row['pct']),
                    'count': int(row['count']),
                    'color': colors.get(row['account_owner_type'], '#9E9E9E'),
                }
                for _, row in type_agg.iterrows()
            ]
        }

    print(f"  tax_basis_breakdown.json: {len(charts)} charts")

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        'firm_id': FIRM_ID,
        'charts': charts,
    }


def generate_tax_deferred_candidates(accounts: pd.DataFrame, txns: pd.DataFrame) -> dict:
    """Generate list of clients who may benefit from tax-deferred strategies."""
    if 'tax_status' not in accounts.columns:
        return {
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'firm_id': FIRM_ID,
            'candidates': [],
        }

    taxable = accounts[accounts['tax_status'] == 'Taxable'].copy()

    rel_agg = taxable.groupby('client_key').agg(
        relationship_id=('relationship_id', 'first'),
        display_name=('display_name', 'first'),
        taxable_aua=('emv', 'sum'),
        account_count=('account_id', 'nunique'),
        architect=('architect', 'first'),
    ).reset_index()

    MIN_AUA = 500000
    candidates = rel_agg[rel_agg['taxable_aua'] >= MIN_AUA].copy()

    # Simple priority score
    candidates['priority_score'] = (
        (candidates['taxable_aua'] >= 2000000).astype(int) * 40 +
        (candidates['taxable_aua'] >= 1000000).astype(int) * 30 +
        (candidates['taxable_aua'] >= 500000).astype(int) * 20 +
        (candidates['account_count'] >= 4).astype(int) * 20 +
        (candidates['account_count'] >= 2).astype(int) * 10 +
        30  # Base points
    )

    candidates = candidates.sort_values('priority_score', ascending=False)
    candidates['architect'] = candidates['architect'].replace('No Architect Value Assigned', 'House')

    candidate_list = [
        {
            'client_key': row['client_key'],
            'relationship_id': row['relationship_id'],
            'display_name': row['display_name'],
            'architect': row['architect'],
            'taxable_aua': float(row['taxable_aua']),
            'account_count': int(row['account_count']),
            'priority_score': int(row['priority_score']),
        }
        for _, row in candidates.head(100).iterrows()
    ]

    print(f"  tax_deferred_candidates.json: {len(candidate_list)} candidates")

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        'firm_id': FIRM_ID,
        'scan_criteria': {'min_taxable_aua': MIN_AUA, 'tax_status': 'Taxable'},
        'summary': {
            'total_candidates': len(candidates),
            'total_opportunity_aua': float(candidates['taxable_aua'].sum()),
        },
        'candidates': candidate_list,
    }


# =============================================================================
# STEP 5: FILTERS
# =============================================================================

def generate_filters(accounts: pd.DataFrame):
    """Generate filter dimensions JSON."""
    accounts = add_client_key(accounts)

    dimensions = {}

    def gen_dim_values(df, column, transform=None, top_n=None, include_aua=True):
        if column not in df.columns:
            return []

        df = df.copy()
        df['dim_value'] = df[column].astype(str)
        if transform:
            df['dim_value'] = df['dim_value'].replace(transform)

        df = df[df['dim_value'].notna() & (df['dim_value'] != '') &
                (df['dim_value'] != 'nan') & (df['dim_value'] != 'None')]

        agg = df.groupby('dim_value').agg(
            aua=('emv', 'sum'),
            client_count=('client_key', 'nunique'),
            account_count=('account_id', 'nunique'),
        ).reset_index()

        agg = agg.sort_values('aua', ascending=False)
        if top_n:
            agg = agg.head(top_n)

        def to_id(value):
            return str(value).lower().replace(' ', '_').replace('&', 'and').replace(',', '')

        values = []
        for _, row in agg.iterrows():
            value = {'id': to_id(row['dim_value']), 'name': row['dim_value']}
            if include_aua:
                value['aua'] = float(row['aua'])
                value['client_count'] = int(row['client_count'])
            values.append(value)

        return values

    dimensions['architect'] = {
        'label': 'Architect',
        'column': 'architect',
        'values': gen_dim_values(accounts, 'architect', {'No Architect Value Assigned': 'House'}),
    }

    dimensions['region'] = {
        'label': 'Region',
        'column': 'local_ops',
        'values': gen_dim_values(accounts, 'local_ops', {'No Local Ops Value Assigned': 'Unassigned'}),
    }

    dimensions['implementor'] = {
        'label': 'Implementor',
        'column': 'implementor',
        'values': gen_dim_values(accounts, 'implementor', {'No Implementor Value Assigned': 'Unassigned'}, top_n=50),
    }

    dimensions['account_type'] = {
        'label': 'Account Type',
        'column': 'account_owner_type',
        'values': gen_dim_values(accounts, 'account_owner_type'),
    }

    dimensions['tax_status'] = {
        'label': 'Tax Status',
        'column': 'tax_status',
        'values': gen_dim_values(accounts, 'tax_status'),
    }

    dimensions['state'] = {
        'label': 'State',
        'column': 'client_state',
        'values': gen_dim_values(accounts, 'client_state', top_n=49),
    }

    dimensions['city'] = {
        'label': 'City',
        'column': 'client_city',
        'values': gen_dim_values(accounts, 'client_city', top_n=50),
    }

    dimensions['relationship'] = {
        'label': 'Household',
        'column': 'display_name',
        'values': gen_dim_values(accounts, 'display_name', top_n=100),
    }

    filters = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'firm_id': FIRM_ID,
        'dimensions': dimensions,
    }

    print(f"  dimensions.json: {len(dimensions)} dimensions")
    save_json(filters, 'gold/filters/dimensions.json')


# =============================================================================
# STEP 6: SUMMARY
# =============================================================================

def generate_summary(accounts: pd.DataFrame, txns: pd.DataFrame):
    """Generate header metrics summary."""
    accounts = add_client_key(accounts)
    txns['trade_date'] = pd.to_datetime(txns['trade_date'])
    as_of_date = txns['trade_date'].max()

    total_aua = float(accounts['emv'].sum())
    total_clients = accounts['client_key'].nunique()
    total_accounts = accounts['account_id'].nunique()

    # Calculate NNA
    today = as_of_date
    ytd_start = datetime(today.year, 1, 1)
    ttm_start = today - timedelta(days=365)

    def calc_nna(start, end):
        NNA_INFLOW_TYPES = ['Cash Deposit', 'Transfer In', 'Wire In', 'Transfer']
        NNA_OUTFLOW_TYPES = ['Cash Withdrawal', 'Transfer Out', 'Wire Out']

        mask = (txns['trade_date'] >= pd.Timestamp(start)) & (txns['trade_date'] <= pd.Timestamp(end))
        period_txns = txns[mask]

        inflow_mask = (
            period_txns['transaction_type'].isin(NNA_INFLOW_TYPES) |
            period_txns['action'].str.contains('Deposit|Transfer In|Wire In', case=False, na=False)
        )
        outflow_mask = (
            period_txns['transaction_type'].isin(NNA_OUTFLOW_TYPES) |
            period_txns['action'].str.contains('Withdrawal|Transfer Out|Wire Out', case=False, na=False)
        )

        return float(period_txns.loc[inflow_mask, 'market_value'].sum() -
                     period_txns.loc[outflow_mask, 'market_value'].sum())

    nna_ytd = calc_nna(ytd_start, today)
    nna_12m = calc_nna(ttm_start, today)

    # Build result
    result = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of': as_of_date.strftime('%Y-%m-%d'),
        'firm_id': FIRM_ID,
        'firm_name': FIRM_NAME,

        'header': {
            'total_aua': {'value': total_aua, 'label': 'Total AUA', 'format': 'currency'},
            'nna_ytd': {'value': nna_ytd, 'label': 'NNA YTD', 'format': 'currency'},
        },

        'summary': {
            'total_aua': total_aua,
            'nna_ytd': nna_ytd,
            'nna_12m': nna_12m,
            'client_count': total_clients,
            'account_count': total_accounts,
        },

        'by_architect': [],
    }

    # Top architects
    if 'architect' in accounts.columns:
        accounts['architect_display'] = accounts['architect'].replace('No Architect Value Assigned', 'House')
        arch_agg = accounts.groupby('architect_display').agg(
            aua=('emv', 'sum'),
            client_count=('client_key', 'nunique'),
            account_count=('account_id', 'nunique'),
        ).reset_index().sort_values('aua', ascending=False).head(10)

        for _, row in arch_agg.iterrows():
            result['by_architect'].append({
                'architect': row['architect_display'],
                'aua': float(row['aua']),
                'aua_pct': round(row['aua'] / total_aua * 100, 1),
                'client_count': int(row['client_count']),
                'account_count': int(row['account_count']),
            })

    print(f"  Total AUA: ${total_aua:,.0f}")
    print(f"  NNA YTD: ${nna_ytd:,.0f}")
    print(f"  NNA 12M: ${nna_12m:,.0f}")
    print(f"  Clients: {total_clients:,}")

    save_json(result, 'gold/summary/header_metrics.json')
```

### bd-portal-advisor-publisher-lambda-advisor-level-publisher.py

```
"""
BD Portal Advisor Publisher Lambda

Triggered by: S3 ObjectCreated on opal-data-bd/gold/pipeline-complete.json
              (same sentinel as bd-portal-publisher — both run in parallel)

Reads account_performance (the large parquet, ~350MB / 10M rows) to produce:
  - implementor_leaderboard.json   (LeaderboardResponse, by implementor)
  - advisors/{advisor_id}/book.json (AdvisorBookResponse, one per architect)
  - clients/{relationship_id}.json  (ClientDetailResponse, one per client)

Separated from bd-portal-publisher because account_performance is too large
to load alongside the other tables in a single Lambda execution.

Memory: 6144 MB  Timeout: 900 s  Runtime: Python 3.12
Layer:  pandas-pyarrow-layer
"""

import gc
import json
import os
import re
from datetime import datetime, timezone
from io import BytesIO

import boto3
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

INPUT_BUCKET  = os.environ.get('INPUT_BUCKET',  'opal-data-bd')
OUTPUT_BUCKET = os.environ.get('OUTPUT_BUCKET', 'opal-data-bd')
FIRM_ID       = os.environ.get('FIRM_ID',       '49financial')
FIRM_NAME     = os.environ.get('FIRM_NAME',     '49 Financial')

s3 = boto3.client('s3', region_name='us-east-1')

WINDOWS = {'3M': 90, '6M': 180, '1Y': 365, '2Y': 730, '3Y': 1095}


# ---------------------------------------------------------------------------
# S3 helpers
# ---------------------------------------------------------------------------

def _load_parquet(key: str, columns: list = None) -> pd.DataFrame:
    resp = s3.get_object(Bucket=INPUT_BUCKET, Key=key)
    kwargs = {}
    if columns:
        kwargs['columns'] = columns
    df = pd.read_parquet(BytesIO(resp['Body'].read()), **kwargs)
    print(f"  Loaded {key}: {len(df):,} rows")
    return df


def _save_json(data: dict, key: str) -> None:
    body = json.dumps(data, default=str, separators=(',', ':'))
    s3.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=key,
        Body=body.encode('utf-8'),
        ContentType='application/json',
        CacheControl='public, max-age=300, s-maxage=3600',
    )
    print(f"  Wrote {key} ({len(body):,} bytes)")


def _advisor_id(name: str) -> str:
    """Convert advisor display name to URL-safe ID: 'Travis Penfield' -> 'travis_penfield'."""
    clean = re.sub(r'[^a-z0-9_]+', '_', str(name).lower().strip())
    return clean.strip('_') or 'unknown'


def _today() -> pd.Timestamp:
    return pd.Timestamp.now(tz='UTC').normalize().tz_localize(None)


def _window_start(today: pd.Timestamp, days: int) -> pd.Timestamp:
    return today - pd.Timedelta(days=days)


def _qtd_start(today: pd.Timestamp) -> pd.Timestamp:
    """Return the first day of the current calendar quarter (QTD start)."""
    q_month = ((today.month - 1) // 3) * 3 + 1
    return pd.Timestamp(year=today.year, month=q_month, day=1)


def _latest_holdings_lots_key() -> str | None:
    """Return the S3 key of the most recent holdings_lots snapshot."""
    paginator = s3.get_paginator('list_objects_v2')
    keys = sorted([
        obj['Key']
        for page in paginator.paginate(Bucket=INPUT_BUCKET,
                                       Prefix='gold/holdings_lots/')
        for obj in page.get('Contents', [])
        if obj['Key'].endswith('.parquet') and 'backfill' not in obj['Key']
    ])
    return keys[-1] if keys else None


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_sources() -> dict:
    """Load all three source parquets with column pruning."""
    print("Loading source parquets...")

    # account_performance: all dates needed for window calculations and timeseries
    acct = _load_parquet(
        'gold/account_performance.parquet',
        columns=[
            'date', 'account_id', 'relationship_id',
            'architect', 'implementor',
            'tax_status',
            'total_aua', 'cum_inflows', 'cum_outflows', 'nna',
            'num_positions',
        ],
    )
    acct['date'] = pd.to_datetime(acct['date'])

    # client_tax_liability: for tax exposure per advisor book
    tax = _load_parquet(
        'gold/views/client_tax_liability.parquet',
        columns=[
            'relationship_id', 'account_id',
            'tax_status', 'qualified_flag',
            'asset_name', 'ticker',
            'purchase_year',
            'total_cost_basis', 'total_market_value', 'total_accrued_gain',
            'short_term_gain', 'long_term_gain',
            'num_open_lots',
        ],
    )

    # client_dimension: first_seen_date for new_clients + relationship names
    cdim = _load_parquet(
        'gold/client_dimension.parquet',
        columns=[
            'relationship_id', 'relationship_name',
            'first_seen_date',
            'primary_architect', 'primary_implementor',
        ],
    )
    cdim['first_seen_date'] = pd.to_datetime(cdim['first_seen_date'])

    # holdings_lots: latest snapshot for per-client open lot detail
    lots_key = _latest_holdings_lots_key()
    lots = pd.DataFrame()
    if lots_key:
        lots = _load_parquet(lots_key)
    else:
        print("  WARNING: no holdings_lots snapshot found")

    gc.collect()
    return dict(acct=acct, tax=tax, cdim=cdim, lots=lots)


# ---------------------------------------------------------------------------
# Shared computation helpers
# ---------------------------------------------------------------------------

def _snapshot_on(df: pd.DataFrame, date: pd.Timestamp, dim_col: str) -> pd.DataFrame:
    """Return a snapshot of df grouped by dim_col on the closest available date <= date."""
    dates_available = df['date'].unique()
    past = dates_available[dates_available <= date]
    snap_date = pd.Timestamp(past.max()) if len(past) > 0 else pd.Timestamp(dates_available.min())
    snap = df[df['date'] == snap_date]
    return snap.groupby(dim_col).agg(
        total_aua=('total_aua', 'sum'),
        cum_inflows=('cum_inflows', 'sum'),
        cum_outflows=('cum_outflows', 'sum'),
        nna=('nna', 'sum'),
        num_accounts=('account_id', 'nunique'),
        num_relationships=('relationship_id', 'nunique'),
    ).reset_index()


def _nna_for_window(acct_dim: pd.DataFrame, dim_col: str, dim_val: str,
                     today: pd.Timestamp, days: int) -> float:
    """
    NNA for one advisor over a window.
    acct_dim is already filtered to this advisor's rows.
    NNA = (cum_inflows - cum_outflows) at end_date - at start_date, summed across accounts.
    """
    sub = acct_dim.copy()
    dates = sub['date'].sort_values().unique()
    end_date   = pd.Timestamp(dates.max())
    start_date = _window_start(today, days)

    past = dates[dates <= start_date]
    snap_start = pd.Timestamp(past.max()) if len(past) > 0 else pd.Timestamp(dates.min())

    end_vals   = sub[sub['date'] == end_date].agg(
        cum_inflows=('cum_inflows', 'sum'), cum_outflows=('cum_outflows', 'sum'))
    start_vals = sub[sub['date'] == snap_start].agg(
        cum_inflows=('cum_inflows', 'sum'), cum_outflows=('cum_outflows', 'sum'))

    inflow_delta  = float(end_vals['cum_inflows'])  - float(start_vals['cum_inflows'])
    outflow_delta = float(end_vals['cum_outflows']) - float(start_vals['cum_outflows'])
    return inflow_delta - outflow_delta


# ---------------------------------------------------------------------------
# 1. Implementor leaderboard  (LeaderboardResponse)
# ---------------------------------------------------------------------------

def build_implementor_leaderboard(acct: pd.DataFrame, cdim: pd.DataFrame,
                                   today: pd.Timestamp) -> dict:
    """
    Same structure as architect_leaderboard from bd-portal-publisher.
    Uses account_performance grouped by implementor.
    """
    print("Building implementor_leaderboard.json...")

    latest_date = acct['date'].max()
    windows_data = {}

    # Rolling trailing windows + calendar QTD + calendar YTD
    all_window_starts = [(lbl, _window_start(today, d)) for lbl, d in WINDOWS.items()]
    all_window_starts.append(('qtd', _qtd_start(today)))
    ytd_start = pd.Timestamp(year=today.year, month=1, day=1)
    all_window_starts.append(('ytd', ytd_start))
    # In Q1 (Jan-Mar), qtd and ytd have identical start dates (both Jan 1)

    for label, w_start in all_window_starts:
        dates   = acct['date'].sort_values().unique()
        past    = dates[dates <= w_start]
        snap_start = pd.Timestamp(past.max()) if len(past) > 0 else pd.Timestamp(dates.min())

        end_snap   = _snapshot_on(acct, latest_date, 'implementor')
        start_snap = _snapshot_on(acct, snap_start,  'implementor').set_index('implementor')

        entries = []
        for _, row in end_snap.iterrows():
            impl = str(row['implementor'])
            if not impl or impl.lower() in ('', 'nan', 'none', 'unassigned',
                                             'no implementor value assigned'):
                impl = 'Unassigned'

            total_aua     = float(row['total_aua'])
            client_count  = int(row['num_relationships'])
            account_count = int(row['num_accounts'])

            s_row      = start_snap.loc[impl] if impl in start_snap.index else None
            nna_end    = float(row['nna'])
            nna_start  = float(s_row['nna']) if s_row is not None else 0.0
            nna_window = nna_end - nna_start

            aua_start_val  = float(s_row['total_aua']) if s_row is not None else 0.0
            aua_growth_pct = (
                (total_aua - aua_start_val) / aua_start_val * 100
                if aua_start_val > 0 else 0.0
            )

            # New clients (relationships) whose primary_implementor matches and joined in window
            cdim_match = cdim[cdim['primary_implementor'] == impl]
            new_clients = int((cdim_match['first_seen_date'] >= w_start).sum())

            entries.append({
                'name':            impl,
                'nna':             round(nna_window, 2),
                'aua_growth_pct':  round(aua_growth_pct, 2),
                'new_clients':     new_clients,
                'total_aua':       round(total_aua, 2),
                'client_count':    client_count,
                'account_count':   account_count,
            })

        entries.sort(key=lambda x: x['nna'], reverse=True)
        for i, e in enumerate(entries):
            e['rank'] = i + 1

        total_nna = sum(e['nna'] for e in entries)
        total_aua_all = sum(e['total_aua'] for e in entries)
        windows_data[label] = {
            'entry_count': len(entries),
            'summary': {
                'total_nna':            round(total_nna, 2),
                'total_aua':            round(total_aua_all, 2),
                'total_new_clients':    sum(e['new_clients'] for e in entries),
                'positive_nna_count':   sum(1 for e in entries if e['nna'] >= 0),
                'negative_nna_count':   sum(1 for e in entries if e['nna'] < 0),
            },
            'entries': entries,
        }
        print(f"  Window {label}: {len(entries)} implementors")

    return {
        'generated_at':     datetime.now(timezone.utc).isoformat(),
        'data_as_of':       latest_date.strftime('%Y-%m-%d'),
        'firm_id':          FIRM_ID,
        'leaderboard_type': 'implementor',
        'available_windows': list(WINDOWS.keys()) + ['qtd', 'ytd'],
        'windows':          windows_data,
    }


# ---------------------------------------------------------------------------
# 2. Per-advisor book files  (AdvisorBookResponse)
# ---------------------------------------------------------------------------

def _build_advisor_tax_exposure(tax: pd.DataFrame, rel_ids: set) -> dict:
    """Tax exposure for a book of relationships from client_tax_liability."""
    book_tax = tax[tax['relationship_id'].isin(rel_ids)]

    if book_tax.empty:
        return {
            'taxable': 0.0, 'taxable_pct': 0.0,
            'tax_deferred': 0.0, 'tax_deferred_pct': 0.0,
            'tax_free': 0.0, 'tax_free_pct': 0.0,
            'qualified_aua': 0.0, 'qualified_pct': 0.0,
            'non_qualified_aua': 0.0, 'non_qualified_pct': 0.0,
            'non_qualified_cost_basis': 0.0,
            'non_qualified_unrealized_gain': 0.0,
            'short_term_gain': 0.0,
            'long_term_gain': 0.0,
        }

    taxable_mv  = float(book_tax.loc[book_tax['tax_status'] == 'taxable',
                                      'total_market_value'].sum())
    deferred_mv = float(book_tax.loc[book_tax['tax_status'] == 'tax_deferred',
                                      'total_market_value'].sum())
    exempt_mv   = float(book_tax.loc[book_tax['tax_status'] == 'tax_exempt',
                                      'total_market_value'].sum())
    total_mv    = taxable_mv + deferred_mv + exempt_mv

    qual_mv    = float(book_tax.loc[book_tax['qualified_flag'] == True,
                                     'total_market_value'].sum())
    nonqual_mv = float(book_tax.loc[book_tax['qualified_flag'] == False,
                                     'total_market_value'].sum())

    taxable_only = book_tax[book_tax['tax_status'] == 'taxable']
    nq_cost_basis   = float(taxable_only['total_cost_basis'].sum())
    nq_unreal_gain  = float(taxable_only['total_accrued_gain'].sum())
    st_gain         = float(taxable_only['short_term_gain'].sum())
    lt_gain         = float(taxable_only['long_term_gain'].sum())

    def pct(v): return round(v / total_mv * 100, 1) if total_mv > 0 else 0.0
    lot_total = qual_mv + nonqual_mv

    return {
        'taxable':                      round(taxable_mv, 2),
        'taxable_pct':                  pct(taxable_mv),
        'tax_deferred':                 round(deferred_mv, 2),
        'tax_deferred_pct':             pct(deferred_mv),
        'tax_free':                     round(exempt_mv, 2),
        'tax_free_pct':                 pct(exempt_mv),
        'qualified_aua':                round(qual_mv, 2),
        'qualified_pct':                round(qual_mv / lot_total * 100, 1) if lot_total > 0 else 0.0,
        'non_qualified_aua':            round(nonqual_mv, 2),
        'non_qualified_pct':            round(nonqual_mv / lot_total * 100, 1) if lot_total > 0 else 0.0,
        'non_qualified_cost_basis':     round(nq_cost_basis, 2),
        'non_qualified_unrealized_gain': round(nq_unreal_gain, 2),
        'short_term_gain':              round(st_gain, 2),
        'long_term_gain':               round(lt_gain, 2),
    }


def _build_advisor_engagement(acct_book: pd.DataFrame, cdim: pd.DataFrame,
                               rel_ids: set, today: pd.Timestamp) -> dict:
    """Engagement metrics for one advisor's book."""
    ttm_cutoff = today - pd.Timedelta(days=365)
    dates = acct_book['date'].sort_values().unique()
    latest_date = pd.Timestamp(dates.max())

    past_ttm = dates[dates <= ttm_cutoff]
    ttm_start_date = (pd.Timestamp(past_ttm.max()) if len(past_ttm) > 0
                      else pd.Timestamp(dates.min()))

    end_snap   = acct_book[acct_book['date'] == latest_date]
    start_snap = acct_book[acct_book['date'] == ttm_start_date]

    inflows_ttm  = float(end_snap['cum_inflows'].sum())  - float(start_snap['cum_inflows'].sum())
    outflows_ttm = float(end_snap['cum_outflows'].sum()) - float(start_snap['cum_outflows'].sum())
    net_flows_ttm = inflows_ttm - outflows_ttm

    # Average tenure: days since first_seen_date for matching relationships
    book_cdim = cdim[cdim['relationship_id'].isin(rel_ids)]
    avg_tenure_days = 0
    if not book_cdim.empty and book_cdim['first_seen_date'].notna().any():
        tenure = (today - book_cdim['first_seen_date'].dropna()).dt.days
        avg_tenure_days = int(tenure.mean()) if len(tenure) > 0 else 0

    return {
        'net_flows_ttm':   round(net_flows_ttm, 2),
        'inflows_ttm':     round(inflows_ttm, 2),
        'outflows_ttm':    round(outflows_ttm, 2),
        'avg_tenure_days': avg_tenure_days,
    }


def build_advisor_books(acct: pd.DataFrame, tax: pd.DataFrame,
                         cdim: pd.DataFrame, today: pd.Timestamp) -> list:
    """
    Build one AdvisorBookResponse per architect and return a list of (key, dict) pairs.
    """
    print("Building advisor book files...")

    latest_date  = acct['date'].max()
    all_dates    = acct['date'].sort_values().unique()

    # Identify all architect values present in latest snapshot
    latest_snap = acct[acct['date'] == latest_date]
    architects  = latest_snap['architect'].dropna().unique().tolist()
    print(f"  {len(architects)} architects to process")

    # Pre-compute quarterly NNA start dates
    def _qstart(quarters_back: int) -> pd.Timestamp:
        today_q_month = ((today.month - 1) // 3) * 3 + 1
        month = today_q_month - quarters_back * 3
        year  = today.year + (month - 1) // 12
        month = ((month - 1) % 12) + 1
        return pd.Timestamp(year=year, month=month, day=1)

    ytd_start = pd.Timestamp(today.year, 1, 1)
    qtd_start = _qstart(0)
    mtd_start = pd.Timestamp(today.year, today.month, 1)

    books = []

    for architect in architects:
        arch_str = str(architect)
        adv_id   = _advisor_id(arch_str)

        # All rows for this architect across all dates
        acct_arch = acct[acct['architect'] == architect]
        if acct_arch.empty:
            continue

        # Relationships in this book (from latest snapshot)
        rel_ids = set(latest_snap.loc[latest_snap['architect'] == architect,
                                       'relationship_id'].unique())

        # ---- Summary (latest date) ----
        snap_latest = acct_arch[acct_arch['date'] == latest_date]
        total_aua     = float(snap_latest['total_aua'].sum())
        account_count = int(snap_latest['account_id'].nunique())
        client_count  = int(snap_latest['relationship_id'].nunique())

        # ---- NNA (ytd / qtd / mtd) ----
        def _nna_since(start_ts: pd.Timestamp) -> float:
            past = all_dates[all_dates <= start_ts]
            snap_start_date = (pd.Timestamp(past.max()) if len(past) > 0
                               else pd.Timestamp(all_dates.min()))
            end_v   = acct_arch[acct_arch['date'] == latest_date]
            start_v = acct_arch[acct_arch['date'] == snap_start_date]
            inf_d  = float(end_v['cum_inflows'].sum())  - float(start_v['cum_inflows'].sum())
            out_d  = float(end_v['cum_outflows'].sum()) - float(start_v['cum_outflows'].sum())
            return inf_d - out_d

        nna_ytd = _nna_since(ytd_start)
        nna_qtd = _nna_since(qtd_start)
        nna_mtd = _nna_since(mtd_start)

        # ---- AUA growth (YTD, QTD) ----
        def _aua_at(start_ts: pd.Timestamp) -> float:
            past = all_dates[all_dates <= start_ts]
            snap_date = (pd.Timestamp(past.max()) if len(past) > 0
                         else pd.Timestamp(all_dates.min()))
            rows = acct_arch[acct_arch['date'] == snap_date]
            return float(rows['total_aua'].sum())

        aua_ytd_start = _aua_at(ytd_start)
        aua_qtd_start = _aua_at(qtd_start)
        ytd_growth_pct = ((total_aua - aua_ytd_start) / aua_ytd_start * 100
                          if aua_ytd_start > 0 else 0.0)
        qtd_growth_pct = ((total_aua - aua_qtd_start) / aua_qtd_start * 100
                          if aua_qtd_start > 0 else 0.0)

        # ---- Tax exposure ----
        tax_exposure = _build_advisor_tax_exposure(tax, rel_ids)

        # ---- Engagement ----
        engagement = _build_advisor_engagement(acct_arch, cdim, rel_ids, today)

        # ---- Client list (sorted by AUA desc) ----
        client_snap = (
            snap_latest
            .groupby('relationship_id')['total_aua']
            .sum()
            .reset_index()
            .merge(cdim[['relationship_id', 'relationship_name']],
                   on='relationship_id', how='left')
            .sort_values('total_aua', ascending=False)
        )
        clients = [
            {
                'client_key':  str(r['relationship_id']),
                'client_name': (str(r['relationship_name'])
                                if pd.notna(r['relationship_name'])
                                else str(r['relationship_id'])),
                'aua': round(float(r['total_aua']), 2),
            }
            for _, r in client_snap.iterrows()
        ]

        book = {
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'data_as_of':   latest_date.strftime('%Y-%m-%d'),

            'book_type': 'architect',
            'book_key':  adv_id,
            'book_name': arch_str,

            'summary': {
                'total_aua':    round(total_aua, 2),
                'client_count': client_count,
                'account_count': account_count,
            },

            'nna': {
                'ytd': round(nna_ytd, 2),
                'qtd': round(nna_qtd, 2),
                'mtd': round(nna_mtd, 2),
            },

            'growth': {
                'ytd_pct': round(ytd_growth_pct, 2),
                'qtd_pct': round(qtd_growth_pct, 2),
            },

            # Tax exposure from client_tax_liability
            # Includes Yang's qualified/non-qualified and cost basis fields
            'tax_exposure': tax_exposure,

            # Income & fees: not available from BD data
            'income_fees': {
                'income_total_ttm':      0.0,
                'avg_income_yield_pct':  0.0,
                'fees_total_ttm':        0.0,
                'avg_fee_rate_pct':      0.0,
            },

            # Portfolio composition: asset class taxonomy not in BD data
            'portfolio_composition': {
                'asset_allocation':  [],
                'avg_expense_ratio': 0.0,
            },

            'engagement': engagement,
            'clients':    clients,
        }

        books.append((_advisor_output_key(adv_id), book))
        print(f"  {arch_str}: AUA=${total_aua:,.0f}, {client_count} clients, "
              f"{account_count} accounts, NNA_YTD=${nna_ytd:,.0f}")

    return books


def _advisor_output_key(adv_id: str) -> str:
    return f'gold/advisors/{adv_id}/book.json'


# ---------------------------------------------------------------------------
# 3. Per-client detail files  (ClientDetailResponse)
# ---------------------------------------------------------------------------

def _build_headline(acct: pd.DataFrame) -> dict:
    latest_date = acct['date'].max()
    snap = acct[acct['date'] == latest_date]
    return {
        'total_aua':        round(float(snap['total_aua'].sum()), 2),
        'account_count':    int(snap['account_id'].nunique()),
        'client_count':     1,
        'fee_rate_pct':     0.0,
        'income_yield_pct': 0.0,
    }


def _build_tax(acct: pd.DataFrame, tax: pd.DataFrame, lots: pd.DataFrame,
               today: pd.Timestamp) -> dict:
    """Full tax section for one household."""
    latest_date = acct['date'].max()
    snap = acct[acct['date'] == latest_date]

    total_aua    = float(snap['total_aua'].sum())
    aua_taxable  = float(snap.loc[snap['tax_status'] == 'taxable',   'total_aua'].sum())
    aua_deferred = float(snap.loc[snap['tax_status'] == 'tax_deferred', 'total_aua'].sum())
    aua_exempt   = float(snap.loc[snap['tax_status'] == 'tax_exempt', 'total_aua'].sum())

    def pct(v): return round(v / total_aua * 100, 1) if total_aua > 0 else 0.0

    # --- Qualified vs non-qualified from client_tax_liability ---
    tax_qual    = tax[tax['qualified_flag'] == True]
    tax_nonqual = tax[tax['qualified_flag'] == False]
    tax_taxable = tax[tax['tax_status'] == 'taxable']

    qual_mv    = float(tax_qual['total_market_value'].sum())
    nonqual_mv = float(tax_nonqual['total_market_value'].sum())
    lot_total  = qual_mv + nonqual_mv

    qual_pct    = round(qual_mv    / lot_total * 100, 1) if lot_total > 0 else 0.0
    nonqual_pct = round(nonqual_mv / lot_total * 100, 1) if lot_total > 0 else 0.0

    qual_acct_count    = int(tax_qual['account_id'].nunique())
    nonqual_acct_count = int(tax_nonqual['account_id'].nunique())

    nq_cost_basis  = float(tax_taxable['total_cost_basis'].sum())
    nq_market_val  = float(tax_taxable['total_market_value'].sum())
    nq_unrealized  = float(tax_taxable['total_accrued_gain'].sum())
    st_gain        = float(tax_taxable['short_term_gain'].sum())
    lt_gain        = float(tax_taxable['long_term_gain'].sum())

    # --- Cost basis by purchase year ---
    year_cols = ['purchase_year', 'total_cost_basis', 'total_market_value',
                 'total_accrued_gain', 'short_term_gain', 'long_term_gain', 'asset_name']
    year_cols_avail = [c for c in year_cols if c in tax_taxable.columns]
    if not tax_taxable.empty and 'purchase_year' in tax_taxable.columns:
        year_agg = (
            tax_taxable[year_cols_avail]
            .groupby('purchase_year', dropna=False)
            .agg(
                cost_basis=('total_cost_basis', 'sum'),
                market_value=('total_market_value', 'sum'),
                unrealized_gain=('total_accrued_gain', 'sum'),
                short_term_gain=('short_term_gain', 'sum'),
                long_term_gain=('long_term_gain', 'sum'),
                num_positions=('asset_name', 'nunique'),
            )
            .reset_index()
            .sort_values('purchase_year')
        )
        cost_basis_by_year = [
            {
                'purchase_year':   int(r['purchase_year']) if pd.notna(r['purchase_year']) else None,
                'cost_basis':      round(float(r['cost_basis']), 2),
                'market_value':    round(float(r['market_value']), 2),
                'unrealized_gain': round(float(r['unrealized_gain']), 2),
                'short_term_gain': round(float(r['short_term_gain']), 2),
                'long_term_gain':  round(float(r['long_term_gain']), 2),
                'num_positions':   int(r['num_positions']),
            }
            for _, r in year_agg.iterrows()
        ]
    else:
        cost_basis_by_year = []

    # --- Top gain positions ---
    if not tax_taxable.empty and 'asset_name' in tax_taxable.columns:
        pos_agg = (
            tax_taxable
            .groupby(['asset_name', 'ticker'], dropna=False)
            .agg(
                cost_basis=('total_cost_basis', 'sum'),
                market_value=('total_market_value', 'sum'),
                unrealized_gain=('total_accrued_gain', 'sum'),
                short_term_gain=('short_term_gain', 'sum'),
                long_term_gain=('long_term_gain', 'sum'),
                num_lots=('num_open_lots', 'sum'),
            )
            .reset_index()
            .sort_values('unrealized_gain', ascending=False)
            .head(20)
        )
        top_gain_positions = [
            {
                'asset_name':      str(r['asset_name']),
                'ticker':          str(r['ticker']) if pd.notna(r['ticker']) else None,
                'cost_basis':      round(float(r['cost_basis']), 2),
                'market_value':    round(float(r['market_value']), 2),
                'unrealized_gain': round(float(r['unrealized_gain']), 2),
                'short_term_gain': round(float(r['short_term_gain']), 2),
                'long_term_gain':  round(float(r['long_term_gain']), 2),
                'num_lots':        int(r['num_lots']),
            }
            for _, r in pos_agg.iterrows()
        ]
    else:
        top_gain_positions = []

    # --- Open lots (taxable only) ---
    open_lots = []
    if not lots.empty:
        taxable_open = lots[
            lots.get('is_open', pd.Series(True, index=lots.index)) == True
        ]
        if 'tax_status' in taxable_open.columns:
            taxable_open = taxable_open[taxable_open['tax_status'] == 'taxable']

        sort_cols = [c for c in ['account_id', 'asset_name', 'lot_index']
                     if c in taxable_open.columns]
        if sort_cols:
            taxable_open = taxable_open.sort_values(sort_cols)

        lot_cols = [
            'account_id', 'account_name',
            'asset_name', 'ticker',
            'acquisition_date', 'purchase_year', 'lot_index',
            'current_units', 'cost_per_unit', 'cost_basis',
            'current_price', 'market_value', 'accrued_gain',
            'holding_period_days', 'term',
        ]
        available = [c for c in lot_cols if c in taxable_open.columns]

        for _, row in taxable_open[available].iterrows():
            lot = {}
            for col in available:
                val = row[col]
                if isinstance(val, (pd.Timestamp,)):
                    lot[col] = val.strftime('%Y-%m-%d')
                elif isinstance(val, float) and pd.notna(val):
                    lot[col] = round(val, 4)
                elif pd.isna(val) if not isinstance(val, str) else False:
                    lot[col] = None
                else:
                    lot[col] = val
            open_lots.append(lot)

    return {
        'taxable':          round(aua_taxable, 2),
        'taxable_pct':      pct(aua_taxable),
        'tax_deferred':     round(aua_deferred, 2),
        'tax_deferred_pct': pct(aua_deferred),
        'tax_free':         round(aua_exempt, 2),
        'tax_free_pct':     pct(aua_exempt),
        'capital_gains_ttm': round(nq_unrealized, 2),
        'qualified_aua':               round(qual_mv, 2),
        'qualified_pct':               qual_pct,
        'non_qualified_aua':           round(nonqual_mv, 2),
        'non_qualified_pct':           nonqual_pct,
        'qualified_account_count':     qual_acct_count,
        'non_qualified_account_count': nonqual_acct_count,
        'non_qualified_cost_basis':      round(nq_cost_basis, 2),
        'non_qualified_market_value':    round(nq_market_val, 2),
        'non_qualified_unrealized_gain': round(nq_unrealized, 2),
        'short_term_gain':               round(st_gain, 2),
        'long_term_gain':                round(lt_gain, 2),
        'cost_basis_by_year': cost_basis_by_year,
        'top_gain_positions': top_gain_positions,
        'open_lots': open_lots,
        'open_lots_count': len(open_lots),
    }


def _build_engagement(acct: pd.DataFrame, cdim_row, today: pd.Timestamp) -> dict:
    """NNA flows TTM and relationship tenure."""
    dates = acct['date'].sort_values().unique()
    latest_date = pd.Timestamp(dates.max())

    ttm_cutoff = today - pd.Timedelta(days=365)
    past_ttm   = dates[dates <= ttm_cutoff]
    ttm_start  = (pd.Timestamp(past_ttm.max()) if len(past_ttm) > 0
                  else pd.Timestamp(dates.min()))

    end_snap   = acct[acct['date'] == latest_date]
    start_snap = acct[acct['date'] == ttm_start]

    inflows_ttm  = float(end_snap['cum_inflows'].sum())  - float(start_snap['cum_inflows'].sum())
    outflows_ttm = float(end_snap['cum_outflows'].sum()) - float(start_snap['cum_outflows'].sum())
    net_flows_ttm = inflows_ttm - outflows_ttm

    avg_relationship_years = 0.0
    if cdim_row is not None and pd.notna(cdim_row.get('first_seen_date')):
        days = (today - cdim_row['first_seen_date']).days
        avg_relationship_years = round(days / 365.25, 2)

    return {
        'trading_buys_ttm':      0,
        'trading_sells_ttm':     0,
        'net_flows_ttm':         round(net_flows_ttm, 2),
        'avg_relationship_years': avg_relationship_years,
        'active_clients_pct':    100.0,
    }


def _build_accounts(acct: pd.DataFrame) -> list:
    """Per-account breakdown for the household drill-down panel."""
    latest_date = acct['date'].max()
    snap = acct[acct['date'] == latest_date].copy()

    accounts = []
    for _, row in snap.sort_values('total_aua', ascending=False).iterrows():
        accounts.append({
            'account_id':    str(row['account_id']),
            'tax_status':    str(row.get('tax_status', 'taxable')),
            'total_aua':     round(float(row['total_aua']), 2),
            'cum_inflows':   round(float(row['cum_inflows']), 2),
            'cum_outflows':  round(float(row['cum_outflows']), 2),
            'nna':           round(float(row['nna']), 2),
            'num_positions': int(row.get('num_positions', 0)),
        })
    return accounts


def build_client_details(acct: pd.DataFrame, tax: pd.DataFrame,
                         lots: pd.DataFrame, cdim: pd.DataFrame,
                         today: pd.Timestamp) -> int:
    """Pre-generate gold/clients/{relationship_id}.json for every client."""
    print("Building client detail files...")

    latest_date = acct['date'].max()
    latest_snap = acct[acct['date'] == latest_date]
    all_rel_ids = latest_snap['relationship_id'].dropna().unique()
    print(f"  {len(all_rel_ids)} clients to process")

    count = 0
    for rel_id in all_rel_ids:
        rel_id_str = str(rel_id)

        # Filter each source to this relationship
        acct_r = acct[acct['relationship_id'] == rel_id].copy()
        tax_r  = tax[tax['relationship_id'] == rel_id].copy() if not tax.empty else pd.DataFrame()
        lots_r = lots[lots['relationship_id'] == rel_id].copy() if not lots.empty else pd.DataFrame()
        cdim_rows = cdim[cdim['relationship_id'] == rel_id]
        cdim_row  = cdim_rows.iloc[0] if len(cdim_rows) > 0 else None

        if acct_r.empty:
            continue

        # Client name
        client_name = rel_id_str
        if cdim_row is not None and pd.notna(cdim_row.get('relationship_name')):
            client_name = str(cdim_row['relationship_name'])

        # Build response sections
        headline   = _build_headline(acct_r)
        tax_sec    = _build_tax(acct_r, tax_r, lots_r, today)
        engagement = _build_engagement(acct_r, cdim_row, today)
        accounts   = _build_accounts(acct_r)

        response = {
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'data_as_of':   latest_date.strftime('%Y-%m-%d'),
            'firm_id':      FIRM_ID,
            'client_key':   rel_id_str,
            'client_name':  client_name,
            'headline':     headline,
            'tax':          tax_sec,
            'income_fees': {
                'dividends_ttm': 0.0, 'interest_ttm': 0.0,
                'total_income_ttm': 0.0, 'income_yield_pct': 0.0,
                'management_fees_ttm': 0.0, 'fee_rate_pct': 0.0,
            },
            'portfolio': {
                'allocation': [],
                'weighted_expense_ratio': 0.0,
                'unique_holdings': int(acct_r[acct_r['date'] == latest_date]['num_positions'].sum()),
                'top_5_concentration_pct': 0.0,
            },
            'engagement': engagement,
            'accounts':   accounts,
        }

        _save_json(response, f'gold/clients/{rel_id_str}.json')
        count += 1

    print(f"  Wrote {count} client detail files")
    return count


# ---------------------------------------------------------------------------
# Lambda handler
# ---------------------------------------------------------------------------

def lambda_handler(event, context):
    print("=" * 70)
    print("BD PORTAL ADVISOR PUBLISHER")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print(f"Event: {json.dumps(event)}")
    print("=" * 70)

    today = _today()

    try:
        # ------------------------------------------------------------------
        # Step 1: Load parquets
        # ------------------------------------------------------------------
        print("\n=== Step 1: Load parquets ===")
        data = load_sources()
        acct = data['acct']
        tax  = data['tax']
        cdim = data['cdim']
        lots = data['lots']

        # ------------------------------------------------------------------
        # Step 2: Implementor leaderboard
        # ------------------------------------------------------------------
        print("\n=== Step 2: Implementor leaderboard ===")
        impl_lb = build_implementor_leaderboard(acct, cdim, today)
        _save_json(impl_lb, 'gold/implementor_leaderboard.json')

        # ------------------------------------------------------------------
        # Step 3: Per-advisor book files
        # ------------------------------------------------------------------
        print("\n=== Step 3: Advisor book files ===")
        books = build_advisor_books(acct, tax, cdim, today)

        for key, book_data in books:
            _save_json(book_data, key)

        # ------------------------------------------------------------------
        # Step 4: Per-client detail JSONs
        # ------------------------------------------------------------------
        print("\n=== Step 4: Client detail files ===")
        client_count = build_client_details(acct, tax, lots, cdim, today)

        # ------------------------------------------------------------------
        # Step 5: Summary
        # ------------------------------------------------------------------
        latest_date = acct['date'].max()
        total_aua   = float(acct[acct['date'] == latest_date]['total_aua'].sum())

        print(f"\n=== Step 5: Complete ===")
        print(f"  Implementor leaderboard: written")
        print(f"  Advisor books:           {len(books)} files")
        print(f"  Client details:          {client_count} files")
        print(f"  Data as of:              {latest_date.date()}")
        print(f"  Total AUA (acct grain):  ${total_aua:,.0f}")
        print(f"Completed: {datetime.now(timezone.utc).isoformat()}")
        print("=" * 70)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'status':       'success',
                'generated_at': datetime.now(timezone.utc).isoformat(),
                'data_as_of':   latest_date.strftime('%Y-%m-%d'),
                'total_aua':    round(total_aua, 2),
                'advisor_books_written': len(books),
                'client_details_written': client_count,
            }),
        }

    except Exception as exc:
        import traceback
        print(f"\nFATAL: {exc}")
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps({'status': 'error', 'error': str(exc)}),
        }
```

### bd-portal-publisher-lambda-partneranalytics-disabled----ec2-script-09-owns-output.py

```
"""
BD Portal Publisher Lambda

Triggered by: S3 ObjectCreated on opal-data-bd/gold/pipeline-complete.json
              (written by bd-gold-layer-runner EC2 at end of gold pipeline run)

Reads validated gold parquets, generates all aggregate static JSON files
consumed by the Advisor Intelligence portal (Leaderboard tab + Clients tab).

Outputs (all written to opal-data-bd):
  gold/timeseries_chart.json              -> CumulativeChartResponse
  gold/architect_leaderboard.json         -> LeaderboardResponse
  gold/clients_tab.json                   -> ClientsTabResponse (with Yang tax fields)
  gold/summary/header_metrics.json        -> HeaderMetricsResponse
  gold/partner_analytics/header_metrics.json -> PartnerAnalyticsResponse
  gold/filters/dimensions.json            -> FiltersResponse
  gold/snapshots/aua_by_architect.json    -> SnapshotResponse
  gold/snapshots/aua_by_state.json        -> SnapshotResponse
  gold/snapshots/aua_by_tax_status.json   -> SnapshotResponse
  gold/snapshots/aua_by_region.json       -> SnapshotResponse

Memory: 4096 MB  Timeout: 900 s  Runtime: Python 3.12
Layer:  pandas-pyarrow-layer
"""

import gc
import json
import os
from datetime import datetime, date, timedelta, timezone
from io import BytesIO

import boto3
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

INPUT_BUCKET  = os.environ.get('INPUT_BUCKET',  'opal-data-bd')
OUTPUT_BUCKET = os.environ.get('OUTPUT_BUCKET', 'opal-data-bd')
FIRM_ID       = os.environ.get('FIRM_ID',       '49financial')
FIRM_NAME     = os.environ.get('FIRM_NAME',     '49 Financial')

s3 = boto3.client('s3', region_name='us-east-1')

# Time windows for leaderboard (label -> calendar days)
WINDOWS = {'3M': 90, '6M': 180, '1Y': 365, '2Y': 730, '3Y': 1095}

# Top N architects/states to show individually; rest collapse to "Other"
TOP_N_ADV = 8
TOP_N_GEO = 8

# Top N clients per architect in adv_drill (per-client AUA drill-down)
TOP_N_CLIENTS_PER_ARCH = 8

# Top N cities per state in cla.geo_city_drill
MAX_CLA_CITIES = 9

# For filters/snapshots
TOP_N_CITIES      = 50
TOP_N_IMPLEMENTOR = 50
TOP_N_STATE       = 49
TOP_N_RELATIONSHIP = 100

# Top positions by unrealized gain shown in tax section
TOP_GAIN_POSITIONS = 20

# ---------------------------------------------------------------------------
# Y3: Asset class classification (name-pattern based)
# ---------------------------------------------------------------------------
# Order matters: more specific patterns checked first.
_CASH_PATTERNS = (
    'cash', 't-bill', 'treasury bill', 'money market', 'mm fund',
    'sweep', 'fdic', 'savings',
)
_FIXED_INCOME_PATTERNS = (
    'bond', 'treasury', 'credit', 'clo', 'duration', 'fixed income',
    'aggregate', 'high yield', 'investment grade', 'tips', 'muni',
    'corporate', 'govt', 'government', 'floating rate', 'loan',
    'mortgage', 'mbs', 'abs', 'securitized',
)
_REAL_ESTATE_PATTERNS = (
    'reit', 'real estate', 'property', 'mortgage reit',
)
_ALTERNATIVES_PATTERNS = (
    'gold', 'commodity', 'vix', 'infrastructure',
    'hedge', 'private', 'alternative', 'merger', 'arbitrage',
    'mlp', 'pipeline', 'timber', 'farmland',
)
_INTL_EQUITY_PATTERNS = (
    'eafe', 'emerging', 'international', 'global', 'world', 'foreign',
    'europe', 'asia', 'japan', 'china', 'em ', 'intl', 'developed markets',
    'ex-us', 'ex us', 'non-us', 'non us', 'acwi',
)
_EQUITY_PATTERNS = (
    's&p', 'nasdaq', 'dividend', 'equity', 'value', 'growth', 'stock',
    'large cap', 'mid cap', 'small cap', 'total market', 'russell',
    'dow', 'bluechip', 'sector', 'technology', 'healthcare', 'financial',
    'energy', 'consumer', 'industrial', 'utilities', 'materials',
    'vti', 'voo', 'spy', 'qqq', 'iwm', 'dia',
)

ASSET_CLASS_LABELS = {
    'equities':     'Equities',
    'fixed_income': 'Fixed Income',
    'real_estate':  'Real Estate',
    'alternatives': 'Alternatives',
    'cash':         'Cash',
    'other':        'Other',
}


def _classify_asset(name: str) -> str:
    """Classify an asset name into one of 6 asset classes."""
    if not name or (isinstance(name, float) and np.isnan(name)):
        return 'other'
    nl = name.lower()
    if any(p in nl for p in _CASH_PATTERNS):
        return 'cash'
    if any(p in nl for p in _FIXED_INCOME_PATTERNS):
        return 'fixed_income'
    if any(p in nl for p in _REAL_ESTATE_PATTERNS):
        return 'real_estate'
    if any(p in nl for p in _ALTERNATIVES_PATTERNS):
        return 'alternatives'
    if any(p in nl for p in _INTL_EQUITY_PATTERNS):
        return 'equities'
    if any(p in nl for p in _EQUITY_PATTERNS):
        return 'equities'
    return 'other'


# ---------------------------------------------------------------------------
# S3 helpers
# ---------------------------------------------------------------------------

def _load_parquet(key: str, columns: list = None) -> pd.DataFrame:
    """Load a parquet from INPUT_BUCKET into a DataFrame."""
    resp = s3.get_object(Bucket=INPUT_BUCKET, Key=key)
    kwargs = {}
    if columns:
        kwargs['columns'] = columns
    df = pd.read_parquet(BytesIO(resp['Body'].read()), **kwargs)
    print(f"  Loaded {key}: {len(df):,} rows")
    return df


def _load_latest_parquet_in_prefix(prefix: str, columns: list = None) -> pd.DataFrame:
    """Load the lexicographically latest .parquet file under a prefix."""
    paginator = s3.get_paginator('list_objects_v2')
    keys = sorted([
        obj['Key']
        for page in paginator.paginate(Bucket=INPUT_BUCKET, Prefix=prefix)
        for obj in page.get('Contents', [])
        if obj['Key'].endswith('.parquet')
    ])
    if not keys:
        raise RuntimeError(f"No parquet files found at s3://{INPUT_BUCKET}/{prefix}")
    return _load_parquet(keys[-1], columns=columns)


def _save_json(data: dict, key: str) -> None:
    """Write a dict as JSON to OUTPUT_BUCKET."""
    body = json.dumps(data, default=str, separators=(',', ':'))
    s3.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=key,
        Body=body.encode('utf-8'),
        ContentType='application/json',
        CacheControl='public, max-age=300, s-maxage=3600',
    )
    print(f"  Wrote {key} ({len(body):,} bytes)")


# ---------------------------------------------------------------------------
# Date helpers
# ---------------------------------------------------------------------------

def _today() -> pd.Timestamp:
    return pd.Timestamp.now(tz='UTC').normalize().tz_localize(None)


def _window_start(days: int) -> pd.Timestamp:
    return _today() - pd.Timedelta(days=days)


def _find_nearest(series: pd.Series, target: pd.Timestamp) -> pd.Timestamp:
    """Return the value in series closest to target (always <= target)."""
    candidates = series[series <= target]
    if candidates.empty:
        return series.min()
    return candidates.max()


def _quarter_start(ref: pd.Timestamp, quarters_back: int) -> pd.Timestamp:
    """Return the first day of the quarter that is `quarters_back` quarters before ref."""
    q = (ref.month - 1) // 3 - quarters_back
    year = ref.year + q // 4
    q = q % 4
    return pd.Timestamp(year=year, month=q * 3 + 1, day=1)


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------

def load_all(today: pd.Timestamp) -> dict:
    """
    Load all source parquets once and return as a dict.
    Column pruning reduces memory — only load what each output needs.
    """
    print("Loading gold parquets...")

    perf = _load_parquet(
        'gold/client_performance.parquet',
        columns=['date', 'relationship_id',
                 'total_aua', 'aua_taxable', 'aua_tax_deferred', 'aua_tax_exempt',
                 'cum_inflows', 'cum_outflows', 'nna',
                 'num_accounts', 'num_positions', 'pct_priced'],
    )
    perf['date'] = pd.to_datetime(perf['date'])

    adv = _load_parquet(
        'gold/views/nna_aua_by_advisor.parquet',
        columns=['date', 'architect',
                 'total_aua', 'aua_taxable', 'aua_tax_deferred', 'aua_tax_exempt',
                 'cum_inflows', 'cum_outflows', 'nna',
                 'num_relationships', 'num_accounts'],
    )
    adv['date'] = pd.to_datetime(adv['date'])

    geo = _load_parquet(
        'gold/views/nna_aua_by_geography.parquet',
        columns=['date', 'state', 'country',
                 'total_aua', 'cum_inflows', 'cum_outflows', 'nna',
                 'num_relationships', 'num_accounts'],
    )
    geo['date'] = pd.to_datetime(geo['date'])

    cdim = _load_parquet(
        'gold/client_dimension.parquet',
        columns=['relationship_id', 'relationship_name', 'first_seen_date',
                 'primary_architect', 'primary_implementor',
                 'primary_city', 'primary_state', 'primary_country',
                 'total_accounts', 'active_accounts',
                 'has_taxable', 'has_tax_deferred', 'has_tax_exempt'],
    )
    cdim['first_seen_date'] = pd.to_datetime(cdim['first_seen_date'])

    adim = _load_parquet(
        'gold/accounts_dimension_latest.parquet',
        columns=['account_id', 'relationship_id', 'account_name',
                 'architect', 'implementor', 'local_relationship',
                 'tax_status', 'qualified_flag',
                 'client_state', 'client_country',
                 'account_type', 'account_is_open'],
    )

    tax = _load_parquet(
        'gold/views/client_tax_liability.parquet',
        columns=['relationship_id', 'account_id',
                 'tax_status', 'qualified_flag',
                 'asset_name', 'ticker',
                 'purchase_year',
                 'total_units', 'total_cost_basis', 'total_market_value', 'total_accrued_gain',
                 'short_term_cost_basis', 'short_term_market_value', 'short_term_gain',
                 'long_term_cost_basis', 'long_term_market_value', 'long_term_gain',
                 'num_open_lots'],
    )

    # City-level geography for geo_drill in timeseries_chart.json
    # Optional: gracefully handle case where the file doesn't exist yet
    try:
        geo_city = _load_parquet(
            'gold/views/nna_aua_by_geography_city.parquet',
            columns=['date', 'state', 'city', 'total_aua',
                     'cum_inflows', 'cum_outflows', 'nna',
                     'num_relationships'],
        )
        geo_city['date'] = pd.to_datetime(geo_city['date'])
    except Exception as e:
        print(f"  WARN: nna_aua_by_geography_city.parquet not available ({e}) -- geo_drill skipped")
        geo_city = None

    gc.collect()

    return dict(perf=perf, adv=adv, geo=geo, geo_city=geo_city,
                cdim=cdim, adim=adim, tax=tax)


# ---------------------------------------------------------------------------
# Y3: Asset class AUA mix from holdings_lots snapshots
# ---------------------------------------------------------------------------

def _build_aua_mix(today: pd.Timestamp) -> list:
    """
    Load monthly holdings_lots snapshots, classify each lot by asset_name,
    and aggregate market_value by asset class per month.

    Returns list of {period, segments: [{label, value}, ...]}.
    """
    prefix = 'gold/holdings_lots/'
    # List available snapshot dates
    paginator = s3.get_paginator('list_objects_v2')
    snapshot_keys = []
    for page in paginator.paginate(Bucket=INPUT_BUCKET, Prefix=prefix):
        for obj in page.get('Contents', []):
            key = obj['Key']
            fname = key.split('/')[-1]
            # Only daily snapshots (YYYY-MM-DD.parquet), skip backfill files
            if fname.endswith('.parquet') and not fname.startswith('backfill'):
                try:
                    d = pd.Timestamp(fname.replace('.parquet', ''))
                    snapshot_keys.append((d, key))
                except Exception:
                    continue

    if not snapshot_keys:
        print("  WARN: no holdings_lots snapshots found -- aua_mix skipped")
        return []

    snapshot_keys.sort(key=lambda x: x[0])

    # Pick last snapshot per month
    monthly_picks = {}
    for d, key in snapshot_keys:
        ym = d.to_period('M')
        monthly_picks[ym] = (d, key)

    # Also compute quarterly and yearly aggregates from monthly data
    aua_mix_data = []
    monthly_class_totals = {}  # ym -> {class: value}

    for ym in sorted(monthly_picks.keys()):
        snap_date, snap_key = monthly_picks[ym]
        try:
            df = _load_parquet(snap_key, columns=['asset_name', 'market_value', 'is_open'])
            df = df[df['is_open'] == True]
            df['asset_class'] = df['asset_name'].apply(_classify_asset)
            class_agg = df.groupby('asset_class')['market_value'].sum()

            segments = []
            for cls_key in ASSET_CLASS_LABELS:
                val = float(class_agg.get(cls_key, 0.0))
                segments.append({
                    'label': ASSET_CLASS_LABELS[cls_key],
                    'value': round(val, 2),
                })
            aua_mix_data.append({'period': str(ym), 'segments': segments})
            monthly_class_totals[ym] = {cls_key: float(class_agg.get(cls_key, 0.0))
                                        for cls_key in ASSET_CLASS_LABELS}
        except Exception as e:
            print(f"  WARN: failed to load holdings_lots {snap_key}: {e}")
            continue

    print(f"  aua_mix: {len(aua_mix_data)} monthly snapshots loaded")
    return aua_mix_data


# ---------------------------------------------------------------------------
# 1. timeseries_chart.json  (CumulativeChartResponse)
# ---------------------------------------------------------------------------

def build_timeseries_chart(perf: pd.DataFrame, adv: pd.DataFrame, geo: pd.DataFrame,
                            cdim: pd.DataFrame, today: pd.Timestamp,
                            geo_city: pd.DataFrame = None) -> dict:
    """
    4+1 views, daily data points:
      aua           -- cumulative NMNC vs NMEC stacked
      nna           -- cumulative firm-level NNA
      geo           -- cumulative AUA by top states (stacked)
      adv           -- cumulative AUA by top architects (stacked)
      geo_drill     -- per-state city-level AUA timeseries (optional)
      adv_drill     -- per-architect per-client AUA timeseries (ADVI-004 A1)
      cla           -- NMNC/NMEC AUM at total/geo_drill/adv_drill/geo_city_drill grains (ADVI-004 A2)
    """
    print("Building timeseries_chart.json...")

    # ---- Metadata: new_clients per window ----
    new_clients_meta = {}
    for label, days in WINDOWS.items():
        cutoff = today - pd.Timedelta(days=days)
        new_clients_meta[label] = int((cdim['first_seen_date'] >= cutoff).sum())

    # ---- AUA view (New Clients / Existing Clients) ----
    # Use actual total_aua (market-valued) per relationship, classified by
    # client vintage.  A "New Client" is any relationship whose first_seen_date
    # is within trailing 12 months of the row date; everything else is
    # "Existing Client".  The stacked total ties exactly to firm-level AUA.
    # Extended merge: pulls first_seen_date for cohort classification plus
    # dimensional attributes needed for adv_drill and CLA sub-views.
    perf_cohort = perf[['date', 'relationship_id', 'total_aua']].merge(
        cdim[['relationship_id', 'relationship_name', 'first_seen_date',
              'primary_architect', 'primary_state', 'primary_city']],
        on='relationship_id', how='left',
    )
    perf_cohort['months_since_first'] = (
        (perf_cohort['date'] - perf_cohort['first_seen_date']).dt.days / 30.44
    )
    perf_cohort['cohort'] = np.where(
        perf_cohort['months_since_first'] <= 12,
        'NMNC',   # New Money New Clients (within trailing 12mo)
        'NMEC',   # New Money Existing Clients (older than 12mo)
    )

    daily_cohort = (
        perf_cohort
        .groupby(['date', 'cohort'])['total_aua']
        .sum()
        .unstack(fill_value=0)
        .sort_index()
        .reset_index()
    )
    # Ensure both columns exist even if one cohort is empty
    for col in ['NMNC', 'NMEC']:
        if col not in daily_cohort.columns:
            daily_cohort[col] = 0.0

    aua_data = [
        {'date': r['date'].strftime('%Y-%m-%d'),
         'NMNC': round(float(r['NMNC']), 2),
         'NMEC': round(float(r['NMEC']), 2)}
        for _, r in daily_cohort.iterrows()
    ]

    # ---- NNA view (cumulative firm-level NNA + inflows/outflows) ----
    # All three columns are cumulative from inception.
    # The frontend diffs adjacent period endpoints to get period-level flows:
    #   period_inflows  = last(Inflows)  - first(Inflows)
    #   period_outflows = last(Outflows) - first(Outflows)
    #   period_nna      = last(NNA)      - first(NNA)
    daily_nna = (
        perf.groupby('date')[['nna', 'cum_inflows', 'cum_outflows']].sum()
        .sort_index()
        .reset_index()
    )
    nna_data = [
        {
            'date':     r['date'].strftime('%Y-%m-%d'),
            'NNA':      round(float(r['nna']), 2),
            'Inflows':  round(float(r['cum_inflows']), 2),
            'Outflows': round(float(r['cum_outflows']), 2),
        }
        for _, r in daily_nna.iterrows()
    ]

    # ---- ADV view (AUA by architect, stacked) ----
    # Pick top N architects by AUA on latest date
    latest_date_adv = adv['date'].max()
    latest_adv = adv[adv['date'] == latest_date_adv]
    top_architects = (
        latest_adv.nlargest(TOP_N_ADV, 'total_aua')['architect'].tolist()
    )

    adv_pivot = adv.copy()
    adv_pivot['_arch'] = adv_pivot['architect'].where(
        adv_pivot['architect'].isin(top_architects), 'Other'
    )
    adv_by_date = (
        adv_pivot.groupby(['date', '_arch'])['total_aua']
        .sum()
        .unstack(fill_value=0)
        .sort_index()
        .reset_index()
    )
    adv_categories = [a for a in top_architects if a in adv_by_date.columns] + (
        ['Other'] if 'Other' in adv_by_date.columns else []
    )
    adv_data = []
    for _, row in adv_by_date.iterrows():
        point = {'date': row['date'].strftime('%Y-%m-%d')}
        for cat in adv_categories:
            point[cat] = round(float(row.get(cat, 0)), 2)
        adv_data.append(point)

    # ---- GEO view (AUA by state, stacked) ----
    # US-only, top N states by AUA on latest date
    geo_us = geo[geo['country'].isin(['USA', 'US', '']) | geo['country'].isna()].copy()
    latest_date_geo = geo_us['date'].max()
    latest_geo = geo_us[geo_us['date'] == latest_date_geo]
    top_states = (
        latest_geo[latest_geo['state'].notna() & (latest_geo['state'] != '') &
                   (latest_geo['state'] != 'Unknown')]
        .nlargest(TOP_N_GEO, 'total_aua')['state'].tolist()
    )

    geo_pivot = geo_us.copy()
    geo_pivot['_state'] = geo_pivot['state'].where(
        geo_pivot['state'].isin(top_states), 'Other'
    )
    geo_by_date = (
        geo_pivot.groupby(['date', '_state'])['total_aua']
        .sum()
        .unstack(fill_value=0)
        .sort_index()
        .reset_index()
    )
    geo_categories = [s for s in top_states if s in geo_by_date.columns] + (
        ['Other'] if 'Other' in geo_by_date.columns else []
    )
    geo_data = []
    for _, row in geo_by_date.iterrows():
        point = {'date': row['date'].strftime('%Y-%m-%d')}
        for cat in geo_categories:
            point[cat] = round(float(row.get(cat, 0)), 2)
        geo_data.append(point)

    # ---- GEO DRILL view (city-level AUA per top state) ----
    MAX_DRILL_CITIES = 9
    geo_drill = {}
    if geo_city is not None and not geo_city.empty:
        # Only drill into the top states that appear in geo_categories (excl "Other")
        drill_states = [s for s in top_states if s != 'Other']
        latest_date_city = geo_city['date'].max()

        for state in drill_states:
            state_city = geo_city[geo_city['state'] == state].copy()
            if state_city.empty:
                continue

            # Rank cities by AUA on latest date, keep top N
            latest_city = state_city[state_city['date'] == latest_date_city]
            top_cities = (
                latest_city.nlargest(MAX_DRILL_CITIES, 'total_aua')['city'].tolist()
            )

            # Bucket the rest as "Other"
            state_city['_city'] = state_city['city'].where(
                state_city['city'].isin(top_cities), 'Other'
            )
            city_by_date = (
                state_city.groupby(['date', '_city'])['total_aua']
                .sum()
                .unstack(fill_value=0)
                .sort_index()
                .reset_index()
            )
            city_categories = [c for c in top_cities if c in city_by_date.columns] + (
                ['Other'] if 'Other' in city_by_date.columns else []
            )
            city_data = []
            for _, row in city_by_date.iterrows():
                point = {'date': row['date'].strftime('%Y-%m-%d')}
                for cat in city_categories:
                    point[cat] = round(float(row.get(cat, 0)), 2)
                city_data.append(point)

            geo_drill[state] = {
                'categories': city_categories,
                'data': city_data,
            }

        print(f"  geo_drill: {len(geo_drill)} states with city drill-down")
    else:
        print("  geo_drill: skipped (no city data)")

    # ---- ADV DRILL (per-architect -> per-client AUA timeseries) ---- A1
    # Keys must match adv.categories exactly (architect display names).
    # Category string per client: "{relationship_name} ({relationship_id})"
    # to prevent collision if two clients share a name.
    def _client_cat_key(rid, name):
        clean = str(name).strip() if pd.notna(name) and str(name).strip() else ''
        return f"{clean} ({rid})" if clean else str(rid)

    adv_drill = {}
    drill_archs = [a for a in adv_categories if a != 'Other']
    for arch in drill_archs:
        arch_perf = perf_cohort[perf_cohort['primary_architect'] == arch].copy()
        if arch_perf.empty:
            continue

        # Top N clients by latest-date AUA
        latest_dt_arch = arch_perf['date'].max()
        top_clients = (
            arch_perf[arch_perf['date'] == latest_dt_arch]
            .nlargest(TOP_N_CLIENTS_PER_ARCH, 'total_aua')
            [['relationship_id', 'relationship_name']]
        )
        cat_key_map = {
            row['relationship_id']: _client_cat_key(row['relationship_id'], row['relationship_name'])
            for _, row in top_clients.iterrows()
        }
        top_ids = set(cat_key_map)

        arch_perf['_cat'] = arch_perf['relationship_id'].apply(
            lambda rid: cat_key_map.get(rid, 'Other')
        )
        arch_pivot = (
            arch_perf.groupby(['date', '_cat'])['total_aua']
            .sum()
            .unstack(fill_value=0)
            .sort_index()
            .reset_index()
        )
        # Preserve top-client order; append Other if present
        arch_categories = [
            cat_key_map[rid] for rid in top_clients['relationship_id']
            if cat_key_map[rid] in arch_pivot.columns
        ]
        if 'Other' in arch_pivot.columns:
            arch_categories.append('Other')

        arch_data = []
        for _, row in arch_pivot.iterrows():
            point = {'date': row['date'].strftime('%Y-%m-%d')}
            for cat in arch_categories:
                point[cat] = round(float(row.get(cat, 0)), 2)
            arch_data.append(point)

        adv_drill[arch] = {
            'description': f'Per-client AUA for architect {arch}',
            'categories': arch_categories,
            'data': arch_data,
        }
    print(f"  adv_drill: {len(adv_drill)} architects with client drill-down")

    # ---- CLA (Client Lifecycle Analysis: NMNC/NMEC AUA timeseries) ---- A2
    # NMNC/NMEC rule: same trailing-12-month vintage classification as aua view
    # (perf_cohort.cohort already computed above from months_since_first).
    # Produces: total, geo_drill, adv_drill, geo_city_drill sub-views.

    def _cla_view(df_subset):
        """Build a CumulativeChartView {categories, data} for NMNC/NMEC over time."""
        daily = (
            df_subset.groupby(['date', 'cohort'])['total_aua']
            .sum()
            .unstack(fill_value=0)
            .sort_index()
            .reset_index()
        )
        for col in ('NMNC', 'NMEC'):
            if col not in daily.columns:
                daily[col] = 0.0
        return {
            'categories': ['NMNC', 'NMEC'],
            'data': [
                {'date': r['date'].strftime('%Y-%m-%d'),
                 'NMNC': round(float(r['NMNC']), 2),
                 'NMEC': round(float(r['NMEC']), 2)}
                for _, r in daily.iterrows()
            ],
        }

    # cla.total: firm-wide NMNC/NMEC AUA (same source as aua view)
    cla_total = _cla_view(perf_cohort)
    cla_total['description'] = 'Firm-wide AUM by client vintage (NMNC=new <=12mo, NMEC=existing >12mo)'

    # cla.geo_drill[state]: per-state NMNC/NMEC AUA; keys match geo.categories
    drill_states_cla = [s for s in top_states if s != 'Other']
    cla_geo_drill = {}
    for state in drill_states_cla:
        state_rows = perf_cohort[perf_cohort['primary_state'] == state]
        if state_rows.empty:
            continue
        view = _cla_view(state_rows)
        view['description'] = f'AUM by client vintage for state {state}'
        cla_geo_drill[state] = view

    # cla.adv_drill[arch]: per-architect NMNC/NMEC AUA; keys match adv.categories
    cla_adv_drill = {}
    for arch in drill_archs:
        arch_rows = perf_cohort[perf_cohort['primary_architect'] == arch]
        if arch_rows.empty:
            continue
        view = _cla_view(arch_rows)
        view['description'] = f'AUM by client vintage for architect {arch}'
        cla_adv_drill[arch] = view

    # cla.geo_city_drill[state][city]: uses cdim.primary_city (CTO A2 correction)
    # State keys match geo.categories; city keys are city display names.
    cla_geo_city_drill = {}
    for state in drill_states_cla:
        state_rows = perf_cohort[
            (perf_cohort['primary_state'] == state) &
            perf_cohort['primary_city'].notna() &
            (perf_cohort['primary_city'] != '')
        ]
        if state_rows.empty:
            continue

        # Top cities by latest-date AUA for this state
        latest_dt_state = state_rows['date'].max()
        top_cities = (
            state_rows[state_rows['date'] == latest_dt_state]
            .groupby('primary_city')['total_aua'].sum()
            .nlargest(MAX_CLA_CITIES)
            .index.tolist()
        )
        if not top_cities:
            continue

        cla_geo_city_drill[state] = {}
        for city in top_cities:
            city_rows = state_rows[state_rows['primary_city'] == city]
            if city_rows.empty:
                continue
            view = _cla_view(city_rows)
            view['description'] = f'AUM by client vintage for {city}, {state}'
            cla_geo_city_drill[state][city] = view

        if not cla_geo_city_drill[state]:
            del cla_geo_city_drill[state]

    print(f"  cla: {len(cla_geo_drill)} state drill, {len(cla_adv_drill)} arch drill, "
          f"{len(cla_geo_city_drill)} state city-drill")

    # ---- Y5: Growth decomposition (monthly granularity) ----
    # market(month) = aua_end - aua_start - nna_net
    # total(month)  = aua_end - aua_start = market + nna
    daily_firm = (
        perf.groupby('date')[['total_aua', 'nna']].sum()
        .sort_index()
        .reset_index()
    )
    daily_firm['year_month'] = daily_firm['date'].dt.to_period('M')
    growth_data = []
    for ym, grp in daily_firm.groupby('year_month'):
        grp_sorted = grp.sort_values('date')
        aua_start = float(grp_sorted.iloc[0]['total_aua'])
        aua_end   = float(grp_sorted.iloc[-1]['total_aua'])
        nna_start = float(grp_sorted.iloc[0]['nna'])
        nna_end   = float(grp_sorted.iloc[-1]['nna'])
        nna_net   = nna_end - nna_start
        total_chg = aua_end - aua_start
        market    = total_chg - nna_net
        growth_data.append({
            'period': str(ym),
            'market': round(market, 2),
            'nna':    round(nna_net, 2),
            'total':  round(total_chg, 2),
        })
    print(f"  growth_decomposition: {len(growth_data)} monthly periods")

    # ---- Y9: NNA at drill levels (cumulative per-category per-date) ----
    # nna_geo: per-state cumulative NNA, inflows, outflows
    geo_us_nna = geo[geo['country'].isin(['USA', 'US', '']) | geo['country'].isna()].copy()
    geo_us_nna = geo_us_nna[geo_us_nna['state'].notna() & (geo_us_nna['state'] != '')]
    geo_nna_pivot = geo_us_nna.copy()
    geo_nna_pivot['_state'] = geo_nna_pivot['state'].where(
        geo_nna_pivot['state'].isin(top_states), 'Other'
    )
    geo_nna_agg = (
        geo_nna_pivot.groupby(['date', '_state'])[['nna', 'cum_inflows', 'cum_outflows']]
        .sum()
        .sort_index()
        .reset_index()
    )
    nna_geo_data = []
    for dt, dt_grp in geo_nna_agg.groupby('date'):
        point = {'date': dt.strftime('%Y-%m-%d')}
        for _, row in dt_grp.iterrows():
            st = row['_state']
            point[st]              = round(float(row['nna']), 2)
            point[f'{st}_inflow']  = round(float(row['cum_inflows']), 2)
            point[f'{st}_outflow'] = round(float(row['cum_outflows']), 2)
        nna_geo_data.append(point)

    # nna_adv: per-architect cumulative NNA, inflows, outflows
    adv_nna_pivot = adv.copy()
    adv_nna_pivot['_arch'] = adv_nna_pivot['architect'].where(
        adv_nna_pivot['architect'].isin(top_architects), 'Other'
    )
    adv_nna_agg = (
        adv_nna_pivot.groupby(['date', '_arch'])[['nna', 'cum_inflows', 'cum_outflows']]
        .sum()
        .sort_index()
        .reset_index()
    )
    nna_adv_data = []
    for dt, dt_grp in adv_nna_agg.groupby('date'):
        point = {'date': dt.strftime('%Y-%m-%d')}
        for _, row in dt_grp.iterrows():
            arch = row['_arch']
            point[arch]                = round(float(row['nna']), 2)
            point[f'{arch}_inflow']    = round(float(row['cum_inflows']), 2)
            point[f'{arch}_outflow']   = round(float(row['cum_outflows']), 2)
        nna_adv_data.append(point)

    # nna_geo_drill: per-city cumulative NNA, inflows, outflows within top states
    nna_geo_drill = {}
    if geo_city is not None and not geo_city.empty:
        drill_states_nna = [s for s in top_states if s != 'Other']
        for state in drill_states_nna:
            state_city_nna = geo_city[geo_city['state'] == state].copy()
            if state_city_nna.empty:
                continue
            latest_city_nna = state_city_nna[state_city_nna['date'] == state_city_nna['date'].max()]
            top_cities_nna = latest_city_nna.nlargest(MAX_DRILL_CITIES, 'total_aua')['city'].tolist()
            state_city_nna['_city'] = state_city_nna['city'].where(
                state_city_nna['city'].isin(top_cities_nna), 'Other'
            )
            city_nna_agg = (
                state_city_nna.groupby(['date', '_city'])[['nna', 'cum_inflows', 'cum_outflows']]
                .sum()
                .sort_index()
                .reset_index()
            )
            city_cats = [c for c in top_cities_nna if c in city_nna_agg['_city'].unique()]
            if 'Other' in city_nna_agg['_city'].unique():
                city_cats.append('Other')
            city_nna_data = []
            for dt, dt_grp in city_nna_agg.groupby('date'):
                point = {'date': dt.strftime('%Y-%m-%d')}
                for _, row in dt_grp.iterrows():
                    city = row['_city']
                    point[city]                = round(float(row['nna']), 2)
                    point[f'{city}_inflow']    = round(float(row['cum_inflows']), 2)
                    point[f'{city}_outflow']   = round(float(row['cum_outflows']), 2)
                city_nna_data.append(point)
            nna_geo_drill[state] = {
                'categories': city_cats,
                'data': city_nna_data,
            }

    print(f"  nna_geo: {len(nna_geo_data)} days, nna_adv: {len(nna_adv_data)} days"
          + (f", nna_geo_drill: {len(nna_geo_drill)} states" if nna_geo_drill else ""))

    # ---- Y3: Asset class AUA mix from holdings_lots ----
    aua_mix_data = _build_aua_mix(today)

    # ---- Assemble response ----
    all_dates = perf['date'].sort_values()
    date_start = all_dates.min().strftime('%Y-%m-%d')
    date_end   = all_dates.max().strftime('%Y-%m-%d')
    days_total = int((all_dates.max() - all_dates.min()).days)

    result = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of':   date_end,
        'firm_id':      FIRM_ID,
        'date_range': {'start': date_start, 'end': date_end, 'days': days_total},
        'metadata': {'new_clients': new_clients_meta},
        'aua': {
            'description': 'Total AUA by client vintage (NMNC=new <=12mo, NMEC=existing >12mo)',
            'categories': ['NMNC', 'NMEC'],
            'data': aua_data,
        },
        'nna': {
            'description': 'Cumulative firm-level net new assets, inflows, and outflows',
            'categories': ['NNA', 'Inflows', 'Outflows'],
            'data': nna_data,
        },
        'adv': {
            'description': 'Cumulative AUA by architect',
            'categories': adv_categories,
            'data': adv_data,
        },
        'geo': {
            'description': 'Cumulative AUA by US state',
            'categories': geo_categories,
            'data': geo_data,
        },
        'growth_decomposition': {
            'description': 'Monthly AUA change decomposed into market appreciation and NNA',
            'data': growth_data,
        },
        'nna_geo': {
            'description': 'Cumulative NNA, inflows, outflows by US state',
            'categories': geo_categories,
            'data': nna_geo_data,
        },
        'nna_adv': {
            'description': 'Cumulative NNA, inflows, outflows by architect',
            'categories': adv_categories,
            'data': nna_adv_data,
        },
    }

    # Only add geo_drill when populated (avoids empty key in JSON)
    if geo_drill:
        result['geo_drill'] = geo_drill

    # Y9: NNA geo drill (per-city NNA with inflow/outflow within top states)
    if nna_geo_drill:
        result['nna_geo_drill'] = nna_geo_drill

    # adv_drill: per-architect per-client AUA drill (ADVI-004 A1)
    if adv_drill:
        result['adv_drill'] = adv_drill

    # Y3: asset class AUA mix (monthly snapshots from holdings_lots)
    if aua_mix_data:
        result['aua_mix'] = {
            'description': 'AUA breakdown by asset class (monthly from holdings snapshots)',
            'categories': list(ASSET_CLASS_LABELS.values()),
            'data': aua_mix_data,
        }

    # cla: NMNC/NMEC timeseries at total/geo_drill/adv_drill/geo_city_drill (ADVI-004 A2)
    cla = {
        'total':     cla_total,
        'geo_drill': cla_geo_drill,
        'adv_drill': cla_adv_drill,
    }
    if cla_geo_city_drill:
        cla['geo_city_drill'] = cla_geo_city_drill
    result['cla'] = cla

    print(f"  timeseries_chart: {len(aua_data)} days, {len(adv_categories)} architects, "
          f"{len(geo_categories)} states"
          + (f", {len(geo_drill)} state drill-downs" if geo_drill else "")
          + (f", {len(adv_drill)} arch client-drills" if adv_drill else "")
          + (f", cla({len(cla_geo_drill)}geo/{len(cla_adv_drill)}adv"
             + (f"/{len(cla_geo_city_drill)}citygeo" if cla_geo_city_drill else "") + ")")
          + (f", aua_mix: {len(aua_mix_data)} months" if aua_mix_data else ""))
    return result


# ---------------------------------------------------------------------------
# 2. Leaderboard helpers
# ---------------------------------------------------------------------------

def _leaderboard_entries(df_by_date: pd.DataFrame, dim_col: str,
                          cdim: pd.DataFrame, architect_col: str,
                          window_start: pd.Timestamp) -> list:
    """
    Build ranked LeaderboardEntry list for one time window.

    df_by_date: daily timeseries (adv or account-performance-based) with
                date, {dim_col}, total_aua, nna columns
    architect_col: column in cdim that maps to dim_col (e.g. 'primary_architect')
    window_start: start of the window (either rolling or calendar QTD/YTD)
    """
    all_dates = df_by_date['date'].sort_values().unique()
    latest_date = all_dates.max()

    # Find the date in the data closest to window_start (looking back)
    past_dates = all_dates[all_dates <= window_start]
    start_date  = past_dates.max() if len(past_dates) > 0 else all_dates.min()

    end_snapshot   = df_by_date[df_by_date['date'] == latest_date].set_index(dim_col)
    start_snapshot = df_by_date[df_by_date['date'] == start_date].set_index(dim_col)

    entries = []
    for dim_val, end_row in end_snapshot.iterrows():
        if not dim_val or str(dim_val).strip() in ('', 'nan', 'None'):
            continue

        total_aua   = float(end_row.get('total_aua', 0) or 0)
        client_count = int(end_row.get('num_relationships', 0) or 0)
        account_count = int(end_row.get('num_accounts', 0) or 0)

        # NNA over window = nna_end - nna_start (cumulative from inception)
        start_row = start_snapshot.loc[dim_val] if dim_val in start_snapshot.index else None
        nna_end   = float(end_row.get('nna', 0) or 0)
        nna_start = float(start_row.get('nna', 0) or 0) if start_row is not None else 0.0
        nna_window = nna_end - nna_start

        # AUA growth % over window
        aua_start = float(start_row.get('total_aua', 0) or 0) if start_row is not None else 0.0
        aua_growth_pct = (
            (total_aua - aua_start) / aua_start * 100
            if aua_start > 0 else 0.0
        )

        # New clients in window (first_seen_date in window AND matching advisor)
        if architect_col in cdim.columns:
            matching = cdim[cdim[architect_col] == dim_val]
        else:
            matching = pd.DataFrame()
        new_clients = int(
            (matching['first_seen_date'] >= window_start).sum()
        ) if not matching.empty else 0

        entries.append({
            'name':            str(dim_val),
            'nna':             round(nna_window, 2),
            'aua_growth_pct':  round(aua_growth_pct, 2),
            'new_clients':     new_clients,
            'total_aua':       round(total_aua, 2),
            'client_count':    client_count,
            'account_count':   account_count,
        })

    # Rank by NNA descending
    entries.sort(key=lambda x: x['nna'], reverse=True)
    for i, e in enumerate(entries):
        e['rank'] = i + 1

    return entries


def _leaderboard_window_data(entries: list) -> dict:
    total_nna = sum(e['nna'] for e in entries)
    total_aua = sum(e['total_aua'] for e in entries)
    return {
        'entry_count': len(entries),
        'summary': {
            'total_nna':            round(total_nna, 2),
            'total_aua':            round(total_aua, 2),
            'total_new_clients':    sum(e['new_clients'] for e in entries),
            'positive_nna_count':   sum(1 for e in entries if e['nna'] >= 0),
            'negative_nna_count':   sum(1 for e in entries if e['nna'] < 0),
        },
        'entries': entries,
    }


def build_architect_leaderboard(adv: pd.DataFrame, cdim: pd.DataFrame,
                                 today: pd.Timestamp) -> dict:
    print("Building architect_leaderboard.json...")

    windows_data = {}
    # Rolling trailing windows
    for label, days in WINDOWS.items():
        w_start = today - pd.Timedelta(days=days)
        entries = _leaderboard_entries(adv, 'architect', cdim, 'primary_architect', w_start)
        windows_data[label] = _leaderboard_window_data(entries)
        print(f"  Window {label}: {len(entries)} architects")
    # Calendar QTD window (Jan 1 / Apr 1 / Jul 1 / Oct 1)
    qtd_start = _quarter_start(today, 0)
    entries = _leaderboard_entries(adv, 'architect', cdim, 'primary_architect', qtd_start)
    windows_data['qtd'] = _leaderboard_window_data(entries)
    print(f"  Window qtd: {len(entries)} architects (calendar start={qtd_start.date()})")
    # Calendar YTD window (Jan 1 of current year)
    # In Q1 (Jan-Mar), qtd and ytd have identical start dates (both Jan 1)
    ytd_start = pd.Timestamp(year=today.year, month=1, day=1)
    entries = _leaderboard_entries(adv, 'architect', cdim, 'primary_architect', ytd_start)
    windows_data['ytd'] = _leaderboard_window_data(entries)
    print(f"  Window ytd: {len(entries)} architects (calendar start={ytd_start.date()})")

    latest_date = adv['date'].max()
    return {
        'generated_at':       datetime.now(timezone.utc).isoformat(),
        'data_as_of':         latest_date.strftime('%Y-%m-%d'),
        'firm_id':            FIRM_ID,
        'leaderboard_type':   'architect',
        'available_windows':  list(WINDOWS.keys()) + ['qtd', 'ytd'],
        'windows':            windows_data,
    }


# ---------------------------------------------------------------------------
# 3. clients_tab.json  (ClientsTabResponse + Yang tax fields)
# ---------------------------------------------------------------------------

def _build_tax_section(perf_latest: pd.DataFrame, tax: pd.DataFrame) -> dict:
    """Build the full tax section combining client_performance and client_tax_liability."""

    # AUA split from client_performance (position-based, all accounts)
    total_aua      = float(perf_latest['total_aua'].sum())
    aua_taxable    = float(perf_latest['aua_taxable'].sum())
    aua_deferred   = float(perf_latest['aua_tax_deferred'].sum())
    aua_exempt     = float(perf_latest['aua_tax_exempt'].sum())
    pct = lambda x: round(x / total_aua * 100, 1) if total_aua > 0 else 0.0

    # Qualified vs non-qualified from client_tax_liability (open lots only, snapshot date)
    tax_taxable = tax[tax['tax_status'] == 'taxable']
    tax_qual    = tax[tax['qualified_flag'] == True]
    tax_nonqual = tax[tax['qualified_flag'] == False]

    qual_mv    = float(tax_qual['total_market_value'].sum())
    nonqual_mv = float(tax_nonqual['total_market_value'].sum())
    lot_total  = qual_mv + nonqual_mv

    qual_pct   = round(qual_mv / lot_total * 100, 1) if lot_total > 0 else 0.0
    nonqual_pct = round(nonqual_mv / lot_total * 100, 1) if lot_total > 0 else 0.0

    # Account counts: unique accounts per qualified flag
    qual_acct_count    = int(tax_qual['account_id'].nunique())
    nonqual_acct_count = int(tax_nonqual['account_id'].nunique())

    # Non-qualified cost basis and gains (taxable positions only)
    nq_cost_basis     = float(tax_taxable['total_cost_basis'].sum())
    nq_market_value   = float(tax_taxable['total_market_value'].sum())
    nq_unrealized     = float(tax_taxable['total_accrued_gain'].sum())
    st_gain           = float(tax_taxable['short_term_gain'].sum())
    lt_gain           = float(tax_taxable['long_term_gain'].sum())

    # Cost basis by purchase year (taxable only)
    year_agg = (
        tax_taxable
        .groupby('purchase_year', dropna=False)
        .agg(
            cost_basis=('total_cost_basis', 'sum'),
            market_value=('total_market_value', 'sum'),
            unrealized_gain=('total_accrued_gain', 'sum'),
            short_term_gain=('short_term_gain', 'sum'),
            long_term_gain=('long_term_gain', 'sum'),
            num_positions=('asset_name', 'nunique'),
        )
        .reset_index()
        .sort_values('purchase_year')
    )
    cost_basis_by_year = [
        {
            'purchase_year':   int(r['purchase_year']) if pd.notna(r['purchase_year']) else None,
            'cost_basis':      round(float(r['cost_basis']), 2),
            'market_value':    round(float(r['market_value']), 2),
            'unrealized_gain': round(float(r['unrealized_gain']), 2),
            'short_term_gain': round(float(r['short_term_gain']), 2),
            'long_term_gain':  round(float(r['long_term_gain']), 2),
            'num_positions':   int(r['num_positions']),
        }
        for _, r in year_agg.iterrows()
    ]

    # Top gain positions (taxable, aggregated across purchase years per asset)
    pos_agg = (
        tax_taxable
        .groupby(['asset_name', 'ticker'], dropna=False)
        .agg(
            cost_basis=('total_cost_basis', 'sum'),
            market_value=('total_market_value', 'sum'),
            unrealized_gain=('total_accrued_gain', 'sum'),
            short_term_gain=('short_term_gain', 'sum'),
            long_term_gain=('long_term_gain', 'sum'),
            num_lots=('num_open_lots', 'sum'),
        )
        .reset_index()
        .nlargest(TOP_GAIN_POSITIONS, 'unrealized_gain')
    )
    top_gain_positions = [
        {
            'asset_name':      str(r['asset_name']),
            'ticker':          str(r['ticker']) if pd.notna(r['ticker']) else None,
            'cost_basis':      round(float(r['cost_basis']), 2),
            'market_value':    round(float(r['market_value']), 2),
            'unrealized_gain': round(float(r['unrealized_gain']), 2),
            'short_term_gain': round(float(r['short_term_gain']), 2),
            'long_term_gain':  round(float(r['long_term_gain']), 2),
            'num_lots':        int(r['num_lots']),
        }
        for _, r in pos_agg.iterrows()
    ]

    return {
        # Standard fields (from client_performance — position-based AUA)
        'taxable':          round(aua_taxable, 2),
        'taxable_pct':      pct(aua_taxable),
        'tax_deferred':     round(aua_deferred, 2),
        'tax_deferred_pct': pct(aua_deferred),
        'tax_free':         round(aua_exempt, 2),
        'tax_free_pct':     pct(aua_exempt),
        'capital_gains_ttm': round(nq_unrealized, 2),  # total unrealized gain on taxable positions

        # Yang's fields: qualified vs non-qualified split
        'qualified_aua':              round(qual_mv, 2),
        'qualified_pct':              qual_pct,
        'non_qualified_aua':          round(nonqual_mv, 2),
        'non_qualified_pct':          nonqual_pct,
        'qualified_account_count':    qual_acct_count,
        'non_qualified_account_count': nonqual_acct_count,

        # Yang's fields: non-qualified cost basis and gains (aggregated position grain)
        'non_qualified_cost_basis':      round(nq_cost_basis, 2),
        'non_qualified_market_value':    round(nq_market_value, 2),
        'non_qualified_unrealized_gain': round(nq_unrealized, 2),
        'short_term_gain':               round(st_gain, 2),
        'long_term_gain':                round(lt_gain, 2),

        # Yang's fields: by purchase year (aggregated position grain)
        'cost_basis_by_year': cost_basis_by_year,

        # Yang's fields: top positions by unrealized gain (aggregated position grain)
        'top_gain_positions': top_gain_positions,

        # Flag for client detail endpoint (lot-level detail available there)
        'lots_available': True,
    }


def build_clients_tab(perf: pd.DataFrame, cdim: pd.DataFrame,
                       adim: pd.DataFrame, tax: pd.DataFrame,
                       today: pd.Timestamp) -> dict:
    print("Building clients_tab.json...")

    latest_date = perf['date'].max()
    perf_latest = perf[perf['date'] == latest_date]

    # Headline
    total_aua     = float(perf_latest['total_aua'].sum())
    account_count = int(perf_latest['num_accounts'].sum())
    client_count  = int(perf_latest['relationship_id'].nunique())

    headline = {
        'total_aua':        round(total_aua, 2),
        'account_count':    account_count,
        'client_count':     client_count,
        'fee_rate_pct':     0.0,   # not available from BD data
        'income_yield_pct': 0.0,   # not available from BD data
    }

    # Tax section
    tax_section = _build_tax_section(perf_latest, tax)

    # Engagement: net_flows TTM
    ttm_cutoff = today - pd.Timedelta(days=365)
    past_dates  = perf['date'][perf['date'] <= ttm_cutoff]
    ttm_start   = past_dates.max() if not past_dates.empty else perf['date'].min()

    perf_ttm_start = perf[perf['date'] == ttm_start]
    inflows_now   = float(perf_latest['cum_inflows'].sum())
    outflows_now  = float(perf_latest['cum_outflows'].sum())
    inflows_then  = float(perf_ttm_start['cum_inflows'].sum())
    outflows_then = float(perf_ttm_start['cum_outflows'].sum())
    net_flows_ttm = (inflows_now - inflows_then) - (outflows_now - outflows_then)

    # Avg relationship tenure from client_dimension
    cdim_active = cdim[cdim['first_seen_date'].notna()]
    avg_tenure_years = 0.0
    if not cdim_active.empty:
        avg_days = (today - cdim_active['first_seen_date']).dt.days.mean()
        avg_tenure_years = round(float(avg_days) / 365.25, 2)

    # Active clients pct: clients with at least 1 account in latest positions
    active_rel_ids = set(perf_latest['relationship_id'].unique())
    all_rel_ids    = set(cdim['relationship_id'].unique())
    active_pct = round(len(active_rel_ids) / len(all_rel_ids) * 100, 1) if all_rel_ids else 0.0

    engagement = {
        'trading_buys_ttm':    0,      # computable from silver but not loaded here
        'trading_sells_ttm':   0,
        'net_flows_ttm':       round(net_flows_ttm, 2),
        'avg_relationship_years': avg_tenure_years,
        'active_clients_pct':  active_pct,
    }

    # Income & Fees: zeroed (not available from BD transaction data)
    income_fees = {
        'dividends_ttm':       0.0,
        'interest_ttm':        0.0,
        'total_income_ttm':    0.0,
        'income_yield_pct':    0.0,
        'management_fees_ttm': 0.0,
        'fee_rate_pct':        0.0,
    }

    # Portfolio: zeroed (asset class taxonomy not available)
    portfolio = {
        'allocation':               [],
        'weighted_expense_ratio':   0.0,
        'unique_holdings':          0,
        'top_5_concentration_pct':  0.0,
    }

    # Client dropdown list (sorted by AUA desc)
    client_list_df = (
        perf_latest[['relationship_id', 'total_aua']]
        .merge(cdim[['relationship_id', 'relationship_name']], on='relationship_id', how='left')
        .sort_values('total_aua', ascending=False)
    )
    clients = [
        {
            'key':  str(r['relationship_id']),
            'name': str(r['relationship_name']) if pd.notna(r['relationship_name'])
                    else str(r['relationship_id']),
            'aua':  round(float(r['total_aua']), 2),
        }
        for _, r in client_list_df.iterrows()
    ]

    print(f"  clients_tab: {client_count} clients, total_aua={total_aua:,.0f}")

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of':   latest_date.strftime('%Y-%m-%d'),
        'firm_id':      FIRM_ID,
        'headline':     headline,
        'tax':          tax_section,
        'income_fees':  income_fees,
        'portfolio':    portfolio,
        'engagement':   engagement,
        'clients':      clients,
    }


# ---------------------------------------------------------------------------
# 4. summary/header_metrics.json  (HeaderMetricsResponse)
# ---------------------------------------------------------------------------

def build_header_metrics(perf: pd.DataFrame, adv: pd.DataFrame,
                          cdim: pd.DataFrame, today: pd.Timestamp) -> dict:
    print("Building summary/header_metrics.json...")

    latest_date = perf['date'].max()
    perf_latest = perf[perf['date'] == latest_date]
    total_aua   = float(perf_latest['total_aua'].sum())

    def _nna_for_period(days: int) -> float:
        cutoff = today - pd.Timedelta(days=days)
        past   = perf['date'][perf['date'] <= cutoff]
        d_start = past.max() if not past.empty else perf['date'].min()
        start_rows = perf[perf['date'] == d_start]
        inf_end  = float(perf_latest['cum_inflows'].sum())
        out_end  = float(perf_latest['cum_outflows'].sum())
        inf_st   = float(start_rows['cum_inflows'].sum())
        out_st   = float(start_rows['cum_outflows'].sum())
        return (inf_end - inf_st) - (out_end - out_st)

    nna_12m = _nna_for_period(365)
    nna_ytd  = _nna_for_period((today - pd.Timestamp(today.year, 1, 1)).days)
    nna_qtd  = _nna_for_period((today - pd.Timestamp(today.year,
                                                       ((today.month - 1) // 3) * 3 + 1,
                                                       1)).days)
    nna_mtd  = _nna_for_period((today - pd.Timestamp(today.year, today.month, 1)).days)

    # Quarterly labels (q0=current quarter, q1=last quarter, etc.)
    def _quarter_label(ts: pd.Timestamp) -> str:
        q = (ts.month - 1) // 3 + 1
        return f"Q{q} '{str(ts.year)[2:]}"

    def _quarter_nna(quarters_back: int) -> dict:
        q_start  = _quarter_start(today, quarters_back)
        q_end    = _quarter_start(today, quarters_back - 1) - pd.Timedelta(days=1)
        prior_qe = q_start - pd.Timedelta(days=1)  # prior quarter-end (e.g. Sep 30) matches script 09
        nna_val = _nna_for_period((today - prior_qe).days) - (
            _nna_for_period((today - q_end).days) if quarters_back > 0 else 0
        )
        return {'nna': round(nna_val, 2), 'label': _quarter_label(q_start)}

    # Architect breakdown (top 10)
    adv_latest = adv[adv['date'] == adv['date'].max()]
    by_arch = []
    for _, row in adv_latest.nlargest(10, 'total_aua').iterrows():
        arch_aua = float(row['total_aua'])
        by_arch.append({
            'architect':     str(row['architect']),
            'aua':           round(arch_aua, 2),
            'aua_pct':       round(arch_aua / total_aua * 100, 1) if total_aua > 0 else 0.0,
            'client_count':  int(row['num_relationships']),
            'account_count': int(row['num_accounts']),
        })

    total = {
        'aua':                  round(total_aua, 2),
        'nna_mtd':              round(nna_mtd, 2),
        'nna_qtd':              round(nna_qtd, 2),
        'nna_ytd':              round(nna_ytd, 2),
        'nna_12m':              round(nna_12m, 2),
        'client_count':         int(perf_latest['relationship_id'].nunique()),
        'account_count':        int(perf_latest['num_accounts'].sum()),
        'new_client_count':     0,   # requires NMNC classification at position level
        'existing_client_count': 0,
        'new_client_aua':       0.0,
        'existing_client_aua':  0.0,
        'new_client_pct':       0.0,
        'q0': {'nna': round(nna_qtd, 2)},
        'q1': _quarter_nna(1),
        'q2': _quarter_nna(2),
        'q3': _quarter_nna(3),
    }

    print(f"  header_metrics: AUA={total_aua:,.0f}, NNA_12M={nna_12m:,.0f}")

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of':   latest_date.strftime('%Y-%m-%d'),
        'firm_id':      FIRM_ID,
        'firm_name':    FIRM_NAME,
        'total':        total,
        'by_architect': by_arch,
    }


# ---------------------------------------------------------------------------
# 5. partner_analytics/header_metrics.json  (PartnerAnalyticsResponse)
# ---------------------------------------------------------------------------

def build_partner_analytics(perf: pd.DataFrame, adv: pd.DataFrame,
                              geo: pd.DataFrame, cdim: pd.DataFrame,
                              today: pd.Timestamp) -> dict:
    """
    Produces PartnerAnalyticsResponse for the partner analytics tab.
    Current period only (no time machine quarters — can be added later).
    """
    print("Building partner_analytics/header_metrics.json...")

    latest_date  = perf['date'].max()
    perf_latest  = perf[perf['date'] == latest_date]
    total_aua    = float(perf_latest['total_aua'].sum())

    def _segment(key, label, aua, client_count, color) -> dict:
        return {
            'key': key, 'label': label,
            'aua': round(float(aua), 2),
            'aua_pct': round(float(aua) / total_aua * 100, 1) if total_aua > 0 else 0.0,
            'client_count': int(client_count),
            'color': color,
        }

    # AUA view: taxable / tax_deferred / tax_exempt
    aua_taxable  = float(perf_latest['aua_taxable'].sum())
    aua_deferred = float(perf_latest['aua_tax_deferred'].sum())
    aua_exempt   = float(perf_latest['aua_tax_exempt'].sum())

    # Client count per tax status (approximate from cdim)
    n_taxable  = int(cdim['has_taxable'].sum())
    n_deferred = int(cdim['has_tax_deferred'].sum())
    n_exempt   = int(cdim['has_tax_exempt'].sum())

    aua_segments = [
        _segment('taxable',      'Non-Qualified',  aua_taxable,  n_taxable,  '#EF4444'),
        _segment('tax_deferred', 'Tax-Deferred',   aua_deferred, n_deferred, '#F59E0B'),
        _segment('tax_free',     'Tax-Free (Roth)', aua_exempt,  n_exempt,   '#10B981'),
    ]

    # ADV view: by architect (top 8 + Other)
    adv_latest   = adv[adv['date'] == latest_date]
    top_arch     = adv_latest.nlargest(TOP_N_ADV, 'total_aua')
    other_aua    = total_aua - float(top_arch['total_aua'].sum())
    arch_colors  = ['#4CAF50', '#2196F3', '#F59E0B', '#EF4444',
                    '#8B5CF6', '#EC4899', '#14B8A6', '#F97316']
    adv_segments = [
        _segment(
            str(r['architect']).lower().replace(' ', '_'),
            str(r['architect']),
            r['total_aua'],
            r['num_relationships'],
            arch_colors[i % len(arch_colors)],
        )
        for i, (_, r) in enumerate(top_arch.iterrows())
    ]
    if other_aua > 0:
        adv_segments.append(_segment('other', 'Other', other_aua, 0, '#6B7280'))

    # GEO view: by state (top 8 + Other)
    geo_us       = geo[(geo['country'].isin(['USA', 'US', ''])) | geo['country'].isna()]
    geo_latest   = geo_us[geo_us['date'] == latest_date]
    top_states   = geo_latest.nlargest(TOP_N_GEO, 'total_aua')
    other_geo    = total_aua - float(top_states['total_aua'].sum())
    state_colors = arch_colors
    geo_segments = [
        _segment(
            str(r['state']).lower(),
            str(r['state']),
            r['total_aua'],
            r['num_relationships'],
            state_colors[i % len(state_colors)],
        )
        for i, (_, r) in enumerate(top_states.iterrows())
        if r['state'] not in ('Unknown', '', None)
    ]
    if other_geo > 0:
        geo_segments.append(_segment('other', 'Other', other_geo, 0, '#6B7280'))

    def _metrics(aua_val, client_count):
        return {
            'aua': round(float(aua_val), 2),
            'client_count': int(client_count),
        }

    def _donut(title, segments):
        return {
            'title': title,
            'total': round(sum(s['aua'] for s in segments), 2),
            'segments': segments,
        }

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of':   latest_date.strftime('%Y-%m-%d'),
        'firm_id':      FIRM_ID,
        'firm_name':    FIRM_NAME,
        'views': {
            'aua': {
                'current': {
                    'donut': _donut('AUA by Tax Status', aua_segments),
                    'metrics': _metrics(total_aua, int(cdim['relationship_id'].nunique())),
                }
            },
            'adv': {
                'current': {
                    'donut': _donut('AUA by Architect', adv_segments),
                    'metrics': _metrics(total_aua, int(cdim['relationship_id'].nunique())),
                }
            },
            'geo': {
                'current': {
                    'donut': _donut('AUA by Geography', geo_segments),
                    'metrics': _metrics(total_aua, int(cdim['relationship_id'].nunique())),
                }
            },
            'nna': {
                'current': {
                    'donut': _donut('AUA by Tax Status', aua_segments),  # fallback same as aua
                    'metrics': _metrics(total_aua, int(cdim['relationship_id'].nunique())),
                }
            },
        },
    }


# ---------------------------------------------------------------------------
# 6. filters/dimensions.json  (FiltersResponse)
# ---------------------------------------------------------------------------

def build_filters(adv: pd.DataFrame, adim: pd.DataFrame,
                   today: pd.Timestamp) -> dict:
    print("Building filters/dimensions.json...")

    latest_adv = adv[adv['date'] == adv['date'].max()]

    # AUA per architect from adv timeseries
    arch_aua = latest_adv.set_index('architect')['total_aua'].to_dict()

    def _dim_values(series: pd.Series, top_n=None, aua_map: dict = None) -> list:
        """Build filter value list from a string series."""
        counts = series.dropna().astype(str).str.strip()
        counts = counts[counts.str.lower().isin({'', 'nan', 'none', 'unassigned'}) == False]
        freq = counts.value_counts()
        if top_n:
            freq = freq.head(top_n)
        values = []
        for name, cnt in freq.items():
            v = {
                'id':   name.lower().replace(' ', '_').replace('&', 'and'),
                'name': name,
            }
            if aua_map and name in aua_map:
                v['aua']           = round(float(aua_map[name]), 2)
                v['client_count']  = int(cnt)
            values.append(v)
        return values

    # Build per-dimension AUA maps from accounts_dimension (static, latest)
    # We use adv timeseries for architect AUA; use adim counts for others
    # (no AUA per implementor/region/account_type from gold — use counts only)

    dimensions = {
        'architect': {
            'label': 'Architect',
            'column': 'architect',
            'values': _dim_values(adim['architect'], aua_map=arch_aua),
        },
        'region': {
            'label': 'Region',
            'column': 'local_ops',
            'values': _dim_values(adim['local_relationship']),
        },
        'implementor': {
            'label': 'Implementor',
            'column': 'implementor',
            'values': _dim_values(adim['implementor'], top_n=TOP_N_IMPLEMENTOR),
        },
        'account_type': {
            'label': 'Account Type',
            'column': 'account_owner_type',
            'values': _dim_values(adim['account_type']),
        },
        'tax_status': {
            'label': 'Tax Status',
            'column': 'tax_status',
            'values': _dim_values(adim['tax_status']),
        },
        'state': {
            'label': 'State',
            'column': 'client_state',
            'values': _dim_values(adim['client_state'], top_n=TOP_N_STATE),
        },
    }

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'firm_id':      FIRM_ID,
        'dimensions':   dimensions,
    }


# ---------------------------------------------------------------------------
# 7. Snapshots  (SnapshotResponse)
# ---------------------------------------------------------------------------

def _snapshot_response(dimension: str, rows: list, total_aua: float,
                        data_as_of: str) -> dict:
    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'data_as_of':   data_as_of,
        'firm_id':      FIRM_ID,
        'dimension':    dimension,
        'total_aua':    round(total_aua, 2),
        'data':         rows,
    }


def build_snapshots(perf: pd.DataFrame, adv: pd.DataFrame,
                     geo: pd.DataFrame, adim: pd.DataFrame) -> dict:
    """Returns dict of {output_key: response_dict} for each snapshot."""
    print("Building snapshot files...")

    latest_date  = adv['date'].max()
    perf_latest  = perf[perf['date'] == perf['date'].max()]
    adv_latest   = adv[adv['date'] == latest_date]
    geo_latest   = geo[geo['date'] == geo['date'].max()]
    total_aua    = float(perf_latest['total_aua'].sum())
    date_str     = latest_date.strftime('%Y-%m-%d')

    def _rows(df, val_col, aua_col, top_n=None, label_transform=None):
        agg = df.groupby(val_col)[aua_col].sum().sort_values(ascending=False)
        if top_n:
            agg = agg.head(top_n)
        total = float(agg.sum())
        rows = []
        for val, aua in agg.items():
            label = label_transform(val) if label_transform else str(val)
            if not label or label.lower() in ('nan', 'none', 'unknown', ''):
                continue
            rows.append({
                'value':         label,
                'aua':           round(float(aua), 2),
                'aua_pct':       round(float(aua) / total * 100, 1) if total > 0 else 0.0,
                'client_count':  0,  # populated below for architect
                'account_count': 0,
            })
        return rows

    # Architect snapshot (from adv timeseries — has num_relationships + num_accounts)
    arch_rows = []
    for _, row in adv_latest.sort_values('total_aua', ascending=False).iterrows():
        arch_aua = float(row['total_aua'])
        arch_rows.append({
            'value':         str(row['architect']),
            'aua':           round(arch_aua, 2),
            'aua_pct':       round(arch_aua / total_aua * 100, 1) if total_aua > 0 else 0.0,
            'client_count':  int(row['num_relationships']),
            'account_count': int(row['num_accounts']),
        })

    # Tax status snapshot (from client_performance aua columns)
    tax_map = {
        'taxable':     ('Non-Qualified',  float(perf_latest['aua_taxable'].sum())),
        'tax_deferred': ('Tax-Deferred',  float(perf_latest['aua_tax_deferred'].sum())),
        'tax_exempt':  ('Tax-Free (Roth)', float(perf_latest['aua_tax_exempt'].sum())),
    }
    tax_rows = [
        {'value': label, 'aua': round(aua, 2),
         'aua_pct': round(aua / total_aua * 100, 1) if total_aua > 0 else 0.0,
         'client_count': 0, 'account_count': 0}
        for _, (label, aua) in sorted(tax_map.items(), key=lambda x: -x[1][1])
    ]

    # State snapshot (from geo timeseries, US only)
    geo_us = geo_latest[
        (geo_latest['country'].isin(['USA', 'US', ''])) | geo_latest['country'].isna()
    ]
    state_agg = (
        geo_us.groupby('state')['total_aua']
        .sum()
        .sort_values(ascending=False)
        .head(TOP_N_STATE)
    )
    state_total = float(state_agg.sum())
    state_rows = [
        {'value': str(state), 'aua': round(float(aua), 2),
         'aua_pct': round(float(aua) / state_total * 100, 1) if state_total > 0 else 0.0,
         'client_count': 0, 'account_count': 0}
        for state, aua in state_agg.items()
        if str(state).lower() not in ('unknown', '', 'nan', 'none')
    ]

    # Region snapshot (from accounts_dimension local_relationship)
    region_agg = (
        adim.groupby('local_relationship')['account_id'].count()
        .sort_values(ascending=False)
    )
    region_rows = [
        {'value': str(region), 'aua': 0.0, 'aua_pct': 0.0,
         'client_count': 0, 'account_count': int(cnt)}
        for region, cnt in region_agg.items()
        if str(region).lower() not in ('', 'nan', 'none', 'unassigned')
    ]

    return {
        'gold/snapshots/aua_by_architect.json': _snapshot_response(
            'architect', arch_rows, total_aua, date_str),
        'gold/snapshots/aua_by_tax_status.json': _snapshot_response(
            'tax_status', tax_rows, total_aua, date_str),
        'gold/snapshots/aua_by_state.json': _snapshot_response(
            'state', state_rows, state_total, date_str),
        'gold/snapshots/aua_by_region.json': _snapshot_response(
            'region', region_rows, 0.0, date_str),
    }


# ---------------------------------------------------------------------------
# Lambda handler
# ---------------------------------------------------------------------------

def lambda_handler(event, context):
    print("=" * 70)
    print("BD PORTAL PUBLISHER")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print(f"Event: {json.dumps(event)}")
    print("=" * 70)

    # Fan-out: invoke advisor publisher in parallel (S3 does not allow two
    # notification rules with the same prefix+suffix, so portal-publisher
    # fires advisor-publisher async and both run concurrently)
    advisor_fn = os.environ.get('ADVISOR_PUBLISHER_FUNCTION')
    if advisor_fn:
        try:
            lam = boto3.client('lambda', region_name='us-east-1')
            lam.invoke(
                FunctionName=advisor_fn,
                InvocationType='Event',
                Payload=json.dumps(event).encode(),
            )
            print(f"Fan-out: invoked {advisor_fn} async")
        except Exception as e:
            print(f"WARN: Could not invoke {advisor_fn}: {e}")

    today = _today()

    try:
        # ------------------------------------------------------------------
        # Step 1: Load all source parquets
        # ------------------------------------------------------------------
        print("\n=== Step 1: Load parquets ===")
        data = load_all(today)
        perf     = data['perf']
        adv      = data['adv']
        geo      = data['geo']
        geo_city = data['geo_city']
        cdim     = data['cdim']
        adim     = data['adim']
        tax      = data['tax']

        # ------------------------------------------------------------------
        # Step 2: Build and write each output
        # ------------------------------------------------------------------
        print("\n=== Step 2: Build outputs ===")
        results = {}

        # timeseries_chart.json
        chart = build_timeseries_chart(perf, adv, geo, cdim, today, geo_city=geo_city)
        _save_json(chart, 'gold/timeseries_chart.json')
        results['timeseries_chart'] = 'ok'

        # architect_leaderboard.json
        lb = build_architect_leaderboard(adv, cdim, today)
        _save_json(lb, 'gold/architect_leaderboard.json')
        results['architect_leaderboard'] = 'ok'

        # clients_tab.json
        clients = build_clients_tab(perf, cdim, adim, tax, today)
        _save_json(clients, 'gold/clients_tab.json')
        results['clients_tab'] = 'ok'

        # summary/header_metrics.json
        hm = build_header_metrics(perf, adv, cdim, today)
        _save_json(hm, 'gold/summary/header_metrics.json')
        results['header_metrics'] = 'ok'

        # DISABLED: EC2 gold script 09_generate_partner_analytics.py now owns this output.
        # The EC2 version includes nested cities, nested clients, and 4-period time machine.
        # Re-enabling the Lambda version would overwrite the richer EC2 output.
        # pa = build_partner_analytics(perf, adv, geo, cdim, today)
        # _save_json(pa, 'gold/partner_analytics/header_metrics.json')
        results['partner_analytics'] = 'disabled (EC2 script owns output)'

        # filters/dimensions.json
        filters = build_filters(adv, adim, today)
        _save_json(filters, 'gold/filters/dimensions.json')
        results['filters'] = 'ok'

        # snapshots
        snapshots = build_snapshots(perf, adv, geo, adim)
        for key, snap in snapshots.items():
            _save_json(snap, key)
        results['snapshots'] = f"{len(snapshots)} files"

        # ------------------------------------------------------------------
        # Step 3: Summary
        # ------------------------------------------------------------------
        print("\n=== Step 3: Complete ===")
        latest_date = perf['date'].max()
        total_aua   = float(perf[perf['date'] == latest_date]['total_aua'].sum())
        print(f"  Data as of:  {latest_date.date()}")
        print(f"  Total AUA:   ${total_aua:,.0f}")
        print(f"  Outputs:     {results}")
        print(f"Completed: {datetime.now(timezone.utc).isoformat()}")
        print("=" * 70)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'status':       'success',
                'generated_at': datetime.now(timezone.utc).isoformat(),
                'data_as_of':   latest_date.strftime('%Y-%m-%d'),
                'total_aua':    round(total_aua, 2),
                'outputs':      results,
            }),
        }

    except Exception as exc:
        import traceback
        print(f"\nFATAL: {exc}")
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps({'status': 'error', 'error': str(exc)}),
        }
```

### distributiontab-snapshot-view-consumes-lookback-data.tsx

```
/**
 * Distribution Tab - Advisor Intelligence
 *
 * Primary view: Snapshot distribution (donut + time machine + bell curve)
 * Secondary view: Continuous stacked area chart
 *
 * Layout (Snapshot mode - default):
 * +------------------------------------------------------------+
 * | [Snapshot] [Continuous]  Cohort: [GEO][ADV]                 |
 * +----------------------------+-------------------------------+
 * |  ApexCharts Donut + Legend  |  Bell Curve Histogram         |
 * |  + Time Machine strip      |  + P10/P25/Median/P75/P90     |
 * +----------------------------+-------------------------------+
 *
 * Layout (Continuous mode):
 * +------------------------------------------------------------+
 * | [Snapshot] [Continuous]  Cohort: [GEO][ADV]  Assets  Window |
 * +---------------+--------------------------------------------+
 * | Hero Metrics   |  Stacked Area Chart                        |
 * | Legend         |                                             |
 * +---------------+--------------------------------------------+
 */

import { useState, useEffect, useMemo, useCallback, lazy, Suspense } from 'react'
import { useQuery } from '@tanstack/react-query'
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  ComposedChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
  CartesianGrid,
  ReferenceLine,
} from 'recharts'

// ApexCharts - lazy loaded (avoids SSR issues)
const Chart = lazy(() => import('react-apexcharts'))
import { Panel, PanelHeader, PanelContent, PanelFooter } from '@/ui/components/panels'
import { LoadingInline } from '@/components/LoadingSpinner'
import { ChevronLeft, HelpCircle, Search, X } from 'lucide-react'
import { Tooltip } from '@/components/Tooltip'
import { formatCurrency, formatNumberTo3Digits } from '@/lib/universalNumberFormatter'
import { getCumulativeChart, getHeaderMetrics } from '@/api/endpoints/advisor-intelligence'
import type {
  CumulativeChartResponse,
  CumulativeChartView,
  CumulativeChartDataPoint,
  CumulativeChartViewMode,
  ChartWindowOption,
  PartnerAnalyticsResponse,
  TimePeriodKey,
  PeriodSnapshot,
  PartnerAnalyticsViewWithPeriods,
  PartnerAnalyticsView,
  DonutSegment,
  DistributionStats,
  CitySegment,
  ClientSegment,
  PeriodsMetadata,
  NnaPeriodView,
  HeaderMetricsResponse,
  SegmentDistribution,
  RollingTimeseriesDataPoint,
  NNADistributionDrill,
  NNASeriesPoint,
  NNASeriesView,
} from '../types'
import { hasTimeMachine, getCurrentSnapshot } from '../types'

// ============================================================================
// TYPES & CONSTANTS
// ============================================================================

type ViewStyle = 'snapshot' | 'continuous'
type CohortOption = 'geo' | 'adv'
type DistMetricOption = 'aua' | 'nna' | 'cla'

const COHORT_OPTIONS: { value: CohortOption; label: string }[] = [
  { value: 'geo', label: 'GEO' },
  { value: 'adv', label: 'ADV' },
]

const METRIC_OPTIONS: { value: DistMetricOption; label: string }[] = [
  { value: 'aua', label: 'AUA' },
  { value: 'nna', label: 'NNA' },
  { value: 'cla', label: 'CLA' },
]

const WINDOW_OPTIONS: { value: ChartWindowOption; label: string; days: number }[] = [
  { value: '1Y', label: '1Y', days: 365 },
  { value: '3Y', label: '3Y', days: 1095 },
  { value: 'Max', label: 'Max', days: Infinity },
]

// --- Distinct color palettes (maximally separated hues) ---
// GEO: 8 states + gray Other
const GEO_COLORS = [
  '#2563EB', '#DC2626', '#16A34A', '#F59E0B',
  '#9333EA', '#06B6D4', '#EA580C', '#DB2777',
]
// ADV: 8 architects + gray Other
const ADV_COLORS = [
  '#0891B2', '#E11D48', '#65A30D', '#7C3AED',
  '#D97706', '#2563EB', '#DC2626', '#059669',
]
// CITY: 9 cities + gray Other
const CITY_COLORS = [
  '#6366F1', '#F43F5E', '#14B8A6', '#F97316',
  '#8B5CF6', '#0EA5E9', '#EAB308', '#EC4899', '#22D3EE',
]
// CLIENT: 10 client relationships + gray Other (used for ADV drill-down into an architect's book)
const CLIENT_COLORS = [
  '#F43F5E', '#3B82F6', '#10B981', '#F59E0B',
  '#8B5CF6', '#EC4899', '#06B6D4', '#84CC16', '#EF4444', '#6366F1',
]

const OTHER_COLOR = '#6B7280'

// Category color map (for continuous chart AUA/NNA cohort views)
const CATEGORY_COLORS: Record<string, string> = {
  'NMNC': '#16A34A',
  'nmnc': '#16A34A',
  'NMEC': '#2563EB',
  'nmec': '#2563EB',
  'Other': OTHER_COLOR,
}

// Fallback palette for continuous chart (geo/adv categories)
const FALLBACK_COLORS = GEO_COLORS

// Snapshot donut fallback (used when seg.color is missing from JSON)
const SNAPSHOT_FALLBACK_COLORS = GEO_COLORS

/** Build a stable name→color map from a palette, keyed by segment/category name. */
function buildColorMap(keys: string[], palette: string[]): Record<string, string> {
  const map: Record<string, string> = {}
  for (let i = 0; i < keys.length; i++) {
    const k = keys[i]
    map[k] = k === 'Other' ? OTHER_COLOR : palette[i % palette.length]
  }
  return map
}

/** Resolve color for a category using the shared color map, with fallback. */
function getCategoryColor(category: string, index: number, colorMap: Record<string, string>, cohort?: CohortOption): string {
  if (colorMap[category]) return colorMap[category]
  if (CATEGORY_COLORS[category]) return CATEGORY_COLORS[category]
  if (category === 'Other') return OTHER_COLOR
  const palette = cohort === 'adv' ? ADV_COLORS : GEO_COLORS
  return palette[index % palette.length]
}

const CATEGORY_DISPLAY_NAMES: Record<string, string> = {
  'NMNC': 'New Client Assets',
  'nmnc': 'New Client Assets',
  'NMEC': 'Existing Client Assets',
  'nmec': 'Existing Client Assets',
}

function getCategoryDisplayName(category: string): string {
  return CATEGORY_DISPLAY_NAMES[category] || category
}

// --- Downsampling helpers (pure functions) ---

/** ISO week key: "YYYY-WW" */
function isoWeekKey(dateStr: string): string {
  const d = new Date(dateStr + 'T12:00:00')
  const jan4 = new Date(d.getFullYear(), 0, 4)
  const dayOfYear = Math.floor((d.getTime() - jan4.getTime()) / 86400000) + 4
  const week = Math.ceil(dayOfYear / 7)
  return `${d.getFullYear()}-${String(week).padStart(2, '0')}`
}

/** Month key: "YYYY-MM" */
function monthKey(dateStr: string): string {
  return dateStr.slice(0, 7)
}

/** Keep last record per group (week or month) */
function keepLastPerGroup(
  data: CumulativeChartDataPoint[],
  keyFn: (dateStr: string) => string,
): CumulativeChartDataPoint[] {
  const map = new Map<string, CumulativeChartDataPoint>()
  for (const pt of data) {
    map.set(keyFn(pt.date), pt)
  }
  return Array.from(map.values())
}

function downsampleTimeseries(
  data: CumulativeChartDataPoint[],
  windowDays: number,
): CumulativeChartDataPoint[] {
  if (data.length <= 100) return data
  if (windowDays <= 365) return keepLastPerGroup(data, isoWeekKey)
  return keepLastPerGroup(data, monthKey)
}

/** Quarter key: "YYYY-Q#" */
function quarterKey(dateStr: string): string {
  const d = new Date(dateStr + 'T12:00:00')
  const q = Math.floor(d.getMonth() / 3) + 1
  return `${d.getFullYear()}-Q${q}`
}

/** Format month label: "Jan '25" */
function formatMonthLabel(dateStr: string): string {
  const d = new Date(dateStr + 'T12:00:00')
  return d.toLocaleDateString('en-US', { month: 'short', year: '2-digit' })
}

/** Format quarter label: "Q1 '25" */
function formatQuarterLabel(dateStr: string): string {
  const d = new Date(dateStr + 'T12:00:00')
  const q = Math.floor(d.getMonth() / 3) + 1
  return `Q${q} '${String(d.getFullYear()).slice(-2)}`
}

function getViewMode(cohort: CohortOption, metric: DistMetricOption): CumulativeChartViewMode {
  if (cohort === 'geo') return 'geo'
  if (cohort === 'adv') return 'adv'
  return metric === 'nna' ? 'nna' : 'aua'
}

// ============================================================================
// PROPS
// ============================================================================

interface DistributionTabProps {
  firmId: string
  analyticsData: PartnerAnalyticsResponse | null
  analyticsLoading: boolean
}

// ============================================================================
// SUB-PANEL COMPONENTS
// ============================================================================

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export function DistributionTab({ firmId, analyticsData, analyticsLoading }: DistributionTabProps) {
  // View style: snapshot (default) or continuous area chart
  const [viewStyle, setViewStyle] = useState<ViewStyle>('snapshot')

  // Two-toggle system
  const [cohort, setCohort] = useState<CohortOption>('geo')
  const [metric, setMetric] = useState<DistMetricOption>('aua')
  const [window, setWindow] = useState<ChartWindowOption>('1Y')

  const {
    data: chartData,
    isLoading,
  } = useQuery<CumulativeChartResponse>({
    queryKey: ['advisor-intelligence', 'cumulative-chart'],
    queryFn: () => getCumulativeChart(),
    enabled: !!firmId,
    staleTime: 5 * 60 * 1000,
    refetchOnWindowFocus: false,
    refetchOnMount: false,
  })

  // Build a stable category→color map from snapshot segments so both
  // Snapshot donut and Continuous area chart use identical colors.
  const categoryColorMap = useMemo(() => {
    const viewKey = cohort === 'geo' ? 'geo' : 'adv'
    const palette = cohort === 'adv' ? ADV_COLORS : GEO_COLORS
    const view = analyticsData?.views?.[viewKey]
    if (!view) return {}
    const snap = getCurrentSnapshot(view)
    const segments = ('donut' in snap) ? snap.donut?.segments : undefined
    if (!segments?.length) return {}
    return buildColorMap(segments.map(s => s.key), palette)
  }, [analyticsData, cohort])

  if (!firmId) {
    return (
      <Panel variant="chart">
        <div className="py-12 text-center">
          <p className="text-white/60">Select a partner to view distribution</p>
        </div>
      </Panel>
    )
  }

  if (isLoading) {
    return <LoadingInline className="py-12" />
  }

  return (
    <Panel variant="chart">
      <PanelHeader
        title="Segment Analytics"
        helpText="AUA distribution and account size analysis across geographic and advisor segments. Switch between snapshot (donut + bell curve) and continuous (stacked area) views. Drill into states/cities or architects/clients."
        actions={
              <div className="flex items-center gap-3">
                {/* View Style Toggle: Snapshot / Continuous */}
                <div className="flex gap-0.5 bg-white/10 rounded-lg p-0.5">
                  {(['snapshot', 'continuous'] as ViewStyle[]).map((style) => (
                    <button
                      key={style}
                      onClick={() => setViewStyle(style)}
                      className={`px-2.5 py-1 text-xs font-medium rounded-md transition-colors capitalize ${
                        viewStyle === style
                          ? 'bg-[hsl(var(--primary))] text-white'
                          : 'text-white/60 hover:text-white hover:bg-white/10'
                      }`}
                    >
                      {style.charAt(0).toUpperCase() + style.slice(1)}
                    </button>
                  ))}
                </div>

                <div className="w-px h-5 bg-white/10" />

                {/* Cohort Toggle (GEO/ADV) */}
                <div className="flex items-center gap-2">
                  <span className="text-[10px] text-white/40 uppercase tracking-wide">Cohort:</span>
                  <div className="flex gap-0.5 bg-white/10 rounded-lg p-0.5">
                    {COHORT_OPTIONS.map((opt) => (
                      <button
                        key={opt.value}
                        onClick={() => setCohort(opt.value)}
                        className={`px-2.5 py-1 text-xs font-medium rounded-md transition-colors ${
                          cohort === opt.value
                            ? 'bg-[hsl(var(--primary))] text-white'
                            : 'text-white/60 hover:text-white hover:bg-white/10'
                        }`}
                      >
                        {opt.label}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="w-px h-5 bg-white/10" />

                {/* Metric Toggle (AUA/NNA/CLA) -- always visible */}
                <div className="flex items-center gap-2">
                  <span className="text-[10px] text-white/40 uppercase tracking-wide">Metric:</span>
                  <div className="flex gap-0.5 bg-white/10 rounded-lg p-0.5">
                    {METRIC_OPTIONS.filter(opt => opt.value !== 'cla').map((opt) => (
                      <button
                        key={opt.value}
                        onClick={() => setMetric(opt.value)}
                        className={`px-2.5 py-1 text-xs font-medium rounded-md transition-colors ${
                          metric === opt.value
                            ? 'bg-[hsl(var(--primary))] text-white'
                            : 'text-white/60 hover:text-white hover:bg-white/10'
                        }`}
                      >
                        {opt.label}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Window Toggle -- continuous mode only */}
                {viewStyle === 'continuous' && (
                  <>
                    <div className="w-px h-5 bg-white/10" />

                    <div className="flex gap-0.5 bg-white/10 rounded-lg p-0.5">
                      {WINDOW_OPTIONS.map((opt) => (
                        <button
                          key={opt.value}
                          onClick={() => setWindow(opt.value)}
                          className={`px-2 py-1 text-xs font-medium rounded-md transition-colors ${
                            window === opt.value
                              ? 'bg-white/20 text-white'
                              : 'text-white/50 hover:text-white hover:bg-white/10'
                          }`}
                        >
                          {opt.label}
                        </button>
                      ))}
                    </div>
                  </>
                )}
              </div>
            }
          />

      <PanelContent>
          {viewStyle === 'snapshot' ? (
            analyticsLoading ? (
              <div className="flex items-center justify-center" style={{ minHeight: '360px' }}>
                <LoadingInline size="sm" />
              </div>
            ) : analyticsData ? (
              <SnapshotDistributionView analyticsData={analyticsData} cohort={cohort} metric={metric} categoryColorMap={categoryColorMap} />
            ) : (
              <div className="flex items-center justify-center" style={{ minHeight: '360px' }}>
                <p className="text-white/40 text-sm">Analytics data unavailable</p>
              </div>
            )
          ) : (
            <ContinuousChartView
              data={chartData ?? null}
              cohort={cohort}
              metric={metric}
              window={window}
              categoryColorMap={categoryColorMap}
              totalClients={(() => {
                const view = cohort === 'geo'
                  ? analyticsData?.views?.geo
                  : analyticsData?.views?.adv
                return view && hasTimeMachine(view) ? view.current.metrics.client_count : undefined
              })()}
            />
          )}
      </PanelContent>
      <PanelFooter content="Source: SS&C Black Diamond Wealth Solutions." timestamp={analyticsData?.generated_at} />
    </Panel>
  )
}

// ============================================================================
// Y9-FE: CONTINUOUS NNA DIVERGING BAR VIEW (per GEO/ADV category)
// ============================================================================

interface ContinuousNnaDivergingViewProps {
  data: CumulativeChartResponse | null
  cohort: CohortOption
  window: ChartWindowOption
  categoryColorMap: Record<string, string>
}

function ContinuousNnaDivergingView({ data, cohort, window: windowOpt, categoryColorMap }: ContinuousNnaDivergingViewProps) {
  const [drillParent, setDrillParent] = useState<string | null>(null)

  // Reset drill on cohort change
  useEffect(() => { setDrillParent(null) }, [cohort])

  const nnaSeriesView = cohort === 'geo' ? data?.nna_geo : data?.nna_adv

  // GEO drill: state -> city via nna_geo_drill[state]
  // ADV drill: architect -> single-architect filtered series from nna_adv
  const drillSeriesView = useMemo((): { categories: string[]; data: NNASeriesPoint[] } | null => {
    if (!drillParent) return null
    if (cohort === 'geo') return data?.nna_geo_drill?.[drillParent] ?? null
    // ADV: filter nna_adv to single architect's series
    if (cohort === 'adv' && nnaSeriesView) {
      return {
        categories: [drillParent],
        data: nnaSeriesView.data,
      }
    }
    return null
  }, [drillParent, cohort, data?.nna_geo_drill, nnaSeriesView])

  const activeView = drillSeriesView || nnaSeriesView
  const canDrillGeo = cohort === 'geo' && !!data?.nna_geo_drill
  const canDrillAdv = cohort === 'adv' && !!(nnaSeriesView?.categories?.length)
  const canDrill = canDrillGeo || canDrillAdv

  const categories = activeView?.categories ?? []
  const rawData = activeView?.data ?? []

  const windowConfig = WINDOW_OPTIONS.find(w => w.value === windowOpt)
  const daysToShow = windowConfig?.days ?? 365
  const isMax = windowOpt === 'Max'

  // Window filter
  const windowedData = useMemo(() => {
    if (rawData.length === 0) return []
    if (!isFinite(daysToShow)) return rawData
    const latestDate = rawData[rawData.length - 1].date
    const cutoffDate = new Date(latestDate)
    cutoffDate.setDate(cutoffDate.getDate() - daysToShow)
    const cutoffStr = cutoffDate.toISOString().split('T')[0]
    return rawData.filter((d: NNASeriesPoint) => d.date >= cutoffStr)
  }, [rawData, daysToShow])

  // Aggregate into period endpoints and diff to get per-period flows
  const barData = useMemo(() => {
    if (windowedData.length === 0 || categories.length === 0) return []
    const keyFn = isMax ? quarterKey : monthKey
    const labelFn = isMax ? formatQuarterLabel : formatMonthLabel

    // Get last point per period
    const periodMap = new Map<string, NNASeriesPoint>()
    for (const pt of windowedData) {
      periodMap.set(keyFn(pt.date), pt)
    }
    const endpoints = Array.from(periodMap.entries())
      .sort(([a], [b]) => a.localeCompare(b))

    if (endpoints.length < 2) return []

    // Diff adjacent periods to get period flows, aggregate across all categories
    const result = []
    for (let i = 1; i < endpoints.length; i++) {
      const [, cur] = endpoints[i]
      const [, prev] = endpoints[i - 1]
      let totalInflow = 0
      let totalOutflow = 0
      let totalNet = 0
      for (const cat of categories) {
        const curInflow = Number(cur[`${cat}_inflow`] || 0)
        const prevInflow = Number(prev[`${cat}_inflow`] || 0)
        const curOutflow = Number(cur[`${cat}_outflow`] || 0)
        const prevOutflow = Number(prev[`${cat}_outflow`] || 0)
        const curNna = Number(cur[cat] || 0)
        const prevNna = Number(prev[cat] || 0)
        totalInflow += curInflow - prevInflow
        totalOutflow += curOutflow - prevOutflow
        totalNet += curNna - prevNna
      }
      result.push({
        period: labelFn(cur.date),
        inflows: totalInflow,
        outflows: -totalOutflow, // negative = renders below zero
        net: totalNet,
      })
    }
    return result
  }, [windowedData, categories, isMax])

  // Hero metrics
  const heroMetrics = useMemo(() => {
    if (windowedData.length < 2 || categories.length === 0) return { totalNet: 0, totalInflows: 0, totalOutflows: 0 }
    const first = windowedData[0]
    const last = windowedData[windowedData.length - 1]
    let totalNet = 0, totalInflows = 0, totalOutflows = 0
    for (const cat of categories) {
      totalNet += Number(last[cat] || 0) - Number(first[cat] || 0)
      totalInflows += Number(last[`${cat}_inflow`] || 0) - Number(first[`${cat}_inflow`] || 0)
      totalOutflows += Number(last[`${cat}_outflow`] || 0) - Number(first[`${cat}_outflow`] || 0)
    }
    return { totalNet, totalInflows, totalOutflows }
  }, [windowedData, categories])

  const isDrilled = drillParent !== null

  if (!nnaSeriesView || windowedData.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-[240px]">
        <p className="text-white/40 text-sm">No NNA {cohort === 'geo' ? 'geographic' : 'advisor'} data available</p>
      </div>
    )
  }

  const changeLabel = isMax ? 'QoQ Change' : 'MoM Change'

  return (
    <div className="flex min-h-[240px]">
      {/* Left: Hero Metrics */}
      <div className="w-[280px] flex-shrink-0 p-5 flex flex-col gap-3 border-r border-white/5">
        {/* Breadcrumb */}
        {isDrilled && (
          <div className="flex items-center gap-1 mb-3 flex-wrap">
            <button
              onClick={() => setDrillParent(null)}
              className="flex items-center gap-0.5 text-xs text-white/50 hover:text-white transition-colors"
            >
              <ChevronLeft size={12} />
              <span>{cohort === 'geo' ? 'All States' : 'All Architects'}</span>
            </button>
            <span className="text-white/30 text-xs mx-1">/</span>
            <span className="text-xs text-white/80 font-medium">{getCategoryDisplayName(drillParent!)}</span>
          </div>
        )}
        <div className="text-[10px] text-white/50 uppercase tracking-widest font-medium mb-1">
          {isDrilled
            ? (cohort === 'geo' ? `${getCategoryDisplayName(drillParent!)} -- Cities` : getCategoryDisplayName(drillParent!))
            : `NNA by ${cohort === 'geo' ? 'State' : 'Architect'}`}
        </div>
        <div className="flex flex-col items-center px-4 py-3 rounded-lg bg-[hsl(var(--success))]/10 border border-[hsl(var(--success))]/30">
          <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-1">Inflows</div>
          <div className="text-2xl font-bold text-[hsl(var(--success))]">
            +{formatNumberTo3Digits(heroMetrics.totalInflows, { unit: '$', includeSign: false })}
          </div>
        </div>
        <div className="flex flex-col items-center px-4 py-3 rounded-lg bg-red-500/10 border border-red-500/30">
          <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-1">Outflows</div>
          <div className="text-2xl font-bold text-red-400">
            -{formatNumberTo3Digits(heroMetrics.totalOutflows, { unit: '$', includeSign: false })}
          </div>
        </div>
        <div className={`flex flex-col items-center px-4 py-3 rounded-lg ${heroMetrics.totalNet >= 0 ? 'bg-[hsl(var(--success))]/10 border border-[hsl(var(--success))]/30' : 'bg-red-500/10 border border-red-500/30'}`}>
          <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-1">Net NNA</div>
          <div className={`text-2xl font-bold ${heroMetrics.totalNet >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
            {formatNumberTo3Digits(heroMetrics.totalNet, { unit: '$', includeSign: true })}
          </div>
        </div>
        {/* Category legend: drillable at top level, static when drilled */}
        {categories.length > 0 && (
          <div className="mt-3 flex flex-col gap-1 max-h-[180px] overflow-y-auto">
            {categories.slice(0, 15).map((cat: string, idx: number) => {
              const showArrow = !isDrilled && canDrill
              return (
                <button
                  key={cat}
                  onClick={() => showArrow ? setDrillParent(cat) : undefined}
                  className={`flex items-center gap-2 px-2 py-1 rounded text-left text-xs ${showArrow ? 'hover:bg-white/10 cursor-pointer' : ''}`}
                >
                  <div className="w-2 h-2 rounded-full flex-shrink-0" style={{ backgroundColor: getCategoryColor(cat, idx, categoryColorMap, cohort) }} />
                  <span className="text-white/70 truncate">{getCategoryDisplayName(cat)}</span>
                  {showArrow && <span className="text-white/30 ml-auto">&rarr;</span>}
                </button>
              )
            })}
          </div>
        )}
      </div>

      {/* Right: Diverging Bar Chart */}
      <div className="flex-1 p-4 flex flex-col">
        <div className="text-[10px] text-white/40 text-right mb-2">{changeLabel}</div>
        <div className="flex-1 min-h-[200px]">
          {barData.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart data={barData} stackOffset="sign" margin={{ top: 10, right: 10, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" vertical={false} />
                <XAxis
                  dataKey="period"
                  stroke="rgba(255,255,255,0.2)"
                  tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.6)' }}
                  axisLine={false}
                  tickLine={false}
                  interval="preserveStartEnd"
                  minTickGap={40}
                />
                <YAxis
                  stroke="rgba(255,255,255,0.2)"
                  tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.6)' }}
                  tickFormatter={(value) => formatNumberTo3Digits(value, { unit: '$', includeSign: false })}
                  width={50}
                  axisLine={false}
                  tickLine={false}
                />
                <ReferenceLine y={0} stroke="rgba(255,255,255,0.15)" strokeDasharray="3 3" />
                <RechartsTooltip
                  wrapperStyle={{ zIndex: 40 }}
                  cursor={{ fill: 'rgba(255,255,255,0.06)' }}
                  content={({ active, payload, label }) => {
                    if (!active || !payload || payload.length === 0) return null
                    const d = payload[0]?.payload
                    return (
                      <div className="bg-[hsl(var(--semantic-background-chartTooltipBg))] border-2 border-[hsl(var(--primary))] rounded-lg px-4 py-3 shadow-xl">
                        <div className="text-[hsl(var(--semantic-text-chartTooltip))] font-bold text-sm mb-2">{label}</div>
                        <div className="space-y-1.5">
                          <div className="flex items-center justify-between gap-6 text-xs">
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70">Inflows</span>
                            <span className="text-[hsl(var(--success))] font-medium">+{formatCurrency(d?.inflows || 0)}</span>
                          </div>
                          <div className="flex items-center justify-between gap-6 text-xs">
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70">Outflows</span>
                            <span className="text-red-400 font-medium">-{formatCurrency(Math.abs(d?.outflows || 0))}</span>
                          </div>
                          <div className="border-t border-[hsl(var(--semantic-text-chartTooltip))]/20 my-1" />
                          <div className="flex items-center justify-between gap-6 text-xs">
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 font-medium">Net NNA</span>
                            <span className={`font-semibold ${(d?.net || 0) >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                              {formatNumberTo3Digits(d?.net || 0, { unit: '$', includeSign: true })}
                            </span>
                          </div>
                        </div>
                      </div>
                    )
                  }}
                />
                <Bar dataKey="inflows" stackId="nna" fill="#2196F3" fillOpacity={0.85} radius={[4, 4, 0, 0]} />
                <Bar dataKey="outflows" stackId="nna" fill="#EF4444" fillOpacity={0.85} radius={[0, 0, 4, 4]} />
                <Line type="monotone" dataKey="net" stroke="#F59E0B" strokeWidth={2} dot={false} />
              </ComposedChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-full">
              <p className="text-white/40 text-sm">Insufficient data for period comparison</p>
            </div>
          )}
        </div>
        {/* Legend */}
        <div className="flex justify-center gap-6 mt-2">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: '#2196F3' }} />
            <span className="text-xs text-white/70">Inflows</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: '#EF4444' }} />
            <span className="text-xs text-white/70">Outflows</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-0.5 rounded-full" style={{ backgroundColor: '#F59E0B' }} />
            <span className="text-xs text-white/70">Net NNA</span>
          </div>
        </div>
      </div>
    </div>
  )
}

// ============================================================================
// CONTINUOUS NNA CHART VIEW (Diverging Bar + Net Line) — Overall NNA fallback
// ============================================================================

interface ContinuousNnaChartViewProps {
  data: CumulativeChartResponse | null
  window: ChartWindowOption
}

function ContinuousNnaChartView({ data, window }: ContinuousNnaChartViewProps) {
  const nnaView = data?.nna
  const cats = nnaView?.categories ?? []
  // categories expected: ['NNA', 'Inflows', 'Outflows'] or similar
  const nnaKey = cats[0] ?? 'NNA'
  const inflowKey = cats[1] ?? 'Inflows'
  const outflowKey = cats[2] ?? 'Outflows'

  const windowConfig = WINDOW_OPTIONS.find(w => w.value === window)
  const daysToShow = windowConfig?.days ?? 365
  const isMax = window === 'Max'

  // Apply window filter
  const windowedData = useMemo(() => {
    if (!nnaView?.data || nnaView.data.length === 0) return []
    let filtered: CumulativeChartDataPoint[]
    if (!isFinite(daysToShow)) {
      filtered = nnaView.data
    } else {
      const latestDate = nnaView.data[nnaView.data.length - 1].date
      const cutoffDate = new Date(latestDate)
      cutoffDate.setDate(cutoffDate.getDate() - daysToShow)
      const cutoffStr = cutoffDate.toISOString().split('T')[0]
      filtered = nnaView.data.filter(d => d.date >= cutoffStr)
    }
    return filtered
  }, [nnaView, daysToShow])

  // Aggregate into period endpoints: last point per period (monthly 1Y/3Y, quarterly Max)
  const periodEndpoints = useMemo(() => {
    if (windowedData.length === 0) return []
    const keyFn = isMax ? quarterKey : monthKey
    const map = new Map<string, CumulativeChartDataPoint>()
    for (const pt of windowedData) {
      map.set(keyFn(pt.date), pt)
    }
    return Array.from(map.values())
  }, [windowedData, isMax])

  // Diff adjacent period endpoints to get period-level flows
  // outflows is negated so it renders below zero (matching PartnerAnalytics convention)
  const barData = useMemo(() => {
    if (periodEndpoints.length < 2) return []
    const result = []
    for (let i = 1; i < periodEndpoints.length; i++) {
      const cur = periodEndpoints[i]
      const prev = periodEndpoints[i - 1]
      const periodInflow = Number(cur[inflowKey] || 0) - Number(prev[inflowKey] || 0)
      const periodOutflow = Number(cur[outflowKey] || 0) - Number(prev[outflowKey] || 0)
      const periodNet = Number(cur[nnaKey] || 0) - Number(prev[nnaKey] || 0)
      result.push({
        period: isMax ? formatQuarterLabel(cur.date) : formatMonthLabel(cur.date),
        inflows: periodInflow,
        outflows: -periodOutflow, // negative = renders below zero
        net: periodNet,
      })
    }
    return result
  }, [periodEndpoints, nnaKey, inflowKey, outflowKey, isMax])

  // Hero metrics: cumulative over the windowed range
  const heroMetrics = useMemo(() => {
    if (windowedData.length < 2) return { totalNet: 0, totalInflows: 0, totalOutflows: 0 }
    const first = windowedData[0]
    const last = windowedData[windowedData.length - 1]
    return {
      totalNet: Number(last[nnaKey] || 0) - Number(first[nnaKey] || 0),
      totalInflows: Number(last[inflowKey] || 0) - Number(first[inflowKey] || 0),
      totalOutflows: Number(last[outflowKey] || 0) - Number(first[outflowKey] || 0),
    }
  }, [windowedData, nnaKey, inflowKey, outflowKey])

  if (!nnaView || windowedData.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-[240px]">
        <p className="text-white/40 text-sm">No NNA data available</p>
      </div>
    )
  }

  const changeLabel = isMax ? 'QoQ Change' : 'MoM Change'

  return (
    <div className="flex min-h-[240px]">
      {/* Left: Hero Metrics -- 3-tile layout matching PartnerAnalytics NNA panel */}
      <div className="w-[280px] flex-shrink-0 p-5 flex flex-col gap-3 border-r border-white/5">
        <div className="flex flex-col items-center px-4 py-3 rounded-lg bg-[hsl(var(--success))]/10 border border-[hsl(var(--success))]/30">
          <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-1">Inflows</div>
          <div className="text-2xl font-bold text-[hsl(var(--success))]">
            +{formatNumberTo3Digits(heroMetrics.totalInflows, { unit: '$', includeSign: false })}
          </div>
        </div>
        <div className="flex flex-col items-center px-4 py-3 rounded-lg bg-red-500/10 border border-red-500/30">
          <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-1">Outflows</div>
          <div className="text-2xl font-bold text-red-400">
            -{formatNumberTo3Digits(heroMetrics.totalOutflows, { unit: '$', includeSign: false })}
          </div>
        </div>
        <div className="flex flex-col items-center px-4 py-3 rounded-lg bg-white/5 border border-white/10">
          <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-1">Net Flow</div>
          <div className={`text-2xl font-bold ${heroMetrics.totalNet >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
            {heroMetrics.totalNet >= 0 ? '+' : ''}{formatNumberTo3Digits(heroMetrics.totalNet, { unit: '$', includeSign: false })}
          </div>
        </div>

        <div className="mt-auto pt-3 border-t border-white/5 space-y-1.5">
          <div className="flex items-center gap-2">
            <div className="w-2.5 h-2.5 rounded-sm bg-[#2196F3]" />
            <span className="text-xs text-white/50">Inflows</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2.5 h-2.5 rounded-sm bg-[#EF4444]" />
            <span className="text-xs text-white/50">Outflows</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2.5 h-2.5 rounded-full bg-[#F59E0B]" />
            <span className="text-xs text-white/50">Net NNA line</span>
          </div>
        </div>
      </div>

      {/* Right: Diverging bar + net line -- exact PartnerAnalytics NNA chart styling */}
      <div className="flex-1 p-4 flex items-center min-h-[280px]">
        {barData.length > 0 ? (
          <ResponsiveContainer width="100%" height="100%" minHeight={240}>
            <ComposedChart data={barData} margin={{ top: 20, right: 30, left: 10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" vertical={false} />
              <XAxis
                dataKey="period"
                stroke="rgba(255,255,255,0.2)"
                tick={({ x, y, payload }) => (
                  <text x={x} y={Number(y) + 12} textAnchor="middle" fontSize={11} fill="rgba(255,255,255,0.6)">
                    {payload.value}
                  </text>
                )}
                axisLine={false}
                tickLine={false}
                interval="preserveStartEnd"
                minTickGap={50}
              />
              <YAxis
                stroke="rgba(255,255,255,0.2)"
                tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.6)' }}
                tickFormatter={(v) => {
                  const abs = Math.abs(v)
                  if (abs >= 1e9) return `${v < 0 ? '-' : ''}$${(abs / 1e9).toFixed(1)}B`
                  if (abs >= 1e6) return `${v < 0 ? '-' : ''}$${(abs / 1e6).toFixed(0)}M`
                  return `$${v}`
                }}
                width={60}
                axisLine={false}
                tickLine={false}
              />
              <ReferenceLine y={0} stroke="rgba(255,255,255,0.3)" strokeWidth={1} />
              <RechartsTooltip
                wrapperStyle={{ zIndex: 40 }}
                cursor={{ fill: 'rgba(255,255,255,0.08)' }}
                content={({ active, payload, label }) => {
                  if (!active || !payload?.length) return null
                  const d = payload[0]?.payload as typeof barData[0]
                  const idx = barData.findIndex(b => b.period === d.period)
                  const priorNet = idx > 0 ? barData[idx - 1].net : null
                  const change = priorNet !== null ? d.net - priorNet : null
                  return (
                    <div className="bg-[#0f1729] border-2 border-white/10 rounded-lg px-4 py-3 shadow-xl">
                      <div className="text-white font-bold text-sm mb-2">{String(label)}</div>
                      <div className="space-y-1.5 text-xs">
                        <div className="flex items-center justify-between gap-4">
                          <div className="flex items-center gap-2">
                            <div className="w-2.5 h-2.5 rounded-full bg-[#2196F3]" />
                            <span className="text-white/70">Inflows</span>
                          </div>
                          <span className="font-medium text-[hsl(var(--success))]">
                            +{formatCurrency(d.inflows)}
                          </span>
                        </div>
                        <div className="flex items-center justify-between gap-4">
                          <div className="flex items-center gap-2">
                            <div className="w-2.5 h-2.5 rounded-full bg-[#EF4444]" />
                            <span className="text-white/70">Outflows</span>
                          </div>
                          <span className="font-medium text-red-400">
                            -{formatCurrency(Math.abs(d.outflows))}
                          </span>
                        </div>
                        <div className="flex items-center justify-between gap-4 border-t border-white/10 pt-1.5 mt-1.5">
                          <span className="text-white/70 font-medium">Net Flow</span>
                          <span className={`font-semibold ${d.net >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                            {d.net >= 0 ? '+' : ''}{formatCurrency(d.net)}
                          </span>
                        </div>
                        {change !== null && (
                          <div className="flex items-center justify-between gap-4 border-t border-white/10 pt-1.5 mt-1.5">
                            <span className="text-white/70 font-medium">{changeLabel}</span>
                            <span className={`font-semibold ${change >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                              {change >= 0 ? '+' : ''}{formatCurrency(change)}
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                  )
                }}
              />
              <Bar dataKey="inflows" radius={[4, 4, 0, 0]}>
                {barData.map((_, i) => (
                  <Cell key={`inflow-${i}`} fill="#2196F3" fillOpacity={i === barData.length - 1 ? 1 : 0.85} />
                ))}
              </Bar>
              <Bar dataKey="outflows" radius={[0, 0, 4, 4]}>
                {barData.map((_, i) => (
                  <Cell key={`outflow-${i}`} fill="#EF4444" fillOpacity={i === barData.length - 1 ? 1 : 0.85} />
                ))}
              </Bar>
              <Line
                type="monotone"
                dataKey="net"
                stroke="#F59E0B"
                strokeWidth={3}
                dot={{ r: 5, fill: '#F59E0B', strokeWidth: 2, stroke: 'hsl(var(--background))' }}
                activeDot={{ r: 7 }}
                connectNulls
              />
            </ComposedChart>
          </ResponsiveContainer>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <p className="text-white/40 text-sm">Insufficient data for selected window</p>
          </div>
        )}
      </div>
    </div>
  )
}

// ============================================================================
// CONTINUOUS CHART VIEW (Stacked Area Chart)
// ============================================================================

interface ContinuousChartViewProps {
  data: CumulativeChartResponse | null
  cohort: CohortOption
  metric: DistMetricOption
  window: ChartWindowOption
  categoryColorMap: Record<string, string>
  totalClients?: number
}

function ContinuousChartView({ data, cohort, metric, window, categoryColorMap, totalClients }: ContinuousChartViewProps) {
  // -----------------------------------------------------------------------
  // ALL hooks unconditionally at the top — Rules of Hooks
  // -----------------------------------------------------------------------
  const [drillParent, setDrillParent] = useState<string | null>(null)
  const [categorySearch, setCategorySearch] = useState('')
  // Y8: Interval toggle for AUA continuous stacked bar (per-view state)
  const [auaInterval, setAuaInterval] = useState<'monthly' | 'quarterly' | 'annually'>('monthly')

  useEffect(() => {
    setDrillParent(null)
    setCategorySearch('')
  }, [cohort, metric])

  // Derive viewData here so memos can use it; null for cla/nna (unused, early-returned below)
  const viewMode = getViewMode(cohort, metric)
  const isDrilled = drillParent !== null
  const drillViewData = isDrilled
    ? (cohort === 'geo' ? data?.geo_drill?.[drillParent!] : data?.adv_drill?.[drillParent!])
    : undefined
  const viewData = (metric === 'cla' || metric === 'nna')
    ? null
    : (drillViewData ?? (data ? data[viewMode] : null))

  const filteredChartData = useMemo(() => {
    if (!viewData?.data || viewData.data.length === 0) return []

    const windowConfig = WINDOW_OPTIONS.find(w => w.value === window)
    const daysToShow = windowConfig?.days ?? 365

    let filtered: CumulativeChartDataPoint[]
    if (!isFinite(daysToShow)) {
      filtered = viewData.data
    } else {
      const latestDate = viewData.data[viewData.data.length - 1].date
      const cutoffDate = new Date(latestDate)
      cutoffDate.setDate(cutoffDate.getDate() - daysToShow)
      const cutoffStr = cutoffDate.toISOString().split('T')[0]
      filtered = viewData.data.filter(d => d.date >= cutoffStr)
    }

    return downsampleTimeseries(filtered, daysToShow)
  }, [viewData, window])

  const categories = useMemo(() => viewData?.categories ?? [], [viewData?.categories])

  // GEO state level: limit chart to top-8 series + always include Other for full AUA tie
  const displayCategories = useMemo(() => {
    if (cohort === 'geo' && !isDrilled) {
      const nonOther = categories.filter(c => c !== 'Other')
      const top8 = nonOther.slice(0, 8)
      return categories.includes('Other') ? [...top8, 'Other'] : top8
    }
    return categories
  }, [categories, cohort, isDrilled])

  const areaMetrics = useMemo(() => {
    if (filteredChartData.length === 0 || displayCategories.length === 0) {
      return { totalNNA: 0, growthPct: 0 }
    }
    const latest = filteredChartData[filteredChartData.length - 1]
    const first = filteredChartData[0]
    const latestTotal = displayCategories.reduce((sum, cat) => sum + (Number(latest[cat]) || 0), 0)
    const firstTotal = displayCategories.reduce((sum, cat) => sum + (Number(first[cat]) || 0), 0)
    const growth = firstTotal !== 0 ? ((latestTotal - firstTotal) / Math.abs(firstTotal)) * 100 : 0
    return { totalNNA: latestTotal, growthPct: growth }
  }, [filteredChartData, displayCategories])

  const startingTotal = useMemo(() => {
    if (filteredChartData.length === 0 || displayCategories.length === 0) return 0
    const first = filteredChartData[0]
    return displayCategories.reduce((sum, cat) => sum + (Number(first[cat]) || 0), 0)
  }, [filteredChartData, displayCategories])

  // Y8: Aggregate daily data into month/quarter/year bars for AUA stacked bar
  const aggregatedBarData = useMemo(() => {
    if (metric !== 'aua' || filteredChartData.length === 0 || displayCategories.length === 0) return []

    const getPeriodKey = (dateStr: string): { key: string; label: string } => {
      const date = new Date(dateStr + 'T12:00:00')
      if (auaInterval === 'monthly') {
        const month = date.toLocaleString('en-US', { month: 'short' })
        const year = date.getFullYear()
        return { key: `${year}-${String(date.getMonth() + 1).padStart(2, '0')}`, label: `${month} '${String(year).slice(-2)}` }
      } else if (auaInterval === 'quarterly') {
        const q = Math.floor(date.getMonth() / 3) + 1
        const year = date.getFullYear()
        return { key: `${year}-Q${q}`, label: `Q${q} '${String(year).slice(-2)}` }
      } else {
        const year = date.getFullYear()
        return { key: `${year}`, label: `${year}` }
      }
    }

    // Take the last data point per period (end-of-period snapshot for cumulative data)
    const periodMap = new Map<string, { periodLabel: string; [k: string]: number | string }>()
    filteredChartData.forEach(point => {
      const { key, label } = getPeriodKey(point.date)
      const entry: { periodLabel: string; [k: string]: number | string } = periodMap.get(key) || { periodLabel: label }
      displayCategories.forEach(cat => {
        entry[cat] = Number(point[cat]) || 0
      })
      periodMap.set(key, entry)
    })

    return Array.from(periodMap.entries())
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([, v]) => v)
  }, [metric, filteredChartData, displayCategories, auaInterval])

  // -----------------------------------------------------------------------
  // Early returns AFTER all hooks
  // -----------------------------------------------------------------------

  // CLA continuous: full stacked area with drill (C4)
  if (metric === 'cla') {
    if (!data) return <LoadingInline className="py-12" />
    return <ClaContinuousView data={data} cohort={cohort} window={window} />
  }

  // NNA continuous: Y9-FE diverging bar at geo/adv drill levels
  if (metric === 'nna') {
    // If nna_geo or nna_adv data exists, use the new per-category diverging bar view
    const nnaSeriesView = cohort === 'geo' ? data?.nna_geo : data?.nna_adv
    if (nnaSeriesView) {
      return (
        <ContinuousNnaDivergingView
          data={data}
          cohort={cohort}
          window={window}
          categoryColorMap={categoryColorMap}
        />
      )
    }
    // Fallback to the overall NNA chart when geo/adv granularity not available
    return <ContinuousNnaChartView data={data} window={window} />
  }

  // -----------------------------------------------------------------------
  // Derived values (non-hooks) for the stacked area render path
  // -----------------------------------------------------------------------
  const showAdvComingSoon = isDrilled && cohort === 'adv' && !drillViewData
  // ADV: legend is drillable at architect level only (client is terminal grain — no second level)
  const canLegendDrill = (cohort === 'adv' && !isDrilled) || (cohort === 'geo' && !!data?.geo_drill)

  const gainSinceStart = areaMetrics.totalNNA - startingTotal
  const startDate = filteredChartData.length > 0 ? filteredChartData[0].date : null
  const startDateFormatted = startDate
    ? new Date(startDate + 'T12:00:00').toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
    : ''

  return (
    <div className="flex min-h-[240px]">
      {/* Left: Hero Metrics */}
      <div className="w-[280px] flex-shrink-0 p-5 flex flex-col border-r border-white/5">
        {/* Breadcrumb: All States / StateName (or All Architects / ArchitectName) */}
        {isDrilled && (
          <div className="flex items-center gap-1 mb-3">
            <button
              onClick={() => setDrillParent(null)}
              className="flex items-center gap-0.5 text-xs text-white/50 hover:text-white transition-colors"
            >
              <ChevronLeft size={12} />
              <span>{cohort === 'geo' ? 'All States' : 'All Architects'}</span>
            </button>
            <span className="text-white/30 text-xs mx-1">/</span>
            <span className="text-xs text-white/80 font-medium">{getCategoryDisplayName(drillParent!)}</span>
          </div>
        )}
        <div className="text-center mb-4">
          <p className="text-3xl font-bold text-white tracking-tight">
            {formatCurrency(areaMetrics.totalNNA)}
          </p>
          <p className="text-xs text-white/40 uppercase tracking-wider mt-1">
            {isDrilled
              ? `${drillParent?.replace(/_/g, ' ')} -- ${cohort === 'geo' ? 'Cities' : 'Clients'}`
              : `${metric === 'aua' ? 'Cumulative AUA' : 'Net New Assets'} by ${cohort === 'geo' ? 'Geography' : 'Advisor'}`}
          </p>
        </div>

        <div className="grid grid-cols-2 gap-2 mb-4">
          <div className="bg-white/5 rounded-lg p-2.5 text-center">
            <p className={`text-sm font-bold ${gainSinceStart >= 0 ? 'text-[hsl(var(--success))]' : 'text-[hsl(var(--destructive))]'}`}>
              {formatNumberTo3Digits(gainSinceStart, { unit: '$', includeSign: true })}
            </p>
            <p className="text-[10px] text-white/40 mt-0.5">
              {startDateFormatted ? `Since ${startDateFormatted}` : 'Period Gain'}
            </p>
          </div>

          <div className="bg-white/5 rounded-lg p-2.5 text-center">
            <p className={`text-sm font-bold ${areaMetrics.growthPct >= 0 ? 'text-[hsl(var(--success))]' : 'text-[hsl(var(--destructive))]'}`}>
              {formatNumberTo3Digits(areaMetrics.growthPct, { unit: '%', includeSign: true })}
            </p>
            <p className="text-[10px] text-white/40 mt-0.5">Growth Rate</p>
          </div>
        </div>

        <div className="bg-white/5 rounded-lg p-2.5 text-center mb-4">
          <p className="text-sm font-bold text-white">
            {window === 'Max'
              ? (totalClients?.toLocaleString() ?? '--')
              : (data?.metadata?.new_clients?.[window as string]?.toLocaleString() ?? '--')}
          </p>
          <p className="text-[10px] text-white/40 mt-0.5">
            {window === 'Max' ? 'Total Clients' : 'New Clients'}
          </p>
        </div>

        {/* Search input: all drillable states (GEO) or architects (ADV), not just top-N */}
        {!isDrilled && (
          <div className="relative mt-auto mb-2">
            <div className="flex items-center gap-2 bg-white/5 border border-white/10 rounded-md px-2 py-1.5">
              <Search size={12} className="text-white/40 flex-shrink-0" />
              <input
                type="text"
                placeholder={cohort === 'geo' ? 'Search all states...' : 'Search all architects...'}
                value={categorySearch}
                onChange={(e) => setCategorySearch(e.target.value)}
                className="bg-transparent text-xs text-white placeholder-white/40 outline-none w-full"
              />
              {categorySearch && (
                <button onClick={() => setCategorySearch('')}>
                  <X size={12} className="text-white/40 hover:text-white transition-colors" />
                </button>
              )}
            </div>
            {categorySearch && (() => {
              const drillKeys = cohort === 'geo'
                ? Object.keys(data?.geo_drill ?? {})
                : Object.keys(data?.adv_drill ?? {})
              const filtered = drillKeys.filter(k =>
                k !== 'Other' && getCategoryDisplayName(k).toLowerCase().includes(categorySearch.toLowerCase())
              )
              return (
                <div className="absolute top-full left-0 right-0 mt-1 bg-[hsl(var(--bg-panel))] border border-white/10 rounded-md max-h-36 overflow-y-auto z-20 shadow-xl">
                  {filtered.map((k, idx) => (
                    <button
                      key={k}
                      onClick={() => { setDrillParent(k); setCategorySearch('') }}
                      className="flex items-center gap-2 w-full px-3 py-1.5 hover:bg-white/10 transition-colors text-left"
                    >
                      <div className="w-2 h-2 rounded-sm flex-shrink-0" style={{ backgroundColor: getCategoryColor(k, idx, categoryColorMap, cohort) }} />
                      <span className="text-xs text-white/70">{getCategoryDisplayName(k)}</span>
                      <span className="text-white/30 text-xs ml-auto">&rarr;</span>
                    </button>
                  ))}
                  {filtered.length === 0 && (
                    <p className="px-3 py-2 text-xs text-white/40">
                      {cohort === 'geo' ? 'No states found' : 'No architects found'}
                    </p>
                  )}
                </div>
              )
            })()}
          </div>
        )}

        {displayCategories.length > 0 && (
          <div className="pt-3 border-t border-white/5 space-y-1.5">
            {displayCategories.map((cat, idx) => {
              const color = getCategoryColor(cat, idx, categoryColorMap, cohort)
              if (canLegendDrill && !isDrilled) {
                return (
                  <button
                    key={cat}
                    onClick={() => setDrillParent(cat)}
                    className="flex items-center gap-2 hover:bg-white/10 rounded px-1 py-0.5 transition-colors w-full text-left"
                  >
                    <div className="w-2.5 h-2.5 rounded-sm flex-shrink-0" style={{ backgroundColor: color }} />
                    <span className="text-xs text-white/50">{getCategoryDisplayName(cat)}</span>
                    <span className="text-white/30 text-xs ml-auto">&rarr;</span>
                  </button>
                )
              }
              return (
                <div key={cat} className="flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-sm" style={{ backgroundColor: color }} />
                  <span className="text-xs text-white/50">{getCategoryDisplayName(cat)}</span>
                </div>
              )
            })}
          </div>
        )}
      </div>

      {/* Right: Stacked Bar Chart (Y8) */}
      <div className="flex-1 flex flex-col min-h-[280px]">
        {/* Y8: Interval toggle */}
        <div className="flex justify-end px-4 pt-3">
          <div className="flex gap-0.5 bg-white/10 rounded-lg p-0.5">
            {([['monthly', 'Month'], ['quarterly', 'Quarter'], ['annually', 'Year']] as const).map(([val, label]) => (
              <button
                key={val}
                onClick={() => setAuaInterval(val)}
                className={`px-2 py-1 text-xs font-medium rounded-md transition-colors ${
                  auaInterval === val ? 'bg-white/20 text-white' : 'text-white/50 hover:text-white hover:bg-white/10'
                }`}
              >
                {label}
              </button>
            ))}
          </div>
        </div>
        <div className="flex-1 p-4 flex items-center">
          {showAdvComingSoon ? (
            <div className="flex-1 flex items-center justify-center w-full">
              <div className="text-center">
                <p className="text-white/50 text-sm font-medium">{drillParent?.replace(/_/g, ' ')}</p>
                <p className="text-white/30 text-xs mt-1">Relationship-level timeseries coming soon</p>
              </div>
            </div>
          ) : aggregatedBarData.length > 0 && displayCategories.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%" minHeight={240}>
              <BarChart data={aggregatedBarData} margin={{ top: 10, right: 10, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" vertical={false} />
                <XAxis
                  dataKey="periodLabel"
                  stroke="rgba(255,255,255,0.2)"
                  tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.6)' }}
                  axisLine={false}
                  tickLine={false}
                  interval="preserveStartEnd"
                  minTickGap={40}
                />
                <YAxis
                  stroke="rgba(255,255,255,0.2)"
                  tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.6)' }}
                  tickFormatter={(value) => formatNumberTo3Digits(value, { unit: '$', includeSign: false })}
                  width={50}
                  axisLine={false}
                  tickLine={false}
                />
                <RechartsTooltip
                  wrapperStyle={{ zIndex: 40 }}
                  cursor={{ fill: 'rgba(255,255,255,0.06)' }}
                  content={({ active, payload, label }) => {
                    if (!active || !payload || payload.length === 0) return null
                    const total = payload.reduce((sum, entry) => sum + (Number(entry.value) || 0), 0)
                    const sortedPayload = [...payload].sort((a, b) => (Number(b.value) || 0) - (Number(a.value) || 0))
                    return (
                      <div className="bg-[hsl(var(--semantic-background-chartTooltipBg))] border-2 border-[hsl(var(--primary))] rounded-lg px-4 py-3 shadow-xl">
                        <div className="text-[hsl(var(--semantic-text-chartTooltip))] font-bold text-sm mb-2">
                          {label}
                        </div>
                        <div className="flex items-center justify-between gap-6 mb-2">
                          <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm">Cumulative AUA</span>
                          <span className="text-[hsl(var(--semantic-text-chartTooltip))] font-semibold text-sm">
                            {formatCurrency(total)}
                          </span>
                        </div>
                        <div className="border-t border-[hsl(var(--semantic-text-chartTooltip))]/20 my-2" />
                        <div className="space-y-1">
                          {sortedPayload.map((entry) => (
                            <div key={entry.dataKey} className="flex items-center justify-between gap-6">
                              <div className="flex items-center gap-2">
                                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.color as string }} />
                                <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-xs">
                                  {getCategoryDisplayName(String(entry.dataKey))}
                                </span>
                              </div>
                              <span className="text-[hsl(var(--semantic-text-chartTooltip))] text-xs font-medium">
                                {formatCurrency(Number(entry.value))}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )
                  }}
                />
                {/* Y1: NMNC on top — reverse so NMEC renders first (bottom) */}
                {[...displayCategories].reverse().map((cat, idx) => {
                  const color = getCategoryColor(cat, idx, categoryColorMap, cohort)
                  const isLast = idx === displayCategories.length - 1
                  return (
                    <Bar
                      key={cat}
                      dataKey={cat}
                      stackId="aua"
                      fill={color}
                      fillOpacity={0.85}
                      radius={isLast ? [4, 4, 0, 0] : [0, 0, 0, 0]}
                    />
                  )
                })}
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex-1 flex items-center justify-center">
              <p className="text-white/40 text-sm">No chart data available</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// ============================================================================
// CLA CONTINUOUS VIEW (C4 — stacked area with total/geo/city/adv drill)
// ============================================================================

interface ClaContinuousViewProps {
  data: CumulativeChartResponse
  cohort: CohortOption
  window: ChartWindowOption
}

function ClaContinuousView({ data, cohort, window: windowProp }: ClaContinuousViewProps) {
  const [drillKey, setDrillKey] = useState<string | null>(null)
  const [cityKey, setCityKey] = useState<string | null>(null)

  useEffect(() => {
    setDrillKey(null)
    setCityKey(null)
  }, [cohort])

  const cla = data.cla

  const activeView = useMemo((): CumulativeChartView | null => {
    if (!cla) return null
    if (cohort === 'adv' && drillKey && cla.adv_drill[drillKey]) return cla.adv_drill[drillKey]
    if (cohort === 'geo' && drillKey && cityKey && cla.geo_city_drill?.[drillKey]?.[cityKey]) return cla.geo_city_drill[drillKey][cityKey]
    if (cohort === 'geo' && drillKey && cla.geo_drill[drillKey]) return cla.geo_drill[drillKey]
    return cla.total
  }, [cla, cohort, drillKey, cityKey])

  const categories = useMemo(() => activeView?.categories ?? [], [activeView])

  const filteredData = useMemo(() => {
    if (!activeView?.data?.length) return []
    const windowConfig = WINDOW_OPTIONS.find(w => w.value === windowProp)
    const daysToShow = windowConfig?.days ?? 365
    let filtered: CumulativeChartDataPoint[]
    if (!isFinite(daysToShow)) {
      filtered = activeView.data
    } else {
      const latestDate = activeView.data[activeView.data.length - 1].date
      const cutoff = new Date(latestDate)
      cutoff.setDate(cutoff.getDate() - daysToShow)
      const cutoffStr = cutoff.toISOString().split('T')[0]
      filtered = activeView.data.filter(d => d.date >= cutoffStr)
    }
    return downsampleTimeseries(filtered, daysToShow)
  }, [activeView, windowProp])

  const latestTotal = useMemo(() => {
    if (!filteredData.length) return 0
    const latest = filteredData[filteredData.length - 1]
    return categories.reduce((sum, cat) => sum + (Number(latest[cat]) || 0), 0)
  }, [filteredData, categories])

  // Drill list for the left panel (contextual based on level)
  const drillList = useMemo(() => {
    if (!cla) return []
    if (cohort === 'adv' && !drillKey) return Object.keys(cla.adv_drill)
    if (cohort === 'geo' && drillKey && !cityKey && cla.geo_city_drill?.[drillKey]) return Object.keys(cla.geo_city_drill[drillKey])
    if (cohort === 'geo' && !drillKey) return Object.keys(cla.geo_drill)
    return []
  }, [cla, cohort, drillKey, cityKey])

  const isDrilled = drillKey !== null

  if (!cla) {
    return (
      <div className="flex items-center justify-center min-h-[240px]">
        <p className="text-white/40 text-sm">CLA timeseries not available</p>
      </div>
    )
  }

  const drillListPalette = (cohort === 'geo' && !drillKey) ? GEO_COLORS : ADV_COLORS

  return (
    <div className="flex min-h-[240px]">
      {/* Left panel */}
      <div className="w-[280px] flex-shrink-0 p-5 flex flex-col border-r border-white/5">

        {/* Breadcrumb */}
        {isDrilled && (
          <div className="flex items-center gap-1 mb-3 flex-wrap">
            <button
              onClick={() => { setDrillKey(null); setCityKey(null) }}
              className="flex items-center gap-0.5 text-xs text-white/50 hover:text-white transition-colors"
            >
              <ChevronLeft size={12} />
              <span>{cohort === 'geo' ? 'All States' : 'All Architects'}</span>
            </button>
            <span className="text-white/30 text-xs mx-1">/</span>
            <button
              onClick={() => setCityKey(null)}
              className={`text-xs transition-colors ${cityKey ? 'text-white/50 hover:text-white' : 'text-white/80 font-medium'}`}
            >
              {getCategoryDisplayName(drillKey)}
            </button>
            {cityKey && (
              <>
                <span className="text-white/30 text-xs mx-1">/</span>
                <span className="text-xs text-white/80 font-medium">{getCategoryDisplayName(cityKey)}</span>
              </>
            )}
          </div>
        )}

        {/* Hero metric */}
        <div className="text-center mb-4">
          <p className="text-3xl font-bold text-white tracking-tight">{formatCurrency(latestTotal)}</p>
          <p className="text-xs text-white/40 uppercase tracking-wider mt-1">
            {isDrilled
              ? `${cohort === 'geo' ? (cityKey ? 'City' : 'State') : 'Architect'} AUA`
              : 'Total CLA AUA'}
          </p>
        </div>

        {/* NMNC/NMEC legend */}
        <div className="flex flex-col gap-1.5 mb-4">
          {categories.map((cat, idx) => (
            <div key={cat} className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-sm flex-shrink-0" style={{ backgroundColor: CATEGORY_COLORS[cat] || FALLBACK_COLORS[idx % FALLBACK_COLORS.length] }} />
              <span className="text-xs text-white/50">{getCategoryDisplayName(cat)}</span>
            </div>
          ))}
        </div>

        {/* Drill list */}
        {drillList.length > 0 && (
          <div className="mt-auto pt-3 border-t border-white/5">
            <p className="text-[10px] text-white/30 uppercase tracking-wider mb-2">
              {cohort === 'geo' && !drillKey ? 'Drill by State' :
               cohort === 'geo' && drillKey && !cityKey ? 'Drill by City' :
               'Drill by Architect'}
            </p>
            <div className="space-y-1 max-h-[160px] overflow-y-auto scrollbar-none">
              {drillList.map((key, idx) => (
                <button
                  key={key}
                  onClick={() => {
                    if (cohort === 'adv') { setDrillKey(key) }
                    else if (drillKey && !cityKey) { setCityKey(key) }
                    else { setDrillKey(key) }
                  }}
                  className="flex items-center gap-2 hover:bg-white/10 rounded px-1 py-0.5 transition-colors w-full text-left"
                >
                  <div className="w-2 h-2 rounded-sm flex-shrink-0" style={{ backgroundColor: drillListPalette[idx % drillListPalette.length] }} />
                  <span className="text-xs text-white/50 truncate">{getCategoryDisplayName(key)}</span>
                  <span className="text-white/30 text-xs ml-auto">&rarr;</span>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Right: Stacked Area Chart */}
      <div className="flex-1 p-4 flex items-center min-h-[280px]">
        {filteredData.length > 0 && categories.length > 0 ? (
          <ResponsiveContainer width="100%" height="100%" minHeight={240}>
            <AreaChart data={filteredData} margin={{ top: 10, right: 10, left: 0, bottom: 5 }}>
              <defs>
                {categories.map((cat, idx) => {
                  const color = CATEGORY_COLORS[cat] || FALLBACK_COLORS[idx % FALLBACK_COLORS.length]
                  return (
                    <linearGradient key={cat} id={`cla-grad-${cat}`} x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor={color} stopOpacity={0.5} />
                      <stop offset="100%" stopColor={color} stopOpacity={0.05} />
                    </linearGradient>
                  )
                })}
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
              <XAxis
                dataKey="date"
                stroke="rgba(255,255,255,0.2)"
                tick={{ fontSize: 10 }}
                tickFormatter={(value) => {
                  const date = new Date(value + 'T12:00:00')
                  return date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' })
                }}
                interval="preserveStartEnd"
                minTickGap={80}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                stroke="rgba(255,255,255,0.2)"
                tick={{ fontSize: 10 }}
                tickFormatter={(value) => formatNumberTo3Digits(value, { unit: '$', includeSign: false })}
                width={50}
                axisLine={false}
                tickLine={false}
              />
              <RechartsTooltip
                wrapperStyle={{ zIndex: 40 }}
                cursor={{ stroke: 'rgba(94,114,228,0.5)', strokeWidth: 2 }}
                content={({ active, payload, label }) => {
                  if (!active || !payload || payload.length === 0) return null
                  const date = new Date(String(label) + 'T12:00:00')
                  const displayDate = date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })
                  const total = payload.reduce((sum, entry) => sum + (Number(entry.value) || 0), 0)
                  return (
                    <div className="bg-[hsl(var(--semantic-background-chartTooltipBg))] border-2 border-[hsl(var(--primary))] rounded-lg px-4 py-3 shadow-xl">
                      <div className="text-[hsl(var(--semantic-text-chartTooltip))] font-bold text-sm mb-2">{displayDate}</div>
                      <div className="flex items-center justify-between gap-6 mb-2">
                        <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm">Total AUA</span>
                        <span className="text-[hsl(var(--semantic-text-chartTooltip))] font-semibold text-sm">{formatCurrency(total)}</span>
                      </div>
                      <div className="border-t border-[hsl(var(--semantic-text-chartTooltip))]/20 my-2" />
                      <div className="space-y-1">
                        {[...payload].sort((a, b) => (Number(b.value) || 0) - (Number(a.value) || 0)).map(entry => (
                          <div key={entry.dataKey} className="flex items-center justify-between gap-6">
                            <div className="flex items-center gap-2">
                              <div className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.color as string }} />
                              <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-xs">{getCategoryDisplayName(String(entry.dataKey))}</span>
                            </div>
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))] text-xs font-medium">{formatCurrency(Number(entry.value))}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )
                }}
              />
              {categories.map((cat, idx) => {
                const color = CATEGORY_COLORS[cat] || FALLBACK_COLORS[idx % FALLBACK_COLORS.length]
                return (
                  <Area
                    key={cat}
                    type="monotone"
                    dataKey={cat}
                    stackId="cla"
                    stroke={color}
                    strokeWidth={2}
                    fill={`url(#cla-grad-${cat})`}
                  />
                )
              })}
            </AreaChart>
          </ResponsiveContainer>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <p className="text-white/40 text-sm">No CLA timeseries data</p>
          </div>
        )}
      </div>
    </div>
  )
}

// ============================================================================
// SNAPSHOT DISTRIBUTION VIEW
// ============================================================================

interface SnapshotDistributionViewProps {
  analyticsData: PartnerAnalyticsResponse
  cohort: CohortOption
  metric: DistMetricOption
  categoryColorMap: Record<string, string>
}

function SnapshotDistributionView({ analyticsData, cohort, metric, categoryColorMap }: SnapshotDistributionViewProps) {
  const viewMode = cohort === 'geo' ? 'geo' : 'adv'

  const [selectedPeriod, setSelectedPeriod] = useState<TimePeriodKey>('current')
  const [geoDrillLevel, setGeoDrillLevel] = useState<'state' | 'city'>('state')
  const [selectedStateKey, setSelectedStateKey] = useState<string | null>(null)
  const [advDrillLevel, setAdvDrillLevel] = useState<'architect' | 'client'>('architect')
  const [selectedArchitectKey, setSelectedArchitectKey] = useState<string | null>(null)
  const [selectedSegmentKey, setSelectedSegmentKey] = useState<string | null>(null)

  // Reset drill state when cohort or metric changes
  useEffect(() => {
    setGeoDrillLevel('state')
    setSelectedStateKey(null)
    setAdvDrillLevel('architect')
    setSelectedArchitectKey(null)
    setSelectedSegmentKey(null)
    setSelectedPeriod('current')
  }, [cohort, metric])

  // --- NNA: read from views.nna[period][cohort] ---
  const nnaSnapshot: PeriodSnapshot | null = useMemo(() => {
    if (metric !== 'nna') return null
    const nnaViews = analyticsData.views?.nna as Record<string, NnaPeriodView> | undefined
    if (!nnaViews) return null
    const periodView = nnaViews[selectedPeriod]
    if (!periodView) return null
    const cohortView = cohort === 'geo' ? periodView.geo : periodView.adv
    if (!cohortView) return null
    return {
      donut: cohortView.donut,
      distribution: cohortView.distribution,
      metrics: { aua: Math.abs(cohortView.metrics.nna), client_count: cohortView.metrics.client_count },
    } as PeriodSnapshot
  }, [analyticsData, metric, selectedPeriod, cohort])

  // --- AUA: read from views[geo|adv][period] ---
  const rawView = analyticsData.views?.[viewMode]
  const hasTimeMachineData = rawView && hasTimeMachine(rawView as PartnerAnalyticsViewWithPeriods | PartnerAnalyticsView)

  const auaSnapshot: PeriodSnapshot | null = useMemo(() => {
    if (!rawView) return null
    const view = rawView as PartnerAnalyticsViewWithPeriods | PartnerAnalyticsView
    if (hasTimeMachine(view)) {
      const vp = view as PartnerAnalyticsViewWithPeriods
      return selectedPeriod === 'current' ? vp.current : (vp[selectedPeriod] || vp.current)
    }
    return view as unknown as PeriodSnapshot
  }, [rawView, selectedPeriod])

  // Select snapshot based on metric
  const currentSnapshot = metric === 'nna' ? nnaSnapshot : auaSnapshot

  const donut = currentSnapshot?.donut
  const distribution = currentSnapshot?.distribution
  const baseSegments: DonutSegment[] = useMemo(() => donut?.segments || [], [donut])

  const isDrilledDown = (cohort === 'geo' && geoDrillLevel === 'city') ||
                        (cohort === 'adv' && advDrillLevel === 'client')

  // Y6b/Y6d: Access raw NNA drill data for distribution resolution when drilled
  // MUST be declared before `segments` memo which reads it
  const nnaDrillData = useMemo(() => {
    if (metric !== 'nna') return null
    const nnaViews = analyticsData.views?.nna as Record<string, NnaPeriodView> | undefined
    if (!nnaViews) return null
    const periodView = nnaViews[selectedPeriod]
    if (!periodView) return null
    const cohortView = cohort === 'geo' ? periodView.geo : periodView.adv
    return cohortView?.drill ?? null
  }, [analyticsData, metric, selectedPeriod, cohort])

  const segments: DonutSegment[] = useMemo(() => {
    if (cohort === 'geo' && geoDrillLevel === 'city' && selectedStateKey) {
      // NNA mode: city segments come from nnaDrillData (NNA donut segments don't embed .cities)
      if (metric === 'nna' && nnaDrillData?.[selectedStateKey]?.by_city) {
        const byCityEntries = Object.entries(nnaDrillData[selectedStateKey].by_city)
        return byCityEntries.map(([cityKey, dist]) => ({
          key: cityKey,
          label: cityKey.split('_').map((w: string) => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
          aua: Math.abs(dist.total ?? 0),
          aua_pct: 0,
          client_count: dist.count ?? 0,
          color: '',
          distribution: dist,
        })) as DonutSegment[]
      }
      // AUA mode: use cities embedded in donut segments
      const parent = baseSegments.find(s => s.key === selectedStateKey)
      if (parent?.cities?.length) {
        return parent.cities.map((city: CitySegment) => ({
          key: city.key, label: city.label, aua: city.aua, aua_pct: city.aua_pct,
          client_count: city.client_count, color: city.color, distribution: city.distribution,
        }))
      }
      return []
    }
    if (cohort === 'adv' && advDrillLevel === 'client' && selectedArchitectKey) {
      const parent = baseSegments.find(s => s.key === selectedArchitectKey)
      if (parent?.clients?.length) {
        return parent.clients.map((client: ClientSegment) => ({
          key: client.key, label: client.label, aua: client.aua, aua_pct: client.aua_pct,
          client_count: client.account_count, color: '', distribution: client.distribution,
        }))
      }
      return []
    }
    return baseSegments
  }, [cohort, metric, geoDrillLevel, advDrillLevel, selectedStateKey, selectedArchitectKey, baseSegments, nnaDrillData])

  const parentSegment: DonutSegment | null = useMemo(() => {
    if (cohort === 'geo' && geoDrillLevel === 'city' && selectedStateKey)
      return baseSegments.find(s => s.key === selectedStateKey) || null
    if (cohort === 'adv' && advDrillLevel === 'client' && selectedArchitectKey)
      return baseSegments.find(s => s.key === selectedArchitectKey) || null
    return null
  }, [cohort, geoDrillLevel, advDrillLevel, selectedStateKey, selectedArchitectKey, baseSegments])

  const selectedSegment: DonutSegment | null = useMemo(
    () => selectedSegmentKey ? segments.find(s => s.key === selectedSegmentKey) || null : null,
    [selectedSegmentKey, segments]
  )

  // Resolve distribution stats for a given period snapshot at the current drill level
  const getDistributionForSnapshot = useCallback((snap: PeriodSnapshot | null | undefined): DistributionStats | null => {
    if (!snap) return null
    const dist = snap.distribution

    // Child drill: inline distribution on the city/client segment
    if (isDrilledDown && selectedSegmentKey) {
      if (cohort === 'geo' && selectedStateKey) {
        const stateSeg = snap.donut?.segments?.find((s: DonutSegment) => s.key === selectedStateKey)
        const city = stateSeg?.cities?.find((c: CitySegment) => c.key === selectedSegmentKey)
        if (city?.distribution) return city.distribution
      } else if (cohort === 'adv' && selectedArchitectKey) {
        const archSeg = snap.donut?.segments?.find((s: DonutSegment) => s.key === selectedArchitectKey)
        const client = archSeg?.clients?.find((c: ClientSegment) => c.key === selectedSegmentKey)
        if (client?.distribution) return client.distribution
      }
      return null
    }

    // Parent drill: by_segment on the parent key, or inline distribution
    const parentKey = selectedStateKey || selectedArchitectKey
    if (isDrilledDown && parentKey) {
      return dist?.by_segment?.[parentKey] || null
    }

    // Segment selected (not drilled): by_segment lookup
    if (selectedSegmentKey && dist?.by_segment?.[selectedSegmentKey]) {
      return dist.by_segment[selectedSegmentKey]
    }

    // Total level
    return dist?.total || null
  }, [cohort, isDrilledDown, selectedSegmentKey, selectedStateKey, selectedArchitectKey])

  const distributionData: DistributionStats | null = useMemo(() => {
    // Y6b/Y6d: When drilled in NNA mode, resolve from NNA drill data
    if (metric === 'nna' && isDrilledDown && nnaDrillData) {
      const parentKey = selectedStateKey || selectedArchitectKey
      if (parentKey) {
        const drillEntry = nnaDrillData[parentKey]
        if (drillEntry) {
          // If a sub-segment is selected and by_city exists, try that first
          if (selectedSegmentKey && drillEntry.by_city?.[selectedSegmentKey]) {
            return drillEntry.by_city[selectedSegmentKey]
          }
          // ADV drill entry has 'distribution'; GEO drill entry has 'total'
          if (drillEntry.distribution) return drillEntry.distribution
          if (drillEntry.total) return drillEntry.total
        }
      }
    }
    if (selectedSegment?.distribution) return selectedSegment.distribution
    if (selectedSegment && distribution?.by_segment?.[selectedSegment.key])
      return distribution.by_segment[selectedSegment.key]
    if (parentSegment?.distribution) return parentSegment.distribution
    if (parentSegment && distribution?.by_segment?.[parentSegment.key])
      return distribution.by_segment[parentSegment.key]
    return distribution?.total || null
  }, [selectedSegment, parentSegment, distribution, metric, isDrilledDown, nnaDrillData, selectedStateKey, selectedArchitectKey, selectedSegmentKey])

  // Current period distribution at the same drill level (for comparison deltas)
  const currentDistributionData: DistributionStats | null = useMemo(() => {
    if (!rawView || selectedPeriod === 'current') return null
    const view = rawView as PartnerAnalyticsViewWithPeriods
    return getDistributionForSnapshot(view.current)
  }, [rawView, selectedPeriod, getDistributionForSnapshot])

  // Context-aware globalMaxCount
  const globalMaxCount: number | undefined = useMemo(() => {
    if (!rawView) return undefined
    const view = rawView as PartnerAnalyticsViewWithPeriods
    const periods: TimePeriodKey[] = ['current', 'q1', 'q2', 'q3']
    const maxCounts: number[] = []
    for (const period of periods) {
      const snap = period === 'current' ? view.current : view[period]
      if (!snap) continue
      let counts: number[] | undefined
      if (selectedSegmentKey && isDrilledDown) {
        if (cohort === 'geo' && selectedStateKey) {
          const stateSeg = snap.donut?.segments?.find((s: DonutSegment) => s.key === selectedStateKey)
          const city = stateSeg?.cities?.find((c: CitySegment) => c.key === selectedSegmentKey)
          counts = city?.distribution?.histogram?.counts
        } else if (cohort === 'adv' && selectedArchitectKey) {
          const archSeg = snap.donut?.segments?.find((s: DonutSegment) => s.key === selectedArchitectKey)
          const client = archSeg?.clients?.find((c: ClientSegment) => c.key === selectedSegmentKey)
          counts = client?.distribution?.histogram?.counts
        }
      } else if (isDrilledDown) {
        const parentKey = selectedStateKey || selectedArchitectKey
        if (parentKey) counts = snap.distribution?.by_segment?.[parentKey]?.histogram?.counts
      } else {
        counts = snap.distribution?.total?.histogram?.counts
      }
      if (counts?.length) maxCounts.push(Math.max(...counts))
    }
    return maxCounts.length ? Math.max(...maxCounts) : undefined
  }, [rawView, cohort, isDrilledDown, selectedStateKey, selectedArchitectKey, selectedSegmentKey])

  const handleSegmentClick = useCallback((seg: DonutSegment) => {
    // Y6b/Y6d: NNA now supports drill-down at top level (same as AUA)
    if (cohort === 'geo' && geoDrillLevel === 'state') {
      // NNA-GEO: drill into state if drill data exists, otherwise toggle segment filter
      if (metric === 'nna' && !nnaDrillData?.[seg.key]) {
        setSelectedSegmentKey(prev => prev === seg.key ? null : seg.key)
        return
      }
      setSelectedStateKey(seg.key); setGeoDrillLevel('city'); setSelectedSegmentKey(null); return
    }
    if (cohort === 'adv' && advDrillLevel === 'architect') {
      // NNA-ADV: drill into architect if drill data exists, otherwise toggle segment filter
      if (metric === 'nna' && !nnaDrillData?.[seg.key]) {
        setSelectedSegmentKey(prev => prev === seg.key ? null : seg.key)
        return
      }
      setSelectedArchitectKey(seg.key); setAdvDrillLevel('client'); setSelectedSegmentKey(null); return
    }
    setSelectedSegmentKey(prev => prev === seg.key ? null : seg.key)
  }, [cohort, metric, geoDrillLevel, advDrillLevel, nnaDrillData])

  const handleDrillUp = useCallback(() => {
    if (cohort === 'geo') { setGeoDrillLevel('state'); setSelectedStateKey(null) }
    else { setAdvDrillLevel('architect'); setSelectedArchitectKey(null) }
    setSelectedSegmentKey(null)
  }, [cohort])

  const isNnaMode = metric === 'nna'

  const donutCenterLabel = selectedSegment
    ? selectedSegment.label
    : parentSegment
    ? parentSegment.label
    : isNnaMode ? 'Net NNA' : 'Total AUA'

  const donutCenterTotal = selectedSegment
    ? (isNnaMode && selectedSegment.value != null ? selectedSegment.value : selectedSegment.aua)
    : parentSegment
    ? (isNnaMode && parentSegment.value != null ? parentSegment.value : parentSegment.aua)
    : (donut?.total || 0)

  const formatCenter = (v: number) =>
    isNnaMode ? formatNumberTo3Digits(v, { unit: '$', includeSign: true }) : formatCurrency(v)

  const donutLabelsConfig = selectedSegment
    ? {
        show: true,
        name: { show: true, fontSize: '12px', fontWeight: 600, color: 'rgba(255,255,255,0.7)', offsetY: -10, formatter: () => selectedSegment.label },
        value: { show: true, fontSize: '22px', fontWeight: 700, color: '#ffffff', offsetY: 6, formatter: () => formatCenter(donutCenterTotal) },
        total: { show: true, showAlways: true, label: selectedSegment.label, fontSize: '11px', fontWeight: 600, color: 'rgba(255,255,255,0.6)', formatter: () => formatCenter(donutCenterTotal) },
      }
    : {
        show: true,
        name: { show: true, fontSize: '12px', fontWeight: 600, color: 'rgba(255,255,255,0.7)', offsetY: -10 },
        value: { show: true, fontSize: '22px', fontWeight: 700, color: '#ffffff', offsetY: 6, formatter: (val: string) => isNnaMode ? formatCenter(donutCenterTotal) : formatCurrency(parseFloat(val)) },
        total: { show: true, showAlways: true, label: donutCenterLabel, fontSize: '11px', fontWeight: 600, color: 'rgba(255,255,255,0.6)', formatter: () => formatCenter(donutCenterTotal) },
      }

  const hasNoDrillData = isDrilledDown && segments.length === 0

  const distributionLabel = isNnaMode
    ? (isDrilledDown
        ? `${cohort === 'geo' ? (selectedStateKey?.toUpperCase() || '') : (selectedArchitectKey?.replace(/_/g, ' ') || '')} -- ${cohort === 'geo' ? 'City' : 'Relationship'} NNA Distribution`
        : selectedSegment
        ? `${selectedSegment.label} -- NNA Flow Distribution`
        : cohort === 'geo' ? 'NNA Flows by Relationship (State)' : 'NNA Flows by Relationship (Advisor)')
    : (selectedSegment
        ? `${selectedSegment.label} -- Account Sizes`
        : parentSegment
        ? `${parentSegment.label} -- Account Sizes`
        : cohort === 'geo' ? 'Account Sizes by State' : 'Account Sizes by Architect')

  // --- CLA: composition view (NMNC/NMEC book breakdown) ---
  if (metric === 'cla') {
    return (
      <ClaSnapshotView
        cohort={cohort}
      />
    )
  }

  return (
    <div className="flex">
      {/* LEFT PARTITION: ApexCharts Donut + Legend + Time Machine */}
      <div className="flex-1 flex items-center justify-center p-6 relative border-r border-white/10">

        {/* Breadcrumb header */}
        <div className="absolute top-4 left-6">
          <div className="flex items-center gap-2">
            {isDrilledDown && (
              <button
                onClick={handleDrillUp}
                className="flex items-center gap-1.5 text-sm font-medium text-white hover:text-white/70 transition-colors mr-2"
              >
                <ChevronLeft size={18} />
                <span>{cohort === 'geo' ? 'States' : 'Architects'}</span>
              </button>
            )}
            <h4 className="text-xs font-medium text-white/60 uppercase tracking-wider">
              {isDrilledDown
                ? (cohort === 'geo' ? selectedStateKey?.toUpperCase() : selectedArchitectKey?.replace(/_/g, ' '))
                : isNnaMode
                ? (cohort === 'geo' ? 'NNA by State' : 'NNA by Architect')
                : (cohort === 'geo' ? 'AUA by State' : 'AUA by Architect')}
            </h4>
            <Tooltip content={
              isNnaMode && isDrilledDown
                ? `Drilled into ${cohort === 'geo' ? selectedStateKey?.toUpperCase() : selectedArchitectKey?.replace(/_/g, ' ')}. Showing ${cohort === 'geo' ? 'city' : 'relationship'}-level NNA distribution.`
                : isNnaMode
                ? `Period NNA across ${cohort === 'geo' ? 'states' : 'architects'}. Click a segment to drill into ${cohort === 'geo' ? 'city' : 'relationship'}-level distribution.`
                : isDrilledDown
                ? `Showing ${cohort === 'geo' ? 'city' : 'client'}-level breakdown. Click a segment to view its account size distribution.`
                : `AUA distribution across ${cohort === 'geo' ? 'states' : 'architects'}. Click a segment to filter, or click through to drill into ${cohort === 'geo' ? 'cities' : 'clients'}.`
            } side="auto">
              <HelpCircle size={14} className="text-white/40 hover:text-white/70 transition-colors cursor-help flex-shrink-0" />
            </Tooltip>
          </div>
        </div>

        <div className="w-full max-w-[700px] flex flex-col gap-6 items-center">
          {/* Donut + Legend row */}
          <div className="h-[450px] flex items-center justify-center relative">
            {hasNoDrillData ? (
              <div className="flex flex-col items-center gap-4 text-center px-8">
                <div className="text-white/60 text-sm">
                  No {cohort === 'geo' ? 'city' : 'client'}-level data available for{' '}
                  <span className="text-white font-medium">
                    {cohort === 'geo' ? selectedStateKey?.toUpperCase() : selectedArchitectKey?.replace(/_/g, ' ')}
                  </span>
                </div>
                <button
                  onClick={handleDrillUp}
                  className="mt-2 px-4 py-2 text-sm bg-white/10 hover:bg-white/15 text-white/80 rounded-lg transition-colors"
                >
                  Back to {cohort === 'geo' ? 'States' : 'Architects'}
                </button>
              </div>
            ) : (
              <>
                <Suspense fallback={<div className="text-white/50 text-sm">Loading chart...</div>}>
                  <Chart
                    key={`snapshot-donut-${cohort}-${geoDrillLevel}-${selectedStateKey ?? 'all'}-${advDrillLevel}-${selectedArchitectKey ?? 'all'}-${selectedSegmentKey ?? 'total'}`}
                    options={{
                      chart: {
                        type: 'donut',
                        background: 'transparent',
                        animations: {
                          enabled: true,
                          speed: 800,
                          animateGradually: { enabled: true, delay: 150 },
                          dynamicAnimation: { enabled: true, speed: 350 },
                        },
                        dropShadow: { enabled: true, top: 4, left: 0, blur: 10, opacity: 0.35 },
                        events: {
                          // eslint-disable-next-line @typescript-eslint/no-explicit-any
                          dataPointSelection: (_event: unknown, _chartContext: unknown, config: any) => {
                            const clickedSegment = segments[config.dataPointIndex]
                            if (clickedSegment) handleSegmentClick(clickedSegment)
                          },
                        },
                      },
                      colors: segments.map((s, i) => {
                        if (s.color) return s.color
                        if (categoryColorMap[s.key]) return categoryColorMap[s.key]
                        if (s.key === 'Other') return OTHER_COLOR
                        const palette = isDrilledDown
                          ? (cohort === 'adv' ? CLIENT_COLORS : CITY_COLORS)
                          : cohort === 'adv' ? ADV_COLORS : GEO_COLORS
                        return palette[i % palette.length]
                      }),
                      labels: segments.map(s => s.label),
                      stroke: { show: true, width: 2, colors: ['rgba(0,0,0,0.3)'] },
                      dataLabels: { enabled: false },
                      plotOptions: {
                        pie: {
                          offsetY: 0,
                          expandOnClick: false,
                          donut: { size: '60%', labels: donutLabelsConfig },
                        },
                      },
                      legend: { show: false },
                      tooltip: { enabled: false },
                      states: {
                        hover: { filter: { type: 'lighten', value: 0.08 } },
                        active: { filter: { type: 'darken', value: 0.1 } },
                      },
                    } as ApexCharts.ApexOptions}
                    series={isNnaMode
                      ? segments.map(s => Math.abs(s.value ?? s.aua))
                      : segments.map(s => s.aua)}
                    type="donut"
                    width={340}
                    height={340}
                  />
                </Suspense>

                {/* Custom Legend */}
                <div className="flex flex-col gap-2 ml-6 max-h-[340px] overflow-y-auto">
                  {segments.map((seg, idx) => {
                    const isSelected = selectedSegmentKey === seg.key
                    // Y6b/Y6d: NNA now drillable at top level when drill data exists
                    const isDrillable = !isDrilledDown && (!isNnaMode || !!nnaDrillData?.[seg.key])

                    return (
                      <button
                        key={seg.key}
                        onClick={() => handleSegmentClick(seg)}
                        className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-all text-left ${
                          isSelected ? 'bg-white/15 ring-1 ring-white/30' : 'hover:bg-white/10'
                        }`}
                      >
                        <div
                          className="w-3 h-3 rounded-full flex-shrink-0"
                          style={{ backgroundColor: seg.color || categoryColorMap[seg.key] || (seg.key === 'Other' ? OTHER_COLOR : (isDrilledDown ? (cohort === 'adv' ? CLIENT_COLORS : CITY_COLORS) : cohort === 'adv' ? ADV_COLORS : GEO_COLORS)[idx % (isDrilledDown ? (cohort === 'adv' ? CLIENT_COLORS : CITY_COLORS) : cohort === 'adv' ? ADV_COLORS : GEO_COLORS).length]) }}
                        />
                        <div className="flex flex-col">
                          <span className="text-sm text-white/80 whitespace-nowrap">
                            {seg.label}
                            {isDrillable && <span className="ml-1 text-white/40">&rarr;</span>}
                          </span>
                          {isNnaMode ? (
                            <span className="text-xs font-medium" style={{ color: (seg.value ?? seg.aua) >= 0 ? '#34d399' : '#f87171' }}>
                              {formatNumberTo3Digits(seg.value ?? seg.aua, { unit: '$', includeSign: true })}
                              <span className="text-white/40 font-normal"> &middot; {(seg.aua_pct ?? 0).toFixed(1)}%</span>
                            </span>
                          ) : (
                            <span className="text-xs text-white/50">
                              {(seg.client_count ?? 0).toLocaleString()} {isDrilledDown && cohort === 'adv' ? 'accounts' : 'clients'} &middot; {(seg.aua_pct ?? 0).toFixed(1)}%
                            </span>
                          )}
                        </div>
                      </button>
                    )
                  })}
                </div>
              </>
            )}
          </div>

          {/* Quarter Strip: NNA reads views.nna; AUA/GEO/ADV reads views.geo/adv */}
          {isNnaMode ? (
            <NnaQuarterlyStrip
              nnaViews={analyticsData.views?.nna as Record<string, NnaPeriodView> | undefined}
              periods={analyticsData.periods}
              cohort={cohort}
              selectedPeriod={selectedPeriod}
              onPeriodChange={setSelectedPeriod}
            />
          ) : hasTimeMachineData && rawView ? (
            <DistributionQuarterlyStrip
              view={rawView as PartnerAnalyticsViewWithPeriods}
              periods={analyticsData.periods}
              selectedPeriod={selectedPeriod}
              onPeriodChange={setSelectedPeriod}
              parentSegmentKey={parentSegment?.key || null}
              childSegmentKey={isDrilledDown && selectedSegment ? selectedSegment.key : null}
              cohort={cohort}
            />
          ) : null}

          {/* Footnote */}
          <p className="text-[10px] text-center mt-2 px-4">
            <span className="text-amber-400 font-bold">
              {isNnaMode && isDrilledDown
                ? `${cohort === 'geo' ? 'City' : 'Relationship'}-level NNA drill for ${cohort === 'geo' ? selectedStateKey?.toUpperCase() : selectedArchitectKey?.replace(/_/g, ' ')}.`
                : isNnaMode
                ? `${cohort === 'geo' ? 'State' : 'Advisor'}-level period NNA from Black Diamond.`
                : isDrilledDown
                ? `${cohort === 'geo' ? 'City' : 'Client'}-level AUA from Black Diamond account data.`
                : `${cohort === 'geo' ? 'State' : 'Architect'}-level AUA from Black Diamond account data.`}
            </span>
            <span className="text-white/40">
              {isNnaMode && isDrilledDown
                ? ' Click back to return to top level.'
                : isNnaMode
                ? ` Click a segment to drill into ${cohort === 'geo' ? 'city' : 'relationship'}-level NNA distribution.`
                : ` Click a segment to filter.${!isDrilledDown ? ' Click through to drill into sub-segments.' : ''}`}
            </span>
          </p>
        </div>
      </div>

      {/* RIGHT PARTITION: Distribution histogram (AUA: account sizes; NNA: relationship flows) */}
      <div className="flex-1 flex items-center justify-center p-6 relative">
        <div className="absolute top-4 left-6">
          <div className="flex items-center gap-2">
            <h4 className="text-xs font-medium text-white/60 uppercase tracking-wider">
              {distributionLabel}
            </h4>
            <Tooltip
              content={isNnaMode
                ? 'Per-relationship period NNA flow distribution. Symmetric log-spaced bins around zero. Red = net outflow relationships; blue = net inflow. Pending data deploy (Script 09).'
                : 'Bell curve of funded account sizes (log-scaled bins). Percentile markers (P10-P90) show the spread. When viewing a historical quarter, deltas vs current appear below each percentile.'}
              side="auto"
            >
              <HelpCircle size={14} className="text-white/40 hover:text-white/70 transition-colors cursor-help flex-shrink-0" />
            </Tooltip>
          </div>
        </div>

        <div className="w-full max-w-[700px] flex flex-col gap-6 items-center">
          {distributionData && distributionData.count > 0 && distributionData.histogram?.counts?.some(c => c > 0) ? (
            <>
              <div className="h-[450px] w-full min-w-0">
                <SnapshotDistributionChart
                  data={distributionData}
                  accentColor={selectedSegment?.color || parentSegment?.color || 'hsl(var(--primary))'}
                  globalMaxCount={globalMaxCount}
                  isNnaMode={isNnaMode}
                />
              </div>
              {isNnaMode ? (
                <NnaSplitMetricsStrip data={distributionData} />
              ) : (
                <SnapshotDistributionMetrics data={distributionData} currentData={currentDistributionData} isNnaMode={isNnaMode} />
              )}
              <p className="text-[10px] text-center mt-2 px-4">
                {isNnaMode ? (
                  <>
                    <span className="text-white/40">Per-relationship NNA flows. Symmetric log bins, $0 at center.</span>
                    <br />
                    <span className="text-white/40">Relationships with net flows between -$1,000 and $1,000 are excluded from this distribution.</span>
                  </>
                ) : (
                  <>
                    <span className="text-amber-400 font-bold">Excludes accounts with $0 balance (unfunded).</span>
                    <span className="text-white/40"> Distribution reflects funded accounts only, log-spaced bins.</span>
                  </>
                )}
              </p>
            </>
          ) : (
            <div className="flex flex-col items-center justify-center h-[380px] gap-3 text-center px-8">
              {isNnaMode ? (
                <>
                  <p className="text-white/50 text-sm">
                    {selectedSegment
                      ? `${selectedSegment.label} relationship flow distribution`
                      : `${cohort === 'geo' ? 'State' : 'Advisor'} relationship flow distribution`}
                  </p>
                  <p className="text-white/30 text-xs">Pending Script 09 deploy (D1)</p>
                </>
              ) : (
                <p className="text-white/60 text-sm">
                  {isDrilledDown
                    ? `Select a ${cohort === 'geo' ? 'city' : 'client'} to view account size distribution`
                    : `Select a ${cohort === 'geo' ? 'state' : 'architect'} to view account size distribution`}
                </p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// ============================================================================
// NNA QUARTERLY STRIP — shows period NNA from views.nna (not views.geo/adv)
// ============================================================================

interface NnaQuarterlyStripProps {
  nnaViews: Record<string, NnaPeriodView> | undefined
  periods?: PeriodsMetadata
  cohort: CohortOption
  selectedPeriod: TimePeriodKey
  onPeriodChange: (period: TimePeriodKey) => void
}

function NnaQuarterlyStrip({ nnaViews, periods, cohort, selectedPeriod, onPeriodChange }: NnaQuarterlyStripProps) {
  const getNna = (period: TimePeriodKey): number => {
    const v = nnaViews?.[period]
    if (!v) return 0
    const cohortView = cohort === 'geo' ? v.geo : v.adv
    return cohortView?.metrics?.nna ?? 0
  }

  const periodDefs: { key: TimePeriodKey; label: string }[] = [
    { key: 'current', label: periods?.current?.label || 'Current' },
    { key: 'q1',      label: periods?.q1?.label      || 'Last Qtr' },
    { key: 'q2',      label: periods?.q2?.label      || '2Q Ago' },
    { key: 'q3',      label: periods?.q3?.label      || '3Q Ago' },
  ]

  return (
    <div className="w-full px-6 py-3 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center">
      <div className="flex flex-wrap items-center justify-evenly gap-x-6 gap-y-3 w-full">
        {periodDefs.map(({ key, label }) => {
          if (!nnaViews?.[key]) return null
          const nna = getNna(key)
          const isSelected = selectedPeriod === key
          const isPositive = nna >= 0
          return (
            <button
              key={key}
              onClick={() => onPeriodChange(key)}
              className={`flex flex-col items-center px-3 py-1.5 rounded min-w-[100px] transition-all ${
                isSelected
                  ? 'bg-[hsl(253,74%,85%)]/15 border border-[hsl(253,74%,85%)]/40'
                  : 'border border-transparent hover:bg-white/5'
              }`}
            >
              <div className="text-xs text-white/50 mb-1">{label}</div>
              <div className={`text-base font-bold ${isPositive ? 'text-emerald-400' : 'text-red-400'}`}>
                {formatNumberTo3Digits(nna, { unit: '$', includeSign: true })}
              </div>
              <div className="text-[10px] text-white/30 mt-0.5">Period NNA</div>
            </button>
          )
        })}
      </div>
    </div>
  )
}

// ============================================================================
// DISTRIBUTION QUARTERLY STRIP — AUA per period (matches AUMGrowthMetrics)
// ============================================================================

interface DistributionQuarterlyStripProps {
  view: PartnerAnalyticsViewWithPeriods
  periods?: PeriodsMetadata
  selectedPeriod: TimePeriodKey
  onPeriodChange: (period: TimePeriodKey) => void
  parentSegmentKey: string | null
  childSegmentKey: string | null
  cohort: CohortOption
}

function DistributionQuarterlyStrip({
  view, periods, selectedPeriod, onPeriodChange,
  parentSegmentKey, childSegmentKey, cohort,
}: DistributionQuarterlyStripProps) {
  const getAuaForPeriod = (period: TimePeriodKey): number => {
    const snap = period === 'current' ? view.current : view[period]
    if (!snap) return 0

    if (childSegmentKey && parentSegmentKey) {
      const parentSeg = snap.donut?.segments?.find((s: DonutSegment) => s.key === parentSegmentKey)
      if (cohort === 'geo' && parentSeg?.cities) {
        const city = parentSeg.cities.find((c: CitySegment) => c.key === childSegmentKey)
        if (city) return city.aua
      }
      if (cohort === 'adv' && parentSeg?.clients) {
        const client = parentSeg.clients.find((c: ClientSegment) => c.key === childSegmentKey)
        if (client) return client.aua
      }
      return 0
    }

    if (parentSegmentKey) {
      const seg = snap.donut?.segments?.find((s: DonutSegment) => s.key === parentSegmentKey)
      return seg?.aua || 0
    }

    return snap.metrics?.aua || snap.donut?.total || 0
  }

  // Resolve AUA for each period
  const currentAua = getAuaForPeriod('current')
  const q1Aua = getAuaForPeriod('q1')
  const q2Aua = getAuaForPeriod('q2')
  const q3Aua = getAuaForPeriod('q3')

  // QoQ growth: each period vs its immediately prior quarter
  const calcQoQ = (thisQtr: number, priorQtr: number): number | null => {
    if (priorQtr === 0) return null
    return ((thisQtr / priorQtr) - 1) * 100
  }

  const currentQoQ = q1Aua > 0 ? calcQoQ(currentAua, q1Aua) : null
  const q1QoQ = q2Aua > 0 ? calcQoQ(q1Aua, q2Aua) : null
  const q2QoQ = q3Aua > 0 ? calcQoQ(q2Aua, q3Aua) : null

  const formatPctChange = (pct: number | null): string => {
    if (pct === null || isNaN(pct)) return ''
    const sign = pct >= 0 ? '+' : ''
    return `${sign}${pct.toFixed(1)}%`
  }

  const getPctColor = (pct: number | null): string => {
    if (pct === null) return 'text-white/40'
    return pct > 0 ? 'text-emerald-400' : pct < 0 ? 'text-red-400' : 'text-white/40'
  }

  const getGrowthDotColor = (pct: number | null): string => {
    if (pct === null) return 'bg-white/30'
    return pct > 0 ? 'bg-emerald-400' : pct < 0 ? 'bg-red-400' : 'bg-white/30'
  }

  const historicalPeriods: { key: TimePeriodKey; label: string; aua: number; qoq: number | null }[] = [
    { key: 'q1', label: periods?.q1?.label || 'Last Qtr', aua: q1Aua, qoq: q1QoQ },
    { key: 'q2', label: periods?.q2?.label || '2Q Ago', aua: q2Aua, qoq: q2QoQ },
    { key: 'q3', label: periods?.q3?.label || '3Q Ago', aua: q3Aua, qoq: null },
  ]

  return (
    <div className="w-full px-6 py-3 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center">
      <div className="flex flex-wrap items-center justify-evenly gap-x-6 gap-y-3 w-full">
        {/* Current AUA - Accented Primary Metric */}
        <button
          onClick={() => onPeriodChange('current')}
          className={`flex flex-col items-center px-4 py-1.5 rounded min-w-[100px] transition-all ${
            selectedPeriod === 'current'
              ? 'bg-[hsl(253,74%,85%)]/15 border border-[hsl(253,74%,85%)]/40'
              : 'bg-white/5 border border-white/10 hover:bg-white/10'
          }`}
        >
          <div className="text-xs text-white/90 font-semibold mb-1">Total AUA</div>
          <div className="flex items-center gap-1.5">
            <div className="text-lg font-bold text-white">
              {formatCurrency(currentAua)}
            </div>
            {currentQoQ !== null && (
              <span className={`text-xs font-medium ${getPctColor(currentQoQ)}`}>
                {formatPctChange(currentQoQ)}
              </span>
            )}
          </div>
        </button>

        {/* Historical quarter-end AUA values with QoQ growth */}
        {historicalPeriods.map(({ key, label, aua, qoq }) => {
          const snap = view[key]
          if (!snap) return null
          const isSelected = selectedPeriod === key

          return (
            <button
              key={key}
              onClick={() => onPeriodChange(key)}
              className={`flex flex-col items-center min-w-[100px] px-3 py-1.5 rounded transition-all ${
                isSelected
                  ? 'bg-[hsl(253,74%,85%)]/10 border border-[hsl(253,74%,85%)]/30'
                  : 'border border-transparent hover:bg-white/5'
              }`}
            >
              <div className="flex items-center gap-1.5 mb-1">
                <div className={`w-2 h-2 rounded-full ${getGrowthDotColor(qoq)}`} />
                <div className="text-xs text-white/50">{label}</div>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="text-sm font-semibold text-white">
                  {aua > 0 ? formatCurrency(aua) : 'N/A'}
                </span>
                {qoq !== null && (
                  <span className={`text-xs font-medium ${getPctColor(qoq)}`}>
                    {formatPctChange(qoq)}
                  </span>
                )}
              </div>
            </button>
          )
        })}
      </div>
    </div>
  )
}

// ============================================================================
// SNAPSHOT DISTRIBUTION CHART — bell curve with percentile reference lines
// ============================================================================

/** Compute weighted percentile from histogram bins/counts (linear interpolation). */
function histogramPercentile(midpoints: number[], counts: number[], pct: number): number | null {
  const total = counts.reduce((s, c) => s + c, 0)
  if (total === 0) return null
  const target = total * (pct / 100)
  let cum = 0
  for (let i = 0; i < counts.length; i++) {
    cum += counts[i]
    if (cum >= target) return midpoints[i]
  }
  return midpoints[midpoints.length - 1]
}

interface NnaSplitPercentiles {
  outflow: { count: number; p25: number | null; median: number | null; p75: number | null }
  inflow:  { count: number; p25: number | null; median: number | null; p75: number | null }
}

/** Split NNA histogram at zero and compute magnitude-ranked percentiles on each side.
 *  Outflows: bins with negative midpoints. Reversed before percentile computation so
 *    P25 = small outflow (near zero), P75 = large outflow (far left on chart).
 *    Matches Y6c intent: largest outflows are top-ranked (P90/P75), not bottom-ranked.
 *  Inflows: bins with positive midpoints, ascending. Standard percentiles. */
function computeNnaSplitPercentiles(data: DistributionStats): NnaSplitPercentiles {
  const { bins, counts } = data.histogram
  const outMids: number[] = [], outCounts: number[] = []
  const inMids: number[] = [], inCounts: number[] = []

  for (let i = 0; i < counts.length; i++) {
    const lo = bins[i] ?? 0
    const hi = bins[i + 1] ?? lo
    const mid = (lo + hi) / 2
    if (mid < 0) { outMids.push(mid); outCounts.push(counts[i]) }
    else if (mid > 0) { inMids.push(mid); inCounts.push(counts[i]) }
  }

  // Reverse outflows so percentiles rank by magnitude: P25 = small outflow, P75 = large outflow.
  // Without reversal, histogramPercentile counts from the most-negative end, making P25 the
  // largest outflow — the opposite of magnitude ranking.
  const revOutMids = [...outMids].reverse()
  const revOutCounts = [...outCounts].reverse()

  return {
    outflow: {
      count: outCounts.reduce((s, c) => s + c, 0),
      p25: histogramPercentile(revOutMids, revOutCounts, 25),
      median: histogramPercentile(revOutMids, revOutCounts, 50),
      p75: histogramPercentile(revOutMids, revOutCounts, 75),
    },
    inflow: {
      count: inCounts.reduce((s, c) => s + c, 0),
      p25: histogramPercentile(inMids, inCounts, 25),
      median: histogramPercentile(inMids, inCounts, 50),
      p75: histogramPercentile(inMids, inCounts, 75),
    },
  }
}

interface SnapshotDistributionChartProps {
  data: DistributionStats
  accentColor?: string
  globalMaxCount?: number
  isNnaMode?: boolean
}

function SnapshotDistributionChart({ data, accentColor = '#5e72e4', globalMaxCount, isNnaMode = false }: SnapshotDistributionChartProps) {
  // NNA distributions have extreme center peaks that dwarf the tails — use log scale
  const useLogScale = isNnaMode
  // Y6: In NNA mode, filter out the two zero-adjacent bins (the bin whose right edge is 0
  // and the bin whose left edge is 0). These always have count=0 due to the $1K materiality
  // threshold and appear as "-$1K-$0" / "$0-$1K" regardless of the exact abs_min value.
  // Checking hi===0 / lo===0 is more reliable than a hardcoded ±1000 comparison because
  // abs_min may be slightly above $1000, placing the actual edges at e.g. -$1050 and $1050.
  const filteredIndices = data.histogram.bin_labels.map((_, index) => index).filter(index => {
    if (!isNnaMode) return true
    const lo = data.histogram.bins?.[index] ?? null
    const hi = data.histogram.bins?.[index + 1] ?? null
    if (lo === null || hi === null) return true
    return hi !== 0 && lo !== 0
  })
  const chartData = filteredIndices.map(index => ({
    bin: data.histogram.bin_labels[index],
    count: useLogScale ? Math.max(data.histogram.counts[index], 0.5) : data.histogram.counts[index],
    rawCount: data.histogram.counts[index],
  }))

  const parseDollarValue = (binLabel: string): number => {
    if (binLabel.includes('+')) {
      const match = binLabel.match(/\$([\d.]+)([KMB]?)\+/)
      if (match) {
        const num = parseFloat(match[1])
        const mult = match[2] === 'K' ? 1000 : match[2] === 'M' ? 1000000 : match[2] === 'B' ? 1000000000 : 1
        return num * mult
      }
    }
    const parts = binLabel.split('-')
    if (parts.length === 2) {
      const parseVal = (s: string): number => {
        const m = s.match(/\$([\d.]+)([KMB]?)/)
        if (!m) return 0
        const mult = m[2] === 'K' ? 1000 : m[2] === 'M' ? 1000000 : m[2] === 'B' ? 1000000000 : 1
        return parseFloat(m[1]) * mult
      }
      return (parseVal(parts[0]) + parseVal(parts[1])) / 2
    }
    return 0
  }

  const findBin = (value: number | null): string | null => {
    if (value === null) return null
    let best = null, minDiff = Infinity
    for (const lbl of data.histogram.bin_labels) {
      const diff = Math.abs(parseDollarValue(lbl) - value)
      if (diff < minDiff) { minDiff = diff; best = lbl }
    }
    return best
  }

  useEffect(() => {
    const t = setTimeout(() => window.dispatchEvent(new Event('resize')), 100)
    return () => clearTimeout(t)
  }, [])

  // For NNA mode, find the bin label whose numeric midpoint is closest to a signed value
  const findBinByNumericValue = (value: number): string | null => {
    const { bins, bin_labels } = data.histogram
    let best: string | null = null, minDiff = Infinity
    for (let i = 0; i < bin_labels.length; i++) {
      const lo = bins[i] ?? 0
      const hi = bins[i + 1] ?? lo
      const mid = (lo + hi) / 2
      const diff = Math.abs(mid - value)
      if (diff < minDiff) { minDiff = diff; best = bin_labels[i] }
    }
    return best
  }

  const nnaSplit = isNnaMode ? computeNnaSplitPercentiles(data) : null

  // NNA: split percentile lines — outflows (negative, red) + inflows (positive, green/blue)
  // Outflows: P75=large outflow (far left, red), P25=small outflow (near zero, yellow)
  const percentileLines = isNnaMode && nnaSplit ? [
    // Net outflow side — P75 is most negative (large), P25 is near zero (small)
    { value: nnaSplit.outflow.p75, label: 'P75', color: '#ef4444' },
    { value: nnaSplit.outflow.median, label: 'Med', color: '#fb923c' },
    { value: nnaSplit.outflow.p25, label: 'P25', color: '#fbbf24' },
    // Net inflow side (positive — P25 near zero, P75 far right)
    { value: nnaSplit.inflow.p25, label: 'P25', color: '#86efac' },
    { value: nnaSplit.inflow.median, label: 'Med', color: '#34d399' },
    { value: nnaSplit.inflow.p75, label: 'P75', color: '#60a5fa' },
  ] : [
    { value: data.percentiles.p10, label: 'P10', color: '#ef4444' },
    { value: data.percentiles.p25, label: 'P25', color: '#fb923c' },
    { value: data.median, label: 'Median', color: '#34d399' },
    { value: data.percentiles.p75, label: 'P75', color: '#60a5fa' },
    { value: data.percentiles.p90, label: 'P90', color: '#a78bfa' },
  ]

  return (
    <div className="w-full h-full relative">
      <div
        className="absolute flex items-center justify-center pointer-events-none"
        style={{ top: '30px', bottom: '50px', left: '-20px', width: '16px' }}
      >
        <span className="text-[11px] text-white/50 whitespace-nowrap" style={{ writingMode: 'vertical-rl', transform: 'rotate(180deg)' }}>
          {isNnaMode ? 'Relationships (log)' : 'Number of Accounts'}
</span>
      </div>
      <div
        className="absolute -translate-x-1/2 pointer-events-none"
        style={{ bottom: '6px', left: 'calc(50% + 15px)' }}
      >
        <span className="text-[11px] text-white/50">{isNnaMode ? 'Period NNA' : 'Account Size'}</span>
      </div>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={chartData} margin={{ top: 30, right: 10, left: 0, bottom: 50 }}>
          <defs>
            <linearGradient id="snapshotDistGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={accentColor} stopOpacity={0.8} />
              <stop offset="95%" stopColor={accentColor} stopOpacity={0.1} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
          <XAxis
            dataKey="bin"
            stroke="rgba(255,255,255,0.5)"
            height={50}
            interval={0}
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            tick={(props: any) => {
              const { x, y, payload } = props
              return (
                <g transform={`translate(${x},${y})`}>
                  <text
                    x={0}
                    y={0}
                    dy={12}
                    textAnchor="end"
                    transform="rotate(-45)"
                    fontSize={7}
                    fill="rgba(255,255,255,0.7)"
                  >
                    {payload.value}
                  </text>
                </g>
              )
            }}
          />
          <YAxis
            stroke="rgba(255,255,255,0.5)"
            tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.7)' }}
            width={40}
            scale={useLogScale ? 'log' : 'auto'}
            domain={useLogScale ? [1, 'auto'] : globalMaxCount ? [0, globalMaxCount] : ['auto', 'auto']}
            allowDataOverflow={false}
            tickFormatter={useLogScale ? (v: number) => (v < 1 ? '' : v.toLocaleString()) : undefined}
          />
          <RechartsTooltip
            cursor={{ stroke: `${accentColor}80`, strokeWidth: 2 }}
            content={({ active, payload, label }) => {
              if (!active || !payload || payload.length === 0) return null
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              const count = useLogScale ? ((payload[0]?.payload as any)?.rawCount ?? payload[0]?.value) as number : payload[0]?.value as number
              const formattedLabel = typeof label === 'string'
                ? label.replace(/(\$[\d.]+[KMB]?)-(\$[\d.]+[KMB]?\+?)/, '$1 - $2')
                : label
              return (
                <div className="bg-[hsl(var(--semantic-background-chartTooltipBg))] rounded-lg px-4 py-3 shadow-xl" style={{ border: `2px solid ${accentColor}` }}>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between gap-4">
                      <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm">{isNnaMode ? 'NNA Range' : 'Account Size'}</span>
                      <span className="text-[hsl(var(--semantic-text-chartTooltip))] font-semibold text-sm">{formattedLabel}</span>
                    </div>
                    <div className="flex items-center justify-between gap-4">
                      <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm">{isNnaMode ? 'Relationship Count' : 'Account Count'}</span>
                      <span className="text-[hsl(var(--semantic-text-chartTooltip))] font-semibold text-sm">{count?.toLocaleString()}</span>
                    </div>
                  </div>
                </div>
              )
            }}
          />
          <Area
            type="monotone"
            dataKey="count"
            stroke="hsl(253, 74%, 85%)"
            strokeWidth={2}
            fill="url(#snapshotDistGradient)"
            isAnimationActive
            animationDuration={800}
          />
          {percentileLines.map(line => {
            const bin = isNnaMode ? findBinByNumericValue(line.value ?? 0) : findBin(line.value)
            if (!bin || line.value === null) return null
            return (
              <ReferenceLine
                key={line.label}
                x={bin}
                stroke={line.color}
                strokeWidth={2}
                strokeDasharray="5 5"
                label={{ value: line.label, position: 'top', fill: line.color, fontSize: 10, fontWeight: 600 }}
              />
            )
          })}
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}

// ============================================================================
// SNAPSHOT DISTRIBUTION METRICS — P10/P25/Median/P75/P90 strip
// (Matches AccountDistributionMetrics from Model Portfolios)
// ============================================================================

function SnapshotDistributionMetrics({ data, currentData, isNnaMode = false }: { data: DistributionStats; currentData?: DistributionStats | null; isNnaMode?: boolean }) {
  const pctDelta = (val: number | null, curVal: number | null): string | null => {
    if (val === null || curVal === null || curVal === 0 || !currentData) return null
    const delta = ((val - curVal) / curVal) * 100
    return `${delta >= 0 ? '+' : ''}${delta.toFixed(1)}%`
  }

  const deltaColorClass = (val: number | null, curVal: number | null): string => {
    if (val === null || curVal === null || curVal === 0) return ''
    return val >= curVal ? 'text-emerald-400' : 'text-red-400'
  }

  const renderDelta = (val: number | null, curVal: number | null) => {
    const delta = pctDelta(val, curVal)
    if (!delta) return null
    return <div className={`text-[9px] mt-0.5 ${deltaColorClass(val, curVal)}`}>{delta} vs current</div>
  }

  return (
    <div className="w-full px-6 py-3 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center">
      <div className="flex flex-wrap items-center justify-evenly gap-x-4 gap-y-3 w-full">
        {/* Total Accounts / Total Relationships */}
        <div className="flex flex-col items-center px-4 py-1.5 rounded bg-[hsl(253,74%,85%)]/15 border border-[hsl(253,74%,85%)]/40 min-w-[100px]">
          <div className="text-xs text-white/90 font-semibold mb-1">{isNnaMode ? 'Total Relationships' : 'Total Accounts'}</div>
          <div className="text-lg font-bold text-white">{data.count.toLocaleString()}</div>
        </div>

        {/* P10 */}
        <div className="flex flex-col items-center min-w-[80px]">
          <div className="flex items-center gap-1.5 mb-1">
            <div className="w-2 h-2 rounded-full bg-red-500" />
            <div className="text-xs text-white/50">P10</div>
          </div>
          <div className="text-sm font-semibold text-white">
            {data.percentiles.p10 !== null ? formatCurrency(data.percentiles.p10) : 'N/A'}
          </div>
          {renderDelta(data.percentiles.p10, currentData?.percentiles.p10 ?? null)}
        </div>

        {/* P25 */}
        <div className="flex flex-col items-center min-w-[80px]">
          <div className="flex items-center gap-1.5 mb-1">
            <div className="w-2 h-2 rounded-full bg-orange-400" />
            <div className="text-xs text-white/50">P25</div>
          </div>
          <div className="text-sm font-semibold text-white">
            {data.percentiles.p25 !== null ? formatCurrency(data.percentiles.p25) : 'N/A'}
          </div>
          {renderDelta(data.percentiles.p25, currentData?.percentiles.p25 ?? null)}
        </div>

        {/* Median */}
        <div className="flex flex-col items-center px-3 py-1.5 rounded bg-emerald-500/10 border border-emerald-500/30 min-w-[100px]">
          <div className="flex items-center gap-1.5 mb-1">
            <div className="w-2 h-2 rounded-full bg-emerald-400" />
            <div className="text-xs text-emerald-300/80 font-semibold">Median</div>
          </div>
          <div className="text-base font-bold text-emerald-400">
            {data.median !== null ? formatCurrency(data.median) : 'N/A'}
          </div>
          {renderDelta(data.median, currentData?.median ?? null)}
        </div>

        {/* P75 */}
        <div className="flex flex-col items-center min-w-[80px]">
          <div className="flex items-center gap-1.5 mb-1">
            <div className="w-2 h-2 rounded-full bg-blue-400" />
            <div className="text-xs text-white/50">P75</div>
          </div>
          <div className="text-sm font-semibold text-white">
            {data.percentiles.p75 !== null ? formatCurrency(data.percentiles.p75) : 'N/A'}
          </div>
          {renderDelta(data.percentiles.p75, currentData?.percentiles.p75 ?? null)}
        </div>

        {/* P90 */}
        <div className="flex flex-col items-center min-w-[80px]">
          <div className="flex items-center gap-1.5 mb-1">
            <div className="w-2 h-2 rounded-full bg-purple-400" />
            <div className="text-xs text-white/50">P90</div>
          </div>
          <div className="text-sm font-semibold text-white">
            {data.percentiles.p90 !== null ? formatCurrency(data.percentiles.p90) : 'N/A'}
          </div>
          {renderDelta(data.percentiles.p90, currentData?.percentiles.p90 ?? null)}
        </div>
      </div>
    </div>
  )
}

// ============================================================================
// NNA SPLIT METRICS STRIP — outflow/inflow absolute-value percentiles
// ============================================================================

function NnaSplitMetricsStrip({ data }: { data: DistributionStats }) {
  const split = computeNnaSplitPercentiles(data)
  // For outflows, display as absolute magnitude (positive) since the "Outflows" label
  // already conveys direction. For inflows, show as-is (already positive).
  const fmtAbs = (v: number | null) => v !== null ? formatCurrency(Math.abs(v)) : 'N/A'

  const renderSide = (side: typeof split.outflow, label: string, dotColor: string, reversed = false) => (
    <div className="flex flex-col items-center gap-2 flex-1">
      <div className="flex items-center gap-1.5 mb-0.5">
        <div className="w-2 h-2 rounded-full" style={{ backgroundColor: dotColor }} />
        <span className="text-[10px] font-semibold text-white/70 uppercase tracking-wider">{label}</span>
        <span className="text-[10px] text-white/40">({side.count.toLocaleString()})</span>
      </div>
      <div className="flex items-center gap-4">
        <div className="flex flex-col items-center">
          <span className="text-[9px] text-white/40">{reversed ? 'P75' : 'P25'}</span>
          <span className="text-xs font-medium text-white/80">{reversed ? fmtAbs(side.p75) : fmtAbs(side.p25)}</span>
        </div>
        <div className="flex flex-col items-center px-2 py-0.5 rounded bg-white/5 border border-white/10">
          <span className="text-[9px] text-white/50 font-semibold">Median</span>
          <span className="text-sm font-bold text-white">{fmtAbs(side.median)}</span>
        </div>
        <div className="flex flex-col items-center">
          <span className="text-[9px] text-white/40">{reversed ? 'P25' : 'P75'}</span>
          <span className="text-xs font-medium text-white/80">{reversed ? fmtAbs(side.p25) : fmtAbs(side.p75)}</span>
        </div>
      </div>
    </div>
  )

  return (
    <div className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 flex items-stretch gap-4">
      {renderSide(split.outflow, 'Net Outflows', '#ef4444', true)}
      <div className="w-px bg-white/15 self-stretch" />
      {renderSide(split.inflow, 'Net Inflows', '#34d399')}
    </div>
  )
}

// ============================================================================
// CLA SNAPSHOT VIEW (Composition View -- NMNC/NMEC book breakdown)
// ============================================================================

const NMNC_COLOR = '#16A34A'
const NMEC_COLOR = '#2563EB'

interface ClaSnapshotViewProps {
  cohort: CohortOption
}

function ClaSnapshotView({ cohort: _cohort }: ClaSnapshotViewProps) {
  const { data: headerData, isLoading: headerLoading } = useQuery<HeaderMetricsResponse>({
    queryKey: ['headerMetrics'],
    queryFn: getHeaderMetrics,
    staleTime: 5 * 60 * 1000,
  })

  if (headerLoading) {
    return <LoadingInline className="py-12" />
  }

  if (!headerData) {
    return (
      <div className="flex items-center justify-center min-h-[360px]">
        <p className="text-white/40 text-sm">CLA data not available</p>
      </div>
    )
  }

  const total = headerData.total
  const nmnc_pct = total.new_client_pct
  const nmec_pct = 100 - nmnc_pct

  // Quarter strip: find last timeseries point at or before each quarter-end date
  // Guard: dates may be absent in older cached header_metrics.json responses
  const dates = headerData.dates as { q0: string; q1: string; q2: string; q3: string } | undefined
  const timeseries: RollingTimeseriesDataPoint[] = headerData.timeseries?.data ?? []
  const quarterKeys = ['q0', 'q1', 'q2', 'q3'] as const
  const quarterStrip = !dates ? [] : quarterKeys
    .map(qk => {
      const qDate = dates[qk]
      if (!qDate) return null
      const pts = timeseries.filter(pt => pt.date <= qDate)
      const pt = pts.length > 0 ? pts[pts.length - 1] : null
      const pct = pt?.nmnc_pct ?? (qk === 'q0' ? nmnc_pct : null)
      if (pct === null) return null
      const d = new Date(qDate + 'T00:00:00')
      const qNum = Math.ceil((d.getMonth() + 1) / 3)
      return { key: qk, label: `Q${qNum} ${d.getFullYear()}`, nmnc_pct: pct, nmec_pct: 100 - pct }
    })
    .filter((x): x is NonNullable<typeof x> => x !== null)

  // Distribution histogram: merge NMNC and NMEC bins by bin_labels
  // Guard: account_distribution may be absent in older cached header_metrics.json responses
  const nmnc_dist: SegmentDistribution | undefined = headerData.account_distribution?.by_segment?.NMNC
  const nmec_dist: SegmentDistribution | undefined = headerData.account_distribution?.by_segment?.NMEC
  const histData = nmnc_dist?.histogram.bin_labels.map((label, i) => ({
    label,
    nmnc: nmnc_dist.histogram.counts[i] ?? 0,
    nmec: nmec_dist?.histogram.counts[i] ?? 0,
  })) ?? []

  const donutData = [
    { name: 'New Clients (NMNC)', value: nmnc_pct, color: NMNC_COLOR },
    { name: 'Existing Clients (NMEC)', value: nmec_pct, color: NMEC_COLOR },
  ]

  return (
    <div className="flex">

      {/* LEFT PARTITION: Donut + Legend + Quarter Strip */}
      <div className="flex-1 flex flex-col items-center justify-start p-6 gap-6 border-r border-white/10">

        {/* Donut + Legend row */}
        <div className="flex items-center gap-8">

          {/* Donut */}
          <div className="relative flex-shrink-0" style={{ width: 200, height: 200 }}>
            <PieChart width={200} height={200}>
              <Pie
                data={donutData}
                dataKey="value"
                cx={100}
                cy={100}
                innerRadius={60}
                outerRadius={92}
                stroke="rgba(0,0,0,0.2)"
                strokeWidth={2}
                startAngle={90}
                endAngle={-270}
              >
                {donutData.map((seg, i) => (
                  <Cell key={i} fill={seg.color} />
                ))}
              </Pie>
            </PieChart>
            {/* Center label */}
            <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
              <p className="text-2xl font-black text-white">{nmnc_pct.toFixed(1)}%</p>
              <p className="text-[10px] text-white/40 uppercase tracking-wide">New Clients</p>
            </div>
          </div>

          {/* Legend */}
          <div className="flex flex-col gap-5">
            <div className="flex flex-col gap-1">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full flex-shrink-0" style={{ backgroundColor: NMNC_COLOR }} />
                <span className="text-sm font-semibold text-white">New Clients (NMNC)</span>
              </div>
              <p className="text-2xl font-black ml-5" style={{ color: NMNC_COLOR }}>{nmnc_pct.toFixed(1)}%</p>
              <p className="text-xs text-white/40 ml-5">{total.new_client_count.toLocaleString()} relationships</p>
              <p className="text-xs text-white/50 ml-5">{formatCurrency(total.new_client_aua)}</p>
            </div>
            <div className="flex flex-col gap-1">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full flex-shrink-0" style={{ backgroundColor: NMEC_COLOR }} />
                <span className="text-sm font-semibold text-white">Existing Clients (NMEC)</span>
              </div>
              <p className="text-2xl font-black ml-5" style={{ color: NMEC_COLOR }}>{nmec_pct.toFixed(1)}%</p>
              <p className="text-xs text-white/40 ml-5">{total.existing_client_count.toLocaleString()} relationships</p>
              <p className="text-xs text-white/50 ml-5">{formatCurrency(total.existing_client_aua)}</p>
            </div>
          </div>
        </div>

        {/* Quarter strip -- read-only new client mix trend */}
        {quarterStrip.length > 0 && (
          <div className="flex flex-col items-center gap-2 pt-4 border-t border-white/10 w-full">
            <p className="text-[10px] text-white/30 uppercase tracking-wider">New Client Mix by Quarter</p>
            <div className="flex items-end gap-4 justify-center">
              {[...quarterStrip].reverse().map(qd => (
                <div key={qd.key} className="flex flex-col items-center gap-1">
                  <p className="text-[10px] font-medium text-white/50">{qd.nmnc_pct.toFixed(0)}%</p>
                  <div className="w-14 h-8 rounded overflow-hidden flex">
                    <div style={{ width: `${qd.nmnc_pct}%`, backgroundColor: NMNC_COLOR, opacity: 0.8 }} />
                    <div style={{ flex: 1, backgroundColor: NMEC_COLOR, opacity: 0.8 }} />
                  </div>
                  <p className="text-[10px] text-white/30">{qd.label}</p>
                </div>
              ))}
            </div>
          </div>
        )}

      </div>

      {/* RIGHT PARTITION: NMNC vs NMEC account size distribution */}
      <div className="flex-1 flex flex-col justify-start p-6 gap-4">
        <h4 className="text-xs font-medium text-white/60 uppercase tracking-wider text-center">
          Account Size Distribution
        </h4>

        <div className="h-[260px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={histData} margin={{ top: 5, right: 10, left: 0, bottom: 50 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
              <XAxis
                dataKey="label"
                tick={{ fill: 'rgba(255,255,255,0.4)', fontSize: 7 }}
                axisLine={{ stroke: 'rgba(255,255,255,0.1)' }}
                tickLine={false}
                angle={-45}
                textAnchor="end"
                interval={0}
              />
              <YAxis
                tick={{ fill: 'rgba(255,255,255,0.4)', fontSize: 9 }}
                axisLine={false}
                tickLine={false}
                width={30}
              />
              <RechartsTooltip
                contentStyle={{
                  backgroundColor: 'hsl(var(--bg-panel))',
                  border: '1px solid rgba(255,255,255,0.1)',
                  borderRadius: '8px',
                  fontSize: '11px',
                }}
                formatter={(value: number | undefined, name: string | undefined) => [
                  typeof value === 'number' ? value : 0,
                  name === 'nmnc' ? 'New Clients (NMNC)' : 'Existing Clients (NMEC)',
                ]}
              />
              <Bar dataKey="nmnc" fill={NMNC_COLOR} fillOpacity={0.75} name="nmnc" />
              <Bar dataKey="nmec" fill={NMEC_COLOR} fillOpacity={0.75} name="nmec" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Per-segment stats (omitted when account_distribution absent) */}
        {(nmnc_dist || nmec_dist) && (
          <div className="grid grid-cols-2 gap-3">
            {[
              { label: 'New Clients (NMNC)', dist: nmnc_dist, color: NMNC_COLOR },
              { label: 'Existing Clients (NMEC)', dist: nmec_dist, color: NMEC_COLOR },
            ].map(({ label, dist, color }) => (
              <div key={label} className="bg-white/5 rounded-lg p-3">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-2.5 h-2.5 rounded-sm flex-shrink-0" style={{ backgroundColor: color }} />
                  <span className="text-[10px] font-medium text-white/70 uppercase tracking-wide">{label}</span>
                </div>
                <div className="grid grid-cols-2 gap-x-3 gap-y-0.5 text-[10px]">
                  <span className="text-white/40">Median</span>
                  <span className="text-white/70 text-right">{dist?.median != null ? formatCurrency(dist.median) : '--'}</span>
                  <span className="text-white/40">Mean</span>
                  <span className="text-white/70 text-right">{dist?.mean != null ? formatCurrency(dist.mean) : '--'}</span>
                  <span className="text-white/40">Count</span>
                  <span className="text-white/70 text-right">{dist?.count.toLocaleString() ?? '--'}</span>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Chart legend */}
        <div className="flex items-center justify-center gap-6">
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: NMNC_COLOR }} />
            <span className="text-xs text-white/50">New Clients (NMNC)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: NMEC_COLOR }} />
            <span className="text-xs text-white/50">Existing Clients (NMEC)</span>
          </div>
        </div>

      </div>
    </div>
  )
}
```

### ec2-user-data.sh-runs-scripts-07-09-10-11-on-ec2.sh

```
#!/bin/bash
# BD Gold Layer - Detail Generator EC2 User Data Script
# Runs scripts 07, 09, 10, 11 (heavy workloads with positions)

set -e

# Configuration
S3_BUCKET="opal-data-bd"
SCRIPTS_DIR="/home/ec2-user/gold-scripts"
LOG_FILE="/var/log/bd-gold-detail-$(date +%Y%m%d_%H%M%S).log"

# Log everything
exec 1> >(tee -a "$LOG_FILE")
exec 2>&1

echo "======================================================================"
echo "BD GOLD LAYER - STAGE 4 DETAIL GENERATION"
echo "Started: $(date -Iseconds)"
echo "======================================================================"

# Install dependencies
echo ""
echo "=== Installing Dependencies ==="
yum install -y python3.11 python3.11-pip
python3.11 -m pip install --upgrade pip

# Create working directory
mkdir -p "$SCRIPTS_DIR"
cd "$SCRIPTS_DIR"

# Download scripts from S3
echo ""
echo "=== Downloading Scripts from S3 ==="
aws s3 sync s3://${S3_BUCKET}/scripts/gold_layer/ . \
  --exclude "*" \
  --include "07_generate_partner_analytics.py" \
  --include "09_generate_client_detail.py" \
  --include "10_generate_book_views.py" \
  --include "11_generate_clients_tab.py" \
  --include "load_silver.py" \
  --include "pii_hasher.py" \
  --include "utils/*.py"

echo "✓ Scripts downloaded"

# Install Python dependencies
echo ""
echo "=== Installing Python Packages ==="
pip3.11 install pandas pyarrow boto3 numpy python-dateutil s3fs -q
echo "✓ Dependencies installed"

# Run heavy analytics scripts
echo ""
echo "=== Running Heavy Analytics Scripts ==="

run_script() {
  local script=$1
  local start=$(date +%s)

  echo ""
  echo ">>> Running: $script"
  echo "    Started: $(date -Iseconds)"

  python3.11 "$script" --upload

  local end=$(date +%s)
  local duration=$((end - start))
  echo "    Duration: ${duration}s"
  echo "    Status: ✓ Complete"
}

# Execute in order (some have dependencies)
run_script "07_generate_partner_analytics.py"
run_script "09_generate_client_detail.py"
run_script "10_generate_book_views.py"
run_script "11_generate_clients_tab.py"

# Upload log to S3
echo ""
echo "=== Uploading Execution Log ==="
aws s3 cp "$LOG_FILE" "s3://${S3_BUCKET}/logs/gold-detail/$(basename $LOG_FILE)"
echo "✓ Log uploaded"

# Create completion marker
echo ""
echo "=== Creating Completion Marker ==="
echo "{\"status\":\"complete\",\"timestamp\":\"$(date -Iseconds)\",\"log\":\"s3://${S3_BUCKET}/logs/gold-detail/$(basename $LOG_FILE)\"}" > /tmp/completion.json
aws s3 cp /tmp/completion.json "s3://${S3_BUCKET}/status/gold-detail-completion.json"
echo "✓ Completion marker created"

echo ""
echo "======================================================================"
echo "STAGE 4 DETAIL GENERATION COMPLETE"
echo "Finished: $(date -Iseconds)"
echo "======================================================================"

# Auto-shutdown
echo ""
echo "Shutting down instance in 60 seconds..."
sleep 60
shutdown -h now
```

### script-09-partner-analytics-generator-produces-quarterly-lookback-data.py

```
#!/usr/bin/env python3
"""
Generate Partner Analytics — header_metrics.json (Multi-Granularity)

CHANGE (2026-03-05): Now generates NMNC/NMEC classifications at all three
granularities (quarterly, monthly, annual) to support frontend toggles.

Produces three portal-ready JSONs to S3:
    s3://opal-data-bd/gold/partner_analytics/header_metrics_quarterly.json
    s3://opal-data-bd/gold/partner_analytics/header_metrics_monthly.json
    s3://opal-data-bd/gold/partner_analytics/header_metrics_annual.json

Each JSON has granularity-appropriate NMNC/NMEC classifications:
- NMNC (New Client Assets) = first_seen_date > period_start_ts
- Period boundaries are quarterly (Q1/Q2/Q3), monthly (m1/m2/m3), or annual (y1/y2/y3)

Data sources (all from s3://opal-data-bd):
    gold/client_performance.parquet           -- primary AUA source (daily x relationship)
    gold/account_performance.parquet          -- account-level AUA for distributions (~90MB)
    gold/accounts_dimension_latest.parquet    -- city/state/architect metadata
    gold/client_dimension.parquet             -- relationship display names
    gold/views/nna_aua_by_geography.parquet   -- pre-aggregated state-level AUA
    gold/views/nna_aua_by_advisor.parquet     -- pre-aggregated advisor-level AUA

Output JSON shape (same for all granularities, only period labels differ):
    {
      "generated_at": "...",
      "data_as_of": "YYYY-MM-DD",
      "firm_id": "49financial",
      "firm_name": "49 Financial",
      "granularity": "quarterly|monthly|annual",
      "periods": { "current": {...}, "q1|m1|y1": {...}, ... },
      "views": {
        "aua": { ... },                    // AUA by tax status donut
        "nna": { ... },                    // Period-differenced NNA
        "geo": { ... },                    // AUA by state donut + cities
        "adv": { ... },                    // AUA by architect donut + clients
        "cla": { ... }                     // NMNC/NMEC lifecycle decomposition
      }
    }

Usage:
    python 09_generate_partner_analytics.py               # local test, all 3 granularities
    python 09_generate_partner_analytics.py --upload      # write all 3 to S3
    python 09_generate_partner_analytics.py --granularity quarterly --upload  # only quarterly
    python 09_generate_partner_analytics.py --dry-run     # compute only, no write
    python 09_generate_partner_analytics.py -v            # verbose output

Author: Data Scientist (Claude)
Date: 2026-02-27
Revision: 2026-03-05 (multi-granularity support)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

import boto3
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

S3_BUCKET = 'opal-data-bd'
S3_OUTPUT_KEY = 'gold/partner_analytics/header_metrics.json'
DEFAULT_LOCAL_OUTPUT = './gold/partner_analytics/header_metrics.json'

NUM_HISTOGRAM_BINS = 20  # log-spaced bins for bell curve shape
NNA_MATERIALITY_THRESHOLD = 1_000  # $1K -- below this is fees/dividends/rounding, not real flows

MAX_SEGMENTS = 8        # max geo states or advisors in donut
MAX_CITIES = 9          # max cities nested under a state
MAX_CLIENTS_PER_ADVISOR = 15

GEO_COLORS  = ['#F44336', '#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#00BCD4', '#795548', '#607D8B']
CITY_COLORS = ['#E91E63', '#9C27B0', '#673AB7', '#3F51B5', '#2196F3']
ADV_COLORS  = ['#5e72e4', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4', '#84CC16', '#F97316']
OTHER_COLOR = '#757575'

MODAL_NULLS = frozenset({
    '', 'none', 'nan', 'unassigned', 'unknown', 'n/a',
    'no architect value assigned', 'no state',
})

# NNA blue/red color palettes (rank-ordered, darkest = largest magnitude)
NNA_BLUE_SHADES = ['#1E40AF', '#1D4ED8', '#2563EB', '#3B82F6', '#60A5FA', '#93C5FD', '#BFDBFE', '#DBEAFE']
NNA_RED_SHADES  = ['#991B1B', '#B91C1C', '#DC2626', '#EF4444', '#F87171', '#FCA5A5', '#FECACA', '#FEE2E2']

# CLA lifecycle colors
CLA_NMNC_COLOR     = '#16A34A'   # Green  -- New Client Inflows
CLA_NMEC_POS_COLOR = '#2563EB'   # Blue   -- Existing Client Inflows
CLA_NMEC_NEG_COLOR = '#DC2626'   # Red    -- Existing Client Outflows

# ---------------------------------------------------------------------------
# Period computation
# ---------------------------------------------------------------------------

def get_periods(ref_date: pd.Timestamp, granularity: str = 'quarterly') -> dict:
    """
    Returns periods based on granularity.

    granularity='quarterly': 4 periods (current + 3 trailing completed quarters)
    granularity='monthly':   4 periods (current month + 3 trailing completed months)
    granularity='annual':    4 periods (current year + 3 trailing completed years)

    Example (ref_date = 2026-02-26):
      quarterly:
        current = 2026-02-26
        q1 = 2025-12-31, q2 = 2025-09-30, q3 = 2025-06-30
      monthly:
        current = 2026-02-26
        m1 = 2026-01-31, m2 = 2025-12-31, m3 = 2025-11-30
      annual:
        current = 2026-02-26
        y1 = 2025-12-31, y2 = 2024-12-31, y3 = 2023-12-31
    """
    if granularity == 'quarterly':
        return _get_periods_quarterly(ref_date)
    elif granularity == 'monthly':
        return _get_periods_monthly(ref_date)
    elif granularity == 'annual':
        return _get_periods_annual(ref_date)
    else:
        raise ValueError(f"Unknown granularity: {granularity}")


def _get_periods_quarterly(ref_date: pd.Timestamp) -> dict:
    """Returns 4 periods: current + 3 trailing completed quarter-ends."""
    qe_month_to_label = {3: 'Q1', 6: 'Q2', 9: 'Q3', 12: 'Q4'}

    quarter_ends = []
    dt = ref_date
    for _ in range(8):  # check up to 8 quarters back; we need 3 completed ones
        if dt.month <= 3:
            qe = pd.Timestamp(dt.year - 1, 12, 31)
        elif dt.month <= 6:
            qe = pd.Timestamp(dt.year, 3, 31)
        elif dt.month <= 9:
            qe = pd.Timestamp(dt.year, 6, 30)
        else:
            qe = pd.Timestamp(dt.year, 9, 30)

        if qe < ref_date and qe not in quarter_ends:
            quarter_ends.append(qe)
        dt = qe - pd.DateOffset(days=1)

        if len(quarter_ends) == 3:
            break

    def period_label(qe: pd.Timestamp) -> str:
        quarter_name = qe_month_to_label[qe.month]
        return f"{quarter_name} '{str(qe.year)[2:]}"  # e.g. "Q4 '25"

    q1, q2, q3 = quarter_ends[0], quarter_ends[1], quarter_ends[2]

    return {
        'current': {'date': ref_date.strftime('%Y-%m-%d'), 'label': 'Current', '_ts': ref_date},
        'q1':      {'date': q1.strftime('%Y-%m-%d'), 'label': period_label(q1), '_ts': q1},
        'q2':      {'date': q2.strftime('%Y-%m-%d'), 'label': period_label(q2), '_ts': q2},
        'q3':      {'date': q3.strftime('%Y-%m-%d'), 'label': period_label(q3), '_ts': q3},
    }


def _get_periods_monthly(ref_date: pd.Timestamp) -> dict:
    """Returns 4 periods: current month end + 3 trailing completed month-ends."""
    # Current month end
    if ref_date.month == 12:
        current_month_end = pd.Timestamp(ref_date.year, 12, 31)
    else:
        current_month_end = pd.Timestamp(ref_date.year, ref_date.month + 1, 1) - pd.DateOffset(days=1)

    # Find 3 trailing completed months
    month_ends = []
    dt = current_month_end
    for _ in range(6):  # look back up to 6 months to find 3 completed ones
        if dt < ref_date and dt not in month_ends:
            month_ends.append(dt)
        if len(month_ends) == 3:
            break
        # Move to previous month-end
        dt = pd.Timestamp(dt.year, dt.month, 1) - pd.DateOffset(days=1)

    def month_label(me: pd.Timestamp) -> str:
        month_name = me.strftime('%b')
        return f"{month_name} '{str(me.year)[2:]}"  # e.g. "Jan '26"

    m1, m2, m3 = month_ends[0], month_ends[1], month_ends[2]

    return {
        'current': {'date': ref_date.strftime('%Y-%m-%d'), 'label': 'Current', '_ts': ref_date},
        'm1':      {'date': m1.strftime('%Y-%m-%d'), 'label': month_label(m1), '_ts': m1},
        'm2':      {'date': m2.strftime('%Y-%m-%d'), 'label': month_label(m2), '_ts': m2},
        'm3':      {'date': m3.strftime('%Y-%m-%d'), 'label': month_label(m3), '_ts': m3},
    }


def _get_periods_annual(ref_date: pd.Timestamp) -> dict:
    """Returns 4 periods: current year-end + 3 trailing completed year-ends."""
    current_year_end = pd.Timestamp(ref_date.year, 12, 31)

    # Find 3 trailing completed years
    year_ends = []
    dt = current_year_end
    for _ in range(6):  # look back up to 6 years
        if dt < ref_date and dt not in year_ends:
            year_ends.append(dt)
        if len(year_ends) == 3:
            break
        dt = pd.Timestamp(dt.year - 1, 12, 31)

    def year_label(ye: pd.Timestamp) -> str:
        return f"{ye.year}"

    y1, y2, y3 = year_ends[0], year_ends[1], year_ends[2]

    return {
        'current': {'date': ref_date.strftime('%Y-%m-%d'), 'label': 'Current', '_ts': ref_date},
        'y1':      {'date': y1.strftime('%Y-%m-%d'), 'label': year_label(y1), '_ts': y1},
        'y2':      {'date': y2.strftime('%Y-%m-%d'), 'label': year_label(y2), '_ts': y2},
        'y3':      {'date': y3.strftime('%Y-%m-%d'), 'label': year_label(y3), '_ts': y3},
    }


def get_period_pairs(periods: dict, granularity: str = 'quarterly') -> dict:
    """
    For each period, determine (end_ts, start_ts) for NNA period differencing.

    Period NNA = cum_nna(end) - cum_nna(start).  Start is the prior period-end.
    NMNC classification: first_seen_date > start_ts.

    Mapping varies by granularity:
      quarterly:  current→q1→q2→q3→(prior quarter)
      monthly:    current→m1→m2→m3→(prior month)
      annual:     current→y1→y2→y3→(prior year)
    """
    keys = list(periods.keys())  # ['current', 'q1'/'m1'/'y1', 'q2'/'m2'/'y2', 'q3'/'m3'/'y3']
    pairs = {}
    for i, key in enumerate(keys):
        end_ts = periods[key]['_ts']
        if i + 1 < len(keys):
            start_ts = periods[keys[i + 1]]['_ts']
        else:
            # Last period's prior: compute one more period-end back
            last_ts = periods[keys[-1]]['_ts']
            if granularity == 'quarterly':
                # One more quarter back
                if last_ts.month == 3:
                    start_ts = pd.Timestamp(last_ts.year - 1, 12, 31)
                elif last_ts.month == 6:
                    start_ts = pd.Timestamp(last_ts.year, 3, 31)
                elif last_ts.month == 9:
                    start_ts = pd.Timestamp(last_ts.year, 6, 30)
                else:
                    start_ts = pd.Timestamp(last_ts.year, 9, 30)
            elif granularity == 'monthly':
                # One more month back
                start_ts = pd.Timestamp(last_ts.year, last_ts.month, 1) - pd.DateOffset(days=1)
            elif granularity == 'annual':
                # One more year back
                start_ts = pd.Timestamp(last_ts.year - 1, 12, 31)
            else:
                raise ValueError(f"Unknown granularity: {granularity}")
        pairs[key] = {'end': end_ts, 'start': start_ts}
    return pairs


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_data(verbose: bool = False) -> tuple:
    """
    Load all required gold tables from S3.
    Returns: (client_perf, acct_perf, acct_dim, client_dim, geo_ts, adv_ts)

    account_performance is ~90MB — read once, filter to target dates in memory.
    """
    s3 = boto3.client('s3', region_name='us-east-1')

    def _read(key: str) -> pd.DataFrame:
        if verbose:
            print(f"  Loading s3://{S3_BUCKET}/{key}")
        resp = s3.get_object(Bucket=S3_BUCKET, Key=key)
        return pd.read_parquet(BytesIO(resp['Body'].read()))

    client_perf = _read('gold/client_performance.parquet')
    acct_perf   = _read('gold/account_performance.parquet')
    acct_dim    = _read('gold/accounts_dimension_latest.parquet')
    client_dim  = _read('gold/client_dimension.parquet')
    geo_ts      = _read('gold/views/nna_aua_by_geography.parquet')
    adv_ts      = _read('gold/views/nna_aua_by_advisor.parquet')
    rel_lookup_df = _read('gold/views/rel_architect_lookup.parquet')

    # Normalize date columns to pd.Timestamp
    for df in (client_perf, acct_perf, geo_ts, adv_ts):
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])

    # Convert lookup to Series indexed by relationship_id (same interface as before)
    rel_arch_lookup = rel_lookup_df.set_index('relationship_id')['architect']

    return client_perf, acct_perf, acct_dim, client_dim, geo_ts, adv_ts, rel_arch_lookup


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------

def _build_rel_geo_lookup(acct_dim: pd.DataFrame) -> pd.Series:
    """
    Derive relationship_id -> modal state from accounts dimension.

    Same logic as script 07 (modal non-null state per relationship).
    Returns a Series indexed by relationship_id with values = state string.
    """
    if 'client_state' not in acct_dim.columns:
        return pd.Series(dtype=str, name='state')

    def _modal_state(s: pd.Series) -> str:
        clean = s.dropna().astype(str).str.strip()
        clean = clean[~clean.str.lower().isin(MODAL_NULLS)]
        return clean.mode().iloc[0] if not clean.empty else 'Unknown'

    return (
        acct_dim
        .groupby('relationship_id')['client_state']
        .agg(_modal_state)
        .rename('state')
    )


def _build_rel_city_lookup(acct_dim: pd.DataFrame) -> pd.Series:
    """
    Derive relationship_id -> modal city from accounts dimension.

    Returns a Series indexed by relationship_id with values = city string.
    Used for Y6b city-level NNA distribution drill-down.
    """
    if 'client_city' not in acct_dim.columns:
        return pd.Series(dtype=str, name='city')

    def _modal_city(s: pd.Series) -> str:
        clean = s.dropna().astype(str).str.strip()
        clean = clean[~clean.str.lower().isin(MODAL_NULLS)]
        return clean.mode().iloc[0] if not clean.empty else 'Unknown'

    return (
        acct_dim
        .groupby('relationship_id')['client_city']
        .agg(_modal_city)
        .rename('city')
    )


# ---------------------------------------------------------------------------
# Distribution stats
# ---------------------------------------------------------------------------

def _fmt_currency(val: float) -> str:
    """Format a dollar value for bin labels ($1K, $250K, $1.2M etc.)."""
    sign = '-' if val < 0 else ''
    val = abs(val)
    if val >= 1_000_000:
        return f"{sign}${val / 1_000_000:.1f}M"
    elif val >= 1_000:
        return f"{sign}${val / 1_000:.0f}K"
    return f"{sign}${val:.0f}"


def calculate_distribution_stats(aua_values: pd.Series) -> dict:
    """
    Compute histogram + percentile stats for an array of AUA values.
    Uses log-spaced bins (same approach as Model Portfolios) so the bell
    curve is visible even when the median is low.

    Returns dict matching the portal's DistributionStats TypeScript interface.
    """
    vals = aua_values.dropna()
    vals = vals[vals > 0]

    if vals.empty:
        return {
            'count':   0,
            'total':   0,
            'mean':    None,
            'median':  None,
            'min':     None,
            'max':     None,
            'std_dev': None,
            'percentiles': {'p10': None, 'p25': None, 'p50': None, 'p75': None, 'p90': None},
            'histogram': {'bins': [], 'counts': [], 'bin_labels': []},
        }

    n = len(vals)

    # Log-spaced bins for proper bell curve shape
    min_val = max(float(vals.min()), 1_000)   # floor at $1K
    max_val = float(vals.max())

    # Guard: single-value or identical-value edge case (e.g. one-account relationship)
    # produces degenerate bins where all edges collapse to a single point.
    if max_val <= min_val:
        max_val = min_val * 2

    bin_edges = np.logspace(np.log10(min_val), np.log10(max_val), NUM_HISTOGRAM_BINS + 1)
    counts, _ = np.histogram(vals, bins=bin_edges)

    bin_labels = [
        f"{_fmt_currency(bin_edges[i])}-{_fmt_currency(bin_edges[i + 1])}"
        for i in range(len(bin_edges) - 1)
    ]

    return {
        'count':   n,
        'total':   round(float(vals.sum()), 2),
        'mean':    round(float(vals.mean()), 2),
        'median':  round(float(vals.median()), 2),
        'min':     round(float(vals.min()), 2),
        'max':     round(float(vals.max()), 2),
        'std_dev': round(float(vals.std()), 2) if n > 1 else None,
        'percentiles': {
            'p10': round(float(vals.quantile(0.10)), 2),
            'p25': round(float(vals.quantile(0.25)), 2),
            'p50': round(float(vals.quantile(0.50)), 2),
            'p75': round(float(vals.quantile(0.75)), 2),
            'p90': round(float(vals.quantile(0.90)), 2),
        },
        'histogram': {
            'bins':       [round(float(b), 2) for b in bin_edges],
            'counts':     [int(c) for c in counts],
            'bin_labels': bin_labels,
        }
    }


def calculate_nna_distribution_stats(nna_values: pd.Series) -> dict:
    """
    Compute histogram + percentile stats for per-relationship period NNA.

    Unlike AUA distribution (always positive, log-spaced), NNA can be negative.
    Uses symmetric log-spaced bins around zero so both inflows and outflows
    are visible.  Relationships below the materiality threshold are excluded
    (fees, dividend reinvestments, rounding -- not genuine flows).

    Returns dict matching the portal's DistributionStats TypeScript interface.
    """
    vals = nna_values.dropna()
    vals = vals[vals.abs() >= NNA_MATERIALITY_THRESHOLD]

    if vals.empty:
        return {
            'count':   0,
            'total':   0,
            'mean':    None,
            'median':  None,
            'min':     None,
            'max':     None,
            'std_dev': None,
            'percentiles': {'p10': None, 'p25': None, 'p50': None, 'p75': None, 'p90': None},
            'histogram': {'bins': [], 'counts': [], 'bin_labels': []},
        }

    n = len(vals)
    abs_max = float(vals.abs().max())
    abs_min = max(float(vals.abs().min()), 1_000)   # floor at $1K

    # Build log-spaced positive bins, then mirror for negatives
    half_bins = NUM_HISTOGRAM_BINS // 2
    pos_edges = np.logspace(np.log10(abs_min), np.log10(max(abs_max, abs_min * 2)), half_bins + 1)

    # Full bin edges: -pos_edges (reversed, excluding 0) + [0] + pos_edges
    neg_edges = -pos_edges[::-1]
    bin_edges = np.concatenate([neg_edges, [0], pos_edges])

    counts, _ = np.histogram(vals, bins=bin_edges)

    bin_labels = [
        f"{_fmt_currency(bin_edges[i])}-{_fmt_currency(bin_edges[i + 1])}"
        for i in range(len(bin_edges) - 1)
    ]

    # Split inflow/outflow percentiles ranked by absolute magnitude.
    # Outflows (negative NNA): rank by abs so P90+ = largest outflow magnitude.
    # Inflows (positive NNA): P90+ = largest inflow (natural order).
    inflows  = vals[vals > 0]
    outflows = vals[vals < 0].abs()  # positive magnitudes for ranking

    def _pctiles(s: pd.Series) -> dict:
        if s.empty:
            return {'p10': None, 'p25': None, 'p50': None, 'p75': None, 'p90': None}
        return {
            'p10': round(float(s.quantile(0.10)), 2),
            'p25': round(float(s.quantile(0.25)), 2),
            'p50': round(float(s.quantile(0.50)), 2),
            'p75': round(float(s.quantile(0.75)), 2),
            'p90': round(float(s.quantile(0.90)), 2),
        }

    return {
        'count':   n,
        'total':   round(float(vals.sum()), 2),
        'mean':    round(float(vals.mean()), 2),
        'median':  round(float(vals.median()), 2),
        'min':     round(float(vals.min()), 2),
        'max':     round(float(vals.max()), 2),
        'std_dev': round(float(vals.std()), 2) if n > 1 else None,
        'percentiles': {
            'p10': round(float(vals.quantile(0.10)), 2),
            'p25': round(float(vals.quantile(0.25)), 2),
            'p50': round(float(vals.quantile(0.50)), 2),
            'p75': round(float(vals.quantile(0.75)), 2),
            'p90': round(float(vals.quantile(0.90)), 2),
        },
        'inflow_percentiles':  _pctiles(inflows),
        'outflow_percentiles': _pctiles(outflows),
        'inflow_count':  len(inflows),
        'outflow_count': len(outflows),
        'histogram': {
            'bins':       [round(float(b), 2) for b in bin_edges],
            'counts':     [int(c) for c in counts],
            'bin_labels': bin_labels,
        }
    }


def _compute_rel_period_nna(
        cp_end: pd.DataFrame, cp_start: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute per-relationship period NNA from client_performance snapshots.

    Returns DataFrame with columns: relationship_id, period_nna
    """
    end_nna = cp_end[['relationship_id', 'nna']].copy()
    start_nna = cp_start[['relationship_id', 'nna']].rename(columns={'nna': 'nna_start'})
    merged = end_nna.merge(start_nna, on='relationship_id', how='left')
    merged['nna_start'] = merged['nna_start'].fillna(0)
    merged['period_nna'] = merged['nna'] - merged['nna_start']
    return merged[['relationship_id', 'period_nna']]


def _empty_view(title: str) -> dict:
    """Return a zeroed-out view structure for periods with no data."""
    empty_dist = calculate_distribution_stats(pd.Series([], dtype=float))
    return {
        'donut': {'title': title, 'total': 0, 'segments': []},
        'distribution': {'total': empty_dist, 'by_segment': {}},
        'metrics': {'aua': 0, 'client_count': 0}
    }


# ---------------------------------------------------------------------------
# GEO view
# ---------------------------------------------------------------------------

def build_geo_view(period_ts: pd.Timestamp,
                   geo_ts: pd.DataFrame,
                   acct_perf_day: pd.DataFrame,
                   acct_dim: pd.DataFrame) -> dict:
    """
    Build the GEO view for one period.

    State-level donut: geo_ts pre-aggregated view (fast, already summed).
    City drill-down:   join acct_perf_day + acct_dim -> group by (state, city).
    Distributions:     acct_perf_day total_aua per account, grouped by state.
    """
    # --- State-level aggregation ---
    geo_day = geo_ts[geo_ts['date'] == period_ts].copy()
    # Exclude non-US / unknown
    geo_day = geo_day[
        geo_day['state'].notna() &
        (geo_day['state'] != '') &
        (geo_day['state'] != 'Unknown')
    ]
    geo_day = geo_day.sort_values('total_aua', ascending=False)

    total_aua = float(geo_day['total_aua'].sum())

    # --- Account-level data for cities + distributions ---
    acct_geo = acct_perf_day.merge(
        acct_dim[['account_id', 'client_city', 'client_state']],
        on='account_id', how='left'
    )
    acct_geo['client_state'] = acct_geo['client_state'].fillna('Unknown').str.strip()
    acct_geo['client_city']  = acct_geo['client_city'].fillna('').str.strip()

    # --- Segments ---
    top_states   = geo_day.head(MAX_SEGMENTS)
    other_states = geo_day.iloc[MAX_SEGMENTS:]

    segments = []
    by_segment_dist = {}

    for i, (_, row) in enumerate(top_states.iterrows()):
        state = row['state']
        aua   = float(row['total_aua'])
        client_count = int(row.get('num_relationships', 0))

        state_accts = acct_geo[acct_geo['client_state'] == state]
        state_dist  = calculate_distribution_stats(state_accts['total_aua'])
        cities      = _build_cities(state_accts, state, aua)

        key = state.lower()
        segments.append({
            'key':          key,
            'label':        state,
            'aua':          round(aua, 2),
            'aua_pct':      round(aua / total_aua * 100, 1) if total_aua > 0 else 0.0,
            'client_count': client_count,
            'color':        GEO_COLORS[i % len(GEO_COLORS)],
            'cities':       cities,
            'distribution': state_dist
        })
        by_segment_dist[key] = state_dist

    # Other bucket
    if not other_states.empty:
        other_aua          = float(other_states['total_aua'].sum())
        other_client_count = int(other_states['num_relationships'].sum())
        other_state_names  = other_states['state'].tolist()
        other_accts        = acct_geo[acct_geo['client_state'].isin(other_state_names)]
        other_dist         = calculate_distribution_stats(other_accts['total_aua'])

        if other_aua > 0:
            segments.append({
                'key':          'other',
                'label':        'Other States',
                'aua':          round(other_aua, 2),
                'aua_pct':      round(other_aua / total_aua * 100, 1) if total_aua > 0 else 0.0,
                'client_count': other_client_count,
                'color':        OTHER_COLOR,
                'cities':       [],
                'distribution': other_dist
            })
            by_segment_dist['other'] = other_dist

    total_dist = calculate_distribution_stats(acct_geo['total_aua'])

    return {
        'donut': {
            'title':    'AUA by State',
            'total':    round(total_aua, 2),
            'segments': segments
        },
        'distribution': {
            'total':      total_dist,
            'by_segment': by_segment_dist
        },
        'metrics': {
            'aua':          round(total_aua, 2),
            'client_count': int(geo_day['num_relationships'].sum())
        }
    }


def _build_cities(state_accts: pd.DataFrame, state: str, state_aua: float) -> list:
    """Build city drill-down list for one state."""
    if state_accts.empty:
        return []

    city_agg = (
        state_accts
        .groupby('client_city')
        .agg(aua=('total_aua', 'sum'), account_count=('account_id', 'count'))
        .reset_index()
        .sort_values('aua', ascending=False)
    )
    # Drop blank city names
    city_agg = city_agg[city_agg['client_city'].str.strip() != '']

    top_cities   = city_agg.head(MAX_CITIES)
    other_cities = city_agg.iloc[MAX_CITIES:]

    cities = []
    for i, (_, row) in enumerate(top_cities.iterrows()):
        city_name = str(row['client_city']).strip()
        aua       = float(row['aua'])
        city_accts = state_accts[state_accts['client_city'] == row['client_city']]
        city_dist  = calculate_distribution_stats(city_accts['total_aua'])

        cities.append({
            'key':          f"{city_name.lower().replace(' ', '_')}_{state.lower()}",
            'label':        city_name,
            'aua':          round(aua, 2),
            'aua_pct':      round(aua / state_aua * 100, 1) if state_aua > 0 else 0.0,
            'client_count': int(row['account_count']),
            'color':        CITY_COLORS[i % len(CITY_COLORS)],
            'distribution': city_dist
        })

    if not other_cities.empty and other_cities['aua'].sum() > 0:
        other_aua   = float(other_cities['aua'].sum())
        other_accts = state_accts[state_accts['client_city'].isin(other_cities['client_city'])]
        cities.append({
            'key':          f"other_{state.lower()}",
            'label':        f"Other {state} Cities",
            'aua':          round(other_aua, 2),
            'aua_pct':      round(other_aua / state_aua * 100, 1) if state_aua > 0 else 0.0,
            'client_count': int(other_cities['account_count'].sum()),
            'color':        OTHER_COLOR,
            'distribution': calculate_distribution_stats(other_accts['total_aua'])
        })

    return cities


# ---------------------------------------------------------------------------
# ADV view
# ---------------------------------------------------------------------------

def build_adv_view(period_ts: pd.Timestamp,
                   adv_ts: pd.DataFrame,
                   client_perf_day: pd.DataFrame,
                   acct_perf_day: pd.DataFrame,
                   acct_dim: pd.DataFrame,
                   client_dim: pd.DataFrame,
                   rel_arch_lookup: pd.Series) -> dict:
    """
    Build the ADV view for one period.

    Advisor-level donut:  adv_ts pre-aggregated view.
    Nested clients:       client_perf_day filtered to advisor, top N by AUA.
    Distributions:        acct_perf_day total_aua per account, grouped by advisor.
    """
    adv_day = adv_ts[adv_ts['date'] == period_ts].copy()
    adv_day = adv_day[adv_day['architect'].notna()]
    adv_day = adv_day.sort_values('total_aua', ascending=False)

    total_aua = float(adv_day['total_aua'].sum())

    # Client-level data: add architect assignment + display name
    client_day = client_perf_day.copy()
    client_day['architect'] = client_day['relationship_id'].map(rel_arch_lookup).fillna('Unassigned')

    if 'relationship_name' in client_dim.columns:
        name_map = client_dim.set_index('relationship_id')['relationship_name']
        client_day['relationship_name'] = (
            client_day['relationship_id'].map(name_map)
            .fillna(client_day['relationship_id'].astype(str))
        )
    else:
        client_day['relationship_name'] = client_day['relationship_id'].astype(str)

    # Account-level data: add architect
    acct_arch = acct_perf_day.copy()
    acct_arch['architect'] = acct_arch['relationship_id'].map(rel_arch_lookup).fillna('Unassigned')

    top_advisors   = adv_day.head(MAX_SEGMENTS)
    other_advisors = adv_day.iloc[MAX_SEGMENTS:]

    segments = []
    by_segment_dist = {}

    for i, (_, row) in enumerate(top_advisors.iterrows()):
        arch         = row['architect']
        aua          = float(row['total_aua'])
        client_count = int(row.get('num_relationships', 0))

        arch_clients = client_day[client_day['architect'] == arch]
        arch_accts   = acct_arch[acct_arch['architect'] == arch]

        adv_dist       = calculate_distribution_stats(arch_accts['total_aua'])
        arch_color     = ADV_COLORS[i % len(ADV_COLORS)]
        nested_clients = _build_clients(arch_clients, arch_accts, arch_aua=aua, arch_color=arch_color)

        key = arch.lower().replace(' ', '_').replace('-', '_')
        segments.append({
            'key':          key,
            'label':        arch,
            'aua':          round(aua, 2),
            'aua_pct':      round(aua / total_aua * 100, 1) if total_aua > 0 else 0.0,
            'client_count': client_count,
            'color':        arch_color,
            'clients':      nested_clients,
            'distribution': adv_dist
        })
        by_segment_dist[key] = adv_dist

    if not other_advisors.empty:
        other_aua         = float(other_advisors['total_aua'].sum())
        other_arch_names  = other_advisors['architect'].tolist()
        other_clients_df  = client_day[client_day['architect'].isin(other_arch_names)]
        other_accts       = acct_arch[acct_arch['architect'].isin(other_arch_names)]
        other_dist        = calculate_distribution_stats(other_accts['total_aua'])

        if other_aua > 0:
            other_nested = _build_clients(other_clients_df, other_accts, arch_aua=other_aua, arch_color=OTHER_COLOR)
            segments.append({
                'key':          'other',
                'label':        'Other Architects',
                'aua':          round(other_aua, 2),
                'aua_pct':      round(other_aua / total_aua * 100, 1) if total_aua > 0 else 0.0,
                'client_count': int(other_advisors['num_relationships'].sum()),
                'color':        OTHER_COLOR,
                'clients':      other_nested,
                'distribution': other_dist
            })
            by_segment_dist['other'] = other_dist

    total_dist = calculate_distribution_stats(acct_arch['total_aua'])

    return {
        'donut': {
            'title':    'AUA by Architect',
            'total':    round(total_aua, 2),
            'segments': segments
        },
        'distribution': {
            'total':      total_dist,
            'by_segment': by_segment_dist
        },
        'metrics': {
            'aua':          round(total_aua, 2),
            'client_count': int(adv_day['num_relationships'].sum())
        }
    }


def _build_clients(arch_clients: pd.DataFrame,
                   arch_accts: pd.DataFrame,
                   arch_aua: float,
                   arch_color: str) -> list:
    """Build nested clients list for an advisor segment.

    Each client (relationship) gets an account-level distribution so the
    frontend can drill: Architect -> Relationship -> Account distribution.
    Mirrors the GEO pattern: State -> City -> account distribution.
    """
    if arch_clients.empty:
        return []

    top_clients = arch_clients.sort_values('total_aua', ascending=False).head(MAX_CLIENTS_PER_ADVISOR)

    clients = []
    for _, row in top_clients.iterrows():
        rel_id = row['relationship_id']
        aua    = float(row['total_aua'])
        name   = str(row.get('relationship_name', rel_id))

        # Account-level distribution for this relationship
        rel_accts = arch_accts[arch_accts['relationship_id'] == rel_id]
        rel_dist  = calculate_distribution_stats(rel_accts['total_aua'])

        clients.append({
            'key':          str(rel_id),
            'label':        name,
            'aua':          round(aua, 2),
            'aua_pct':      round(aua / arch_aua * 100, 1) if arch_aua > 0 else 0.0,
            'account_count': int(len(rel_accts)),
            'color':        arch_color,
            'distribution': rel_dist
        })

    return clients


# ---------------------------------------------------------------------------
# AUA view (tax status donut)
# ---------------------------------------------------------------------------

AUA_TAX_COLORS = {
    'taxable':      '#EF4444',   # Red — Non-Qualified
    'tax_deferred': '#F59E0B',   # Amber — Tax-Deferred
    'tax_free':     '#10B981',   # Green — Tax-Free (Roth)
}


def _build_aua_tax_view(cp_day: pd.DataFrame, client_dim: pd.DataFrame) -> dict:
    """
    Build AUA-by-tax-status donut for one period.

    Segments: Non-Qualified, Tax-Deferred, Tax-Free (Roth).
    Uses aua_taxable / aua_tax_deferred / aua_tax_exempt from client_performance.
    Client counts from client_dimension has_taxable / has_tax_deferred / has_tax_exempt.
    """
    total_aua    = float(cp_day['total_aua'].sum())
    aua_taxable  = float(cp_day['aua_taxable'].sum())  if 'aua_taxable'      in cp_day.columns else 0.0
    aua_deferred = float(cp_day['aua_tax_deferred'].sum()) if 'aua_tax_deferred' in cp_day.columns else 0.0
    aua_exempt   = float(cp_day['aua_tax_exempt'].sum())   if 'aua_tax_exempt'   in cp_day.columns else 0.0

    n_taxable  = int(client_dim['has_taxable'].sum())      if 'has_taxable'      in client_dim.columns else 0
    n_deferred = int(client_dim['has_tax_deferred'].sum())  if 'has_tax_deferred' in client_dim.columns else 0
    n_exempt   = int(client_dim['has_tax_exempt'].sum())    if 'has_tax_exempt'   in client_dim.columns else 0

    def _seg(key, label, aua, count, color):
        return {
            'key':          key,
            'label':        label,
            'aua':          round(aua, 2),
            'aua_pct':      round(aua / total_aua * 100, 1) if total_aua > 0 else 0.0,
            'client_count': count,
            'color':        color,
        }

    segments = [
        _seg('taxable',      'Non-Qualified',   aua_taxable,  n_taxable,  AUA_TAX_COLORS['taxable']),
        _seg('tax_deferred', 'Tax-Deferred',    aua_deferred, n_deferred, AUA_TAX_COLORS['tax_deferred']),
        _seg('tax_free',     'Tax-Free (Roth)', aua_exempt,   n_exempt,   AUA_TAX_COLORS['tax_free']),
    ]

    total_clients = int(client_dim['relationship_id'].nunique()) if 'relationship_id' in client_dim.columns else 0

    return {
        'donut': {
            'title':    'AUA by Tax Status',
            'total':    round(total_aua, 2),
            'segments': segments
        },
        'distribution': {
            'total':      calculate_distribution_stats(pd.Series([], dtype=float)),
            'by_segment': {}
        },
        'metrics': {
            'aua':          round(total_aua, 2),
            'client_count': total_clients
        }
    }


# ---------------------------------------------------------------------------
# NNA views (period-differenced, blue/red by sign)
# ---------------------------------------------------------------------------

def _assign_nna_colors(segments: list) -> list:
    """
    Assign blue shades to positive-NNA segments and red shades to negative-NNA
    segments, rank-ordered by absolute magnitude within each group.
    """
    pos = [(i, s) for i, s in enumerate(segments) if s.get('_nna', 0) >= 0]
    neg = [(i, s) for i, s in enumerate(segments) if s.get('_nna', 0) < 0]

    # Sort each group by absolute NNA descending (darkest = largest magnitude)
    pos.sort(key=lambda x: abs(x[1].get('_nna', 0)), reverse=True)
    neg.sort(key=lambda x: abs(x[1].get('_nna', 0)), reverse=True)

    for rank, (idx, _) in enumerate(pos):
        segments[idx]['color'] = NNA_BLUE_SHADES[rank % len(NNA_BLUE_SHADES)]
    for rank, (idx, _) in enumerate(neg):
        segments[idx]['color'] = NNA_RED_SHADES[rank % len(NNA_RED_SHADES)]

    # Strip the internal _nna key
    for s in segments:
        s.pop('_nna', None)

    return segments


def build_nna_geo_view(end_ts: pd.Timestamp,
                       start_ts: pd.Timestamp,
                       geo_ts: pd.DataFrame,
                       cp_end: pd.DataFrame = None,
                       cp_start: pd.DataFrame = None,
                       rel_geo_lookup: pd.Series = None,
                       rel_city_lookup: pd.Series = None) -> dict:
    """
    Build NNA-mode GEO view: period-differenced NNA by state.

    Donut slices sized by abs(period_nna), colored blue (growth) / red (attrition).
    Distribution: per-relationship period NNA histogram (signed, symmetric log bins).
    """
    geo_end   = geo_ts[geo_ts['date'] == end_ts].copy()
    geo_start = geo_ts[geo_ts['date'] == start_ts]

    # Exclude non-US and blank states; keep 'Unknown' as a named segment
    geo_end = geo_end[
        geo_end['state'].notna() & (geo_end['state'] != '')
    ].copy()

    if geo_end.empty:
        return _empty_nna_view('NNA by State')

    # Merge start-of-period cumulative values to compute period flows
    start_cols = geo_start[['state', 'country', 'nna', 'cum_inflows', 'cum_outflows']].copy()
    start_cols = start_cols.rename(columns={
        'nna': 'nna_start', 'cum_inflows': 'inflows_start', 'cum_outflows': 'outflows_start'
    })
    merged = geo_end.merge(start_cols, on=['state', 'country'], how='left')
    merged['nna_start']     = merged['nna_start'].fillna(0)
    merged['inflows_start'] = merged['inflows_start'].fillna(0)
    merged['outflows_start'] = merged['outflows_start'].fillna(0)

    merged['period_nna']      = merged['nna']          - merged['nna_start']
    merged['period_inflows']  = merged['cum_inflows']  - merged['inflows_start']
    merged['period_outflows'] = merged['cum_outflows'] - merged['outflows_start']

    # Sort by absolute period NNA (biggest movers first)
    merged = merged.reindex(merged['period_nna'].abs().sort_values(ascending=False).index)

    total_abs_nna = float(merged['period_nna'].abs().sum())
    total_net_nna = float(merged['period_nna'].sum())

    top     = merged.head(MAX_SEGMENTS)
    others  = merged.iloc[MAX_SEGMENTS:]

    segments = []
    for _, row in top.iterrows():
        nna_val = float(row['period_nna'])
        segments.append({
            'key':             row['state'].lower(),
            'label':           row['state'],
            'aua':             round(abs(nna_val), 2),          # abs for donut slice sizing
            'aua_pct':         round(abs(nna_val) / total_abs_nna * 100, 1) if total_abs_nna > 0 else 0.0,
            'value':           round(nna_val, 2),               # signed NNA for display
            'client_count':    int(row.get('num_relationships', 0)),
            'period_inflows':  round(float(row['period_inflows']), 2),
            'period_outflows': round(float(row['period_outflows']), 2),
            'color':           '',                              # assigned below
            '_nna':            nna_val,                         # temp for color assignment
        })

    if not others.empty:
        other_nna      = float(others['period_nna'].sum())
        other_inflows  = float(others['period_inflows'].sum())
        other_outflows = float(others['period_outflows'].sum())
        other_count    = int(others['num_relationships'].sum())
        if abs(other_nna) > 0:
            segments.append({
                'key':             'other',
                'label':           'Other States',
                'aua':             round(abs(other_nna), 2),
                'aua_pct':         round(abs(other_nna) / total_abs_nna * 100, 1) if total_abs_nna > 0 else 0.0,
                'value':           round(other_nna, 2),
                'client_count':    other_count,
                'period_inflows':  round(other_inflows, 2),
                'period_outflows': round(other_outflows, 2),
                'color':           OTHER_COLOR,
                '_nna':            other_nna,
            })

    segments = _assign_nna_colors(segments)

    # --- Per-relationship NNA distribution ---
    empty_nna_dist = calculate_nna_distribution_stats(pd.Series([], dtype=float))
    total_dist = empty_nna_dist
    by_segment_dist = {}

    if cp_end is not None and cp_start is not None and rel_geo_lookup is not None:
        rel_nna = _compute_rel_period_nna(cp_end, cp_start)
        rel_nna['state'] = rel_nna['relationship_id'].map(rel_geo_lookup).fillna('Unknown')

        # Filter to US with non-blank state; keep 'Unknown' matching geo_end treatment
        rel_nna = rel_nna[
            rel_nna['state'].notna() &
            (rel_nna['state'] != '')
        ]

        total_dist = calculate_nna_distribution_stats(rel_nna['period_nna'])

        # Top segment keys (state lowercase)
        seg_keys = {s['key']: s['label'] for s in segments if s['key'] != 'other'}
        for key, label in seg_keys.items():
            state_nna = rel_nna[rel_nna['state'].str.lower() == key]['period_nna']
            by_segment_dist[key] = calculate_nna_distribution_stats(state_nna)

    # --- Y6b: Per-state city-level NNA distribution drill-down ---
    geo_drill_dist = {}
    if (cp_end is not None and cp_start is not None
            and rel_geo_lookup is not None and rel_city_lookup is not None):
        # rel_nna already computed above; add city
        if 'period_nna' not in rel_nna.columns:
            rel_nna = _compute_rel_period_nna(cp_end, cp_start)
            rel_nna['state'] = rel_nna['relationship_id'].map(rel_geo_lookup).fillna('Unknown')
        rel_nna['city'] = rel_nna['relationship_id'].map(rel_city_lookup).fillna('Unknown')

        seg_keys = {s['key']: s['label'] for s in segments if s['key'] != 'other'}
        for key, label in seg_keys.items():
            state_rels = rel_nna[rel_nna['state'].str.lower() == key]
            if state_rels.empty:
                continue
            # Per-city distributions within this state
            city_dists = {}
            for city_name, city_group in state_rels.groupby('city'):
                if city_name == 'Unknown' or len(city_group) < 2:
                    continue
                city_key = city_name.lower().replace(' ', '_').replace('-', '_')
                city_dists[city_key] = calculate_nna_distribution_stats(city_group['period_nna'])
            if city_dists:
                geo_drill_dist[key] = {
                    'total': by_segment_dist.get(key, empty_nna_dist),
                    'by_city': city_dists,
                }

    return {
        'donut': {
            'title':    'NNA by State',
            'total':    round(total_net_nna, 2),
            'total_abs': round(total_abs_nna, 2),
            'segments': segments
        },
        'distribution': {
            'total':      total_dist,
            'by_segment': by_segment_dist
        },
        'drill': geo_drill_dist,
        'metrics': {
            'nna':          round(total_net_nna, 2),
            'client_count': int(merged['num_relationships'].sum())
        }
    }


def build_nna_adv_view(end_ts: pd.Timestamp,
                       start_ts: pd.Timestamp,
                       adv_ts: pd.DataFrame,
                       cp_end: pd.DataFrame = None,
                       cp_start: pd.DataFrame = None,
                       rel_arch_lookup: pd.Series = None,
                       client_dim: pd.DataFrame = None) -> dict:
    """
    Build NNA-mode ADV view: period-differenced NNA by architect.

    Same pattern as NNA GEO but keyed on architect instead of state.
    Distribution: per-relationship period NNA histogram (signed, symmetric log bins).
    """
    adv_end   = adv_ts[adv_ts['date'] == end_ts].copy()
    adv_start = adv_ts[adv_ts['date'] == start_ts]

    adv_end = adv_end[adv_end['architect'].notna()]

    if adv_end.empty:
        return _empty_nna_view('NNA by Architect')

    start_cols = adv_start[['architect', 'nna', 'cum_inflows', 'cum_outflows']].copy()
    start_cols = start_cols.rename(columns={
        'nna': 'nna_start', 'cum_inflows': 'inflows_start', 'cum_outflows': 'outflows_start'
    })
    merged = adv_end.merge(start_cols, on='architect', how='left')
    merged['nna_start']      = merged['nna_start'].fillna(0)
    merged['inflows_start']  = merged['inflows_start'].fillna(0)
    merged['outflows_start'] = merged['outflows_start'].fillna(0)

    merged['period_nna']      = merged['nna']          - merged['nna_start']
    merged['period_inflows']  = merged['cum_inflows']  - merged['inflows_start']
    merged['period_outflows'] = merged['cum_outflows'] - merged['outflows_start']

    merged = merged.reindex(merged['period_nna'].abs().sort_values(ascending=False).index)

    total_abs_nna = float(merged['period_nna'].abs().sum())
    total_net_nna = float(merged['period_nna'].sum())

    top    = merged.head(MAX_SEGMENTS)
    others = merged.iloc[MAX_SEGMENTS:]

    segments = []
    for _, row in top.iterrows():
        arch    = row['architect']
        nna_val = float(row['period_nna'])
        segments.append({
            'key':             arch.lower().replace(' ', '_').replace('-', '_'),
            'label':           arch,
            'aua':             round(abs(nna_val), 2),
            'aua_pct':         round(abs(nna_val) / total_abs_nna * 100, 1) if total_abs_nna > 0 else 0.0,
            'value':           round(nna_val, 2),
            'client_count':    int(row.get('num_relationships', 0)),
            'period_inflows':  round(float(row['period_inflows']), 2),
            'period_outflows': round(float(row['period_outflows']), 2),
            'color':           '',
            '_nna':            nna_val,
        })

    if not others.empty:
        other_nna      = float(others['period_nna'].sum())
        other_inflows  = float(others['period_inflows'].sum())
        other_outflows = float(others['period_outflows'].sum())
        other_count    = int(others['num_relationships'].sum())
        if abs(other_nna) > 0:
            segments.append({
                'key':             'other',
                'label':           'Other Architects',
                'aua':             round(abs(other_nna), 2),
                'aua_pct':         round(abs(other_nna) / total_abs_nna * 100, 1) if total_abs_nna > 0 else 0.0,
                'value':           round(other_nna, 2),
                'client_count':    other_count,
                'period_inflows':  round(other_inflows, 2),
                'period_outflows': round(other_outflows, 2),
                'color':           OTHER_COLOR,
                '_nna':            other_nna,
            })

    segments = _assign_nna_colors(segments)

    # --- Per-relationship NNA distribution ---
    empty_nna_dist = calculate_nna_distribution_stats(pd.Series([], dtype=float))
    total_dist = empty_nna_dist
    by_segment_dist = {}

    if cp_end is not None and cp_start is not None and rel_arch_lookup is not None:
        rel_nna = _compute_rel_period_nna(cp_end, cp_start)
        rel_nna['architect'] = rel_nna['relationship_id'].map(rel_arch_lookup).fillna('Unassigned')

        total_dist = calculate_nna_distribution_stats(rel_nna['period_nna'])

        # Top segment keys (architect name -> key)
        seg_keys = {s['key']: s['label'] for s in segments if s['key'] != 'other'}
        for key, label in seg_keys.items():
            arch_nna = rel_nna[
                rel_nna['architect'].str.lower().str.replace(' ', '_').str.replace('-', '_') == key
            ]['period_nna']
            by_segment_dist[key] = calculate_nna_distribution_stats(arch_nna)

    # --- Y6d: Per-architect relationship-level NNA distribution drill-down ---
    adv_drill_dist = {}
    if cp_end is not None and cp_start is not None and rel_arch_lookup is not None:
        # rel_nna already computed above
        # Add relationship names for labeling
        name_map = None
        if client_dim is not None and 'relationship_name' in client_dim.columns:
            name_map = client_dim.set_index('relationship_id')['relationship_name']

        for key, label in seg_keys.items():
            arch_rels = rel_nna[
                rel_nna['architect'].str.lower().str.replace(' ', '_').str.replace('-', '_') == key
            ]
            if len(arch_rels) < 2:
                continue
            # Compute the distribution for all relationships under this architect
            arch_dist = calculate_nna_distribution_stats(arch_rels['period_nna'])
            adv_drill_dist[key] = {
                'distribution': arch_dist,
                'relationship_count': len(arch_rels),
            }

    return {
        'donut': {
            'title':    'NNA by Architect',
            'total':    round(total_net_nna, 2),
            'total_abs': round(total_abs_nna, 2),
            'segments': segments
        },
        'distribution': {
            'total':      total_dist,
            'by_segment': by_segment_dist
        },
        'drill': adv_drill_dist,
        'metrics': {
            'nna':          round(total_net_nna, 2),
            'client_count': int(merged['num_relationships'].sum())
        }
    }


def _empty_nna_view(title: str) -> dict:
    """Return a zeroed-out NNA view structure."""
    empty_dist = calculate_distribution_stats(pd.Series([], dtype=float))
    return {
        'donut': {'title': title, 'total': 0, 'total_abs': 0, 'segments': []},
        'distribution': {'total': empty_dist, 'by_segment': {}},
        'metrics': {'nna': 0, 'client_count': 0}
    }


# ---------------------------------------------------------------------------
# CLA views (NMNC/NMEC lifecycle decomposition per GEO/ADV segment)
# ---------------------------------------------------------------------------

def build_cla_view(end_ts: pd.Timestamp,
                   start_ts: pd.Timestamp,
                   client_perf: pd.DataFrame,
                   client_dim: pd.DataFrame,
                   rel_geo_lookup: pd.Series,
                   rel_arch_lookup: pd.Series,
                   verbose: bool = False) -> dict:
    """
    Build CLA view for one period: NMNC/NMEC decomposition within GEO and ADV segments.

    For each relationship:
      1. Compute period NNA = nna(end) - nna(start)
      2. Classify as NMNC (first_seen_date > start) or NMEC (first_seen_date <= start)
      3. Aggregate by (segment, lifecycle_bucket)

    Output is keyed by cohort ('geo', 'adv'), each containing a list of segments
    with nested nmnc/nmec objects. This powers the diverging stacked bar chart.
    """
    cp_end   = client_perf[client_perf['date'] == end_ts].copy()
    cp_start = client_perf[client_perf['date'] == start_ts][['relationship_id', 'nna', 'cum_inflows', 'cum_outflows']]

    if cp_end.empty:
        return _empty_cla_view()

    # Merge start-of-period values
    cp_start = cp_start.rename(columns={
        'nna': 'nna_start', 'cum_inflows': 'inflows_start', 'cum_outflows': 'outflows_start'
    })
    merged = cp_end.merge(cp_start, on='relationship_id', how='left')
    merged['nna_start']      = merged['nna_start'].fillna(0)
    merged['inflows_start']  = merged['inflows_start'].fillna(0)
    merged['outflows_start'] = merged['outflows_start'].fillna(0)

    merged['period_nna']      = merged['nna']          - merged['nna_start']
    merged['period_inflows']  = merged['cum_inflows']  - merged['inflows_start']
    merged['period_outflows'] = merged['cum_outflows'] - merged['outflows_start']

    # Join first_seen_date for lifecycle classification
    if 'first_seen_date' in client_dim.columns:
        fsd_map = client_dim.set_index('relationship_id')['first_seen_date']
        merged['first_seen_date'] = merged['relationship_id'].map(fsd_map)
        merged['first_seen_date'] = pd.to_datetime(merged['first_seen_date'])
    else:
        merged['first_seen_date'] = pd.NaT

    # NMNC = first appeared AFTER start of this period; NMEC = existed before
    merged['lifecycle'] = np.where(
        merged['first_seen_date'].notna() & (merged['first_seen_date'] > start_ts),
        'nmnc', 'nmec'
    )

    # Attach segment assignments
    merged['state']     = merged['relationship_id'].map(rel_geo_lookup).fillna('Unknown')
    merged['architect'] = merged['relationship_id'].map(rel_arch_lookup).fillna('Unassigned')

    if verbose:
        n_nmnc = (merged['lifecycle'] == 'nmnc').sum()
        n_nmec = (merged['lifecycle'] == 'nmec').sum()
        nmnc_nna = merged.loc[merged['lifecycle'] == 'nmnc', 'period_nna'].sum()
        nmec_nna = merged.loc[merged['lifecycle'] == 'nmec', 'period_nna'].sum()
        print(f"  CLA: {n_nmnc} NMNC rels (${nmnc_nna:,.0f} NNA), "
              f"{n_nmec} NMEC rels (${nmec_nna:,.0f} NNA)")

    geo_segments = _build_cla_segments(merged, 'state', 'Unknown')
    adv_segments = _build_cla_segments(merged, 'architect', 'Unassigned')

    firm_totals = _build_cla_totals(merged)

    return {
        'geo': {
            'segments': geo_segments,
            'totals':   firm_totals,
        },
        'adv': {
            'segments': adv_segments,
            'totals':   firm_totals,
        }
    }


def _build_cla_segments(df: pd.DataFrame, group_col: str, exclude_val: str) -> list:
    """
    Aggregate NMNC/NMEC lifecycle stats per segment (state or architect).

    Returns a list of segments sorted by absolute total NNA, each containing
    nested nmnc and nmec objects with flows and counts.
    """
    # Filter out unknown/unassigned
    filtered = df[df[group_col] != exclude_val].copy()

    # Aggregate per (segment, lifecycle)
    agg = (
        filtered
        .groupby([group_col, 'lifecycle'])
        .agg(
            nna=('period_nna', 'sum'),
            inflows=('period_inflows', 'sum'),
            outflows=('period_outflows', 'sum'),
            count=('relationship_id', 'nunique'),
        )
        .reset_index()
    )

    # Pivot to one row per segment
    seg_totals = (
        filtered.groupby(group_col)
        .agg(nna_total=('period_nna', 'sum'), rel_count=('relationship_id', 'nunique'))
        .reset_index()
        .sort_values('nna_total', key=lambda s: s.abs(), ascending=False)
    )

    top_segs   = seg_totals.head(MAX_SEGMENTS)
    other_segs = seg_totals.iloc[MAX_SEGMENTS:]

    segments = []
    for _, row in top_segs.iterrows():
        seg_name  = row[group_col]
        seg_key   = seg_name.lower().replace(' ', '_').replace('-', '_')
        nna_total = float(row['nna_total'])

        nmnc_data = agg[(agg[group_col] == seg_name) & (agg['lifecycle'] == 'nmnc')]
        nmec_data = agg[(agg[group_col] == seg_name) & (agg['lifecycle'] == 'nmec')]

        nmnc = _lifecycle_bucket(nmnc_data)
        nmec = _lifecycle_bucket(nmec_data)

        segments.append({
            'key':       seg_key,
            'label':     seg_name,
            'nna_total': round(nna_total, 2),
            'nmnc':      nmnc,
            'nmec':      nmec,
        })

    # Other bucket
    if not other_segs.empty:
        other_names = other_segs[group_col].tolist()
        other_agg   = agg[agg[group_col].isin(other_names)]

        other_nmnc_data = other_agg[other_agg['lifecycle'] == 'nmnc']
        other_nmec_data = other_agg[other_agg['lifecycle'] == 'nmec']

        other_nna = float(other_segs['nna_total'].sum())
        if abs(other_nna) > 0:
            segments.append({
                'key':       'other',
                'label':     'Other',
                'nna_total': round(other_nna, 2),
                'nmnc':      _lifecycle_bucket(other_nmnc_data),
                'nmec':      _lifecycle_bucket(other_nmec_data),
            })

    return segments


def _lifecycle_bucket(data: pd.DataFrame) -> dict:
    """Summarize one lifecycle bucket (NMNC or NMEC) from aggregated rows."""
    if data.empty:
        return {'nna': 0, 'inflows': 0, 'outflows': 0, 'count': 0}
    return {
        'nna':      round(float(data['nna'].sum()), 2),
        'inflows':  round(float(data['inflows'].sum()), 2),
        'outflows': round(float(data['outflows'].sum()), 2),
        'count':    int(data['count'].sum()),
    }


def _build_cla_totals(df: pd.DataFrame) -> dict:
    """Compute firm-wide CLA totals."""
    nmnc = df[df['lifecycle'] == 'nmnc']
    nmec = df[df['lifecycle'] == 'nmec']
    return {
        'nna':        round(float(df['period_nna'].sum()), 2),
        'nmnc_nna':   round(float(nmnc['period_nna'].sum()), 2),
        'nmec_nna':   round(float(nmec['period_nna'].sum()), 2),
        'nmnc_count': int(nmnc['relationship_id'].nunique()),
        'nmec_count': int(nmec['relationship_id'].nunique()),
    }


def _empty_cla_view() -> dict:
    """Return a zeroed-out CLA view structure."""
    empty = {
        'segments': [],
        'totals': {'nna': 0, 'nmnc_nna': 0, 'nmec_nna': 0, 'nmnc_count': 0, 'nmec_count': 0}
    }
    return {'geo': empty, 'adv': empty}


# ---------------------------------------------------------------------------
# Main assembly
# ---------------------------------------------------------------------------

def generate_header_metrics(verbose: bool = False, granularity: str = 'quarterly') -> dict:
    """
    Load all gold tables, compute 4-period views (AUA, NNA, GEO, ADV, CLA),
    return JSON-ready dict.

    granularity: 'quarterly' (default), 'monthly', or 'annual'
    NMNC/NMEC classification applies boundaries appropriate to each granularity.
    """
    print("Loading gold tables from S3...")
    client_perf, acct_perf, acct_dim, client_dim, geo_ts, adv_ts, rel_arch_lookup = load_data(verbose=verbose)

    ref_date = client_perf['date'].max()
    periods  = get_periods(ref_date, granularity=granularity)
    period_pairs = get_period_pairs(periods, granularity=granularity)

    data_as_of   = ref_date.strftime('%Y-%m-%d')

    # Collect all dates we need: 4 period ends + up to 4 period starts
    all_dates = set()
    for pp in period_pairs.values():
        all_dates.add(pp['end'])
        all_dates.add(pp['start'])
    target_dates = sorted(all_dates)

    print(f"Reference date: {data_as_of}")
    if verbose:
        for key, p in periods.items():
            pp = period_pairs[key]
            print(f"  {key}: {p['date']} ({p['label']}) | "
                  f"period start: {pp['start'].strftime('%Y-%m-%d')}")

    # Pre-filter to target dates (memory optimization)
    client_perf_filtered = client_perf[client_perf['date'].isin(target_dates)]
    acct_perf_filtered   = acct_perf[acct_perf['date'].isin(target_dates)]

    # account_performance may lag client_performance (05b excluded from incremental runs).
    # Build a fallback map: for each target date missing from acct_perf, use the closest
    # prior date that IS available. This keeps cities/distributions populated even when
    # account_performance hasn't been rebuilt yet.
    acct_dates_available = set(acct_perf['date'].unique())
    _acct_date_fallback = {}
    for td in target_dates:
        if td in acct_dates_available:
            _acct_date_fallback[td] = td
        else:
            # Find closest prior date in account_performance
            prior = acct_perf['date'][acct_perf['date'] <= td].max()
            if pd.notna(prior):
                _acct_date_fallback[td] = prior
                print(f"  NOTE: account_performance missing {td.date()} -- "
                      f"falling back to {prior.date()} for cities/distributions")
            else:
                _acct_date_fallback[td] = None

    # Extend acct_perf_filtered to include fallback dates
    all_acct_dates = set(target_dates) | {v for v in _acct_date_fallback.values() if v is not None}
    acct_perf_filtered = acct_perf[acct_perf['date'].isin(all_acct_dates)]

    # Build relationship -> state/city lookups for CLA-GEO and Y6b drill-down
    rel_geo_lookup = _build_rel_geo_lookup(acct_dim)
    rel_city_lookup = _build_rel_city_lookup(acct_dim)

    views = {'aua': {}, 'nna': {}, 'geo': {}, 'adv': {}, 'cla': {}}

    for period_key, period_info in periods.items():
        ts       = period_info['_ts']
        start_ts = period_pairs[period_key]['start']
        print(f"Building views for {period_key} ({period_info['date']})...")

        cp_day = client_perf_filtered[client_perf_filtered['date'] == ts]
        ap_date = _acct_date_fallback.get(ts, ts)
        ap_day = acct_perf_filtered[acct_perf_filtered['date'] == ap_date] if ap_date is not None else pd.DataFrame()

        if cp_day.empty:
            print(f"  WARN: No client_performance data for {period_info['date']} -- skipping period")
            views['aua'][period_key] = _empty_view('AUA by Tax Status')
            views['nna'][period_key] = _empty_nna_view('NNA by State')
            views['geo'][period_key] = _empty_view('AUA by State')
            views['adv'][period_key] = _empty_view('AUA by Architect')
            views['cla'][period_key] = _empty_cla_view()
            continue

        # --- AUA view: tax status donut (unchanged) ---
        views['aua'][period_key] = _build_aua_tax_view(cp_day, client_dim)

        # --- GEO view: AUA by State (unchanged) ---
        views['geo'][period_key] = build_geo_view(ts, geo_ts, ap_day, acct_dim)

        # --- ADV view: AUA by Architect (unchanged) ---
        views['adv'][period_key] = build_adv_view(
            ts, adv_ts, cp_day, ap_day, acct_dim, client_dim, rel_arch_lookup
        )

        # --- NNA view: period-differenced NNA by GEO + ADV (blue/red donuts) ---
        cp_start = client_perf_filtered[client_perf_filtered['date'] == start_ts]
        nna_geo = build_nna_geo_view(ts, start_ts, geo_ts,
                                      cp_end=cp_day, cp_start=cp_start,
                                      rel_geo_lookup=rel_geo_lookup,
                                      rel_city_lookup=rel_city_lookup)
        nna_adv = build_nna_adv_view(ts, start_ts, adv_ts,
                                      cp_end=cp_day, cp_start=cp_start,
                                      rel_arch_lookup=rel_arch_lookup,
                                      client_dim=client_dim)
        views['nna'][period_key] = {
            'geo': nna_geo,
            'adv': nna_adv,
        }

        # --- CLA view: NMNC/NMEC lifecycle decomposition (stacked bars) ---
        views['cla'][period_key] = build_cla_view(
            ts, start_ts, client_perf_filtered, client_dim,
            rel_geo_lookup, rel_arch_lookup, verbose=verbose
        )

        if verbose:
            aua_total = views['aua'][period_key]['donut']['total']
            geo_segs  = len(views['geo'][period_key]['donut']['segments'])
            adv_segs  = len(views['adv'][period_key]['donut']['segments'])
            geo_aua   = views['geo'][period_key]['donut']['total']
            adv_aua   = views['adv'][period_key]['donut']['total']
            nna_net   = nna_geo['metrics']['nna']
            cla_nmnc  = views['cla'][period_key]['geo']['totals']['nmnc_nna']
            cla_nmec  = views['cla'][period_key]['geo']['totals']['nmec_nna']
            print(f"  AUA: total ${aua_total:,.0f}")
            print(f"  GEO: {geo_segs} segments, total AUA ${geo_aua:,.0f}")
            print(f"  ADV: {adv_segs} segments, total AUA ${adv_aua:,.0f}")
            print(f"  NNA: net ${nna_net:,.0f} (GEO view)")
            print(f"  CLA: NMNC ${cla_nmnc:,.0f} | NMEC ${cla_nmec:,.0f}")

    # Strip internal _ts key from periods before output
    periods_out = {k: {'date': v['date'], 'label': v['label']} for k, v in periods.items()}

    return {
        'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'data_as_of':   data_as_of,
        'firm_id':      '49financial',
        'firm_name':    '49 Financial',
        'granularity':  granularity,
        'periods':      periods_out,
        'views':        views
    }


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def write_local(payload: dict, output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, default=str)
    print(f"OK: Written to {path} ({path.stat().st_size:,} bytes)")


def write_s3(payload: dict, granularity: str = 'quarterly') -> None:
    """Write payload to S3 with granularity-specific path."""
    body = json.dumps(payload, separators=(',', ':'), default=str).encode('utf-8')
    s3 = boto3.client('s3', region_name='us-east-1')
    # Use granularity in path: header_metrics_quarterly.json, header_metrics_monthly.json, etc.
    key = f'gold/partner_analytics/header_metrics_{granularity}.json'
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=body,
        ContentType='application/json',
        CacheControl='public, max-age=300, s-maxage=3600'
    )
    print(f"OK: Uploaded to s3://{S3_BUCKET}/{key} ({len(body):,} bytes)")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Generate partner_analytics/header_metrics.json from gold tables'
    )
    parser.add_argument(
        '--upload', action='store_true',
        help='Upload outputs to S3 (generates quarterly, monthly, annual variants)'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Compute and validate output but do not write anywhere'
    )
    parser.add_argument(
        '--output', type=str, default=None,
        help=f'Local output path (default: {DEFAULT_LOCAL_OUTPUT}). Will add _GRANULARITY suffix.'
    )
    parser.add_argument(
        '--granularity', type=str, choices=['quarterly', 'monthly', 'annual'], default=None,
        help='Generate only specific granularity (default: all three)'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Verbose logging'
    )
    args = parser.parse_args()

    print('============================================================')
    print('09_generate_partner_analytics.py (Multi-Granularity)')
    print(f'Started: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}')
    print('============================================================')

    # Determine which granularities to generate
    granularities = [args.granularity] if args.granularity else ['quarterly', 'monthly', 'annual']

    for granularity in granularities:
        print(f"\nGenerating {granularity} variant...")
        payload = generate_header_metrics(verbose=args.verbose, granularity=granularity)

        # Validate: check that current period has non-zero AUA and NNA data
        current_geo_aua = payload['views']['geo']['current']['donut']['total']
        current_adv_aua = payload['views']['adv']['current']['donut']['total']
        current_nna_net = payload['views']['nna']['current']['geo']['metrics']['nna']
        current_cla     = payload['views']['cla']['current']['geo']['totals']
        print(f"  Validation: GEO AUA=${current_geo_aua:,.0f}, ADV AUA=${current_adv_aua:,.0f}")
        print(f"    NNA net=${current_nna_net:,.0f}")
        print(f"    CLA: NMNC=${current_cla['nmnc_nna']:,.0f} ({current_cla['nmnc_count']} rels) | "
              f"NMEC=${current_cla['nmec_nna']:,.0f} ({current_cla['nmec_count']} rels)")

        if current_geo_aua == 0:
            print("    WARN: GEO current period AUA is zero -- check nna_aua_by_geography.parquet")
        if current_adv_aua == 0:
            print("    WARN: ADV current period AUA is zero -- check nna_aua_by_advisor.parquet")

        if args.dry_run:
            print(f"  OK: Dry run for {granularity} -- no output written")
            period_keys = list(payload['periods'].keys())
            for period_key in period_keys:
                g_total = payload['views']['geo'][period_key]['donut']['total']
                a_total = payload['views']['adv'][period_key]['donut']['total']
                n_net   = payload['views']['nna'][period_key]['geo']['metrics']['nna']
                cla_t   = payload['views']['cla'][period_key]['geo']['totals']
                label   = payload['periods'][period_key]['label']
                print(f"    {period_key} ({label}): GEO=${g_total:,.0f}  ADV=${a_total:,.0f}  "
                      f"NNA=${n_net:,.0f}  NMNC=${cla_t['nmnc_nna']:,.0f}  NMEC=${cla_t['nmec_nna']:,.0f}")
        elif args.upload:
            write_s3(payload, granularity=granularity)
        else:
            if args.output:
                # Insert granularity before .json extension
                output_path = args.output.replace('.json', f'_{granularity}.json')
            else:
                output_path = DEFAULT_LOCAL_OUTPUT.replace('.json', f'_{granularity}.json')
            write_local(payload, output_path)

    if args.dry_run:
        print("\nOK: Dry run complete -- no output written")
        sys.exit(0)

    print('\n============================================================')
    print(f'COMPLETE: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}')
    print(f'Generated {len(granularities)} variant(s): {", ".join(granularities)}')
    print('============================================================')


if __name__ == '__main__':
    main()
```

---

## Participant Background

### 0.4.0_DE_ClientPlatform -- Recent Session Logs

#### advi_49fnv3_f3_f5_n1n2_investigation.md

# ADVI_49FNV3 — F3/F5/N1-N2 Investigation and Closeout — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-06
**Start Time:** session start
**End Time:** session end

## Objective

Close out three pending ADVI_49FNV3 DE task orders: F5-DE (QTD/YTD period toggle
investigation), F3 (DistributionTab NNA geo drill wiring), and N1-N2-DE (firm dashboard +
advisor book wiring). DS confirmed F5 is not a Lambda bug; DT confirmed N1+N2 wiring was
already implemented in the prior session (1dc96b5).

---

## Work Completed

### 1. F5-DE: QTD/YTD Period Toggle Investigation

**Task order:** `ADVI_49FNV3.F5-DE.qtd-ytd-frontend-investigation.md`

**DS finding (from advi_49fnv3_f1_f5_investigation.md):**
- `bd-portal-advisor-publisher` computes `qtd_start = Jan 1, 2026` and
  `ytd_start = Jan 1, 2026` for any date in Q1. Identical. Lambda is correct.
- Root cause is **not** in the Lambda.

**DT finding (from advi_49fnv3_session1.md, prior session):**
- `periodToChartWindow('qtd')` in `AdvisorsTab.tsx` maps to `'3M'` (trailing 90 days).
- `periodToChartWindow('ytd')` maps to `'1Y'` (trailing 1 year).
- The leaderboard publisher emits **rolling trailing windows** only. In March 2026,
  QTD = Jan 1 to today (~65 days) but `'3M'` = trailing 90 days from today. These are
  different date ranges producing different NNA values.
- **Frontend cannot fix this alone.** Fix requires DS to emit a `qtd` calendar window
  in `architect_leaderboard.json` and `implementor_leaderboard.json`.

**DE finding:** No code change made. Root cause is rolling-vs-calendar window mismatch.
Fix is Lambda-side (DS task). Task order marked complete.

---

### 2. F3: DistributionTab NNA Geo Drill Investigation

**Task order:** `ADVI_49FNV3.F3.segment-drilldown-wiring.md`

**Investigation:**

Audited `DistributionTab.tsx` and `types.ts` against task order requirements.

**Q1: Is `nna_geo_drill` from `timeseries_chart.json` consumed by the Snapshot NNA donut?**

NO — and correctly so. `nna_geo_drill` from `timeseries_chart.json` has type
`NNAGeoDrillView` (`{ [stateKey]: { categories: string[], data: NNASeriesPoint[] } }`).
This is a **time series**, not donut segment data. It is consumed by
`ContinuousNnaDivergingView` (line 443) for the continuous NNA chart — the correct use.

**Q2: Is state→city drill wired for the Snapshot NNA geo donut?**

YES — already wired. `handleSegmentClick` at line 1815-1834 handles NNA geo drill:
- If `nnaDrillData[seg.key]` exists → `setSelectedStateKey(seg.key)` + `setGeoDrillLevel('city')`
- City segments built from `nnaDrillData[selectedStateKey].by_city` at line 1658-1668

`nnaDrillData` reads from `analyticsData.views.nna[period].geo.drill` in
`header_metrics_quarterly.json`. This is the correct data source for distribution stats.

**Q3: Is `by_city` data populated in the published JSON?**

YES — confirmed in `data/black_diamond/scripts/gold/09_generate_partner_analytics.py`,
lines 1061-1087 (Y6b block): `geo_drill_dist[state] = { total: ..., by_city: {...} }`.
The EC2 script emits `by_city: Record<string, DistributionStats>` for each top state
that has at least 2 relationships in any city. This feeds into `views.nna[period].geo.drill`.

**Q4: City→client drill?**

NOT available in GEO mode. `by_city` entries are `DistributionStats` aggregates, not
individual relationship records. Y6d client drill is ADV-mode only (architect →
relationships via `views.nna[period].adv.drill[arch].distribution`). There is no
per-relationship list within geo city entries. This is a data constraint, not a wiring gap.

**Conclusion:** No code change needed. F3 wiring is complete in existing code. Task order
marked complete.

---

### 3. N1-N2-DE: Firm Dashboard + Advisor Book Wiring Verification

**Task order:** `ADVI_49FNV3.N1-N2-DE.firm-dashboard-and-advisor-book-wiring.md`

Prior DT session (1dc96b5) implemented all requirements. Verified against task order:

| Requirement | Status |
|---|---|
| TypeScript interfaces from design brief Section 6 | Done — already in `types.ts` (AdvisorBookResponse, BooksClientDetailResponse, BooksClientAccount, BooksClientTaxDetail, CostBasisYear, GainPosition, OpenLot) |
| N1 Firm Overview KPIs | Done — `N1FirmDashboard` component, Panel 1 (line 930-940 of ClientsTab.tsx) |
| N1 Tax Status Breakdown | Done — TaxRow components, Panel 2 (lines 942-952) |
| N1 Engagement Summary | Done — FlowMetric + MetricCard, Panel 3 (lines 954-966) |
| N1 AUA by Advisor (1Y, sorted by total_aua, row click -> N2) | Done — `AdvisorSummaryTable` (line 329, sorts by total_aua desc, onClick -> handleSelectAdvisor) |
| N2 Advisor Book View (L2AdvisorBook) | Done — all 4 panels: Summary KPIs, Tax Exposure, Engagement, Clients table (lines 345-426) |
| advisorId slug fix | Done — exact replica of `_advisor_id()` at line 186 |
| Access gate `isInternal() \|\| isDev()` | Done — line 52-53 |
| Data fetch: leaderboard + clients_tab in parallel | Done — Promise.all at lines 84-98 |

Task order marked complete. Updated N1-N2-RD task order dependency from `pending` to
`complete`. RD may review and polish visual layout per their task order.

---

## Decisions Made

| Decision | Rationale |
|---|---|
| F5-DE: no frontend fix | Root cause is rolling-vs-calendar window mismatch in leaderboard publisher. Frontend maps `qtd` to `'3M'` which is incorrect but unfixable until Lambda emits a `qtd` calendar window. Route to DS for Lambda fix. |
| F3: no wiring change | State→city drill already wired in `handleSegmentClick`. `nna_geo_drill` from timeseries_chart.json is correctly NOT used in snapshot donut — it's time series data for the continuous view. |
| F3: city→client gap as data constraint | EC2 script 09 emits `by_city: DistributionStats`, not relationship lists. ADV mode has client drill but GEO city level does not. Correct behavior — no stub or workaround. |
| N1-N2-DE: complete without new code | DT implemented all functional requirements in 1dc96b5. No additional wiring needed. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI_49FNV3.F5-DE.qtd-ytd-frontend-investigation.md` | status -> complete | No — local only |
| `org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI_49FNV3.F3.segment-drilldown-wiring.md` | status -> complete | No — local only |
| `org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI_49FNV3.N1-N2-DE.firm-dashboard-and-advisor-book-wiring.md` | status -> complete | No — local only |
| `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI_49FNV3.N1-N2-RD.firm-dashboard-and-advisor-book-ui.md` | dependency status -> complete, constraint note updated | No — local only |

---

## Blockers

- **F5 fix**: BLOCKED on DS — Lambda must emit a `qtd` calendar window in
  `architect_leaderboard.json` / `implementor_leaderboard.json`. Task order F5-DS is
  with 0.4.0_DS_ClientPlatform.
- **F1 GRO data**: BLOCKED on DT — bd-portal-publisher redeploy required per
  `docs/briefs/devops-brief-49fnv3-f1-gro-publisher-fix.md`. No DE action.

---

## Current State

**Status:** COMPLETE
**Active branch:** `CLOUD`

All three DE task orders for ADVI_49FNV3 are closed. No portal code changes were made
this session — all findings were investigative. Key result: the snapshot NNA geo drill
in DistributionTab.tsx is already correctly wired via `views.nna[period].geo.drill[state].by_city`
from partner_analytics JSON. N1+N2 wiring in ClientsTab.tsx is complete. N1-N2-RD task
order dependency is unblocked for 0.4.2_RD_AdvisorIntelligence.

---

## Next Steps

1. **[0.4.0_DS_ClientPlatform] F5 Lambda fix** — emit `qtd` calendar window in leaderboard
   JSON so `periodToChartWindow('qtd')` can map to `'qtd'` directly instead of `'3M'` approximation.
2. **[0.4.0_DT_ClientPlatform] F1 redeploy** — rebuild and redeploy bd-portal-publisher per
   devops brief to surface `growth_decomposition` in portal GRO mode.
3. **[0.4.2_RD_AdvisorIntelligence] N1-N2-RD visual polish** — dependency now resolved,
   RD can review DT's panel implementation and polish visual layout per task order.
4. **[0.4.2_RD_AdvisorIntelligence] F2, F4** — projected bars and stacked bar (already
   issued task orders per COO session).

**Files to touch next:**
- None (all DE items complete for this project sprint)

**Do NOT:**
- Wire `nna_geo_drill` from `timeseries_chart.json` into the snapshot NNA donut — it is
  a time series and is correctly placed in the continuous view.
- Fix F5 frontend-side — the window mismatch cannot be resolved without a Lambda-side
  `qtd` calendar window addition.

#### advi_49fnv3_f3_fix_nna_drill_tdz.md

# ADVI_49FNV3 F3-fix + F3b: NNA Drill Fixes -- 0.4.0_DE_ClientPlatform

**Date:** 2026-03-09
**Portal DEV commits:** `9c1881a` -> `3367cd8`
**Workspace CLOUD commit:** pending

## Objective

Fix the NNA snapshot drill error in DistributionTab.tsx. Andrew confirmed on 2026-03-09
that clicking a state in NNA+GEO Snapshot mode triggers an error. CTO reopened F3 via
task order `ADVI_49FNV3.F3-fix.nna-snapshot-drill-error.md`, overriding the prior
2026-03-06 investigative closeout.

---

## Work Completed

### 1. Root Cause: Temporal Dead Zone (TDZ) in useMemo Ordering

`nnaDrillData` was declared at line 1707 via `useMemo`, but consumed inside the
`segments` useMemo factory at line 1658. JavaScript `const` declarations are hoisted
but not initialized until execution reaches the declaration (TDZ).

**The crash sequence:**
1. User clicks a state segment in NNA+GEO Snapshot mode
2. `handleSegmentClick` sets `geoDrillLevel('city')` + `selectedStateKey(seg.key)`
3. React re-renders. The `segments` useMemo runs first (line 1655) because its deps
   (`geoDrillLevel`) changed
4. Inside the factory, the condition `metric === 'nna' && nnaDrillData?.[...]` executes
5. `nnaDrillData` is a `const` declared later at line 1707 -- still in the TDZ
6. `ReferenceError: Cannot access 'nnaDrillData' before initialization`

**Why it wasn't caught earlier:**
- On initial render, `geoDrillLevel === 'state'` so the `if` at line 1656 is false --
  `nnaDrillData` is never accessed, no TDZ error
- AUA mode drill doesn't hit the NNA branch (`metric !== 'nna'`) so also no TDZ
- The error only surfaces on the FIRST NNA drill click (the re-render where
  `geoDrillLevel` transitions from 'state' to 'city')

### 2. Secondary Bug: Missing useMemo Dependencies

The `segments` dependency array was `[cohort, geoDrillLevel, advDrillLevel, selectedStateKey, selectedArchitectKey, baseSegments]` -- missing both `metric` and `nnaDrillData`. This meant:
- Switching between AUA and NNA while drilled would use stale city segments
- Changes to the drill data (e.g., period change) wouldn't recompute segments

### 3. Fix Applied

Two changes in a single commit (`9c1881a`):
1. Moved `nnaDrillData` useMemo declaration from line 1707 to line 1655 (before
   `segments` memo). Added comment: "MUST be declared before `segments` memo which reads it"
2. Added `metric` and `nnaDrillData` to the `segments` dependency array

### 4. Drill Path Verification (All 5 Acceptance Criteria)

| Drill Path | Status | Detail |
|---|---|---|
| GEO state -> city (NNA) | FIXED | `nnaDrillData` now accessible; `by_city` entries map to DonutSegment with `aua=abs(total)`, `client_count=count` |
| City -> client (NNA GEO) | Graceful | No per-relationship data in `by_city` (each entry is DistributionStats, not a segment list). City click toggles selection only. `hasNoDrillData` guard at line 1874 shows "No city-level data available" if segments empty |
| ADV architect -> client (NNA) | Graceful | ADV drill data has `{ distribution, relationship_count }` per architect, no per-relationship segments. `parent?.clients?.length` is false for NNA donut segments. Falls to empty segments -> `hasNoDrillData` UI message |
| GEO state -> city (AUA) | Unaffected | Uses `parent.cities` path (line 1683), not `nnaDrillData` |
| ADV architect -> client (AUA) | Unaffected | Uses `parent.clients` path (line 1694) |

### 5. F3b: Continuous NNA Drill Parity (`3367cd8`)

**Task order:** `ADVI_49FNV3.F3b.continuous-nna-drill-parity.md`

**Data investigation:** Checked `bd-portal-publisher` Lambda for drill data availability:
- `nna_geo_drill`: EXISTS -- `{ [state]: { categories, data } }` (city-level NNA timeseries)
- `nna_adv_drill`: DOES NOT EXIST -- Lambda only emits `nna_adv` (top-level architect NNA)
- No second-level city drill data (city within state is terminal)

**Changes to ContinuousNnaDivergingView:**

| Change | Detail |
|--------|--------|
| ADV drill enabled | Click architect legend item -> filters `nna_adv` to single-architect series (`categories: [drillParent]`). Shows that architect's NNA diverging bars only. |
| Drill state reset | `useEffect(() => setDrillParent(null), [cohort])` -- prevents stale drill on cohort switch |
| CLA-style breadcrumb | Replaced simple back button with breadcrumb: `ChevronLeft All States / StateName` (matches ClaContinuousView pattern) |
| Legend always visible | Categories shown at both levels: drillable with arrow at top, static (no arrow) when drilled. Uses `getCategoryDisplayName()` for consistent label formatting. |
| `canDrill` expanded | Was `cohort === 'geo' && !!data?.nna_geo_drill`. Now also `cohort === 'adv' && !!(nnaSeriesView?.categories?.length)` |
| `drillSeriesView` memo | Changed from inline ternary to `useMemo` with proper dependency tracking |

**Graceful degradation:** Since `nna_adv_drill` doesn't exist, the ADV drill shows the single-architect
series from the top-level `nna_adv` data (filtering categories to just the selected architect). This
produces a valid single-series diverging bar chart -- no error, no dead-end click.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Move declaration, don't restructure | Minimal diff. The memo logic is correct; only the declaration order was wrong. |
| No defensive try-catch | TDZ is a deterministic crash from declaration order, not a data shape issue. Moving the declaration eliminates it permanently. |
| City-to-client and ADV-to-client: accept graceful degradation | EC2 script 09 emits `DistributionStats` per city (not segment lists). ADV drill emits aggregate `distribution` per architect. Neither provides per-relationship detail for donut rendering. Existing `hasNoDrillData` UI handles this correctly. |
| F3b: ADV drill via category filter, not dedicated data | `nna_adv_drill` doesn't exist in Lambda. Filtering `nna_adv` to `categories: [architect]` achieves single-architect view without backend changes. |
| F3b: No second-level GEO drill | `nna_geo_drill[state]` is city-level timeseries -- already terminal. No per-city-relationship data exists in the Lambda output. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | F3-fix: Move nnaDrillData before segments; add metric + nnaDrillData to deps | Yes -- portal DEV `9c1881a` |
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | F3b: ADV drill + breadcrumb + legend parity in ContinuousNnaDivergingView | Yes -- portal DEV `3367cd8` |
| `org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI_49FNV3.F3-fix.nna-snapshot-drill-error.md` | status -> complete | No -- local only |
| `org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI_49FNV3.F3b.continuous-nna-drill-parity.md` | status -> complete | No -- local only |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`, workspace `CLOUD`

Two commits: `9c1881a` (F3-fix: snapshot TDZ crash) and `3367cd8` (F3b: continuous drill parity).
F3-fix moved `nnaDrillData` declaration above its consumer memo. F3b added ADV drill to
ContinuousNnaDivergingView (filter to single-architect series from nna_adv), CLA-style breadcrumb,
and always-visible category legend. `bunx tsc -b` clean. No `nna_adv_drill` data exists in Lambda,
so ADV drill uses category filtering as graceful degradation.

---

## Next Steps

1. **[0.4.0_DT_ClientPlatform] Push portal DEV** -- commits `594c3f6` (F2/F4/N1-N2) + `9c1881a` (F3-fix) + `3367cd8` (F3b) pending push. DT QA gate.
2. **[0.4.0_DE_ClientPlatform] Review RD commit `594c3f6`** -- F2 projected bars, F4 stacked bar, N1-N2 polish. Still pending DE review.

**Do NOT:**
- Add per-relationship donut segments to city or ADV drill -- the data doesn't exist in the EC2 output and there's no task order requesting it
- Modify `handleSegmentClick` -- the click guard logic is correct, it was only the memo ordering that was wrong
- Add `nna_adv_drill` to the Lambda without a DS task order -- current category filter approach is sufficient

#### benchmark_scatter_granular_selection.md

# Benchmark Scatter Granular Selection — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-06
**Portal DEV commits:** `60f1ee0` -> `0ac188c` -> `5cc598f` -> `b3f3bec` -> `adc5e4c` -> `fcaa484` -> `a1fb029` -> `a493db4` -> `312ca3d`
**Workspace CLOUD commit:** `pending`

## Objective

Add a general/granular state toggle to the Return vs Volatility scatter chart on the
ModelPortfolios Benchmark tab. Clicking a legend item enters granular state: only that
model's circle and paired benchmark diamond are visible, the chart auto-zooms around
them, and persistent tooltip cards appear on both points without hover. Clicking again
returns to general state. Clicking a different model while in granular state switches
context directly.

---

## Work Completed

### 1. Core State + Legend Interaction (`60f1ee0`)

Added `selectedModel: string | null` state. `null` = general, code string = granular.
- `filteredData` filters `scatterData` to the selected model's 2 points in granular state
- Axis domains recalculate from `filteredData` automatically — chart auto-zooms with no
  extra logic
- Model legend `<div>` items converted to `<button>` elements: toggle on same code,
  switch on different code, `opacity-30` on unselected items, white ring + bold label
  on selected item, 200ms transitions throughout

### 2. Persistent Tooltips — Iteration History

Six iterations to arrive at the correct implementation. Documented in full for future reference.

#### Attempt 1 — SVG text labels via `makeShapeRenderer` factory (`0ac188c`, `5cc598f`)
Approach: extend shape renderer to also draw SVG `<rect>` + `<text>` elements as
persistent labels when `showLabel=true`.
Issues: SVG text has no CSS wrapping control, size/content was too abbreviated, and
grid-aware placement (above/below based on return rank + axis padding) was overly
complex for what was essentially a cosmetic layer.
Reverted.

#### Attempt 2 — HTML cards below the chart (`b3f3bec`)
Approach: remove SVG labels entirely; render `<CustomTooltip active={true} ...>`
as a flex row of HTML divs below the `ResponsiveContainer`.
Issue: user wanted tooltips inside the chart adjacent to their data points, not
in a separate section below.
Reverted.

#### Attempt 3 — `Customized` component with `foreignObject` (`adc5e4c`)
Approach: use Recharts' `Customized` component (receives chart internals as props)
to render `<foreignObject>` tooltip cards at pixel positions computed from `xAxisMap`
and `yAxisMap` scales.
Issue: Recharts 3.x deprecated `Customized`. The `xAxisMap`/`yAxisMap` internal
state it relied on no longer exists in v3 — early-return guard always fired, nothing
rendered.

#### Attempt 4 — Recharts 3.x public hooks (`fcaa484`)
Approach: replace `Customized` with a `GranularTooltips` component (direct chart
child) using `useXAxisDomain(0)`, `useYAxisDomain(0)`, `usePlotArea()` — all public
v3 exports. Construct linear scales manually from domain + plot area to compute exact
pixel positions. Render `<foreignObject>` + `<CustomTooltip>`.
Issues: (a) `TH=128` too small — tooltip HTML was ~136px for long model names,
foreignObject clips at declared height. (b) bottom clamp used `plotBottom` (plot area
edge) not `chartHeight` (full SVG height), over-restricting vertical range.

#### Attempt 5 — Fix bottom clip (`a1fb029`)
Added `useChartHeight()` hook; clamp `ty` against `svgHeight - 8` rather than
`plotBottom`. Bumped `TH=160`. Resolved bottom cutoff.

#### Attempt 6 — No-wrap + Z-order (`a493db4`, `312ca3d`)
Two final issues:
1. Text wrapping: long model names wrapped at 220px foreignObject width. Fix: set
   `style={{ whiteSpace: 'nowrap' }}` on wrapper div (inherited by all CustomTooltip
   text); bumped `TW=300`, dropped `TH=130` (single-line content is shorter).
2. Z-order: Recharts 3.x renders custom children through its own pipeline, so
   CartesianGrid could appear after the `<g>` in SVG document order (last = topmost
   in SVG). Fix: `useLayoutEffect` with `svg.appendChild(g)` after each render —
   fires synchronously before browser paint, moves `<g>` to last child of the SVG
   unconditionally. Guard `svg.lastElementChild !== g` makes it a no-op when
   already in position.

### 3. Final Architecture of `GranularTooltips`

```tsx
function GranularTooltips({ points }) {
  const gRef = useRef<SVGGElement>(null)
  useLayoutEffect(() => {
    const g = gRef.current
    if (!g) return
    const svg = g.closest('svg')
    if (svg && svg.lastElementChild !== g) svg.appendChild(g)
  })
  const xDomain = useXAxisDomain(0)   // public Recharts 3.x hook
  const yDomain = useYAxisDomain(0)   // public Recharts 3.x hook
  const plotArea = usePlotArea()      // public Recharts 3.x hook
  const chartHeight = useChartHeight() // public Recharts 3.x hook
  // manual linear scales mirroring XAxis/YAxis
  // model → right of point, benchmark → left, fallback on overflow
  // vertical clamp to [plotTop, svgHeight - 8]
  // <foreignObject> per point, whiteSpace: nowrap, overflow="visible"
  // <CustomTooltip active={true} payload={[{payload: point}]} />
}
```

Hover tooltip (`<Tooltip content={<CustomTooltip />} />`) suppressed in granular
state to avoid double-display.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| `useLayoutEffect` for SVG reorder | Fires before paint; no user-visible flicker. `useEffect` would be too late. |
| Public hooks only (`useXAxisDomain`, `usePlotArea`, etc.) | `useXAxis`/`useYAxis` are internal-only in Recharts 3.x, not exported from index |
| Manual linear scale construction | Scale is linear with known domain+range; matches Recharts exactly without private API access |
| `whiteSpace: 'nowrap'` on wrapper div | `white-space` is inherited CSS — cascades to all CustomTooltip text without modifying shared component |
| model → right, benchmark → left | Opposite sides guarantees no overlap; both points share same model code so same X range |
| Hover tooltip suppressed in granular state | Both pinned and hover would show simultaneously; pinned already shows full info |
| BenchmarkHeatmap unaffected | Scoped to scatter chart only per Andrew |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/components/ReturnVolatilityScatter.tsx` | Full granular feature + GranularTooltips | Yes — `312ca3d` (DEV) |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** `DEV` (portal), `CLOUD` (workspace)

`ReturnVolatilityScatter.tsx` is complete through `312ca3d`. Portal DEV pushed to
`origin/DEV`. CLOUD submodule pointer updated and pushed. Feature is live on remote.

---

## Next Steps

None — feature complete and pushed.

**Do NOT:**
- Touch `BenchmarkHeatmap.tsx` — heatmap granular filtering is explicitly out of scope.
- Modify `ModelPortfolios.tsx` — feature is self-contained in `ReturnVolatilityScatter.tsx`.

#### coo_briefing_all_gates_cleared.md

# COO Briefing: All CTO Stall Items Resolved — Phase 3 Unblocked

**Date:** 2026-03-05
**From:** 0.4.0_DE_ClientPlatform
**To:** 2.0.0_SA_COO

---

## Status: All 5 CTO-Flagged Items Resolved

| # | Item | Status | Who | Evidence |
|---|------|--------|-----|----------|
| 1 | DS Phase 2 batch | DEPLOYED | DS committed, DT deployed | Lambda `bd-v2.16.2`, EC2 `bd-v2.16.3` — both tagged and pushed |
| 2 | DT J2/J3 | COMPLETE | DT | Commit `67a400b3`, deployment_map updated, task order marked complete |
| 3 | DE ADVI-006 design brief | COMPLETE | DE | Commit `aaf97585`, brief at `docs/architecture/advisor_intelligence/books_tab_design_brief.md`, task order marked complete |
| 4 | Portal DEV push | PUSHED | DT | `2291669..4b768c3` — 15 commits (RD Phase 1 + Y4 fixes + Y8 AUA stacked bar) |
| 5 | Phase 3 FE task orders | AWAITING COO | -- | All gates cleared |

---

## What's Unblocked

**Phase 3 FE task orders can be issued now.** Both prerequisite gates are satisfied:

1. **DS delivery gate** — DS Phase 2 batch (11 streams: Y2/Y3/Y5/Y6b/Y6c/Y6d/Y7/Y9/Y10/Y11/Y13) is committed, deployed, and live. New data keys available: `growth_decomposition`, `nna_geo`, `nna_adv`, `nna_geo_drill`, `aua_mix`, Y6b city drill, Y6d relationship drill, Y13 monthly stacked bar.

2. **Books design brief gate** — ADVI-006 brief complete with L2/L3/L4 field mappings, 6 backend gaps documented with exact function targets, TypeScript interfaces drafted. Ready for RD task order decomposition.

**Books tab (Y14/Y15/Y16)** — additionally unblocked by DT J2/J3 completion (auth-handler + authorizer deployed).

---

## Action Required

COO to issue Phase 3 FE task orders. DE is reactive until received.

#### coo_handoff_pod4_state_validation.md

# COO Handoff: Pod 4 State Validation — 2026-03-05

**From:** 0.4.0_DE_ClientPlatform
**To:** 2.0.0_SA_COO
**Date:** 2026-03-05
**Scope:** Full pod 4 agent state audit — DE, DT, DS, RD_AdvisorIntelligence, RD_ModelPortfolios

---

## Summary

ADVI_YANGV2 Phases 1–4 are fully implemented and approved. Portal DEV has 5 unpushed
commits awaiting DT push. DS has two additional research outputs (NNA canonical fix +
orphan theory disproof) that are committed but **awaiting CEO decision** before a gold
layer rebuild can be triggered. RD_ModelPortfolios has no active work. No open DE task
orders remain.

---

## Agent-by-Agent State

### 0.4.0_DE_ClientPlatform — IDLE / COMPLETE

**Last active:** 2026-03-05
**Open task orders:** 0 (all complete)

| Task Order | Status |
|---|---|
| `ADVI_V1VERS.004.portal-types-wiring.md` | complete |
| `ADVI_V1VERS.006.books-design-brief.md` | complete |
| `ADVI_YANGV2.Y-phase3.de-type-wiring.md` | complete |
| `macro_project_code_retroactive_cleanup.md` | complete |

**What was done this session:**
- Reviewed and approved all 4 Phase 3 RD commits (`7460f35` → `9b902dc`): Y3-FE, Y5-FE,
  Y6b/Y6d/Y9, Y13, Y15. tsc clean confirmed.
- Executed retroactive macro/project code cleanup across pod 4 (27 renames, 14 XML
  metadata updates, CLOUD commit `ad206388`).

**Status:** Reactive. Awaiting new task orders from COO.

---

### 0.4.0_DT_ClientPlatform — IDLE / PENDING PUSH

**Last active:** 2026-03-04 (bd-v2.16.2 / bd-v2.16.3 deploy + J2/J3 + portal submodule push)
**Open task orders:** 0 (J2/J3 complete; deployment_audit superseded)

**Latest deployment tags:**

| Tag | What | Status |
|---|---|---|
| `bd-v2.15.0` | bd-portal-publisher (adv_drill + cla) | DEPLOYED |
| `bd-v2.15.1` | bd-gold-layer-runner (script 10) | DEPLOYED |
| `bd-v2.16.1` | HOTFIX account_performance date fallback | DEPLOYED |
| `bd-v2.16.2` | bd-portal-publisher Yang V2 Phase 2 (Y3/Y5/Y9) | DEPLOYED |
| `bd-v2.16.3` | bd-gold-layer-runner Yang V2 Phase 2 (Y6b/Y6c/Y6d/Y7/Y13) | DEPLOYED |

**PENDING — Portal DEV push:** DT last pushed portal DEV at `4b768c3`. Five new
approved commits are sitting locally:

| Commit | Author | Description |
|---|---|---|
| `542197c` | DE | Y3/Y5/Y6b/Y6c/Y6d/Y9/Y13/Y15 type wiring |
| `7460f35` | RD | Y3-FE AUA mix sub-toggle + Y5-FE GRO mode |
| `0bd3f66` | RD | Y6b/Y6d snapshot drill + Y9 continuous NNA bar |
| `54163de` | RD | Y13 rolling flows diverging bar |
| `9b902dc` | RD | Y15 Books tab L2/L3/L4 MVP |

**Action required from COO:** Issue DT a push order for portal DEV through `9b902dc`.

---

### 0.4.0_DS_ClientPlatform — IDLE / CEO DECISION PENDING

**Last active:** 2026-03-05
**Open task orders:** 0 (all V1VERS and YANGV2 task orders complete)

**What is deployed (CLOUD, part of bd-v2.16.2/v2.16.3):**
- Y2: NMNC/NMEC classification confirmed correct — no patch needed
- Y3: Asset class AUA mix (holdings_lots join) — Lambda deployed
- Y5: Growth decomposition time series — Lambda deployed
- Y6b: City-level NNA drill data — script 09 deployed
- Y6c: Outflows quartile inversion fix — script 09 deployed
- Y6d: Relationship-level ADV drill data — script 09 deployed
- Y7: Single-account AUA binning fix — script 09 deployed
- Y9: Diverging NNA bar data at all drill levels — Lambda deployed
- Y10: QTD/YTD math bug — investigated and fixed
- Y11: "Advisor" field investigation — no distinct Advisor field exists in BD gold layer (confirmed); Y11 resolved as "no Advisor toggle possible"
- Y13: Monthly stacked_bar granularity — script 10 deployed

**Two additional DS outputs NOT in a task order (research-driven):**

**1. NNA canonical classification fix (commits `9bfb289b`, `b4f2d7a7`):**
DS discovered that BD's NNA figures undercount Schwab's by ~40% due to phantom
flows from internal journal entries (`JNL - LONG` / `JNL - SHORT`) and Schwab-internal
cash sweeps (`TRF BTWN SCH ACCTS`, `TO SEP ACCT MGR`, `FDIC sweeps`). Fix is committed
to `05_build_client_performance.py` and `05b_build_account_performance.py`.

**Status: Awaiting CEO approval before gold layer rebuild.** The fix would require
re-running the full gold layer pipeline and redeploying. Net NNA impact is small
(-$1.5M over 4 months), but accuracy improvement is material (12,050 phantom events
removed). DS logged this as requiring CEO decision, not a routine DT deploy.

**2. ACAT orphan theory disproof (log: `smoke_test_orphan_theory.md`):**
DS investigated whether BD has missing ACAT transaction records that explain the
Schwab NNA gap. **Conclusion: Disproven.** BD transaction coverage is complete (0%
orphan rate). The NNA gap is entirely a cash flow classification boundary issue, not
a data completeness gap. No allocation-diff pipeline is warranted.

**Action required from COO/CEO:** Decide whether to approve the NNA canonical
classification rebuild (commits `9bfb289b` + `b4f2d7a7`). If approved, DT deploys
via `safe-ec2-deploy.sh` followed by a triggered pipeline run.

---

### 0.4.2_RD_AdvisorIntelligence — IDLE / COMPLETE

**Last active:** 2026-03-05 (portal DEV `9b902dc`)
**Open task orders:** 0 (all 8 YANGV2 task orders complete)

**Completed YANGV2 FE streams:**

| Commit | Streams | Status |
|---|---|---|
| `f9c0e59` | Y1, Y4 (partial), Y6, Y12 | complete |
| `76c7621` → `2981133` | Y4 final fix | complete |
| `4b768c3` | Y8 | complete — pushed to remote |
| `7460f35` | Y3-FE, Y5-FE | complete — awaiting DT push |
| `0bd3f66` | Y6b-FE, Y6d-FE, Y9-FE | complete — awaiting DT push |
| `54163de` | Y13-FE | complete — awaiting DT push |
| `9b902dc` | Y15 Books L2/L3/L4 | complete — awaiting DT push |

**What Y15 covers:** L2 advisor book summary (AUA/clients/NNA/growth KPIs, tax
exposure, engagement, clients table), L3 client detail (getBooksClientDetail endpoint,
taxable open lots with term filter), L4 inline account drill (open_lots filtered by
account_id). Admin/internal gate (`isInternal() || isDev()`) maintained.

**Unimplemented YANGV2 streams (no task orders issued):**
- Y2: NMNC/NMEC audit — resolved as no-op (DS confirmed classification is correct)
- Y11: Advisor toggle — resolved as no data (DS confirmed no Advisor field exists)
- Y14: Books access gating — blocked on J1→J2→J3 chain (J2/J3 now live; J1 AE work)
- Y17: AI RAG executive summary — deferred, flagged for separate PRD

---

### 0.4.1_RD_ModelPortfolios — NO ACTIVE WORK

**Last active:** Unknown (no log entries in any date folder)
**Open task orders:** `page_inventory.md`, `xtick_spacing_fix.md` (check statuses)
**Status:** Dormant. No YANGV2 work assigned to this agent. ModelPortfolios page
not part of the Yang V2 feedback scope.

---

## Open Items by Priority

### P0 — Blocked on DT push

**Portal DEV has 5 approved commits not yet on remote.** All Phase 3 FE work (Books tab,
Y13 rolling flows, Y6b/Y6d drills, Y3-FE AUA mix, Y5-FE GRO mode) is sitting in local
portal DEV at `9b902dc`. None of this is visible to users until DT pushes and a portal
PROD build runs.

**Assign:** 0.4.0_DT_ClientPlatform push portal DEV → `9b902dc`.

---

### P1 — CEO Decision Required

**NNA canonical classification fix** is committed but not deployed. The fix removes
12,050 phantom events (internal journals + Schwab sweeps) from NNA computation. Net
dollar impact is small. Accuracy improvement is material. Requires CEO direction because
it changes the definition of a core metric (NNA) and the gold layer rebuild touches the
full pipeline.

**Assign:** Andrew/Yang to decide. If approved → DT deploys scripts 05/05b + triggers
pipeline run → gold layer updates.

---

### P2 — Y14 Books Access Gating (J1 dependency)

Books tab is live (Y15 implemented) but showing admin-only content. The access model
(advisors see only their own book) depends on the full J1→J2→J3 partner identity chain.
J2/J3 (auth-handler + authorizer passthrough) are deployed as of bd-v2.16.2. J1
(DynamoDB `opal-partner-49financial` table with `advisorKey` mapping) is an AE task
(0.7.0_AE_CloudOps).

**Status:** J1 is the only remaining gate. AE has the task order
(`ADVI_V1VERS.J1.partner-identity-dynamo.md`).

---

### P3 — Y17 AI RAG Executive Summary (Deferred)

Three-level AI-generated summaries (firm/advisor/client) defined in the Yang V2 PRD
Section 4.5. Marked as requiring a separate mini-PRD. High effort. No agents assigned.
DS (context design) + 0.7.0_AE_CloudOps (Lambda + Claude API infrastructure) are the
leads when this is activated.

**Assign:** COO to decide when to open Y17 track and issue mini-PRD.

---

## ADVI_YANGV2 Completion Scorecard

| Phase | Streams | Status |
|---|---|---|
| Phase 1 — Visual (no data dep) | Y1, Y4, Y6, Y8, Y12 | COMPLETE + deployed to portal remote |
| Phase 2 — DS data batch | Y2, Y3, Y5, Y6b, Y6c, Y6d, Y7, Y9, Y10, Y11, Y13 | COMPLETE — bd-v2.16.2 / bd-v2.16.3 live |
| Phase 3 — FE integration | Y3-FE, Y5-FE, Y6b-FE, Y6d-FE, Y9-FE, Y13-FE | COMPLETE — portal DEV `9b902dc`, DT push pending |
| Phase 4 — Books | Y15 L2/L3/L4 | COMPLETE — portal DEV `9b902dc`, DT push pending |
| Phase 5 — AI Summary | Y17 | NOT STARTED — deferred |

Resolved as no-ops: Y2 (classification correct), Y11 (no Advisor field in data)
Blocked on external: Y14 (J1 AE gate), Y17 (deferred)

---

## Recommended COO Actions

1. **Issue DT push order** for portal DEV `9b902dc` — highest priority, unblocks Y15 Books tab for users
2. **Escalate NNA canonical fix** to CEO (Andrew/Yang) for go/no-go on gold layer rebuild
3. **Check J1 AE status** — `ADVI_V1VERS.J1.partner-identity-dynamo.md` in 0.7.0_AE_CloudOps task_orders; if complete, Y14 access gating can be activated
4. **Decide Y17 timeline** — open AI RAG mini-PRD when Books tab is stable post-Y14

#### rd_phase3_review_all_complete.md

# RD Phase 3 Review — All 4 Task Orders Complete — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-05
**Portal DEV commits reviewed:** `7460f35` -> `0bd3f66` -> `54163de` -> `9b902dc`
**Workspace CLOUD commit:** pending (this log + task order status updates)

## Objective

Review all Phase 3 RD portal DEV commits (4 commits covering Y3-FE, Y5-FE, Y6b-FE, Y6d-FE, Y9-FE, Y13-FE, Y15) for correctness, type safety, task order compliance, and tsc cleanliness. Mark all task orders complete if approved.

---

## Work Completed

### 1. 7460f35 — Y3-FE AUA mix sub-toggle + Y5-FE GRO growth decomposition mode

**Files:** `PartnerAnalytics.tsx` — 3 files, -100/+170 lines.

**Y3-FE (AUA Mix):** New `auaSubMode` state (`'clients' | 'mix'`). Secondary toggle rendered inside AUA panel content area. `mix` view iterates `aua_mix` data from DS Phase 2 response key — segments mapped with appropriate color styling. No data fetching changes. Type-safe against `AuaMixView` added in `542197c`.

**Y5-FE (Growth Decomposition):** New `growthMode` state (`'standard' | 'decomposition'`). Decomposition path renders `GrowthDecompositionView` from DS response `growth_decomposition` key. Standard path unchanged.

**Compliance check:** No emojis. No API calls added. No shared type mutations. `tsc` clean.

**Verdict: APPROVED.**

---

### 2. 0bd3f66 — Y6b/Y6d snapshot NNA drill + Y9-FE continuous NNA diverging bar

**Files:** `DistributionTab.tsx` — 3 files, -60/+196 lines.

**Y6b-FE (GEO snapshot drill):** Click handler on state-level bars opens drill-down view. State selected stores `selectedGeoState`. Drill uses `nna_geo_drill` key on `CumulativeChartResponse` — matches `NNAGeoDrillView` type. Back button clears selection.

**Y6d-FE (Relationship drill):** Same pattern on ADV snapshot. `selectedDrillKey` state. Drill uses `drill` key on `NnaView` — matches `NNADistributionDrill` type.

**Y9-FE (Continuous NNA diverging bar):** `ComposedChart` with `stackOffset="sign"` — inflows above zero, outflows below. Uses `nna_series` and `nna_adv` keys from `CumulativeChartResponse`. Type-safe against `NNASeriesView`/`NNAGeoDrillView` from `542197c`.

**Compliance check:** No emojis. No shared type mutations. `tsc` clean.

**Verdict: APPROVED.**

---

### 3. 54163de — Y13-FE rolling flows per-period diverging bar with interval toggle

**Files:** `AdvisorsTab.tsx` — 2 files, -45/+111 lines.

Replaced per-advisor stacked bar (deprecated by Yang feedback removing advisor-level breakdown) with per-period aggregate diverging bar. `ComposedChart` with `stackOffset="sign"`. Interval toggle (Month/Quarter/Year) drives `aggregatedFlowsData` memo — sums `inflow`/`outflow` per period from `monthly` key on `AdvisorRollingFlowsResponseV2`. Type-safe against `monthly?` added in `542197c`. No advisor-row loop in chart anymore — aggregate only. Correct per task order requirement.

**Compliance check:** No emojis. No API calls changed. `tsc` clean.

**Verdict: APPROVED.**

---

### 4. 9b902dc — Y15 Books tab L2/L3/L4 MVP

**Files:** `ClientsTab.tsx` + supporting files — 4 files, -270/+380+ lines. Largest Phase 3 commit.

**L2 (Advisor Book Summary):** AUA/clients/accounts/NNA/growth KPI cards using `AdvisorBookResponse` (existing type, existing `getAdvisorBook()` endpoint). Tax Exposure panel. Engagement panel (flows TTM + avg tenure). Clients table with row click triggering L3.

**L3 (Client Detail):** Activated by `selectedClientKey`. Calls `getBooksClientDetail(clientKey)` — the new endpoint wired in `542197c`. Uses `BooksClientDetailResponse`. Taxable Open Lots panel with term filter (ST/LT/All). Account table.

**L4 (Inline Account Drill):** `selectedAccountId` state. Drills `open_lots` array filtered by `account_id` and `term`. Renders inline below account table row, no modal/routing.

**Key compliance checks:**
- `income_fees` and `portfolio_composition` panels: all references are in removed lines (`-`), none in added code. Correctly hidden per task order and ADVI-006 brief.
- `isInternal() || isDev()` gate: maintained at component top level.
- "Taxable Open Lots" label used (not "Holdings").
- `getBooksClientDetail` (not legacy `getClientDetail`).
- No emojis. `tsc` clean.

**Verdict: APPROVED.**

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| All 4 task orders marked complete | All commits pass type safety, task order compliance, and tsc checks |
| No follow-up type changes required | RD consumed all types from `542197c` correctly; no gaps found |
| Y15 `BooksClientDetailResponse` naming validated | RD used the correct name (not legacy `ClientDetailResponse`) |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-Y3-Y5-FE-header-panel.md` | status: pending -> complete | Yes -- CLOUD (this commit) |
| `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-Y6b-Y6d-Y9-FE-drill-and-continuous-nna.md` | status: pending -> complete | Yes -- CLOUD (this commit) |
| `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-Y13-FE-rolling-flows-nna-bar.md` | status: pending -> complete | Yes -- CLOUD (this commit) |
| `org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI-Y15-books-tab-l2-l3-l4.md` | status: pending -> complete | Yes -- CLOUD (this commit) |
| `org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-03-05/rd_phase3_review_all_complete.md` | This log | Yes -- CLOUD (this commit) |

---

## Current State

**Status:** COMPLETE
**Active branch:** `CLOUD` (workspace), `DEV` (portal)

All Phase 3 DE responsibilities complete. RD delivered all 4 Phase 3 task orders (Y3/Y5, Y6b/Y6d/Y9, Y13, Y15) — 4 portal DEV commits (`7460f35` -> `0bd3f66` -> `54163de` -> `9b902dc`) reviewed, approved, and task orders marked complete. tsc clean confirmed. Portal DEV now has 20 approved commits total (20 commits ahead of last DT push at `4b768c3`, now advanced to `9b902dc`). No open DE task orders remain.

---

## Next Steps

1. **[DT] Push portal DEV** — 4 new approved commits (`7460f35` -> `0bd3f66` -> `54163de` -> `9b902dc`), brings portal DEV to `9b902dc`
2. **[COO/CTO] Review Phase 3 completeness** — all Yang V2 FE streams (Y3/Y5/Y6b/Y6d/Y8/Y9/Y13/Y15) implemented and approved
3. **[DE] Await next task orders** — reactive until new work arrives

**Do NOT:**
- Touch `portal/` — all portal work belongs to DT push gate
- Mark any RD task orders without reading the commit diffs

#### rd_y4_y8_review_and_advi006_brief.md

# RD Y4/Y8 Commit Review + ADVI-006 Books Design Brief — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-05
**Portal DEV commits reviewed:** `f9c0e59` -> `76c7621` -> `7258c5e` -> `2981133` -> `4b768c3`
**Workspace CLOUD commit:** pending (this log + brief commit)

## Objective

Catch-up review of 5 new RD portal DEV commits (4 Y4 fixes + 1 Y8 feature) not covered by prior session logs. Then execute ADVI-006 task order: write Books tab design brief.

---

## Reviews Completed

### f9c0e59 — Y1+Y4+Y6+Y12 phase 1 visual fixes

3 files, -332/+39 lines. Scope:
- **PartnerAnalytics.tsx**: Y1 reversed `barCategories` (NMEC bottom, NMNC top). Y4 added `stackOffset="sign"` to NNA ComposedChart.
- **AdvisorsTab.tsx**: Y12 removal of 1Y Rolling view per Yang feedback. Deleted `RollingFlowsChart`, `Rolling1YChart`, unused state (`flowsMetric`, `flowsWindow`, `flowsView`), unused types/constants. Rolling Flows panel simplified to stacked bar only. Clean dead code removal — no chart logic altered.
- **DistributionTab.tsx**: Y6 NNA distribution filter — exclude histogram bins within [-1000, 1000] range. Added explanatory footnote for the exclusion.

No emojis. No data fetching changes. **Verdict: APPROVED.**

### 76c7621 — Y4 fix: net line at actual NNA value, not midpoint

1 file, -4/+2 lines. Removed incorrect midpoint computation for NNA net line; now uses `net` directly (= actual NNA = inflows + outflows). **Verdict: APPROVED.**

### 7258c5e — Y4 fix: remove stackId from NNA bars

1 file, -2/+2 lines. Intermediate iteration — removed `stackId="nna"` to test independent bar rendering. Superseded by next commit. **Verdict: APPROVED (iteration).**

### 2981133 — Y4 fix: align NNA bars on same x-position

1 file, -2/+3 lines. Re-added `stackId="nna"` on both inflow/outflow bars, extracted variables for clarity. Final correct state: stacked bars with `stackOffset="sign"` makes inflows above 0, outflows below 0, both on same x-position. **Verdict: APPROVED.**

### 4b768c3 — Y8 continuous AUA area-to-stacked-bar + interval toggle

1 file (DistributionTab.tsx), -115/+141 lines. Major visual change:
- Replaced `AreaChart`/`Area` with `BarChart`/`Bar` for continuous AUA view.
- New `auaInterval` state: Month/Quarter/Year toggle. `aggregatedBarData` memo takes last data point per period (end-of-period snapshot — correct for cumulative AUA).
- NMNC renders on top (Y1 consistency via `[...displayCategories].reverse()`).
- Tooltip uses `periodLabel` instead of raw date. `stackId="aua"`. Top bar gets `radius={[4, 4, 0, 0]}`.
- No new API calls, no type changes, no emojis.

**Verdict: APPROVED.**

---

## DT Signal

All 5 portal DEV commits approved. Combined with prior session approval (10 commits), DT is cleared to push full portal DEV history.

---

## ADVI-006 Design Brief

Executed task order `ADVI-006-books_design_brief.md`. Synthesized thread turns 6 (DE scope), 7 (DS data confirmation), 8 (RD layout spec) into `docs/architecture/advisor_intelligence/books_tab_design_brief.md`.

---

## Phase 3 Type Wiring (ADVI-Y-phase3-de-type-wiring)

Executed COO task order. Added all TypeScript types for DS Phase 2 deployed data + ADVI-006 Books types. This unblocks all Phase 3 RD task orders.

Portal DEV commit `542197c`:

**Extended existing types:**
- `DistributionStats`: +`inflow_percentiles`, `outflow_percentiles`, `inflow_count`, `outflow_count` (Y6c)
- `NnaView`: +`drill?: NNADistributionDrill` (Y6b/Y6d)
- `CumulativeChartResponse`: +`growth_decomposition?`, `nna_geo?`, `nna_adv?`, `nna_geo_drill?`, `aua_mix?` (Y5/Y9/Y3)
- `AdvisorRollingFlowsResponseV2`: +`monthly?` (Y13)

**New types added:**
- Y6b/Y6d: `NNADistributionDrillEntry`, `NNADistributionDrill`
- Y5: `GrowthDecompositionPoint`, `GrowthDecompositionView`
- Y9: `NNASeriesPoint`, `NNASeriesView`, `NNAGeoDrillView`
- Y3: `AuaMixSegment`, `AuaMixPoint`, `AuaMixView`
- Y15: `BooksClientDetailResponse`, `BooksClientAccount`, `BooksClientTaxDetail`, `CostBasisYear`, `GainPosition`, `OpenLot`

**New endpoint:** `getBooksClientDetail(clientKey)` in `advisor-intelligence.ts`

**Note on Y15 naming:** Design brief specified `ClientDetailResponse` but that name was already taken by the legacy `clients_tab.json` type (line 777). Named `BooksClientDetailResponse` to avoid collision per task order constraint "do not modify existing types." Existing `AdvisorBookResponse` (line 901) already covers L2 — no new L2 type needed. Existing `getAdvisorBook()` endpoint already wired.

tsc clean (no errors).

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-03-05/rd_y4_y8_review_and_advi006_brief.md` | This log | Yes -- CLOUD `aaf97585` (initial), updated this commit |
| `docs/architecture/advisor_intelligence/books_tab_design_brief.md` | ADVI-006 deliverable | Yes -- CLOUD `aaf97585` |
| `org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI-006-books_design_brief.md` | Status: pending -> complete | Yes -- CLOUD `aaf97585` |
| `portal/src/pages/AdvisorIntelligence/types.ts` | +184 lines: Y3/Y5/Y6b/Y6c/Y6d/Y9/Y13/Y15 types | Yes -- portal DEV `542197c` |
| `portal/src/api/endpoints/advisor-intelligence.ts` | +BooksClientDetailResponse import, +getBooksClientDetail() | Yes -- portal DEV `542197c` |
| `org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI-Y-phase3-de-type-wiring.md` | Status: pending -> complete | Yes -- CLOUD (this commit) |

---

## Current State

**Status:** COMPLETE
**Active branch:** `CLOUD` (workspace), `DEV` (portal)

All DE responsibilities cleared:
- 16 portal DEV commits approved (10 prior + 5 RD review + 1 type wiring `542197c`)
- ADVI-006 design brief written and committed
- Phase 3 type wiring complete — RD is unblocked
- Both task orders marked complete

---

## Next Steps

1. **[DT] Push portal DEV** -- 16 commits approved (must include `542197c`)
2. **[COO] Issue Phase 3 RD task orders** -- all gates cleared (DS delivered, types wired, brief done)
3. **[DE] Await Phase 3 RD output** -- reactive until RD commits land

#### task_order_completeness_audit.md

# Task Order Completeness Audit: ADVI_V1VERS + ADVI_YANGV2 — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-05
**Method:** Full sweep of all task orders in both project namespaces + all ad-hoc task orders
across pod 4. Blocker Verification Protocol (AGENT_START_HERE.md) applied to every
non-complete item before any BLOCKED or AMBIGUOUS designation.

---

## 1. Complete Task Order Status Table

### ADVI_V1VERS

| Task Order | Agent | Status | Verification |
|---|---|---|---|
| `ADVI_V1VERS.004.portal-types-wiring.md` | DE | **complete** | Portal DEV `7df26bb` |
| `ADVI_V1VERS.006.books-design-brief.md` | DE | **complete** | CLOUD `aaf97585`, brief at `docs/architecture/advisor_intelligence/books_tab_design_brief.md` |
| `ADVI_V1VERS.004.adv-drill-cla.md` | DS | **complete** | CLOUD `cc3ad9fa` (adv_drill + cla in bd-portal-publisher) |
| `ADVI_V1VERS.005.rolling-flows-data.md` | DS | **complete** | CLOUD `6a3ff256` (stacked_bar + monthly in script 10) |
| `ADVI_V1VERS.J1.partner-identity-dynamo.md` | AE | **complete** | VERIFIED — see section 3 |
| `ADVI_V1VERS.J2-J3.auth-handler-authorizer.md` | DT | **complete** | VERIFIED — see section 3 |
| `ADVI_V1VERS.004.distribution-continuous.md` | RD | **complete** | Portal DEV (C2/C4 in DistributionTab) |
| `ADVI_V1VERS.005.advisors-tab.md` | RD | **complete** | Portal DEV (stacked bar + rolling 1Y rendered) |

**V1VERS: 8 of 8 task orders complete.**

---

### ADVI_YANGV2

| Task Order | Agent | Status | Verification |
|---|---|---|---|
| `ADVI_YANGV2.Y-phase2.ds-data-batch.md` | DS | **complete** | CLOUD `0c9bb501`/`cc3ad9fa`/`6a3ff256`, deployed bd-v2.16.2/v2.16.3 |
| `ADVI_YANGV2.Y-phase3.de-type-wiring.md` | DE | **complete** | Portal DEV `542197c` |
| `ADVI_YANGV2.Y1-Y4-Y6-Y12.phase1-visual.md` | RD | **complete** | Portal DEV `f9c0e59`→`2981133` |
| `ADVI_YANGV2.Y8.continuous-aua-stacked-bar.md` | RD | **complete** | Portal DEV `4b768c3` (pushed to remote) |
| `ADVI_YANGV2.Y3-Y5.fe-header-panel.md` | RD | **complete** | Portal DEV `7460f35` |
| `ADVI_YANGV2.Y6b-Y6d-Y9.fe-drill-and-continuous-nna.md` | RD | **complete** | Portal DEV `0bd3f66` |
| `ADVI_YANGV2.Y13.fe-rolling-flows-nna-bar.md` | RD | **complete** | Portal DEV `54163de` |
| `ADVI_YANGV2.Y15.books-tab-l2-l3-l4.md` | RD | **complete** | Portal DEV `9b902dc` |
| `ADVI_YANGV2.portal-push.phase3.md` | DT | **PENDING** | Not started — see section 2 |

**YANGV2: 8 of 9 task orders complete. 1 pending (DT portal push).**

---

### Ad-hoc task orders (pre-namespace, still active scope)

| Task Order | Agent | Status | Notes |
|---|---|---|---|
| `advi_c1_geo_continuous.md` | RD | **complete** | DistributionTab C1 (continuous GEO NNA) done |
| `advi_c3_cla_snapshot.md` + addendum | RD | **complete** | CLA snapshot view done |
| `advi_h_portal_primitives.md` | RD | **complete** | Portal primitives refactor done |
| `advi_i_top_performers.md` | RD | **complete** | Top performers visual done |
| `continuous_view_max_window_clients_fix.md` | RD | **complete** | Done |
| `distribution_nomenclature_fix.md` | RD | **complete** | Done |
| `xtick_spacing_fix.md` + addendum | RD | **complete** | Done |
| `advi_a4_bell_curve_verify.md` | DS | **complete** | Snapshot NNA bell curve verified — no patch needed |
| `advi_a5_users_v2_mapping.md` | DS | **complete** | Scenario C — no advisorKey mapping exists in opal-users-v2 |
| `acat-inkind-nna-testing.md` | DS | **PENDING** | Not blocked — see section 2 |
| `HOTFIX-drilldown-account-perf-fallback.md` | DT | **complete** | bd-v2.16.1 deployed |
| `deployment_audit.md` | DT | **superseded** | Superseded by deployment_map.xml |

---

## 2. Open Items — Detailed Status

### OPEN #1 — DT: ADVI_YANGV2.portal-push.phase3.md

**Status: PENDING (not blocked)**

**What:** Push portal DEV to remote origin/DEV through `9b902dc` (5 commits:
`542197c` → `7460f35` → `0bd3f66` → `54163de` → `9b902dc`). Update parent repo
submodule pointer on CLOUD.

**Blocker Verification (Protocol Step 1–3):**
- Step 1: Checked DT's task order — no dependency agents listed. Task order states
  "No code changes — push only."
- Step 2: No dependency to check — this is a standalone push with all prereqs already
  satisfied (DE-reviewed at `f9161bed`, commits DE-approved).
- Step 3: **Not blocked.** DT can execute immediately.

**Who acts:** 0.4.0_DT_ClientPlatform
**What they do:** `cd portal && git push origin DEV`, then update CLOUD submodule pointer.
**Impact of not doing:** Y3-FE, Y5-FE, Y6b-FE, Y6d-FE, Y9-FE, Y13-FE, Y15 all
unreachable on remote. The Books tab, GRO mode, NNA drills, and rolling flows bar are
invisible to the server deployment pipeline until this push happens.

---

### OPEN #2 — DS: acat-inkind-nna-testing.md (Steps 2–5 pending)

**Status: IN PROGRESS (not blocked on Steps 1–2; BLOCKED on Steps 3–5)**

**What:** CEO-directed investigation of ACAT in-kind NNA undercount ($106M inflow gap
vs Schwab TOA). 5-step task order.

**Step 1 (commit scripts):** COMPLETE — `90424dba` committed `diag_acat_inkind_scan_v1/v2/v3.py`.

**Step 2 (write DT brief):** NOT DONE. `docs/briefs/devops-brief-acat-inkind-nna-ec2-run.md`
does not exist. DS's 2026-03-05 session logs (`canonical_nna_logic.md`,
`smoke_test_orphan_theory.md`) make no mention of this brief. This is DS's next action
and they can execute it now — no dependency.

**Steps 3–5 (DT run → DS analysis → DS production design brief):**
**Blocker Verification for Steps 3–5:**
- Step 1 (protocol): Checked DT task orders — no ACAT EC2 run task order issued to DT yet. The brief (Step 2) is the prerequisite.
- Step 2 (protocol): DS has not written the brief that would trigger DT's action.
- Step 3 (protocol): **BLOCKED on DS completing Step 2** (DT brief not written → DT cannot act → DS cannot read output → DS cannot write analysis or design brief).
  Evidence: `docs/briefs/devops-brief-acat-inkind-nna-ec2-run.md` does not exist. DT task orders contain no ACAT item.

**Who acts next:** 0.4.0_DS_ClientPlatform — write `docs/briefs/devops-brief-acat-inkind-nna-ec2-run.md`.
**Then:** 0.4.0_DT_ClientPlatform — upload v3 to S3, run on EC2, capture output.
**Then:** DS — read S3 output, write analysis + production design brief.

---

## 3. Blocker Verification: J1 + J2/J3 (Cited as Y14 Gate)

Both items are cited as gating Y14 (Books access gating). Applied full protocol.

### J1 — opal-partner-49financial DynamoDB table (AE)

**Blocker Verification:**
- Step 1: Read `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-03-04/advi_j1_partner_identity_dynamo_deploy.md`.
  Log documents full deploy sequence:
  - CLOUD commit `1b918471`: `feat(shared-infra): opal-partner-49financial DynamoDB table + IAM read policy`
  - `terraform apply`: 2 added, 0 destroyed, 0-diff confirmed
  - AWS CLI verification: table ACTIVE, hash_key=email, ByAdvisorRole GSI present
  - Table ARN: `arn:aws:dynamodb:us-east-1:313476888478:table/opal-partner-49financial`
  - Tag `shared-infra-v1.3.0` applied and pushed (confirmed: `git tag -l "shared-infra-*"` returns v1.3.0)
- Step 2: Log and git tag both corroborate delivery. Task order marked complete.
- Step 3: **Not blocked. J1 is verified complete.**

### J2/J3 — auth-handler + portal-authorizer (DT)

**Blocker Verification:**
- Step 1: Checked DT CLOUD commits.
  - `de023eed`: `feat(portal-authorizer): J3 -- pass advisorKey/advisorName/advisorRole to Lambda context (ADVI-J3)`
  - `ba0cbc19`: `0.4.0_DT_ClientPlatform: deployment_map.xml -- portal-auth J2/J3 (v1.1.0/v1.2.0)`
  - `67a400b3`: `0.4.0_DT_ClientPlatform: deployment_map.xml bd-v2.16.2/bd-v2.16.3 + J2/J3 complete`
  - DT task order `ADVI_V1VERS.J2-J3.auth-handler-authorizer.md` status: complete
- Step 2: Multiple CLOUD commits + task order corroborate delivery.
- Step 3: **Not blocked. J2/J3 verified complete.**

**Consequence for Y14:** J1 + J2 + J3 are all confirmed live. The auth chain that
gates Books advisor access is complete. Y14 is **unblocked**. No task order has been
issued for Y14 implementation.

---

## 4. Untouched PRD Streams (No Task Orders Issued)

The Yang V2 PRD (Section 5) defines 21 streams. The following were never given task orders:

| Stream | Why No Task Order | Current State |
|---|---|---|
| **Y2** — NMNC/NMEC period-bookend audit | DS investigated and found no patch needed | Resolved as no-op (data_contract.xml documents finding) |
| **Y11** — Advisor field investigation | DS investigated; no distinct Advisor field exists in BD gold | Resolved as no-op. Y13 Advisor toggle cannot be built. |
| **Y14** — Books access gating (portal) | Was gated on J1+J2+J3. Now unblocked. No task order issued. | **GAP — see section 5** |
| **Y17** — AI RAG executive summary | Deferred by CTO/COO; flagged for separate mini-PRD | Intentionally deferred |

Y2 and Y11 are legitimately closed without task orders (investigation-only, resolved
as no-ops). Y17 is intentionally deferred. **Y14 is a gap** — the gate cleared,
but no task order was ever issued for the implementation.

---

## 5. Y14 Gap Analysis — Books Access Gating

**What Y14 requires (from Yang V2 PRD Section 4.1):**

The Books tab (`ClientsTab.tsx`) currently gates all content behind `isInternal() || isDev()`.
Y14 is the switch from this admin-only model to a role-based model where:
- Admin users (internal/dev) see all advisors via dropdown — unchanged
- Authenticated advisor users see **only their own book** — new behavior
- The JWT (now containing `advisorKey`, `advisorName`, `advisorRole` via J3) is the
  identity source

**What the auth chain delivers (verified above):**
- `advisorKey`, `advisorName`, `advisorRole` are injected into the Lambda context by
  the portal-authorizer (J3)
- The auth-handler reads `opal-partner-49financial` at login to resolve portal user
  email → advisor identity (J2)
- The table exists and is empty (J1) — **populated at advisor onboarding time by Andrew**

**What is still needed for Y14:**
1. **RD task order** — `ClientsTab.tsx` needs to read `advisorKey` from auth context
   and scope the Books content to that advisor when the user is not admin/internal
2. **Portal API/backend** — the `getAdvisorBook(advisorKey)` call must be scoped to
   the logged-in advisor's key (currently the advisory key is likely hardcoded or passed
   via admin selector)
3. **Population gate** — Y14 cannot be used by real advisors until `opal-partner-49financial`
   has their email → advisorKey entries (Andrew's manual action)

**Note:** Y14 is frontend-only (RD + DE), no new Lambda or data work needed. The
backend auth chain is complete. The portal just needs to read the advisor identity from
the JWT claims and conditionally scope the Books view.

---

## 6. Committed-But-Undeployed Code

Two DS commits are on CLOUD but not deployed — separate from the task order system:

| Commits | What | Status |
|---|---|---|
| `9bfb289b` + `b4f2d7a7` | NNA canonical classification fix (scripts 05 + 05b — exclude JNL journals and Schwab sweeps) | **Awaiting CEO go/no-go before DT triggers gold layer rebuild** |

This is not tracked in any task order. The fix was research-driven (Schwab SOT
cross-reference session). CEO decision is the gate.

---

## 7. Action Summary for COO

| Priority | Action | Owner | Unblocks |
|---|---|---|---|
| P0 | Execute portal DEV push (`ADVI_YANGV2.portal-push.phase3.md`) | **DT** | Y15 Books tab, Y3-FE/Y5-FE/Y6b-FE/Y6d-FE/Y9-FE/Y13-FE reaching server deploy pipeline |
| P1 | Write DT brief for ACAT v3 EC2 run (`acat-inkind-nna-testing.md` Step 2) | **DS** | DT EC2 run → DS analysis → production design brief |
| P1 | Execute ACAT v3 EC2 run once DS brief is written | **DT** | DS analysis → CEO design review |
| P2 | Issue Y14 task order to RD | **COO** | Books tab advisor access gating (auth chain ready; table needs populating) |
| P2 | Populate `opal-partner-49financial` with advisor email mappings | **Andrew** | Y14 actually usable by real advisors |
| P3 | CEO go/no-go on NNA canonical fix (commits `9bfb289b`+`b4f2d7a7`) | **CEO/Andrew** | DT gold layer rebuild + improved NNA accuracy |
| P4 | Issue Y17 mini-PRD when Books tab is stable | **COO** | AI RAG executive summary |

---

## Status: COMPLETE
**Active branch:** CLOUD
**Workspace CLOUD commit:** pending (this log)


### 0.4.0_DE_ClientPlatform -- Recent Commits

# Recent commits by 0.4.0_DE_ClientPlatform

4da580a1 0.4.0_DE_ClientPlatform: ADVI_49FNV3 -- F3/F5/N1-N2 investigation complete, task orders closed
de994aec 0.4.0_DE_ClientPlatform: ModelPortfolios/Benchmark -- granular scatter selection + persistent tooltips (session log + submodule)
dd667949 0.4.0_DE_ClientPlatform: update portal submodule -- Y6b/Y6d drill fix (3702264)
7855dea3 0.4.0_DE_ClientPlatform: update portal submodule -- multi-granularity header_metrics (b0a33d7)
0ee72ab2 0.4.0_DE_ClientPlatform: update portal submodule -- Y6/Y6c NNA distribution fixes (b8cbf7a)
c1c50e3a 0.4.0_DE_ClientPlatform: task order completeness audit -- V1VERS + YANGV2 full sweep
518159a7 0.4.0_DE_ClientPlatform: COO handoff -- pod 4 state validation 2026-03-05
ad206388 0.4.0_DE_ClientPlatform: retroactive macro/project code cleanup -- pod 4 scope
3bbc980a org(1.0.0_SA_CTO): retroactive cleanup task orders + session log
f9161bed 0.4.0_DE_ClientPlatform: Phase 3 RD review complete + all 4 task orders marked complete
87cfe32c 0.4.0_DE_ClientPlatform: Phase 3 type wiring complete + COO briefing + session log update
d9686db0 org(2.0.0_SA_COO): ADVI-006 run + trade engine polish task orders
3252e5ce 0.4.0_DE_ClientPlatform: V2 types + RD task order refresh (gates cleared ADVI-004/005)
6048ce3c 0.4.0_DE_ClientPlatform: session log + ADVI-004 types task order complete
816f6fa2 0.4.0_DE_ClientPlatform: session log + I2 task order complete (leaderboard sort)
ff7f1ba3 0.4.0_DE_ClientPlatform: pod_inventory.xml -- leaderboard sort resolved
4a8e3d47 log(0.4.0_DE_ClientPlatform): pod_inventory.xml upgrade session log
5efb15f4 0.4.0_DE_ClientPlatform: upgrade pod_inventory.xml AdvisorIntelligence to full-fidelity from 0.4.2 RD audit
076e1120 0.4.0_DT_ClientPlatform: enrich Pod 4 (ClientPlatform) agent prompts with source-grounded context
b331d3e6 feat(org): 0.4.0_DE_ClientPlatform — continuous view Max window clients fix task order

### 0.4.2_RD_AdvisorIntelligence -- Recent Session Logs

#### ADVI_49FNV3_F2_F4_F6_F7_N1N2.md

# ADVI_49FNV3 — F2, F4, F6, F7, N1-N2-RD Complete — 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-09
**Portal DEV commit:** `594c3f6`

## Objective

Execute all 5 pending ADVI_49FNV3 task orders: F2 (projected ghost bars), F4 (stacked bar top 10),
F6 (unassigned sorting), F7 (zebra striping), N1-N2-RD (firm dashboard + advisor book visual polish).

---

## Work Completed

### 1. F6 + F7 — Pre-Applied (DT commit `1dc96b5`)

Both were already implemented by DT in portal DEV commit `1dc96b5`:
- **F6:** `PINNED_BOTTOM_NAMES = new Set([FIRM_ACCOUNT_NAME, 'Unassigned'])` at AdvisorsTab.tsx:80.
  Leaderboard separates pinned entries (lines 688-698), renders them in a dimmed "Unranked" section.
- **F7:** `bg-white/[0.025]` on odd leaderboard rows at line 771. Matches SecurityScanner pattern.

Marked both task orders as `complete`. No code changes needed.

### 2. F4 — Top Ten Advisors Stacked Bar (New Component)

Added `TopTenStackedBar` component to AdvisorsTab.tsx. Renders inside Panel 1 (Top Performers)
when `flowsData?.stacked_bar?.[period]?.[role]` data is available. Falls back to Top3Highlights
cards when stacked_bar data absent.

| Property | Value |
|----------|-------|
| Chart type | Recharts ComposedChart with stackOffset="sign" |
| Data source | `flowsData.stacked_bar[period][role]` (AdvisorBarEntry[]) |
| Sort | nna_net descending, tie-break: advisor_name ascending, top 10 |
| Inflows bar | stackId="flows", fill #2563EB, opacity 0.8 |
| Outflows bar | stackId="flows", fill #DC2626, dataKey outflowsNeg (negated client-side) |
| NNA dash | RechartsLine with custom dot — gold (#F59E0B) horizontal dash at y=nna_net |
| X-axis | advisor_name truncated at 12 chars, -45 degree angle |
| Tooltip | advisor_name, inflows, outflows, NNA (signed + colored) |

### 3. N1-N2-RD — Visual Polish

DT commit `1dc96b5` implemented functional N1 (firm dashboard) and N2 (advisor book) panels.
RD polish applied:

| Change | File | Line |
|--------|------|------|
| Back button: "All Advisors" -> "Back to Firm Overview" | ClientsTab.tsx | L2 back button |
| Zebra striping on AdvisorSummaryTable rows | ClientsTab.tsx | `bg-white/[0.025]` on odd rows |
| Zebra striping on L2 ClientsTable rows | ClientsTab.tsx | same pattern |

### 4. F2 — Projected Ghost Bars (PartnerAnalytics.tsx)

Added projection computation for the current incomplete period across all three panel views.

**Helper functions added:**
- `computePeriodDays(granularity, periodKey)` — returns totalDays + elapsedDays for monthly/quarterly/annually
- `currentPeriodKey` memo — identifies today's period

**AUA view ghost bars:**
- `augmentedAuaData` memo adds `{cat}_ghost` fields (e.g., `NMNC_ghost`, `NMEC_ghost`)
- Formula: `projected = actual * (totalDays / elapsedDays)`, capped at `max(actual, prior * 1.5)`
- Ghost rendered as additional stacked Bars with fillOpacity 0.25
- Only non-zero for the current incomplete period

**NNA view ghost bars:**
- `augmentedNnaData` memo adds `inflow_ghost` and `outflow_ghost` fields
- Inflow ghost extends upward (blue, 25% opacity)
- Outflow ghost extends downward (red, 25% opacity)
- Net line does NOT get a ghost (per task order)

**GRO view dashed extensions:**
- `augmentedGroData` memo adds a projected data point after the last actual point
- Three additional Line components with `strokeDasharray="6 3"` for market_proj, nna_proj, total_proj
- Dashed segments connect last actual to projected value using `connectNulls={false}`

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| F6/F7: mark complete without changes | DT already implemented in `1dc96b5`; code verified correct |
| F4: ComposedChart (not BarChart) | Needed for NNA dash overlay (Line component) alongside stacked bars |
| F4: NNA dash via Line + custom dot | Cleanest Recharts pattern for per-bar markers without Scatter complexity |
| F2: Cap formula `max(actual, prior * 1.5)` | Prevents ghost from being negative if actual already exceeds 1.5x prior |
| F2: `any` type for augmented AUA data | Dynamic ghost key generation (`${cat}_ghost`) not expressible in static type; `any` cast avoids TS errors on downstream consumers |
| N1-N2: "Back to Firm Overview" | Task order explicitly requested this text over the DT's "All Advisors" |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` | F4: TopTenStackedBar component + Panel 1 conditional rendering | Yes -- portal DEV `594c3f6` |
| `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx` | N1-N2: back button text + zebra striping | Yes -- portal DEV `594c3f6` |
| `portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx` | F2: projection helpers + augmented data memos + ghost bars + GRO dashed lines | Yes -- portal DEV `594c3f6` |
| Task orders (5 files) | All marked complete | Local only |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`

All 5 ADVI_49FNV3 task orders are complete. Portal DEV commit `594c3f6` contains F4 stacked bar,
F2 projected ghost bars (AUA + NNA + GRO), and N1-N2 visual polish. `bunx tsc -b` clean.
F6 and F7 were pre-applied by DT. DE review needed before DT pushes.

---

## Next Steps

1. **[0.4.0_DE_ClientPlatform] Review commit `594c3f6`** -- F2 projection logic, F4 stacked bar visual, N1-N2 polish.
2. **[0.4.0_DT_ClientPlatform] Push portal DEV after DE review** -- QA gate.
3. **[0.4.2_RD_AdvisorIntelligence] No further ADVI_49FNV3 task orders pending** -- await next assignment.

**Do NOT:**
- Push portal DEV -- DT is the push gate after DE reviews
- Implement L3/L4 visual panels for N1-N2 -- Phase 2a only per task order constraint

#### ADVI-005_4C_stacked_bar_rolling_1y.md

# ADVI-005 4C — Stacked Bar Primary + Rolling 1Y Secondary — 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-04
**Portal DEV commit:** `0bceb64`

## Objective

Implement Advisors tab rolling flows redesign (Stream 4C):
- Primary view: stacked bar chart (inflows up / outflows down) per advisor per period
- Secondary view: rolling 1Y line chart sliced by period toggle
- Legacy fallback preserved when stacked_bar or rolling_1y keys absent

Gate status was CLEARED (bd-v2.15.1). Types added by DE at portal DEV `5125eb9`.

---

## Work Completed

### Imports

- Recharts: added `BarChart as RechartsBarChart`, `Bar`, `ReferenceLine`
- Types: replaced `AdvisorRollingFlowsResponse` with `AdvisorRollingFlowsResponseV2`;
  added `AdvisorBarEntry`, `AdvisorRolling1YSeries`, `StackedBarPeriodKey`

### New types + constants

- `type FlowsViewMode = 'primary' | 'secondary'`
- `STACKED_BAR_PERIOD_OPTIONS` — qtd/ytd/1y/3y/max with labels QTD/YTD/1Y/3Y/Max
- `FLOWS_VIEW_OPTIONS` — Stacked / 1Y Rolling

### New state

- `flowsView: FlowsViewMode` — defaults to `'primary'`
- `stackedBarPeriod: StackedBarPeriodKey` — defaults to `'ytd'`
- `flowsData` type upgraded from `AdvisorRollingFlowsResponse | null` to `AdvisorRollingFlowsResponseV2 | null`

### Rolling Flows panel

Header now shows view toggle (Stacked / 1Y Rolling) + period toggle (QTD/YTD/1Y/3Y/Max).
Content conditionally renders:
- `StackedBarChart` when `flowsView === 'primary' && flowsData?.stacked_bar`
- `Rolling1YChart` when `flowsView === 'secondary' && flowsData?.rolling_1y`
- Legacy `RollingFlowsChart` as fallback when new keys absent

### StackedBarChart (new component)

| Property | Value |
|----------|-------|
| Chart type | Recharts BarChart |
| Data source | `data.stacked_bar[period][role]` (AdvisorBarEntry[]) |
| Sort order | nna_net ascending (lowest leftmost, highest rightmost) |
| Inflows bar | `stackId="flows"`, fill: hsl(var(--success)), opacity 0.75 |
| Outflows bar | `stackId="flows"`, fill: hsl(var(--destructive)), opacity 0.75, dataKey="outflowsNeg" |
| Outflows encoding | Positive in JSON; negated client-side: `outflowsNeg = -e.outflows` |
| Reference line | y=0 at rgba(255,255,255,0.2) |
| X-axis | advisor_name, angle -45, 12-char truncation |
| Tooltip | Custom content showing advisor_name + inflows/outflows/nna_net |

Waterfall style: inflows segment 0→inflows, outflows segment inflows→(inflows + outflowsNeg).
Net position of bar = nna_net.

### Rolling1YChart (new component)

| Property | Value |
|----------|-------|
| Chart type | Recharts LineChart (same pattern as legacy RollingFlowsChart) |
| Data source | `data.rolling_1y[role]` (AdvisorRolling1YSeries[]) |
| Period slicing | `period` toggle controls x-axis cutoff date (rolling window stays 1Y) |
| Selection | Same `selectedAdvisorIds` set as leaderboard row clicks |
| Metric plotted | nna (per contract: NNA-only primary; inflows/outflows in series for future) |
| Tooltip | advisor_name + formatted NNA per date |

Period → startDate mapping:
- qtd: start of current calendar quarter
- ytd: Jan 1 of current year
- 1y: 365 days ago
- 3y: 3 years ago
- max: no cutoff (full history)

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| stackId="flows" on both bars | Waterfall: inflows up from 0, outflows pull back from inflows top |
| flowsData typed as V2 (not V1) | Gate cleared; V2 extends V1 so backward compat holds |
| Legacy fallback path kept | Guard on stacked_bar/rolling_1y keys per 4C.5 requirement |
| Period toggle shared between primary and secondary | PRD: both views show period toggle; secondary uses it to slice x-axis |
| Default period: ytd | Most relevant business view; qtd too short, max too wide |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` | 4C stacked bar + rolling 1Y | Yes — portal DEV `0bceb64` |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`

Portal DEV is 7 commits ahead of origin: `3dc9dc5`, `7df26bb`, `5125eb9`, `ed832db`, `5f42dc6`, `bdcd00c`, `0bceb64`.
`bunx tsc -b` clean.

---

## Next Steps

1. **[DE] Review 4C visual design** before DT pushes portal DEV.
2. **[RD 0.4.2] Task 6 — advi_c3_cla_snapshot** — CLA snapshot view fix in DistributionTab.
3. **[RD 0.4.2] Task 7 — advi_c1_geo_continuous** — GEO continuous NNA view.
4. **[RD 0.4.2] Task 9 — ADVI-004 C2+C4** — ADV continuous + CLA continuous (gated).

#### AdvisorsTab_H_portal_primitives_I_top_performers.md

# AdvisorsTab H + I — Portal Primitives Refactor + Top Performers Redesign — 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-04
**Portal DEV commits:** `5f42dc6` (H) -> `bdcd00c` (I)

## Objective

Task H: Replace ad-hoc `SubPanel`/`SubPanelHeader` in AdvisorsTab with portal primitives.
Task I: Redesign Top Performers panel for rank prominence and achievement feel.
H before I per dependency order — H provides canonical structure that I builds on.

---

## Work Completed

### 1. Task H — Portal Primitives Refactor (`5f42dc6`)

Removed inline `SubPanel` (lines 97-103) and `SubPanelHeader` (lines 105-112) component
definitions. Both were locally defined shadows of the portal primitive system.

Replaced all three section usages:

| Section | Old | New |
|---------|-----|-----|
| Top Performers | `SubPanel` + `SubPanelHeader` | `Panel variant="chart" className="overflow-hidden"` + `PanelHeader` + `PanelContent noPadding` |
| Rolling Flows | `SubPanel` + `SubPanelHeader` | Same pattern |
| Leaderboard | `SubPanel` + `SubPanelHeader` | Same pattern |

`PanelContent noPadding` preserves inner padding from the existing `<div className="p-4">`
wrappers — no content layout change. `overflow-hidden` added to Panel to preserve corner
clipping behavior that `SubPanel` had.

Note: `Panel variant="chart"` uses `bg-[hsl(var(--semantic-background-contentPanel))]`
rather than the old `bg-white/5`. Minor visual difference (flat vs slightly elevated). This
is the canonical portal treatment — content layout, chart sizes, and section positions
are identical.

### 2. Task I — Top Performers Visual Redesign (`bdcd00c`)

| Element | Before | After |
|---------|--------|-------|
| Rank badge | Absolute-positioned `-top-2 -left-2` w-7 h-7 corner circle | Top of card w-10 h-10 center-aligned badge |
| Rank text | `text-sm font-bold` | `text-lg font-black` |
| Advisor name | `text-sm font-semibold ml-4` | `text-base font-bold` — top element under badge |
| NNA metric | `text-xl font-bold` | `text-2xl font-black` — hero metric |
| Trophy icon | In PanelHeader only | PanelHeader + rank-1 card accent (`size={16}`) |
| Card layout | Relative-positioned corner badge + margin offset | Flex column: badge row -> name -> NNA -> secondary |
| Card radius | `rounded-lg` | `rounded-xl` |

`rankStyles` updated to separate `badgeBg`, `badgeBorder`, `badgeText` for the new badge
component. No new Lucide imports — `Trophy` already present.

Data flow unchanged: `top3` slice of `data.windows[window].entries`, responds to all period
toggles (3M/6M/1Y/2Y/3Y) via the existing `window` prop.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| `overflow-hidden` on Panel | SubPanel had it; without it, rounded corners clip incorrectly on sticky table header |
| `PanelContent noPadding` for all three sections | Content manages its own padding; PanelContent's default `p-6` would break chart/table sizing |
| Trophy icon at card level for rank 1 only | Adds achievement signal without cluttering ranks 2 and 3 |
| `text-2xl font-black` for NNA | NNA is the primary achievement metric — needs to read immediately; font-black adds weight |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` | H: panel primitives refactor | Yes — portal DEV `5f42dc6` |
| `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` | I: Top Performers visual redesign | Yes — portal DEV `bdcd00c` |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`

Portal DEV is 6 commits ahead of origin: `3dc9dc5`, `7df26bb`, `5125eb9`, `ed832db`,
`5f42dc6`, `bdcd00c`. AdvisorsTab structure is now canonical. `bunx tsc -b` clean.

---

## Next Steps

1. **[RD 0.4.2] Start 4C (ADVI-005-advisors_tab)** — Stacked bar + rolling 1Y on AdvisorsTab.
   Use `AdvisorRollingFlowsResponseV2`. H is done so no structural collision risk.
2. **[RD 0.4.2] DistributionTab: C3 -> C1 -> C2+C4** — after 4C.
3. **[DE] Review all committed work** — before DT pushes DEV.

**Files to touch next:**
- `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` — 4C stacked bar + rolling 1Y

#### DistributionTab_C1_geo_continuous.md

# DistributionTab C1 — GEO Continuous Search and Drill — 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-04
**Portal DEV commit:** `4469ad7`

## Objective

Update the GEO continuous NNA view: limit chart to top-8 state series, add search input
covering all available states, keep existing click-to-drill into per-city data.

## Work Completed

### Top-8 display limit

Added `displayCategories` useMemo:
```tsx
const displayCategories = useMemo(() => {
  if (cohort === 'geo' && !isDrilled) return categories.slice(0, 8)
  return categories
}, [categories, cohort, isDrilled])
```
All chart rendering (gradients, Area components) and legend rendering switched from
`categories` to `displayCategories`. Metrics (`areaMetrics`, `startingTotal`) also use
`displayCategories` — consistent with what is shown in the chart.

For ADV cohort and for drilled city view: all categories rendered (no limit).

### Search input (GEO state level only)

Added `geoSearch: string` state. Search input renders in the left panel when
`cohort === 'geo' && !isDrilled` (before the legend).

- Input filters `categories` (full list, not just top-8) by display name
- Dropdown appears below input when `geoSearch` is non-empty
- Each result shows the state color dot, name, and right-arrow drill affordance
- Clicking a result: `setDrillParent(cat)` + clears search
- "No states found" empty state
- X button clears search

Search and geoSearch state both reset on cohort/metric change (via existing `useEffect`).

### Breadcrumb update

Replaced "Back to States" back button with breadcrumb path:
```
< All States / StateName
```
- Left-click on "All States" returns to state level
- StateName is read-only display

### No new API calls

Drill is purely local state — `setDrillParent(cat)` → `data?.geo_drill?.[cat]` (existing logic).
Search is also local state filtering `categories`. No new endpoints or queries.

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | C1 GEO continuous search + drill | Yes — portal DEV `4469ad7` |

## Blockers

None. tsc clean.

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`
Portal DEV: 9 commits ahead of origin.

## Next Steps

**[RD 0.4.2] Task 9 — ADVI-004 C2+C4** — ADV continuous + CLA continuous.
Gate CLEARED at bd-v2.15.0. Types at portal DEV `7df26bb`.

#### DistributionTab_C2_C4_adv_drill_cla_continuous.md

# DistributionTab C2+C4 — ADV Drill + CLA Continuous — 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-04
**Portal DEV commit:** `c562257`

## Objective

C2: ADV continuous NNA with architect->client drill (adv_drill now live at bd-v2.15.0).
C4: CLA continuous stacked area with full drill hierarchy (total/geo_drill/geo_city_drill/adv_drill).

---

## Work Completed

### C2 — ADV Continuous Drill

The drill logic for ADV already existed in `ContinuousChartView`:
```tsx
const drillViewData = isDrilled
  ? (cohort === 'geo' ? data?.geo_drill?.[drillParent!] : data?.adv_drill?.[drillParent!])
  : undefined
const showAdvComingSoon = isDrilled && cohort === 'adv' && !drillViewData
```
With `adv_drill` now live (bd-v2.15.0), this path returns real data. The "coming soon" message
only shows when drillViewData is undefined — no longer triggered.

**Fix added:** `canLegendDrill` now guards against second-level drill in ADV:
```tsx
// Before:
const canLegendDrill = (cohort === 'adv') || (cohort === 'geo' && !!data?.geo_drill)
// After:
const canLegendDrill = (cohort === 'adv' && !isDrilled) || (cohort === 'geo' && !!data?.geo_drill)
```
Client-level entries (drilled ADV) no longer show drill arrow buttons — ADV is terminal at client grain.

**Breadcrumb** was already updated in C1 to show `All Architects / ArchitectName` for ADV.

### C4 — CLA Continuous (new ClaContinuousView component)

Added new `ClaContinuousView` component (~200 lines) replacing the "Coming soon" placeholder.

**Data source:** `data.cla` (CumulativeChartResponse.cla — guarded if absent)

**Drill levels (GEO cohort):**
| Level | Data source | Drill to |
|-------|------------|---------|
| Total | `cla.total` | States from `cla.geo_drill` keys |
| State | `cla.geo_drill[stateKey]` | Cities from `cla.geo_city_drill[stateKey]` keys (guarded) |
| City | `cla.geo_city_drill[stateKey][cityKey]` | Terminal |

**Drill levels (ADV cohort):**
| Level | Data source | Drill to |
|-------|------------|---------|
| Total | `cla.total` | Architects from `cla.adv_drill` keys |
| Architect | `cla.adv_drill[advKey]` | Terminal |

**Chart:** Recharts AreaChart with `stackId="cla"` — same pattern as main continuous view.
Colors: `CATEGORY_COLORS.NMNC` (#16A34A green) and `CATEGORY_COLORS.NMEC` (#2563EB blue).
Fallback: `FALLBACK_COLORS` for any unexpected categories.

**Left panel layout:**
- Breadcrumb with back buttons at each level
- Hero metric: total AUA of current view
- NMNC/NMEC legend (current series)
- Contextual drill list (states/cities/architects) with right-arrow affordance, max-h-[160px] scroll

**Breadcrumb:** `< All States / StateName / CityName` (geo) or `< All Architects / ArchitectName` (adv).
Clicking intermediate breadcrumb level clears child drill (e.g., clicking StateName clears cityKey).

**Window toggle:** Updated to show for CLA mode too (removed `metric !== 'cla'` exclusion).
`CumulativeChartView` added to types import.

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | C2 ADV drill + C4 CLA continuous | Yes — portal DEV `c562257` |

---

## Blockers

None. tsc clean.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`
Portal DEV: 10 commits ahead of origin: `3dc9dc5`, `7df26bb`, `5125eb9`, `ed832db`,
`5f42dc6`, `bdcd00c`, `0bceb64`, `174958a`, `4469ad7`, `c562257`.

All 9 tasks complete. Portal DEV ready for DE review before DT push.

---

## All Tasks Summary

| # | Task | Commit | Status |
|---|------|--------|--------|
| 1 | distribution_nomenclature_fix | pre-applied | complete |
| 2 | continuous_view_max_window_clients_fix | ed832db | complete |
| 3 | xtick_spacing_fix | pre-applied | complete |
| 4 | advi_h_portal_primitives | 5f42dc6 | complete |
| 5 | advi_i_top_performers | bdcd00c | complete |
| 6 | advi_c3_cla_snapshot (addendum) | 174958a | complete |
| 7 | advi_c1_geo_continuous | 4469ad7 | complete |
| 8 | ADVI-005 4C stacked bar + rolling 1Y | 0bceb64 | complete |
| 9 | ADVI-004 C2+C4 ADV drill + CLA continuous | c562257 | complete |

#### DistributionTab_C3_cla_snapshot.md

# DistributionTab C3 — CLA Snapshot Redesign — 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-04
**Portal DEV commit:** `174958a`

## Objective

Replace the CLA snapshot diverging bar chart (inflows/outflows/NNA) with a composition view
showing NMNC vs NMEC book breakdown. Data source corrected to `getHeaderMetrics()` per addendum
`advi_c3_cla_snapshot_addendum.md` (1.0.0_SA_CTO-2026-03-04).

---

## Work Completed

### Data source change

Removed all `analyticsData.views.cla` reads from `ClaSnapshotView`. Added `useQuery` inside
the component:
```tsx
const { data: headerData, isLoading: headerLoading } = useQuery<HeaderMetricsResponse>({
  queryKey: ['headerMetrics'],
  queryFn: getHeaderMetrics,
  staleTime: 5 * 60 * 1000,
})
```
No prop threading. No dependency on `PartnerAnalyticsResponse`.

### Props interface update

| Removed | Kept |
|---------|------|
| `analyticsData: PartnerAnalyticsResponse` | `cohort: CohortOption` (kept for future use) |
| `selectedPeriod: TimePeriodKey` | |
| `onPeriodChange: (period: TimePeriodKey) => void` | |

Call site updated: `<ClaSnapshotView cohort={cohort} />`. Parent `selectedPeriod`/`setSelectedPeriod`
state preserved for other views (DistributionQuarterlyStrip, NnaQuarterlyStrip).

### Layout

Two-column flex split (same pattern as the rest of DistributionTab):

**Left partition:** Donut + legend + quarter strip
- Recharts `PieChart` with inner radius 60, outer 92 — two segments NMNC (green `#16A34A`) / NMEC (blue `#2563EB`)
- Absolute-positioned center label: `nmnc_pct%` + "New Clients" subtitle
- Legend: per-segment label, %, relationship count, AUA dollar amount
- Quarter strip: read-only mini stacked bars showing NMNC/NMEC mix per Q0-Q3
  - Finds last timeseries data point where `date <= dates.qN`
  - Falls back to `total.new_client_pct` for q0 if timeseries absent

**Right partition:** Account size distribution histogram + stats
- Recharts `BarChart` — two grouped bars per bin (NMNC green, NMEC blue)
- Bin labels: `nmnc_dist.histogram.bin_labels`
- Per-segment stats card: median, mean, count
- Legend row

### Removed

- `CLA_COLORS` constant (flows vocabulary — removed entirely)
- `ClaBarDatum` interface
- All NNA/inflows/outflows rendering
- Debug `console.log` statement
- `ClaView` type import (no longer used)

### New imports

- Recharts: `PieChart, Pie` (added to existing imports)
- API: `getHeaderMetrics` (added alongside `getCumulativeChart`)
- Types: `HeaderMetricsResponse, SegmentDistribution, RollingTimeseriesDataPoint`

### TypeScript fix

Recharts `Tooltip` `formatter` prop requires `value: number | undefined, name: string | undefined`
to match the `Formatter<number, string>` type signature. Fixed the formatter lambda accordingly.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| `useQuery` inside component, not prop threading | Addendum constraint: no headerData prop on DistributionTab |
| `_cohort` parameter name | cohort prop kept for future geo/adv split; unused now to avoid lint |
| Quarter strip reversed order | Show oldest→newest left-to-right (Q3→Q0) for natural time flow |
| Grouped bars (not overlapping) | Clearest comparison for NMNC vs NMEC account sizes |
| Stats card instead of reference lines | Median/mean are dollar values, not bin labels; text readout is cleaner |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | C3 CLA snapshot redesign | Yes — portal DEV `174958a` |

---

## Blockers

None. tsc clean.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`

Portal DEV is 8 commits ahead of origin.

---

## Next Steps

1. **[DE] Review C3 visual design** — confirm queryKey `['headerMetrics']` matches any existing
   key used by other components calling `getHeaderMetrics()`.
2. **[RD 0.4.2] Task 7 — advi_c1_geo_continuous** — GEO continuous NNA view.
3. **[RD 0.4.2] Task 9 — ADVI-004 C2+C4** — ADV continuous + CLA continuous.

#### DistributionTab_nomenclature_and_max_window_fix.md

# DistributionTab Nomenclature + Max Window Fix — 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-04
**Portal DEV commit:** `ed832db`

## Objective

Execute task orders `distribution_nomenclature_fix` and `continuous_view_max_window_clients_fix`
on DistributionTab.tsx, plus confirm xtick_spacing_fix (addendum) is already applied.

---

## Work Completed

### 1. Audit of Pre-Applied Changes

Before writing any code, audited DistributionTab.tsx against all three task orders.

**distribution_nomenclature_fix (11 changes):** 10 of 11 already applied in a prior session.
- `SnapshotDistributionChartProps.isNnaMode?: boolean` — present
- `SnapshotDistributionChart` function signature destructures `isNnaMode = false` — present
- Y-axis NNA label: `'Relationships (log)'` instead of `'Number of Relationships'`. Deviation
  is intentional — `(log)` suffix accurately reflects the log scale used in NNA mode. Left as-is.
- X-axis label: `{isNnaMode ? 'Period NNA' : 'Account Size'}` — present
- Tooltip row 1: `{isNnaMode ? 'NNA Range' : 'Account Size'}` — present
- Tooltip row 2: `{isNnaMode ? 'Relationship Count' : 'Account Count'}` — present
- `SnapshotDistributionMetrics` signature has `isNnaMode?: boolean` — present
- Primary tile: `{isNnaMode ? 'Total Relationships' : 'Total Accounts'}` — present
- Both `<SnapshotDistributionChart>` and `<SnapshotDistributionMetrics>` call sites pass `isNnaMode={isNnaMode}` — present
- AUA footnote muted span: `' Distribution reflects funded accounts only, log-spaced bins.'` — present

**xtick_spacing_fix (addendum — 3 changes):** Fully applied.
- Both containers at `h-[450px]` (donut ~line 1271, bell curve ~line 1449) — present
- `AreaChart margin={{ ..., bottom: 50 }}` — present
- `XAxis` uses custom SVG tick renderer with `height={50}`, `dy={12}`, `transform="rotate(-45)"` — present
- Y-axis label div: `justify-center`, `pointer-events-none`, `width: '16px'` — present
- X-axis label div: `bottom: '6px'`, `left: 'calc(50% + 15px)'` — present

### 2. continuous_view_max_window_clients_fix — Implemented (4 changes)

**The issue:** `ContinuousChartView` always shows "New Clients" tile. At Max window,
`data.metadata.new_clients['Max']` is never populated by the backend — always shows '--'.
"New Clients" is also semantically wrong over all time (every client is cumulative total).

**Type investigation:** The task order specified `cohortView?.current?.metrics?.client_count ?? cohortView?.metrics?.client_count`.
This fails tsc: `PartnerAnalyticsView.metrics` is `ViewMetrics` (no `client_count`); only
`PartnerAnalyticsViewWithPeriods.current.metrics` is `PeriodMetrics` (has `client_count`).
Used `hasTimeMachine()` guard (already imported) to satisfy TypeScript.

| Change | Location | What |
|--------|----------|------|
| Interface | `ContinuousChartViewProps` | Added `totalClients?: number` |
| Signature | `ContinuousChartView` | Destructures `totalClients` |
| Call site | `<ContinuousChartView>` in `DistributionTab` | IIFE with `hasTimeMachine` guard derives `view.current.metrics.client_count` |
| Tile | ~line 807 | `window === 'Max'` ternary: label/value switch |

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| `hasTimeMachine` guard instead of task order's `??` fallback | `ViewMetrics` has no `client_count` — task order's double-access pattern fails tsc. Guard is correct and already used elsewhere in the file. |
| IIFE at call site | `hasTimeMachine` needs a variable to guard; IIFE keeps it inline without polluting JSX scope above. |
| Leave Y-axis `'Relationships (log)'` as-is | More informative than `'Number of Relationships'`; log scale is factual for NNA mode. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | `totalClients` prop wiring + Max window tile fix | Yes — portal DEV `ed832db` |

---

## Blockers

None.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`

Tasks 1 (nomenclature — pre-applied), 2 (max window — implemented), and 3 (xtick — pre-applied)
are all done. `bunx tsc -b` clean. Portal DEV is now 4 commits ahead of origin: `3dc9dc5`,
`7df26bb`, `5125eb9`, `ed832db`. DE reviews before DT pushes.

---

## Next Steps

1. **[RD 0.4.2] Start H (advi_h_portal_primitives)** — AdvisorsTab panel primitives refactor.
   Must precede I (Top Performers redesign) and 4C (stacked bar).
2. **[RD 0.4.2] Then I (advi_i_top_performers)** — Top Performers visual redesign.
3. **[RD 0.4.2] Then 4C (ADVI-005)** — Stacked bar + rolling 1Y in AdvisorsTab.
4. **[RD 0.4.2] DistributionTab: C3, C1, C2+C4** — in that order.

**Files to touch next:**
- `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` — H then I then 4C

**Do NOT:**
- Push portal DEV — DT is the push gate after DE reviews
- Start 4C before completing H (structural refactor prevents collision)

#### Y1_Y4_Y6_Y12_phase1_visual.md

# Y1+Y4+Y6+Y12 Phase 1 Visual Fixes -- 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-04
**Portal DEV commits:** `f9c0e59` -> `76c7621` -> `7258c5e` -> `2981133`

## Objective

Execute four Phase 1 visual-only changes from Yang V2 PRD. All use existing data, no DS/DT dependency.

---

## Work Completed

### Y1 -- AUA Stack Order Flip (PartnerAnalytics.tsx)

Reversed `barCategories` array in the `Bar` map so NMNC (new clients, green) renders above
NMEC (existing clients, blue). Recharts renders first-declared Bar at bottom of stack.
`[...barCategories].reverse()` ensures NMEC is bottom, NMNC is top regardless of data order.

### Y4 -- NNA Diverging Bar Alignment + Net Line (PartnerAnalytics.tsx)

This required three iterations to get right. The task order's instructions were incorrect
about Recharts stacking mechanics. Documenting the full iteration for future reference.

**Attempt 1 (`f9c0e59`):** Added `stackId="nna"` to both Bar components + `netMidpoint`
field with formula `(inflow + outflow) / 2` for the Line dataKey.

Two problems:
- `stackId` without `stackOffset="sign"` causes Recharts to stack additively: outflow bar
  renders ON TOP of inflow bar (starting from inflow's top, going downward), not
  independently from zero. Visually broken.
- `netMidpoint` formula was wrong. NNA line should show actual net value (e.g., +10M
  inflows - 20M outflows = -10M NNA), not the geometric center of the bar span.

**Attempt 2 (`76c7621`):** Fixed net line -- reverted Line dataKey back to `"net"` (actual
NNA value), removed `netMidpoint` computed field. Net line now correctly shows actual NNA.

**Attempt 3 (`7258c5e`):** Removed `stackId="nna"` entirely to fix the stacking problem.
Bars now extend independently from zero (inflow up, outflow down). But without stackId,
Recharts places the two bars side-by-side (two thin columns per period) -- visually messy.

**Final fix (`2981133`):** The correct Recharts pattern for diverging bars at the same
x-position:
1. Add `stackOffset="sign"` to the `<ComposedChart>` component
2. Add `stackId="nna"` to both `<Bar>` components

`stackOffset="sign"` is the key -- it tells Recharts to route positive values above zero
and negative values below zero when stacking. Combined with `stackId`, both bars share one
column per period while each extends from the zero line in the correct direction.

**Recharts diverging bar reference (for future agents):**
- `stackId` alone = additive stacking (bar 2 starts where bar 1 ends). WRONG for diverging.
- No `stackId` = side-by-side bars. Correct direction but misaligned x-position.
- `stackId` + `stackOffset="sign"` = diverging bars at same x-position. CORRECT.

### Y6 -- Snapshot NNA Bucket Filter + Footnote (DistributionTab.tsx)

**Y6.1:** Added `filteredIndices` array in `SnapshotDistributionChart`. In NNA mode, filters
out any histogram bin where both `bins[i]` (lo) and `bins[i+1]` (hi) fall within [-1000, 1000].
Non-NNA mode passes all bins through.

**Y6.2:** Added footnote below NNA histogram: "Relationships with net flows between -$1,000
and $1,000 are excluded from this distribution." Wrapped in JSX fragment with existing footnote.

### Y12 -- Drop 1Y Rolling from Advisors Tab (AdvisorsTab.tsx)

Removed:
- `FlowsViewMode` type
- `FLOWS_VIEW_OPTIONS` constant
- `flowsView` / `setFlowsView` state
- View toggle from Rolling Flows PanelHeader
- `Rolling1YChart` component (~120 lines)
- `RollingFlowsChart` legacy component (~110 lines)
- `activeFlowsSeries` useMemo
- `FlowsMetric` type, `FLOWS_METRIC_OPTIONS`, `FLOWS_WINDOW_OPTIONS` constants
- `flowsMetric`, `flowsWindow` state
- Unused imports: `LineChart`, `Line`, `useMemo`, `Users`, `AdvisorRolling1YSeries`,
  `RollingFlowsWindowKey`, `RollingFlowsDataPoint`, `AdvisorRollingSeries`, `LINE_COLORS`

Kept: StackedBarChart, period toggle (QTD/YTD/1Y/Max), role toggle.

**DS coordination note:** rolling_1y key removal from script 10 is DS's call -- confirm no
other consumer before DS drops it. Y12 removes the UI only.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| `[...barCategories].reverse()` for Y1 | Declarative reversal; works regardless of data order |
| `stackOffset="sign"` + `stackId="nna"` for Y4 | Only correct Recharts pattern for diverging bars at same x-position. See iteration notes above. |
| Net line uses `dataKey="net"` (actual NNA) | Task order's midpoint formula was wrong; NNA line must show true net value |
| `filteredIndices` array for Y6 | Filters by numeric bin boundaries, not label strings |
| Bulk removal for Y12 | 332 lines deleted, 39 added. Clean separation of concerns. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx` | Y1 stack flip + Y4 diverging bar (4 commits) | Yes -- portal DEV `f9c0e59` `76c7621` `7258c5e` `2981133` |
| `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` | Y12 1Y rolling removal | Yes -- portal DEV `f9c0e59` |
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | Y6 bucket filter + footnote | Yes -- portal DEV `f9c0e59` |

---

## Blockers

None. tsc clean.

---

## Current State

**Status:** COMPLETE
**Active branch:** portal `DEV`

All four Y-streams implemented across 4 commits. Portal DEV head at `2981133`.
Andrew confirmed Y4 NNA diverging bar visual is correct.

---

## Next Steps

1. **[DE] Review commits** before DT pushes portal DEV.
2. **[RD 0.4.2] Next task orders** -- ADVI-Y8 (continuous AUA stacked bar) pending.

#### Y8_continuous_aua_stacked_bar.md

# Y8 Continuous AUA Stacked Bar -- 0.4.2_RD_AdvisorIntelligence

**Date:** 2026-03-04
**Portal DEV commits:** pending (uncommitted on portal DEV)

## Objective

Convert the AUA continuous view from AreaChart (stacked area) to BarChart (stacked bar)
and add a Month/Quarter/Year interval toggle. Task order: ADVI-Y8-continuous-aua-stacked-bar.

---

## Work Completed

### Y8 -- Continuous AUA: Area to Stacked Bar + Interval Toggle (DistributionTab.tsx)

**State (line 690):** Added `auaInterval` state (`'monthly' | 'quarterly' | 'annually'`,
default `'monthly'`) to `ContinuousChartView`. Per-view state -- does not leak to other
metrics or views.

**Aggregation memo (lines 757-791):** Added `aggregatedBarData` useMemo that buckets
daily `filteredChartData` into period snapshots:
- `getPeriodKey()` maps each date to a month, quarter, or year key + display label
- Uses last-data-point-per-period strategy (end-of-period snapshot for cumulative AUA data)
- Sorted by period key for chronological ordering
- Only runs when `metric === 'aua'` (NNA and CLA early-return before this code path)

**Chart replacement (lines 956-1066):** Replaced `AreaChart`/`Area` with `BarChart`/`Bar`:
- Stacked bars with `stackId="aua"`, 0.85 fill opacity
- Reversed `displayCategories` for render order (NMNC on top, consistent with Y1)
- Rounded top corners (`radius={[4,4,0,0]}`) on topmost bar segment
- `vertical={false}` on CartesianGrid for cleaner bar chart appearance
- Cursor changed from line stroke to subtle fill highlight

**Interval toggle (lines 958-973):** Pill toggle (Month / Quarter / Year) positioned
top-right of the chart area. Uses same styling pattern as other toggles in the codebase
(bg-white/10 container, bg-white/20 active state).

**Tooltip:** Simplified -- shows period label (e.g., "Mar '26", "Q1 '26", "2026")
instead of raw date. "Cumulative AUA" header. Categories sorted by value descending.

### What was NOT changed

- NNA and CLA views are unaffected (early returns before the bar chart code path)
- `Area` import remains in the file -- may be used by other chart paths; did not audit
- No color changes, no data source changes
- No new dependencies

---

## Technical Notes

**Why last-data-point-per-period (not average or sum)?**
AUA is cumulative (total assets under advisement at a point in time). Summing or averaging
daily AUA values within a month has no financial meaning. The correct bar value is the
end-of-period snapshot -- the last available data point before the period boundary.

**Why `metric !== 'aua'` guard returns empty array?**
At the chart render level, only AUA reaches the BarChart path. But the memo runs on every
render regardless of which early-return fires. The guard prevents unnecessary computation
and ensures `aggregatedBarData` is always a valid empty array for non-AUA metrics.

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` | Y8 area-to-bar + interval toggle | Pending |

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| End-of-period snapshot (last point per period) | Cumulative AUA is a point-in-time metric; sum/average is meaningless |
| Reversed displayCategories for bar order | Consistent with Y1 -- NMNC (new) on top of NMEC (existing) |
| Per-view `auaInterval` state | Interval preference is specific to AUA continuous view; no reason to share globally |
| Pill toggle top-right | Matches existing toggle patterns; does not crowd the category list on the left |

---

## Blockers

None. tsc clean.

---

## Current State

**Status:** CODE COMPLETE -- awaiting commit
**Active branch:** portal `DEV`
**tsc:** Clean (no type errors)

The DistributionTab.tsx diff also contains unrelated PortfolioManagement changes from another
agent's work. Y8 changes are isolated to the `ContinuousChartView` component within
DistributionTab.tsx.

---

## Next Steps

1. **Commit Y8** to portal DEV (isolated commit for DistributionTab.tsx Y8 changes only).
2. **Visual QA** -- Andrew/Yang confirm stacked bar appearance and interval toggle behavior.
3. **Check if `Area` import can be cleaned up** -- audit whether any other chart path in DistributionTab.tsx still uses Area.


### 0.4.2_RD_AdvisorIntelligence -- Pending Task Orders

#### page_inventory.md

# Task Order: Page Inventory

<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-page-inventory</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-02</date>
    <status>pending</status>
  </metadata>

  <objective>
    Produce a complete structured inventory of your page. This is a one-time
    codebase audit that becomes your permanent context for all future sessions.
    Read every file in your page directory and document what exists.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
  </scope>

  <requirements>
    <requirement id="1">List every .tsx/.ts file in your page directory tree with a 1-line description of what it does</requirement>
    <requirement id="2">For every API call (useQuery, useMutation, fetch, axios) found in your page: document the endpoint URL, HTTP method, request payload shape, and response shape</requirement>
    <requirement id="3">For every shared component imported from outside your page directory (e.g., from portal/src/components/): list the import path and what it provides</requirement>
    <requirement id="4">For every TypeScript type/interface your page defines or imports: list the type name, which file defines it, and its key fields</requirement>
    <requirement id="5">Document current page state: what tabs/panels exist, which are functional vs. stubbed vs. broken</requirement>
    <requirement id="6">List any TODO/FIXME/HACK comments found in your page code</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Output is valid XML written to org/tier3_junior/0.4.2_RD_AdvisorIntelligence/deliverables/page_inventory.xml</criterion>
    <criterion id="2">Every .tsx/.ts file in the page directory is accounted for</criterion>
    <criterion id="3">API endpoints include actual URL strings, not just hook names</criterion>
    <criterion id="4">Shared component imports include the actual import path</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify any source code -- this is a read-only audit</constraint>
    <constraint>Do NOT create or edit files outside your agent folder</constraint>
    <constraint>Use Glob, Grep, and Read tools only -- no Explore agent, no Task agent</constraint>
  </constraints>

  <deliverables>
    <deliverable type="document">
      org/tier3_junior/0.4.2_RD_AdvisorIntelligence/deliverables/page_inventory.xml
    </deliverable>
  </deliverables>
</task_order>

## Deliverable XML Schema

Write your inventory using this structure:

```xml
<page_inventory>
  <metadata>
    <agent>0.4.2_RD_AdvisorIntelligence</agent>
    <page>AdvisorIntelligence</page>
    <directory>portal/src/pages/AdvisorIntelligence/</directory>
    <date>2026-03-02</date>
  </metadata>

  <files>
    <file path="portal/src/pages/AdvisorIntelligence/ComponentName.tsx" type="component">
      One-line description
    </file>
  </files>

  <api_calls>
    <api_call>
      <hook>useQuery / useMutation / fetch</hook>
      <endpoint>/api/scoped/some-endpoint</endpoint>
      <method>GET</method>
      <request_shape>{ param1: string, param2: number }</request_shape>
      <response_shape>{ data: Array, total: number }</response_shape>
      <file>portal/src/pages/AdvisorIntelligence/hooks.ts:42</file>
    </api_call>
  </api_calls>

  <shared_imports>
    <import>
      <from>portal/src/components/ui/Panel.tsx</from>
      <provides>Panel, PanelHeader</provides>
      <used_in>portal/src/pages/AdvisorIntelligence/SomeComponent.tsx</used_in>
    </import>
  </shared_imports>

  <types>
    <type name="SomeType" defined_in="portal/src/pages/AdvisorIntelligence/types.ts">
      Key fields: id: string, name: string, value: number
    </type>
  </types>

  <page_structure>
    <tab name="TabName" status="functional | stubbed | broken">
      Description of what this tab shows
    </tab>
  </page_structure>

  <issues>
    <issue file="path:line" type="TODO | FIXME | HACK">
      Comment text
    </issue>
  </issues>
</page_inventory>
```


### 0.4.2_RD_AdvisorIntelligence -- Recent Commits

# Recent commits by 0.4.2_RD_AdvisorIntelligence

513adfdf org(0.4.2_RD_AdvisorIntelligence): Y8 session log + phase 1 task order status update
ce2cb497 0.4.2_RD_AdvisorIntelligence: mark 9 task orders complete + session logs + portal submodule advance
076e1120 0.4.0_DT_ClientPlatform: enrich Pod 4 (ClientPlatform) agent prompts with source-grounded context
b5ace0c0 org: quality audit -- fix bugs, upgrade thin profiles, seed missing deliverables
b331d3e6 feat(org): 0.4.0_DE_ClientPlatform — continuous view Max window clients fix task order
c08effac feat(org): 0.4.0_DE_ClientPlatform wave 2 — pod inventory + RD task orders
42f99352 logs: 0.4.2_RD_AdvisorIntelligence distribution nomenclature fix session log
2f8de475 docs(org): add xtick fix addendum for 0.4.2_RD_AdvisorIntelligence
4e046836 logs: 0.4.2_RD_AdvisorIntelligence xtick spacing fix session log

