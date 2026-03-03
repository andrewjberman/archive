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
