 
/**
 * Partner Analytics Panel - v5
 *
 * Header panel for Advisor Intelligence page with multi-view support.
 * Mirrors the Model Portfolios "Portfolio Analytics" pattern:
 * - Left: Donut chart showing breakdown by selected view
 * - Right: Bell curve showing distribution
 * - Below: Quarterly metrics with time machine support
 *
 * Views (toggle bar):
 * - AUA: Total assets by client type (new vs existing) - default
 * - NNA: Net new assets with inflows/outflows drill-down
 * - GEO: Geographic breakdown with city drill-down
 * - ADV: Architect breakdown with client drill-down
 */

import { useState, useEffect, useMemo, useCallback } from 'react'
import { useQuery } from '@tanstack/react-query'
import { AreaChart, Area, BarChart, Bar, Cell, ComposedChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, ReferenceLine } from 'recharts'
import { Panel, PanelHeader, PanelContent, PanelFooter } from '@/ui/components/panels'
import { LoadingInline } from '@/components/LoadingSpinner'
import { Tooltip } from '@/components/Tooltip'
import { HelpCircle } from 'lucide-react'
import { formatCurrency } from '@/lib/universalNumberFormatter'
import type { PartnerAnalyticsResponse, PartnerAnalyticsViewMode, DistributionStats, DonutSegment, CitySegment, ClientSegment, TimePeriodKey, PeriodSnapshot, PartnerAnalyticsViewWithPeriods, PartnerAnalyticsView, CumulativeChartResponse, GrowthDecompositionPoint, AuaDataPoint } from '../types'

// Mock AUA timeseries in the PSCFIX schema (used as placeholderData until publisher Lambda is live)
const MOCK_AUA_TIMESERIES: Partial<CumulativeChartResponse> = {
  aua: {
    quarterly: {
      categories: ['NMNC', 'NMEC'],
      data: [
        { period: '2023-Q4', label: "Q4 '23", end_date: '2023-12-31', NMNC: 160000000, NMEC: 1060000000 },
        { period: '2024-Q1', label: "Q1 '24", end_date: '2024-03-31', NMNC: 190000000, NMEC: 1090000000 },
        { period: '2024-Q2', label: "Q2 '24", end_date: '2024-06-30', NMNC: 220000000, NMEC: 1130000000 },
        { period: '2024-Q3', label: "Q3 '24", end_date: '2024-09-30', NMNC: 250000000, NMEC: 1190000000 },
        { period: '2024-Q4', label: "Q4 '24", end_date: '2024-12-31', NMNC: 280000000, NMEC: 1250000000 },
        { period: '2025-Q1', label: "Q1 '25", end_date: '2025-03-09', NMNC: 300000000, NMEC: 1300000000 },
      ],
    },
    monthly: {
      categories: ['NMNC', 'NMEC'],
      data: [
        { period: '2024-10', label: "Oct '24", end_date: '2024-10-31', NMNC: 256000000, NMEC: 1220000000 },
        { period: '2024-11', label: "Nov '24", end_date: '2024-11-30', NMNC: 265000000, NMEC: 1232000000 },
        { period: '2024-12', label: "Dec '24", end_date: '2024-12-31', NMNC: 280000000, NMEC: 1250000000 },
        { period: '2025-01', label: "Jan '25", end_date: '2025-01-31', NMNC: 288000000, NMEC: 1268000000 },
        { period: '2025-02', label: "Feb '25", end_date: '2025-02-28', NMNC: 295000000, NMEC: 1284000000 },
        { period: '2025-03', label: "Mar '25", end_date: '2025-03-09', NMNC: 300000000, NMEC: 1300000000 },
      ],
    },
    annually: {
      categories: ['NMNC', 'NMEC'],
      data: [
        { period: '2022', label: '2022', end_date: '2022-12-31', NMNC: 100000000, NMEC:  900000000 },
        { period: '2023', label: '2023', end_date: '2023-12-31', NMNC: 160000000, NMEC: 1060000000 },
        { period: '2024', label: '2024', end_date: '2024-12-31', NMNC: 280000000, NMEC: 1250000000 },
        { period: '2025', label: '2025', end_date: '2025-03-09', NMNC: 300000000, NMEC: 1300000000 },
      ],
    },
  },
}
import { hasTimeMachine } from '../types'
import { getCumulativeChart } from '@/api/endpoints/advisor-intelligence'
import { useSelectTracking } from '@/hooks/useFilterTracking'
import { useAuth } from '@/hooks/useAuth'

// Granularity options for bar charts (Monthly | Quarterly | Annually)
type GranularityOption = 'monthly' | 'quarterly' | 'annually'

// Panel view mode: AUA (stacked bar), NNA (diverging bar), GRO (growth decomposition lines)
type PanelViewMode = 'aua' | 'nna' | 'gro'

// AUA sub-mode: Clients (NMNC/NMEC) or Mix (asset class breakdown)
type AuaSubMode = 'clients' | 'mix'

// Y3-FE: AUA sub-mode label — placeholder pending Andrew/Yang decision
const AUA_SUB_MODE_CLIENTS_LABEL = 'Clients'

// Time window for chart data
type TimeWindow = '1Y' | '3Y' | 'Max'

// Category colors for AUA stacked bar chart
const CATEGORY_COLORS: Record<string, string> = {
  'NMNC': '#4CAF50',           // Green - New Client Assets
  'nmnc': '#4CAF50',
  'NMEC': '#2196F3',           // Blue - Existing Client Assets
  'nmec': '#2196F3',
}

// NNA flow colors
const NNA_COLORS = {
  inflow: '#2196F3',   // Blue - Inflows (positive, above zero)
  outflow: '#EF4444',  // Red - Outflows (negative, below zero)
}

const FALLBACK_COLORS = [
  '#4CAF50', '#2196F3', '#F59E0B', '#EF4444', '#8B5CF6', '#6B7280',
]

// Y3-FE: Asset class colors for Mix mode (distinct from NMNC/NMEC)
const ASSET_CLASS_COLORS: Record<string, string> = {
  'Equities': '#8B5CF6',        // Violet
  'Fixed Income': '#06B6D4',    // Cyan
  'Real Estate': '#F97316',     // Orange
  'Alternatives': '#EC4899',    // Pink
  'Cash': '#6B7280',            // Gray
  'Other': '#A3A3A3',           // Light gray
}

function getAssetClassColor(label: string, index: number): string {
  return ASSET_CLASS_COLORS[label] || FALLBACK_COLORS[index % FALLBACK_COLORS.length]
}

// Y5-FE: GRO growth decomposition line colors
const GRO_COLORS = {
  market: '#8B5CF6',  // Violet — Market Performance
  nna: '#2196F3',     // Blue — NNA (reuse existing NNA color)
  total: '#F59E0B',   // Amber — Total AUA Change
}

function getBarCategoryColor(category: string, index: number): string {
  return CATEGORY_COLORS[category] || FALLBACK_COLORS[index % FALLBACK_COLORS.length]
}

// Category display names
const CATEGORY_DISPLAY_NAMES: Record<string, string> = {
  'NMNC': 'New Client Assets',
  'nmnc': 'New Client Assets',
  'NMEC': 'Existing Client Assets',
  'nmec': 'Existing Client Assets',
}

function getBarCategoryDisplayName(category: string): string {
  return CATEGORY_DISPLAY_NAMES[category] || category
}

const AVAILABLE_FIRMS = [
  { id: 'bd', name: '49 Financial' },
]

interface PartnerAnalyticsProps {
  data: PartnerAnalyticsResponse | null
  isLoading: boolean
  selectedFirmId: string
  onPartnerChange: (firmId: string) => void
  granularity: GranularityOption
  onGranularityChange: (g: GranularityOption) => void
  firmOverride?: string
}

// View mode labels (city/client are hidden - accessed via drill-down)
const VIEW_LABELS: Record<PartnerAnalyticsViewMode, string> = {
  aua: 'AUA',      // Default - AUA by client type
  nna: 'NNA',      // Flows view with drill-down
  geo: 'GEO',
  city: 'City',    // Not shown in toggle, used for GEO drill-down
  adv: 'ADV',
  client: 'Client',  // Not shown in toggle, used for ADV drill-down
}

// GEO drill-down state type
type GeoDrillLevel = 'state' | 'city'

// ADV drill-down state type
type AdvDrillLevel = 'architect' | 'client'

// NNA drill-down state type (segment → flows showing inflows/outflows)
type NnaDrillLevel = 'segment' | 'flow'

export function PartnerAnalytics({ data, isLoading, selectedFirmId, onPartnerChange, granularity, onGranularityChange, firmOverride }: PartnerAnalyticsProps) {
  const { isInternal } = useAuth()
  const internal = isInternal()
  // View mode with analytics tracking
  const [viewMode, _setViewMode] = useSelectTracking<PartnerAnalyticsViewMode>('view-mode', 'aua', 'partner-analytics')

  // GEO drill-down state
  const [geoDrillLevel, _setGeoDrillLevel] = useState<GeoDrillLevel>('state')
  const [selectedStateKey, _setSelectedStateKey] = useState<string | null>(null)
  const [selectedCityKey, _setSelectedCityKey] = useState<string | null>(null)  // City selection for distribution

  // ADV drill-down state
  const [advDrillLevel, _setAdvDrillLevel] = useState<AdvDrillLevel>('architect')
  const [selectedArchitectKey, _setSelectedArchitectKey] = useState<string | null>(null)
  const [selectedClientKey, _setSelectedClientKey] = useState<string | null>(null)  // Client selection for distribution

  // NNA drill-down state (segment level → flow level showing inflows/outflows)
  const [nnaDrillLevel, _setNnaDrillLevel] = useState<NnaDrillLevel>('segment')
  const [selectedNnaSegmentKey, _setSelectedNnaSegmentKey] = useState<string | null>(null)
  const [selectedNnaFlowKey, _setSelectedNnaFlowKey] = useState<string | null>(null)  // Flow selection for distribution

  // Time Machine state with analytics tracking
  const [selectedPeriod, _setSelectedPeriod] = useSelectTracking<TimePeriodKey>('time-period', 'current', 'partner-analytics')

  // Panel-level view mode: AUA (stacked bar), NNA (diverging bar), GRO (growth decomposition)
  const [panelViewMode, setPanelViewMode] = useState<PanelViewMode>('aua')

  // Y3-FE: AUA sub-mode (Clients = NMNC/NMEC, Mix = asset class breakdown)
  const [auaSubMode, setAuaSubMode] = useState<AuaSubMode>('clients')

  // Time window: 1Y, 3Y, Max
  const [timeWindow, setTimeWindow] = useState<TimeWindow>('3Y')

  // Bar Chart state with analytics tracking for granularity
  // granularity is controlled from AdvisorIntelligence.tsx (drives the query re-fetch)
  const [selectedBarPeriod, setSelectedBarPeriod] = useState<string | null>(null) // Selected bar period key (e.g., "2023-Q1")

  // Maps granularity prop to the aua sub-key in the PSCFIX timeseries schema
  const auaGranularity: 'quarterly' | 'monthly' | 'annually' =
    granularity === 'annually' ? 'annually'
    : granularity === 'monthly' ? 'monthly'
    : 'quarterly'

  // Shared/cached timeseries query to avoid duplicate network fetches across tabs/components
  const { data: timeseriesData, isLoading: timeseriesLoading } = useQuery<CumulativeChartResponse>({
    queryKey: ['advisor-intelligence', 'cumulative-chart', firmOverride],
    queryFn: () => getCumulativeChart(firmOverride),
    staleTime: 5 * 60 * 1000,
    refetchOnWindowFocus: false,
    refetchOnMount: false,
  })

  // Helper to get period key and label from a date
  const getPeriodInfo = useCallback((date: Date): { periodKey: string; periodLabel: string } => {
    if (granularity === 'monthly') {
      const month = date.toLocaleString('en-US', { month: 'short' })
      const year = date.getFullYear()
      return {
        periodKey: `${year}-${String(date.getMonth() + 1).padStart(2, '0')}`,
        periodLabel: `${month} '${year.toString().slice(-2)}`
      }
    } else if (granularity === 'quarterly') {
      const quarter = Math.floor(date.getMonth() / 3) + 1
      const year = date.getFullYear()
      return {
        periodKey: `${year}-Q${quarter}`,
        periodLabel: `Q${quarter} '${year.toString().slice(-2)}`
      }
    } else {
      // annually
      const year = date.getFullYear()
      return {
        periodKey: `${year}`,
        periodLabel: `${year}`
      }
    }
  }, [granularity])

  // Time window cutoff date
  const timeWindowCutoff = useMemo(() => {
    if (timeWindow === 'Max') return null
    const now = new Date()
    const years = timeWindow === '1Y' ? 1 : 3
    return new Date(now.getFullYear() - years, now.getMonth(), now.getDate())
  }, [timeWindow])

  // Full-history AUA period list (unfiltered) — pre-aggregated by publisher (PSCFIX schema).
  // Selected directly from the correct granularity sub-key; no client-side aggregation needed.
  const allSortedAuaPeriods: AuaDataPoint[] = useMemo(() => {
    return timeseriesData?.aua?.[auaGranularity]?.data ?? []
  }, [timeseriesData, auaGranularity])

  // Windowed AUA periods for display — filtered by time window using end_date
  const aggregatedAuaData: AuaDataPoint[] = useMemo(() => {
    if (allSortedAuaPeriods.length === 0) return []
    if (!timeWindowCutoff) return allSortedAuaPeriods
    return allSortedAuaPeriods.filter(point =>
      new Date(point.end_date + 'T12:00:00') >= timeWindowCutoff
    )
  }, [allSortedAuaPeriods, timeWindowCutoff])

  // Whether the nna view has separate gross inflow/outflow columns.
  // True only after the publisher has been updated to output cum_inflows/cum_outflows.
  // When false, only net NNA is available — the chart shows a single net bar, not diverging.
  const hasGrossFlowData = useMemo(() => {
    const cats = timeseriesData?.nna?.categories || []
    return cats.includes('Inflows') && cats.includes('Outflows')
  }, [timeseriesData])

  // Aggregate daily NNA data to monthly/quarterly/annually.
  //
  // ALL columns (NNA, Inflows, Outflows) are CUMULATIVE from inception.
  // Period flows are derived by differencing adjacent period endpoints:
  //   period_net      = last(NNA)      - prev_last(NNA)
  //   period_inflows  = last(Inflows)  - prev_last(Inflows)   [always >= 0]
  //   period_outflows = last(Outflows) - prev_last(Outflows)  [always >= 0, stored negative]
  //
  // When hasGrossFlowData is false, only net is available — inflow/outflow left at 0
  // so the chart does not fabricate a split that doesn't exist in the data.
  const aggregatedNnaData = useMemo(() => {
    if (!timeseriesData?.nna?.data) return []

    const allData = timeseriesData.nna.data
    const dailyData = timeWindowCutoff
      ? allData.filter(p => new Date(String(p.date) + 'T12:00:00') >= timeWindowCutoff)
      : allData
    const categories = timeseriesData.nna.categories || []
    if (dailyData.length === 0 || categories.length === 0) return []

    const grossFlows = categories.includes('Inflows') && categories.includes('Outflows')

    // Collect the last data point per period (cumulative snapshot at period end)
    // Use ALL data (unfiltered) so the first windowed period can diff against its true prior
    const fullPeriodMap = new Map<string, {
      period: string; label: string; endDate: string;
      lastNNA: number; lastInflows: number; lastOutflows: number;
    }>()

    allData.forEach((point) => {
      const date = new Date(point.date + 'T12:00:00')
      const { periodKey, periodLabel } = getPeriodInfo(date)

      fullPeriodMap.set(periodKey, {
        period: periodKey,
        label: periodLabel,
        endDate: point.date,
        lastNNA:      Number(point['NNA'])      || 0,
        lastInflows:  Number(point['Inflows'])  || 0,
        lastOutflows: Number(point['Outflows']) || 0,
      })
    })

    // Build the windowed period map for display
    const windowedPeriodKeys = new Set<string>()
    dailyData.forEach((point) => {
      const date = new Date(point.date + 'T12:00:00')
      const { periodKey } = getPeriodInfo(date)
      windowedPeriodKeys.add(periodKey)
    })

    const allSorted = Array.from(fullPeriodMap.values()).sort((a, b) =>
      String(a.period).localeCompare(String(b.period))
    )

    // Only show periods within the window, but use full history for differencing
    const sorted = allSorted.filter(e => windowedPeriodKeys.has(e.period))

    // Difference adjacent periods to get period-level flows
    return sorted.map((entry) => {
      // Find the prior period from the full (unfiltered) sorted list
      const fullIdx = allSorted.findIndex(e => e.period === entry.period)
      const prev = fullIdx > 0 ? allSorted[fullIdx - 1] : null
      const prevNNA      = prev ? prev.lastNNA      : 0
      const prevInflows  = prev ? prev.lastInflows  : 0
      const prevOutflows = prev ? prev.lastOutflows : 0

      const periodNet      = entry.lastNNA      - prevNNA
      const periodInflows  = entry.lastInflows  - prevInflows
      const periodOutflows = entry.lastOutflows - prevOutflows

      const inflow = grossFlows ? periodInflows : 0
      const outflow = grossFlows ? -periodOutflows : 0
      return {
        period:   entry.period,
        label:    entry.label,
        endDate:  entry.endDate,
        // Gross mode: both bars present every period (inflows above 0, outflows below 0)
        // Net-only mode: leave 0 — the chart renders as a single net bar instead
        inflow,
        outflow,
        net:     periodNet,
      }
    })
  }, [timeseriesData, getPeriodInfo, timeWindowCutoff])

  // Y3-FE: Aggregate aua_mix data (asset class breakdown) by period
  const aggregatedMixData = useMemo(() => {
    const mixView = timeseriesData?.aua_mix
    if (!mixView?.data || mixView.data.length === 0) return []

    const categories = mixView.categories || []
    const mixData = timeWindowCutoff
      ? mixView.data.filter(p => new Date(p.period + '-01T12:00:00') >= timeWindowCutoff)
      : mixView.data

    if (mixData.length === 0) return []

    // aua_mix data is monthly. Aggregate to quarter/year when needed.
    const periodMap = new Map<string, { period: string; label: string; [k: string]: number | string }>()

    mixData.forEach((point) => {
      const date = new Date(point.period + '-01T12:00:00')
      const { periodKey, periodLabel } = getPeriodInfo(date)

      // For cumulative AUA mix, take end-of-period snapshot (last month in the period)
      const entry: { period: string; label: string; [k: string]: number | string } = { period: periodKey, label: periodLabel }
      point.segments.forEach(seg => {
        entry[seg.label] = seg.value
      })
      periodMap.set(periodKey, entry)
    })

    return Array.from(periodMap.values()).sort((a, b) =>
      String(a.period).localeCompare(String(b.period))
    )
  }, [timeseriesData, getPeriodInfo, timeWindowCutoff])

  // Y3-FE: Categories for the Mix stacked bar
  const mixCategories = useMemo(() => {
    return timeseriesData?.aua_mix?.categories || []
  }, [timeseriesData])

  // Y5-FE: Aggregate growth_decomposition data by period
  //
  // IMPORTANT: aggregate ALL months first, then filter which periods to display.
  // Filtering monthly points before aggregation produces partial-year bars on
  // 3Y/1Y windows (e.g. 3Y starting mid-March 2023 would show Apr-Dec 2023
  // only, understating that year by Jan-Mar).  The NNA view diffs full-history
  // year endpoints so the same partial-year bar would mismatch by ~$125M.
  // Mirror the NNA view: compute full-period sums from complete history, then
  // filter which period labels fall within the time window.
  const aggregatedGroData = useMemo(() => {
    const groView = timeseriesData?.growth_decomposition
    if (!groView?.data || groView.data.length === 0) return []

    // GRO data is monthly. For quarterly/annually, SUM values (not snapshot).
    // Use complete monthly history regardless of time window.
    const periodMap = new Map<string, { period: string; label: string; market: number; nna: number; total: number; endDate: string }>()

    groView.data.forEach((point: GrowthDecompositionPoint) => {
      const date = new Date(point.period + '-01T12:00:00')
      const { periodKey, periodLabel } = getPeriodInfo(date)

      // Derive end date from source month: last day of point.period (YYYY-MM)
      const [srcY, srcM] = point.period.split('-').map(Number)
      const lastDayOfMonth = new Date(srcY, srcM, 0).getDate()
      const srcEndDate = `${point.period}-${String(lastDayOfMonth).padStart(2, '0')}`

      const existing = periodMap.get(periodKey) || { period: periodKey, label: periodLabel, market: 0, nna: 0, total: 0, endDate: srcEndDate }
      existing.market += point.market
      existing.nna += point.nna
      existing.total += point.total
      existing.endDate = srcEndDate // always take the latest contributing month
      periodMap.set(periodKey, existing)
    })

    // Filter which periods to display: only show periods whose end date falls
    // within the selected time window. This hides old years without truncating
    // the period sums of years that are partially within the window.
    const allPeriods = Array.from(periodMap.values()).sort((a, b) =>
      String(a.period).localeCompare(String(b.period))
    )
    if (!timeWindowCutoff) return allPeriods
    return allPeriods.filter(p => new Date(p.endDate + 'T12:00:00') >= timeWindowCutoff)
  }, [timeseriesData, getPeriodInfo, timeWindowCutoff])

  // ============================================================================
  // F2: Projection computation for the current incomplete period
  // ============================================================================

  const currentPeriodKey = useMemo(() => {
    return getPeriodInfo(new Date()).periodKey
  }, [getPeriodInfo])

  // Compute total and elapsed days for a given period.
  // dataEndDate is the last date with actual data (YYYY-MM-DD) — elapsed is measured
  // from the period start to this date, NOT from today's wall clock.
  function computePeriodDays(g: GranularityOption, periodKey: string, dataEndDate: string): { totalDays: number; elapsedDays: number } {
    const dataDate = new Date(dataEndDate + 'T12:00:00')
    if (g === 'monthly') {
      const [y, m] = periodKey.split('-').map(Number)
      const start = new Date(y, m - 1, 1)
      const end = new Date(y, m, 0)
      return {
        totalDays: end.getDate(),
        elapsedDays: Math.max(1, Math.floor((dataDate.getTime() - start.getTime()) / 86400000) + 1),
      }
    } else if (g === 'quarterly') {
      const parts = periodKey.split('-Q')
      const y = Number(parts[0])
      const q = Number(parts[1])
      const startMonth = (q - 1) * 3
      const start = new Date(y, startMonth, 1)
      const end = new Date(y, startMonth + 3, 0)
      return {
        totalDays: Math.floor((end.getTime() - start.getTime()) / 86400000) + 1,
        elapsedDays: Math.max(1, Math.floor((dataDate.getTime() - start.getTime()) / 86400000) + 1),
      }
    } else {
      const y = Number(periodKey)
      const start = new Date(y, 0, 1)
      const end = new Date(y, 11, 31)
      return {
        totalDays: Math.floor((end.getTime() - start.getTime()) / 86400000) + 1,
        elapsedDays: Math.max(1, Math.floor((dataDate.getTime() - start.getTime()) / 86400000) + 1),
      }
    }
  }

  // AUA: project end-of-period value using a two-input weighted blend.
  // 66.67% weight on the current trajectory, 33.33% on the last complete
  // period's delta. The current trajectory's weight on the TIME-SCALED delta
  // vs the RAW observed delta slides with how much of the period has elapsed
  // (elapsedFraction). Early in a period the raw observation dominates (avoids
  // amplifying a few days of noise by 4-5x); late in a period the time-scaled
  // delta dominates (the extrapolation ratio is small and trustworthy).
  const augmentedAuaData = useMemo(() => {
    if (aggregatedAuaData.length === 0) return aggregatedAuaData
    const cats = timeseriesData?.aua?.[auaGranularity]?.categories || []
    const lastIdx = aggregatedAuaData.length - 1
    return aggregatedAuaData.map((entry, idx) => {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const aug = { ...entry } as any

      // Only project the last bar (most recent period with data)
      if (idx !== lastIdx) return aug

      const { totalDays, elapsedDays } = computePeriodDays(granularity, entry.period, String(entry.end_date))
      if (elapsedDays >= totalDays) return aug

      const fullIdx = allSortedAuaPeriods.findIndex(e => e.period === entry.period)
      const prior = fullIdx > 0 ? allSortedAuaPeriods[fullIdx - 1] : null
      const priorPrior = fullIdx > 1 ? allSortedAuaPeriods[fullIdx - 2] : null

      if (!prior) {
        aug._projectionUnavailable = true
        return aug
      }

      const ratio = totalDays / elapsedDays
      const elapsedFraction = elapsedDays / totalDays  // 0..1 how far into the period

      let projectedTotal = 0
      let actualTotal = 0

      cats.forEach(cat => {
        const actual = Number(entry[cat]) || 0
        actualTotal += actual
        const priorEnd = Number((prior as Record<string, unknown>)[cat]) || 0
        const rawDelta = actual - priorEnd

        // Current period contribution: blend between raw observed delta (safe
        // early in period) and time-scaled delta (accurate late in period).
        // At elapsedFraction=0.2 (early month/year): 80% raw + 20% scaled
        // At elapsedFraction=0.7 (late quarter):      30% raw + 70% scaled
        const scaledDelta = rawDelta * ratio
        const currentDelta = rawDelta * (1 - elapsedFraction) + scaledDelta * elapsedFraction

        // Last complete period's delta (prior vs priorPrior)
        const priorPriorEnd = priorPrior ? (Number((priorPrior as Record<string, unknown>)[cat]) || 0) : priorEnd
        const historicalDelta = priorEnd - priorPriorEnd

        // Blend: 2/3 current trajectory, 1/3 last complete period
        const weightedDelta = priorPrior
          ? currentDelta * (2 / 3) + historicalDelta * (1 / 3)
          : currentDelta  // only one prior exists — use current signal alone

        const projectedValue = priorEnd + weightedDelta
        aug[`_projected_${cat}`] = projectedValue
        projectedTotal += projectedValue
      })

      aug._projectedTotal = projectedTotal
      aug._actualTotal = actualTotal

      return aug
    })
  }, [aggregatedAuaData, allSortedAuaPeriods, granularity, auaGranularity, timeseriesData])

  // NNA: compute projected values for the most recent incomplete period
  const augmentedNnaData = useMemo(() => {
    if (aggregatedNnaData.length === 0) return aggregatedNnaData
    const lastNnaIdx = aggregatedNnaData.length - 1
    return aggregatedNnaData.map((entry, idx) => {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const aug = { ...entry } as any

      if (idx !== lastNnaIdx) return aug

      const { totalDays, elapsedDays } = computePeriodDays(granularity, entry.period, entry.endDate)
      if (elapsedDays >= totalDays) return aug

      const prior = idx > 0 ? aggregatedNnaData[idx - 1] : null
      const ratio = totalDays / elapsedDays

      // Inflows (positive)
      const projInflow = entry.inflow * ratio
      const priorInflow = prior ? prior.inflow : entry.inflow
      const capInflow = Math.abs(priorInflow) * 1.5
      aug._projectedInflow = Math.min(projInflow, capInflow)

      // Outflows (negative)
      const projOutflow = entry.outflow * ratio
      const priorOutflow = prior ? prior.outflow : entry.outflow
      const capOutflow = -Math.abs(priorOutflow) * 1.5
      aug._projectedOutflow = Math.max(projOutflow, capOutflow)

      // Net
      aug._projectedNet = aug._projectedInflow + aug._projectedOutflow

      return aug
    })
  }, [aggregatedNnaData, granularity])

  // GRO: add dashed Total-only projection point for the most recent incomplete period
  const augmentedGroData = useMemo(() => {
    if (aggregatedGroData.length === 0) return aggregatedGroData
    const lastIdx = aggregatedGroData.length - 1
    const last = aggregatedGroData[lastIdx]

    const { totalDays, elapsedDays } = computePeriodDays(granularity, last.period, last.endDate)
    if (elapsedDays >= totalDays) return aggregatedGroData.map(d => ({ ...d, total_proj: null as number | null }))

    const prior = lastIdx > 0 ? aggregatedGroData[lastIdx - 1] : null
    const ratio = totalDays / elapsedDays

    // Total-only projection (per thread decision — no market/nna projections)
    const projectedTotal = (() => {
      const projected = last.total * ratio
      const cap = Math.abs(prior?.total ?? last.total) * 1.5
      if (last.total >= 0) return Math.min(projected, cap)
      return Math.max(projected, -cap)
    })()

    const projectedPoint = {
      period: last.period + '_proj',
      label: last.label,
      endDate: last.endDate,
      market: 0,
      nna: 0,
      total: projectedTotal,
      total_proj: projectedTotal,
      _isProjection: true,
    }

    // Mark the last actual point to connect the dashed line
    const markedLast = { ...last, total_proj: last.total }
    const markedProj = projectedPoint

    return [
      ...aggregatedGroData.slice(0, lastIdx).map(d => ({ ...d, total_proj: null as number | null })),
      markedLast,
      markedProj,
    ]
  }, [aggregatedGroData, granularity])

  // Get the appropriate aggregated data based on panel view mode
  const aggregatedBarData = panelViewMode === 'aua' ? augmentedAuaData : augmentedNnaData

  // Get the selected bar's data
  const selectedBarData = useMemo(() => {
    if (!selectedBarPeriod) return null
    return aggregatedBarData.find(d => d.period === selectedBarPeriod) || null
  }, [selectedBarPeriod, aggregatedBarData])

  // Handle bar click - toggle selection
  const handleBarClick = (data: { period: string }) => {
    setSelectedBarPeriod(prev => prev === data.period ? null : data.period)
  }

  // Get categories for the AUA bar chart
  const barCategories = timeseriesData?.aua?.[auaGranularity]?.categories || []

  // Handle period change (time machine)
  // Get base view data (always use the base view mode, not drill-down mode)
  // Drill-down data is nested inside segments (geo.cities, adv.clients, nna.flows)
  // All 4 views (aua, nna, geo, adv) are now separate top-level views
  const getDataViewKey = (): 'aua' | 'nna' | 'geo' | 'adv' => {
    if (viewMode === 'city') return 'geo'
    if (viewMode === 'client') return 'adv'
    return viewMode as 'aua' | 'nna' | 'geo' | 'adv'
  }
  const dataViewKey = getDataViewKey()
  const rawView = data?.views?.[dataViewKey]

  // All views now use the standard structure: view.current.donut
  const getSnapshotForPeriod = (): PeriodSnapshot | null => {
    if (!rawView) return null

    // Standard structure for all views
    const view = rawView as PartnerAnalyticsViewWithPeriods | PartnerAnalyticsView
    if (hasTimeMachine(view)) {
      const viewWithPeriods = view as PartnerAnalyticsViewWithPeriods
      if (selectedPeriod === 'current') {
        return viewWithPeriods.current
      }
      return viewWithPeriods[selectedPeriod] || viewWithPeriods.current
    }

    // v4 format - treat the whole view as the snapshot
    return view as unknown as PeriodSnapshot
  }

  const currentSnapshot = getSnapshotForPeriod()

  // Check if the BASE view has valid data (not drill-down data)
  // This determines if we should show the panel at all
  // When drilled down, we only need base data to exist - drill data can be empty
  const hasValidBaseData = currentSnapshot && currentSnapshot.donut?.segments?.length > 0 && currentSnapshot.metrics
  const hasValidData = hasValidBaseData

  // Extract data if available
  const donut = currentSnapshot?.donut
  const distribution = currentSnapshot?.distribution
  const baseSegments: DonutSegment[] = donut?.segments || []

  // Get segments for current drill level
  // - At base level: return base segments
  // - When drilled: return nested flows/cities/clients from selected parent segment
  const getSegmentsForDrillLevel = (): DonutSegment[] => {
    // NNA drill-down: show nested flows (inflows/outflows) from selected segment
    if (viewMode === 'nna' && nnaDrillLevel === 'flow' && selectedNnaSegmentKey) {
      const parentSeg = baseSegments.find(s => s.key === selectedNnaSegmentKey)
      if (parentSeg?.flows && parentSeg.flows.length > 0) {
        // Convert NnaFlowSegment[] to DonutSegment[] for consistent rendering
        // Use absolute value for donut (negative outflows would break the chart)
        return parentSeg.flows.map(flow => ({
          key: flow.key,
          label: flow.label,
          aua: Math.abs(flow.value),  // Use absolute value for donut size
          aua_pct: 0,  // Will be calculated relative to parent
          value: flow.value,  // Keep original signed value
          value_pct: 0,
          client_count: 0,  // Flows don't have client count
          color: flow.color,
        }))
      }
      // No nested flows - return empty (will show "no data" message)
      return []
    }

    // GEO drill-down: show nested cities from selected state
    if (viewMode === 'geo' && geoDrillLevel === 'city' && selectedStateKey) {
      const parentSeg = baseSegments.find(s => s.key === selectedStateKey)
      if (parentSeg?.cities && parentSeg.cities.length > 0) {
        // Convert CitySegment[] to DonutSegment[] for consistent rendering
        return parentSeg.cities.map(city => ({
          key: city.key,
          label: city.label,
          aua: city.aua,
          aua_pct: city.aua_pct,
          client_count: city.client_count,
          color: city.color,
          distribution: city.distribution,  // Include city's distribution if available
        }))
      }
      // No nested cities - return empty (will show "no data" message)
      return []
    }

    // ADV drill-down: show nested clients from selected architect
    if (viewMode === 'adv' && advDrillLevel === 'client' && selectedArchitectKey) {
      const parentSegment = baseSegments.find(s => s.key === selectedArchitectKey)
      if (parentSegment?.clients && parentSegment.clients.length > 0) {
        // Convert ClientSegment[] to DonutSegment[] for consistent rendering
        return parentSegment.clients.map(client => ({
          key: client.key,
          label: client.label,
          aua: client.aua,
          aua_pct: client.aua_pct,
          client_count: client.account_count, // Use account_count as proxy
          color: '', // Let frontend palette (CLIENT_COLORS) assign vivid distinct colors
          distribution: client.distribution,  // Include client's distribution if available
        }))
      }
      // No nested clients - return empty (will show "no data" message)
      return []
    }

    // Base level: return base segments
    return baseSegments
  }

  const segments = getSegmentsForDrillLevel()

  // Get parent segment when drilled (for showing parent's value in donut center)
  const getParentSegment = (): DonutSegment | null => {
    if (viewMode === 'nna' && nnaDrillLevel === 'flow' && selectedNnaSegmentKey) {
      return baseSegments.find(s => s.key === selectedNnaSegmentKey) || null
    }
    if (viewMode === 'geo' && geoDrillLevel === 'city' && selectedStateKey) {
      return baseSegments.find(s => s.key === selectedStateKey) || null
    }
    if (viewMode === 'adv' && advDrillLevel === 'client' && selectedArchitectKey) {
      return baseSegments.find(s => s.key === selectedArchitectKey) || null
    }
    return null
  }
  const parentSegment = getParentSegment()

  // Check if we're in NNA view (use value instead of aua)
  const _isNnaView = viewMode === 'nna'

  // Get selected segment key based on current view/drill state
  const getSelectedSegmentKey = (): string | null => {
    // AUA mode: segment selection for distribution filter (no drill-down)
    if (viewMode === 'aua') {
      return selectedNnaSegmentKey
    }
    if (viewMode === 'nna') {
      if (nnaDrillLevel === 'flow') return selectedNnaFlowKey
      return selectedNnaSegmentKey
    }
    if (viewMode === 'geo' && geoDrillLevel === 'city') return selectedCityKey
    if (viewMode === 'adv' && advDrillLevel === 'client') return selectedClientKey
    // At top level of GEO/ADV, no segment selection (drill-through only)
    return null
  }
  const selectedSegmentKey = getSelectedSegmentKey()

  // Look up selected segment by key (persists across period changes)
  const selectedSegment = selectedSegmentKey ? segments.find(s => s.key === selectedSegmentKey) || null : null

  // Get distribution data based on drill-down level and selection
  // Priority: selected segment > parent segment > view total
  // Note: distribution data is stored in two places:
  //   1. View-level: distribution.by_segment["state_key"]
  //   2. Segment-level: segment.distribution (for nested cities/clients)
  const getDistributionData = (): DistributionStats | null => {
    if (!distribution) return null

    // Special case: NNA drilled into flows - always use parent segment's distribution
    // Flows (inflows/outflows) don't have their own distribution data
    if (viewMode === 'nna' && nnaDrillLevel === 'flow' && selectedNnaSegmentKey) {
      return distribution.by_segment?.[selectedNnaSegmentKey] || distribution.total
    }

    // Case 1: A segment is clicked/selected
    if (selectedSegment) {
      // First check if segment has its own distribution (nested city/client)
      if (selectedSegment.distribution) {
        return selectedSegment.distribution
      }
      // Otherwise look up in view-level by_segment
      return distribution.by_segment?.[selectedSegment.key] || distribution.total
    }

    // Case 2: Drilled down but no specific selection (showing parent context)
    if (parentSegment) {
      // First check if parent segment has its own distribution
      if (parentSegment.distribution) {
        return parentSegment.distribution
      }
      // Otherwise look up parent in view-level by_segment
      return distribution.by_segment?.[parentSegment.key] || distribution.total
    }

    // Case 3: Base level, no selection - show total
    return distribution.total
  }

  const distributionData = getDistributionData()

  // Compute global max for Y-axis consistency across ALL time periods
  // This ensures distributions are comparable when using time machine
  // IMPORTANT: Only compare within the SAME aggregation context (e.g., FL across quarters,
  // not FL vs GEO total). When drill level changes, scale resets appropriately.
  const globalMaxCount = (() => {
    if (!rawView) return undefined

    const view = rawView as PartnerAnalyticsViewWithPeriods
    const periods: (keyof PartnerAnalyticsViewWithPeriods)[] = ['current', 'q1', 'q2', 'q3']
    const maxCounts: number[] = []

    // Determine current distribution context (must match getDistributionData logic)
    // Context types: total, segment (by key), nested city, nested client
    type DistContext =
      | { type: 'total' }
      | { type: 'segment'; key: string }
      | { type: 'nested_city'; stateKey: string; cityKey: string }
      | { type: 'nested_client'; architectKey: string; clientKey: string }

    const getDistributionContext = (): DistContext => {
      // City selected within drilled state
      if (selectedCityKey && selectedStateKey && geoDrillLevel === 'city') {
        return { type: 'nested_city', stateKey: selectedStateKey, cityKey: selectedCityKey }
      }
      // Client selected within drilled architect
      if (selectedClientKey && selectedArchitectKey && advDrillLevel === 'client') {
        return { type: 'nested_client', architectKey: selectedArchitectKey, clientKey: selectedClientKey }
      }
      // Drilled into state (showing state's distribution)
      if (selectedStateKey && geoDrillLevel === 'city') {
        return { type: 'segment', key: selectedStateKey }
      }
      // Drilled into architect (showing architect's distribution)
      if (selectedArchitectKey && advDrillLevel === 'client') {
        return { type: 'segment', key: selectedArchitectKey }
      }
      // NNA/AUA segment selected
      if (selectedNnaSegmentKey && (viewMode === 'aua' || viewMode === 'nna')) {
        return { type: 'segment', key: selectedNnaSegmentKey }
      }
      // Base level, no selection
      return { type: 'total' }
    }

    const context = getDistributionContext()

    // Look up distribution counts for this context across all periods
    for (const period of periods) {
      const snapshot = view[period] as PeriodSnapshot | undefined
      if (!snapshot) continue

      let counts: number[] | undefined

      switch (context.type) {
        case 'total':
          counts = snapshot.distribution?.total?.histogram?.counts
          break
        case 'segment':
          counts = snapshot.distribution?.by_segment?.[context.key]?.histogram?.counts
          break
        case 'nested_city': {
          const stateSegment = snapshot.donut?.segments?.find((s: DonutSegment) => s.key === context.stateKey)
          const city = stateSegment?.cities?.find((c: CitySegment) => c.key === context.cityKey)
          counts = city?.distribution?.histogram?.counts
          break
        }
        case 'nested_client': {
          const archSegment = snapshot.donut?.segments?.find((s: DonutSegment) => s.key === context.architectKey)
          const client = archSegment?.clients?.find((c: ClientSegment) => c.key === context.clientKey)
          counts = client?.distribution?.histogram?.counts
          break
        }
      }

      if (counts && counts.length > 0) {
        maxCounts.push(Math.max(...counts))
      }
    }

    return maxCounts.length > 0 ? Math.max(...maxCounts) : undefined
  })()

  // Header actions: AUA/NNA toggle + Partner dropdown
  const headerActions = (
    <div className="flex items-center gap-4">
      {/* AUA / NNA / GRO Toggle */}
      <div className="flex items-center gap-2">
        <span className="text-xs text-white/50 tracking-wider">Mode:</span>
        <div className="flex gap-1 bg-white/5 rounded-lg p-1">
          {([['aua', 'AUA'], ['nna', 'NNA'], ['gro', 'GRO']] as [PanelViewMode, string][]).map(([mode, label]) => (
            <button
              key={mode}
              onClick={() => { setPanelViewMode(mode); setSelectedBarPeriod(null); }}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                panelViewMode === mode
                  ? 'bg-[hsl(var(--primary))] text-white shadow-sm shadow-[hsl(var(--primary))]/30'
                  : 'bg-white/5 text-white/60 hover:bg-white/10 hover:text-white/80'
              }`}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* Interval Toggle */}
      <div className="flex items-center gap-2">
        <span className="text-xs text-white/50 tracking-wider">Interval:</span>
        <div className="flex gap-1 bg-white/5 rounded-lg p-1">
          {([['monthly', 'Month'], ['quarterly', 'Quarter'], ['annually', 'Year']] as [GranularityOption, string][]).map(([opt, label]) => (
            <button
              key={opt}
              onClick={() => { onGranularityChange(opt); setSelectedBarPeriod(null); }}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                granularity === opt
                  ? 'bg-[hsl(var(--primary))] text-white shadow-sm shadow-[hsl(var(--primary))]/30'
                  : 'bg-white/5 text-white/60 hover:bg-white/10 hover:text-white/80'
              }`}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* Time Window Toggle */}
      <div className="flex items-center gap-2">
        <span className="text-xs text-white/50 tracking-wider">Window:</span>
        <div className="flex gap-1 bg-white/5 rounded-lg p-1">
          {(['1Y', '3Y', 'Max'] as TimeWindow[]).map((opt) => (
            <button
              key={opt}
              onClick={() => { setTimeWindow(opt); setSelectedBarPeriod(null); }}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                timeWindow === opt
                  ? 'bg-[hsl(var(--primary))] text-white shadow-sm shadow-[hsl(var(--primary))]/30'
                  : 'bg-white/5 text-white/60 hover:bg-white/10 hover:text-white/80'
              }`}
            >
              {opt}
            </button>
          ))}
        </div>
      </div>

      {/* Firm Picker — Opal internal users only */}
      {internal && (
        <div className="flex items-center gap-2">
          <span className="text-xs text-white/50 tracking-wider">Firm:</span>
          <select
            value={selectedFirmId}
            onChange={e => onPartnerChange(e.target.value)}
            className="px-3 py-1.5 rounded-lg bg-[#1e1e2d] border border-white/20 text-white text-xs font-medium focus:outline-none focus:ring-2 focus:ring-[hsl(var(--primary))] cursor-pointer"
          >
            {AVAILABLE_FIRMS.map(f => (
              <option key={f.id} value={f.id} className="bg-[#1e1e2d] text-white">{f.name}</option>
            ))}
          </select>
        </div>
      )}
    </div>
  )

  // Loading state — gate on timeseries fetch, not header_metrics.json
  // The Assets Overview panel renders bar charts from timeseries_chart.json only.
  // header_metrics.json (data prop) is consumed by the Distribution tab, not here.
  if (timeseriesLoading) {
    return (
      <Panel variant="mixed">
        <PanelHeader
          title="Assets Overview"
          helpText="Total market value of all client accounts managed through the platform, broken down by new vs existing clients. Toggle to NNA to see net new asset flows."
          actions={headerActions}
        />
        <PanelContent className="pt-6">
          <LoadingInline className="py-16" />
        </PanelContent>
      </Panel>
    )
  }

  // No timeseries data available
  if (aggregatedAuaData.length === 0 && aggregatedNnaData.length === 0) {
    return (
      <Panel variant="mixed">
        <PanelHeader
          title="Assets Overview"
          helpText="Total market value of all client accounts managed through the platform, broken down by new vs existing clients. Toggle to NNA to see net new asset flows."
          actions={headerActions}
        />
        <PanelContent className="pt-6">
          <div className="flex items-center justify-center py-16">
            <p className="text-white/60">No timeseries data available</p>
          </div>
        </PanelContent>
        <PanelFooter content="Source: SS&C Black Diamond Wealth Solutions." timestamp={data?.generated_at} />
      </Panel>
    )
  }

  return (
    <Panel variant="mixed">
      <PanelHeader
        title="Assets Overview"
        helpText={panelViewMode === 'aua' ? "Total market value of all client accounts managed through the platform, broken down by new vs existing clients. New clients are those onboarded within the trailing 12 months." : panelViewMode === 'nna' ? "Net new assets measure organic growth — money flowing in from new and existing clients minus money flowing out. Positive NNA means the business is gathering assets beyond market movement." : "Monthly AUA change decomposed into market appreciation and net new assets. Shows whether growth is driven by market performance or organic inflows."}
        actions={headerActions}
      />
      <PanelContent className="pt-4">
        <div className="flex">
          {/* MAIN CHART AREA */}
          <div className="flex flex-col p-6 relative w-full">
            {/* Section Title + Y3-FE AUA Sub-Toggle */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <h4 className="text-xs font-medium text-white/60 uppercase tracking-wider">
                  {panelViewMode === 'aua' ? 'Assets Under Advisory' : panelViewMode === 'nna' ? 'Net New Assets' : 'Growth Decomposition'}
                </h4>
                <Tooltip
                  content={panelViewMode === 'gro' ? "Monthly AUA change decomposed into market appreciation and net new assets." : "Click a bar to filter the breakdown table to that client type."}
                  side="auto"
                >
                  <HelpCircle size={14} className="text-white/40 hover:text-white/70 transition-colors cursor-help flex-shrink-0" />
                </Tooltip>
              </div>
              {/* Y3-FE: AUA sub-toggle (Clients / Mix) — inside panel content, not header */}
              {panelViewMode === 'aua' && (
                <div className="flex gap-0.5 bg-white/10 rounded-lg p-0.5">
                  {([['clients', AUA_SUB_MODE_CLIENTS_LABEL], ['mix', 'Mix']] as [AuaSubMode, string][]).map(([mode, label]) => (
                    <button
                      key={mode}
                      onClick={() => setAuaSubMode(mode)}
                      className={`px-2.5 py-1 text-xs font-medium rounded-md transition-colors ${
                        auaSubMode === mode ? 'bg-white/20 text-white' : 'text-white/50 hover:text-white hover:bg-white/10'
                      }`}
                    >
                      {label}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Chart Area */}
            <div className="flex-1 min-h-[400px]">
              {timeseriesLoading ? (
                <div className="h-full flex items-center justify-center">
                  <LoadingInline size="sm" />
                </div>
              ) : panelViewMode === 'aua' && auaSubMode === 'clients' && aggregatedAuaData.length > 0 && barCategories.length > 0 ? (
                /* AUA Clients Stacked Bar Chart */
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={aggregatedBarData}
                    margin={{ top: 20, right: 30, left: 10, bottom: 5 }}
                    onClick={(data) => {
                      // eslint-disable-next-line @typescript-eslint/no-explicit-any
                      const chartData = data as any
                      if (chartData?.activePayload?.[0]?.payload?.period) {
                        handleBarClick({ period: chartData.activePayload[0].payload.period })
                      }
                    }}
                    style={{ cursor: 'pointer' }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" vertical={false} />
                    <XAxis
                      dataKey="label"
                      stroke="rgba(255,255,255,0.2)"
                      tick={({ x, y, payload }) => {
                        const isSelected = aggregatedBarData.find(d => d.label === payload.value)?.period === selectedBarPeriod
                        return (
                          <text
                            x={x}
                            y={Number(y) + 12}
                            textAnchor="middle"
                            fontSize={11}
                            fill={isSelected ? 'hsl(var(--primary))' : 'rgba(255,255,255,0.6)'}
                            fontWeight={isSelected ? 600 : 400}
                          >
                            {payload.value}
                          </text>
                        )
                      }}
                      axisLine={false}
                      tickLine={false}
                    />
                    <YAxis
                      stroke="rgba(255,255,255,0.2)"
                      tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.6)' }}
                      tickFormatter={(value) => {
                        if (value >= 1e9) return `$${(value / 1e9).toFixed(1)}B`
                        if (value >= 1e6) return `$${(value / 1e6).toFixed(0)}M`
                        return `$${value}`
                      }}
                      width={55}
                      axisLine={false}
                      tickLine={false}
                      domain={[0, (dataMax: number) => {
                        const last = panelViewMode === 'aua' ? augmentedAuaData[augmentedAuaData.length - 1] : null
                        const proj = last?._projectedTotal as number | undefined
                        return Math.max(dataMax, proj ?? 0) * 1.05
                      }]}
                    />
                    <RechartsTooltip
                      wrapperStyle={{ zIndex: 40 }}
                      cursor={{ fill: 'rgba(255,255,255,0.08)' }}
                      content={({ active, payload, label }) => {
                        if (!active || !payload || payload.length === 0) return null

                        const total = payload.reduce((sum, entry) => sum + (Number(entry.value) || 0), 0)
                        const sortedPayload = [...payload].sort((a, b) => (Number(b.value) || 0) - (Number(a.value) || 0))
                        const periodData = payload[0]?.payload
                        const isSelected = periodData?.period === selectedBarPeriod
                        const isCurrentPeriod = periodData?.period === aggregatedAuaData[aggregatedAuaData.length - 1]?.period

                        // Period-over-period growth
                        const currentIdx = aggregatedAuaData.findIndex(d => d.period === periodData?.period)
                        const priorPeriod = currentIdx > 0 ? aggregatedAuaData[currentIdx - 1] : null
                        const priorTotal = priorPeriod
                          ? barCategories.reduce((sum, cat) => sum + (Number((priorPeriod as Record<string, unknown>)[cat]) || 0), 0)
                          : null
                        const growth = priorTotal !== null && priorTotal > 0 ? total - priorTotal : null
                        const growthPct = priorTotal !== null && priorTotal > 0 ? ((total / priorTotal) - 1) * 100 : null
                        const growthLabel = granularity === 'monthly' ? 'MoM Growth' : granularity === 'quarterly' ? 'QoQ Growth' : 'YoY Growth'

                        // Projection from stored values
                        const hasProjections = isCurrentPeriod && periodData?._projectedTotal != null
                        const projectionUnavailable = isCurrentPeriod && periodData?._projectionUnavailable === true

                        return (
                          <div className={`bg-[#0f1729] border-2 rounded-lg px-4 py-3 shadow-xl ${isSelected ? 'border-[hsl(var(--primary))]' : 'border-white/10'}`}>
                            <div className="text-white font-bold text-sm mb-2 flex items-center gap-2">
                              {label}
                              {isSelected && <span className="text-xs font-normal text-[hsl(var(--primary))]">(Selected)</span>}
                            </div>
                            <div className="flex items-center justify-between gap-6 mb-2">
                              <span className="text-white/70 text-sm">Total AUA</span>
                              <span className="text-white font-semibold text-sm">
                                {formatCurrency(total)}
                              </span>
                            </div>
                            <div className="space-y-1.5 border-t border-white/10 pt-2">
                              {sortedPayload.map((entry, index) => (
                                <div key={index} className="flex items-center justify-between gap-4 text-xs">
                                  <div className="flex items-center gap-2">
                                    <div
                                      className="w-2.5 h-2.5 rounded-full"
                                      style={{ backgroundColor: entry.color }}
                                    />
                                    <span className="text-white/70">
                                      {getBarCategoryDisplayName(String(entry.dataKey))}
                                    </span>
                                  </div>
                                  <span className="text-white font-medium">
                                    {formatCurrency(Number(entry.value) || 0)}
                                  </span>
                                </div>
                              ))}
                            </div>
                            {growth !== null && (
                              <div className="border-t border-white/10 pt-1.5 mt-1.5 space-y-1">
                                <div className="flex items-center justify-between gap-4 text-xs">
                                  <span className="text-white/70 font-medium">{growthLabel}</span>
                                  <span className={`font-semibold ${growth >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                                    {growth >= 0 ? '+' : ''}{formatCurrency(growth)}
                                  </span>
                                </div>
                                {growthPct !== null && (
                                  <div className="flex items-center justify-end text-xs">
                                    <span className={`font-semibold ${growth >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                                      {growth >= 0 ? '+' : ''}{growthPct.toFixed(1)}%
                                    </span>
                                  </div>
                                )}
                              </div>
                            )}
                            {hasProjections && (
                              <div className="border-t border-white/10 pt-1.5 mt-1.5 space-y-1.5 opacity-50">
                                <div className="text-white/50 text-[10px] font-medium uppercase tracking-wide">Projected Full Period</div>
                                {barCategories.map((cat, index) => {
                                  const actual = Number(periodData[cat]) || 0
                                  const projected = Number(periodData[`_projected_${cat}`]) || 0
                                  if (projected === actual) return null
                                  return (
                                    <div key={index} className="flex items-center justify-between gap-4 text-xs">
                                      <span className="text-white/50">
                                        {getBarCategoryDisplayName(cat)}
                                      </span>
                                      <span className="text-white/60 font-medium">
                                        {formatCurrency(projected)} <span className="text-white/30">(currently {formatCurrency(actual)})</span>
                                      </span>
                                    </div>
                                  )
                                })}
                                <div className="flex items-center justify-between gap-4 text-xs border-t border-white/5 pt-1">
                                  <span className="text-white/50 font-medium">Projected Total</span>
                                  <span className="text-white/60 font-semibold">
                                    {formatCurrency(periodData._projectedTotal)} <span className="text-white/30">(currently {formatCurrency(periodData._actualTotal)})</span>
                                  </span>
                                </div>
                              </div>
                            )}
                            {projectionUnavailable && (
                              <div className="border-t border-white/10 pt-1.5 mt-1.5">
                                <span className="text-white/30 text-[10px] italic">Projection unavailable (insufficient history)</span>
                              </div>
                            )}
                          </div>
                        )
                      }}
                    />
                    {/* Y1: Render NMEC first (bottom), NMNC last (top) per Yang feedback */}
                    {[...barCategories].reverse().map((cat, idx) => {
                      const baseColor = getBarCategoryColor(cat, idx)
                      const isLastCategory = idx === barCategories.length - 1
                      return (
                        <Bar
                          key={cat}
                          dataKey={cat}
                          stackId="aua"
                          fill={baseColor}
                          radius={isLastCategory ? [4, 4, 0, 0] : [0, 0, 0, 0]}
                        >
                          {aggregatedBarData.map((entry, index) => {
                            const isSelected = entry.period === selectedBarPeriod
                            const isLatest = index === aggregatedBarData.length - 1
                            // Selected bars get full opacity, others are dimmed when something is selected
                            const opacity = selectedBarPeriod
                              ? (isSelected ? 1 : 0.4)
                              : (isLatest ? 1 : 0.85)
                            return (
                              <Cell
                                key={`cell-${cat}-${index}`}
                                fill={baseColor}
                                fillOpacity={opacity}
                                stroke={isSelected ? 'hsl(var(--primary))' : 'transparent'}
                                strokeWidth={isSelected ? 2 : 0}
                              />
                            )
                          })}
                        </Bar>
                      )
                    })}
                    {/* F2: Dashed horizontal line at projected total AUA */}
                    {(() => {
                      const lastEntry = augmentedAuaData[augmentedAuaData.length - 1]
                      if (lastEntry?._projectedTotal == null || lastEntry._projectedTotal === lastEntry._actualTotal) return null
                      const isUp = lastEntry._projectedTotal > lastEntry._actualTotal
                      return (
                        <ReferenceLine
                          y={lastEntry._projectedTotal}
                          stroke={isUp ? 'hsl(var(--success))' : '#EF4444'}
                          strokeWidth={2}
                          strokeDasharray="6 3"
                          label={{ value: `Proj: ${formatCurrency(lastEntry._projectedTotal)}`, position: 'right', fill: isUp ? 'hsl(var(--success))' : '#EF4444', fontSize: 10 }}
                        />
                      )
                    })()}
                  </BarChart>
                </ResponsiveContainer>
              ) : panelViewMode === 'nna' && augmentedNnaData.length > 0 ? (
                /*
                 * NNA Chart — two modes:
                 * GROSS (hasGrossFlowData): Diverging bar chart.
                 *   Inflow bars above zero, outflow bars below zero (both present every period),
                 *   net flow line overlay shows the netted movement.
                 * NET-ONLY (!hasGrossFlowData): Single net bar, green = positive, red = negative.
                 *   Used until the publisher is updated to output cum_inflows/cum_outflows.
                 */
                <ResponsiveContainer width="100%" height="100%">
                  <ComposedChart
                    data={augmentedNnaData}
                    stackOffset="sign"
                    margin={{ top: 20, right: 30, left: 10, bottom: 5 }}
                    onClick={(data) => {
                      // eslint-disable-next-line @typescript-eslint/no-explicit-any
                      const chartData = data as any
                      if (chartData?.activePayload?.[0]?.payload?.period) {
                        handleBarClick({ period: chartData.activePayload[0].payload.period })
                      }
                    }}
                    style={{ cursor: 'pointer' }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" vertical={false} />
                    <XAxis
                      dataKey="label"
                      stroke="rgba(255,255,255,0.2)"
                      tick={({ x, y, payload }) => {
                        const isSelected = aggregatedNnaData.find(d => d.label === payload.value)?.period === selectedBarPeriod
                        return (
                          <text
                            x={x}
                            y={Number(y) + 12}
                            textAnchor="middle"
                            fontSize={11}
                            fill={isSelected ? 'hsl(var(--primary))' : 'rgba(255,255,255,0.6)'}
                            fontWeight={isSelected ? 600 : 400}
                          >
                            {payload.value}
                          </text>
                        )
                      }}
                      axisLine={false}
                      tickLine={false}
                    />
                    <YAxis
                      stroke="rgba(255,255,255,0.2)"
                      tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.6)' }}
                      tickFormatter={(value) => {
                        const absVal = Math.abs(value)
                        if (absVal >= 1e9) return `${value < 0 ? '-' : ''}$${(absVal / 1e9).toFixed(1)}B`
                        if (absVal >= 1e6) return `${value < 0 ? '-' : ''}$${(absVal / 1e6).toFixed(0)}M`
                        return `$${value}`
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
                        if (!active || !payload || payload.length === 0) return null
                        // eslint-disable-next-line @typescript-eslint/no-explicit-any
                        const periodData = payload[0]?.payload as any
                        const isSelected = periodData?.period === selectedBarPeriod
                        const isCurrentNnaPeriod = periodData?.period === aggregatedNnaData[aggregatedNnaData.length - 1]?.period

                        // Period-over-period growth for NNA
                        const nnaGrowthLabel = granularity === 'monthly' ? 'MoM Change' : granularity === 'quarterly' ? 'QoQ Change' : 'YoY Change'
                        const currentNnaIdx = aggregatedNnaData.findIndex(d => d.period === periodData?.period)
                        const priorNnaPeriod = currentNnaIdx > 0 ? aggregatedNnaData[currentNnaIdx - 1] : null
                        const priorNet = priorNnaPeriod?.net ?? null
                        const currentNet = periodData?.net || 0
                        const nnaChange = priorNet !== null ? currentNet - priorNet : null

                        return (
                          <div className={`bg-[#0f1729] border-2 rounded-lg px-4 py-3 shadow-xl ${isSelected ? 'border-[hsl(var(--primary))]' : 'border-white/10'}`}>
                            <div className="text-white font-bold text-sm mb-2 flex items-center gap-2">
                              {label}
                              {isSelected && <span className="text-xs font-normal text-[hsl(var(--primary))]">(Selected)</span>}
                            </div>
                            <div className="space-y-1.5">
                              {hasGrossFlowData ? (
                                <>
                                  <div className="flex items-center justify-between gap-4 text-xs">
                                    <div className="flex items-center gap-2">
                                      <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: NNA_COLORS.inflow }} />
                                      <span className="text-white/70">Inflows</span>
                                    </div>
                                    <span className="font-medium text-[hsl(var(--success))]">
                                      +{formatCurrency(periodData?.inflow || 0)}
                                    </span>
                                  </div>
                                  <div className="flex items-center justify-between gap-4 text-xs">
                                    <div className="flex items-center gap-2">
                                      <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: NNA_COLORS.outflow }} />
                                      <span className="text-white/70">Outflows</span>
                                    </div>
                                    <span className="font-medium text-red-400">
                                      -{formatCurrency(Math.abs(periodData?.outflow || 0))}
                                    </span>
                                  </div>
                                  <div className="flex items-center justify-between gap-4 text-xs border-t border-white/10 pt-1.5 mt-1.5">
                                    <span className="text-white/70 font-medium">Net Flow</span>
                                    <span className={`font-semibold ${(periodData?.net || 0) >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                                      {(periodData?.net || 0) >= 0 ? '+' : ''}{formatCurrency(periodData?.net || 0)}
                                    </span>
                                  </div>
                                </>
                              ) : (
                                <div className="flex items-center justify-between gap-4 text-xs">
                                  <span className="text-white/70 font-medium">Net NNA</span>
                                  <span className={`font-semibold ${(periodData?.net || 0) >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                                    {(periodData?.net || 0) >= 0 ? '+' : ''}{formatCurrency(periodData?.net || 0)}
                                  </span>
                                </div>
                              )}
                            </div>
                            {nnaChange !== null && (
                              <div className="border-t border-white/10 pt-1.5 mt-1.5">
                                <div className="flex items-center justify-between gap-4 text-xs">
                                  <span className="text-white/70 font-medium">{nnaGrowthLabel}</span>
                                  <span className={`font-semibold ${nnaChange >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                                    {nnaChange >= 0 ? '+' : ''}{formatCurrency(nnaChange)}
                                  </span>
                                </div>
                              </div>
                            )}
                            {isCurrentNnaPeriod && periodData?._projectedNet != null && hasGrossFlowData && (() => {
                              const projInflow = periodData._projectedInflow as number
                              const projOutflow = periodData._projectedOutflow as number
                              const projNet = periodData._projectedNet as number
                              return (
                                <div className="border-t border-white/10 pt-1.5 mt-1.5 space-y-1.5 opacity-50">
                                  <div className="text-white/50 text-[10px] font-medium uppercase tracking-wide">Projected Full Period</div>
                                  <div className="flex items-center justify-between gap-4 text-xs">
                                    <span className="text-white/50">Inflows</span>
                                    <span className="text-white/60 font-medium">
                                      +{formatCurrency(projInflow)} <span className="text-white/30">(currently +{formatCurrency(periodData.inflow)})</span>
                                    </span>
                                  </div>
                                  <div className="flex items-center justify-between gap-4 text-xs">
                                    <span className="text-white/50">Outflows</span>
                                    <span className="text-white/60 font-medium">
                                      -{formatCurrency(Math.abs(projOutflow))} <span className="text-white/30">(currently -{formatCurrency(Math.abs(periodData.outflow))})</span>
                                    </span>
                                  </div>
                                  <div className="flex items-center justify-between gap-4 text-xs border-t border-white/5 pt-1">
                                    <span className="text-white/50 font-medium">Net</span>
                                    <span className="text-white/60 font-semibold">
                                      {projNet >= 0 ? '+' : ''}{formatCurrency(projNet)} <span className="text-white/30">(currently {(periodData.net || 0) >= 0 ? '+' : ''}{formatCurrency(periodData.net || 0)})</span>
                                    </span>
                                  </div>
                                </div>
                              )
                            })()}
                            {isCurrentNnaPeriod && !hasGrossFlowData && periodData?._projectedNet != null && (() => {
                              const projNet = periodData._projectedNet as number
                              return (
                                <div className="border-t border-white/10 pt-1.5 mt-1.5 space-y-1.5 opacity-50">
                                  <div className="text-white/50 text-[10px] font-medium uppercase tracking-wide">Projected Full Period</div>
                                  <div className="flex items-center justify-between gap-4 text-xs">
                                    <span className="text-white/50 font-medium">Net</span>
                                    <span className="text-white/60 font-semibold">
                                      {projNet >= 0 ? '+' : ''}{formatCurrency(projNet)} <span className="text-white/30">(currently {(periodData.net || 0) >= 0 ? '+' : ''}{formatCurrency(periodData.net || 0)})</span>
                                    </span>
                                  </div>
                                </div>
                              )
                            })()}
                          </div>
                        )
                      }}
                    />
                    {hasGrossFlowData ? (
                      <>
                        {/* GROSS MODE: Inflow bar above zero, outflow bar below zero */}
                        <Bar dataKey="inflow" stackId="nna" radius={[4, 4, 0, 0]}>
                          {augmentedNnaData.map((entry, index) => {
                            const isSelected = entry.period === selectedBarPeriod
                            const isLatest = index === augmentedNnaData.length - 1
                            const opacity = selectedBarPeriod ? (isSelected ? 1 : 0.4) : (isLatest ? 1 : 0.85)
                            return (
                              <Cell
                                key={`inflow-${index}`}
                                fill={NNA_COLORS.inflow}
                                fillOpacity={opacity}
                                stroke={isSelected ? 'hsl(var(--primary))' : 'transparent'}
                                strokeWidth={isSelected ? 2 : 0}
                              />
                            )
                          })}
                        </Bar>
                        <Bar dataKey="outflow" stackId="nna" radius={[0, 0, 4, 4]}>
                          {augmentedNnaData.map((entry, index) => {
                            const isSelected = entry.period === selectedBarPeriod
                            const isLatest = index === augmentedNnaData.length - 1
                            const opacity = selectedBarPeriod ? (isSelected ? 1 : 0.4) : (isLatest ? 1 : 0.85)
                            return (
                              <Cell
                                key={`outflow-${index}`}
                                fill={NNA_COLORS.outflow}
                                fillOpacity={opacity}
                                stroke={isSelected ? 'hsl(var(--primary))' : 'transparent'}
                                strokeWidth={isSelected ? 2 : 0}
                              />
                            )
                          })}
                        </Bar>
                        {/* Net flow line: actual NNA value (inflows + outflows) */}
                        <Line
                          type="monotone"
                          dataKey="net"
                          stroke="#F59E0B"
                          strokeWidth={3}
                          dot={{ r: 5, fill: '#F59E0B', strokeWidth: 2, stroke: 'hsl(var(--background))' }}
                          activeDot={{ r: 7 }}
                          connectNulls
                        />
                      </>
                    ) : (
                      /* NET-ONLY MODE: Single bar colored green/red per sign */
                      <Bar dataKey="net" radius={[4, 4, 0, 0]}>
                        {augmentedNnaData.map((entry, index) => {
                          const isSelected = entry.period === selectedBarPeriod
                          const isLatest = index === augmentedNnaData.length - 1
                          const opacity = selectedBarPeriod ? (isSelected ? 1 : 0.4) : (isLatest ? 1 : 0.85)
                          return (
                            <Cell
                              key={`net-${index}`}
                              fill={entry.net >= 0 ? NNA_COLORS.inflow : NNA_COLORS.outflow}
                              fillOpacity={opacity}
                              stroke={isSelected ? 'hsl(var(--primary))' : 'transparent'}
                              strokeWidth={isSelected ? 2 : 0}
                            />
                          )
                        })}
                      </Bar>
                    )}
                    {/* F2: Dashed horizontal line at projected net NNA */}
                    {(() => {
                      const lastNna = augmentedNnaData[augmentedNnaData.length - 1]
                      if (lastNna?._projectedNet == null) return null
                      const projNet = lastNna._projectedNet as number
                      const actualNet = lastNna.net
                      if (projNet === actualNet) return null
                      const isUp = projNet > actualNet
                      return (
                        <ReferenceLine
                          y={projNet}
                          stroke={isUp ? 'hsl(var(--success))' : '#EF4444'}
                          strokeWidth={2}
                          strokeDasharray="6 3"
                          label={{ value: `Proj: ${projNet >= 0 ? '+' : ''}${formatCurrency(projNet)}`, position: 'right', fill: isUp ? 'hsl(var(--success))' : '#EF4444', fontSize: 10 }}
                        />
                      )
                    })()}
                  </ComposedChart>
                </ResponsiveContainer>
              ) : panelViewMode === 'aua' && auaSubMode === 'mix' && aggregatedMixData.length > 0 && mixCategories.length > 0 ? (
                /* Y3-FE: AUA Mix Stacked Bar Chart (asset class breakdown) */
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={aggregatedMixData}
                    margin={{ top: 20, right: 30, left: 10, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" vertical={false} />
                    <XAxis
                      dataKey="label"
                      stroke="rgba(255,255,255,0.2)"
                      tick={{ fontSize: 11, fill: 'rgba(255,255,255,0.6)' }}
                      axisLine={false}
                      tickLine={false}
                    />
                    <YAxis
                      stroke="rgba(255,255,255,0.2)"
                      tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.6)' }}
                      tickFormatter={(value) => {
                        if (value >= 1e9) return `$${(value / 1e9).toFixed(1)}B`
                        if (value >= 1e6) return `$${(value / 1e6).toFixed(0)}M`
                        return `$${value}`
                      }}
                      width={55}
                      axisLine={false}
                      tickLine={false}
                    />
                    <RechartsTooltip
                      wrapperStyle={{ zIndex: 40 }}
                      cursor={{ fill: 'rgba(255,255,255,0.08)' }}
                      content={({ active, payload, label }) => {
                        if (!active || !payload || payload.length === 0) return null
                        const total = payload.reduce((sum, entry) => sum + (Number(entry.value) || 0), 0)
                        const sortedPayload = [...payload].sort((a, b) => (Number(b.value) || 0) - (Number(a.value) || 0))
                        return (
                          <div className="bg-[#0f1729] border-2 border-white/10 rounded-lg px-4 py-3 shadow-xl">
                            <div className="text-white font-bold text-sm mb-2">{label}</div>
                            <div className="flex items-center justify-between gap-6 mb-2">
                              <span className="text-white/70 text-sm">Total AUA</span>
                              <span className="text-white font-semibold text-sm">{formatCurrency(total)}</span>
                            </div>
                            <div className="space-y-1.5 border-t border-white/10 pt-2">
                              {sortedPayload.map((entry, index) => (
                                <div key={index} className="flex items-center justify-between gap-4 text-xs">
                                  <div className="flex items-center gap-2">
                                    <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: entry.color }} />
                                    <span className="text-white/70">{String(entry.dataKey)}</span>
                                  </div>
                                  <span className="text-white font-medium">{formatCurrency(Number(entry.value) || 0)}</span>
                                </div>
                              ))}
                            </div>
                          </div>
                        )
                      }}
                    />
                    {[...mixCategories].reverse().map((cat, idx) => {
                      const color = getAssetClassColor(cat, idx)
                      const isLast = idx === mixCategories.length - 1
                      return (
                        <Bar
                          key={cat}
                          dataKey={cat}
                          stackId="mix"
                          fill={color}
                          fillOpacity={0.85}
                          radius={isLast ? [4, 4, 0, 0] : [0, 0, 0, 0]}
                        />
                      )
                    })}
                  </BarChart>
                </ResponsiveContainer>
              ) : panelViewMode === 'aua' && auaSubMode === 'mix' ? (
                /* Y3-FE: Mix data unavailable */
                <div className="h-full flex items-center justify-center">
                  <p className="text-white/60 text-sm">Asset class mix data unavailable</p>
                </div>
              ) : panelViewMode === 'gro' && augmentedGroData.length > 0 ? (
                /* GRO: Stacked bars (Market + Net Flows) + Total line overlay */
                <ResponsiveContainer width="100%" height="100%">
                  <ComposedChart
                    data={augmentedGroData}
                    margin={{ top: 20, right: 30, left: 10, bottom: 5 }}
                    stackOffset="sign"
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" vertical={false} />
                    <XAxis
                      dataKey="label"
                      stroke="rgba(255,255,255,0.2)"
                      tick={{ fontSize: 11, fill: 'rgba(255,255,255,0.6)' }}
                      axisLine={false}
                      tickLine={false}
                    />
                    <YAxis
                      stroke="rgba(255,255,255,0.2)"
                      tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.6)' }}
                      tickFormatter={(value) => {
                        if (Math.abs(value) >= 1e9) return `${value < 0 ? '-' : ''}$${(Math.abs(value) / 1e9).toFixed(1)}B`
                        if (Math.abs(value) >= 1e6) return `${value < 0 ? '-' : ''}$${(Math.abs(value) / 1e6).toFixed(0)}M`
                        return `$${value}`
                      }}
                      width={55}
                      axisLine={false}
                      tickLine={false}
                      label={{ value: 'AUA Change', angle: -90, position: 'insideLeft', offset: -5, style: { fontSize: 9, fill: 'rgba(255,255,255,0.3)' } }}
                    />
                    <ReferenceLine y={0} stroke="rgba(255,255,255,0.3)" strokeWidth={1} />
                    <RechartsTooltip
                      wrapperStyle={{ zIndex: 40 }}
                      cursor={{ fill: 'rgba(255,255,255,0.08)' }}
                      content={({ active, payload }) => {
                        if (!active || !payload || payload.length === 0) return null
                        // Datum-driven rendering — not payload.map()
                        const datum = payload[0]?.payload as { label: string; market: number; nna: number; total: number; total_proj?: number | null; period: string; _isProjection?: boolean; endDate: string }
                        if (!datum || datum._isProjection) return null

                        const signFmt = (v: number) => `${v >= 0 ? '+' : ''}${formatCurrency(v)}`
                        const signColor = (v: number) => v >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'

                        // Period-over-period comparison (Total only)
                        const groGrowthLabel = granularity === 'monthly' ? 'MoM Change' : granularity === 'quarterly' ? 'QoQ Change' : 'YoY Change'
                        const groIdx = aggregatedGroData.findIndex(d => d.period === datum.period)
                        const priorGro = groIdx > 0 ? aggregatedGroData[groIdx - 1] : null
                        const groTotalChange = priorGro ? datum.total - priorGro.total : null

                        // Projection (Total only, last period)
                        const isLastPeriod = datum.period === aggregatedGroData[aggregatedGroData.length - 1]?.period
                        const hasGroProjection = isLastPeriod && datum.total_proj != null && datum.total_proj !== datum.total

                        return (
                          <div className="bg-[#0f1729] border-2 border-white/10 rounded-lg px-4 py-3 shadow-xl">
                            <div className="text-white font-bold text-sm mb-0.5">{datum.label}</div>
                            <div className="text-white/30 text-[10px] mb-2">AUA change (period delta)</div>
                            <div className="space-y-1.5">
                              <div className="flex items-center justify-between gap-6 text-xs">
                                <div className="flex items-center gap-2">
                                  <div className="w-2.5 h-2.5 rounded-sm" style={{ backgroundColor: GRO_COLORS.market }} />
                                  <span className="text-white/70">Market</span>
                                </div>
                                <span className={`font-medium ${signColor(datum.market)}`}>{signFmt(datum.market)}</span>
                              </div>
                              <div className="flex items-center justify-between gap-6 text-xs">
                                <div className="flex items-center gap-2">
                                  <div className="w-2.5 h-2.5 rounded-sm" style={{ backgroundColor: GRO_COLORS.nna }} />
                                  <span className="text-white/70">Net Flows</span>
                                </div>
                                <span className={`font-medium ${signColor(datum.nna)}`}>{signFmt(datum.nna)}</span>
                              </div>
                              <div className="flex items-center justify-between gap-6 text-xs border-t border-white/10 pt-1.5 mt-1.5">
                                <div className="flex items-center gap-2">
                                  <div className="w-3 h-0.5 rounded-full" style={{ backgroundColor: GRO_COLORS.total }} />
                                  <span className="text-white/70 font-medium">Total Change</span>
                                </div>
                                <span className={`font-semibold ${signColor(datum.total)}`}>{signFmt(datum.total)}</span>
                              </div>
                            </div>
                            {groTotalChange !== null && (
                              <div className="border-t border-white/10 pt-1.5 mt-1.5">
                                <div className="flex items-center justify-between gap-4 text-xs">
                                  <span className="text-white/70 font-medium">{groGrowthLabel}</span>
                                  <span className={`font-semibold ${signColor(groTotalChange)}`}>{signFmt(groTotalChange)}</span>
                                </div>
                              </div>
                            )}
                            {hasGroProjection && (
                              <div className="border-t border-white/10 pt-1.5 mt-1.5 opacity-50">
                                <div className="text-white/50 text-[10px] font-medium uppercase tracking-wide mb-1">Projected Full Period</div>
                                <div className="flex items-center justify-between gap-4 text-xs">
                                  <span className="text-white/50">Total Change</span>
                                  <span className="text-white/60 font-semibold">
                                    {signFmt(datum.total_proj!)} <span className="text-white/30">(currently {signFmt(datum.total)})</span>
                                  </span>
                                </div>
                              </div>
                            )}
                          </div>
                        )
                      }}
                    />
                    <Bar dataKey="market" stackId="gro" fill={GRO_COLORS.market} fillOpacity={0.8} radius={[0, 0, 0, 0]} isAnimationActive={false} />
                    <Bar dataKey="nna" stackId="gro" fill={GRO_COLORS.nna} fillOpacity={0.8} radius={[0, 0, 0, 0]} isAnimationActive={false} />
                    <Line type="monotone" dataKey="total" stroke={GRO_COLORS.total} strokeWidth={3} dot={false} />
                    {/* Total-only dashed projection line */}
                    <Line type="monotone" dataKey="total_proj" stroke={GRO_COLORS.total} strokeWidth={2} strokeDasharray="6 3" dot={false} connectNulls={false} isAnimationActive={false} legendType="none" />
                  </ComposedChart>
                </ResponsiveContainer>
              ) : panelViewMode === 'gro' ? (
                /* Y5-FE: GRO data unavailable */
                <div className="h-full flex items-center justify-center">
                  <p className="text-white/60 text-sm">Growth decomposition data unavailable</p>
                </div>
              ) : (
                <div className="h-full flex items-center justify-center">
                  <p className="text-white/60 text-sm">No {panelViewMode === 'aua' ? 'AUA' : 'NNA'} data available</p>
                </div>
              )}
            </div>

            {/* Legend */}
            <div className="flex justify-center gap-6 mt-4">
              {panelViewMode === 'aua' && auaSubMode === 'clients' ? (
                barCategories.map((cat, idx) => (
                  <div key={cat} className="flex items-center gap-2">
                    <div
                      className="w-3 h-3 rounded-sm"
                      style={{ backgroundColor: getBarCategoryColor(cat, idx) }}
                    />
                    <span className="text-xs text-white/70">{getBarCategoryDisplayName(cat)}</span>
                  </div>
                ))
              ) : panelViewMode === 'aua' && auaSubMode === 'mix' ? (
                mixCategories.map((cat, idx) => (
                  <div key={cat} className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: getAssetClassColor(cat, idx) }} />
                    <span className="text-xs text-white/70">{cat}</span>
                  </div>
                ))
              ) : panelViewMode === 'gro' ? (
                <>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: GRO_COLORS.market }} />
                    <span className="text-xs text-white/70">Market</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: GRO_COLORS.nna }} />
                    <span className="text-xs text-white/70">Net Flows (NNA)</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-0.5 rounded-full" style={{ backgroundColor: GRO_COLORS.total }} />
                    <span className="text-xs text-white/70">Total (Market + NNA)</span>
                  </div>
                </>
              ) : hasGrossFlowData ? (
                <>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: NNA_COLORS.inflow }} />
                    <span className="text-xs text-white/70">Inflows</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: NNA_COLORS.outflow }} />
                    <span className="text-xs text-white/70">Outflows</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-0.5 rounded-full" style={{ backgroundColor: '#F59E0B' }} />
                    <span className="text-xs text-white/70">Net Flow</span>
                  </div>
                </>
              ) : (
                <>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: NNA_COLORS.inflow }} />
                    <span className="text-xs text-white/70">Positive NNA</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: NNA_COLORS.outflow }} />
                    <span className="text-xs text-white/70">Negative NNA</span>
                  </div>
                </>
              )}
            </div>

            {/* Selected/Latest Value Highlight (AUA Clients + NNA only — not Mix or GRO) */}
            {panelViewMode !== 'gro' && !(panelViewMode === 'aua' && auaSubMode === 'mix') && (panelViewMode === 'aua' ? aggregatedAuaData : aggregatedNnaData).length > 0 && (() => {
              const activeData = panelViewMode === 'aua' ? aggregatedAuaData : aggregatedNnaData
              const latest = activeData[activeData.length - 1]
              const src = selectedBarData || latest
              const isSelectedPeriod = !!selectedBarData
              const isLatestPeriod = src.period === latest.period

              // --- Helper: get period start date from a period key ---
              const getPeriodStartDate = (periodKey: string): Date => {
                if (granularity === 'monthly') {
                  // "2026-02" -> Feb 1
                  const [y, m] = periodKey.split('-').map(Number)
                  return new Date(y, m - 1, 1)
                } else if (granularity === 'quarterly') {
                  // "2026-Q1" -> Jan 1
                  const [y, q] = periodKey.split('-Q').map(Number)
                  return new Date(y, (q - 1) * 3, 1)
                } else {
                  // "2026" -> Jan 1
                  return new Date(Number(periodKey), 0, 1)
                }
              }

              // --- Helper: find comparable prior-period snapshot from daily data ---
              // For in-progress periods: finds the data point at the same day-offset in the prior period
              // For completed periods: returns the end-of-period (last) data point
              // With pre-aggregated period data (PSCFIX schema), prior comparison is a direct
              // period lookup — no daily data or day-offset matching needed.

              // --- AUA current values ---
              const auaTotal = panelViewMode === 'aua'
                ? barCategories.reduce((sum, cat) => sum + (Number((src as Record<string, unknown>)[cat]) || 0), 0)
                : 0
              const auaNewClient = panelViewMode === 'aua'
                ? (Number((src as Record<string, unknown>)['NMNC']) || Number((src as Record<string, unknown>)['nmnc']) || 0)
                : 0
              const auaExistingClient = panelViewMode === 'aua'
                ? (Number((src as Record<string, unknown>)['NMEC']) || Number((src as Record<string, unknown>)['nmec']) || 0)
                : 0

              // --- AUA comparable growth ---
              const auaSrcIdx = panelViewMode === 'aua'
                ? aggregatedAuaData.findIndex(d => d.period === src.period)
                : -1
              const auaPriorAgg = auaSrcIdx > 0 ? aggregatedAuaData[auaSrcIdx - 1] : null
              const auaPriorLabel = auaPriorAgg ? String(auaPriorAgg.label) : null

              let auaGrowth: number | null = null
              let auaGrowthPct: number | null = null
              let auaNewGrowth: number | null = null
              let auaNewGrowthPct: number | null = null
              let auaExistingGrowth: number | null = null
              let auaExistingGrowthPct: number | null = null
              let auaComparableDays: number | null = null

              if (auaPriorAgg) {
                const prior = auaPriorAgg as Record<string, unknown>
                const priorTotal = barCategories.reduce((sum, cat) => sum + (Number(prior[cat]) || 0), 0)
                const priorNew = Number(prior['NMNC']) || Number(prior['nmnc']) || 0
                const priorExisting = Number(prior['NMEC']) || Number(prior['nmec']) || 0
                auaComparableDays = null  // not applicable with pre-aggregated period data

                if (priorTotal > 0) {
                  auaGrowth = auaTotal - priorTotal
                  auaGrowthPct = ((auaTotal / priorTotal) - 1) * 100
                }
                if (priorNew > 0) {
                  auaNewGrowth = auaNewClient - priorNew
                  auaNewGrowthPct = ((auaNewClient / priorNew) - 1) * 100
                }
                if (priorExisting > 0) {
                  auaExistingGrowth = auaExistingClient - priorExisting
                  auaExistingGrowthPct = ((auaExistingClient / priorExisting) - 1) * 100
                }
              }

              // --- NNA current values ---
              const nnaInflow  = Number((src as { inflow?: number }).inflow) || 0
              const nnaOutflow = Math.abs(Number((src as { outflow?: number }).outflow) || 0)
              const nnaNet     = Number((src as { net?: number }).net) || 0

              // --- NNA comparable growth ---
              const nnaSrcIdx = panelViewMode === 'nna'
                ? aggregatedNnaData.findIndex(d => d.period === src.period)
                : -1
              const nnaPriorAgg = nnaSrcIdx > 0 ? aggregatedNnaData[nnaSrcIdx - 1] : null
              const nnaPriorLabel = nnaPriorAgg ? String(nnaPriorAgg.label) : null

              let nnaInflowGrowth: number | null = null
              let nnaInflowGrowthPct: number | null = null
              let nnaOutflowGrowth: number | null = null
              let nnaOutflowGrowthPct: number | null = null
              let nnaNetGrowth: number | null = null
              let nnaNetGrowthPct: number | null = null
              let nnaComparableDays: number | null = null

              if (nnaPriorAgg && timeseriesData?.nna?.data) {
                const nnaDaily = timeseriesData.nna.data
                const nnaCategories = timeseriesData.nna.categories || []
                const grossFlows = nnaCategories.includes('Inflows') && nnaCategories.includes('Outflows')
                const isInProgress = isLatestPeriod && !isSelectedPeriod

                // For NNA flows we need to compute period-to-date flows (not snapshots)
                // Flow = last cumulative value in window - first cumulative value before window (end of prior period)
                const computePeriodFlows = (periodKey: string, maxDayOffset?: number) => {
                  const periodStart = getPeriodStartDate(periodKey)
                  const maxDate = maxDayOffset !== undefined
                    ? new Date(periodStart.getTime() + maxDayOffset * 24 * 60 * 60 * 1000)
                    : new Date(9999, 0, 1) // no limit

                  const periodPoints = nnaDaily.filter(p => {
                    const d = new Date(String(p.date) + 'T12:00:00')
                    return getPeriodInfo(d).periodKey === periodKey && d <= maxDate
                  })
                  if (periodPoints.length === 0) return null

                  const first = periodPoints[0]
                  const last = periodPoints[periodPoints.length - 1]

                  // Get the cumulative value just before this period (last point of prior period)
                  // For differencing: flow = last_cum - first_cum_before_period
                  // Since first point in period IS the first cum value at period start,
                  // and last is the cum value at the end of the window:
                  // period flow = last_cum - prev_period_end_cum
                  // But we already have the first point of this period which ~= prev period end
                  // Use first point as the baseline (it's the earliest snapshot in the period)
                  const netFlow = (Number(last['NNA']) || 0) - (Number(first['NNA']) || 0)
                  const inflowFlow = grossFlows ? (Number(last['Inflows']) || 0) - (Number(first['Inflows']) || 0) : 0
                  const outflowFlow = grossFlows ? Math.abs((Number(last['Outflows']) || 0) - (Number(first['Outflows']) || 0)) : 0

                  return { net: netFlow, inflow: inflowFlow, outflow: outflowFlow, days: periodPoints.length }
                }

                if (isInProgress) {
                  // Comparable: same day-offset in both periods
                  const currentStart = getPeriodStartDate(String(src.period))
                  const currentEndDate = new Date(String(src.endDate) + 'T12:00:00')
                  const dayOffset = Math.floor((currentEndDate.getTime() - currentStart.getTime()) / (1000 * 60 * 60 * 24))

                  const currentFlows = computePeriodFlows(String(src.period))
                  const priorFlows = computePeriodFlows(String(nnaPriorAgg.period), dayOffset)

                  if (currentFlows && priorFlows) {
                    nnaComparableDays = dayOffset + 1
                    nnaNetGrowth = currentFlows.net - priorFlows.net
                    if (priorFlows.net !== 0) nnaNetGrowthPct = ((currentFlows.net / Math.abs(priorFlows.net)) - (priorFlows.net >= 0 ? 1 : -1)) * 100
                    if (grossFlows) {
                      nnaInflowGrowth = currentFlows.inflow - priorFlows.inflow
                      if (priorFlows.inflow > 0) nnaInflowGrowthPct = ((currentFlows.inflow / priorFlows.inflow) - 1) * 100
                      nnaOutflowGrowth = currentFlows.outflow - priorFlows.outflow
                      if (priorFlows.outflow > 0) nnaOutflowGrowthPct = ((currentFlows.outflow / priorFlows.outflow) - 1) * 100
                    }
                  }
                } else {
                  // Completed period: full period vs full prior period (from aggregated data)
                  const priorInflow = Number((nnaPriorAgg as { inflow?: number }).inflow) || 0
                  const priorOutflow = Math.abs(Number((nnaPriorAgg as { outflow?: number }).outflow) || 0)
                  const priorNet = Number((nnaPriorAgg as { net?: number }).net) || 0

                  if (priorInflow > 0) { nnaInflowGrowth = nnaInflow - priorInflow; nnaInflowGrowthPct = ((nnaInflow / priorInflow) - 1) * 100 }
                  if (priorOutflow > 0) { nnaOutflowGrowth = nnaOutflow - priorOutflow; nnaOutflowGrowthPct = ((nnaOutflow / priorOutflow) - 1) * 100 }
                  nnaNetGrowth = nnaNet - priorNet
                  if (priorNet !== 0) nnaNetGrowthPct = ((nnaNet / Math.abs(priorNet)) - (priorNet >= 0 ? 1 : -1)) * 100
                }
              }

              // Comparable period label: "vs Day 58 of Q4 '25" for in-progress, "vs Q4 '25" for completed
              const comparableDays = panelViewMode === 'aua' ? auaComparableDays : nnaComparableDays
              const priorLabel = panelViewMode === 'aua' ? auaPriorLabel : nnaPriorLabel
              const comparisonLabel = comparableDays && comparableDays > 0
                ? `vs Day ${comparableDays} of ${priorLabel}`
                : priorLabel ? `vs ${priorLabel}` : null

              return (
                <div className="w-full mt-4 rounded-xl bg-white/5 border border-white/10 px-6 py-4">
                  {/* Period header */}
                  <div className="flex items-center justify-center gap-2 mb-4">
                    {isSelectedPeriod && (
                      <div className="w-1.5 h-1.5 rounded-full bg-[hsl(var(--primary))] animate-pulse flex-shrink-0" />
                    )}
                    <span className="text-[10px] text-white/50 uppercase tracking-widest font-medium">
                      {src.label}
                    </span>
                    {isSelectedPeriod && (
                      <button
                        onClick={() => setSelectedBarPeriod(null)}
                        className="text-[10px] text-white/30 hover:text-white/60 transition-colors"
                      >
                        (clear)
                      </button>
                    )}
                  </div>

                  {/* Metric tiles */}
                  {panelViewMode === 'aua' ? (
                    <div className="flex flex-wrap items-stretch gap-3">
                      <div className="flex-1 min-w-[180px] flex flex-col items-center px-4 py-3 rounded-lg bg-[#4CAF50]/10 border border-[#4CAF50]/30">
                        <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2">New Clients</div>
                        <div className="text-2xl font-bold text-[#4CAF50]">{formatCurrency(auaNewClient)}</div>
                        {auaNewGrowth !== null && (
                          <>
                            <div className={`text-sm font-semibold mt-2 ${auaNewGrowth >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                              {auaNewGrowth >= 0 ? '+' : ''}{formatCurrency(auaNewGrowth)}
                              {auaNewGrowthPct !== null && <span className="ml-1">({auaNewGrowth >= 0 ? '+' : ''}{auaNewGrowthPct.toFixed(1)}%)</span>}
                            </div>
                            <div className="text-[9px] text-white/40 tracking-widest mt-0.5">{comparisonLabel}</div>
                          </>
                        )}
                      </div>
                      <div className="flex-1 min-w-[180px] flex flex-col items-center px-4 py-3 rounded-lg bg-[#2196F3]/10 border border-[#2196F3]/30">
                        <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2">Existing Clients</div>
                        <div className="text-2xl font-bold text-[#2196F3]">{formatCurrency(auaExistingClient)}</div>
                        {auaExistingGrowth !== null && (
                          <>
                            <div className={`text-sm font-semibold mt-2 ${auaExistingGrowth >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                              {auaExistingGrowth >= 0 ? '+' : ''}{formatCurrency(auaExistingGrowth)}
                              {auaExistingGrowthPct !== null && <span className="ml-1">({auaExistingGrowth >= 0 ? '+' : ''}{auaExistingGrowthPct.toFixed(1)}%)</span>}
                            </div>
                            <div className="text-[9px] text-white/40 tracking-widest mt-0.5">{comparisonLabel}</div>
                          </>
                        )}
                      </div>
                      <div className="flex-1 min-w-[180px] flex flex-col items-center px-4 py-3 rounded-lg bg-white/5 border border-white/10">
                        <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2">Total AUA</div>
                        <div className="text-2xl font-bold text-white">{formatCurrency(auaTotal)}</div>
                        {auaGrowth !== null && (
                          <>
                            <div className={`text-sm font-semibold mt-2 ${auaGrowth >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                              {auaGrowth >= 0 ? '+' : ''}{formatCurrency(auaGrowth)}
                              {auaGrowthPct !== null && <span className="ml-1">({auaGrowth >= 0 ? '+' : ''}{auaGrowthPct.toFixed(1)}%)</span>}
                            </div>
                            <div className="text-[9px] text-white/40 tracking-widest mt-0.5">{comparisonLabel}</div>
                          </>
                        )}
                      </div>
                    </div>
                  ) : hasGrossFlowData ? (
                    <div className="flex flex-wrap items-stretch gap-3">
                      <div className="flex-1 min-w-[180px] flex flex-col items-center px-4 py-3 rounded-lg bg-[hsl(var(--success))]/10 border border-[hsl(var(--success))]/30">
                        <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2">Inflows</div>
                        <div className="text-2xl font-bold text-[hsl(var(--success))]">+{formatCurrency(nnaInflow)}</div>
                        {nnaInflowGrowth !== null && (
                          <>
                            <div className={`text-sm font-semibold mt-2 ${nnaInflowGrowth >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                              {nnaInflowGrowth >= 0 ? '+' : ''}{formatCurrency(nnaInflowGrowth)}
                              {nnaInflowGrowthPct !== null && <span className="ml-1">({nnaInflowGrowth >= 0 ? '+' : ''}{nnaInflowGrowthPct.toFixed(1)}%)</span>}
                            </div>
                            <div className="text-[9px] text-white/40 tracking-widest mt-0.5">{comparisonLabel}</div>
                          </>
                        )}
                      </div>
                      <div className="flex-1 min-w-[180px] flex flex-col items-center px-4 py-3 rounded-lg bg-red-500/10 border border-red-500/30">
                        <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2">Outflows</div>
                        <div className="text-2xl font-bold text-red-400">-{formatCurrency(nnaOutflow)}</div>
                        {nnaOutflowGrowth !== null && (
                          <>
                            <div className={`text-sm font-semibold mt-2 ${nnaOutflowGrowth >= 0 ? 'text-red-400' : 'text-[hsl(var(--success))]'}`}>
                              {nnaOutflowGrowth >= 0 ? '+' : ''}{formatCurrency(nnaOutflowGrowth)}
                              {nnaOutflowGrowthPct !== null && <span className="ml-1">({nnaOutflowGrowth >= 0 ? '+' : ''}{nnaOutflowGrowthPct.toFixed(1)}%)</span>}
                            </div>
                            <div className="text-[9px] text-white/40 tracking-widest mt-0.5">{comparisonLabel}</div>
                          </>
                        )}
                      </div>
                      <div className="flex-1 min-w-[180px] flex flex-col items-center px-4 py-3 rounded-lg bg-white/5 border border-white/10">
                        <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2">Net Flow</div>
                        <div className={`text-2xl font-bold ${nnaNet >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                          {nnaNet >= 0 ? '+' : ''}{formatCurrency(nnaNet)}
                        </div>
                        {nnaNetGrowth !== null && (
                          <>
                            <div className={`text-sm font-semibold mt-2 ${nnaNetGrowth >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                              {nnaNetGrowth >= 0 ? '+' : ''}{formatCurrency(nnaNetGrowth)}
                              {nnaNetGrowthPct !== null && <span className="ml-1">({nnaNetGrowth >= 0 ? '+' : ''}{nnaNetGrowthPct.toFixed(1)}%)</span>}
                            </div>
                            <div className="text-[9px] text-white/40 tracking-widest mt-0.5">{comparisonLabel}</div>
                          </>
                        )}
                      </div>
                    </div>
                  ) : (
                    <div className="flex justify-center">
                      <div className="flex flex-col items-center px-10 py-3 rounded-lg bg-white/5 border border-white/10">
                        <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2">Net New Assets</div>
                        <div className={`text-3xl font-bold ${nnaNet >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                          {nnaNet >= 0 ? '+' : ''}{formatCurrency(nnaNet)}
                        </div>
                        {nnaNetGrowth !== null && (
                          <>
                            <div className={`text-sm font-semibold mt-2 ${nnaNetGrowth >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                              {nnaNetGrowth >= 0 ? '+' : ''}{formatCurrency(nnaNetGrowth)}
                              {nnaNetGrowthPct !== null && <span className="ml-1">({nnaNetGrowth >= 0 ? '+' : ''}{nnaNetGrowthPct.toFixed(1)}%)</span>}
                            </div>
                            <div className="text-[9px] text-white/40 tracking-widest mt-0.5">{comparisonLabel}</div>
                          </>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Date */}
                  {src.end_date && (
                    <div className="text-[10px] text-white/30 text-center mt-3">
                      as of {new Date((src.end_date as string) + 'T12:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                    </div>
                  )}
                </div>
              )
            })()}

            {/* GRO hero metrics tiles */}
            {panelViewMode === 'gro' && aggregatedGroData.length > 0 && (() => {
              const latest = aggregatedGroData[aggregatedGroData.length - 1]
              const groGrowthLabel = granularity === 'monthly' ? 'MoM' : granularity === 'quarterly' ? 'QoQ' : 'YoY'
              const priorIdx = aggregatedGroData.length - 2
              const prior = priorIdx >= 0 ? aggregatedGroData[priorIdx] : null
              const totalChange = prior ? latest.total - prior.total : null

              return (
                <div className="w-full mt-4 rounded-xl bg-white/5 border border-white/10 px-6 py-4">
                  <div className="flex items-center justify-center gap-2 mb-4">
                    <span className="text-[10px] text-white/50 uppercase tracking-widest font-medium">
                      {latest.label}
                    </span>
                  </div>
                  <div className="flex flex-wrap items-stretch gap-3">
                    <div className="flex-1 min-w-[160px] flex flex-col items-center px-4 py-3 rounded-lg bg-[#8B5CF6]/10 border border-[#8B5CF6]/30">
                      <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2">Market</div>
                      <div className={`text-2xl font-bold ${latest.market >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                        {latest.market >= 0 ? '+' : ''}{formatCurrency(latest.market)}
                      </div>
                    </div>
                    <div className="flex-1 min-w-[160px] flex flex-col items-center px-4 py-3 rounded-lg bg-[#2196F3]/10 border border-[#2196F3]/30">
                      <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2">Net Flows</div>
                      <div className={`text-2xl font-bold ${latest.nna >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                        {latest.nna >= 0 ? '+' : ''}{formatCurrency(latest.nna)}
                      </div>
                    </div>
                    <div className="flex-1 min-w-[160px] flex flex-col items-center px-4 py-3 rounded-lg bg-white/5 border border-white/10">
                      <div className="text-[10px] text-white/60 font-medium uppercase tracking-widest mb-2">Total Change</div>
                      <div className={`text-2xl font-bold ${latest.total >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                        {latest.total >= 0 ? '+' : ''}{formatCurrency(latest.total)}
                      </div>
                      {totalChange !== null && (
                        <>
                          <div className={`text-sm font-semibold mt-2 ${totalChange >= 0 ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                            {totalChange >= 0 ? '+' : ''}{formatCurrency(totalChange)}
                          </div>
                          <div className="text-[9px] text-white/40 tracking-widest mt-0.5">vs {prior!.label} ({groGrowthLabel})</div>
                        </>
                      )}
                    </div>
                  </div>
                  {latest.endDate && (
                    <div className="text-[10px] text-white/30 text-center mt-3">
                      as of {new Date(latest.endDate + 'T12:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                    </div>
                  )}
                </div>
              )
            })()}

            {/* Footnotes */}
            <div className="text-[10px] text-center px-4 mt-4 space-y-1">
              <p>
                {panelViewMode === 'aua' && auaSubMode === 'clients' ? (
                  <>
                    <span className="text-amber-400 font-bold">New Client Assets = Clients onboarded within trailing 12 months.</span>
                    <span className="text-white/40"> Existing Client Assets = Clients onboarded before trailing 12 months. Does not include cash balances.</span>
                  </>
                ) : panelViewMode === 'aua' && auaSubMode === 'mix' ? (
                  <>
                    <span className="text-amber-400 font-bold">Asset class breakdown of total AUA.</span>
                    <span className="text-white/40"> End-of-period snapshots derived from holdings data.</span>
                  </>
                ) : panelViewMode === 'gro' ? (
                  <>
                    <span className="text-amber-400 font-bold">Market = AUA change from market movement. NNA = net new assets from client flows.</span>
                    <span className="text-white/40"> Total = Market + NNA. Values can be negative in down markets or during outflow periods.</span>
                  </>
                ) : hasGrossFlowData ? (
                  <>
                    <span className="text-amber-400 font-bold">Inflows above zero, Outflows below zero — both shown every period.</span>
                    <span className="text-white/40"> The line shows net movement (Inflows - Outflows).</span>
                  </>
                ) : (
                  <>
                    <span className="text-amber-400 font-bold">Net New Assets per period.</span>
                    <span className="text-white/40"> Green = net inflow, Red = net outflow. Gross inflow/outflow breakdown available after next data update.</span>
                  </>
                )}
              </p>
              {panelViewMode !== 'gro' && !(panelViewMode === 'aua' && auaSubMode === 'mix') && (
                <p className="text-white/30 italic">
                  {panelViewMode === 'aua'
                    ? 'Growth metrics compare the same calendar day in the prior period (e.g., Day 24 of Feb vs Day 24 of Jan) for an apples-to-apples snapshot comparison.'
                    : 'Growth metrics compare the same calendar day in the prior period (e.g., cumulative flows through Day 24 of Feb vs Day 24 of Jan). Tooltip period-over-period compares against the full prior period.'}
                </p>
              )}
            </div>
          </div>
        </div>
      </PanelContent>
      <PanelFooter content="Source: SS&C Black Diamond Wealth Solutions." timestamp={data?.generated_at} />
    </Panel>
  )
}

// ============================================================================
// Helper Components (Legacy - kept for reference but no longer used in main UI)
// ============================================================================

interface AUAGrowthMetricsProps {
  data: {
    aua: number
    nna_ytd: number
    q0: { nna: number; growth?: number }
    q1: { nna: number; growth?: number }
    q2: { nna: number; growth?: number }
  }
}

function _AUAGrowthMetrics({ data }: AUAGrowthMetricsProps) {
  const getGrowthDotColor = (growth: number | undefined): string => {
    if (growth === undefined) return 'bg-white/30'
    return growth > 0 ? 'bg-emerald-400' : growth < 0 ? 'bg-red-400' : 'bg-white/30'
  }

  const formatGrowth = (growth: number | undefined): string => {
    if (growth === undefined) return ''
    const sign = growth >= 0 ? '+' : ''
    return `${sign}${growth.toFixed(1)}%`
  }

  const getGrowthColor = (growth: number | undefined): string => {
    if (growth === undefined) return 'text-white/40'
    return growth > 0 ? 'text-emerald-400' : growth < 0 ? 'text-red-400' : 'text-white/40'
  }

  return (
    <div className="w-full h-[72px] px-6 py-3 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center">
      <div className="flex items-center justify-evenly gap-6 w-full">
        {/* Total AUA - Primary metric */}
        <div className="flex flex-col items-center px-4 py-1.5 rounded bg-[hsl(253,74%,85%)]/15 border border-[hsl(253,74%,85%)]/40">
          <div className="text-xs text-white/90 font-semibold mb-1">Total AUA</div>
          <div className="text-lg font-bold text-white">
            {formatCurrency(data.aua)}
          </div>
        </div>

        {/* NNA YTD */}
        <div className="flex flex-col items-center">
          <div className="text-xs text-white/50 mb-1">NNA YTD</div>
          <div className={`text-sm font-semibold ${data.nna_ytd >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
            {data.nna_ytd >= 0 ? '+' : ''}{formatCurrency(data.nna_ytd)}
          </div>
        </div>

        {/* Q0 NNA (This Quarter) */}
        <div className="flex flex-col items-center">
          <div className="flex items-center gap-1.5 mb-1">
            <div className={`w-2 h-2 rounded-full ${getGrowthDotColor(data.q0.growth)}`} />
            <div className="text-xs text-white/50">This Qtr</div>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="text-sm font-semibold text-white">
              {formatCurrency(data.q0.nna)}
            </span>
            {data.q0.growth !== undefined && (
              <span className={`text-xs font-medium ${getGrowthColor(data.q0.growth)}`}>
                {formatGrowth(data.q0.growth)}
              </span>
            )}
          </div>
        </div>

        {/* Q1 NNA (Last Quarter) */}
        <div className="flex flex-col items-center">
          <div className="flex items-center gap-1.5 mb-1">
            <div className={`w-2 h-2 rounded-full ${getGrowthDotColor(data.q1.growth)}`} />
            <div className="text-xs text-white/50">Last Qtr</div>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="text-sm font-semibold text-white">
              {formatCurrency(data.q1.nna)}
            </span>
            {data.q1.growth !== undefined && (
              <span className={`text-xs font-medium ${getGrowthColor(data.q1.growth)}`}>
                {formatGrowth(data.q1.growth)}
              </span>
            )}
          </div>
        </div>

        {/* Q2 NNA (2 Quarters Ago) */}
        <div className="flex flex-col items-center">
          <div className="flex items-center gap-1.5 mb-1">
            <div className={`w-2 h-2 rounded-full ${getGrowthDotColor(data.q2.growth)}`} />
            <div className="text-xs text-white/50">2Q Ago</div>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="text-sm font-semibold text-white">
              {formatCurrency(data.q2.nna)}
            </span>
            {data.q2.growth !== undefined && (
              <span className={`text-xs font-medium ${getGrowthColor(data.q2.growth)}`}>
                {formatGrowth(data.q2.growth)}
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

// ============================================================================
// Time Machine Metrics Component
// ============================================================================

interface TimeMachineMetricsProps {
  view: PartnerAnalyticsViewWithPeriods
  periods?: {
    current: { date: string; label: string }
    q1: { date: string; label: string }
    q2: { date: string; label: string }
    q3: { date: string; label: string }
  }
  selectedPeriod: TimePeriodKey
  onPeriodChange: (period: TimePeriodKey) => void
  parentSegmentKey?: string | null  // State/architect key when drilled down
  parentSegmentLabel?: string | null  // Label for display
  childSegmentKey?: string | null  // City/client key when selected within drill-down
  childSegmentLabel?: string | null  // Label for display
  isNnaView?: boolean  // When true, use 'value' (net flows) instead of 'aua'
}

function _TimeMachineMetrics({ view, periods, selectedPeriod, onPeriodChange, parentSegmentKey, parentSegmentLabel, childSegmentKey, childSegmentLabel, isNnaView = false }: TimeMachineMetricsProps) {
  // Get value for a specific period - always looks up in THAT period's data
  // For NNA view, uses 'value' (net flows); for other views, uses 'aua'
  const getValueForPeriod = (period: TimePeriodKey): number => {
    const snapshot = period === 'current' ? view.current : view[period]

    // If a child segment (city/client) is selected, look it up within the parent
    if (childSegmentKey && parentSegmentKey) {
      const parentInPeriod = snapshot?.donut?.segments?.find(
        (s: DonutSegment) => s.key === parentSegmentKey
      )
      // Look in cities array for GEO drill-down
      if (parentInPeriod?.cities) {
        const cityInPeriod = parentInPeriod.cities.find(
          (c: CitySegment) => c.key === childSegmentKey
        )
        if (cityInPeriod) {
          return cityInPeriod.aua
        }
      }
      // Look in clients array for ADV drill-down
      if (parentInPeriod?.clients) {
        const clientInPeriod = parentInPeriod.clients.find(
          (c: ClientSegment) => c.key === childSegmentKey
        )
        if (clientInPeriod) {
          return clientInPeriod.aua
        }
      }
      return 0
    }

    // If just a parent segment (state/architect/NNA segment) is selected
    if (parentSegmentKey) {
      const segmentInPeriod = snapshot?.donut?.segments?.find(
        (s: DonutSegment) => s.key === parentSegmentKey
      )
      if (segmentInPeriod) {
        // NNA view: use 'value' (net flows), not 'aua'
        if (isNnaView && segmentInPeriod.value !== undefined) {
          return segmentInPeriod.value
        }
        return segmentInPeriod.aua
      }
      return 0
    }

    // Total level
    // NNA view at total level also uses the donut total (which is net NNA)
    return snapshot?.metrics?.aua || snapshot?.donut?.total || 0
  }

  // Get % change for a historical period (compared to current)
  const getChangeForPeriod = (period: TimePeriodKey): number | undefined => {
    if (period === 'current') return undefined
    const snapshot = view[period]
    return snapshot?.metrics?.aua_change_pct
  }

  // Check if a period has data
  const hasPeriodData = (period: TimePeriodKey): boolean => {
    if (period === 'current') return !!view.current
    return !!view[period]
  }

  // Check if viewing estimated data
  const _isEstimated = (period: TimePeriodKey): boolean => {
    if (period === 'current') return false
    const snapshot = view[period]
    return (snapshot?.metrics as { estimated?: boolean })?.estimated === true
  }

  // Format change percentage
  const formatChange = (change: number | undefined): string => {
    if (change === undefined) return ''
    const sign = change >= 0 ? '+' : ''
    return `${sign}${change.toFixed(1)}%`
  }

  // Get change color
  const getChangeColor = (change: number | undefined): string => {
    if (change === undefined) return 'text-white/40'
    return change > 0 ? 'text-emerald-400' : change < 0 ? 'text-red-400' : 'text-white/40'
  }

  // Period configurations - show most specific label (child > parent > total)
  // NNA view spells out "Net New Assets" instead of abbreviating
  const metricLabel = (() => {
    const baseLabel = childSegmentLabel || parentSegmentLabel || 'Total'
    if (isNnaView) {
      // Replace "NNA" suffix with full "Net New Assets" if present
      if (baseLabel.endsWith('NNA')) {
        return baseLabel.replace(/NNA$/, 'Net New Assets')
      }
      return `${baseLabel} Net New Assets`
    }
    return `${baseLabel} AUA`
  })()

  const periodConfigs: { key: TimePeriodKey; label: string; subLabel?: string }[] = [
    { key: 'current', label: 'Current', subLabel: metricLabel },
    { key: 'q1', label: periods?.q1?.label || 'Last Qtr' },
    { key: 'q2', label: periods?.q2?.label || '2Q Ago' },
    { key: 'q3', label: periods?.q3?.label || '3Q Ago' },
  ]

  return (
    <div className="w-full h-[72px] px-6 py-3 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center">
      <div className="flex items-center justify-evenly gap-6 w-full">
        {periodConfigs.map(({ key, label, subLabel }) => {
          const isSelected = selectedPeriod === key
          const hasData = hasPeriodData(key)
          const aua = getValueForPeriod(key)
          const change = getChangeForPeriod(key)

          if (!hasData && key !== 'current') {
            return null  // Don't show periods without data
          }

          // Current period gets special "Total AUA" styling to match canonical
          const isCurrent = key === 'current'

          return (
            <button
              key={key}
              onClick={() => onPeriodChange(key)}
              disabled={!hasData}
              className={`flex flex-col items-center px-3 py-1.5 rounded-lg transition-all ${
                isSelected
                  ? 'bg-[hsl(253,74%,85%)]/15 border border-[hsl(253,74%,85%)]/40'
                  : hasData
                  ? 'hover:bg-white/10 border border-transparent'
                  : 'opacity-40 cursor-not-allowed border border-transparent'
              }`}
            >
              {/* Period label */}
              <div className="flex items-center gap-1.5 mb-0.5">
                <span className={`text-xs ${isSelected ? 'text-white/90 font-semibold' : 'text-white/60 font-medium'}`}>
                  {isCurrent ? (subLabel || label) : label}
                </span>
              </div>

              {/* AUA value */}
              <div className="flex items-center gap-1.5">
                <span className={`font-bold ${isSelected ? 'text-lg text-white' : 'text-sm text-white/80'}`}>
                  {formatCurrency(aua)}
                </span>
                {change !== undefined && (
                  <span className={`text-xs font-medium ${getChangeColor(change)}`}>
                    {formatChange(change)}
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
// Client Distribution Chart Component
// ============================================================================

interface ClientDistributionChartProps {
  data: DistributionStats
  accentColor?: string
  globalMaxCount?: number  // Fixed Y-axis max for consistent scaling across segments
}

function ClientDistributionChart({ data, accentColor = '#5e72e4', globalMaxCount }: ClientDistributionChartProps) {
  const chartData = data.histogram.bin_labels.map((label, index) => ({
    bin: label,
    count: data.histogram.counts[index],
    binIndex: index,
  }))

  const parseDollarValue = (binLabel: string): number => {
    if (binLabel.includes('+')) {
      const match = binLabel.match(/\$([\d.]+)([KMB]?)\+/)
      if (match) {
        const num = parseFloat(match[1])
        const multiplier = match[2] === 'K' ? 1000 : match[2] === 'M' ? 1000000 : match[2] === 'B' ? 1000000000 : 1
        return num * multiplier
      }
    }
    const parts = binLabel.split('-')
    if (parts.length === 2) {
      const parseValue = (str: string): number => {
        const match = str.match(/\$([\d.]+)([KMB]?)/)
        if (match) {
          const num = parseFloat(match[1])
          const multiplier = match[2] === 'K' ? 1000 : match[2] === 'M' ? 1000000 : match[2] === 'B' ? 1000000000 : 1
          return num * multiplier
        }
        return 0
      }
      return (parseValue(parts[0]) + parseValue(parts[1])) / 2
    }
    return 0
  }

  const findBinForValue = (value: number | null): string | null => {
    if (value === null) return null
    let closestBin = null
    let minDiff = Infinity
    for (const binLabel of data.histogram.bin_labels) {
      const binMidpoint = parseDollarValue(binLabel)
      const diff = Math.abs(binMidpoint - value)
      if (diff < minDiff) {
        minDiff = diff
        closestBin = binLabel
      }
    }
    return closestBin
  }

  const percentileLines = [
    { value: data.percentiles.p10, label: 'P10', color: '#ef4444' },
    { value: data.percentiles.p25, label: 'P25', color: '#fb923c' },
    { value: data.median, label: 'Median', color: '#34d399' },
    { value: data.percentiles.p75, label: 'P75', color: '#60a5fa' },
    { value: data.percentiles.p90, label: 'P90', color: '#a78bfa' },
  ]

  useEffect(() => {
    const timer = setTimeout(() => window.dispatchEvent(new Event('resize')), 100)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="w-full h-full relative">
      <div className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-2">
        <span className="text-[11px] text-white/50 whitespace-nowrap" style={{ writingMode: 'vertical-rl', transform: 'rotate(180deg)' }}>
          Number of Clients
        </span>
      </div>
      <div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-4">
        <span className="text-[11px] text-white/50">Client AUA</span>
      </div>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={chartData} margin={{ top: 30, right: 10, left: 0, bottom: 5 }}>
          <defs>
            <linearGradient id="distributionGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={accentColor} stopOpacity={0.8} />
              <stop offset="95%" stopColor={accentColor} stopOpacity={0.1} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
          <XAxis dataKey="bin" stroke="rgba(255,255,255,0.5)" tick={{ fontSize: 7, fill: 'rgba(255,255,255,0.7)' }} angle={-65} textAnchor="end" height={50} interval={0} />
          <YAxis
                            stroke="rgba(255,255,255,0.5)"
                            tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.7)' }}
                            width={40}
                            domain={globalMaxCount ? [0, globalMaxCount] : ['auto', 'auto']}
                            allowDataOverflow={false}
                          />
          <RechartsTooltip
            cursor={{ stroke: `${accentColor}80`, strokeWidth: 2 }}
            content={({ active, payload, label }) => {
              if (!active || !payload || payload.length === 0) return null
              const count = payload[0]?.value as number
              const formattedLabel = typeof label === 'string' ? label.replace(/(\$[\d.]+[KMB]?)-(\$[\d.]+[KMB]?\+?)/, '$1 - $2') : label
              return (
                <div className="bg-[hsl(var(--semantic-background-chartTooltipBg))] rounded-lg px-4 py-3 shadow-xl" style={{ border: `2px solid ${accentColor}` }}>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between gap-4">
                      <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm">Client AUA</span>
                      <span className="text-[hsl(var(--semantic-text-chartTooltip))] font-semibold text-sm">{formattedLabel}</span>
                    </div>
                    <div className="flex items-center justify-between gap-4">
                      <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm">Client Count</span>
                      <span className="text-[hsl(var(--semantic-text-chartTooltip))] font-semibold text-sm">{count?.toLocaleString()}</span>
                    </div>
                  </div>
                </div>
              )
            }}
          />
          <Area type="monotone" dataKey="count" stroke="hsl(253, 74%, 85%)" strokeWidth={2} fill="url(#distributionGradient)" isAnimationActive={true} animationDuration={800} />
          {percentileLines.map((line) => {
            const binLabel = findBinForValue(line.value)
            if (!binLabel) return null
            return (
              <ReferenceLine key={line.label} x={binLabel} stroke={line.color} strokeWidth={2} strokeDasharray="5 5" label={{ value: line.label, position: 'top', fill: line.color, fontSize: 10, fontWeight: 600 }} />
            )
          })}
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}

// ============================================================================
// Client Distribution Metrics Component
// ============================================================================

interface ClientDistributionMetricsProps {
  data: DistributionStats
}

function ClientDistributionMetrics({ data }: ClientDistributionMetricsProps) {
  return (
    <div className="w-full h-[72px] px-6 py-3 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center">
      <div className="flex items-center justify-evenly gap-4 w-full">
        {/* Total Clients */}
        <div className="flex flex-col items-center px-4 py-1.5 rounded bg-[hsl(253,74%,85%)]/15 border border-[hsl(253,74%,85%)]/40">
          <div className="text-xs text-white/90 font-semibold mb-1">Total Clients</div>
          <div className="text-lg font-bold text-white">{data.count.toLocaleString()}</div>
        </div>

        {/* P10 */}
        <div className="flex flex-col items-center">
          <div className="flex items-center gap-1.5 mb-1">
            <div className="w-2 h-2 rounded-full bg-red-500" />
            <div className="text-xs text-white/50">P10</div>
          </div>
          <div className="text-sm font-semibold text-white">{data.percentiles.p10 !== null ? formatCurrency(data.percentiles.p10) : 'N/A'}</div>
        </div>

        {/* P25 */}
        <div className="flex flex-col items-center">
          <div className="flex items-center gap-1.5 mb-1">
            <div className="w-2 h-2 rounded-full bg-orange-400" />
            <div className="text-xs text-white/50">P25</div>
          </div>
          <div className="text-sm font-semibold text-white">{data.percentiles.p25 !== null ? formatCurrency(data.percentiles.p25) : 'N/A'}</div>
        </div>

        {/* Median */}
        <div className="flex flex-col items-center px-3 py-1.5 rounded bg-emerald-500/10 border border-emerald-500/30">
          <div className="flex items-center gap-1.5 mb-1">
            <div className="w-2 h-2 rounded-full bg-emerald-400" />
            <div className="text-xs text-emerald-300/80 font-semibold">Median</div>
          </div>
          <div className="text-base font-bold text-emerald-400">{data.median !== null ? formatCurrency(data.median) : 'N/A'}</div>
        </div>

        {/* Mean */}
        <div className="flex flex-col items-center">
          <div className="text-xs text-white/50 mb-1">Mean</div>
          <div className="text-sm font-semibold text-white">{data.mean !== null ? formatCurrency(data.mean) : 'N/A'}</div>
        </div>

        {/* P75 */}
        <div className="flex flex-col items-center">
          <div className="flex items-center gap-1.5 mb-1">
            <div className="w-2 h-2 rounded-full bg-blue-400" />
            <div className="text-xs text-white/50">P75</div>
          </div>
          <div className="text-sm font-semibold text-white">{data.percentiles.p75 !== null ? formatCurrency(data.percentiles.p75) : 'N/A'}</div>
        </div>

        {/* P90 */}
        <div className="flex flex-col items-center">
          <div className="flex items-center gap-1.5 mb-1">
            <div className="w-2 h-2 rounded-full bg-purple-400" />
            <div className="text-xs text-white/50">P90</div>
          </div>
          <div className="text-sm font-semibold text-white">{data.percentiles.p90 !== null ? formatCurrency(data.percentiles.p90) : 'N/A'}</div>
        </div>
      </div>
    </div>
  )
}
