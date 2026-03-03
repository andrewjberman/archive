# Thread Context -- Pattern 0 alignment: adv_drill (Continuous NNA ADV) + cla_timeseries (Continuous CLA)

**Thread ID:** 2026-03-03-continuous-nna-cla-alignment
**Created by:** 2.0.0_SA_COO
**Created at:** 2026-03-03T19:42:18Z

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

This is a Pattern 0 pre-implementation alignment thread for two interface-dependent work streams in the AdvisorIntelligence completion PRD.

Stream A1: adv_drill — The publisher Lambda needs to generate per-architect NNA time series (analogous to the existing geo_drill per-city series). This does NOT yet exist. DS must describe what advisor/client-level NNA data is currently available in the gold layer and what an adv_drill output can realistically look like.

Stream A2: cla_timeseries — A new time-series view showing NMNC (new client) vs NMEC (existing client) AUM composition over time. This data does NOT exist anywhere in the current pipeline. DS must describe what classification data (NMNC vs NMEC) is available in the gold layer and what a realistic cla_timeseries output looks like.

Knowledge source: 0.4.0_DS_ClientPlatform (what the gold layer can produce).
Interface specifier: 0.4.0_DE_ClientPlatform (what TypeScript shape the portal needs).
Layout specifier: 0.4.2_RD_AdvisorIntelligence (what the chart component requires from the data).

Deliverable of this thread: agreed JSON output schemas for adv_drill and cla_timeseries, agreed TypeScript interface names and shapes, agreed S3 key patterns. The final turn must contain this as a structured contract. The COO will embed this receipt in the DS and RD task orders as the binding specification.


### advisor-intelligence-api-endpoints-current-endpoint-contract.ts

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

### advisorintelligence-completion-prd--section-3-distribution-tab.md

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

### advisorintelligence-typescript-types-current-portal-types.ts

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

### bd-portal-publisher-lambda-current-output-producer.py

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

# For filters/snapshots
TOP_N_CITIES      = 50
TOP_N_IMPLEMENTOR = 50
TOP_N_STATE       = 49
TOP_N_RELATIONSHIP = 100

# Top positions by unrealized gain shown in tax section
TOP_GAIN_POSITIONS = 20


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
                 'primary_state', 'primary_country',
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
# 1. timeseries_chart.json  (CumulativeChartResponse)
# ---------------------------------------------------------------------------

def build_timeseries_chart(perf: pd.DataFrame, adv: pd.DataFrame, geo: pd.DataFrame,
                            cdim: pd.DataFrame, today: pd.Timestamp,
                            geo_city: pd.DataFrame = None) -> dict:
    """
    4+1 views, daily data points:
      aua       -- cumulative NMNC vs NMEC stacked
      nna       -- cumulative firm-level NNA
      geo       -- cumulative AUA by top states (stacked)
      adv       -- cumulative AUA by top architects (stacked)
      geo_drill -- per-state city-level AUA timeseries (optional)
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
    perf_cohort = perf[['date', 'relationship_id', 'total_aua']].merge(
        cdim[['relationship_id', 'first_seen_date']],
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
    }

    # Only add geo_drill when populated (avoids empty key in JSON)
    if geo_drill:
        result['geo_drill'] = geo_drill

    print(f"  timeseries_chart: {len(aua_data)} days, {len(adv_categories)} architects, "
          f"{len(geo_categories)} states"
          + (f", {len(geo_drill)} state drill-downs" if geo_drill else ""))
    return result


# ---------------------------------------------------------------------------
# 2. Leaderboard helpers
# ---------------------------------------------------------------------------

def _leaderboard_entries(df_by_date: pd.DataFrame, dim_col: str,
                          cdim: pd.DataFrame, architect_col: str,
                          today: pd.Timestamp, days: int) -> list:
    """
    Build ranked LeaderboardEntry list for one time window.

    df_by_date: daily timeseries (adv or account-performance-based) with
                date, {dim_col}, total_aua, nna columns
    architect_col: column in cdim that maps to dim_col (e.g. 'primary_architect')
    """
    window_start = today - pd.Timedelta(days=days)

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
    for label, days in WINDOWS.items():
        entries = _leaderboard_entries(adv, 'architect', cdim, 'primary_architect',
                                        today, days)
        windows_data[label] = _leaderboard_window_data(entries)
        print(f"  Window {label}: {len(entries)} architects")

    latest_date = adv['date'].max()
    return {
        'generated_at':       datetime.now(timezone.utc).isoformat(),
        'data_as_of':         latest_date.strftime('%Y-%m-%d'),
        'firm_id':            FIRM_ID,
        'leaderboard_type':   'architect',
        'available_windows':  list(WINDOWS.keys()),
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
        q_start = _quarter_start(today, quarters_back)
        q_end   = _quarter_start(today, quarters_back - 1) - pd.Timedelta(days=1)
        nna_val = _nna_for_period((today - q_start).days) - (
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

### distributiontab-component-current-consumer.tsx

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
import { ChevronLeft, HelpCircle } from 'lucide-react'
import { Tooltip } from '@/components/Tooltip'
import { formatCurrency, formatNumberTo3Digits } from '@/lib/universalNumberFormatter'
import { getCumulativeChart } from '@/api/endpoints/advisor-intelligence'
import type {
  CumulativeChartResponse,
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
  ClaView,
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
                    {METRIC_OPTIONS.map((opt) => (
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
                {viewStyle === 'continuous' && metric !== 'cla' && (
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
            />
          )}
      </PanelContent>
      <PanelFooter content="Source: SS&C Black Diamond Wealth Solutions." timestamp={analyticsData?.generated_at} />
    </Panel>
  )
}

// ============================================================================
// CONTINUOUS NNA CHART VIEW (Diverging Bar + Net Line)
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
}

function ContinuousChartView({ data, cohort, metric, window, categoryColorMap }: ContinuousChartViewProps) {
  // -----------------------------------------------------------------------
  // ALL hooks unconditionally at the top — Rules of Hooks
  // -----------------------------------------------------------------------
  const [drillParent, setDrillParent] = useState<string | null>(null)

  useEffect(() => {
    setDrillParent(null)
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

  const areaMetrics = useMemo(() => {
    if (filteredChartData.length === 0 || categories.length === 0) {
      return { totalNNA: 0, growthPct: 0 }
    }
    const latest = filteredChartData[filteredChartData.length - 1]
    const first = filteredChartData[0]
    const latestTotal = categories.reduce((sum, cat) => sum + (Number(latest[cat]) || 0), 0)
    const firstTotal = categories.reduce((sum, cat) => sum + (Number(first[cat]) || 0), 0)
    const growth = firstTotal !== 0 ? ((latestTotal - firstTotal) / Math.abs(firstTotal)) * 100 : 0
    return { totalNNA: latestTotal, growthPct: growth }
  }, [filteredChartData, categories])

  const startingTotal = useMemo(() => {
    if (filteredChartData.length === 0 || categories.length === 0) return 0
    const first = filteredChartData[0]
    return categories.reduce((sum, cat) => sum + (Number(first[cat]) || 0), 0)
  }, [filteredChartData, categories])

  // -----------------------------------------------------------------------
  // Early returns AFTER all hooks
  // -----------------------------------------------------------------------

  // CLA continuous: placeholder
  if (metric === 'cla') {
    return (
      <div className="flex items-center justify-center min-h-[240px]">
        <div className="text-center">
          <p className="text-white/50 text-sm font-medium">CLA Timeseries</p>
          <p className="text-white/30 text-xs mt-1">Coming soon</p>
        </div>
      </div>
    )
  }

  // NNA continuous: diverging bar + net line
  if (metric === 'nna') {
    return <ContinuousNnaChartView data={data} window={window} />
  }

  // -----------------------------------------------------------------------
  // Derived values (non-hooks) for the stacked area render path
  // -----------------------------------------------------------------------
  const showAdvComingSoon = isDrilled && cohort === 'adv' && !drillViewData
  const canLegendDrill = (cohort === 'adv') || (cohort === 'geo' && !!data?.geo_drill)

  const gainSinceStart = areaMetrics.totalNNA - startingTotal
  const startDate = filteredChartData.length > 0 ? filteredChartData[0].date : null
  const startDateFormatted = startDate
    ? new Date(startDate + 'T12:00:00').toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
    : ''

  return (
    <div className="flex min-h-[240px]">
      {/* Left: Hero Metrics */}
      <div className="w-[280px] flex-shrink-0 p-5 flex flex-col border-r border-white/5">
        {/* Back button when drilled */}
        {isDrilled && (
          <button
            onClick={() => setDrillParent(null)}
            className="flex items-center gap-1.5 text-xs text-white/60 hover:text-white transition-colors mb-3"
          >
            <ChevronLeft size={14} />
            <span>Back to {cohort === 'geo' ? 'States' : 'Architects'}</span>
          </button>
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
            {data?.metadata?.new_clients?.[window as string] ?? '--'}
          </p>
          <p className="text-[10px] text-white/40 mt-0.5">New Clients</p>
        </div>

        {categories.length > 0 && (
          <div className="mt-auto pt-3 border-t border-white/5 space-y-1.5">
            {categories.map((cat, idx) => {
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

      {/* Right: Area Chart */}
      <div className="flex-1 p-4 flex items-center min-h-[280px]">
        {showAdvComingSoon ? (
          <div className="flex-1 flex items-center justify-center w-full">
            <div className="text-center">
              <p className="text-white/50 text-sm font-medium">{drillParent?.replace(/_/g, ' ')}</p>
              <p className="text-white/30 text-xs mt-1">Relationship-level timeseries coming soon</p>
            </div>
          </div>
        ) : filteredChartData.length > 0 && categories.length > 0 ? (
          <ResponsiveContainer width="100%" height="100%" minHeight={240}>
            <AreaChart data={filteredChartData} margin={{ top: 10, right: 10, left: 0, bottom: 5 }}>
              <defs>
                {categories.map((cat, idx) => {
                  const color = getCategoryColor(cat, idx, categoryColorMap, cohort)
                  const gradientId = `dist-gradient-${cat.replace(/\s+/g, '-')}`
                  return (
                    <linearGradient key={gradientId} id={gradientId} x1="0" y1="0" x2="0" y2="1">
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
                  const displayDate = date.toLocaleDateString('en-US', {
                    month: 'long',
                    day: 'numeric',
                    year: 'numeric',
                  })

                  const total = payload.reduce((sum, entry) => sum + (Number(entry.value) || 0), 0)
                  const sortedPayload = [...payload].sort((a, b) => (Number(b.value) || 0) - (Number(a.value) || 0))

                  return (
                    <div className="bg-[hsl(var(--semantic-background-chartTooltipBg))] border-2 border-[hsl(var(--primary))] rounded-lg px-4 py-3 shadow-xl">
                      <div className="text-[hsl(var(--semantic-text-chartTooltip))] font-bold text-sm mb-2">
                        {displayDate}
                      </div>
                      <div className="flex items-center justify-between gap-6 mb-2">
                        <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm">
                          {metric === 'aua' ? 'Cumulative AUA' : 'Cumulative NNA'}
                        </span>
                        <span className="text-[hsl(var(--semantic-text-chartTooltip))] font-semibold text-sm">
                          {formatCurrency(total)}
                        </span>
                      </div>
                      <div className="border-t border-[hsl(var(--semantic-text-chartTooltip))]/20 my-2" />
                      <div className="space-y-1">
                        {sortedPayload.map((entry) => (
                          <div key={entry.dataKey} className="flex items-center justify-between gap-6">
                            <div className="flex items-center gap-2">
                              <div
                                className="w-2 h-2 rounded-full"
                                style={{ backgroundColor: entry.color as string }}
                              />
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
              {categories.map((cat, idx) => {
                const color = getCategoryColor(cat, idx, categoryColorMap, cohort)
                const gradientId = `dist-gradient-${cat.replace(/\s+/g, '-')}`
                return (
                  <Area
                    key={cat}
                    type="monotone"
                    dataKey={cat}
                    stackId="cumulative"
                    stroke={color}
                    strokeWidth={2}
                    fill={`url(#${gradientId})`}
                  />
                )
              })}
            </AreaChart>
          </ResponsiveContainer>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <p className="text-white/40 text-sm">No chart data available</p>
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

  const segments: DonutSegment[] = useMemo(() => {
    if (cohort === 'geo' && geoDrillLevel === 'city' && selectedStateKey) {
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
  }, [cohort, geoDrillLevel, advDrillLevel, selectedStateKey, selectedArchitectKey, baseSegments])

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
    if (selectedSegment?.distribution) return selectedSegment.distribution
    if (selectedSegment && distribution?.by_segment?.[selectedSegment.key])
      return distribution.by_segment[selectedSegment.key]
    if (parentSegment?.distribution) return parentSegment.distribution
    if (parentSegment && distribution?.by_segment?.[parentSegment.key])
      return distribution.by_segment[parentSegment.key]
    return distribution?.total || null
  }, [selectedSegment, parentSegment, distribution])

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
    // NNA: no drill-down -- select/deselect only (for histogram filtering)
    if (metric === 'nna') {
      setSelectedSegmentKey(prev => prev === seg.key ? null : seg.key)
      return
    }
    if (cohort === 'geo' && geoDrillLevel === 'state') {
      setSelectedStateKey(seg.key); setGeoDrillLevel('city'); setSelectedSegmentKey(null); return
    }
    if (cohort === 'adv' && advDrillLevel === 'architect') {
      setSelectedArchitectKey(seg.key); setAdvDrillLevel('client'); setSelectedSegmentKey(null); return
    }
    setSelectedSegmentKey(prev => prev === seg.key ? null : seg.key)
  }, [cohort, metric, geoDrillLevel, advDrillLevel])

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
    ? (selectedSegment
        ? `${selectedSegment.label} -- NNA Flow Distribution`
        : cohort === 'geo' ? 'NNA Flows by Relationship (State)' : 'NNA Flows by Relationship (Advisor)')
    : (selectedSegment
        ? `${selectedSegment.label} -- Account Sizes`
        : parentSegment
        ? `${parentSegment.label} -- Account Sizes`
        : cohort === 'geo' ? 'Account Sizes by State' : 'Account Sizes by Architect')

  // --- CLA: diverging stacked bar chart (replaces donut + histogram) ---
  if (metric === 'cla') {
    return (
      <ClaSnapshotView
        analyticsData={analyticsData}
        cohort={cohort}
        selectedPeriod={selectedPeriod}
        onPeriodChange={setSelectedPeriod}
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
            {isDrilledDown && !isNnaMode && (
              <button
                onClick={handleDrillUp}
                className="flex items-center gap-1.5 text-sm font-medium text-white hover:text-white/70 transition-colors mr-2"
              >
                <ChevronLeft size={18} />
                <span>{cohort === 'geo' ? 'States' : 'Architects'}</span>
              </button>
            )}
            <h4 className="text-xs font-medium text-white/60 uppercase tracking-wider">
              {isDrilledDown && !isNnaMode
                ? (cohort === 'geo' ? selectedStateKey?.toUpperCase() : selectedArchitectKey?.replace(/_/g, ' '))
                : isNnaMode
                ? (cohort === 'geo' ? 'NNA by State' : 'NNA by Architect')
                : (cohort === 'geo' ? 'AUA by State' : 'AUA by Architect')}
            </h4>
            <Tooltip content={
              isNnaMode
                ? `Period NNA across ${cohort === 'geo' ? 'states' : 'architects'}. Click a segment to filter the relationship flow distribution on the right.`
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
                    // NNA: no drill affordance; AUA: drillable at top level only
                    const isDrillable = !isNnaMode && !isDrilledDown

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
              {isNnaMode
                ? `${cohort === 'geo' ? 'State' : 'Advisor'}-level period NNA from Black Diamond.`
                : isDrilledDown
                ? `${cohort === 'geo' ? 'City' : 'Client'}-level AUA from Black Diamond account data.`
                : `${cohort === 'geo' ? 'State' : 'Architect'}-level AUA from Black Diamond account data.`}
            </span>
            <span className="text-white/40">
              {isNnaMode
                ? ' Click a segment to filter relationship flows on the right.'
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
                  <span className="text-white/40">Per-relationship NNA flows. Symmetric log bins, $0 at center.</span>
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

/** Split NNA histogram at zero and compute absolute-value percentiles on each side.
 *  Outflows: bins with negative midpoints, sorted ascending (most negative first).
 *    Percentiles are computed on |midpoint| but counted from the tail inward,
 *    so P25 = magnitude exceeded by 25% of outflows (large), P75 = exceeded by 75% (small).
 *    This keeps P25 < P75 on the signed axis (P25 far left, P75 near zero).
 *  Inflows: bins with positive midpoints, already ascending. Standard percentiles. */
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

  // Outflows are already in ascending order (most negative → least negative)
  // Standard percentiles on signed values: P25 = large negative, P75 = near zero
  return {
    outflow: {
      count: outCounts.reduce((s, c) => s + c, 0),
      p25: histogramPercentile(outMids, outCounts, 25),
      median: histogramPercentile(outMids, outCounts, 50),
      p75: histogramPercentile(outMids, outCounts, 75),
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
  const chartData = data.histogram.bin_labels.map((label, index) => ({
    bin: label,
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
  // Outflow values are already signed negative; P25 far left, P75 near zero.
  const percentileLines = isNnaMode && nnaSplit ? [
    // Net outflow side (signed negative — P25 is most negative, P75 near zero)
    { value: nnaSplit.outflow.p25, label: 'Out P25', color: '#ef4444' },
    { value: nnaSplit.outflow.median, label: 'Out Med', color: '#fb923c' },
    { value: nnaSplit.outflow.p75, label: 'Out P75', color: '#fbbf24' },
    // Net inflow side (positive — P25 near zero, P75 far right)
    { value: nnaSplit.inflow.p25, label: 'In P25', color: '#86efac' },
    { value: nnaSplit.inflow.median, label: 'In Med', color: '#34d399' },
    { value: nnaSplit.inflow.p75, label: 'In P75', color: '#60a5fa' },
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

  const renderSide = (side: typeof split.outflow, label: string, dotColor: string) => (
    <div className="flex flex-col items-center gap-2 flex-1">
      <div className="flex items-center gap-1.5 mb-0.5">
        <div className="w-2 h-2 rounded-full" style={{ backgroundColor: dotColor }} />
        <span className="text-[10px] font-semibold text-white/70 uppercase tracking-wider">{label}</span>
        <span className="text-[10px] text-white/40">({side.count.toLocaleString()})</span>
      </div>
      <div className="flex items-center gap-4">
        <div className="flex flex-col items-center">
          <span className="text-[9px] text-white/40">P25</span>
          <span className="text-xs font-medium text-white/80">{fmtAbs(side.p25)}</span>
        </div>
        <div className="flex flex-col items-center px-2 py-0.5 rounded bg-white/5 border border-white/10">
          <span className="text-[9px] text-white/50 font-semibold">Median</span>
          <span className="text-sm font-bold text-white">{fmtAbs(side.median)}</span>
        </div>
        <div className="flex flex-col items-center">
          <span className="text-[9px] text-white/40">P75</span>
          <span className="text-xs font-medium text-white/80">{fmtAbs(side.p75)}</span>
        </div>
      </div>
    </div>
  )

  return (
    <div className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 flex items-stretch gap-4">
      {renderSide(split.outflow, 'Net Outflows', '#ef4444')}
      <div className="w-px bg-white/15 self-stretch" />
      {renderSide(split.inflow, 'Net Inflows', '#34d399')}
    </div>
  )
}

// ============================================================================
// CLA SNAPSHOT VIEW (Diverging Stacked Bar Chart)
// ============================================================================

const CLA_COLORS = {
  nmnc: '#16A34A',    // green -- new client inflows
  nmec_in: '#2563EB', // blue  -- existing client inflows
  nmec_out: '#DC2626', // red  -- existing client outflows
}

interface ClaBarDatum {
  label: string
  key: string
  color: string   // canonical segment color matching the donut palette
  nmnc_in: number
  nmec_in: number
  nmec_out: number
  net: number
}

interface ClaSnapshotViewProps {
  analyticsData: PartnerAnalyticsResponse
  cohort: CohortOption
  selectedPeriod: TimePeriodKey
  onPeriodChange: (period: TimePeriodKey) => void
}

function ClaSnapshotView({ analyticsData, cohort, selectedPeriod, onPeriodChange }: ClaSnapshotViewProps) {
  const claViews = analyticsData.views?.cla as Record<string, { geo: ClaView; adv: ClaView }> | undefined
  console.log('CLA views debug:', { claViews, selectedPeriod, cohort, views: analyticsData.views })
  const periodData = claViews?.[selectedPeriod]
  const claView: ClaView | null = periodData ? (cohort === 'geo' ? periodData.geo : periodData.adv) : null

  // Build canonical color map from the matching AUA view (geo or adv) so CLA bar colors
  // match the segment colors shown in the donut elsewhere in the panel.
  const canonicalColorMap = useMemo(() => {
    const viewKey = cohort === 'geo' ? 'geo' : 'adv'
    const view = analyticsData.views?.[viewKey]
    if (!view) return {} as Record<string, string>
    const snap = getCurrentSnapshot(view as PartnerAnalyticsViewWithPeriods | PartnerAnalyticsView)
    const segments = ('donut' in snap) ? (snap as PeriodSnapshot).donut?.segments : undefined
    if (!segments) return {} as Record<string, string>
    const palette = cohort === 'adv' ? ADV_COLORS : GEO_COLORS
    return Object.fromEntries(
      segments.map((s, i) => [s.key, s.color || (s.key === 'Other' ? OTHER_COLOR : palette[i % palette.length])])
    ) as Record<string, string>
  }, [analyticsData, cohort])

  const barData: ClaBarDatum[] = useMemo(() => {
    if (!claView?.segments) return []
    const palette = cohort === 'adv' ? ADV_COLORS : GEO_COLORS
    return [...claView.segments]
      .sort((a, b) => Math.abs(b.nna_total) - Math.abs(a.nna_total))
      .map((seg, i) => ({
        label: seg.label,
        key: seg.key,
        color: canonicalColorMap[seg.key] || palette[i % palette.length],
        nmnc_in: seg.nmnc.inflows,
        nmec_in: seg.nmec.inflows,
        nmec_out: seg.nmec.outflows, // negative value extends left of zero
        net: seg.nna_total,
      }))
  }, [claView, canonicalColorMap, cohort])

  const totals = claView?.totals
  const periods = analyticsData.periods
  const periodKeys: TimePeriodKey[] = ['current', 'q1', 'q2', 'q3']
  const yAxisWidth = 210

  if (!claView) {
    return (
      <div className="flex items-center justify-center min-h-[360px]">
        <p className="text-white/40 text-sm">CLA data not available</p>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-4 p-4">

      {/* Summary tiles -- same layout as PartnerAnalytics NNA panel */}
      <div className="flex flex-wrap items-stretch gap-3">
        <div className="flex-1 min-w-[140px] flex flex-col items-center px-4 py-3 rounded-lg bg-[#16A34A]/10 border border-[#16A34A]/30">
          <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-1">NMNC</div>
          <div className="text-xl font-bold text-[#16A34A]">
            {formatNumberTo3Digits(totals?.nmnc_nna ?? 0, { unit: '$', includeSign: true })}
          </div>
          <div className="text-xs text-white/40 mt-0.5">{(totals?.nmnc_count ?? 0).toLocaleString()} new rels</div>
        </div>
        <div className="flex-1 min-w-[140px] flex flex-col items-center px-4 py-3 rounded-lg bg-[#2563EB]/10 border border-[#2563EB]/30">
          <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-1">NMEC</div>
          <div className="text-xl font-bold text-[#2563EB]">
            {formatNumberTo3Digits(totals?.nmec_nna ?? 0, { unit: '$', includeSign: true })}
          </div>
          <div className="text-xs text-white/40 mt-0.5">{(totals?.nmec_count ?? 0).toLocaleString()} existing rels</div>
        </div>
        <div className="flex-1 min-w-[140px] flex flex-col items-center px-4 py-3 rounded-lg bg-white/5 border border-white/10">
          <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-1">Net NNA</div>
          <div className={`text-xl font-bold ${(totals?.nna ?? 0) >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
            {formatNumberTo3Digits(totals?.nna ?? 0, { unit: '$', includeSign: true })}
          </div>
        </div>
      </div>

      {/* Chart legend */}
      <div className="flex items-center gap-5 text-xs text-white/50 px-1">
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: CLA_COLORS.nmnc }} />
          <span>NMNC inflows</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: CLA_COLORS.nmec_in }} />
          <span>NMEC inflows</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: CLA_COLORS.nmec_out }} />
          <span>NMEC outflows</span>
        </div>
      </div>

      {/* Diverging stacked bar chart */}
      <div style={{ height: Math.max(260, barData.length * 48) }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={barData}
            layout="vertical"
            margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
            stackOffset="sign"
          >
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" horizontal={false} />
            <XAxis
              type="number"
              stroke="rgba(255,255,255,0.2)"
              tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.6)' }}
              tickFormatter={(v) => {
                const abs = Math.abs(v)
                if (abs >= 1e9) return `${v < 0 ? '-' : ''}$${(abs / 1e9).toFixed(1)}B`
                if (abs >= 1e6) return `${v < 0 ? '-' : ''}$${(abs / 1e6).toFixed(0)}M`
                return `$${v}`
              }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              type="category"
              dataKey="label"
              width={yAxisWidth}
              axisLine={false}
              tickLine={false}
              tick={(props) => {
                // eslint-disable-next-line @typescript-eslint/no-explicit-any
                const { x, y, payload } = props as any
                const datum = barData.find(d => d.label === payload.value)
                const color = datum?.color || '#6B7280'
                const net = datum?.net ?? 0
                const truncLabel = payload.value.length > 15 ? payload.value.slice(0, 14) + '…' : payload.value
                const nnaText = formatNumberTo3Digits(net, { unit: '$', includeSign: true })
                return (
                  <g transform={`translate(${x},${y})`}>
                    {/* Canonical color square */}
                    <rect x={-yAxisWidth + 6} y={-7} width={12} height={12} rx={2} fill={color} />
                    {/* Segment label */}
                    <text x={-yAxisWidth + 22} y={4.5} textAnchor="start" fontSize={11} fill="rgba(255,255,255,0.8)">
                      {truncLabel}
                    </text>
                    {/* Net NNA right-aligned */}
                    <text x={-4} y={4.5} textAnchor="end" fontSize={11} fontWeight={600} fill={net >= 0 ? '#34d399' : '#f87171'}>
                      {nnaText}
                    </text>
                  </g>
                )
              }}
            />
            <ReferenceLine x={0} stroke="rgba(255,255,255,0.2)" strokeWidth={1} />
            <RechartsTooltip
              wrapperStyle={{ zIndex: 40 }}
              cursor={{ fill: 'rgba(255,255,255,0.04)' }}
              content={({ active, payload }) => {
                if (!active || !payload?.length) return null
                const d = payload[0]?.payload as ClaBarDatum
                return (
                  <div className="bg-[#0f1729] border-2 border-white/10 rounded-lg px-4 py-3 shadow-xl">
                    <div className="flex items-center gap-2 mb-2">
                      <div className="w-3 h-3 rounded-sm flex-shrink-0" style={{ backgroundColor: d.color }} />
                      <span className="text-white font-bold text-sm">{d.label}</span>
                    </div>
                    <div className="space-y-1.5 text-xs">
                      <div className="flex items-center justify-between gap-6">
                        <div className="flex items-center gap-1.5">
                          <div className="w-2 h-2 rounded-sm" style={{ backgroundColor: CLA_COLORS.nmnc }} />
                          <span className="text-white/70">NMNC</span>
                        </div>
                        <span className="font-medium text-[#4ade80]">+{formatCurrency(d.nmnc_in)}</span>
                      </div>
                      <div className="flex items-center justify-between gap-6">
                        <div className="flex items-center gap-1.5">
                          <div className="w-2 h-2 rounded-sm" style={{ backgroundColor: CLA_COLORS.nmec_in }} />
                          <span className="text-white/70">NMEC inflows</span>
                        </div>
                        <span className="font-medium text-[#60a5fa]">+{formatCurrency(d.nmec_in)}</span>
                      </div>
                      <div className="flex items-center justify-between gap-6">
                        <div className="flex items-center gap-1.5">
                          <div className="w-2 h-2 rounded-sm" style={{ backgroundColor: CLA_COLORS.nmec_out }} />
                          <span className="text-white/70">NMEC outflows</span>
                        </div>
                        <span className="font-medium text-red-400">{formatNumberTo3Digits(d.nmec_out, { unit: '$', includeSign: true })}</span>
                      </div>
                      <div className="flex items-center justify-between gap-6 border-t border-white/10 pt-1.5 mt-1.5 font-medium">
                        <span className="text-white/70">Net NNA</span>
                        <span className={d.net >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}>
                          {formatNumberTo3Digits(d.net, { unit: '$', includeSign: true })}
                        </span>
                      </div>
                    </div>
                  </div>
                )
              }}
            />
            <Bar dataKey="nmec_out" stackId="stack" fill={CLA_COLORS.nmec_out} radius={[4, 0, 0, 4]} />
            <Bar dataKey="nmnc_in"  stackId="stack" fill={CLA_COLORS.nmnc} />
            <Bar dataKey="nmec_in"  stackId="stack" fill={CLA_COLORS.nmec_in} radius={[0, 4, 4, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Time Machine quarter strip */}
      {periods && (
        <div className="flex items-center gap-1 justify-center pt-2 border-t border-white/5">
          {periodKeys.map(pk => {
            const def = periods[pk]
            if (!def) return null
            const isActive = selectedPeriod === pk
            return (
              <button
                key={pk}
                onClick={() => onPeriodChange(pk)}
                className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                  isActive
                    ? 'bg-[hsl(var(--primary))] text-white'
                    : 'text-white/40 hover:text-white hover:bg-white/10'
                }`}
              >
                {def.label}
              </button>
            )
          })}
        </div>
      )}
    </div>
  )
}
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

