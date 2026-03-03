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
