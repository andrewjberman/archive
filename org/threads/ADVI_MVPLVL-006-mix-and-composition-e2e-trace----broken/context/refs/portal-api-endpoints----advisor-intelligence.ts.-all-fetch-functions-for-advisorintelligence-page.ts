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
  BooksTimeseriesResponse,
  BooksCompositionResponse,
  FirmMixViewsResponse,
  MixTimeseriesPoint,
  MixWindow,
  ConcentrationResponse,
  AdvisorTimeseriesResponse,
  AdvisorMixTimeseriesResponse,
} from '@/pages/AdvisorIntelligence/types'

// ============================================================================
// Configuration
// ============================================================================

// API base URL
const API_BASE_URL = import.meta.env.VITE_PORTAL_API_URL ?? ''

// S3 bucket suffix -> DynamoDB firm key mapping for Lambda-routed endpoints.
// S3-routed endpoints use ?firm={bucketSuffix}, but Lambda endpoints (opal-partners-data)
// expect ?firmId={ddbFirmId} where the value is the DynamoDB partition key.
const LAMBDA_FIRM_ID: Record<string, string> = { bd: '49financial' }

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
 * Dynamic API call — firmId is passed as query param.
 * Routes via CloudFront /api/scoped/ -> shared-advisor-router -> opal-data-{firmId}/gold/
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
export async function getHeaderMetrics(firmOverride?: string): Promise<HeaderMetricsResponse> {
  const base = '/api/scoped/advisor-intelligence/summary/header_metrics.json'
  return await apiRequest<HeaderMetricsResponse>(firmOverride ? `${base}?firm=${firmOverride}` : base)
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
export async function getPartnerAnalytics(granularity: 'monthly' | 'quarterly' | 'annually' = 'quarterly', firmOverride?: string): Promise<PartnerAnalyticsResponse> {
  // S3 files use _annual (not _annually) — map the suffix
  const suffix = granularity === 'annually' ? 'annual' : granularity
  const base = `/api/scoped/advisor-intelligence/partner_analytics/header_metrics_${suffix}.json`
  return await apiRequest<PartnerAnalyticsResponse>(firmOverride ? `${base}?firm=${firmOverride}` : base)
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
export async function getCumulativeChart(firmOverride?: string): Promise<CumulativeChartResponse> {
  const base = '/api/scoped/advisor-intelligence/timeseries_chart.json'
  return await apiRequest<CumulativeChartResponse>(firmOverride ? `${base}?firm=${firmOverride}` : base)
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
export async function getClientsTab(firmOverride?: string): Promise<ClientsTabResponse> {
  const base = '/api/scoped/advisor-intelligence/clients_tab.json'
  return await apiRequest<ClientsTabResponse>(firmOverride ? `${base}?firm=${firmOverride}` : base)
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
export async function getClientDetail(clientKey: string, firmOverride?: string): Promise<ClientDetailResponse> {
  const base = `/api/scoped/advisor-intelligence/clients/${clientKey}.json`
  return await apiRequest<ClientDetailResponse>(firmOverride ? `${base}?firm=${firmOverride}` : base)
}

/**
 * Get Architect Leaderboard data
 *
 * Returns ranked list of architects by NNA (trailing 12M):
 * - entries: Ranked architect data with NNA, AUA growth %, new clients
 * - summary: Aggregate totals (total_nna, total_aua, positive/negative counts)
 */
export async function getArchitectLeaderboard(firmOverride?: string): Promise<LeaderboardResponse> {
  const base = '/api/scoped/advisor-intelligence/architect_leaderboard.json'
  return await apiRequest<LeaderboardResponse>(firmOverride ? `${base}?firm=${firmOverride}` : base)
}

/**
 * Get Implementor Leaderboard data
 *
 * Returns ranked list of implementors by NNA (trailing 12M):
 * - entries: Ranked implementor data with NNA, AUA growth %, new clients
 * - summary: Aggregate totals (total_nna, total_aua, positive/negative counts)
 */
export async function getImplementorLeaderboard(firmOverride?: string): Promise<LeaderboardResponse> {
  const base = '/api/scoped/advisor-intelligence/implementor_leaderboard.json'
  return await apiRequest<LeaderboardResponse>(firmOverride ? `${base}?firm=${firmOverride}` : base)
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
export async function getAdvisorBook(advisorId: string, firmOverride?: string): Promise<AdvisorBookResponse> {
  const base = `/api/scoped/advisor-intelligence/advisors/${advisorId}/book.json`
  return await apiRequest<AdvisorBookResponse>(firmOverride ? `${base}?firm=${firmOverride}` : base)
}

/**
 * Get Advisor Rolling Flows data (Advisors tab -- two views)
 *
 * Returns both NNA summary (donut chart) and rolling time series:
 * - summary.architects / summary.implementors: MTD/QTD/YTD NNA breakdown by advisor
 * - architects[] / implementors[]: daily rolling 30d/90d/1Y flows per advisor
 *
 * Static JSON served via CloudFront -> S3 (shared-advisor-router routes to opal-data-{firmId}/gold/)
 */
export async function getAdvisorRollingFlows(firmOverride?: string): Promise<AdvisorRollingFlowsResponse> {
  const base = '/api/scoped/advisor-intelligence/advisor_rolling_flows.json'
  return await apiRequest<AdvisorRollingFlowsResponse>(firmOverride ? `${base}?firm=${firmOverride}` : base)
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
export async function getBooksClientDetail(clientKey: string, firmOverride?: string): Promise<BooksClientDetailResponse> {
  const base = `/api/scoped/advisor-intelligence/clients/${clientKey}.json`
  return await apiRequest<BooksClientDetailResponse>(firmOverride ? `${base}?firm=${firmOverride}` : base)
}

/**
 * Get Books relationship-level timeseries (AUA + cumulative flows)
 *
 * @param relationshipId - Relationship identifier
 */
export async function getBooksRelationshipTimeseries(relationshipId: string, firmOverride?: string): Promise<BooksTimeseriesResponse> {
  const base = `/api/scoped/partners/books/relationship/${relationshipId}/timeseries`
  return await apiRequest<BooksTimeseriesResponse>(firmOverride ? `${base}?firmId=${LAMBDA_FIRM_ID[firmOverride] ?? firmOverride}` : base)
}

/**
 * Get Books account-level timeseries (AUA + cumulative flows)
 *
 * @param accountId - Account identifier
 */
export async function getBooksAccountTimeseries(accountId: string, firmOverride?: string): Promise<BooksTimeseriesResponse> {
  const base = `/api/scoped/partners/books/account/${accountId}/timeseries`
  return await apiRequest<BooksTimeseriesResponse>(firmOverride ? `${base}?firmId=${LAMBDA_FIRM_ID[firmOverride] ?? firmOverride}` : base)
}

/**
 * Get Books relationship-level composition (asset class mix + concentration)
 *
 * @param relationshipId - Relationship identifier
 */
/**
 * Get Books firm-level composition (asset class mix + top-N concentration)
 * Aggregates ALL open holdings across the firm.
 */
export async function getBooksFirmComposition(firmOverride?: string): Promise<BooksCompositionResponse> {
  const firmKey = firmOverride ? (LAMBDA_FIRM_ID[firmOverride] ?? firmOverride) : '49financial'
  return await apiRequest<BooksCompositionResponse>(`/api/scoped/partners/books/firm/all/composition?firmId=${firmKey}`)
}

export async function getBooksRelationshipComposition(relationshipId: string, firmOverride?: string): Promise<BooksCompositionResponse> {
  const base = `/api/scoped/partners/books/relationship/${relationshipId}/composition`
  return await apiRequest<BooksCompositionResponse>(firmOverride ? `${base}?firmId=${LAMBDA_FIRM_ID[firmOverride] ?? firmOverride}` : base)
}

/**
 * Get Books account-level composition (asset class mix + concentration)
 *
 * @param accountId - Account identifier
 */
export async function getBooksAccountComposition(accountId: string, firmOverride?: string): Promise<BooksCompositionResponse> {
  const base = `/api/scoped/partners/books/account/${accountId}/composition`
  return await apiRequest<BooksCompositionResponse>(firmOverride ? `${base}?firmId=${LAMBDA_FIRM_ID[firmOverride] ?? firmOverride}` : base)
}

// The Lambda serves the full client_timeseries JSON envelope for both mix and concentration.
interface ClientTimeseriesEnvelope {
  generated_at: string
  data_as_of: string
  relationship_id: string | number
  mix: MixTimeseriesPoint[]
  concentration: ConcentrationResponse
}

/**
 * Get Mix timeseries for a relationship (asset class allocation over time)
 *
 * Returns daily data points where each class is 0-1 pct, summing to 1.0 per row.
 * The Lambda serves the full envelope ({mix, concentration}); this function extracts mix[].
 *
 * @param relationshipId - Relationship identifier. Use '0' for firm-level aggregate.
 * @param firmId - Partner firm ID (S3 bucket suffix, e.g. 'bd')
 * @param window - Time window: 1Y, 3Y, or Max (client-side filter only)
 */
export async function getMixTimeseries(
  relationshipId: string,
  firmId: string,
  window?: MixWindow
): Promise<MixTimeseriesPoint[]> {
  const params = new URLSearchParams({ firmId: LAMBDA_FIRM_ID[firmId] ?? firmId })
  if (window) params.set('window', window)
  const envelope = await apiRequest<ClientTimeseriesEnvelope>(
    `/api/scoped/partners/books/relationship/${relationshipId}/mix-timeseries?${params}`
  )
  return envelope.mix ?? []
}

/**
 * Get firm-level aggregate mix timeseries (relationship_id = '0').
 * 2,000+ daily data points spanning full firm history.
 *
 * @param firmId - Partner firm ID (S3 bucket suffix, e.g. 'bd')
 */
export async function getFirmMixTimeseries(firmId: string): Promise<MixTimeseriesPoint[]> {
  return getMixTimeseries('0', firmId)
}

/**
 * Get firm-level pre-aggregated mix views (quarterly, monthly, annually).
 *
 * Returns absolute dollar amounts and allocation fractions (0-1) per asset class
 * for each period. Replaces the daily getMixTimeseries + client-side aggregation approach.
 *
 * @param firmId - Partner firm ID (S3 bucket suffix, e.g. 'bd')
 */
export async function getFirmMixViews(firmId: string): Promise<FirmMixViewsResponse> {
  const resolvedFirmId = LAMBDA_FIRM_ID[firmId] ?? firmId
  return await apiRequest<FirmMixViewsResponse>(
    `/api/scoped/partners/books/firm/all/mix-views?firmId=${resolvedFirmId}`
  )
}

/**
 * Get Concentration timeseries for a relationship (top-N holdings over time)
 *
 * Returns flat array of top-N holdings per date, filtered by window.
 * top_n field indicates the N used by the Lambda.
 *
 * @param relationshipId - Relationship identifier
 * @param firmId - Partner firm ID
 * @param window - Time window: 1Y, 3Y, or Max (default 1Y)
 */
export async function getConcentrationTimeseries(
  relationshipId: string,
  firmId: string,
  window?: MixWindow
): Promise<ConcentrationResponse> {
  const params = new URLSearchParams({ firmId: LAMBDA_FIRM_ID[firmId] ?? firmId })
  if (window) params.set('window', window)
  return await apiRequest<ConcentrationResponse>(
    `/api/scoped/partners/books/relationship/${relationshipId}/concentration-timeseries?${params}`
  )
}

export async function getAdvisorTimeseries(
  advisorId: string,
  firmId: string
): Promise<AdvisorTimeseriesResponse> {
  const mappedFirmId = LAMBDA_FIRM_ID[firmId] ?? firmId
  return await apiRequest<AdvisorTimeseriesResponse>(
    `/api/scoped/partners/books/advisor/${advisorId}/timeseries?firmId=${mappedFirmId}`
  )
}

export async function getAdvisorMixTimeseries(
  advisorId: string,
  firmId: string,
  window?: MixWindow
): Promise<AdvisorMixTimeseriesResponse> {
  const mappedFirmId = LAMBDA_FIRM_ID[firmId] ?? firmId
  const params = new URLSearchParams({ firmId: mappedFirmId })
  if (window) params.set('window', window)
  return await apiRequest<AdvisorMixTimeseriesResponse>(
    `/api/scoped/partners/books/advisor/${advisorId}/mix-timeseries?${params}`
  )
}
