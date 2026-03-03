# Thread Context -- Data pipeline orientation for ClientPlatform pod (AdvisorIntelligence, ModelPortfolios)

**Thread ID:** 2026-03-02-ds-client-platform-pipeline-intake
**Created by:** 0.4.0_DS_ClientPlatform
**Created at:** 2026-03-03T00:58:18Z

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
| **Pod Partner** | 0.4.0_DE_ClientPlatform |

## Responsibility

Data modeling, analysis, and technical investigation for the Client Platform pod.

## Abilities & Permissions

### CAN DO
- **Edit and commit code locally** — pipeline scripts, Lambda functions, data transformations, analysis code
- Write technical documents, investigation reports, and specs to `deliverables/`
- Read any file in the codebase for analysis
- Tag commits: `0.4.0_DS_ClientPlatform: <description>`

### CANNOT DO
- **Push** to any branch (DT pushes your work)
- **Deploy** AWS resources (DT/AE responsibility)
- **Run** `terraform plan/apply`, `build-and-upload.sh`, `safe-ec2-deploy.sh`

### SESSION LOGS (Encouraged)
- Location: `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/YYYY-MM-DD/`

### TASK ORDERS
- Received from: 0.4.0_DE (PM), Andrew (ad hoc), CTO, COO
- Location: `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/`

### DELIVERABLES
- Technical documents and specs: `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/`

## Pages Served

ModelPortfolios, AdvisorIntelligence


### 0.6.0_AE_PartnerETL

# Agent 0.6.0_AE_PartnerETL — AWS Engineer

| Field | Value |
|-------|-------|
| **Agent ID** | 0.6.0_AE_PartnerETL |
| **Role** | AWS Engineer |
| **Title** | Partner ETL/Pipelines Engineer |
| **Tier** | 1 (Management — Shared Services) |
| **Reports To** | 1.0.0_SA_CTO, 2.0.0_SA_COO |

## Responsibility

Partner-specific ETL pipelines. Primary focus: BD pipeline for 49 Financial (Black Diamond).

## Abilities & Permissions

### CAN DO
- **Deploy AWS resources** — Lambda, EC2, Terraform for BD pipeline
- **Commit** infrastructure and pipeline code — `infra/aws/lambda/bd-pipeline/`, `infra/aws/terraform/bd-pipeline/`, `data/black_diamond/`
- **Push** commits to `CLOUD` branch
- Run `terraform plan/apply`, `build-and-upload.sh`, `safe-ec2-deploy.sh`
- Tag releases: `{pipeline}-v{X.Y.Z}` and push with `--follow-tags`
- Write gold layer scripts, EventBridge rules, IAM policies

### MUST DO
- Follow mandatory deployment protocols
- Commit -> plan -> apply -> 0-diff -> tag -> push
- Log all deployments

### CANNOT DO
- Commit portal frontend code | Push portal to DEV/PROD | Make architecture decisions unilaterally

### SESSION LOGS (Encouraged)
- Location: `org/tier2_senior/0.6.0_AE_PartnerETL/logs/YYYY-MM-DD/`
- Naming: `{pipeline}_{action}.md`
  - Example: `bd_pipeline_gold_layer_fix.md`
  - Example: `bd_pipeline_price_update_idempotency.md`

### TASK ORDERS
- Received from: Andrew Berman (ad hoc), 1.0.0_SA_CTO, 2.0.0_SA_COO
- Location: `org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/`

## Pipeline Owned

| Pipeline | Terraform Module | Tag |
|----------|-----------------|-----|
| BD | `infra/aws/terraform/bd-pipeline/` | bd-v2.13.1 |

## Key Infrastructure

- BD Lambda functions: `infra/aws/lambda/bd-pipeline/`
- BD gold layer scripts: `data/black_diamond/scripts/gold/`
- BD EC2 runner: tracked in `infra/aws/ec2/EC2_MANIFEST.json`
- EventBridge rules: `infra/aws/terraform/bd-pipeline/eventbridge.tf`


---

## Reference Material

### Briefing Notes

This thread is a structured pipeline orientation session. 0.4.0_DS_ClientPlatform is brand new to the BD pipeline and needs to understand the data layer behind the AdvisorIntelligence and ModelPortfolios pages. 0.6.0_AE_PartnerETL owns the BD pipeline (infra/aws/terraform/bd-pipeline/, infra/aws/lambda/bd-pipeline/, data/black_diamond/scripts/gold/). The DS has reviewed the portal endpoint files in context. The goal is for AE to provide a concrete data-flow map: portal endpoint -> Lambda/script producer -> storage location -> refresh schedule -> known issues. DS will use this to produce a data_inventory.xml deliverable.


### advisorintelligence-api-endpoints.ts

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

### aum-api-endpoints.ts

```
/**
 * AUM API Client - SmartX Portfolio Data
 *
 * Endpoints for Assets Under Management summary, flows, and model breakdowns
 *
 * UPDATED 2025-12-01: Now uses secure Lambda proxy instead of direct DynamoDB access
 * This eliminates AWS credential exposure in the browser bundle.
 *
 * UPDATED 2026-01-04: Now uses shared apiRequest() for authentication
 *
 * API Proxy: opal-portal-data-proxy Lambda
 */

import * as portalProxy from '../portal-proxy'
import { apiRequest } from '../api-client'

// ============================================================================
// TypeScript Types
// ============================================================================

export interface AUMByAssetClass {
  asset_class: string
  aum: number
  account_count: number
}

export interface AUMByModel {
  model_name: string
  aum: number
  account_count: number
}

export interface AUMSummaryResponse {
  period: string
  total_aum: number
  total_accounts: number
  by_asset_class: AUMByAssetClass[]
  by_model: AUMByModel[]
}

export interface ModelFlowChange {
  model_name: string
  start_aum: number
  end_aum: number
  aum_change: number
  change_pct: number
}

export interface AUMFlowsResponse {
  start_period: string
  end_period: string
  total_start_aum: number
  total_end_aum: number
  total_change: number
  total_change_pct: number
  by_model: ModelFlowChange[]
  note?: string
}

export interface PeriodData {
  period: string
  aum: number
  account_count: number
  aum_change: number | null
  aum_change_pct: number | null
}

export interface ModelTimeSeriesResponse {
  model_name: string
  total_periods: number
  latest_aum: number
  latest_period: string
  time_series: PeriodData[]
}

/**
 * Metrics for a time period (Month, Quarter, Year)
 */
export interface PeriodMetrics {
  change: number | null      // Dollar amount change
  growth: number | null      // Percentage growth
  priorLevel: number | null  // AUM level at start of period
}

/**
 * Extended AUM metrics with quarterly periods
 */
export interface AUMWithMetrics {
  aum: number
  account_count?: number
  q0: PeriodMetrics  // Current or most recent quarter
  q1: PeriodMetrics  // Last completed quarter (Q3 2025, etc)
  q2: PeriodMetrics  // Two quarters ago (Q2 2025, etc)
  q3: PeriodMetrics  // Three quarters ago (Q1 2025, etc)
}

/**
 * Extended model flow with metrics across time periods
 */
export interface ModelFlowWithMetrics extends AUMWithMetrics {
  model_name: string
}

/**
 * Extended AUM flows response with period metrics
 */
export interface AUMFlowsWithMetricsResponse {
  period: string
  total: AUMWithMetrics
  by_model: ModelFlowWithMetrics[]
  dates?: {
    q0: string  // Current/recent quarter end
    q1: string  // Last completed quarter end
    q2: string  // Two quarters ago end
    q3: string  // Three quarters ago end
  }
  last_updated?: string  // SmartX EC2 process timestamp
  note?: string
}

/**
 * Account distribution statistics for a dataset
 */
export interface DistributionStats {
  account_count: number
  total_aum: number
  mean: number
  median: number
  percentiles: {
    p10: number
    p25: number
    p50: number
    p75: number
    p90: number
  }
  min?: number
  max?: number
  std_dev?: number
  histogram: {
    bins: number[]
    counts: number[]
    bin_labels: string[]
  }
}

/**
 * Account distribution data from S3
 */
export interface AccountDistribution {
  generated_at: string
  period: string
  total: DistributionStats
  by_model: {
    [modelName: string]: DistributionStats
  }
}

// ============================================================================
// API Functions
// ============================================================================

/**
 * Get AUM summary for latest period
 * Shows total AUM and breakdowns by asset class and model
 */
export async function getAUMSummary(assetClass?: string): Promise<AUMSummaryResponse> {
  const data = await portalProxy.getAUMSummary()

  // Filter by asset class if provided
  if (assetClass && data.by_asset_class) {
    data.by_asset_class = (data.by_asset_class as AUMByAssetClass[]).filter(
      (item) => item.asset_class === assetClass
    )
  }

  return data as AUMSummaryResponse
}

/**
 * Get AUM flows between periods
 * Calculates change in AUM for each model portfolio and aggregates totals
 * Properly maps SmartX data to model portfolios (Conservative, Intermediate, Aggressive, Short-Term, Ultra Short-Term)
 *
 * @param startPeriod - Start period in YYYYMM format (e.g., "202409")
 * @param endPeriod - End period in YYYYMM format (e.g., "202511")
 * @param assetClass - Optional filter by asset class (UST, INT, LTC, LTA, ST)
 */
export async function getAUMFlows(
  startPeriod?: string,
  endPeriod?: string,
  assetClass?: string
): Promise<AUMFlowsResponse> {
  const flows = await portalProxy.getAUMFlows(startPeriod, endPeriod)

  if (!flows || flows.length === 0) {
    return {
      start_period: startPeriod || '',
      end_period: endPeriod || '',
      total_start_aum: 0,
      total_end_aum: 0,
      total_change: 0,
      total_change_pct: 0,
      by_model: [],
      note: 'No AUM data available for the requested period',
    }
  }

  // Group flows by model portfolio
  // Data structure from DynamoDB: PK=FLOWS#{period}, SK={model_name}, with start_aum and end_aum attributes
  const modelMap = new Map<string, { start_aum: number; end_aum: number }>()
  let startPeriodFound = ''
  let endPeriodFound = ''

  for (const flow of flows) {
    const flowData = flow as { period?: string; SK?: string; model_name?: string; start_aum?: number; end_aum?: number }
    const period = String(flowData.period || flowData.SK?.split('#')[0] || '')
    const modelName = String(flowData.model_name || flowData.SK || '')

    // Track period range
    if (!startPeriodFound || period < startPeriodFound) startPeriodFound = period
    if (!endPeriodFound || period > endPeriodFound) endPeriodFound = period

    // Aggregate by model
    if (!modelMap.has(modelName)) {
      modelMap.set(modelName, { start_aum: 0, end_aum: 0 })
    }

    const modelData = modelMap.get(modelName)!
    // Use start_aum from first period, end_aum from last period
    if (!modelData.start_aum || period === startPeriodFound) {
      modelData.start_aum = Number(flowData.start_aum) || 0
    }
    if (!modelData.end_aum || period === endPeriodFound) {
      modelData.end_aum = Number(flowData.end_aum) || 0
    }
  }

  // Build model flow changes and calculate totals
  let totalStartAUM = 0
  let totalEndAUM = 0
  const byModel: ModelFlowChange[] = []

  for (const [modelName, data] of modelMap.entries()) {
    const change = data.end_aum - data.start_aum
    const changePct = data.start_aum > 0 ? (change / data.start_aum) * 100 : 0

    byModel.push({
      model_name: modelName,
      start_aum: data.start_aum,
      end_aum: data.end_aum,
      aum_change: change,
      change_pct: changePct,
    })

    totalStartAUM += data.start_aum
    totalEndAUM += data.end_aum
  }

  // Filter by asset class if provided
  let filteredModels = byModel
  if (assetClass) {
    filteredModels = byModel.filter((m: ModelFlowChange) => {
      // Map asset class codes to model names
      const assetClassMap: Record<string, string[]> = {
        'UST': ['Ultra Short-Term'],
        'ST': ['Short-Term'],
        'INT': ['Intermediate'],
        'LTC': ['Conservative'],
        'LTA': ['Aggressive'],
      }
      const modelNames = assetClassMap[assetClass] || []
      return modelNames.some(name => m.model_name.includes(name))
    })

    // Recalculate totals for filtered models
    totalStartAUM = filteredModels.reduce((sum, m) => sum + m.start_aum, 0)
    totalEndAUM = filteredModels.reduce((sum, m) => sum + m.end_aum, 0)
  }

  const totalChange = totalEndAUM - totalStartAUM
  const totalChangePct = totalStartAUM > 0 ? (totalChange / totalStartAUM) * 100 : 0

  return {
    start_period: startPeriodFound || startPeriod || '',
    end_period: endPeriodFound || endPeriod || '',
    total_start_aum: totalStartAUM,
    total_end_aum: totalEndAUM,
    total_change: totalChange,
    total_change_pct: totalChangePct,
    by_model: filteredModels,
  } as AUMFlowsResponse
}

/**
 * Get detailed time series for a specific model
 * Shows month-over-month AUM changes and account counts
 *
 * @param model - Model name (partial match, case-insensitive)
 * @param assetClass - Optional filter by asset class (not used with proxy)
 */
export async function getModelTimeSeries(
  model: string,
   
  _assetClass?: string
): Promise<ModelTimeSeriesResponse> {
  // Use the proxy's getAUMTimeSeries and extract model-specific data
  const allTimeSeries = await portalProxy.getAUMTimeSeries()

  // Find matching model (case-insensitive partial match)
  const modelLower = model.toLowerCase()
  const matchingModel = Object.keys(allTimeSeries.by_model).find(
    m => m.toLowerCase().includes(modelLower)
  )

  if (!matchingModel) {
    return {
      model_name: model,
      total_periods: 0,
      latest_aum: 0,
      latest_period: '',
      time_series: []
    }
  }

  const modelData = allTimeSeries.by_model[matchingModel] || []
  const latestEntry = modelData[modelData.length - 1]

  // Calculate period-over-period changes
  const timeSeriesWithChanges: PeriodData[] = modelData.map((entry, index) => {
    const prevEntry = index > 0 ? modelData[index - 1] : null
    const aumChange = prevEntry ? entry.aum - prevEntry.aum : null
    const aumChangePct = prevEntry && prevEntry.aum > 0
      ? ((entry.aum - prevEntry.aum) / prevEntry.aum) * 100
      : null

    return {
      period: entry.period,
      aum: entry.aum,
      account_count: entry.account_count,
      aum_change: aumChange,
      aum_change_pct: aumChangePct
    }
  })

  return {
    model_name: matchingModel,
    total_periods: modelData.length,
    latest_aum: latestEntry?.aum || 0,
    latest_period: latestEntry?.period || '',
    time_series: timeSeriesWithChanges
  }
}

/**
 * Get AUM metrics with Month-over-Month, Quarter-over-Quarter, and Year-over-Year changes
 * This is the main endpoint for the Asset Management dashboard
 *
 * Fetches SmartX time series data from DynamoDB and calculates:
 * - MoM: Current month vs previous month
 * - QoQ: Current quarter vs previous quarter
 * - YoY: Current year vs previous year
 */
export async function getAUMMetrics(bustCache: boolean = false): Promise<AUMFlowsWithMetricsResponse> {
  try {
    const metricsData = await portalProxy.getAUMMetricsWithCalculations(bustCache)

    return {
      period: metricsData.period,
      total: metricsData.total,
      by_model: metricsData.by_model,
      dates: metricsData.dates,
      last_updated: metricsData.last_updated,  // SmartX EC2 process timestamp
      note: 'Metrics from SmartX time series data',
    } as AUMFlowsWithMetricsResponse
  } catch (error) {
    console.error('[getAUMMetrics] Error fetching metrics:', error)

    // Return empty structure if data unavailable
    const emptyDates = {
      q0: '',
      q1: '',
      q2: '',
      q3: '',
    }

    return {
      period: 'Current',
      total: {
        aum: 0,
        account_count: 0,
        q0: { change: null, growth: null, priorLevel: null },
        q1: { change: null, growth: null, priorLevel: null },
        q2: { change: null, growth: null, priorLevel: null },
        q3: { change: null, growth: null, priorLevel: null },
      },
      by_model: [],
      dates: emptyDates,
      note: 'Error retrieving metrics from SmartX',
    }
  }
}

interface AUMTimeSeriesData {
  aggregate: Array<{ period: string; aum: number; account_count: number }>
  by_model: Record<string, Array<{ period: string; aum: number; account_count: number }>>
  periods: string[]
}

/**
 * Get historical AUM time series data for charting
 * Returns aggregate AUM trend and per-model AUM trends
 */
export async function getAUMTimeSeries(): Promise<AUMTimeSeriesData> {
  try {
    const timeSeriesData = await portalProxy.getAUMTimeSeries()
    return timeSeriesData
  } catch (error) {
    console.error('[getAUMTimeSeries] Error fetching time series:', error)
    return {
      aggregate: [],
      by_model: {},
      periods: [],
    }
  }
}

/**
 * Get account size distribution statistics
 * Returns histogram data and percentile statistics for all accounts and by model
 * CACHED: Results cached in-memory for 60 minutes (data updates daily)
 */
let accountDistributionCache: {
  data: AccountDistribution | null
  timestamp: number
} = {
  data: null,
  timestamp: 0,
}

const ACCOUNT_DIST_CACHE_TTL = 60 * 60 * 1000 // 60 minutes in milliseconds

/**
 * Clear the account distribution cache and optionally force a fresh fetch
 * Call this when user manually refreshes to ensure fresh data
 *
 * @param fetchFresh - If true, immediately fetches fresh data bypassing all caches
 * @returns The fresh data if fetchFresh=true, otherwise void
 */
export async function clearAccountDistributionCache(fetchFresh: boolean = false): Promise<AccountDistribution | void> {
  accountDistributionCache = {
    data: null,
    timestamp: 0,
  }
  console.log('[clearAccountDistributionCache] In-memory cache cleared')

  if (fetchFresh) {
    // Force fetch with cache-buster to bypass browser/CDN cache
    return getAccountDistribution(true)
  }
}

/**
 * Get account size distribution statistics
 *
 * 🚧 DEMO MODE: Using public endpoint (no auth) for demo purposes
 * TODO: Revert to private endpoint for production:
 *   Path: /api/private/portfolios/account-distribution.json
 *   Auth: JWT Bearer token (firm-scoped)
 *
 * PUBLIC DATA (DEMO): No auth required
 * Path: /api/general/portfolios/account-distribution.json
 * Cache: CloudFront edge cache
 *
 * Returns histogram data and percentile statistics for all accounts and by model
 * Data: Account size distribution, percentiles (p10, p25, p50, p75, p90), histogram bins
 *
 * @param forceRefresh - Deprecated (CloudFront handles caching)
 */
export async function getAccountDistribution(forceRefresh: boolean = false): Promise<AccountDistribution> {
  const now = Date.now()

  // Return cached data if valid (unless force refresh)
  if (
    !forceRefresh &&
    accountDistributionCache.data &&
    now - accountDistributionCache.timestamp < ACCOUNT_DIST_CACHE_TTL
  ) {
    const cacheAgeSeconds = ((now - accountDistributionCache.timestamp) / 1000).toFixed(1)
    console.log(`[getAccountDistribution] Cache HIT (${cacheAgeSeconds}s old)`)
    return accountDistributionCache.data
  }

  const fetchMode = forceRefresh ? 'FORCE REFRESH' : 'Cache MISS'
  console.log(`[getAccountDistribution] ${fetchMode} - fetching from Lambda via CloudFront`)

  // 🚧 DEMO: Using public endpoint (no auth)
  // TODO: Revert to private for production:
  // const accessToken = localStorage.getItem('accessToken')
  // const data = await apiRequest<AccountDistribution>('/api/private/portfolios/account-distribution.json', {
  //   headers: { 'Authorization': `Bearer ${accessToken}` }
  // })
  const data = await apiRequest<AccountDistribution>('/api/general/portfolios/account-distribution.json')

  // Store in cache
  accountDistributionCache = {
    data,
    timestamp: now,
  }

  console.log('[getAccountDistribution] Cache STORED (TTL: 60 minutes)')

  return data
}

// ============================================================================
// Helper Functions
// ============================================================================

/**
 * Format AUM value as currency string
 */
export function formatAUM(aum: number): string {
  if (aum >= 1_000_000_000) {
    return `$${(aum / 1_000_000_000).toFixed(2)}B`
  } else if (aum >= 1_000_000) {
    return `$${(aum / 1_000_000).toFixed(2)}M`
  } else if (aum >= 1_000) {
    return `$${(aum / 1_000).toFixed(2)}K`
  } else {
    return `$${aum.toFixed(2)}`
  }
}

/**
 * Format period (YYYYMM) as readable string
 */
export function formatPeriod(period: string): string {
  if (!period || period === 'None') return 'N/A'

  const year = period.substring(0, 4)
  const month = period.substring(4, 6)
  const date = new Date(`${year}-${month}-01`)

  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short' })
}

/**
 * Format percentage change
 */
export function formatPercentChange(changePct: number | null): string {
  if (changePct === null || changePct === undefined || isNaN(changePct)) {
    return 'N/A'
  }

  const sign = changePct > 0 ? '+' : ''
  return `${sign}${changePct.toFixed(2)}%`
}

/**
 * Get color for percentage change
 */
export function getChangeColor(changePct: number | null): string {
  if (changePct === null || changePct === undefined || isNaN(changePct)) {
    return 'text-white/60'
  }

  return changePct > 0 ? 'text-success' : changePct < 0 ? 'text-danger' : 'text-white/60'
}

/**
 * Calculate month-over-month change for latest period
 */
export function getLatestMoMChange(timeSeries: PeriodData[]): {
  amount: number | null
  percent: number | null
} {
  if (timeSeries.length < 2) {
    return { amount: null, percent: null }
  }

  const latest = timeSeries[timeSeries.length - 1]
  return {
    amount: latest.aum_change,
    percent: latest.aum_change_pct,
  }
}

/**
 * Get summary statistics for a time series
 */
export function getTimeSeriesStats(timeSeries: PeriodData[]): {
  totalGrowth: number
  totalGrowthPct: number
  avgMonthlyChange: number
  peakAUM: number
  peakPeriod: string
} {
  if (timeSeries.length === 0) {
    return {
      totalGrowth: 0,
      totalGrowthPct: 0,
      avgMonthlyChange: 0,
      peakAUM: 0,
      peakPeriod: '',
    }
  }

  const firstPeriod = timeSeries[0]
  const lastPeriod = timeSeries[timeSeries.length - 1]

  const totalGrowth = lastPeriod.aum - firstPeriod.aum
  const totalGrowthPct = (totalGrowth / firstPeriod.aum) * 100

  const monthlyChanges = timeSeries
    .filter(p => p.aum_change !== null && !isNaN(p.aum_change))
    .map(p => p.aum_change as number)

  const avgMonthlyChange = monthlyChanges.length > 0
    ? monthlyChanges.reduce((sum, val) => sum + val, 0) / monthlyChanges.length
    : 0

  const peak = timeSeries.reduce((max, current) =>
    current.aum > max.aum ? current : max
  , timeSeries[0])

  return {
    totalGrowth,
    totalGrowthPct,
    avgMonthlyChange,
    peakAUM: peak.aum,
    peakPeriod: peak.period,
  }
}

/**
 * Sort models by AUM (descending)
 */
export function sortModelsByAUM(models: AUMByModel[]): AUMByModel[] {
  return [...models].sort((a, b) => b.aum - a.aum)
}

/**
 * Get model portfolio color
 */
export function getModelColor(modelName: string): string {
  const colorMap: Record<string, string> = {
    'Aggressive': '#f5365c',       // Red
    'Conservative': '#2dce89',     // Green
    'Intermediate': '#5e72e4',     // Purple-blue
    'Short-Term': '#fb6340',       // Orange
    'Ultra Short-Term': '#11cdef', // Teal
  }

  for (const [key, color] of Object.entries(colorMap)) {
    if (modelName.includes(key)) {
      return color
    }
  }

  return '#8b5cf6' // Default purple
}
```

---

## Participant Background

### 0.4.0_DS_ClientPlatform -- Pending Task Orders

#### data_contract.md

# Task Order — Data Contract: ClientPlatform

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-data-contract-client-platform</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-02</date>
    <status>pending</status>
  </metadata>

  <objective>
    Produce a data_contract.xml mapping the data layer for the ClientPlatform pod.
    This pod is architecturally unique: its two pages draw from entirely different
    pipelines. ModelPortfolios is Yang-driven (yang-model-portfolio-benchmarks).
    AdvisorIntelligence is BD-driven (opal-partners-data, bd-portal-publisher,
    bd-portal-advisor-publisher, bd-client-detail). Document both sides clearly,
    including the BD gold layer stages that produce the publisher inputs.
  </objective>

  <scope>
    <files>
      <!-- Primary input -->
      <file action="read">org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/pod_inventory.xml</file>

      <!-- ModelPortfolios Lambda -->
      <file action="read">infra/aws/lambda/yang_model_portfolio_benchmarks/lambda_function.py</file>

      <!-- AdvisorIntelligence Lambdas -->
      <file action="read">infra/aws/lambda/opal_partners_data/lambda_function.py</file>
      <file action="read">infra/aws/lambda/bd_portal_publisher/lambda_function.py</file>
      <file action="read">infra/aws/lambda/bd_portal_advisor_publisher/lambda_function.py</file>
      <file action="read">infra/aws/lambda/bd_client_detail/lambda_function.py</file>

      <!-- BD gold layer scripts that produce publisher inputs -->
      <file action="read">infra/aws/ec2/bd-gold-layer-runner/scripts/</file>

      <!-- Portal endpoint files -->
      <file action="read">portal/src/api/endpoints/advisor-intelligence.ts</file>
      <file action="read">portal/src/api/endpoints/aum.ts</file>

      <!-- Lambda source map -->
      <file action="read">infra/aws/lambda/ci/lambda-source-map.json</file>

      <!-- Output -->
      <file action="create">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read pod_inventory.xml first. Use the api_endpoints section to understand
      which endpoints serve ModelPortfolios vs AdvisorIntelligence and what
      data shapes the portal expects.
    </requirement>
    <requirement id="2">
      For ModelPortfolios: read yang_model_portfolio_benchmarks/lambda_function.py.
      Extract what Yang outputs it reads (S3 key patterns), what it produces,
      and how the portal fetches it via the Yang versioning system.
    </requirement>
    <requirement id="3">
      For AdvisorIntelligence: trace the BD publisher chain.
      Read opal_partners_data, bd_portal_publisher, and bd_portal_advisor_publisher.
      Document what S3 keys each Lambda writes (portal-ready JSON paths) and what
      shape each JSON has at its top level.
    </requirement>
    <requirement id="4">
      For bd_client_detail: document what it reads (per-client detail from gold tables),
      the S3 key pattern it writes to, and the response shape. This Lambda produces
      the drill-down data for advisor/client detail views in AdvisorIntelligence.
    </requirement>
    <requirement id="5">
      List the BD gold layer scripts (from infra/aws/ec2/bd-gold-layer-runner/scripts/)
      that feed the publisher Lambdas. Use Glob or ls to enumerate the scripts directory.
      Document which gold scripts produce the input that bd-portal-publisher and
      bd-portal-advisor-publisher consume. You do not need to document every script's
      internals — just which ones produce publisher-input data and what files they write.
    </requirement>
    <requirement id="6">
      Document the GEO/ADV cohort split in the AdvisorIntelligence data model.
      The portal has a GEO (geographic/city drill-down) and ADV (advisor/client
      drill-down) dimension. Document how these are reflected in the publisher
      output shape.
    </requirement>
    <requirement id="7">
      Mark task order status as "complete" when deliverable is written.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      data_contract.xml exists at org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml
    </criterion>
    <criterion id="2">
      File follows this schema:
      &lt;data_contract&gt;
        &lt;metadata&gt; agent, pod, date &lt;/metadata&gt;

        &lt;page_contracts&gt;
          One &lt;page&gt; per pod page:
            name,
            &lt;data_sources&gt;
              One &lt;source&gt; per distinct data feed:
                lambda_function, trigger, s3_output_key_pattern,
                &lt;response_shape&gt; top-level keys and value types &lt;/response_shape&gt;
                &lt;portal_endpoint&gt; endpoint function &lt;/portal_endpoint&gt;
            &lt;/data_sources&gt;
            &lt;data_freshness&gt; how often data is updated &lt;/data_freshness&gt;
        &lt;/page_contracts&gt;

        &lt;pipeline_split&gt;
          Explicit documentation of the Yang vs BD pipeline boundary:
            ModelPortfolios: yang-pipeline source, trigger, versioning
            AdvisorIntelligence: bd-pipeline source, gold stage inputs, publisher outputs
        &lt;/pipeline_split&gt;

        &lt;bd_gold_inputs&gt;
          Which BD gold scripts produce data consumed by the portal publishers.
          One entry per gold script that feeds publisher input.
        &lt;/bd_gold_inputs&gt;

        &lt;upstream_dependencies&gt;
          For Yang side: Yang PKL workspace, benchmark data
          For BD side: 49 Financial allocation/transaction raw files, BD gold tables
        &lt;/upstream_dependencies&gt;

        &lt;data_quality_notes&gt;
          Known issues: AUA undercount history, data shape mismatches, fallback
          behaviors found in code comments
        &lt;/data_quality_notes&gt;

        &lt;gaps&gt;
          Any data sources where the contract could not be determined from code
        &lt;/gaps&gt;
      &lt;/data_contract&gt;
    </criterion>
    <criterion id="3">
      pipeline_split section must be complete and unambiguous. The Yang/BD split
      is the most important architectural fact about this pod.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not modify any Lambda source files or portal files.</constraint>
    <constraint>Do not run any Lambda functions or AWS CLI commands.</constraint>
    <constraint>
      infra/aws/ec2/bd-gold-layer-runner/scripts/ is a directory.
      Use Glob or Bash ls to enumerate its contents before reading individual scripts.
      You only need to identify which scripts produce publisher-input data —
      do not read every gold script in full.
    </constraint>
    <constraint>
      If a Lambda file path is not found at the underscore path, try hyphen variants.
      Document the actual path found.
    </constraint>
    <constraint>
      The BD pipeline had a significant AUA undercount incident resolved in the
      Feb 23-27 sprint. Code comments or recent edits in the publisher Lambdas
      may reference this. Note any such context in data_quality_notes.
    </constraint>
    <constraint>
      The full BD pipeline infrastructure (allocation trigger, transaction processing,
      gold layer runner) is owned by DS_PartnerETL (0.6.0_AE_PartnerETL). Your scope
      is the portal-facing output layer only: publisher Lambdas + opal-partners-data.
      Reference the BD pipeline as an upstream dependency, do not re-document its
      full internals.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform" task="pod_inventory" status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml
    </deliverable>
  </deliverables>
</task_order>
```


### 0.6.0_AE_PartnerETL -- Pending Task Orders

#### infrastructure_inventory.md

# Task Order: Infrastructure Inventory

<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-infrastructure-inventory</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-02</date>
    <status>pending</status>
  </metadata>

  <objective>
    Produce a complete structured inventory of all AWS infrastructure in your scope.
    This is a one-time audit that becomes your permanent context for all future sessions.
    Read every Terraform file, Lambda source directory, and deployment artifact in your
    pipeline scope and document what exists.
  </objective>

  <scope>
    <terraform_dirs>
      <dir>infra/aws/terraform/bd-pipeline/</dir>
    </terraform_dirs>
    <lambda_source_map>infra/aws/lambda/ci/lambda-source-map.json</lambda_source_map>
    <data_scripts>
      <dir>data/black_diamond/scripts/bronze/</dir>
      <dir>data/black_diamond/scripts/silver/</dir>
      <dir>data/black_diamond/scripts/gold/</dir>
    </data_scripts>
    <ec2_manifest>infra/aws/ec2/EC2_MANIFEST.json</ec2_manifest>
  </scope>

  <requirements>
    <requirement id="1">For every Terraform pipeline directory in your scope: list all .tf files with a 1-line description of what each declares</requirement>
    <requirement id="2">For every Lambda function in your scope (from lambda-source-map.json and Terraform): document the function name, source directory, runtime, memory, timeout, trigger type (S3/EventBridge/API Gateway/Step Functions), and what it does</requirement>
    <requirement id="3">For every Lambda Layer used by your functions: document the layer name, S3 key, version, and what packages it provides</requirement>
    <requirement id="4">For every IAM role in your Terraform: document the role name, what services it grants access to, and key policy statements</requirement>
    <requirement id="5">For every EventBridge rule or S3 notification trigger: document the schedule/event pattern and what it invokes</requirement>
    <requirement id="6">For every S3 path your pipelines read from or write to: document the bucket, prefix, and data flow direction</requirement>
    <requirement id="7">Document the current deployment tag and any pipelines that are NOT yet Terraformed</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Output is valid XML written to org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/infrastructure_inventory.xml</criterion>
    <criterion id="2">Every Lambda function in your scope from lambda-source-map.json is accounted for</criterion>
    <criterion id="3">Every .tf file in your Terraform directories is referenced</criterion>
    <criterion id="4">Trigger types and schedules are actual values from the Terraform, not guesses</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify any source code or infrastructure -- this is a read-only audit</constraint>
    <constraint>Do NOT run terraform plan/apply or any AWS CLI commands</constraint>
    <constraint>Do NOT create or edit files outside your agent folder</constraint>
    <constraint>Use Glob, Grep, and Read tools only -- no Explore agent, no Task agent</constraint>
  </constraints>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/infrastructure_inventory.xml
    </deliverable>
  </deliverables>
</task_order>

## Key Files to Read

### Terraform Directory
- `infra/aws/terraform/bd-pipeline/` -- all .tf files (tag: bd-v2.14.0)

### Lambda Source Map
- `infra/aws/lambda/ci/lambda-source-map.json` -- filter to all bd-* functions

### Lambda Source Directories
- `infra/aws/lambda/bd-pipeline/` -- BD pipeline Lambda functions
- Any other `bd-*` directories under `infra/aws/lambda/`
- Read each function's handler file to understand what it does

### Data Scripts (Bronze / Silver / Gold layers)
- `data/black_diamond/scripts/bronze/` -- raw data ingestion scripts
- `data/black_diamond/scripts/silver/` -- data cleaning and transformation scripts
- `data/black_diamond/scripts/gold/` -- 10 active gold scripts run sequentially (00 through 10)
  - Read each script to understand its role in the sequential pipeline

### EC2 Manifest
- `infra/aws/ec2/EC2_MANIFEST.json` -- BD gold layer runner service entry

### Deployment Tag
- bd-v2.14.0

## Deliverable XML Schema

Write your inventory using this structure:

```xml
<infrastructure_inventory>
  <metadata>
    <agent>0.6.0_AE_PartnerETL</agent>
    <scope>BD (Black Diamond / 49 Financial)</scope>
    <date>2026-03-02</date>
  </metadata>

  <pipelines>
    <pipeline name="{name}" terraform_dir="infra/aws/terraform/{dir}/" tag="{current_tag}">

      <lambda_functions>
        <lambda name="{function_name}"
                source_dir="infra/aws/lambda/{dir}/"
                tf_resource="{module.name.aws_lambda_function.this}"
                runtime="python3.12"
                memory_mb="256"
                timeout_s="30"
                trigger="{S3 | EventBridge | API Gateway | Step Functions | manual}"
                last_deployed="{commit_sha} @ {date}">
          One-line description of what this function does
        </lambda>
      </lambda_functions>

      <layers>
        <layer name="{layer_name}" s3_key="{key}" version="{n}">
          What packages this layer provides
        </layer>
      </layers>

      <iam_roles>
        <role name="{role_name}" tf_resource="{resource_path}">
          What this role allows -- key policy statements
        </role>
      </iam_roles>

      <triggers>
        <trigger type="{EventBridge | S3 | API Gateway}" resource="{rule/bucket/api}">
          Schedule or event pattern
        </trigger>
      </triggers>

      <s3_paths>
        <path bucket="{bucket}" prefix="{prefix}" direction="read | write">
          What data flows through this path
        </path>
      </s3_paths>

    </pipeline>
  </pipelines>

  <ec2_services>
    <service name="{service}" instance_id="{id}" manifest_entry="true | false">
      What this EC2 instance runs
    </service>
  </ec2_services>
</infrastructure_inventory>
```

#### pipeline_inventory.md

# Task Order — Pipeline Inventory: PartnerETL

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-pipeline-inventory-partner-etl</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-02</date>
    <status>pending</status>
  </metadata>

  <objective>
    Produce a pipeline_inventory.xml covering the entire BD pipeline — the
    partner ETL that processes 49 Financial's allocation, transaction, and
    portfolio data into gold-layer outputs consumed by AdvisorIntelligence
    and other client-facing portal views. This is your permanent activation
    document. The BD pipeline is the most operationally complex in the system
    (multi-stage gold layer, EC2 runner, ephemeral EC2 for historical prices,
    multiple publisher chains). Thorough documentation is critical.
  </objective>

  <scope>
    <files>
      <!-- Terraform module — read all .tf files -->
      <file action="read">infra/aws/terraform/bd-pipeline/main.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/lambdas.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/iam.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/eventbridge.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/layers.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/ec2.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/s3-notifications.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/CHANGELOG.json</file>

      <!-- Gold layer scripts (EC2 runner) — document what each script does -->
      <file action="read">infra/aws/ec2/bd-gold-layer-runner/run_gold_layer.sh</file>

      <!-- Lambda source map — filter to bd- prefixed functions -->
      <file action="read">infra/aws/lambda/ci/lambda-source-map.json</file>

      <!-- EC2 manifest — bd services -->
      <file action="read">infra/aws/ec2/EC2_MANIFEST.json</file>

      <!-- Output -->
      <file action="create">org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/pipeline_inventory.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read all .tf files in infra/aws/terraform/bd-pipeline/ in full. Extract every
      aws_lambda_function, aws_lambda_layer_version, aws_cloudwatch_event_rule,
      aws_instance, aws_s3_bucket_notification, and aws_iam_role resource.
    </requirement>
    <requirement id="2">
      From lambda-source-map.json, extract source_path, memory_mb, timeout_s,
      and last_deployed_commit for all bd- prefixed functions:
      bd-allocation-processor, bd-allocation-trigger, bd-client-detail,
      bd-gold-detail-checker, bd-gold-foundation, bd-gold-layer, bd-gold-trigger,
      bd-portal-advisor-publisher, bd-portal-publisher, bd-price-update,
      bd-transactions-trigger. Also include historical-prices-scheduler (BD-owned).
    </requirement>
    <requirement id="3">
      Read run_gold_layer.sh to document the gold layer execution stages.
      The BD gold layer runs in numbered stages (01 through 10+) on an EC2 runner.
      Document each stage: script name, what it produces, dependencies, whether
      it runs in the full or incremental path.
    </requirement>
    <requirement id="4">
      From EC2_MANIFEST.json, identify all BD EC2 services: bd-gold-layer-runner
      (persistent), bd-gold-detail-generator (ephemeral), historical-prices EC2.
      Document instance IDs, source paths, and last deployed commits.
    </requirement>
    <requirement id="5">
      Document the full pipeline trigger chain:
      S3 drop (raw allocation/transaction file) → EventBridge or S3 notification →
      trigger Lambda → processor Lambda → gold layer stages → publisher Lambdas →
      portal S3 output. This chain is the operational heart of the BD pipeline.
    </requirement>
    <requirement id="6">
      Note the current Terraform tag from CHANGELOG.json as the version baseline.
    </requirement>
    <requirement id="7">
      Mark task order status as "complete" when deliverable is written.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      pipeline_inventory.xml exists at org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/pipeline_inventory.xml
    </criterion>
    <criterion id="2">
      File follows this schema:
      &lt;pipeline_inventory&gt;
        &lt;metadata&gt; agent, pipeline="bd-pipeline", current_tag, date &lt;/metadata&gt;

        &lt;pipeline name="bd-pipeline" terraform_module="infra/aws/terraform/bd-pipeline/" current_tag="bd-vX.Y.Z"&gt;
          &lt;trigger_chain&gt;
            Ordered description of how a raw data file becomes portal output.
            Name every Lambda in sequence, every S3 key written, every EC2 stage.
          &lt;/trigger_chain&gt;

          &lt;lambdas&gt;
            One &lt;lambda&gt; per function:
              name, source_path, memory_mb, timeout_s, layers[], trigger, role_in_pipeline
          &lt;/lambdas&gt;

          &lt;gold_layer_stages&gt;
            One &lt;stage&gt; per gold script:
              script_name, stage_number, produces, depends_on, runs_in (full|incremental|both)
          &lt;/gold_layer_stages&gt;

          &lt;ec2_services&gt;
            One &lt;service&gt; per EC2:
              name, type (persistent|ephemeral), instance_id, source_path, last_deployed_commit
          &lt;/ec2_services&gt;

          &lt;eventbridge_rules&gt; rule name, schedule_or_trigger, target &lt;/eventbridge_rules&gt;
          &lt;s3_notifications&gt; bucket, prefix filter, target Lambda &lt;/s3_notifications&gt;
          &lt;layers&gt; layer name, S3 key, Python packages &lt;/layers&gt;
          &lt;iam_roles&gt; role names owned &lt;/iam_roles&gt;
        &lt;/pipeline&gt;

        &lt;known_issues&gt;
          Operational notes, known drift, gotchas from recent incidents
        &lt;/known_issues&gt;
      &lt;/pipeline_inventory&gt;
    </criterion>
    <criterion id="3">
      trigger_chain section must be complete — it is the primary operational reference
      for anyone debugging a data delivery failure.
    </criterion>
    <criterion id="4">
      All function names, instance IDs, script names, and tag values are verbatim
      from source files.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not modify any Terraform files or EC2 scripts. Read-and-document only.</constraint>
    <constraint>Do not run terraform plan, apply, or any AWS CLI commands.</constraint>
    <constraint>
      The BD pipeline has had several recent operational incidents (AUA undercount,
      triple-bug fix, EC2 gold runner expansion to scripts 09+10). Document known
      operational complexity in known_issues rather than trying to resolve it.
    </constraint>
    <constraint>
      historical-prices-scheduler is technically a BD pipeline asset (it feeds
      bd-price-update). Include it in the BD pipeline inventory even though its
      Lambda prefix is not bd-.
    </constraint>
  </constraints>

  <dependencies>
    <!-- No pod wave dependencies — AE pipelines are independent -->
  </dependencies>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/pipeline_inventory.xml
    </deliverable>
  </deliverables>
</task_order>
```


