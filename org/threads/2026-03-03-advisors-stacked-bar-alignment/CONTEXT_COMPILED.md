# Thread Context -- Pattern 0 alignment: Advisors tab stacked bar (Stream A3)

**Thread ID:** 2026-03-03-advisors-stacked-bar-alignment
**Created by:** 2.0.0_SA_COO
**Created at:** 2026-03-03T19:45:13Z

---

## Participants

### 0.4.0_DS_ClientPlatform

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

This is a Pattern 0 pre-implementation alignment thread for Stream A3 of the AdvisorIntelligence completion PRD.

Stream A3: The Advisors tab currently shows rolling NNA with 30d/90d/1Y window toggles as line charts. This is being replaced with two views:
  (1) Stacked bar chart: one bar per advisor showing inflows, outflows, NNA net — sorted by NNA — for period aggregations (QTD/YTD/1Y/3Y/Max).
  (2) 1-year rolling line chart: daily 1Y trailing NNA per advisor, x-axis window controlled by period toggle (3Y/Max supported).

Script 10 currently produces trailing rolling NNA at 30d/90d/1Y windows. It needs to be updated or supplemented to produce period-anchored aggregations and extended rolling series.

Knowledge source: 0.4.0_DS_ClientPlatform (what script 10 currently computes, what nna_aua_by_advisor.parquet contains, what period-anchored aggregations are feasible).
Interface specifier: 0.4.0_DE_ClientPlatform (TypeScript shape needed for both views).
Layout specifier: 0.4.2_RD_AdvisorIntelligence (chart implementation constraints — Recharts vs Nivo, how negative outflows should be encoded in the bar data, what fields the tooltip needs).

Deliverable: agreed JSON output schema for advisor_rolling_flows.json replacement/additions, agreed TypeScript interface names, agreed encoding for negative outflow values in the bar chart data. The final turn must contain this as a structured contract.


### advisor-intelligence-api-endpoints.ts

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
export async function getPartnerAnalytics(): Promise<PartnerAnalyticsResponse> {
  return await apiRequest<PartnerAnalyticsResponse>('/api/scoped/advisor-intelligence/partner_analytics/header_metrics.json')
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
```

### advisorintelligence-completion-prd--section-4c-rolling-flows-new-model.md

```
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
```

### advisorintelligence-typescript-types.ts

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
```

### advisorstab-component-current-consumer.tsx

```
/**
 * Advisors Tab - Advisor Intelligence
 *
 * Single Architects/Implementors toggle controls entire tab.
 * Two independent control groups:
 *
 * 1. Rolling Flows (time series) -- metric toggle (NNA/Inflows/Outflows) + window (30d/90d/1Y)
 * 2. Leaderboard (table) -- trailing window (3M/6M/1Y/2Y/3Y)
 *
 * Layout:
 * +------------------------------------------------------------+
 * |  [Architects] [Implementors]                                |
 * +------------------------------------------------------------+
 * |  TOP 3 HIGHLIGHTS (for selected role, leaderboard window)   |
 * +------------------------------------------------------------+
 * |  ROLLING FLOWS  [NNA|Inflows|Outflows] [30d|90d|1Y]        |
 * |  LineChart -- one line per selected advisor                 |
 * +------------------------------------------------------------+
 * |  LEADERBOARD  [3M|6M|1Y|2Y|3Y]         Search [_______]   |
 * |  Click row to toggle chart line                             |
 * +------------------------------------------------------------+
 */

import { useState, useEffect, useMemo } from 'react'
import {
  LineChart as RechartsLineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts'
import { Panel } from '@/ui/components/panels'
import { LoadingInline } from '@/components/LoadingSpinner'
import {
  ArrowUpRight,
  ArrowDownRight,
  ChevronUp,
  ChevronDown,
  Trophy,
  TrendingUp,
  Search,
  Users,
} from 'lucide-react'
import { formatCurrency, formatNumberTo3Digits } from '@/lib/universalNumberFormatter'
import { getArchitectLeaderboard, getImplementorLeaderboard, getAdvisorRollingFlows } from '@/api/endpoints/advisor-intelligence'
import type {
  LeaderboardResponse,
  LeaderboardEntry,
  ChartWindowOption,
  AdvisorRollingFlowsResponse,
  RollingFlowsWindowKey,
  RollingFlowsDataPoint,
  AdvisorRollingSeries,
} from '../types'

// ============================================================================
// TYPES & CONSTANTS
// ============================================================================

type AdvisorRole = 'architects' | 'implementors'
type SortField = 'name' | 'total_aua' | 'nna' | 'aua_growth_pct' | 'new_clients'
type SortDirection = 'asc' | 'desc'
type FlowsMetric = 'nna' | 'inflows' | 'outflows'

const LEADERBOARD_WINDOW_OPTIONS: { value: ChartWindowOption; label: string }[] = [
  { value: '3M', label: '3M' },
  { value: '6M', label: '6M' },
  { value: '1Y', label: '1Y' },
  { value: '2Y', label: '2Y' },
  { value: '3Y', label: '3Y' },
]

const FLOWS_METRIC_OPTIONS: { value: FlowsMetric; label: string }[] = [
  { value: 'nna', label: 'NNA' },
  { value: 'inflows', label: 'Inflows' },
  { value: 'outflows', label: 'Outflows' },
]

const FLOWS_WINDOW_OPTIONS: { value: RollingFlowsWindowKey; label: string }[] = [
  { value: '30d', label: '30d' },
  { value: '90d', label: '90d' },
  { value: '1Y', label: '1Y' },
]

// Fallback colors for chart lines when no pre-assigned color
const LINE_COLORS = [
  '#5e72e4', '#2dce89', '#fb6340', '#f5365c', '#11cdef',
  '#8965e0', '#ffd600', '#ff8d72', '#5603ad', '#1aae6f',
]

// ============================================================================
// SUB-PANEL COMPONENTS
// ============================================================================

function SubPanel({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={`bg-white/5 rounded-lg border border-white/10 overflow-hidden ${className}`}>
      {children}
    </div>
  )
}

function SubPanelHeader({ title, actions, className = '' }: { title: string; actions?: React.ReactNode; className?: string }) {
  return (
    <div className={`px-4 py-2.5 bg-[hsl(var(--bg-header))] flex items-center justify-between rounded-t-lg ${className}`}>
      <h3 className="text-xs font-semibold text-white uppercase tracking-wide">{title}</h3>
      {actions}
    </div>
  )
}

function ToggleGroup<T extends string>({ options, value, onChange, size = 'sm' }: {
  options: { value: T; label: string }[]
  value: T
  onChange: (v: T) => void
  size?: 'sm' | 'xs'
}) {
  const textSize = size === 'xs' ? 'text-[10px]' : 'text-xs'
  const padding = size === 'xs' ? 'px-1.5 py-0.5' : 'px-2 py-1'
  return (
    <div className="flex gap-0.5 bg-white/10 rounded-lg p-0.5">
      {options.map((opt) => (
        <button
          key={opt.value}
          onClick={() => onChange(opt.value)}
          className={`${padding} ${textSize} font-medium rounded-md transition-colors ${
            value === opt.value
              ? 'bg-white/20 text-white'
              : 'text-white/50 hover:text-white hover:bg-white/10'
          }`}
        >
          {opt.label}
        </button>
      ))}
    </div>
  )
}

// ============================================================================
// PROPS
// ============================================================================

interface AdvisorsTabProps {
  firmId: string
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export function AdvisorsTab({ firmId }: AdvisorsTabProps) {
  // Data state
  const [isLoading, setIsLoading] = useState(true)
  const [architectData, setArchitectData] = useState<LeaderboardResponse | null>(null)
  const [implementorData, setImplementorData] = useState<LeaderboardResponse | null>(null)
  const [flowsData, setFlowsData] = useState<AdvisorRollingFlowsResponse | null>(null)
  const [flowsLoading, setFlowsLoading] = useState(true)

  // Tab-wide toggle: architects or implementors
  const [role, setRole] = useState<AdvisorRole>('architects')

  // Control group 1: Rolling Flows time series
  const [flowsMetric, setFlowsMetric] = useState<FlowsMetric>('nna')
  const [flowsWindow, setFlowsWindow] = useState<RollingFlowsWindowKey>('90d')
  const [selectedAdvisorIds, setSelectedAdvisorIds] = useState<Set<string>>(new Set())

  // Control group 2: Leaderboard table
  const [leaderboardWindow, setLeaderboardWindow] = useState<ChartWindowOption>('1Y')
  const [searchQuery, setSearchQuery] = useState('')

  // Fetch leaderboard data
  useEffect(() => {
    if (!firmId) {
      setIsLoading(false)
      return
    }

    setIsLoading(true)

    Promise.all([
      getArchitectLeaderboard(),
      getImplementorLeaderboard(),
    ])
      .then(([architects, implementors]) => {
        setArchitectData(architects)
        setImplementorData(implementors)
        setIsLoading(false)
      })
      .catch(error => {
        console.error('[AdvisorsTab] Failed to load leaderboard:', error)
        setArchitectData(null)
        setImplementorData(null)
        setIsLoading(false)
      })
  }, [firmId])

  // Fetch rolling flows data (separate fetch -- may 404 if not yet deployed)
  useEffect(() => {
    if (!firmId) {
      setFlowsLoading(false)
      return
    }

    setFlowsLoading(true)

    getAdvisorRollingFlows()
      .then((data) => {
        setFlowsData(data)
        setFlowsLoading(false)

        // Auto-select top 5 advisors from the current role
        const advisors = role === 'architects' ? data.architects : data.implementors
        const top5Ids = advisors.slice(0, 5).map(a => a.advisor_id)
        setSelectedAdvisorIds(new Set(top5Ids))
      })
      .catch(error => {
        console.error('[AdvisorsTab] Rolling flows not available:', error)
        setFlowsData(null)
        setFlowsLoading(false)
      })
  }, [firmId]) // eslint-disable-line react-hooks/exhaustive-deps

  // Update selected advisors when role changes and flows data exists
  useEffect(() => {
    if (!flowsData) return
    const advisors = role === 'architects' ? flowsData.architects : flowsData.implementors
    const top5Ids = advisors.slice(0, 5).map(a => a.advisor_id)
    setSelectedAdvisorIds(new Set(top5Ids))
  }, [role, flowsData])

  // Active leaderboard data based on role toggle
  const activeLeaderboard = role === 'architects' ? architectData : implementorData

  // Active rolling flows series based on role
  const activeFlowsSeries: AdvisorRollingSeries[] = useMemo(() => {
    if (!flowsData) return []
    return role === 'architects' ? flowsData.architects : flowsData.implementors
  }, [flowsData, role])

  // Toggle advisor selection for chart
  const toggleAdvisor = (advisorId: string) => {
    setSelectedAdvisorIds(prev => {
      const next = new Set(prev)
      if (next.has(advisorId)) {
        next.delete(advisorId)
      } else {
        next.add(advisorId)
      }
      return next
    })
  }

  if (!firmId) {
    return (
      <Panel variant="chart">
        <div className="py-12 text-center">
          <p className="text-white/60">Select a partner to view advisors</p>
        </div>
      </Panel>
    )
  }

  if (isLoading) {
    return <LoadingInline className="py-12" />
  }

  return (
    <Panel variant="chart" className="p-0">
      {/* Tab-wide Role Toggle */}
      <div className="flex items-center justify-between p-4 border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className="flex gap-0.5 bg-white/10 rounded-lg p-0.5">
            {(['architects', 'implementors'] as AdvisorRole[]).map((r) => (
              <button
                key={r}
                onClick={() => { setRole(r); setSearchQuery('') }}
                className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
                  role === r
                    ? 'bg-[hsl(var(--primary))] text-white'
                    : 'text-white/60 hover:text-white hover:bg-white/10'
                }`}
              >
                {r.charAt(0).toUpperCase() + r.slice(1)}
              </button>
            ))}
          </div>
        </div>

        <div className="text-xs text-white/40">
          {activeLeaderboard?.windows?.[leaderboardWindow]?.entry_count ?? 0} {role}
        </div>
      </div>

      {/* Top 3 Highlights */}
      <Top3Highlights data={activeLeaderboard} window={leaderboardWindow} role={role} />

      {/* Rolling Flows Time Series */}
      <div className="p-4 pb-0">
        <SubPanel>
          <SubPanelHeader
            title="Rolling Flows"
            actions={
              <div className="flex items-center gap-3">
                <ToggleGroup options={FLOWS_METRIC_OPTIONS} value={flowsMetric} onChange={setFlowsMetric} size="xs" />
                <div className="w-px h-4 bg-white/10" />
                <ToggleGroup options={FLOWS_WINDOW_OPTIONS} value={flowsWindow} onChange={setFlowsWindow} size="xs" />
              </div>
            }
          />
          <RollingFlowsChart
            series={activeFlowsSeries}
            selectedIds={selectedAdvisorIds}
            metric={flowsMetric}
            window={flowsWindow}
            loading={flowsLoading}
          />
        </SubPanel>
      </div>

      {/* Leaderboard Table */}
      <div className="p-4">
        <SubPanel>
          <SubPanelHeader
            title={`${role === 'architects' ? 'Architect' : 'Implementor'} Leaderboard`}
            actions={
              <div className="flex items-center gap-3">
                <ToggleGroup options={LEADERBOARD_WINDOW_OPTIONS} value={leaderboardWindow} onChange={setLeaderboardWindow} size="xs" />
                <div className="w-px h-4 bg-white/10" />
                <div className="flex items-center gap-2 bg-white/5 border border-white/10 rounded-md px-2 py-1">
                  <Search size={12} className="text-white/40" />
                  <input
                    type="text"
                    placeholder="Search..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="bg-transparent text-xs text-white placeholder-white/40 outline-none w-24"
                  />
                </div>
              </div>
            }
          />
          <LeaderboardTable
            data={activeLeaderboard?.windows?.[leaderboardWindow]?.entries ?? []}
            searchQuery={searchQuery}
            selectedAdvisorIds={selectedAdvisorIds}
            onToggleAdvisor={toggleAdvisor}
            flowsSeries={activeFlowsSeries}
          />
        </SubPanel>
      </div>
    </Panel>
  )
}

// ============================================================================
// ROLLING FLOWS TIME SERIES
// ============================================================================

interface RollingFlowsChartProps {
  series: AdvisorRollingSeries[]
  selectedIds: Set<string>
  metric: FlowsMetric
  window: RollingFlowsWindowKey
  loading: boolean
}

function RollingFlowsChart({ series, selectedIds, metric, window, loading }: RollingFlowsChartProps) {
  if (loading) {
    return <LoadingInline className="py-12" />
  }

  if (!series || series.length === 0) {
    return (
      <div className="flex items-center justify-center h-[250px]">
        <div className="flex flex-col items-center gap-3 text-center">
          <Users size={32} className="text-white/20" />
          <div>
            <p className="text-sm text-white/40">Rolling flows not yet available</p>
            <p className="text-xs text-white/30 mt-1">Data will appear after the next pipeline run</p>
          </div>
        </div>
      </div>
    )
  }

  // Filter to selected advisors
  const selectedSeries = series.filter(s => selectedIds.has(s.advisor_id))

  if (selectedSeries.length === 0) {
    return (
      <div className="flex items-center justify-center h-[250px]">
        <p className="text-sm text-white/40">Click advisor rows below to add lines to the chart</p>
      </div>
    )
  }

  // Build unified date array from all selected advisors
  const dateMap = new Map<string, Record<string, number>>()

  selectedSeries.forEach(advisor => {
    const points: RollingFlowsDataPoint[] = advisor.series[window] ?? []
    points.forEach(pt => {
      if (!dateMap.has(pt.date)) {
        dateMap.set(pt.date, {})
      }
      const row = dateMap.get(pt.date)!
      row[advisor.advisor_id] = pt[metric]
    })
  })

  const chartData = Array.from(dateMap.entries())
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([date, values]) => ({ date, ...values }))

  // Build color map from series order
  const colorMap: Record<string, string> = {}
  series.forEach((s, i) => {
    colorMap[s.advisor_id] = LINE_COLORS[i % LINE_COLORS.length]
  })

  // Format date for X axis
  const formatDate = (d: string) => {
    const date = new Date(d + 'T00:00:00')
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  }

  return (
    <div className="p-4 h-[280px]">
      <ResponsiveContainer width="100%" height="100%">
        <RechartsLineChart data={chartData} margin={{ top: 5, right: 10, left: 10, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
          <XAxis
            dataKey="date"
            tickFormatter={formatDate}
            tick={{ fill: 'rgba(255,255,255,0.4)', fontSize: 10 }}
            axisLine={{ stroke: 'rgba(255,255,255,0.1)' }}
            tickLine={false}
            minTickGap={60}
          />
          <YAxis
            tickFormatter={(v: number) => formatNumberTo3Digits(v, { unit: '$', includeSign: false })}
            tick={{ fill: 'rgba(255,255,255,0.4)', fontSize: 10 }}
            axisLine={false}
            tickLine={false}
            width={65}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'hsl(var(--bg-panel))',
              border: '1px solid rgba(255,255,255,0.1)',
              borderRadius: '8px',
              fontSize: '11px',
            }}
            labelFormatter={(label) => formatDate(String(label))}
            formatter={(value: number | undefined, name: string | undefined) => {
              const numericValue = typeof value === 'number' ? value : 0
              const advisor = selectedSeries.find(s => s.advisor_id === name)
              return [formatCurrency(numericValue), advisor?.advisor_name ?? (name ?? 'Unknown')]
            }}
          />
          {selectedSeries.map((advisor) => (
            <Line
              key={advisor.advisor_id}
              dataKey={advisor.advisor_id}
              name={advisor.advisor_id}
              stroke={colorMap[advisor.advisor_id] || '#5e72e4'}
              strokeWidth={1.5}
              dot={false}
              activeDot={{ r: 3 }}
              connectNulls
            />
          ))}
        </RechartsLineChart>
      </ResponsiveContainer>
    </div>
  )
}

// ============================================================================
// TOP 3 HIGHLIGHTS
// ============================================================================

interface Top3HighlightsProps {
  data: LeaderboardResponse | null
  window: ChartWindowOption
  role: AdvisorRole
}

function Top3Highlights({ data, window, role }: Top3HighlightsProps) {
  const top3 = data?.windows?.[window]?.entries?.slice(0, 3) ?? []

  if (top3.length === 0) return null

  const rankStyles: Record<number, { bg: string; border: string; badge: string }> = {
    1: {
      bg: 'bg-gradient-to-br from-amber-500/10 to-amber-600/5',
      border: 'border-amber-500/30',
      badge: 'bg-amber-500/20 text-amber-400 border-amber-500/40',
    },
    2: {
      bg: 'bg-gradient-to-br from-slate-400/10 to-slate-500/5',
      border: 'border-slate-400/30',
      badge: 'bg-slate-400/20 text-slate-300 border-slate-400/40',
    },
    3: {
      bg: 'bg-gradient-to-br from-orange-600/10 to-orange-700/5',
      border: 'border-orange-600/30',
      badge: 'bg-orange-600/20 text-orange-400 border-orange-600/40',
    },
  }

  return (
    <div className="p-4 pb-0">
      <SubPanel>
        <SubPanelHeader
          title="Top Performers"
          actions={
            <div className="flex items-center gap-2">
              <Trophy size={14} className="text-amber-400" />
              <span className="text-[10px] text-white/40">
                By Net New Assets ({window}) &middot; {role === 'architects' ? 'Architects' : 'Implementors'}
              </span>
            </div>
          }
        />
        <div className="p-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {top3.map((entry, idx) => {
              const rank = idx + 1
              const style = rankStyles[rank] || rankStyles[3]

              return (
                <div
                  key={entry.name}
                  className={`relative rounded-lg border ${style.border} ${style.bg} p-4 transition-all hover:scale-[1.02]`}
                >
                  <div className={`absolute -top-2 -left-2 w-7 h-7 rounded-full ${style.badge} border flex items-center justify-center font-bold text-sm`}>
                    {rank}
                  </div>

                  <div className="ml-4">
                    <h4 className="font-semibold text-white text-sm truncate mb-3">
                      {entry.name}
                    </h4>

                    <div className="mb-2">
                      <p className={`text-xl font-bold ${entry.nna >= 0 ? 'text-[hsl(var(--success))]' : 'text-[hsl(var(--destructive))]'}`}>
                        {entry.nna >= 0 ? '+' : ''}{formatNumberTo3Digits(entry.nna, { unit: '$', includeSign: false })}
                      </p>
                      <p className="text-[10px] text-white/40 uppercase tracking-wide">Net New Assets</p>
                    </div>

                    <div className="flex items-center gap-4 pt-2 border-t border-white/5">
                      <div className="flex items-center gap-1">
                        {entry.aua_growth_pct >= 0 ? (
                          <TrendingUp size={12} className="text-[hsl(var(--success))]" />
                        ) : (
                          <ArrowDownRight size={12} className="text-[hsl(var(--destructive))]" />
                        )}
                        <span className={`text-xs font-medium ${entry.aua_growth_pct >= 0 ? 'text-[hsl(var(--success))]' : 'text-[hsl(var(--destructive))]'}`}>
                          {entry.aua_growth_pct >= 0 ? '+' : ''}{entry.aua_growth_pct.toFixed(1)}%
                        </span>
                      </div>

                      <div className="text-xs text-white/50">
                        <span className="font-medium text-white/70">{entry.new_clients}</span> new clients
                      </div>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </SubPanel>
    </div>
  )
}

// ============================================================================
// LEADERBOARD TABLE
// ============================================================================

function SortIcon({ field, sortField, sortDirection }: { field: SortField; sortField: SortField; sortDirection: SortDirection }) {
  if (sortField !== field) return null
  return sortDirection === 'asc' ? <ChevronUp size={12} /> : <ChevronDown size={12} />
}

interface LeaderboardTableProps {
  data: LeaderboardEntry[]
  searchQuery: string
  selectedAdvisorIds: Set<string>
  onToggleAdvisor: (advisorId: string) => void
  flowsSeries: AdvisorRollingSeries[]
}

function LeaderboardTable({ data, searchQuery, selectedAdvisorIds, onToggleAdvisor, flowsSeries }: LeaderboardTableProps) {
  const [sortField, setSortField] = useState<SortField>('nna')
  const [sortDirection, setSortDirection] = useState<SortDirection>('desc')

  if (!data || data.length === 0) {
    return (
      <div className="p-8 text-center text-white/50">
        No data available
      </div>
    )
  }

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDirection('desc')
    }
  }

  // Filter by search
  const filteredData = searchQuery.trim()
    ? data.filter(entry => entry.name.toLowerCase().includes(searchQuery.toLowerCase()))
    : data

  const sortedData = [...filteredData].sort((a, b) => {
    const aVal = a[sortField]
    const bVal = b[sortField]
    if (typeof aVal === 'string' && typeof bVal === 'string') {
      return sortDirection === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal)
    }
    return sortDirection === 'asc' ? Number(aVal) - Number(bVal) : Number(bVal) - Number(aVal)
  }).map((item, idx) => ({ ...item, rank: idx + 1 }))

  // Build a name->advisorId lookup from flows series
  const nameToId = new Map<string, string>()
  flowsSeries.forEach(s => nameToId.set(s.advisor_name, s.advisor_id))

  return (
    <div className="overflow-y-auto overflow-x-hidden scrollbar-none" style={{ maxHeight: 500 }}>
      <table className="w-full text-xs table-fixed">
        <thead className="bg-[hsl(var(--bg-header))] sticky top-0 z-10">
          <tr className="border-b border-white/20">
            <th className="w-10 px-2 py-2 text-left text-[10px] font-semibold text-white/80 uppercase tracking-wider">
              #
            </th>
            <th
              className="w-[28%] px-2 py-2 text-left text-[10px] font-semibold text-white/80 uppercase tracking-wider cursor-pointer hover:text-white"
              onClick={() => handleSort('name')}
            >
              <span className="flex items-center gap-1">
                Name <SortIcon field="name" sortField={sortField} sortDirection={sortDirection} />
              </span>
            </th>
            <th
              className="w-[18%] px-2 py-2 text-right text-[10px] font-semibold text-white/80 uppercase tracking-wider cursor-pointer hover:text-white"
              onClick={() => handleSort('total_aua')}
            >
              <span className="flex items-center justify-end gap-1">
                AUA <SortIcon field="total_aua" sortField={sortField} sortDirection={sortDirection} />
              </span>
            </th>
            <th
              className="w-[18%] px-2 py-2 text-right text-[10px] font-semibold text-white/80 uppercase tracking-wider cursor-pointer hover:text-white"
              onClick={() => handleSort('nna')}
            >
              <span className="flex items-center justify-end gap-1">
                NNA <SortIcon field="nna" sortField={sortField} sortDirection={sortDirection} />
              </span>
            </th>
            <th
              className="w-[16%] px-2 py-2 text-right text-[10px] font-semibold text-white/80 uppercase tracking-wider cursor-pointer hover:text-white"
              onClick={() => handleSort('aua_growth_pct')}
            >
              <span className="flex items-center justify-end gap-1">
                Growth <SortIcon field="aua_growth_pct" sortField={sortField} sortDirection={sortDirection} />
              </span>
            </th>
            <th
              className="w-[10%] px-2 py-2 text-right text-[10px] font-semibold text-white/80 uppercase tracking-wider cursor-pointer hover:text-white"
              onClick={() => handleSort('new_clients')}
            >
              <span className="flex items-center justify-end gap-1">
                Clients <SortIcon field="new_clients" sortField={sortField} sortDirection={sortDirection} />
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          {sortedData.map((entry) => {
            const advisorId = nameToId.get(entry.name)
            const isSelected = advisorId ? selectedAdvisorIds.has(advisorId) : false
            const lineColor = advisorId ? LINE_COLORS[flowsSeries.findIndex(s => s.advisor_id === advisorId) % LINE_COLORS.length] : undefined

            return (
              <tr
                key={entry.name}
                onClick={() => advisorId && onToggleAdvisor(advisorId)}
                className={`border-b border-white/5 hover:bg-white/5 transition-colors cursor-pointer ${
                  isSelected ? 'bg-white/[0.03]' : ''
                }`}
              >
                <td className="w-10 px-2 py-2">
                  <div className="flex items-center gap-1">
                    {isSelected && lineColor && (
                      <div className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ backgroundColor: lineColor }} />
                    )}
                    <RankBadge rank={entry.rank} />
                  </div>
                </td>
                <td className="w-[28%] px-2 py-2">
                  <span className="font-medium text-white truncate block">{entry.name}</span>
                </td>
                <td className="w-[18%] px-2 py-2 text-right text-white/70">
                  {formatCurrency(entry.total_aua)}
                </td>
                <td className="w-[18%] px-2 py-2 text-right">
                  <span className={entry.nna >= 0 ? 'text-[hsl(var(--success))]' : 'text-[hsl(var(--destructive))]'}>
                    {entry.nna >= 0 ? '+' : ''}{formatNumberTo3Digits(entry.nna, { unit: '$', includeSign: false })}
                  </span>
                </td>
                <td className="w-[16%] px-2 py-2 text-right">
                  <span className="inline-flex items-center justify-end gap-0.5">
                    {entry.aua_growth_pct >= 0 ? (
                      <ArrowUpRight size={11} className="text-[hsl(var(--success))]" />
                    ) : (
                      <ArrowDownRight size={11} className="text-[hsl(var(--destructive))]" />
                    )}
                    <span className={entry.aua_growth_pct >= 0 ? 'text-[hsl(var(--success))]' : 'text-[hsl(var(--destructive))]'}>
                      {entry.aua_growth_pct >= 0 ? '+' : ''}{entry.aua_growth_pct.toFixed(1)}%
                    </span>
                  </span>
                </td>
                <td className="w-[10%] px-2 py-2 text-right text-white/70">
                  {entry.new_clients}
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
      {searchQuery && sortedData.length === 0 && (
        <div className="p-6 text-center text-white/40 text-sm">
          No results for &quot;{searchQuery}&quot;
        </div>
      )}
    </div>
  )
}

function RankBadge({ rank }: { rank: number }) {
  const colors: Record<number, string> = {
    1: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
    2: 'bg-gray-400/20 text-gray-300 border-gray-400/30',
    3: 'bg-orange-600/20 text-orange-400 border-orange-600/30',
  }
  const defaultColor = 'bg-white/5 text-white/50 border-white/10'

  return (
    <span className={`inline-flex items-center justify-center w-5 h-5 rounded-full text-[10px] font-bold border ${colors[rank] || defaultColor}`}>
      {rank}
    </span>
  )
}
```

### script-10--current-advisor-rolling-flows-generator.py

```
#!/usr/bin/env python3
"""
Generate Advisor Rolling Flows — advisor_rolling_flows.json

Produces the portal-ready JSON at:
    s3://opal-data-bd/gold/advisor_rolling_flows.json

Served via CloudFront: shared-advisor-router:3 rewrites
    /api/scoped/advisor-intelligence/advisor_rolling_flows.json -> /gold/advisor_rolling_flows.json

Two views for the Advisors tab on Advisor Intelligence:

  1. NNA Summary (default view — donut chart)
     MTD, QTD, YTD NNA per advisor as donut-ready segments.
     Shows which advisors are driving net new asset growth in the
     current month, quarter, and year-to-date.

  2. Rolling Flows (time series view)
     Per-advisor rolling NNA, Inflows, and Outflows for trailing
     30-day, 90-day, and 1-year windows. Each data point is a
     cumulative diff: roll_val[D] = cum_val[D] - cum_val[D - W_days].

Data sources (from s3://opal-data-bd):
    gold/views/nna_aua_by_advisor.parquet      -- daily cum_inflows/cum_outflows/nna per architect
    gold/client_performance.parquet             -- household daily cumulative flows
    gold/accounts_dimension_latest.parquet      -- relationship -> implementor mapping

Architects: pre-aggregated in nna_aua_by_advisor.parquet.
Implementors: no pre-built view exists — computed on-the-fly by assigning the
modal implementor per relationship from accounts_dimension_latest, then
aggregating client_performance to (date, implementor) grain.

Output JSON shape:
    {
      "generated_at": "...",
      "data_as_of": "YYYY-MM-DD",
      "firm_id": "49financial",
      "summary": {
        "architects": {
          "mtd": { "period_start": "...", "period_end": "...", "total_nna": 0, "segments": [...] },
          "qtd": { ... },
          "ytd": { ... }
        },
        "implementors": { "mtd": {...}, "qtd": {...}, "ytd": {...} }
      },
      "architects": [
        {
          "advisor_name": "Jane Smith",
          "advisor_id": "arch_jane_smith",
          "series": {
            "30d": [{"date": "...", "nna": 0, "inflows": 0, "outflows": 0}, ...],
            "90d": [...],
            "1Y":  [...]
          }
        }
      ],
      "implementors": [...]
    }

Usage:
    python 10_generate_advisor_rolling_flows.py               # local test
    python 10_generate_advisor_rolling_flows.py --upload      # write to S3
    python 10_generate_advisor_rolling_flows.py --dry-run     # compute only, no write
    python 10_generate_advisor_rolling_flows.py -v            # verbose

Author: Data Scientist (Claude)
Date: 2026-02-27
"""

import argparse
import json
import re
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

INPUT_BUCKET  = 'opal-data-bd'
OUTPUT_BUCKET = 'opal-data-bd'
OUTPUT_KEY    = 'gold/advisor_rolling_flows.json'
DEFAULT_LOCAL_OUTPUT = './gold/advisor_rolling_flows.json'

FIRM_ID = '49financial'

# Rolling windows: label -> trailing days
WINDOWS = {'30d': 30, '90d': 90, '1Y': 365}

# Donut chart colors (matches ADV palette in script 09)
DONUT_COLORS = ['#5e72e4', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6',
                '#06B6D4', '#84CC16', '#F97316']
OTHER_COLOR  = '#757575'
MAX_DONUT_SEGMENTS = 8

MODAL_NULLS = frozenset({
    '', 'none', 'nan', 'unassigned', 'unknown', 'n/a',
    'no architect value assigned', 'no implementor value assigned', 'no state',
})

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def _read_parquet(key: str, columns: list = None, verbose: bool = False) -> pd.DataFrame:
    s3 = boto3.client('s3', region_name='us-east-1')
    if verbose:
        print(f"  Loading s3://{INPUT_BUCKET}/{key}")
    resp = s3.get_object(Bucket=INPUT_BUCKET, Key=key)
    kwargs = {'columns': columns} if columns else {}
    df = pd.read_parquet(BytesIO(resp['Body'].read()), **kwargs)
    if verbose:
        print(f"    {len(df):,} rows")
    return df


def load_data(verbose: bool = False) -> tuple:
    """
    Load 3 gold tables needed for this script.
    Returns: (adv_ts, client_perf, acct_dim)

    adv_ts:       nna_aua_by_advisor (pre-aggregated architect daily flows)
    client_perf:  client_performance (household daily cumulative flows)
    acct_dim:     accounts_dimension_latest (for implementor assignment)
    """
    print("Loading gold tables from S3...")

    adv_ts = _read_parquet(
        'gold/views/nna_aua_by_advisor.parquet',
        columns=['date', 'architect', 'total_aua', 'cum_inflows', 'cum_outflows', 'nna',
                 'num_relationships'],
        verbose=verbose
    )
    adv_ts['date'] = pd.to_datetime(adv_ts['date']).astype('datetime64[ns]')

    client_perf = _read_parquet(
        'gold/client_performance.parquet',
        columns=['date', 'relationship_id', 'total_aua', 'cum_inflows', 'cum_outflows', 'nna'],
        verbose=verbose
    )
    client_perf['date'] = pd.to_datetime(client_perf['date']).astype('datetime64[ns]')

    acct_dim = _read_parquet(
        'gold/accounts_dimension_latest.parquet',
        columns=['relationship_id', 'implementor'],
        verbose=verbose
    )

    client_dim = _read_parquet(
        'gold/client_dimension.parquet',
        columns=['relationship_id', 'first_seen_date', 'primary_architect', 'primary_implementor'],
        verbose=verbose
    )
    if 'first_seen_date' in client_dim.columns:
        client_dim['first_seen_date'] = pd.to_datetime(client_dim['first_seen_date']).astype('datetime64[ns]')

    return adv_ts, client_perf, acct_dim, client_dim


# ---------------------------------------------------------------------------
# Implementor view builder (no pre-aggregated gold view exists)
# ---------------------------------------------------------------------------

def _modal_str(series: pd.Series, default: str = 'Unassigned') -> str:
    """Return the most common non-null, non-empty value in a Series."""
    clean = series.dropna().astype(str).str.strip()
    clean = clean[~clean.str.lower().isin(MODAL_NULLS)]
    if clean.empty:
        return default
    return clean.mode().iloc[0]


def build_implementor_daily(client_perf: pd.DataFrame,
                             acct_dim: pd.DataFrame,
                             verbose: bool = False) -> pd.DataFrame:
    """
    Aggregate client_performance to (date, implementor) grain using modal
    implementor per relationship from accounts_dimension_latest.

    Output columns: date, implementor, cum_inflows, cum_outflows, nna, num_relationships
    """
    print("Building implementor daily timeseries...")

    if 'implementor' not in acct_dim.columns:
        print("  WARN: 'implementor' column not found in accounts_dimension_latest -- skipping")
        return pd.DataFrame(columns=['date', 'implementor', 'cum_inflows', 'cum_outflows',
                                     'nna', 'num_relationships'])

    # Compute modal implementor per relationship
    rel_impl = (
        acct_dim.groupby('relationship_id', sort=False)['implementor']
        .agg(lambda s: _modal_str(s, 'Unassigned'))
        .reset_index()
        .rename(columns={'implementor': 'implementor'})
    )

    n_distinct = rel_impl[rel_impl['implementor'] != 'Unassigned']['implementor'].nunique()
    n_unassigned = (rel_impl['implementor'] == 'Unassigned').sum()
    if verbose:
        print(f"  {len(rel_impl):,} relationships | {n_distinct} distinct implementors | "
              f"{n_unassigned} unassigned")

    # Join to client_performance
    joined = client_perf.merge(rel_impl, on='relationship_id', how='left')
    joined['implementor'] = joined['implementor'].fillna('Unassigned')

    # Aggregate to (date, implementor) grain
    impl_daily = (
        joined.groupby(['date', 'implementor'], sort=False)
        .agg(
            total_aua=('total_aua', 'sum'),
            cum_inflows=('cum_inflows', 'sum'),
            cum_outflows=('cum_outflows', 'sum'),
            nna=('nna', 'sum'),
            num_relationships=('relationship_id', 'nunique')
        )
        .reset_index()
    )

    if verbose:
        n_impl_advisors = impl_daily[impl_daily['implementor'] != 'Unassigned']['implementor'].nunique()
        print(f"  Built {len(impl_daily):,} rows across {n_impl_advisors} implementors")

    return impl_daily


# ---------------------------------------------------------------------------
# Rolling window computation
# ---------------------------------------------------------------------------

def _slugify(name: str) -> str:
    """Convert an advisor name to a lowercase underscore slug."""
    slug = name.lower().strip()
    slug = re.sub(r'[^a-z0-9]+', '_', slug)
    slug = slug.strip('_')
    return slug


def compute_rolling_series(daily_df: pd.DataFrame,
                            advisor_col: str,
                            advisor_prefix: str,
                            verbose: bool = False) -> list:
    """
    Given a daily timeseries with cumulative cum_inflows, cum_outflows, nna
    per advisor, compute rolling window series for each non-Unassigned advisor.

    Rolling method:
        For each date D and window W (in days):
            Find the latest data date <= (D - W days) for this advisor.
            roll_val[D] = cum_val[D] - cum_val[that_past_date]
        Data points where no past date exists are excluded (insufficient history).

    Returns list of advisor dicts matching the output schema.
    """
    advisors_out = []

    sorted_df = daily_df.sort_values(['date']).reset_index(drop=True)
    unique_advisors = (
        sorted_df[sorted_df[advisor_col] != 'Unassigned'][advisor_col].unique()
    )

    if verbose:
        print(f"  Computing rolling series for {len(unique_advisors)} {advisor_prefix}s...")

    for advisor_name in unique_advisors:
        adv = (
            sorted_df[sorted_df[advisor_col] == advisor_name]
            .sort_values('date')
            .reset_index(drop=True)
        )

        if adv.empty:
            continue

        series = {}
        for window_label, window_days in WINDOWS.items():
            window_td = pd.Timedelta(days=window_days)

            # Build "past" lookup: for each row, find cum values ~W days ago
            # merge_asof finds the latest row with date <= (current_date - window_td)
            adv_lookup = adv[['date', 'cum_inflows', 'cum_outflows', 'nna']].copy()
            adv_current = adv[['date', 'cum_inflows', 'cum_outflows', 'nna']].copy()
            adv_current['target_date'] = adv_current['date'] - window_td

            lagged = pd.merge_asof(
                adv_current.sort_values('target_date'),
                adv_lookup.rename(columns={
                    'date': 'past_date',
                    'cum_inflows': 'past_inflows',
                    'cum_outflows': 'past_outflows',
                    'nna': 'past_nna'
                }).sort_values('past_date'),
                left_on='target_date',
                right_on='past_date',
                direction='backward'
            )

            # Drop rows with no valid past date (insufficient history for this window)
            valid = lagged[lagged['past_date'].notna()].copy()

            valid['roll_inflows']  = valid['cum_inflows']  - valid['past_inflows']
            valid['roll_outflows'] = valid['cum_outflows'] - valid['past_outflows']
            valid['roll_nna']      = valid['nna']          - valid['past_nna']

            # Outflows are stored as positive cumulative sums; rolling diff stays positive
            series[window_label] = [
                {
                    'date':     row['date'].strftime('%Y-%m-%d'),
                    'nna':      round(float(row['roll_nna']), 2),
                    'inflows':  round(float(row['roll_inflows']), 2),
                    'outflows': round(float(row['roll_outflows']), 2)
                }
                for _, row in valid.sort_values('date').iterrows()
            ]

        advisor_id = f"{advisor_prefix}_{_slugify(advisor_name)}"
        advisors_out.append({
            'advisor_name': str(advisor_name),
            'advisor_id':   advisor_id,
            'series':       series
        })

    # Sort by most recent AUA (use length of series as proxy for history richness)
    # Primary sort: descending by 1Y series length, then by name for stability
    advisors_out.sort(key=lambda x: (-len(x['series'].get('1Y', [])), x['advisor_name']))

    if verbose:
        for a in advisors_out:
            pts_30d = len(a['series'].get('30d', []))
            pts_1Y  = len(a['series'].get('1Y', []))
            print(f"    {a['advisor_name']}: 30d={pts_30d} pts, 1Y={pts_1Y} pts")

    return advisors_out


# ---------------------------------------------------------------------------
# MTD / QTD / YTD summary (donut chart data)
# ---------------------------------------------------------------------------

def _get_period_boundaries(ref_date: pd.Timestamp) -> dict:
    """
    Compute current + prior period boundaries for MTD, QTD, YTD.

    Returns dict with current and prior period dates for each label.
    Prior periods are the immediately preceding complete period of the same type.
    """
    # --- Current periods ---
    mtd_start = pd.Timestamp(ref_date.year, ref_date.month, 1)

    q_month = ((ref_date.month - 1) // 3) * 3 + 1
    qtd_start = pd.Timestamp(ref_date.year, q_month, 1)

    ytd_start = pd.Timestamp(ref_date.year, 1, 1)

    # --- Prior periods (complete, immediately preceding) ---
    # Prior month: full previous month
    if ref_date.month == 1:
        prior_mtd_start = pd.Timestamp(ref_date.year - 1, 12, 1)
        prior_mtd_end   = pd.Timestamp(ref_date.year - 1, 12, 31)
    else:
        prior_mtd_start = pd.Timestamp(ref_date.year, ref_date.month - 1, 1)
        prior_mtd_end   = mtd_start - pd.Timedelta(days=1)

    # Prior quarter: full previous quarter
    if q_month == 1:
        prior_qtd_start = pd.Timestamp(ref_date.year - 1, 10, 1)
        prior_qtd_end   = pd.Timestamp(ref_date.year - 1, 12, 31)
    else:
        prior_q_month   = q_month - 3
        prior_qtd_start = pd.Timestamp(ref_date.year, prior_q_month, 1)
        prior_qtd_end   = qtd_start - pd.Timedelta(days=1)

    # Prior YTD: same calendar range last year (Jan 1 to same day-of-year)
    prior_ytd_start = pd.Timestamp(ref_date.year - 1, 1, 1)
    prior_ytd_end   = pd.Timestamp(ref_date.year - 1, ref_date.month, min(ref_date.day, 28))
    # Use min(day, 28) to avoid Feb 29 issues; merge_asof will find closest available date

    def _label_month(dt):
        return dt.strftime('%b %Y')

    def _label_quarter(dt):
        return f"Q{(dt.month - 1) // 3 + 1} {dt.year}"

    return {
        'mtd': {
            'start': mtd_start,
            'display': _label_month(ref_date),
            'prior_start': prior_mtd_start,
            'prior_end': prior_mtd_end,
            'prior_display': _label_month(prior_mtd_start),
            'growth_label': 'MoM',
        },
        'qtd': {
            'start': qtd_start,
            'display': _label_quarter(ref_date),
            'prior_start': prior_qtd_start,
            'prior_end': prior_qtd_end,
            'prior_display': _label_quarter(prior_qtd_start),
            'growth_label': 'QoQ',
        },
        'ytd': {
            'start': ytd_start,
            'display': str(ref_date.year),
            'prior_start': prior_ytd_start,
            'prior_end': prior_ytd_end,
            'prior_display': str(ref_date.year - 1),
            'growth_label': 'YoY',
        },
    }


def _compute_nna_for_range(sorted_df: pd.DataFrame, advisor_col: str,
                            start_date: pd.Timestamp, end_date: pd.Timestamp) -> dict:
    """
    Compute NNA/inflows/outflows for each advisor over [start_date, end_date].
    Returns dict keyed by advisor_name -> {nna, inflows, outflows}.
    """
    all_dates = sorted_df['date'].sort_values().unique()

    # End snapshot: closest date <= end_date
    end_dates = all_dates[all_dates <= end_date]
    if len(end_dates) == 0:
        return {}
    actual_end = end_dates.max()

    # Base snapshot: closest date < start_date
    base_dates = all_dates[all_dates < start_date]
    if len(base_dates) == 0:
        actual_base = all_dates.min()
    else:
        actual_base = base_dates.max()

    end_snap  = sorted_df[sorted_df['date'] == actual_end].set_index(advisor_col)
    base_snap = sorted_df[sorted_df['date'] == actual_base].set_index(advisor_col)

    result = {}
    for adv_name in end_snap.index:
        if adv_name == 'Unassigned':
            continue
        end_row = end_snap.loc[adv_name]
        if isinstance(end_row, pd.DataFrame):
            end_row = end_row.iloc[0]

        nna_end = float(end_row.get('nna', 0) or 0)
        inf_end = float(end_row.get('cum_inflows', 0) or 0)
        out_end = float(end_row.get('cum_outflows', 0) or 0)

        if adv_name in base_snap.index:
            base_row = base_snap.loc[adv_name]
            if isinstance(base_row, pd.DataFrame):
                base_row = base_row.iloc[0]
            nna_base = float(base_row.get('nna', 0) or 0)
            inf_base = float(base_row.get('cum_inflows', 0) or 0)
            out_base = float(base_row.get('cum_outflows', 0) or 0)
        else:
            nna_base = inf_base = out_base = 0.0

        result[str(adv_name)] = {
            'nna':      round(nna_end - nna_base, 2),
            'inflows':  round(inf_end - inf_base, 2),
            'outflows': round(out_end - out_base, 2),
        }
    return result


def compute_period_summary(daily_df: pd.DataFrame,
                            advisor_col: str,
                            advisor_prefix: str,
                            latest_date: pd.Timestamp,
                            client_dim: pd.DataFrame = None,
                            advisor_map_col: str = None,
                            verbose: bool = False) -> dict:
    """
    Compute MTD/QTD/YTD summary with prior-period comparison, growth rates,
    AUA, new clients, and rank changes.

    Each period includes:
    - Current period NNA/inflows/outflows per advisor (donut segments)
    - Prior period NNA per advisor (for growth calculation)
    - MoM/QoQ/YoY growth percentages (total and per advisor)
    - Rank and rank_change vs prior period
    - AUA and client_count from latest snapshot
    - new_clients from client_dimension.first_seen_date
    """
    periods = _get_period_boundaries(latest_date)
    sorted_df = daily_df.sort_values(['date']).reset_index(drop=True)

    # Latest snapshot for AUA + client count
    latest_snap = sorted_df[sorted_df['date'] == latest_date].set_index(advisor_col)

    # New clients lookup: count of relationships with first_seen_date in period
    # Keyed by (advisor_name, period_start) -> count
    new_clients_cache = {}
    if client_dim is not None and advisor_map_col and advisor_map_col in client_dim.columns:
        for period_label, pinfo in periods.items():
            period_start = pinfo['start']
            new_in_period = client_dim[
                (client_dim['first_seen_date'] >= period_start) &
                (client_dim['first_seen_date'] <= latest_date)
            ]
            if not new_in_period.empty:
                counts = new_in_period.groupby(advisor_map_col)['relationship_id'].nunique()
                for adv_name, cnt in counts.items():
                    new_clients_cache[(str(adv_name), period_label)] = int(cnt)

    result = {}

    for period_label, pinfo in periods.items():
        # Current period
        current_data = _compute_nna_for_range(
            sorted_df, advisor_col, pinfo['start'], latest_date
        )

        # Prior period
        prior_data = _compute_nna_for_range(
            sorted_df, advisor_col, pinfo['prior_start'], pinfo['prior_end']
        )

        # Build segments sorted by current NNA
        segments = []
        for adv_name, cur in current_data.items():
            prior = prior_data.get(adv_name, {'nna': 0, 'inflows': 0, 'outflows': 0})

            # AUA + client count from latest snapshot
            aua = 0.0
            client_count = 0
            if adv_name in latest_snap.index:
                snap_row = latest_snap.loc[adv_name]
                if isinstance(snap_row, pd.DataFrame):
                    snap_row = snap_row.iloc[0]
                aua = float(snap_row.get('total_aua', 0) or 0)
                client_count = int(snap_row.get('num_relationships', 0) or 0)

            new_clients = new_clients_cache.get((adv_name, period_label), 0)

            # Growth: current vs prior NNA
            prior_nna = prior['nna']
            nna_growth_pct = (
                round((cur['nna'] - prior_nna) / abs(prior_nna) * 100, 1)
                if abs(prior_nna) > 100 else 0.0  # avoid div-by-near-zero
            )

            segments.append({
                'advisor_name':    adv_name,
                'advisor_id':      f"{advisor_prefix}_{_slugify(adv_name)}",
                'nna':             cur['nna'],
                'inflows':         cur['inflows'],
                'outflows':        cur['outflows'],
                'total_aua':       round(aua, 2),
                'client_count':    client_count,
                'new_clients':     new_clients,
                'prior_nna':       prior_nna,
                'nna_growth_pct':  nna_growth_pct,
            })

        # Sort by NNA descending, assign ranks
        segments.sort(key=lambda x: x['nna'], reverse=True)
        for i, seg in enumerate(segments):
            seg['rank'] = i + 1

        # Compute prior ranks for rank_change
        prior_ranked = sorted(segments, key=lambda x: x['prior_nna'], reverse=True)
        prior_rank_map = {s['advisor_name']: i + 1 for i, s in enumerate(prior_ranked)}
        for seg in segments:
            prior_rank = prior_rank_map.get(seg['advisor_name'], seg['rank'])
            seg['prior_rank']   = prior_rank
            seg['rank_change']  = prior_rank - seg['rank']  # positive = moved up

        # Totals
        total_nna      = sum(s['nna'] for s in segments)
        total_inflows  = sum(s['inflows'] for s in segments)
        total_outflows = sum(s['outflows'] for s in segments)
        prior_total_nna = sum(s['prior_nna'] for s in segments)

        total_growth_pct = (
            round((total_nna - prior_total_nna) / abs(prior_total_nna) * 100, 1)
            if abs(prior_total_nna) > 100 else 0.0
        )

        # nna_pct + colors on top segments, Other bucket for remainder
        abs_total = sum(abs(s['nna']) for s in segments)
        top_segments   = segments[:MAX_DONUT_SEGMENTS]
        other_segments = segments[MAX_DONUT_SEGMENTS:]

        for i, seg in enumerate(top_segments):
            seg['nna_pct'] = round(abs(seg['nna']) / abs_total * 100, 1) if abs_total > 0 else 0.0
            seg['color'] = DONUT_COLORS[i % len(DONUT_COLORS)]

        if other_segments:
            other_nna      = sum(s['nna'] for s in other_segments)
            other_inflows  = sum(s['inflows'] for s in other_segments)
            other_outflows = sum(s['outflows'] for s in other_segments)
            other_aua      = sum(s['total_aua'] for s in other_segments)
            other_clients  = sum(s['client_count'] for s in other_segments)
            other_new      = sum(s['new_clients'] for s in other_segments)
            other_prior    = sum(s['prior_nna'] for s in other_segments)
            other_growth   = (
                round((other_nna - other_prior) / abs(other_prior) * 100, 1)
                if abs(other_prior) > 100 else 0.0
            )
            top_segments.append({
                'advisor_name': 'Other',
                'advisor_id':   f'{advisor_prefix}_other',
                'nna':          round(other_nna, 2),
                'nna_pct':      round(abs(other_nna) / abs_total * 100, 1) if abs_total > 0 else 0.0,
                'inflows':      round(other_inflows, 2),
                'outflows':     round(other_outflows, 2),
                'total_aua':    round(other_aua, 2),
                'client_count': other_clients,
                'new_clients':  other_new,
                'prior_nna':    round(other_prior, 2),
                'nna_growth_pct': other_growth,
                'rank': MAX_DONUT_SEGMENTS + 1,
                'prior_rank': MAX_DONUT_SEGMENTS + 1,
                'rank_change': 0,
                'color':        OTHER_COLOR,
            })

        result[period_label] = {
            'period_start':   pinfo['start'].strftime('%Y-%m-%d'),
            'period_end':     latest_date.strftime('%Y-%m-%d'),
            'display':        pinfo['display'],
            'growth_label':   pinfo['growth_label'],
            'total_nna':      round(total_nna, 2),
            'total_inflows':  round(total_inflows, 2),
            'total_outflows': round(total_outflows, 2),
            'prior': {
                'period_start': pinfo['prior_start'].strftime('%Y-%m-%d'),
                'period_end':   pinfo['prior_end'].strftime('%Y-%m-%d'),
                'display':      pinfo['prior_display'],
                'total_nna':    round(prior_total_nna, 2),
            },
            'growth_pct':     total_growth_pct,
            'segments':       top_segments,
        }

        if verbose:
            n_pos = sum(1 for s in segments if s['nna'] >= 0)
            n_neg = len(segments) - n_pos
            print(f"  {period_label}: NNA ${total_nna:,.0f} ({pinfo['growth_label']} "
                  f"{total_growth_pct:+.1f}%) | {n_pos} positive, {n_neg} negative | "
                  f"top={top_segments[0]['advisor_name'] if top_segments else 'N/A'}")

    return result


# ---------------------------------------------------------------------------
# Main assembly
# ---------------------------------------------------------------------------

def generate_advisor_rolling_flows(verbose: bool = False) -> dict:
    """
    Load data, compute rolling series for architects and implementors,
    return JSON-ready dict.
    """
    adv_ts, client_perf, acct_dim, client_dim = load_data(verbose=verbose)

    data_as_of = adv_ts['date'].max().strftime('%Y-%m-%d')
    latest_date = adv_ts['date'].max()
    print(f"Data as of: {data_as_of}")

    # --- Architects: use pre-aggregated nna_aua_by_advisor ---
    print("Processing architects...")
    adv_clean = adv_ts[
        adv_ts['architect'].notna() &
        ~adv_ts['architect'].str.strip().str.lower().isin(MODAL_NULLS)
    ].copy()
    architects = compute_rolling_series(adv_clean, 'architect', 'arch', verbose=verbose)

    # --- Implementors: build daily view on-the-fly, then compute rolling ---
    print("Processing implementors...")
    impl_daily = build_implementor_daily(client_perf, acct_dim, verbose=verbose)
    if impl_daily.empty or impl_daily['implementor'].nunique() <= 1:
        print("  WARN: No implementor data available -- implementors list will be empty")
        implementors = []
    else:
        impl_clean = impl_daily[
            impl_daily['implementor'].notna() &
            ~impl_daily['implementor'].str.strip().str.lower().isin(MODAL_NULLS)
        ].copy()
        implementors = compute_rolling_series(impl_clean, 'implementor', 'impl', verbose=verbose)

    # --- MTD/QTD/YTD summary (donut chart default view) ---
    print("Computing MTD/QTD/YTD summary for architects...")
    arch_summary = compute_period_summary(
        adv_clean, 'architect', 'arch', latest_date,
        client_dim=client_dim, advisor_map_col='primary_architect',
        verbose=verbose
    )

    if impl_daily.empty or impl_daily['implementor'].nunique() <= 1:
        impl_summary = {'mtd': _empty_period(), 'qtd': _empty_period(), 'ytd': _empty_period()}
    else:
        print("Computing MTD/QTD/YTD summary for implementors...")
        impl_summary = compute_period_summary(
            impl_clean, 'implementor', 'impl', latest_date,
            client_dim=client_dim, advisor_map_col='primary_implementor',
            verbose=verbose
        )

    # Validation
    if architects:
        sample = architects[0]
        sample_30d = sample['series'].get('30d', [])
        sample_1Y  = sample['series'].get('1Y', [])
        print(f"Validation: {len(architects)} architects, {len(implementors)} implementors")
        print(f"  Sample ({sample['advisor_name']}): 30d={len(sample_30d)} pts, 1Y={len(sample_1Y)} pts")
        if sample_30d:
            pt = sample_30d[-1]
            computed_nna = round(pt['inflows'] - pt['outflows'], 2)
            if abs(computed_nna - pt['nna']) > 1.0:
                print(f"  WARN: nna mismatch on sample point: "
                      f"inflows-outflows={computed_nna} vs nna={pt['nna']}")
            else:
                print(f"  OK: nna == inflows - outflows check passed on latest 30d point")

    if arch_summary.get('qtd'):
        qtd = arch_summary['qtd']
        print(f"  Summary QTD: {len(qtd['segments'])} segments, total NNA ${qtd['total_nna']:,.0f}")

    return {
        'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'data_as_of':   data_as_of,
        'firm_id':      FIRM_ID,
        'summary': {
            'architects':   arch_summary,
            'implementors': impl_summary,
        },
        'architects':   architects,
        'implementors': implementors
    }


def _empty_period() -> dict:
    """Return an empty period summary for when no data is available."""
    return {
        'period_start': '', 'period_end': '', 'display': '',
        'total_nna': 0, 'total_inflows': 0, 'total_outflows': 0,
        'segments': []
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


def write_s3(payload: dict) -> None:
    body = json.dumps(payload, indent=2, default=str).encode('utf-8')
    s3 = boto3.client('s3', region_name='us-east-1')
    s3.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=OUTPUT_KEY,
        Body=body,
        ContentType='application/json'
    )
    print(f"OK: Uploaded to s3://{OUTPUT_BUCKET}/{OUTPUT_KEY} ({len(body):,} bytes)")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Generate advisor_rolling_flows.json from gold tables'
    )
    parser.add_argument(
        '--upload', action='store_true',
        help=f'Upload output to s3://{OUTPUT_BUCKET}/{OUTPUT_KEY}'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Compute and validate but do not write anywhere'
    )
    parser.add_argument(
        '--output', type=str, default=None,
        help=f'Local output path (default: {DEFAULT_LOCAL_OUTPUT})'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Verbose logging'
    )
    args = parser.parse_args()

    print('============================================================')
    print('10_generate_advisor_rolling_flows.py')
    print(f'Started: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}')
    print('============================================================')

    payload = generate_advisor_rolling_flows(verbose=args.verbose)

    if args.dry_run:
        print("OK: Dry run complete -- no output written")
        # Summary preview
        for role in ('architects', 'implementors'):
            summary = payload['summary'][role]
            print(f"  {role} summary:")
            for period in ('mtd', 'qtd', 'ytd'):
                p = summary[period]
                n_seg = len(p.get('segments', []))
                print(f"    {period}: NNA=${p['total_nna']:,.0f} ({n_seg} segments)")
        # Rolling series preview
        for adv_type in ('architects', 'implementors'):
            advisors = payload[adv_type]
            print(f"  {adv_type} rolling: {len(advisors)} advisors")
            for a in advisors[:3]:
                pts = {w: len(a['series'].get(w, [])) for w in ('30d', '90d', '1Y')}
                print(f"    {a['advisor_name']}: {pts}")
        sys.exit(0)

    if args.upload:
        write_s3(payload)
    else:
        output_path = args.output or DEFAULT_LOCAL_OUTPUT
        write_local(payload, output_path)

    print('============================================================')
    print(f'COMPLETE: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}')
    print('============================================================')


if __name__ == '__main__':
    main()
```

---

## Participant Background

### 0.4.0_DS_ClientPlatform -- Pending Task Orders

#### advisor_intelligence_completion.md

# Task Order: AdvisorIntelligence Data Completion — 0.4.0_DS_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-03-ds-advisor-intelligence-completion</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
  </metadata>

  <objective>
    Implement all data-layer additions for AdvisorIntelligence completion. Streams A1, A2,
    and A3 require Pattern 0 alignment threads to run FIRST — the thread receipts define
    the exact JSON shapes and TypeScript interfaces DS must implement. Do NOT implement
    A1/A2/A3 based on this task order's descriptions alone; the thread receipt is the
    binding specification. Streams A4 and A5 have no interface dependency and start
    immediately. Stream E is blocked by the Books tab design thread (Stream D).
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-continuous-nna-cla-alignment.sh</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-advisors-stacked-bar-alignment.sh</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-books-tab-design.sh</ref>
    <ref type="data-contract">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</ref>
  </references>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</file>
      <file action="modify">data/black_diamond/scripts/gold/10_generate_advisor_rolling_flows.py</file>
      <file action="verify">data/black_diamond/scripts/gold/09_build_distribution_stats.py</file>
      <file action="modify">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</file>
    </files>
  </scope>

  <requirements>

    <!-- ================================================================ -->
    <!-- STREAM A4 — Snapshot NNA bell curve math verification            -->
    <!-- UNBLOCKED — start immediately, no interface dependency           -->
    <!-- ================================================================ -->
    <requirement id="A4.1">
      Verify that commit 8247c6d0 correctly implemented |abs| for negative NNA accounts
      in script 09's bell curve percentile threshold calculation.
      Open partner_analytics/header_metrics.json from S3 and inspect the distribution
      field for the NNA view's outflow segment.
      Confirm P10/P25/Median/P75/P90 thresholds are non-degenerate: not all zero,
      not symmetric mirrors of the positive side.
    </requirement>
    <requirement id="A4.2">
      If the fix did NOT land: write a targeted patch to script 09 and coordinate with
      0.4.0_DT to deploy the EC2 script update.
      If the fix DID land: document the verification result in your session log with
      the specific threshold values observed in header_metrics.json.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM A5 — opal-users-v2 advisor identity investigation         -->
    <!-- UNBLOCKED — start immediately, no interface dependency           -->
    <!-- ================================================================ -->
    <requirement id="A5.1">
      Investigate the schema of the opal-users-v2 DynamoDB table (read-only):
        - What fields identify an advisor (userId, email, advisorId, firmId)?
        - What is the partition key / sort key structure?
    </requirement>
    <requirement id="A5.2">
      Determine whether a mapping from opal-users-v2 identity fields to
      accounts_dimension_latest.architect or rel_architect_lookup.parquet already exists:
        (a) Direct field match
        (b) Email-based lookup
        (c) No existing mapping — new data registration step required
      Document findings in your session log. This is the linchpin for Books tab auth gating.
      If option (c): flag as a blocker and surface to COO and CTO before any auth work proceeds.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM A1 — adv_drill in timeseries_chart.json                   -->
    <!-- BLOCKED: run Pattern 0 thread first                              -->
    <!-- Thread: org/threads/staging/run-2026-03-03-continuous-nna-cla-alignment.sh -->
    <!-- ================================================================ -->
    <requirement id="A1.1">
      GATE: Do not implement adv_drill until the Pattern 0 alignment thread
      (2026-03-03-continuous-nna-cla-alignment) has completed and you have a receipt at:
        org/tier2_senior/0.4.0_DS_ClientPlatform/threads/
      The thread receipt is the binding specification for the adv_drill JSON shape,
      S3 key pattern, cardinality constraints, and date range. Implement exactly what
      was agreed in the thread — not what is described in the PRD or this task order.
    </requirement>
    <requirement id="A1.2">
      In the thread, you are the knowledge source. Describe what per-architect and
      per-client NNA data currently exists in the gold layer. Name specific parquet
      files, column names, and cardinality. Let DE specify the TypeScript interface
      and RD specify the chart constraint — then converge on the exact shape.
    </requirement>
    <requirement id="A1.3">
      After thread completes: implement adv_drill in bd-portal-publisher/lambda_function.py
      per the agreed contract. Update data_contract.xml with the agreed shape, S3 key,
      and grain definitions BEFORE signaling DT to deploy.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM A2 — cla_timeseries in timeseries_chart.json              -->
    <!-- BLOCKED: run Pattern 0 thread first (same thread as A1)          -->
    <!-- Thread: org/threads/staging/run-2026-03-03-continuous-nna-cla-alignment.sh -->
    <!-- ================================================================ -->
    <requirement id="A2.1">
      GATE: Same as A1 — do not implement cla_timeseries until the thread receipt from
      2026-03-03-continuous-nna-cla-alignment is in your threads/ folder.
      The thread defines: NMNC/NMEC classification logic (agreed with DE and RD),
      the exact JSON structure, grain definitions (total/geo/adv/geo_drill),
      and whether implementation lives in script 09 (EC2) or the publisher Lambda.
    </requirement>
    <requirement id="A2.2">
      In the thread, surface what NMNC/NMEC classification data currently exists in
      the gold layer. Do NOT assume the classification. Name the specific field or
      derivation logic and let all three agents agree on the definition in the thread.
      Do not commit any classification logic until DE has confirmed it matches how
      CLA is currently defined in header_metrics.json.
    </requirement>
    <requirement id="A2.3">
      After thread completes: implement cla_timeseries per the agreed contract.
      Update data_contract.xml BEFORE signaling DT to deploy.
      Note: adv_drill and cla_timeseries should deploy together in one publisher update
      (Stream B1) to minimize deploy events.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM A3 — Stacked bar + 1Y rolling for Advisors tab            -->
    <!-- BLOCKED: run Pattern 0 thread first                              -->
    <!-- Thread: org/threads/staging/run-2026-03-03-advisors-stacked-bar-alignment.sh -->
    <!-- ================================================================ -->
    <requirement id="A3.1">
      GATE: Do not modify script 10 until the Pattern 0 alignment thread
      (2026-03-03-advisors-stacked-bar-alignment) has completed and you have a receipt at:
        org/tier2_senior/0.4.0_DS_ClientPlatform/threads/
      The thread receipt defines: the exact output schema for advisor_rolling_flows.json,
      how outflows are encoded (sign convention vs separate field), what period-anchored
      aggregation is feasible given available history, and the TypeScript interface
      DE and RD agreed on.
    </requirement>
    <requirement id="A3.2">
      In the thread, describe what script 10 currently computes, what parquet columns
      carry inflows vs outflows vs net NNA, and what date history is available.
      Be specific about whether inflows and outflows are tracked separately in the
      source data or only as net NNA. Let DE and RD shape the output contract from
      what you describe as feasible.
    </requirement>
    <requirement id="A3.3">
      After thread completes: implement the agreed stacked_bar and rolling_1y output
      in script 10. Update data_contract.xml BEFORE signaling DT for Stream B2 deploy.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM E — Books data contract audit (BLOCKED by Stream D)       -->
    <!-- ================================================================ -->
    <requirement id="E.1">
      BLOCKED: Do not begin Stream E until the Books design thread
      (2026-03-03-books-tab-design) completes and you have a receipt in your threads/ folder.
      In that thread, you are the knowledge source. Read the advisor-publisher Lambda and
      scripts 03, 05b, and 06 carefully. Describe precisely what each script produces
      and which of those outputs currently flow into the publisher vs remain gold-layer only.
    </requirement>
    <requirement id="E.2">
      After thread: produce a gap list (what L4 fields exist in gold but are absent from
      the publisher output). Add to data_contract.xml as a pending Books L4 section.
      Implement the publisher additions. Update data_contract.xml to complete status
      BEFORE signaling DT for Stream F deploy.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">A4: Bell curve verification result in session log with actual threshold values; patch applied if needed.</criterion>
    <criterion id="2">A5: opal-users-v2 mapping findings documented in session log; option (c) flagged to COO if no mapping exists.</criterion>
    <criterion id="3">A1: adv_drill implemented per thread receipt; data_contract.xml updated; DT deploy confirmed.</criterion>
    <criterion id="4">A2: cla_timeseries implemented per thread receipt; classification logic agreed in thread; data_contract.xml updated.</criterion>
    <criterion id="5">A3: advisor_rolling_flows.json updated per thread receipt; data_contract.xml updated; DT deploy confirmed.</criterion>
    <criterion id="6">E: L4 publisher gap list produced and closed; data_contract.xml updated (post-thread).</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>A1, A2, A3 are BLOCKED until Pattern 0 thread receipts are in your threads/ folder. Do not implement from PRD descriptions alone — the thread contract supersedes the PRD's suggested shapes.</constraint>
    <constraint>data_contract.xml must be updated and committed BEFORE signaling DT to deploy any Lambda change. This is a non-negotiable quality gate.</constraint>
    <constraint>Do NOT deploy directly. Hand off to 0.4.0_DT via your session log next steps with the commit hash of your code change.</constraint>
    <constraint>Do NOT use emojis in any script, Lambda, or log output. Plain ASCII only.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" -m "..."</constraint>
    <constraint>Start A4 and A5 in your first session. These have no thread dependency.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="2.0.0_SA_COO" task="2026-03-03-continuous-nna-cla-alignment" status="pending" note="A1 and A2 blocked until thread receipt"/>
    <dependency agent="2.0.0_SA_COO" task="2026-03-03-advisors-stacked-bar-alignment" status="pending" note="A3 blocked until thread receipt"/>
    <dependency agent="2.0.0_SA_COO" task="2026-03-03-books-tab-design" status="pending" note="E blocked until thread receipt"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Script 09 verification result (and patch if needed)</deliverable>
    <deliverable type="document">Session log with A5 opal-users-v2 findings</deliverable>
    <deliverable type="commit">bd-portal-publisher/lambda_function.py: adv_drill + cla_timeseries per thread receipt (A1+A2)</deliverable>
    <deliverable type="commit">10_generate_advisor_rolling_flows.py: stacked_bar + rolling_1y per thread receipt (A3)</deliverable>
    <deliverable type="document">data_contract.xml updated for A1, A2, A3 (before each DT deploy)</deliverable>
    <deliverable type="document">data_contract.xml updated with Books L4 contract (post-thread, Stream E)</deliverable>
  </deliverables>
</task_order>
```


### 0.4.0_DS_ClientPlatform -- Recent Commits

# Recent commits by 0.4.0_DS_ClientPlatform

076e1120 0.4.0_DT_ClientPlatform: enrich Pod 4 (ClientPlatform) agent prompts with source-grounded context

### 0.4.0_DE_ClientPlatform -- Recent Session Logs

#### pod_inventory_upgrade_ai_full_fidelity.md

# pod_inventory.xml Upgrade: AdvisorIntelligence Full-Fidelity — 0.4.0_DE_ClientPlatform

**Date:** 2026-03-03
**Start Time:** session start
**End Time:** ~15 min
**Workspace CLOUD commit:** `5efb15f4`

## Objective

Upgrade the AdvisorIntelligence section of pod_inventory.xml from medium-fidelity (sourced from
portal source reads) to full-fidelity now that 0.4.2_RD_AdvisorIntelligence produced their
page_inventory.xml deliverable (2026-03-02, discovered at session start today).

---

## Work Completed

### 1. Read 0.4.2_RD page_inventory.xml

Confirmed deliverable exists and is 100% complete (16 .tsx files, 3 .ts files, 10 API calls,
all shared imports traced). Key additions vs. prior pod_inventory AdvisorIntelligence section:
- Full tab state (UI state variables per tab documented)
- CLA metric in Distribution tab documented
- Drill-down path (states->cities, architects->clients) confirmed
- lifecycle_and_state section: state management approach, full data_flow sequence, type_guards
- unused_tabs section: AssetIntelligenceTab correctly labeled as NOT wired in v5
- `useAuth` and `useFilterTracking` shared imports confirmed (BooksTab)
- `@/lib/dateUtils.formatPanelTimestamp` import confirmed (page level)

### 2. Updated pod_inventory.xml

Changes made:
- `rd_deliverable_status` for 0.4.2: MISSING -> complete
- Removed `rd_deliverable_warning` block; replaced with `rd_audit_completeness` note
- Upgraded all 3 tab descriptions with full state/behavior detail from RD audit
- Added `unused_tabs` section for AssetIntelligenceTab
- Added `lifecycle_and_state` section (state_management, data_flow, type_guards)
- Removed missing_deliverable known_issue for 0.4.2; replaced with accurate limitation notes
- pod_health: missing_deliverables_count 1 -> 0; blocker #1 cleared; summary updated
- date: 2026-03-02 -> 2026-03-03 with last_updated note

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Add `lifecycle_and_state` section to AdvisorIntelligence only | ModelPortfolios is simpler (fewer state interactions); AI has complex multi-tab state that the DE must track for task order coordination |
| Add `unused_tabs` as separate section from `tabs` | Separates what is functional from what is present but unwired — prevents future confusion when issuing task orders |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/pod_inventory.xml` | Upgraded AdvisorIntelligence section to full-fidelity | Yes — `5efb15f4` |

---

## Blockers

None. The previous session blocker (0.4.2 page_inventory.xml missing) is resolved.

---

## Current State

**Status:** COMPLETE
**Active branch:** `CLOUD`

pod_inventory.xml is now at 100% fidelity for both pod pages. AdvisorIntelligence section
sourced from the 0.4.2_RD page_inventory.xml (produced 2026-03-02). Both RD deliverables are
complete. Wave 3 DS data_contract.xml issuance is now unblocked for the ClientPlatform pod.

---

## Next Steps

1. **Await Wave 3 DS task order from CTO/COO** — DS can now issue data_contract.xml for
   ClientPlatform. DS needs to trace: getPartnerAnalytics -> bd-portal-publisher Lambda -> S3;
   getAUMMetrics -> opal-portal-data-proxy -> SmartX DynamoDB.

2. **Monitor 0.4.2_RD_AdvisorIntelligence task order status** — The SA-issued page_inventory
   task order is still marked `pending` even though the deliverable was produced. Either 0.4.2
   should mark it `complete` themselves, or flag to SA for cleanup.

**Files to touch next:**
- None required immediately. Waiting on Wave 3 DS task order.

**Do NOT:**
- Issue Wave 3 DS task orders without CTO/COO direction — that is SA responsibility
- Modify any portal source files (no active code task orders)


### 0.4.0_DE_ClientPlatform -- Pending Task Orders

#### advisor_intelligence_completion.md

# Task Order: AdvisorIntelligence DE Completion — 0.4.0_DE_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-03-de-advisor-intelligence-completion</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
  </metadata>

  <objective>
    Drive completion of the AdvisorIntelligence page to v1.0 shippable state.
    DE responsibilities: leaderboard sort stability investigation (I2), review
    gate for all RD deliverables before DT pushes, NMNC/NMEC classification
    acknowledgment for DS (A2 gate), and Books tab coordination (G — blocked by thread).
    DE session logs are MANDATORY and are the primary status signal for COO tracking.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-continuous-nna-cla-alignment.sh</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-advisors-stacked-bar-alignment.sh</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-books-tab-design.sh</ref>
    <ref>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/pod_inventory.xml</ref>
    <ref>portal/src/pages/AdvisorIntelligence/</ref>
    <ref>portal/src/api/endpoints/advisor-intelligence.ts</ref>
    <ref>portal/src/pages/AdvisorIntelligence/types.ts</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <file action="investigate">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
      <file action="review">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</file>
      <file action="modify">org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/pod_inventory.xml</file>
    </files>
  </scope>

  <requirements>

    <!-- ================================================================ -->
    <!-- STREAM I2 — Leaderboard sort stability investigation + fix       -->
    <!-- UNBLOCKED                                                         -->
    <!-- ================================================================ -->
    <requirement id="I2.1">
      Investigate the leaderboard sort stability issue:
        (a) Frontend: check whether JS .sort() on equal NNA values is stable.
            Read AdvisorsTab.tsx sort logic — if there is no secondary sort key
            for ties, add name as a stable tiebreaker.
        (b) Data: check architect_leaderboard.json S3 output — confirm the rank
            field is correctly set and entries are pre-sorted by rank in the publisher.
      Determine root cause (a), (b), or both.
    </requirement>
    <requirement id="I2.2">
      If (a) — frontend sort fix: implement stable sort in AdvisorsTab.tsx.
        Use: .sort((a, b) => a.nna !== b.nna ? a.nna - b.nna : a.name.localeCompare(b.name))
        or equivalent. Commit the fix.
      If (b) — data fix: document the publisher sort bug in your session log and
        file a follow-up item in your next steps for DS + DT to address via script
        update and Lambda deploy.
      If both: fix the frontend sort now; flag the data issue separately.
    </requirement>
    <requirement id="I2.3">
      After investigation, update pod_inventory.xml to reflect the current leaderboard
      sort behavior (resolved vs. open).
    </requirement>

    <!-- ================================================================ -->
    <!-- PATTERN 0 THREAD PARTICIPATION — A1+A2 and A3                   -->
    <!-- ================================================================ -->
    <requirement id="thread.1">
      You are a participant in two Pattern 0 alignment threads. These threads run
      BEFORE DS writes any code for A1, A2, and A3. Your role in each:

      Thread 1 (2026-03-03-continuous-nna-cla-alignment):
        After DS describes available gold layer data, specify:
        - The TypeScript interface name(s) and shape the portal will use for adv_drill
        - The TypeScript interface name(s) and shape for cla_timeseries
        - The NMNC/NMEC definition your portal types currently expect
          (check header_metrics.json CLA structure vs what DS proposes)
        - Any query key or endpoint path change needed in advisor-intelligence.ts

      Thread 2 (2026-03-03-advisors-stacked-bar-alignment):
        After DS describes what script 10 can produce, specify:
        - The TypeScript interface for the stacked bar data per period
        - The TypeScript interface for the rolling 1Y series
        - How the period toggle maps to data keys
        - Outflow encoding requirement from a portal typing perspective

      The thread receipts are the binding interface specs. Your task orders for
      C2, C4, and 4C (issued to RD) reference these receipts. Do NOT finalize
      those stream requirements before the receipts are available.
    </requirement>

    <!-- ================================================================ -->
    <!-- RD REVIEW GATE — all streams before DT push                      -->
    <!-- ================================================================ -->
    <requirement id="review.1">
      You are the QA review gate for all RD (0.4.2_RD) commits before DT pushes to DEV.
      Review each stream as RD completes it:
        - C1 (GEO continuous): verify drill interaction works correctly, breadcrumb is clear
        - C3 (CLA snapshot): verify two-color NMNC/NMEC labels are accurate and match header_metrics.json field values
        - H (portal primitives refactor): verify no visual regression, panel structure is correct
        - I (Top Performers): verify rank clarity, period toggle updates rankings
        - C2, C4, 4C: review when RD signals completion (after DT B1/B2 deploys)
      Signal DT to push to DEV only after you have reviewed and approved.
    </requirement>
    <requirement id="review.2">
      After each RD stream you review, note it in your mandatory session log:
        - Stream reviewed, what you found, any corrections sent back to RD, approval status
      This is your primary status reporting mechanism to COO.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM G — Books tab coordination (BLOCKED by Stream D thread)   -->
    <!-- ================================================================ -->
    <requirement id="G.1">
      BLOCKED: Do not begin Books tab wiring until Stream D thread completes.
      When thread receipt lands in your threads/ folder, read the Books design brief at:
        docs/architecture/advisor_intelligence/books_tab_design_brief.md
      Your role for Books tab: API wiring (hook up L2/L3/L4 endpoints), auth gating
      logic (admin vs advisor view), and component structure — RD owns visual layout.
    </requirement>
    <requirement id="G.2">
      Auth gating for Books tab:
        - Admin (userRole === 'admin'): show advisor selector dropdown (all advisors)
        - Advisor: land directly on their own book — no dropdown, no selection
        - Use existing useAuth pattern for isInternal() / isDev() for L1 gating
        - Advisor identity resolution (JWT userId -> advisor name): implement ONLY after
          DS A5 investigation confirms the opal-users-v2 -> gold layer mapping exists.
          Do not assume the mapping exists until DS confirms.
    </requirement>
    <requirement id="G.3">
      Update pod_inventory.xml when Books tab API endpoints are wired.
      The Books tab section in pod_inventory.xml is currently missing — add it.
    </requirement>

    <!-- ================================================================ -->
    <!-- ONGOING — Session log mandate                                     -->
    <!-- ================================================================ -->
    <requirement id="log.1">
      DE session logs are MANDATORY. Write a session log for EVERY work session at:
        org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-03-03/{scope_action}.md
      Minimum sections: Objective, Work Completed, Decisions Made, Files Modified,
      Blockers, Current State, Next Steps.
      Include portal DEV commit hashes in header and Files Modified table.
    </requirement>
    <requirement id="log.2">
      Your first session log is also the pre-flight signal for COO to schedule
      the Books design thread (Stream D). COO cannot run the thread until you have
      at least one session log (O3 constraint in THREAD_KNOWLEDGE.md).
      Write your first session log after your initial orientation, before beginning I2.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">I2: Leaderboard sort root cause identified; frontend fix committed if applicable; data issue flagged if applicable.</criterion>
    <criterion id="2">A2-gate: NMNC/NMEC classification acknowledged in writing in session log before DS commits cla_timeseries.</criterion>
    <criterion id="3">All RD streams reviewed and documented in session log before DT pushes each stream to DEV.</criterion>
    <criterion id="4">Session log written for every work session (mandatory — no exceptions).</criterion>
    <criterion id="5">pod_inventory.xml updated for I2 resolution and Books tab endpoint wiring (post-thread).</criterion>
    <criterion id="6">Books tab auth gating wired and functional after DS A5 confirms mapping (post-thread).</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Session logs are MANDATORY for DE — not optional. This is a system-wide rule, not just for this task order.</constraint>
    <constraint>Do NOT push to DEV yourself. DT owns all pushes. Your role: review and approve.</constraint>
    <constraint>Do NOT implement Books tab auth gating until DS A5 confirms opal-users-v2 -> gold layer mapping exists.</constraint>
    <constraint>Do NOT use emojis in any code or log output. Plain ASCII only.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DE_ClientPlatform &lt;0.4.0_DE_ClientPlatform@opal.agent&gt;" -m "..."</constraint>
    <constraint>NOTE: You have no prior session logs. Write your first log immediately after orientation — it is the trigger for the COO to schedule the Books thread.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="advisor_intelligence_completion" status="pending" note="A2-gate requires DS to send classification logic for acknowledgment"/>
    <dependency agent="2.0.0_SA_COO" task="Stream-D-thread" status="pending" note="G blocked until thread completes"/>
    <dependency agent="0.4.2_RD_AdvisorIntelligence" task="advisor_intelligence_completion" status="pending" note="Review gate on all C/H/I/G streams"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Leaderboard sort fix in AdvisorsTab.tsx (if frontend root cause)</deliverable>
    <deliverable type="document">Mandatory session log for every work session — first log triggers COO thread scheduling</deliverable>
    <deliverable type="document">Written NMNC/NMEC classification acknowledgment in session log</deliverable>
    <deliverable type="document">RD stream review notes in session log for each reviewed stream</deliverable>
    <deliverable type="commit">Books tab API wiring + auth gating (post-thread, per design brief)</deliverable>
    <deliverable type="commit">pod_inventory.xml updated for I2 and Books tab</deliverable>
  </deliverables>
</task_order>
```


### 0.4.0_DE_ClientPlatform -- Recent Commits

# Recent commits by 0.4.0_DE_ClientPlatform

5efb15f4 0.4.0_DE_ClientPlatform: upgrade pod_inventory.xml AdvisorIntelligence to full-fidelity from 0.4.2 RD audit
076e1120 0.4.0_DT_ClientPlatform: enrich Pod 4 (ClientPlatform) agent prompts with source-grounded context
b331d3e6 feat(org): 0.4.0_DE_ClientPlatform — continuous view Max window clients fix task order
c08effac feat(org): 0.4.0_DE_ClientPlatform wave 2 — pod inventory + RD task orders
0033f9ca 0.4.0_DE_ClientPlatform: fix Daily AUA Analysis bottom margin to 70
e70b9730 0.4.0_DE_ClientPlatform: fix x-tick spacing on ModelPortfolios charts (corrected values)
4bda06a8 0.4.0_DE_ClientPlatform: fix x-tick spacing on ModelPortfolios charts

### 0.4.2_RD_AdvisorIntelligence -- Pending Task Orders

#### advisor_intelligence_completion.md

# Task Order: AdvisorIntelligence Portal Completion — 0.4.2_RD_AdvisorIntelligence

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-03-rd-advisor-intelligence-completion</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
  </metadata>

  <objective>
    Implement all portal-layer changes for AdvisorIntelligence completion. Covers
    7 streams: Distribution tab continuous and snapshot views (C1-C4), Advisors tab
    UI refactor (H, I, 4C stacked bar), and Books tab implementation (G — blocked).
    Streams C1, C3, H, and I have no data dependencies and can start immediately.
    Streams C2 and C4 are blocked by DT deploying the updated publisher (Stream B1).
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-continuous-nna-cla-alignment.sh</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-advisors-stacked-bar-alignment.sh</ref>
    <ref type="thread-staging">org/threads/staging/run-2026-03-03-books-tab-design.sh</ref>
    <ref>portal/src/pages/AdvisorIntelligence/</ref>
    <ref>portal/src/api/endpoints/advisor-intelligence.ts</ref>
    <ref>portal/src/pages/AdvisorIntelligence/types.ts</ref>
    <ref>portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</ref>
    <ref>portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</ref>
    <ref>portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/</page>
    </pages>
    <files>
      <!-- Distribution tab -->
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
      <!-- Advisors tab -->
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
      <!-- Books tab (blocked) -->
      <!-- portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx and related — pending thread -->
    </files>
  </scope>

  <requirements>

    <!-- ================================================================ -->
    <!-- STREAM C1 — Continuous NNA GEO: search + city drill-down         -->
    <!-- UNBLOCKED — geo_drill data already in timeseries_chart.json      -->
    <!-- ================================================================ -->
    <requirement id="C1.1">
      Update the GEO continuous NNA view in DistributionTab to render the top-8 states
      as separate series in the cumulative NNA chart. Use the same chart type, axis format,
      color scheme, and window toggle as the Assets Overview header panel's cumulative NNA chart.
      Data source: timeseries_chart.json geo view (per-state categories).
    </requirement>
    <requirement id="C1.2">
      Add a search input in the left panel controls that filters across ALL available states
      (not just top-8). States outside top-8 are accessible via search.
    </requirement>
    <requirement id="C1.3">
      Implement click-to-drill interaction:
        - Clicking a state in the chart legend OR selecting from search drills into that state
        - Chart re-renders showing per-city series for that state
          (sourced from timeseries_chart.json geo_drill[stateKey])
        - A breadcrumb/back control returns to the state-level view
      The drill state is local UI state — no API call needed (data already in the JSON).
    </requirement>
    <requirement id="C1.4">
      The back/breadcrumb must clearly display the current drill level:
        "All States" (default) or "Texas" (drilled) etc.
      Consistent with the existing GEO/ADV cohort toggle pattern already in the page.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM C2 — Continuous NNA ADV: search + client drill-down       -->
    <!-- BLOCKED: requires Stream B1 (DT deploys adv_drill)               -->
    <!-- ================================================================ -->
    <requirement id="C2.1">
      GATE: Do not begin C2 until DT confirms adv_drill is deployed and present in
      timeseries_chart.json S3 output.
    </requirement>
    <requirement id="C2.2">
      Implement ADV continuous NNA view using the adv_drill shape agreed in the
      Pattern 0 thread (2026-03-03-continuous-nna-cla-alignment). The thread receipt
      defines: adv_drill JSON structure, architect key format, client series format,
      and the TypeScript interface name DE typed against. Do not infer the shape from
      the PRD alone — use the receipt as the binding spec.
      Behavior:
        - Top architects as separate series, same chart format as GEO view
        - Search input for architects not in top list
        - Click architect -> drill to client/relationship level (adv_drill[architectKey])
        - Breadcrumb returns to architect-level view
        - No drill-down past relationship level
    </requirement>
    <requirement id="C2.3">
      The ADV drill interaction uses the same component and pattern as GEO drill (C1).
      Factor out the drill logic into a shared hook or utility if C1 and C2 share enough
      structure — but only if the abstraction is clean. No premature abstraction.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM C3 — Snapshot CLA: simplified two-color visualization     -->
    <!-- UNBLOCKED — data already in header_metrics.json                  -->
    <!-- ================================================================ -->
    <requirement id="C3.1">
      Replace the current CLA snapshot rendering (which incorrectly uses a flows/NNA chart)
      with a clean two-color proportional display:
        - Green = NMNC (New Client AUA percentage of total AUA)
        - Blue = NMEC (Existing Client AUA percentage of total AUA)
        - Preferred format: horizontal stacked bar or split donut — clean, no axes,
          just the two proportions with AUA dollar amounts labeled
      NO inflow/outflow data. NO NNA vocabulary. NO blue/red flows visual language.
    </requirement>
    <requirement id="C3.2">
      The visualization must support the time machine period selector (q1/q2/q3 periods)
      to show how the new-client percentage has shifted over time.
      Data source: header_metrics.json views.aua CLA structure
        (cla.current.geo.totals.nmnc_nna and related fields).
      Confirm field availability with DS if uncertain which fields carry NMNC/NMEC AUA.
    </requirement>
    <requirement id="C3.3">
      Label each segment clearly: "New Clients (NMNC)" in green, "Existing Clients (NMEC)"
      in blue. Include the AUA dollar amount and percentage for each segment.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM C4 — Continuous CLA: new time series stacked area chart   -->
    <!-- BLOCKED: requires Stream B1 (DT deploys cla_timeseries)          -->
    <!-- ================================================================ -->
    <requirement id="C4.1">
      GATE: Do not begin C4 until DT confirms cla_timeseries is deployed and present in
      timeseries_chart.json S3 output (cla.total field).
    </requirement>
    <requirement id="C4.2">
      Implement the continuous CLA view using the cla_timeseries shape agreed in the
      Pattern 0 thread (2026-03-03-continuous-nna-cla-alignment). The thread receipt
      defines: exact JSON structure (field names for NMNC and NMEC series, grain keys),
      S3 key, and the TypeScript interface name DE typed against.
      Chart behavior:
        - Y-axis = dollar AUM (absolute), two stacked areas: NMNC (green) and NMEC (blue)
        - Total height at each date = total firm AUM
        - Date range = same window toggle as other continuous views
        - Grains: total (firm-wide), geo/geo_drill, adv (architect terminal — no client drill)
      Use the agreed field names from the thread receipt, not the PRD's suggested naming.
    </requirement>
    <requirement id="C4.3">
      Add search input and drill-down behavior consistent with C1/C2:
        - GEO view: search states, click to drill to cities
        - ADV view: search architects (no client drill-down for CLA)
      Same breadcrumb/back pattern.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM H — Advisors tab: Portal Primitives Refactor              -->
    <!-- UNBLOCKED                                                         -->
    <!-- ================================================================ -->
    <requirement id="H.1">
      Refactor all sections in AdvisorsTab.tsx to use portal panel primitives:
        Panel, PanelHeader, PanelContent, SmartPanelFooter from @/ui/components/panels
      Sections affected: Top Performers panel, Rolling Flows panel, Leaderboard panel.
      The visual output should be identical to the current layout after refactor —
      this is purely a structural change to match portal conventions.
    </requirement>
    <requirement id="H.2">
      Run bunx tsc -b after refactor to confirm no type errors introduced.
      DE reviews before DT pushes.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM I — Advisors tab: Top Performers visual identity           -->
    <!-- UNBLOCKED                                                         -->
    <!-- ================================================================ -->
    <requirement id="I.1">
      Redesign the Top Performers (Top 3 highlights) panel to communicate rank and
      achievement more clearly:
        - Rank (1st / 2nd / 3rd) must be visually prominent
        - Advisor name prominent
        - Key metric (NNA for the active period) immediately readable
        - Use trophy/medal iconography or rank-badge treatment using Lucide icons
          already in the codebase (confirm which Lucide icons are available before choosing)
    </requirement>
    <requirement id="I.2">
      The redesign must work for all period toggles (QTD/YTD/1Y/3Y/Max).
      When the active period changes, Top Performers rankings update accordingly.
    </requirement>
    <requirement id="I.3">
      DE reviews the visual design before DT pushes to DEV.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM 4C — Advisors tab: New Rolling Flows visualization        -->
    <!-- BLOCKED: requires Stream B2 (DT deploys script 10 stacked bar)  -->
    <!-- ================================================================ -->
    <requirement id="4C.1">
      GATE: Do not begin 4C until DT confirms stacked_bar data is in
      advisor_rolling_flows.json S3 output (from script 10 Stream B2 deploy).
    </requirement>
    <requirement id="4C.2">
      Implement PRIMARY VIEW — Stacked Bar Chart — using the shape agreed in the
      Pattern 0 thread (2026-03-03-advisors-stacked-bar-alignment). The thread receipt
      defines: exact top-level key names in advisor_rolling_flows.json, how outflows
      are encoded (negative number? separate field? sign flag?), period key names,
      and the TypeScript interface name.
      Chart behavior:
        - X-axis: one bar per architect or implementor (per toggle)
        - Bars show inflows, outflows, NNA net per the agreed encoding
        - Sorted lowest to highest by NNA (highest performers rightmost)
        - Period toggle: per agreed period keys in thread receipt
        - Architects / Implementors toggle controls both views
      Use the agreed field names from the thread receipt, not the PRD's suggested naming.
    </requirement>
    <requirement id="4C.3">
      Implement SECONDARY VIEW — 1-Year Rolling Line Chart — using the rolling_1y shape
      agreed in the same thread receipt (2026-03-03-advisors-stacked-bar-alignment).
      The thread defines: per-advisor series structure, date+value format, and
      what date range DS committed to providing.
      Chart behavior:
        - X-axis: dates over the selected period window (period toggle = x-axis window)
        - Y-axis: 1-year rolling NNA per advisor (fixed 1Y rolling window per date point)
        - Same Architects/Implementors toggle as primary view
    </requirement>
    <requirement id="4C.4">
      View toggle (Primary / Secondary) must be clear and accessible.
      Recommended: a segmented control or tab above the chart area.
      The period toggle and Architects/Implementors toggle must remain visible in both views.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM G — Books tab implementation                               -->
    <!-- BLOCKED: requires Stream D thread receipt + Stream F deploy      -->
    <!-- ================================================================ -->
    <requirement id="G.1">
      BLOCKED: Do not begin Books tab implementation until both:
        (a) Stream D (Books design thread) receipt is available at:
            org/tier3_junior/0.4.2_RD_AdvisorIntelligence/threads/
        (b) Stream F (DT deploys advisor-publisher with L4 fields) is confirmed complete.
      The thread receipt defines the visual design brief for L2/L3/L4. Do not design
      the Books tab independently — the thread outcome is the specification.
    </requirement>
    <requirement id="G.2">
      When gates are met: implement Books tab per the design brief at
        docs/architecture/advisor_intelligence/books_tab_design_brief.md
      Scope: L2 (advisor book), L3 (relationship view), L4 (account + holdings + tax).
      Access gating: admin sees advisor selector (all advisors), advisor sees only own book.
      Use portal panel primitives throughout (consistent with Stream H refactor).
    </requirement>
    <requirement id="G.3">
      DE coordinates the Books tab implementation — RD implements visuals,
      DE handles API wiring and auth gating logic.
      Do not wire auth gating until 0.7.0_AE_CloudOps has confirmed opal-users-v2 mapping.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">C1: GEO continuous NNA shows top-8 states as series; search filters all states; click drills to cities; breadcrumb returns to state view.</criterion>
    <criterion id="2">C2: ADV continuous NNA identical to GEO but for architects and clients (post-B1 deploy).</criterion>
    <criterion id="3">C3: CLA snapshot is a clean two-color NMNC/NMEC split; no flows/NNA vocabulary; time machine periods work.</criterion>
    <criterion id="4">C4: CLA continuous is a stacked area chart with NMNC (green) and NMEC (blue) AUM over time at all grains (post-B1).</criterion>
    <criterion id="5">H: All Advisors tab sections use portal panel primitives; bunx tsc -b passes; no visual regression.</criterion>
    <criterion id="6">I: Top Performers shows clear rank (1/2/3), advisor name, and NNA with medal/badge treatment; works across all periods.</criterion>
    <criterion id="7">4C: Stacked bar primary view + rolling line secondary view implemented with period toggle and Architects/Implementors toggle.</criterion>
    <criterion id="8">G: Books tab L2/L3/L4 implemented per design brief; access gating functional (post-thread and post-F).</criterion>
    <criterion id="9">bunx tsc -b passes after each stream's changes.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Immediate start items (no blocks): C1, C3, H, I. Begin these in your first activation session.</constraint>
    <constraint>C2 and C4 blocked by DT Stream B1 deploy — check DT session log for deploy confirmation before starting.</constraint>
    <constraint>4C blocked by DT Stream B2 deploy — same pattern.</constraint>
    <constraint>G blocked by Stream D thread completion AND Stream F deploy.</constraint>
    <constraint>Do NOT use emojis in any component, comment, or log output. Plain ASCII only.</constraint>
    <constraint>DE (0.4.0_DE_ClientPlatform) must review C3 NMNC/NMEC label accuracy and Top Performers (I) before DT pushes to DEV.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "0.4.2_RD_AdvisorIntelligence: AdvisorIntelligence/{Tab} -- description"</constraint>
    <constraint>NOTE: You have 3 pending task orders (page_inventory, distribution_nomenclature_fix, continuous_view_max_window_clients_fix). Complete those before starting C1 if they conflict with the Distribution tab changes. Confirm with DE if there is overlap.</constraint>
    <constraint>NOTE: You have no prior session logs. Write a session log after your first activation and first work session. The COO needs it before scheduling the Books thread (Stream D).</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="advisor_intelligence_completion" status="pending" note="C2, C4 blocked by B1; 4C blocked by B2"/>
    <dependency agent="2.0.0_SA_COO" task="Stream-D-thread" status="pending" note="G blocked by thread completion"/>
    <dependency agent="0.4.0_DT_ClientPlatform" task="advisor_intelligence_completion" status="pending" note="G blocked by F deploy"/>
    <dependency agent="0.4.0_DS_ClientPlatform" task="advisor_intelligence_completion" status="pending" note="C3 field confirmation — DS to confirm NMNC/NMEC field names in header_metrics.json"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">DistributionTab.tsx: GEO continuous with search + drill (C1)</deliverable>
    <deliverable type="commit">DistributionTab.tsx: ADV continuous with search + drill (C2, post-B1)</deliverable>
    <deliverable type="commit">DistributionTab.tsx: CLA snapshot two-color (C3)</deliverable>
    <deliverable type="commit">DistributionTab.tsx: CLA continuous stacked area (C4, post-B1)</deliverable>
    <deliverable type="commit">AdvisorsTab.tsx: portal primitives refactor (H)</deliverable>
    <deliverable type="commit">AdvisorsTab.tsx: Top Performers visual redesign (I)</deliverable>
    <deliverable type="commit">AdvisorsTab.tsx: stacked bar primary + rolling line secondary (4C, post-B2)</deliverable>
    <deliverable type="commit">ClientsTab.tsx and related: Books tab L2/L3/L4 (G, post-thread + post-F)</deliverable>
  </deliverables>
</task_order>
```

#### continuous_view_max_window_clients_fix.md

# Task Order — Continuous View: "Total Clients" at Max Window

```xml
<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-03-02-continuous-max-window-clients</id>
    <issued_by>0.4.0_DE_ClientPlatform</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-02</date>
    <status>pending</status>
    <priority>medium</priority>
    <type>bug-fix</type>
  </metadata>

  <objective>
    In the Segment Analytics continuous view (both GEO and ADV cohorts), the left-panel
    hero metrics tile currently shows "New Clients" regardless of window selection.
    When window = "Max", this is wrong on two counts:
      1. The value displays "--" (the backend does not populate new_clients['Max']).
      2. "New Clients" is semantically incorrect for an all-time window — over all time,
         every client is a "new" client. The correct label is "Total Clients" and the
         correct value is the current total relationship count.

    Fix: make the tile window-aware.
      - 1Y / 3Y windows:  label = "New Clients",    value = new_clients[window]  (existing)
      - Max window:       label = "Total Clients",  value = current total relationships
  </objective>

  <problem>
    File: portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx
    Location: ContinuousChartView component, ~lines 802-807

    Current code:
      &lt;div className="bg-white/5 rounded-lg p-2.5 text-center mb-4"&gt;
        &lt;p className="text-sm font-bold text-white"&gt;
          {data?.metadata?.new_clients?.[window as string] ?? '--'}
        &lt;/p&gt;
        &lt;p className="text-[10px] text-white/40 mt-0.5"&gt;New Clients&lt;/p&gt;
      &lt;/div&gt;

    Root cause:
      data.metadata.new_clients is a Record&lt;string, number&gt; keyed by window string.
      The backend populates keys '1Y' and '3Y' but NOT 'Max', so window='Max' always
      falls through to '--'. Even if it were populated, "New Clients" over all time
      is meaningless — it is equivalent to total clients.

    Affected views:
      Both GEO and ADV continuous AUA views — they share the same ContinuousChartView
      component, so the fix is in one place.
  </problem>

  <fix>
    Three changes required:

    1. Add totalClients?: number to ContinuousChartViewProps interface.
       (~line 658 — interface definition)

    2. Pass totalClients at the ContinuousChartView call site.
       (~line 396-402 in DistributionTab — the JSX element)
       Derive totalClients from analyticsData (available in DistributionTab scope):
         const cohortView = cohort === 'geo'
           ? analyticsData?.views?.geo
           : analyticsData?.views?.adv
         totalClients = cohortView?.current?.metrics?.client_count
                        ?? cohortView?.metrics?.client_count

    3. Make the tile window-aware in ContinuousChartView.
       (~lines 802-807)
       When window === 'Max': label = "Total Clients", value = totalClients ?? '--'
       When window !== 'Max': label = "New Clients",   value = data?.metadata?.new_clients?.[window] ?? '--'
  </fix>

  <files_to_modify>

    <file path="portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx">
      <description>
        Three locations to edit, all within DistributionTab.tsx.
      </description>

      <change id="1">
        <location>
          ~Lines 658-664 — ContinuousChartViewProps interface
          (search: "interface ContinuousChartViewProps")
        </location>
        <current>
interface ContinuousChartViewProps {
  data: CumulativeChartResponse | null
  cohort: CohortOption
  metric: DistMetricOption
  window: ChartWindowOption
  categoryColorMap: Record&lt;string, string&gt;
}
        </current>
        <new>
interface ContinuousChartViewProps {
  data: CumulativeChartResponse | null
  cohort: CohortOption
  metric: DistMetricOption
  window: ChartWindowOption
  categoryColorMap: Record&lt;string, string&gt;
  totalClients?: number
}
        </new>
        <rationale>Adds the optional total relationship count for the Max-window tile.</rationale>
      </change>

      <change id="2">
        <location>
          ~Line 666 — ContinuousChartView function signature
          (search: "function ContinuousChartView({")
        </location>
        <current>
function ContinuousChartView({ data, cohort, metric, window, categoryColorMap }: ContinuousChartViewProps) {
        </current>
        <new>
function ContinuousChartView({ data, cohort, metric, window, categoryColorMap, totalClients }: ContinuousChartViewProps) {
        </new>
        <rationale>Destructures the new prop.</rationale>
      </change>

      <change id="3">
        <location>
          ~Lines 396-402 — ContinuousChartView JSX call site in DistributionTab
          (search: "&lt;ContinuousChartView" — the component usage, not the definition)
        </location>
        <current>
            &lt;ContinuousChartView
              data={chartData ?? null}
              cohort={cohort}
              metric={metric}
              window={window}
              categoryColorMap={categoryColorMap}
            /&gt;
        </current>
        <new>
            &lt;ContinuousChartView
              data={chartData ?? null}
              cohort={cohort}
              metric={metric}
              window={window}
              categoryColorMap={categoryColorMap}
              totalClients={
                cohort === 'geo'
                  ? (analyticsData?.views?.geo?.current?.metrics?.client_count
                     ?? analyticsData?.views?.geo?.metrics?.client_count)
                  : (analyticsData?.views?.adv?.current?.metrics?.client_count
                     ?? analyticsData?.views?.adv?.metrics?.client_count)
              }
            /&gt;
        </new>
        <rationale>
          analyticsData and cohort are both in scope in DistributionTab at this point.
          Derives total relationship count from the current period snapshot metrics.
          The ?? fallback handles both the legacy PartnerAnalyticsView shape (.metrics)
          and the current PartnerAnalyticsViewWithPeriods shape (.current.metrics).
        </rationale>
      </change>

      <change id="4">
        <location>
          ~Lines 802-807 — "New Clients" tile inside ContinuousChartView
          (search: the bg-white/5 div with "New Clients" label text)
        </location>
        <current>
        &lt;div className="bg-white/5 rounded-lg p-2.5 text-center mb-4"&gt;
          &lt;p className="text-sm font-bold text-white"&gt;
            {data?.metadata?.new_clients?.[window as string] ?? '--'}
          &lt;/p&gt;
          &lt;p className="text-[10px] text-white/40 mt-0.5"&gt;New Clients&lt;/p&gt;
        &lt;/div&gt;
        </current>
        <new>
        &lt;div className="bg-white/5 rounded-lg p-2.5 text-center mb-4"&gt;
          &lt;p className="text-sm font-bold text-white"&gt;
            {window === 'Max'
              ? (totalClients?.toLocaleString() ?? '--')
              : (data?.metadata?.new_clients?.[window as string]?.toLocaleString() ?? '--')}
          &lt;/p&gt;
          &lt;p className="text-[10px] text-white/40 mt-0.5"&gt;
            {window === 'Max' ? 'Total Clients' : 'New Clients'}
          &lt;/p&gt;
        &lt;/div&gt;
        </new>
        <rationale>
          Max window: shows total relationship count with "Total Clients" label.
            - Semantically correct: over all time every client is cumulative total.
            - Fixes the '--' display (new_clients['Max'] is never populated by backend).
          1Y / 3Y: unchanged — shows new_clients[window] with "New Clients" label.
          .toLocaleString() added to both paths for consistent number formatting.
        </rationale>
      </change>
    </file>

  </files_to_modify>

  <requirements>
    <requirement id="1">
      Read DistributionTab.tsx before editing. Use offset reads:
      - ~line 658 for Changes 1-2 (interface + function signature)
      - ~line 390 for Change 3 (call site)
      - ~line 800 for Change 4 (tile)
      Use the Edit tool — never sed or heredoc.
    </requirement>
    <requirement id="2">
      Apply all 4 changes as a unit. Change 3 and Change 4 are the user-visible
      fix; Changes 1 and 2 are the required plumbing.
    </requirement>
    <requirement id="3">
      The type access paths for totalClients in Change 3 use optional chaining
      with a ?? fallback to handle both the legacy PartnerAnalyticsView shape
      (direct .metrics.client_count) and the current PartnerAnalyticsViewWithPeriods
      shape (.current.metrics.client_count). Verify the actual types at read time
      and adjust if needed — the intent is to get the current total relationship count
      for the selected cohort (geo or adv).
    </requirement>
    <requirement id="4">
      analyticsData is the PartnerAnalyticsResponse prop passed into DistributionTab.
      It is in scope at the ContinuousChartView call site (line ~396). You are not
      introducing a new data fetch or state variable.
    </requirement>
    <requirement id="5">
      Do not change the 1Y or 3Y behavior. The existing new_clients[window] path
      is correct for those windows.
    </requirement>
    <requirement id="6">
      Commit with tag:
      "0.4.0_DE_ClientPlatform: fix continuous view — Total Clients at Max window"
      Do not git push — DT is the QA gate.
    </requirement>
    <requirement id="7">
      Write a session log at:
      logs/sessions/2026-03-02/react_designer/continuous_view_max_window_clients_fix.md
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      ContinuousChartViewProps interface has totalClients?: number field.
    </criterion>
    <criterion id="2">
      ContinuousChartView function signature destructures totalClients.
    </criterion>
    <criterion id="3">
      At the call site, totalClients is derived from analyticsData.views[cohort]
      current relationship count (with legacy shape fallback).
    </criterion>
    <criterion id="4">
      When window = "Max":
        - Tile label = "Total Clients"
        - Tile value = current total relationship count (not '--')
    </criterion>
    <criterion id="5">
      When window = "1Y" or "3Y":
        - Tile label = "New Clients" (unchanged)
        - Tile value = new_clients[window] from metadata (unchanged)
    </criterion>
    <criterion id="6">
      Both GEO and ADV cohorts exhibit the correct behavior (they share
      ContinuousChartView so this is automatic).
    </criterion>
    <criterion id="7">
      Changes committed. Session log written.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>
      Do not change the window toggle options (1Y, 3Y, Max) or their ordering.
    </constraint>
    <constraint>
      Do not change any other hero metric tiles (the gain-since-start tile
      or growth-rate tile in the 2-column grid above). Only the "New Clients"
      / "Total Clients" tile is in scope.
    </constraint>
    <constraint>Do not push to remote — DT deploys.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="code-commit">
      Changes to portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx
      (4 changes: ContinuousChartViewProps, function signature, call site prop,
      window-aware tile label + value)
    </deliverable>
    <deliverable type="session-log">
      logs/sessions/2026-03-02/react_designer/continuous_view_max_window_clients_fix.md
    </deliverable>
  </deliverables>
</task_order>
```

#### distribution_nomenclature_fix.md

# Task Order — Distribution Chart Nomenclature Fix: AdvisorIntelligence

```xml
<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-03-02-distribution-nomenclature-advisor-intelligence</id>
    <issued_by>0.4.0_DE_ClientPlatform</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-02</date>
    <status>pending</status>
    <priority>high</priority>
    <type>nomenclature-fix</type>
  </metadata>

  <objective>
    Fix all axis labels, tooltip labels, metrics tile labels, and footnotes in
    SnapshotDistributionChart and SnapshotDistributionMetrics to use accurate,
    mode-aware nomenclature.

    The chart operates in two fundamentally different data modes, each with its
    own correct unit of analysis:

    - AUA mode  (default, isNnaMode=false):
        Histogram bins individual Black Diamond *account* balances.
        Data source: gold/account_performance.parquet (account_id level).
        One observation = one funded account.
        Canonical unit: "account".

    - NNA mode  (isNnaMode=true):
        Histogram bins each *relationship's* period NNA.
        Data source: client_performance.parquet (relationship_id level).
        One observation = one relationship (relationship_id).
        Canonical unit: "relationship".

    Current labels ("Client AUA", "Client Count", "Number of Clients", "Total Clients")
    are wrong in both modes:
    - In AUA mode: data is account-level but labels imply relationship-level.
    - In NNA mode: "client" is informal and non-specific; "relationship" is the
      correct BD term that matches the underlying relationship_id key.

    ModelPortfolios (SmartX data) uses "Holdings" for the equivalent chart.
    AdvisorIntelligence (Black Diamond data) must NOT copy "holdings" — the correct
    BD term is "account". The formatting pattern (consistent label + tooltip + footnote)
    is the same; only the vocabulary differs.
  </objective>

  <data_context>
    Confirmed by reading data/black_diamond/scripts/gold/09_generate_partner_analytics.py:

    AUA distribution (lines 584, 621-623):
      acct_arch = acct_perf_day (gold/account_performance.parquet)
      arch_accts = acct_arch[acct_arch['architect'] == arch]
      adv_dist   = calculate_distribution_stats(arch_accts['total_aua'])
      One row = one Black Diamond account (account_id level).
      DistributionStats.count = number of funded accounts in that segment.

    NNA distribution (line 396-400, 508-509):
      rel_nna = _compute_rel_period_nna(cp_end, cp_start)
        returns DataFrame with columns: relationship_id, period_nna
      calculate_nna_distribution_stats(rel_nna['period_nna'])
      One row = one relationship (relationship_id level).
      DistributionStats.count = number of relationships.

    ModelPortfolios reference (AccountDistributionChart.tsx):
      Y-axis:       "Number of Holdings"    (SmartX-specific vocabulary)
      X-axis:       "Holding Size"          (SmartX-specific vocabulary)
      Tooltip row 1: "Holding Size"
      Tooltip row 2: "Account Count"        (note: row 2 already says "Account")
      Metrics tile: "Total Holdings"        (SmartX-specific vocabulary)
      Footnote:     "Excludes {N} newly opened holdings with $0 balance (unfunded)."

    AdvisorIntelligence must NOT use "Holdings" — that is SmartX terminology.
    The correct BD vocabulary is "account" (singular/plural) for AUA mode and
    "relationship" for NNA mode.
  </data_context>

  <nomenclature_standard>
    AUA mode (isNnaMode = false) — account-level data:
      Y-axis label:       "Number of Accounts"
      X-axis label:       "Account Size"
      Tooltip row 1 key:  "Account Size"
      Tooltip row 2 key:  "Account Count"
      Metrics tile label: "Total Accounts"
      Footnote amber:     "Excludes accounts with $0 balance (unfunded)."
      Footnote muted:     " Distribution reflects funded accounts only, log-spaced bins."

    NNA mode (isNnaMode = true) — relationship-level data:
      Y-axis label:       "Number of Relationships"
      X-axis label:       "Period NNA"
      Tooltip row 1 key:  "NNA Range"
      Tooltip row 2 key:  "Relationship Count"
      Metrics tile label: "Total Relationships"
      Footnote:           (keep existing NNA footnote — no change)
  </nomenclature_standard>

  <files_to_modify>

    <file path="portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx">
      <description>
        Eleven changes across four locations:
        (A) SnapshotDistributionChartProps interface + function signature (~lines 1696-1702)
        (B) SnapshotDistributionChart body — axis labels + tooltip (~lines 1759-1812)
        (C) SnapshotDistributionMetrics function signature + primary tile (~lines 1853-1877)
        (D) Call sites in SnapshotDistributionView + right-partition footnote (~lines 1444-1462)
      </description>

      <!-- ================================================================ -->
      <!-- A. SnapshotDistributionChartProps + function signature           -->
      <!-- ================================================================ -->

      <change id="1">
        <location>~Lines 1696-1700 — SnapshotDistributionChartProps interface</location>
        <current>
interface SnapshotDistributionChartProps {
  data: DistributionStats
  accentColor?: string
  globalMaxCount?: number
}
        </current>
        <new>
interface SnapshotDistributionChartProps {
  data: DistributionStats
  accentColor?: string
  globalMaxCount?: number
  isNnaMode?: boolean
}
        </new>
        <rationale>Adds the mode flag so the chart can render mode-aware labels.</rationale>
      </change>

      <change id="2">
        <location>~Line 1702 — SnapshotDistributionChart function signature</location>
        <current>
function SnapshotDistributionChart({ data, accentColor = '#5e72e4', globalMaxCount }: SnapshotDistributionChartProps) {
        </current>
        <new>
function SnapshotDistributionChart({ data, accentColor = '#5e72e4', globalMaxCount, isNnaMode = false }: SnapshotDistributionChartProps) {
        </new>
        <rationale>Destructures the new prop with a safe default of false (AUA mode).</rationale>
      </change>

      <!-- ================================================================ -->
      <!-- B. SnapshotDistributionChart body — axis labels + tooltip        -->
      <!-- ================================================================ -->

      <change id="3">
        <location>
          ~Line 1760 — Y-axis label text inside SnapshotDistributionChart
          (the span inside the absolute-positioned vertical div,
           search context: writingMode vertical-rl, text "Number of Clients")
        </location>
        <current>
          Number of Clients
        </current>
        <new>
          {isNnaMode ? 'Number of Relationships' : 'Number of Accounts'}
        </new>
        <rationale>
          AUA mode: counts individual Black Diamond accounts.
          NNA mode: counts relationships (relationship_id level).
          "Clients" was wrong for both.
        </rationale>
      </change>

      <change id="4">
        <location>
          ~Line 1767 — X-axis label span inside SnapshotDistributionChart
          (absolute-positioned div at bottom, search: "Client AUA")
        </location>
        <current>
          &lt;span className="text-[11px] text-white/50"&gt;Client AUA&lt;/span&gt;
        </current>
        <new>
          &lt;span className="text-[11px] text-white/50"&gt;{isNnaMode ? 'Period NNA' : 'Account Size'}&lt;/span&gt;
        </new>
        <rationale>
          AUA mode: x-axis is the size of an individual account ("Account Size").
          NNA mode: x-axis is the relationship's period NNA ("Period NNA").
        </rationale>
      </change>

      <change id="5">
        <location>
          ~Line 1807 — Tooltip row 1 label inside RechartsTooltip
          (search: the span with text "Client AUA" — first row in tooltip content)
        </location>
        <current>
                      &lt;span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm"&gt;Client AUA&lt;/span&gt;
        </current>
        <new>
                      &lt;span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm"&gt;{isNnaMode ? 'NNA Range' : 'Account Size'}&lt;/span&gt;
        </new>
        <rationale>Tooltip row 1 names the x-axis bin. Must match x-axis label.</rationale>
      </change>

      <change id="6">
        <location>
          ~Line 1811 — Tooltip row 2 label inside RechartsTooltip
          (search: the span with text "Client Count" — second row in tooltip content)
        </location>
        <current>
                      &lt;span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm"&gt;Client Count&lt;/span&gt;
        </current>
        <new>
                      &lt;span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm"&gt;{isNnaMode ? 'Relationship Count' : 'Account Count'}&lt;/span&gt;
        </new>
        <rationale>
          AUA mode: the bar height is a count of accounts in that size bin.
          "Account Count" matches ModelPortfolios tooltip row 2 exactly.
          NNA mode: count is relationships.
        </rationale>
      </change>

      <!-- ================================================================ -->
      <!-- C. SnapshotDistributionMetrics — function signature + tile label -->
      <!-- ================================================================ -->

      <change id="7">
        <location>
          ~Line 1853 — SnapshotDistributionMetrics function signature
          (search: "function SnapshotDistributionMetrics({ data, currentData }")
        </location>
        <current>
function SnapshotDistributionMetrics({ data, currentData }: { data: DistributionStats; currentData?: DistributionStats | null }) {
        </current>
        <new>
function SnapshotDistributionMetrics({ data, currentData, isNnaMode = false }: { data: DistributionStats; currentData?: DistributionStats | null; isNnaMode?: boolean }) {
        </new>
        <rationale>Adds mode flag so the primary tile label can be mode-aware.</rationale>
      </change>

      <change id="8">
        <location>
          ~Lines 1874-1878 — Primary tile inside SnapshotDistributionMetrics
          (search: comment "Total Clients" and the div containing it)
        </location>
        <current>
        {/* Total Clients */}
        &lt;div className="flex flex-col items-center px-4 py-1.5 rounded bg-[hsl(253,74%,85%)]/15 border border-[hsl(253,74%,85%)]/40 min-w-[100px]"&gt;
          &lt;div className="text-xs text-white/90 font-semibold mb-1"&gt;Total Clients&lt;/div&gt;
          &lt;div className="text-lg font-bold text-white"&gt;{data.count.toLocaleString()}&lt;/div&gt;
        &lt;/div&gt;
        </current>
        <new>
        {/* Total Accounts / Total Relationships */}
        &lt;div className="flex flex-col items-center px-4 py-1.5 rounded bg-[hsl(253,74%,85%)]/15 border border-[hsl(253,74%,85())]/40 min-w-[100px]"&gt;
          &lt;div className="text-xs text-white/90 font-semibold mb-1"&gt;{isNnaMode ? 'Total Relationships' : 'Total Accounts'}&lt;/div&gt;
          &lt;div className="text-lg font-bold text-white"&gt;{data.count.toLocaleString()}&lt;/div&gt;
        &lt;/div&gt;
        </new>
        <rationale>
          AUA mode: count is funded Black Diamond accounts → "Total Accounts".
          NNA mode: count is relationships → "Total Relationships".
          data.count is correct for both — only the label text changes.
        </rationale>
      </change>

      <!-- ================================================================ -->
      <!-- D. Call sites + right-partition footnote                         -->
      <!-- ================================================================ -->

      <change id="9">
        <location>
          ~Line 1444 — SnapshotDistributionChart JSX element inside SnapshotDistributionView
          (search: "&lt;SnapshotDistributionChart" — the component usage, not its definition)
        </location>
        <current>
              &lt;SnapshotDistributionChart
                data={distributionData}
                accentColor={selectedSegment?.color || parentSegment?.color || 'hsl(var(--primary))'}
                globalMaxCount={globalMaxCount}
              /&gt;
        </current>
        <new>
              &lt;SnapshotDistributionChart
                data={distributionData}
                accentColor={selectedSegment?.color || parentSegment?.color || 'hsl(var(--primary))'}
                globalMaxCount={globalMaxCount}
                isNnaMode={isNnaMode}
              /&gt;
        </new>
        <rationale>
          isNnaMode is already a const in SnapshotDistributionView scope
          (derived from: const isNnaMode = metric === 'nna').
          Threading it into the chart component so it can render mode-aware labels.
        </rationale>
      </change>

      <change id="10">
        <location>
          ~Line 1451 — SnapshotDistributionMetrics JSX element inside SnapshotDistributionView
          (search: "&lt;SnapshotDistributionMetrics data={distributionData}")
        </location>
        <current>
              &lt;SnapshotDistributionMetrics data={distributionData} currentData={currentDistributionData} /&gt;
        </current>
        <new>
              &lt;SnapshotDistributionMetrics data={distributionData} currentData={currentDistributionData} isNnaMode={isNnaMode} /&gt;
        </new>
        <rationale>Threads the mode flag into the metrics component for the tile label.</rationale>
      </change>

      <change id="11">
        <location>
          ~Lines 1457-1461 — AUA branch of the right-partition footnote
          (search: amber span "Excludes accounts with $0 balance (unfunded)."
           and the muted span " Distribution uses log-spaced bins across funded accounts only.")
        </location>
        <current>
                    &lt;span className="text-amber-400 font-bold"&gt;Excludes accounts with $0 balance (unfunded).&lt;/span&gt;
                    &lt;span className="text-white/40"&gt; Distribution uses log-spaced bins across funded accounts only.&lt;/span&gt;
        </current>
        <new>
                    &lt;span className="text-amber-400 font-bold"&gt;Excludes accounts with $0 balance (unfunded).&lt;/span&gt;
                    &lt;span className="text-white/40"&gt; Distribution reflects funded accounts only, log-spaced bins.&lt;/span&gt;
        </new>
        <rationale>
          The amber span is already correct — "accounts" is right.
          Only the muted span changes: shorter phrasing, consistent with ModelPortfolios
          footnote structure ("reflects funded accounts only" instead of the more wordy
          "uses log-spaced bins across funded accounts only").
        </rationale>
      </change>
    </file>

  </files_to_modify>

  <requirements>
    <requirement id="1">
      Read DistributionTab.tsx before editing. Use offset reads:
      - ~line 1696 for Changes 1-2 (interface + function signature)
      - ~line 1755 for Changes 3-6 (axis labels + tooltip body)
      - ~line 1853 for Changes 7-8 (metrics component)
      - ~line 1440 for Changes 9-11 (call sites + footnote)
      Use the Edit tool — never sed or heredoc.
    </requirement>
    <requirement id="2">
      Apply all 11 changes. Do not apply a subset.
      Changes 3-6 and 8 are the most visible to users. Changes 1-2 and 7 are
      the prerequisite interface wiring. Changes 9-11 are the connective tissue.
    </requirement>
    <requirement id="3">
      isNnaMode is already declared in SnapshotDistributionView scope as:
        const isNnaMode = metric === 'nna'
      You are NOT introducing a new variable. You are only threading it as a prop
      into SnapshotDistributionChart (Change 9) and SnapshotDistributionMetrics
      (Change 10), then consuming it inside those functions (Changes 3-8).
    </requirement>
    <requirement id="4">
      Do not change the NNA footnote text (the isNnaMode=true branch, ~line 1454).
      Only the AUA branch text is updated (Change 11 — muted span wording only).
    </requirement>
    <requirement id="5">
      Do not change the right-partition section header (distributionLabel h4),
      the help tooltip on that header, or the donut legend client_count labels.
      Those are in separate scope and are not part of this task.
    </requirement>
    <requirement id="6">
      Do not change any percentile tile (P10/P25/Median/P75/P90) in
      SnapshotDistributionMetrics. Only the primary "Total" tile (Change 8) changes.
    </requirement>
    <requirement id="7">
      ModelPortfolios uses data.account_count; DistributionTab uses data.count.
      These are different TypeScript interface shapes (aum endpoint vs AI types).
      Do NOT attempt to change data.count to data.account_count. Display label
      changes only — field access is untouched.
    </requirement>
    <requirement id="8">
      Commit with tag:
      "0.4.0_DE_ClientPlatform: fix distribution chart nomenclature — accounts/relationships"
      Do not git push — DT is the QA gate.
    </requirement>
    <requirement id="9">
      Write a session log at:
      logs/sessions/2026-03-02/react_designer/distribution_nomenclature_fix.md
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      SnapshotDistributionChartProps has isNnaMode?: boolean field.
    </criterion>
    <criterion id="2">
      In AUA mode (isNnaMode=false):
      Y-axis = "Number of Accounts"
      X-axis = "Account Size"
      Tooltip row 1 = "Account Size"
      Tooltip row 2 = "Account Count"
    </criterion>
    <criterion id="3">
      In NNA mode (isNnaMode=true):
      Y-axis = "Number of Relationships"
      X-axis = "Period NNA"
      Tooltip row 1 = "NNA Range"
      Tooltip row 2 = "Relationship Count"
    </criterion>
    <criterion id="4">
      SnapshotDistributionMetrics primary tile:
      AUA mode = "Total Accounts", NNA mode = "Total Relationships".
    </criterion>
    <criterion id="5">
      Right-partition AUA footnote muted span reads:
      " Distribution reflects funded accounts only, log-spaced bins."
    </criterion>
    <criterion id="6">
      isNnaMode={isNnaMode} is present on both
      &lt;SnapshotDistributionChart&gt; and &lt;SnapshotDistributionMetrics&gt; call sites.
    </criterion>
    <criterion id="7">
      No other labels, data fields, percentile tiles, section headers,
      or donut legend text changed.
    </criterion>
    <criterion id="8">
      Changes committed. Session log written.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>
      Do not use "Holdings" anywhere — that is SmartX/ModelPortfolios vocabulary.
      AdvisorIntelligence data is Black Diamond. The correct terms are
      "account" (AUA mode) and "relationship" (NNA mode).
    </constraint>
    <constraint>
      Change 8 edits the JSX comment and the tile label text only.
      The className strings on the surrounding divs are identical — match them
      exactly when constructing the old_string for the Edit tool.
    </constraint>
    <constraint>Do not push to remote — DT deploys.</constraint>
    <constraint>
      Changes 3-6 use JSX expressions ({isNnaMode ? '...' : '...'}) inside
      text nodes. Verify JSX is syntactically valid after each edit.
    </constraint>
  </constraints>

  <deliverables>
    <deliverable type="code-commit">
      Changes to portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx
      (11 changes: SnapshotDistributionChartProps, SnapshotDistributionChart body,
      SnapshotDistributionMetrics, call sites, AUA footnote)
    </deliverable>
    <deliverable type="session-log">
      logs/sessions/2026-03-02/react_designer/distribution_nomenclature_fix.md
    </deliverable>
  </deliverables>
</task_order>
```

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

#### xtick_spacing_fix.md

# Task Order — X-Tick Spacing Fix: AdvisorIntelligence

```xml
<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-03-02-xtick-spacing-advisor-intelligence</id>
    <issued_by>0.4.0_DE_ClientPlatform</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-02</date>
    <status>pending</status>
    <priority>high</priority>
    <type>bug-fix</type>
  </metadata>

  <objective>
    Make the DistributionTab split layout in AdvisorIntelligence visually canonical
    with the equivalent split layout in ModelPortfolios. This means:
    (a) the donut (left partition) and bell curve (right partition) containers are
        the same height, and
    (b) the metrics rows below each chart partition sit at the same vertical level.
    Root cause is four structural mismatches vs ModelPortfolios, not purely a tick
    spacing issue.
  </objective>

  <problem>
    Four differences vs ModelPortfolios cause the visual disparity:

    1. DONUT CONTAINER HEIGHT (primary cause of layout misalignment):
       DistributionTab wraps the ApexCharts donut (left partition) in h-[380px].
       ModelPortfolios wraps its donut in h-[450px].
       This 70px mismatch means the left partition is shorter than the right, so
       the SnapshotDistributionMetrics row starts at a different Y position than
       the donut-side content — the two partitions are not level.

    2. BELL CURVE CONTAINER HEIGHT (mirrors problem 1):
       DistributionTab wraps SnapshotDistributionChart (right partition) in h-[380px].
       ModelPortfolios wraps AccountDistributionChart in h-[450px].
       The 70px deficit directly shrinks the plot area and makes the chart cramped.

    3. XAXIS HEIGHT (cause of gap between tick labels and metrics):
       SnapshotDistributionChart uses XAxis height={72}.
       AccountDistributionChart uses XAxis height={50}.
       The extra 22px allocates a dead strip of space below the axis line — the tick
       labels at negative angle extend upward (not downward) so that strip is visually
       empty, creating the perceived gap between the chart and the metrics row below.

    4. TICK MARGIN (secondary — same as other charts):
       No tickMargin set, so labels are flush against the axis line.
  </problem>

  <fix_standard>
    Four changes required to make DistributionTab canonical with ModelPortfolios:
    1. Donut container height: h-[380px] → h-[450px]   (DistributionTab.tsx ~line 1266)
    2. Bell curve container height: h-[380px] → h-[450px]  (DistributionTab.tsx ~line 1443)
    3. XAxis height: 72 → 50                            (SnapshotDistributionChart XAxis)
    4. tickMargin={16}                                  (SnapshotDistributionChart XAxis)
    The bottom margin change (15 → 50) also stands — with the container now at 450px,
    bottom=50 gives a plot area of 320px (identical to ModelPortfolios after its own fix:
    450 - 30 - 50 - 50 = 320).
    With both partitions at h-[450px], the SnapshotDistributionMetrics row and the
    donut-side quarter strip sit at identical vertical positions — matching ModelPortfolios.
  </fix_standard>

  <files_to_modify>

    <file path="portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx">
      <description>
        Four locations to edit:
        (1) the donut container div ~line 1266 (LEFT partition),
        (2) the bell curve container div ~line 1443 (RIGHT partition),
        (3) SnapshotDistributionChart AreaChart margin ~line 1764, and
        (4) SnapshotDistributionChart XAxis ~lines 1772-1780.
        All four are inside DistributionTab.tsx.
      </description>

      <change id="1">
        <location>
          ~Line 1266 — donut container div in the LEFT partition
          (search context: directly inside
           "&lt;div className="w-full max-w-[700px] flex flex-col gap-6 items-center"&gt;"
           in the LEFT PARTITION section, wrapping the ApexCharts donut + legend row)
        </location>
        <current>&lt;div className="h-[380px] flex items-center justify-center relative"&gt;</current>
        <new>&lt;div className="h-[450px] flex items-center justify-center relative"&gt;</new>
        <rationale>
          ModelPortfolios wraps its donut in h-[450px]. With the left partition at
          h-[380px] and the right at h-[450px] (after Change 2), the two partitions
          are mismatched in height — the SnapshotDistributionMetrics row starts 70px
          higher than the donut-side content. Setting both to h-[450px] levels them.
        </rationale>
      </change>

      <change id="2">
        <location>
          ~Line 1443 — chart container div wrapping SnapshotDistributionChart
          (search context: directly inside
           "&lt;div className="w-full max-w-[700px] flex flex-col gap-6 items-center"&gt;"
           in the RIGHT PARTITION section)
        </location>
        <current>&lt;div className="h-[380px] w-full min-w-0"&gt;</current>
        <new>&lt;div className="h-[450px] w-full min-w-0"&gt;</new>
        <rationale>
          ModelPortfolios uses h-[450px]. The 70px deficit is the primary cause of
          the cramped plot area. This is the most important change for the bell curve.
        </rationale>
      </change>

      <change id="3">
        <location>
          ~Line 1764 — AreaChart margin prop inside SnapshotDistributionChart
          (search context: the AreaChart directly under
           "&lt;ResponsiveContainer width="100%" height="100%"&gt;" inside
           SnapshotDistributionChart)
        </location>
        <current>margin={{ top: 30, right: 10, left: 0, bottom: 15 }}</current>
        <new>margin={{ top: 30, right: 10, left: 0, bottom: 50 }}</new>
        <rationale>
          With h-[450px] container, bottom=50 yields plot area of 320px
          (450 - 30 - 50 - 50 = 320) — identical to ModelPortfolios after its fix.
        </rationale>
      </change>

      <change id="4">
        <location>
          ~Lines 1772-1780 — XAxis inside SnapshotDistributionChart AreaChart
        </location>
        <current>
          &lt;XAxis
            dataKey="bin"
            stroke="rgba(255,255,255,0.5)"
            tick={{ fontSize: 7, fill: 'rgba(255,255,255,0.7)' }}
            angle={-55}
            textAnchor="end"
            height={72}
            interval={0}
          /&gt;
        </current>
        <new>
          &lt;XAxis
            dataKey="bin"
            stroke="rgba(255,255,255,0.5)"
            tick={{ fontSize: 7, fill: 'rgba(255,255,255,0.7)' }}
            angle={-55}
            textAnchor="end"
            height={50}
            interval={0}
            tickMargin={16}
          /&gt;
        </new>
        <rationale>
          height: 72 → 50 — matches AccountDistributionChart. The 22px reduction
          eliminates the dead strip below the axis line (tick labels at negative angle
          extend upward, not downward, so that strip was visually empty whitespace).
          tickMargin={16} — adds gap between axis tick line and label text.
        </rationale>
      </change>
    </file>

  </files_to_modify>

  <requirements>
    <requirement id="1">
      Read DistributionTab.tsx before editing. The file is very large.
      Read ~line 1260 for the donut container div (Change 1).
      Read ~line 1440 for the bell curve container div (Change 2).
      Read ~line 1690 onward for SnapshotDistributionChart (Changes 3 and 4).
      Use the Edit tool — never sed or heredoc.
    </requirement>
    <requirement id="2">
      Apply all 4 changes. Changes 1 and 2 (both container heights) are the most
      important — they are what levels the two partitions. Do not apply a subset.
    </requirement>
    <requirement id="3">
      The two h-[380px] → h-[450px] changes are on different divs with different
      className strings:
      - Change 1 (donut): "h-[380px] flex items-center justify-center relative"
      - Change 2 (bell curve): "h-[380px] w-full min-w-0"
      Do not confuse them. Match on the full className string for each Edit call.
    </requirement>
    <requirement id="4">
      Do not touch any other container divs, chart components, or XAxis elements
      in DistributionTab.tsx. The only div heights being changed are the two at
      ~line 1266 and ~line 1443. No other heights, no other charts.
    </requirement>
    <requirement id="5">
      Do NOT touch the other XAxis elements in DistributionTab.tsx:
      - ComposedChart XAxis at ~line 546 (continuous view) — not in scope
      - AreaChart XAxis at ~line 862 (daily NNA chart) — not in scope
      - ClaSnapshotView XAxis at ~line 2067 (CLA diverging bar) — not in scope
    </requirement>
    <requirement id="6">
      Commit with tag: "0.4.0_DE_ClientPlatform: canonicalize AdvisorIntelligence distribution layout"
      Do not git push — DT is the QA gate.
    </requirement>
    <requirement id="7">
      Write a session log at:
      logs/sessions/2026-03-02/react_designer/xtick_spacing_advisor_intelligence.md
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      Donut container div (LEFT partition, ~line 1266) is h-[450px] (was h-[380px]).
    </criterion>
    <criterion id="2">
      Bell curve container div (RIGHT partition, ~line 1443) is h-[450px] (was h-[380px]).
    </criterion>
    <criterion id="3">
      SnapshotDistributionChart AreaChart bottom margin = 50.
    </criterion>
    <criterion id="4">
      SnapshotDistributionChart XAxis height = 50 (was 72). tickMargin={16}.
    </criterion>
    <criterion id="5">
      Resulting plot area = 450 - 30 - 50 - 50 = 320px. Matches ModelPortfolios.
    </criterion>
    <criterion id="6">
      Both partitions at h-[450px]: SnapshotDistributionMetrics and donut-side
      quarter strip sit at identical vertical positions — layout mirrors ModelPortfolios.
    </criterion>
    <criterion id="7">
      No other container heights or XAxis elements in DistributionTab.tsx modified.
    </criterion>
    <criterion id="8">
      Changes committed. Session log written.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Change 1 must target the div at ~line 1266 (className contains "flex items-center justify-center relative"). Change 2 must target the div at ~line 1443 (className contains "w-full min-w-0"). Do not swap them.</constraint>
    <constraint>Do not change angle, textAnchor, fontSize, or interval on the XAxis.</constraint>
    <constraint>Do not push to remote — DT deploys.</constraint>
    <constraint>
      This fix is being applied in parallel with task order
      0.4.0_DE_ClientPlatform-2026-03-02-xtick-spacing-model-portfolios (issued to 0.4.1_RD_ModelPortfolios).
      Both fixes must use identical tickMargin={16} standard for cross-page uniformity.
    </constraint>
  </constraints>

  <deliverables>
    <deliverable type="code-commit">
      Changes to portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx (4 changes:
      donut container height, bell curve container height, AreaChart bottom margin,
      XAxis height + tickMargin)
    </deliverable>
    <deliverable type="session-log">
      logs/sessions/2026-03-02/react_designer/xtick_spacing_advisor_intelligence.md
    </deliverable>
  </deliverables>
</task_order>
```


### 0.4.2_RD_AdvisorIntelligence -- Recent Commits

# Recent commits by 0.4.2_RD_AdvisorIntelligence

076e1120 0.4.0_DT_ClientPlatform: enrich Pod 4 (ClientPlatform) agent prompts with source-grounded context
b5ace0c0 org: quality audit -- fix bugs, upgrade thin profiles, seed missing deliverables
b331d3e6 feat(org): 0.4.0_DE_ClientPlatform — continuous view Max window clients fix task order
c08effac feat(org): 0.4.0_DE_ClientPlatform wave 2 — pod inventory + RD task orders
42f99352 logs: 0.4.2_RD_AdvisorIntelligence distribution nomenclature fix session log
2f8de475 docs(org): add xtick fix addendum for 0.4.2_RD_AdvisorIntelligence
4e046836 logs: 0.4.2_RD_AdvisorIntelligence xtick spacing fix session log

