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
