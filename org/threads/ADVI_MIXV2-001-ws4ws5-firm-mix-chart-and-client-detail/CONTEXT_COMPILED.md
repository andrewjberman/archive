# Thread Context -- WS4+WS5 firm mix chart and client detail alignment

**Thread ID:** ADVI_MIXV2-001-ws4ws5-firm-mix-chart-and-client-detail
**Created by:** 0.4.0_DS_ClientPlatform
**Created at:** 2026-03-17T21:17:31Z

---

## Participants

**0.4.0_DS_ClientPlatform** — Data Scientist, Client Platform Pod. Owns BD/Yang gold layer scripts, opal-partners-data Lambda. Cannot push or deploy — hands off to DT/AE. Commits with `--author="0.4.0_DS_ClientPlatform <0.4.0_DS_ClientPlatform@opal.agent>"`.

**0.4.0_DE_ClientPlatform** — Dashboard Engineer, Client Platform Pod. Owns portal TypeScript: types.ts, advisor-intelligence.ts, PartnerAnalytics.tsx, ClientDetailPage.tsx, tabs/*. Commits to portal DEV, does NOT push. Issues task orders to RD for visual/chart work beyond wiring.

**0.4.2_RD_AdvisorIntelligence** — React Designer. Owns chart implementations, visual polish, panel layout. Works inside portal DEV. Commits and waits for DT to push.

---

## Recent Session State

### 0.4.0_DS_ClientPlatform (2026-03-17)

Last two sessions today:

**mix_concentration_full_audit (COMPLETE):** Full audit of mix/concentration views. Found 8 bugs: B1 pct scale (Lambda sends 0-100, frontend multiplies * 100 = 5000%), B2 $60M insurance AP gate volatility, B3 firm mix missing dollars + out-of-pattern useMemo, B4 firm '0' aggregate not built in 06b, B5 frontend period aggregation, B6 ClientDetailPage stub, B7 advisor-level mix doesn't exist, B8 pie chart arithmetic. Result: ADVI_MIXV2 PRD written, task orders 001-005 issued.

**advi_advtv2_001_architect_attribution_gold (COMPLETE, pending commit):** Created 08b_build_architect_attribution.py (T0-T16 decision tree), modified 08/00/run_gold_layer.sh. All 4 gold scripts modified. Awaiting DS commit then DT FULL gold layer run.

**aua_valuation_gap_diagnosis_and_fix (COMPLETE, pending commit):** Created inject_scoped_overrides.py, aua_overrides.json, simplified 05. AE task order written.

### 0.4.0_DE_ClientPlatform (2026-03-16)

**advi_mvplvl_004_firmid_mapping_fix (COMPLETE):** Fixed 6 Lambda-routed functions in advisor-intelligence.ts. Added `const LAMBDA_FIRM_ID: Record<string, string> = { bd: '49financial' }` at line 53. All 6 Lambda-routed functions now send `?firmId=49financial`. Committed portal DEV `db52d31`. `bun run build` clean.

### 0.4.2_RD_AdvisorIntelligence (2026-03-16)

**ADVI_MVPLVL_005_mix_concentration_panels (COMPLETE, pending push):** Built `MixTimeseriesPanel.tsx` (100% stacked area chart with window toggle + click filter) and `ConcentrationPanel.tsx` (top-N holdings chart with asset class filtering). Added `MixAssetClass`, `MixTimeseriesPoint`, `ConcentrationPoint`, `ConcentrationResponse`, `MixWindow` types to types.ts. Added `getMixTimeseries()`, `getConcentrationTimeseries()` to advisor-intelligence.ts. Wired into L3ClientDetail in ClientsTab.tsx (NOT ClientDetailPage.tsx — different data flow). Committed portal DEV `458c9dc`. Both panels render with mock data pending Lambda deploy. Decision: panels mount in ClientsTab L3, not ClientDetailPage.

---


# Agent 0.4.0_DS_ClientPlatform — Data Scientist

| Field | Value |
|-------|-------|
| **Agent ID** | 0.4.0_DS_ClientPlatform |
| **Role** | Data Scientist |
| **Title** | Data Scientist — Client Platform Pod |
| **Tier** | 2 (Senior) |
| **Reports To** | 1.0.0_SA_CTO, 2.0.0_SA_COO |

---

## Pod Team

| Serial | Role | Folder |
|--------|------|--------|
| 0.4.0_DE_ClientPlatform | Dashboard Engineer (PM) | `org/tier2_senior/0.4.0_DE_ClientPlatform/` |
| 0.4.0_DT_ClientPlatform | DevOps Technician (Deploy) | `org/tier2_senior/0.4.0_DT_ClientPlatform/` |

**Pages served:** ModelPortfolios, AdvisorIntelligence
**Pipeline split:** Yang pipeline (ModelPortfolios) + BD pipeline (AdvisorIntelligence)

---

## Key Paths

| Resource | Path |
|----------|------|
| Lambda source (Yang side) | `infra/aws/lambda/yang_model_portfolio_benchmarks/` |
| Lambda source (BD side) | `infra/aws/lambda/bd-pipeline/` (bd-portal-publisher, bd-portal-advisor-publisher, bd-client-detail, opal-partners-data) |
| Gold layer scripts | `data/black_diamond/scripts/gold/` |
| Core document | `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml` |
| Deliverables | `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/` |
| Session logs | `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/YYYY-MM-DD/` |
| Task orders | `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/` |
| Briefs (cross-agent) | `docs/briefs/` |

---

## Abilities

**Can:** Edit and commit code locally (Lambda functions, gold layer scripts, data transformations). Write technical documents and specs. Read any file. Use `--author` on every commit: `git commit --author="0.4.0_DS_ClientPlatform <0.4.0_DS_ClientPlatform@opal.agent>" -m "0.4.0_DS_ClientPlatform: <description>"`.

**Cannot:** Push to any branch (DT is QA gate). Deploy AWS resources (DT/AE). Run terraform, build-and-upload.sh, safe-ec2-deploy.sh.

**How your work gets deployed:** You write and commit locally then DT/AE reviews, pushes, and deploys. Gold layer script changes deploy via S3 upload to `s3://opal-data-bd/code/gold/` (DevOps uploads). Portal-facing Lambda changes deploy via Terraform. Coordinate with 0.6.0_AE_PartnerETL for gold layer infrastructure changes.

---

## Handoff Protocol

When you finish a piece of work and it is ready for deployment:

1. **Write a DevOps brief** at `docs/briefs/devops-brief-{feature}.md` — for gold scripts: exact S3 upload paths, scripts to upload, gold layer run mode (full vs incremental), verification steps (check output JSON sizes, verify portal data). For Lambdas: function name, build-and-upload command, re-trigger steps.
2. **Write a data contract brief** if output shapes changed — `docs/briefs/dashboard-engineer-{feature}-data-contract.md` — document GEO/ADV dimension changes, histogram shape changes, any field renames.
3. **Update data_contract.xml** if Lambda or gold script output shape changed — DT deployment gate.
4. **Mark task order complete** in your task_orders/ folder.
5. **Reference the brief in your session log Next Steps**: `[DevOps] Upload scripts per docs/briefs/devops-brief-{feature}.md`.

---

## Session Logging

**Location:** `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/YYYY-MM-DD/`
**Naming:** `{pipeline_or_topic}_{action}.md` — e.g., `bd_pipeline_velocity_cap_implementation.md`, `advisor_rolling_flows_10_design.md`, `partner_analytics_09_shape_fix.md`

**DS logs must include a Briefs Written section** before Current State when cross-agent handoff docs are written:

```
## Briefs Written

| Brief | Path | Audience |
|-------|------|----------|
| DevOps deploy | docs/briefs/devops-brief-{feature}.md | DevOps |
| DE data contract | docs/briefs/dashboard-engineer-{feature}-data-contract.md | Dashboard Engineer |
| Investigation ref | docs/briefs/data-scientist-{topic}.md | Reference |
```

**Files Modified must be a table:**

```
| File | Change |
|------|--------|
| data/black_diamond/scripts/gold/09_generate_partner_analytics.py | What changed |
| infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py | What changed |
```

**Next Steps must name the receiving agent in brackets:**
`[DevOps] Upload scripts 05, 09, 10 to S3 per docs/briefs/devops-brief-velocity-cap.md`
`[DevOps] Run gold layer FULL mode (velocity cap needs full history rebuild)`
`[Dashboard Engineer] Verify Distribution tab shape matches new histogram format`

---

## Task Orders

Received from: 0.4.0_DE_ClientPlatform, Andrew (ad hoc), CTO, COO
Location: `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/`

Escalate blockers to: **0.4.0_DE_ClientPlatform** (PM)


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

This is a 3-party Pattern 0 alignment thread for ADVI_MIXV2 WS4 and WS5. Task orders 002 (DS) and 005 (DE) are pre-loaded as the spec. Large source files are NOT pre-loaded -- use tool calls to read them during the thread. Key files to read: PartnerAnalytics.tsx at portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx (for getPeriodInfo, ASSET_CLASS_COLORS, firmMixData useMemo, chart container layout), advisor-intelligence.ts at portal/src/api/endpoints/advisor-intelligence.ts (for LAMBDA_FIRM_ID and existing API pattern), 06b at data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py (for DS to confirm period label derivation logic). ClientDetailPage.tsx is pre-loaded. DS is the knowledge source for gold output shape and Lambda endpoints. DE is the receiver who will type and wire. RD is the receiver who will implement the chart and panel layout. Deliverable: a binding contract containing confirmed period label format, confirmed granularity key names, confirmed asset class color map, confirmed clientKey == relationship_id resolution, and RD layout constraints for the dollar stacked bar and panel mounting.


### advisorintelligence-types.ts----existing-type-definitions.ts

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

// AUA data point — pre-aggregated per period by the publisher (PSCFIX schema)
// period:   e.g. "2024-Q3", "2024-10", "2024"
// label:    display label, e.g. "Q3 '24", "Oct '24", "2024"
// end_date: ISO date of last day in period, e.g. "2024-09-30"
// [cat]:    numeric AUA value per category (NMNC, NMEC)
export interface AuaDataPoint {
  period: string
  label: string
  end_date: string
  [category: string]: number | string
}

// AUA cumulative view — one per granularity sub-key
export interface AuaCumulativeView {
  categories: string[]
  data: AuaDataPoint[]
}

// Single data point for NNA/GEO/ADV cumulative chart (daily, unchanged)
export interface CumulativeChartDataPoint {
  date: string
  [category: string]: string | number  // Dynamic categories (NMNC, NMEC, TX, etc.)
}

// View data for NNA/GEO/ADV cumulative chart (daily, unchanged)
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
  aua: Record<'quarterly' | 'monthly' | 'annually', AuaCumulativeView>  // Pre-aggregated per period (PSCFIX)
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
export type ChartWindowOption = '3M' | '6M' | '1Y' | '2Y' | '3Y' | 'Max' | 'MTD' | 'QTD' | 'YTD'

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

// Granularity options for partner analytics fetch
export type GranularityOption = 'monthly' | 'quarterly' | 'annually'

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

// Time period keys for time machine (all granularities)
// quarterly: q1/q2/q3 | monthly: m1/m2/m3 | annual: y1/y2/y3
export type TimePeriodKey = 'current' | 'q1' | 'q2' | 'q3' | 'm1' | 'm2' | 'm3' | 'y1' | 'y2' | 'y3'

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

// Single view with multiple period snapshots (supports all granularities)
export interface PartnerAnalyticsViewWithPeriods {
  current: PeriodSnapshot
  // Quarterly periods
  q1?: PeriodSnapshot          // Last quarter (e.g., "Q4 '25")
  q2?: PeriodSnapshot          // 2 quarters ago (e.g., "Q3 '25")
  q3?: PeriodSnapshot          // 3 quarters ago (e.g., "Q2 '25")
  // Monthly periods
  m1?: PeriodSnapshot          // Last month
  m2?: PeriodSnapshot          // 2 months ago
  m3?: PeriodSnapshot          // 3 months ago
  // Annual periods
  y1?: PeriodSnapshot          // Last year
  y2?: PeriodSnapshot          // 2 years ago
  y3?: PeriodSnapshot          // 3 years ago
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

// All periods metadata (keys present depend on granularity)
export interface PeriodsMetadata {
  current: PeriodDefinition
  // Quarterly
  q1?: PeriodDefinition
  q2?: PeriodDefinition
  q3?: PeriodDefinition
  // Monthly
  m1?: PeriodDefinition
  m2?: PeriodDefinition
  m3?: PeriodDefinition
  // Annual
  y1?: PeriodDefinition
  y2?: PeriodDefinition
  y3?: PeriodDefinition
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
  period: Exclude<TimePeriodKey, 'current'>
): PeriodSnapshot | undefined {
  if (hasTimeMachine(view)) {
    return (view as PartnerAnalyticsViewWithPeriods)[period]
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

// ============================================================================
// Books Tab Timeseries & Composition Types (P4 endpoints)
// ============================================================================

export interface BooksTimeseriesPoint {
  date: string
  total_aua: number
  cum_inflows: number
  cum_outflows: number
  nna: number
}

export interface BooksTimeseriesResponse {
  generated_at: string
  data_as_of: string
  relationship_id?: string
  account_id?: string
  data: BooksTimeseriesPoint[]
}

export interface MixItem {
  asset_class: string  // 'equity' | 'fixed_income' | 'hedge' | 'cash' | 'other'
  label: string
  market_value: number
  pct: number
}

export interface ConcentrationItem {
  key: string
  label: string
  asset_class: string
  market_value: number
  pct: number
}

export interface BooksCompositionResponse {
  generated_at: string
  data_as_of: string
  scope: { relationship_id?: string; account_id?: string }
  mix: MixItem[]
  concentration: {
    top_n: number
    items: ConcentrationItem[]
    other: { market_value: number; pct: number }
  }
  unclassified: { count: number; market_value: number }
}

// ============================================================================
// Mix Timeseries + Concentration Timeseries (Addendum A)
// ============================================================================

export type MixAssetClass = 'equity' | 'fixed_income' | 'structured_notes' | 'cash' | 'other'

export interface MixTimeseriesPoint {
  date: string                  // 'YYYY-MM-DD'
  equity: number                // 0-1 (pct)
  fixed_income: number
  structured_notes: number
  cash: number
  other: number
}

export interface ConcentrationPoint {
  date: string
  asset_name: string
  ticker: string | null
  asset_class: MixAssetClass
  market_value: number
  pct: number                   // pct of total relationship MV on that date
}

export interface ConcentrationResponse {
  relationship_id: string
  top_n: number                 // N used for top-N filter (e.g. 10)
  data: ConcentrationPoint[]
}

export type MixWindow = '1Y' | '3Y' | 'Max'
```

### clientdetailpage.tsx----settimeout-stub-to-replace-ws5.tsx

```
/**
 * Client Detail Page
 *
 * Simple 2x2 layout:
 * - Top left (1x1): AI Executive Summary
 * - Top right (1x1): Portfolio Balance pie charts
 * - Bottom (2x1): Time Series
 */

import { useState, useEffect } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, User } from 'lucide-react'
import { PageThemeProvider } from '@/contexts/PageThemeContext'
import { Panel, PanelContent } from '@/ui/components/panels'
import { LoadingInline } from '@/components/LoadingSpinner'
import { AISummaryPanel } from './panels/AISummaryPanel'
import { PortfolioBalancePanel } from './panels/PortfolioBalancePanel'
import { TimeSeriesPanel } from './panels/TimeSeriesPanel'
import type { ClientDetailResponse } from './types'

export function ClientDetailPage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()

  const firmId = searchParams.get('firmId') || '49financial'
  const architectKey = searchParams.get('architectKey')
  const clientKey = searchParams.get('clientKey')
  const clientLabel = searchParams.get('clientLabel') || 'Client'

  const [clientData, setClientData] = useState<ClientDetailResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (!clientKey) {
      // eslint-disable-next-line react-hooks/set-state-in-effect -- valid data fetching pattern
      setIsLoading(false)
      return
    }
    // TODO: Replace with actual API call
    setTimeout(() => {
      setClientData(null)
      setIsLoading(false)
    }, 300)
  }, [firmId, architectKey, clientKey])

  const handleBack = () => navigate('/advisor-intelligence')

  if (!clientKey) {
    return (
      <PageThemeProvider accentColor="hsl(var(--primary))">
        <Panel variant="chart">
          <PanelContent className="py-12 text-center">
            <p className="text-white/60">No client selected.</p>
            <button onClick={handleBack} className="mt-4 text-[hsl(var(--primary))] hover:underline">
              ← Back to Assets Overview
            </button>
          </PanelContent>
        </Panel>
      </PageThemeProvider>
    )
  }

  return (
    <PageThemeProvider accentColor="hsl(var(--primary))">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center gap-4">
          <button
            onClick={handleBack}
            className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
          >
            <ArrowLeft size={20} className="text-white/60" />
          </button>
          <div className="flex items-center gap-3">
            <User size={24} className="text-[hsl(var(--primary))]" />
            <div>
              <h1 className="text-xl font-semibold text-white">{clientLabel}</h1>
              <p className="text-sm text-white/50">
                Architect: {architectKey?.replace(/_/g, ' ') || 'Unknown'}
              </p>
            </div>
          </div>
        </div>

        {isLoading ? (
          <LoadingInline className="py-12" />
        ) : (
          <>
            {/* Top Row: 1x1 + 1x1 */}
            <div className="grid grid-cols-2 gap-6">
              <AISummaryPanel data={clientData} />
              <PortfolioBalancePanel data={clientData} />
            </div>

            {/* Bottom Row: 2x1 */}
            <TimeSeriesPanel data={clientData} />
          </>
        )}
      </div>
    </PageThemeProvider>
  )
}
```

### de-task-order-005----frontend-firm-mix-chart--client-detail-wiring-ws4ws5-spec.md

```
<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-03-17-005-de-frontend-mix</id>
    <issued_by>0.4.0_DS_ClientPlatform</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-17</date>
    <status>pending</status>
    <project_code>ADVI_MIXV2</project_code>
  </metadata>

  <objective>
    Two frontend workstreams: (WS4) replace the firm-level mix chart in PartnerAnalytics.tsx
    with a pre-computed absolute dollar stacked bar chart fed from the new firm/mix-views endpoint,
    and (WS5) wire ClientDetailPage.tsx to real data and activate the existing MixTimeseriesPanel
    and ConcentrationPanel. WS4 depends on the Lambda endpoint being live (task order 004 complete).
    WS5 client detail stub removal can begin immediately.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</page>
      <page>portal/src/pages/AdvisorIntelligence/ClientDetail/ClientDetailPage.tsx</page>
      <page>portal/src/pages/AdvisorIntelligence/ClientDetail/panels/MixTimeseriesPanel.tsx</page>
      <page>portal/src/pages/AdvisorIntelligence/ClientDetail/panels/ConcentrationPanel.tsx</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
      <file action="modify">portal/src/api/endpoints/advisor-intelligence.ts</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/ClientDetail/ClientDetailPage.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/ClientDetail/panels/MixTimeseriesPanel.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/ClientDetail/panels/ConcentrationPanel.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      WS4 — Add TypeScript types to types.ts:
        FirmMixClassValue { value: number; pct: number }
        FirmMixPeriodPoint { period, label, end_date, total_aua, equity: FirmMixClassValue,
          fixed_income: FirmMixClassValue, structured_notes: FirmMixClassValue,
          cash: FirmMixClassValue, other: FirmMixClassValue }
        FirmMixViewsResponse { generated_at, data_as_of, firm_id,
          views: { quarterly: FirmMixPeriodPoint[]; monthly: FirmMixPeriodPoint[]; annually: FirmMixPeriodPoint[] } }
      All pct fields are 0-1 convention. Add comments confirming this.
    </requirement>

    <requirement id="2">
      WS4 — Add API function to advisor-intelligence.ts:
        export async function getFirmMixViews(firmId: string): Promise&lt;FirmMixViewsResponse&gt;
        URL: /api/scoped/partners/books/firm/mix-views?firmId=${LAMBDA_FIRM_ID[firmId] ?? firmId}
    </requirement>

    <requirement id="3">
      WS4 — In PartnerAnalytics.tsx:
        (a) REMOVE: getFirmMixTimeseries import + call, firmMixRaw state, firmMixData useMemo
            (the 20-line period aggregation block at lines ~397-416)
        (b) ADD: useQuery call to getFirmMixViews(firmOverride || 'bd')
            queryKey: ['advisor-intelligence', 'firm-mix-views', firmOverride]
            staleTime: 10 * 60 * 1000 (same as other queries)
        (c) Derive chart data: firmMixViews?.views[granularity] ?? []
            where granularity maps: 'monthly' -&gt; 'monthly', 'quarterly' -&gt; 'quarterly', 'annually' -&gt; 'annually'
    </requirement>

    <requirement id="4">
      WS4 — Replace the 100% stacked bar chart with an absolute dollar stacked bar chart.
      The chart currently uses values like 0.62 (pct) for bar heights. The new chart uses
      asset class dollar amounts as bar heights, stacked to total_aua.

      Chart spec:
        - Recharts BarChart with stackId="mix"
        - dataKey for each Bar: use a computed field (equity_value, fixed_income_value, etc.)
          OR map each FirmMixPeriodPoint to a flat object before passing to BarChart:
          { label, total_aua, equity: pt.equity.value, fixed_income: pt.fixed_income.value, ... }
        - YAxis tickFormatter: formatNumberTo3Digits(value, { unit: '$', includeSign: false })
          (same formatter used in PartnerAnalytics.tsx for NNA bars)
        - domain: [0, 'auto'] — do not hardcode domain={[0, 1]}
        - Colors: same ASSET_CLASS_COLORS already in PartnerAnalytics.tsx

      Tooltip spec (per period bar):
        Line 1: label (period label, bold)
        Line 2: "Total AUA: $X.XXB"
        Divider
        Lines 3-7: each asset class with color dot, label, dollar value, and pct in parens
          e.g., "Equities   $1.02B  (62.0%)"
        Source: use the FirmMixPeriodPoint fields — pt.equity.value and pt.equity.pct * 100
    </requirement>

    <requirement id="5">
      WS5 — ClientDetailPage.tsx: replace the setTimeout stub with a real API call.
      The clientKey param is a relationship_id (confirm by reading how Books tab sets
      the clientKey param in navigation — it should be relationship_id or convertible).
      Call getClientDetail(firmId, clientKey) or the appropriate endpoint that provides
      BooksClientDetailResponse. If a different key mapping is needed, consult ClientsTab.tsx
      to understand how clientKey is set when navigating to ClientDetailPage.
    </requirement>

    <requirement id="6">
      WS5 — Mount MixTimeseriesPanel and ConcentrationPanel in ClientDetailPage.tsx.
      Add selectedAssetClass state (MixAssetClass | null) and mixWindow state (MixWindow).
      Pass relationshipId={clientKey} and firmId={firmId} to both panels.
      The two panels should be shared-state linked: clicking an area in MixTimeseriesPanel
      updates selectedAssetClass, which filters ConcentrationPanel.
    </requirement>

    <requirement id="7">
      WS5 — Remove mock data fallback from MixTimeseriesPanel and ConcentrationPanel.
      Currently: isPlaceholder = !data || data.length === 0; chartData = isPlaceholder ? MOCK_DATA : data
      Change to: show a clean empty state ("No allocation data available for this client")
      instead of rendering MOCK_DATA. The mock data makes it impossible to distinguish
      "no API response" from "real data that happens to look like the mock."
    </requirement>

    <requirement id="8">
      Commit all changes to portal DEV branch:
        git commit --author="0.4.0_DE_ClientPlatform &lt;0.4.0_DE_ClientPlatform@opal.agent&gt;"
      Separate commits for WS4 and WS5 (DE should split these for auditability).
      DE does NOT push — DT pushes portal DEV to remote.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">WS4: firm-level mix chart shows dollar-valued stacked bars, not percentage bars</criterion>
    <criterion id="2">WS4: tooltip shows both $ and % for each asset class</criterion>
    <criterion id="3">WS4: firmMixData useMemo is completely removed from PartnerAnalytics.tsx</criterion>
    <criterion id="4">WS4: when endpoint returns 503 (data not yet built), chart shows appropriate loading/empty state</criterion>
    <criterion id="5">WS5: ClientDetailPage fetches real client data (no more setTimeout stub)</criterion>
    <criterion id="6">WS5: MixTimeseriesPanel and ConcentrationPanel mounted in ClientDetailPage with live data</criterion>
    <criterion id="7">WS5: selecting an asset class in mix panel filters concentration panel</criterion>
    <criterion id="8">WS5: no mock data rendered in either panel — empty state shown when no data</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>WS4 chart implementation requires Lambda endpoint live (task order 004 complete).
      For WS4 development before endpoint is live: implement against the type contract but leave
      the useQuery in loading state. Do not render mock data for the firm chart either.</constraint>
    <constraint>WS5 can begin immediately — the stub removal and panel mounting do not depend on the Lambda</constraint>
    <constraint>DE commits to portal DEV only — DT pushes</constraint>
    <constraint>No emojis in code or comments</constraint>
    <constraint>Issue a task order to 0.4.2_RD_AdvisorIntelligence for any visual/chart work that
      goes beyond wiring (chart color decisions, layout refinements, legend styling)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="ADVI_MIXV2.004" status="pending">
      WS4 requires Lambda endpoint to be live. WS5 has no Lambda dependency.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">WS4 firm mix chart committed to portal DEV</deliverable>
    <deliverable type="commit">WS5 client detail wiring committed to portal DEV</deliverable>
    <deliverable type="document">pod_inventory.xml updated with new API functions and component changes</deliverable>
  </deliverables>
</task_order>
```

### ds-task-order-002----06b-firmadvisor-aggregation--lambda-endpoints-ws3ws6-spec.md

```
<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-03-17-002-firm-advisor-gold-lambda</id>
    <issued_by>0.4.0_DS_ClientPlatform</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-17</date>
    <status>pending</status>
    <project_code>ADVI_MIXV2</project_code>
  </metadata>

  <objective>
    Extend 06b_build_client_mix_timeseries.py to produce two new pre-computed artifacts:
    (1) firm-level period-aggregated mix views with dollar amounts, and (2) per-advisor
    period-aggregated mix views. Add two new Lambda passthrough endpoints to serve them.
    This is WS3 + WS6 from ADVI_MIXV2_PRD.md.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py</file>
      <file action="modify">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
      <file action="modify">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      DEPENDENCY: This task order must not begin until ADVI_MIXV2.001 is committed. The AP gate
      fix must be in place before the firm-level pre-computed views are built — otherwise the
      $60M insurance volatility gets baked into the quarterly snapshots.
    </requirement>

    <requirement id="2">
      Extend 06b per-date processing to also track firm-level market value by asset class.
      In process_date(), the function already returns {rel_id: {mix: {equity: pct, ...}, conc: [...]}}
      per relationship. Modify to ALSO return total_mv per relationship:
        result[rel_id] = {'mix': mix, 'conc': holdings, 'total_mv': total_mv}
      This allows the caller to back-compute dollar amounts: dollar[ac] = pct[ac] * total_mv.
    </requirement>

    <requirement id="3">
      In the full-build and incremental-build paths, accumulate a firm_daily dict:
        firm_daily[date_str] = {equity: $, fixed_income: $, structured_notes: $, cash: $, other: $, total: $}
      Computed as sum across all relationships: for each rel, dollar[ac] = mix[ac] * total_mv.
      Also accumulate advisor_daily in the same loop:
        advisor_daily[advisor_id][date_str] = {same shape as firm_daily entry}
      The advisor→relationship mapping comes from rel_architect_lookup.parquet at
      gold/views/rel_architect_lookup.parquet. Load this at startup alongside static tables.
      If the file does not exist, skip advisor aggregation and log a warning (do not crash).
    </requirement>

    <requirement id="4">
      Implement compute_period_views(daily_dict, data_as_of) function that:
        - Accepts {date_str: {equity: $, ..., total: $}}
        - For each granularity (quarterly, monthly, annually):
          - Groups dates by period key using the same period logic as PartnerAnalytics.tsx
            (quarterly: YYYY-Q#, monthly: YYYY-MM, annually: YYYY)
          - Takes the LAST date in each period as the end-of-period snapshot
          - Computes pct = asset_mv / total for that snapshot
        - Returns {"quarterly": [...], "monthly": [...], "annually": [...]}
      Each period entry shape:
        {period, label, end_date, total_aua, equity: {value, pct}, fixed_income: {value, pct},
         structured_notes: {value, pct}, cash: {value, pct}, other: {value, pct}}
      All pct values are 0-1. Values are floats rounded to 2 decimal places.
      Period labels follow the same format as PartnerAnalytics.tsx getPeriodInfo():
        quarterly: "Q4 '24", monthly: "Oct '24", annually: "2024"
    </requirement>

    <requirement id="5">
      Write firm mix views to S3:
        gold/firm_mix_views.json
      Shape:
        {generated_at, data_as_of, firm_id: "49financial", views: {quarterly, monthly, annually}}
      Write this at the end of the build (full or incremental), after the watermark.
    </requirement>

    <requirement id="6">
      Write per-advisor mix views to S3:
        gold/advisors/{advisor_id}/mix.json  (one per advisor)
      Shape:
        {generated_at, data_as_of, advisor_id, advisor_name, views: {quarterly, monthly, annually}}
      advisor_name comes from the rel_architect_lookup.parquet canonical_name column (or advisor_id
      reformatted if canonical_name is absent). Write in parallel using the existing WRITE_WORKERS pool.
      Only write advisors that have at least one period entry in the annual view (skip advisors
      with no funded relationship data).
    </requirement>

    <requirement id="7">
      Add two Lambda endpoints to opal-partners-data:

      (a) GET /api/scoped/partners/books/firm/mix-views?firmId=xxx
          -> serve_s3_json(bucket, 'gold/firm_mix_views.json')
          Route: entity_type == 'firm', action == 'mix-views'
          Validator: entity_type == 'firm' and entity_id == 'all' (same as composition endpoint)

      (b) GET /api/shared/advisor-intelligence/advisors/{id}/mix-views?firmId=xxx
          -> serve_s3_json(bucket, f'gold/advisors/{advisor_id}/mix.json')
          Route: add elif for this path in the shared/advisor-intelligence branch
          Validator: reuse existing _validate_advisor_id check from handle_advisor_book
    </requirement>

    <requirement id="8">
      Update data_contract.xml with new output artifacts:
        - gold/firm_mix_views.json: schema, written_by 06b, served_by new Lambda endpoint
        - gold/advisors/{id}/mix.json: schema, written_by 06b, served_by new Lambda endpoint
    </requirement>

    <requirement id="9">
      Commit to CLOUD with:
        git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;"
      Two commits:
        (a) "0.4.0_DS_ClientPlatform: 06b firm + advisor mix period views (WS3+WS6)"
        (b) "0.4.0_DS_ClientPlatform: opal-partners-data -- firm/mix-views + advisor/mix-views endpoints"
      Update data_contract.xml in commit (a).
      Write DevOps brief at docs/briefs/devops-brief-mixv2-002.md:
        - 06b: run sequence (incremental is sufficient after 001 full run), expected output sizes
        - Lambda: endpoints to add, Terraform plan expected (no new resources, code change only)
        - Verification steps: check S3 for firm_mix_views.json, curl test both endpoints
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">gold/firm_mix_views.json exists in S3 with correct shape after 06b run</criterion>
    <criterion id="2">gold/advisors/{id}/mix.json exists for all 19 active advisors</criterion>
    <criterion id="3">Each period entry pct values sum to 1.0 ± 0.001</criterion>
    <criterion id="4">Lambda endpoint GET /api/scoped/partners/books/firm/mix-views returns 200 with views.quarterly populated</criterion>
    <criterion id="5">Lambda endpoint GET /api/shared/advisor-intelligence/advisors/{id}/mix-views returns 200</criterion>
    <criterion id="6">data_contract.xml updated with new artifacts</criterion>
    <criterion id="7">DevOps brief at docs/briefs/devops-brief-mixv2-002.md is actionable for AE + DT</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT begin until ADVI_MIXV2.001 is committed (AP gate fix must be in place)</constraint>
    <constraint>Do NOT deploy — AE deploys 06b (task order 003), DT deploys Lambda (task order 004)</constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13)</constraint>
    <constraint>Period label format MUST match PartnerAnalytics.tsx getPeriodInfo() output exactly — DE relies on this for direct rendering without transformation</constraint>
    <constraint>If rel_architect_lookup.parquet is missing, skip advisor aggregation with a warning — do not crash the entire 06b run</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MIXV2.001" status="pending">
      AP gate fix must be committed before this task order begins
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">06b extended with firm + advisor aggregation, committed to CLOUD</deliverable>
    <deliverable type="commit">Lambda endpoints committed to CLOUD</deliverable>
    <deliverable type="commit">data_contract.xml updated</deliverable>
    <deliverable type="document">docs/briefs/devops-brief-mixv2-002.md</deliverable>
  </deliverables>
</task_order>
```

---

## End of Context

(Full session logs available via tool: read files under org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-03-17/, org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-03-16/, org/tier3_junior/0.4.2_RD_AdvisorIntelligence/logs/2026-03-16/ if needed.)

