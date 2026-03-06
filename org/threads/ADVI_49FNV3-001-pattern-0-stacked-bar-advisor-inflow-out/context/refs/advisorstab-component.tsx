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

import { useState, useEffect } from 'react'
import { useMemo } from 'react'
import {
  ComposedChart,
  Bar,
  Line as RechartsLine,
  ReferenceLine,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts'
import { Panel, PanelHeader, PanelContent } from '@/ui/components/panels'
import { LoadingInline } from '@/components/LoadingSpinner'
import {
  ArrowUpRight,
  ArrowDownRight,
  ChevronUp,
  ChevronDown,
  Trophy,
  TrendingUp,
  Search,
} from 'lucide-react'
import { formatCurrency, formatNumberTo3Digits } from '@/lib/universalNumberFormatter'
import { getArchitectLeaderboard, getImplementorLeaderboard, getAdvisorRollingFlows } from '@/api/endpoints/advisor-intelligence'
import type {
  LeaderboardResponse,
  LeaderboardEntry,
  ChartWindowOption,
  AdvisorRollingFlowsResponseV2,
  StackedBarPeriodKey,
} from '../types'

// ============================================================================
// ROLLING FLOWS INTERVAL (Y13)
// ============================================================================

type RollingFlowsInterval = 'month' | 'quarter' | 'year'

const ROLLING_FLOWS_INTERVAL_OPTIONS: { value: RollingFlowsInterval; label: string }[] = [
  { value: 'month', label: 'Month' },
  { value: 'quarter', label: 'Quarter' },
  { value: 'year', label: 'Year' },
]

// ============================================================================
// TYPES & CONSTANTS
// ============================================================================

type AdvisorRole = 'architects' | 'implementors'
type SortField = 'name' | 'total_aua' | 'nna' | 'aua_growth_pct' | 'new_clients'
type SortDirection = 'asc' | 'desc'
// Firm house account — excluded from individual rankings, shown separately in leaderboard
const FIRM_ACCOUNT_NAME = '49F House'

const LEADERBOARD_WINDOW_OPTIONS: { value: ChartWindowOption; label: string }[] = [
  { value: '3M', label: '3M' },
  { value: '6M', label: '6M' },
  { value: '1Y', label: '1Y' },
  { value: '2Y', label: '2Y' },
  { value: '3Y', label: '3Y' },
]

// Shared period toggle — controls Top Performers, Rolling Flows, and Leaderboard
const PERIOD_OPTIONS: { value: StackedBarPeriodKey; label: string }[] = [
  { value: 'qtd', label: 'QTD' },
  { value: 'ytd', label: 'YTD' },
  { value: '1y', label: '1Y' },
  { value: 'max', label: 'Max' },
]

// Map the shared period to the leaderboard's ChartWindowOption key space
function periodToChartWindow(p: StackedBarPeriodKey): ChartWindowOption {
  if (p === 'qtd') return '3M'
  if (p === 'max' || p === '3y') return '3Y'
  return '1Y' // ytd, 1y
}

// variant="primary" — view/role toggles: bg-[hsl(var(--primary))] active, px-2.5 py-1
// variant="secondary" — period/window toggles: bg-white/20 active, px-2 py-1
function ToggleGroup<T extends string>({ options, value, onChange, variant = 'secondary' }: {
  options: { value: T; label: string }[]
  value: T
  onChange: (v: T) => void
  variant?: 'primary' | 'secondary'
}) {
  const padding = variant === 'primary' ? 'px-2.5 py-1' : 'px-2 py-1'
  const activeClass = variant === 'primary'
    ? 'bg-[hsl(var(--primary))] text-white'
    : 'bg-white/20 text-white'
  const inactiveClass = variant === 'primary'
    ? 'text-white/60 hover:text-white hover:bg-white/10'
    : 'text-white/50 hover:text-white hover:bg-white/10'
  return (
    <div className="flex gap-0.5 bg-white/10 rounded-lg p-0.5">
      {options.map((opt) => (
        <button
          key={opt.value}
          onClick={() => onChange(opt.value)}
          className={`${padding} text-xs font-medium rounded-md transition-colors ${
            value === opt.value ? activeClass : inactiveClass
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
  const [flowsData, setFlowsData] = useState<AdvisorRollingFlowsResponseV2 | null>(null)
  const [flowsLoading, setFlowsLoading] = useState(true)

  // Tab-wide toggle: architects or implementors
  const [role, setRole] = useState<AdvisorRole>('architects')

  // Shared period — owned by Top Performers, drives all three panels
  const [period, setPeriod] = useState<StackedBarPeriodKey>('ytd')

  // Rolling Flows interval (Y13: Month/Quarter/Year replaces old period toggle for this panel)
  const [rollingFlowsInterval, setRollingFlowsInterval] = useState<RollingFlowsInterval>('month')

  // Leaderboard
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
        // no selection state to update
      })
      .catch(error => {
        console.error('[AdvisorsTab] Rolling flows not available:', error)
        setFlowsData(null)
        setFlowsLoading(false)
      })
  }, [firmId]) // eslint-disable-line react-hooks/exhaustive-deps

  // Active leaderboard data based on role toggle
  const activeLeaderboard = role === 'architects' ? architectData : implementorData

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
    <div className="flex flex-col gap-4">

      {/* Panel 1: Top Performers — owns the Architects/Implementors toggle */}
      <Panel variant="chart">
        <PanelHeader
          title="Top Performers"
          actions={
            <div className="flex items-center gap-3">
              <div className="flex gap-0.5 bg-white/10 rounded-lg p-0.5">
                {(['architects', 'implementors'] as AdvisorRole[]).map((r) => (
                  <button
                    key={r}
                    onClick={() => { setRole(r); setSearchQuery('') }}
                    className={`px-2.5 py-1 text-xs font-medium rounded-md transition-colors ${
                      role === r
                        ? 'bg-[hsl(var(--primary))] text-white'
                        : 'text-white/60 hover:text-white hover:bg-white/10'
                    }`}
                  >
                    {r.charAt(0).toUpperCase() + r.slice(1)}
                  </button>
                ))}
              </div>
              <div className="w-px h-5 bg-white/10" />
              <ToggleGroup options={PERIOD_OPTIONS} value={period} onChange={setPeriod} variant="secondary" />
              <div className="w-px h-5 bg-white/10" />
              <div className="flex items-center gap-2">
                <Trophy size={14} className="text-amber-400" />
                <span className="text-[10px] text-white/40">
                  {activeLeaderboard?.windows?.[periodToChartWindow(period)]?.entry_count ?? 0} {role}
                </span>
              </div>
            </div>
          }
        />
        <PanelContent noPadding>
          <Top3Highlights data={activeLeaderboard} window={periodToChartWindow(period)} role={role} />
        </PanelContent>
      </Panel>

      {/* Panel 2: Rolling Flows — per-period diverging bar (Y13: replaces per-advisor stacked bar) */}
      <Panel variant="chart">
        <PanelHeader
          title="Rolling Flows"
          actions={
            <ToggleGroup
              options={ROLLING_FLOWS_INTERVAL_OPTIONS}
              value={rollingFlowsInterval}
              onChange={setRollingFlowsInterval}
              variant="secondary"
            />
          }
        />
        <PanelContent noPadding>
          {flowsLoading ? (
            <LoadingInline className="py-12" />
          ) : flowsData?.monthly ? (
            <RollingFlowsDivergingBar
              data={flowsData}
              interval={rollingFlowsInterval}
            />
          ) : (
            <div className="flex items-center justify-center h-[280px]">
              <p className="text-sm text-white/40">Monthly flows data not yet available</p>
            </div>
          )}
        </PanelContent>
      </Panel>

      {/* Panel 3: Leaderboard — role controlled by Top Performers toggle */}
      <Panel variant="chart">
        <PanelHeader
          title={`${role === 'architects' ? 'Architect' : 'Implementor'} Leaderboard`}
          actions={
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
          }
        />
        <PanelContent noPadding>
          <LeaderboardTable
            data={activeLeaderboard?.windows?.[periodToChartWindow(period)]?.entries ?? []}
            searchQuery={searchQuery}
          />
        </PanelContent>
      </Panel>

    </div>
  )
}

// ============================================================================
// ROLLING FLOWS DIVERGING BAR (Y13 — per-period aggregate, replaces per-advisor stacked bar)
// ============================================================================

interface RollingFlowsDivergingBarProps {
  data: AdvisorRollingFlowsResponseV2
  interval: RollingFlowsInterval
}

interface PeriodAggregate {
  label: string
  sortKey: string
  inflows: number
  outflowsNeg: number
  nna: number
}

/** Format "YYYY-MM" to short month label */
function formatMonthLabel(key: string): string {
  const [y, m] = key.split('-')
  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
  const mi = parseInt(m, 10) - 1
  return `${months[mi] ?? m} ${y}`
}

/** Get quarter from "YYYY-MM" */
function getQuarterKey(key: string): string {
  const [y, m] = key.split('-')
  const q = Math.ceil(parseInt(m, 10) / 3)
  return `${y}-Q${q}`
}

function formatQuarterLabel(qKey: string): string {
  const [y, q] = qKey.split('-')
  return `${q} ${y}`
}

function RollingFlowsDivergingBar({ data, interval }: RollingFlowsDivergingBarProps) {
  const chartData = useMemo<PeriodAggregate[]>(() => {
    const monthly = data.monthly
    if (!monthly) return []

    // Step 1: aggregate each monthly key into {inflows, outflows, nna}
    const monthAggs: Record<string, { inflows: number; outflows: number; nna: number }> = {}
    for (const [monthKey, entries] of Object.entries(monthly)) {
      let inf = 0, out = 0
      for (const e of entries) {
        inf += e.inflows
        out += e.outflows
      }
      monthAggs[monthKey] = { inflows: inf, outflows: out, nna: inf - out }
    }

    // Step 2: bucket by interval
    if (interval === 'month') {
      return Object.entries(monthAggs)
        .map(([k, v]) => ({
          label: formatMonthLabel(k),
          sortKey: k,
          inflows: v.inflows,
          outflowsNeg: -v.outflows,
          nna: v.nna,
        }))
        .sort((a, b) => a.sortKey.localeCompare(b.sortKey))
    }

    if (interval === 'quarter') {
      const qMap: Record<string, { inflows: number; outflows: number; nna: number }> = {}
      for (const [k, v] of Object.entries(monthAggs)) {
        const qk = getQuarterKey(k)
        if (!qMap[qk]) qMap[qk] = { inflows: 0, outflows: 0, nna: 0 }
        qMap[qk].inflows += v.inflows
        qMap[qk].outflows += v.outflows
        qMap[qk].nna += v.nna
      }
      return Object.entries(qMap)
        .map(([k, v]) => ({
          label: formatQuarterLabel(k),
          sortKey: k,
          inflows: v.inflows,
          outflowsNeg: -v.outflows,
          nna: v.nna,
        }))
        .sort((a, b) => a.sortKey.localeCompare(b.sortKey))
    }

    // year
    const yMap: Record<string, { inflows: number; outflows: number; nna: number }> = {}
    for (const [k, v] of Object.entries(monthAggs)) {
      const yr = k.split('-')[0]
      if (!yMap[yr]) yMap[yr] = { inflows: 0, outflows: 0, nna: 0 }
      yMap[yr].inflows += v.inflows
      yMap[yr].outflows += v.outflows
      yMap[yr].nna += v.nna
    }
    return Object.entries(yMap)
      .map(([k, v]) => ({
        label: k,
        sortKey: k,
        inflows: v.inflows,
        outflowsNeg: -v.outflows,
        nna: v.nna,
      }))
      .sort((a, b) => a.sortKey.localeCompare(b.sortKey))
  }, [data.monthly, interval])

  if (chartData.length === 0) {
    return (
      <div className="flex items-center justify-center h-[280px]">
        <p className="text-sm text-white/40">No data for this interval</p>
      </div>
    )
  }

  return (
    <div className="flex flex-col">
      <div className="p-4 h-[380px]">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart
            data={chartData}
            stackOffset="sign"
            margin={{ top: 10, right: 10, left: 10, bottom: 10 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
            <XAxis
              dataKey="label"
              tick={{ fill: 'rgba(255,255,255,0.4)', fontSize: 10 }}
              axisLine={{ stroke: 'rgba(255,255,255,0.1)' }}
              tickLine={false}
              angle={interval === 'month' ? -45 : 0}
              textAnchor={interval === 'month' ? 'end' : 'middle'}
              interval={0}
              height={interval === 'month' ? 70 : 40}
            />
            <YAxis
              tickFormatter={(v: number) => formatNumberTo3Digits(v, { unit: '$', includeSign: false })}
              tick={{ fill: 'rgba(255,255,255,0.4)', fontSize: 10 }}
              axisLine={false}
              tickLine={false}
              width={65}
            />
            <ReferenceLine y={0} stroke="rgba(255,255,255,0.25)" strokeWidth={1} />
            <Tooltip
              wrapperStyle={{ zIndex: 40 }}
              cursor={{ fill: 'rgba(255,255,255,0.04)' }}
              content={(props) => {
                const payload = props.payload as Array<{ payload: PeriodAggregate }> | undefined
                if (!payload?.length) return null
                const row = payload[0].payload
                const nnaColor = row.nna >= 0 ? '#16A34A' : '#EC4899'
                return (
                  <div className="bg-[#0f1729] border-2 border-white/10 rounded-lg px-4 py-3 shadow-xl">
                    <div className="text-white font-bold text-sm mb-2">{row.label}</div>
                    <div className="space-y-1.5">
                      <div className="flex items-center justify-between gap-6 text-xs">
                        <div className="flex items-center gap-2">
                          <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: '#2563EB' }} />
                          <span className="text-white/70">Inflows</span>
                        </div>
                        <span className="text-white font-medium">{formatCurrency(row.inflows)}</span>
                      </div>
                      <div className="flex items-center justify-between gap-6 text-xs">
                        <div className="flex items-center gap-2">
                          <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: '#DC2626' }} />
                          <span className="text-white/70">Outflows</span>
                        </div>
                        <span className="text-white font-medium">{formatCurrency(Math.abs(row.outflowsNeg))}</span>
                      </div>
                      <div className="flex items-center justify-between gap-6 text-xs border-t border-white/10 pt-1.5 mt-1">
                        <div className="flex items-center gap-2">
                          <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: nnaColor }} />
                          <span className="text-white/70">NNA</span>
                        </div>
                        <span className="font-semibold" style={{ color: nnaColor }}>
                          {row.nna >= 0 ? '+' : ''}{formatCurrency(row.nna)}
                        </span>
                      </div>
                    </div>
                  </div>
                )
              }}
            />
            {/* Inflows: blue, extends above zero */}
            <Bar dataKey="inflows" stackId="nna" fill="#2563EB" fillOpacity={0.8} />
            {/* Outflows: red, extends below zero */}
            <Bar dataKey="outflowsNeg" stackId="nna" fill="#DC2626" fillOpacity={0.8} />
            {/* Net NNA line — actual NNA value (not midpoint) */}
            <RechartsLine
              dataKey="nna"
              type="monotone"
              stroke="#F59E0B"
              strokeWidth={2}
              dot={{ r: 3, fill: '#F59E0B', stroke: '#F59E0B' }}
              activeDot={{ r: 5, fill: '#F59E0B' }}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      {/* Legend */}
      <div className="flex items-center justify-center gap-5 pb-4 pt-1">
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded-sm bg-[#2563EB]" />
          <span className="text-[10px] text-white/50">Inflows</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded-sm bg-[#DC2626]" />
          <span className="text-[10px] text-white/50">Outflows</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-2.5 h-0.5 bg-[#F59E0B] rounded-full" />
          <span className="text-[10px] text-white/50">Net NNA</span>
        </div>
      </div>
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
  const top3 = data?.windows?.[window]?.entries
    ?.filter(e => e.name !== FIRM_ACCOUNT_NAME)
    .slice(0, 3) ?? []

  if (top3.length === 0) return null

  const rankStyles: Record<number, {
    bg: string; border: string
    badgeBg: string; badgeBorder: string; badgeText: string
  }> = {
    1: {
      bg: 'bg-gradient-to-b from-amber-500/15 to-amber-500/5',
      border: 'border-amber-500/40',
      badgeBg: 'bg-amber-500/25',
      badgeBorder: 'border-amber-500/60',
      badgeText: 'text-amber-400',
    },
    2: {
      bg: 'bg-gradient-to-b from-slate-400/10 to-slate-400/5',
      border: 'border-slate-400/30',
      badgeBg: 'bg-slate-400/20',
      badgeBorder: 'border-slate-400/50',
      badgeText: 'text-slate-300',
    },
    3: {
      bg: 'bg-gradient-to-b from-orange-600/10 to-orange-600/5',
      border: 'border-orange-600/30',
      badgeBg: 'bg-orange-600/20',
      badgeBorder: 'border-orange-600/50',
      badgeText: 'text-orange-400',
    },
  }

  return (
    <div className="p-4">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {top3.map((entry, idx) => {
                const rank = idx + 1
                const style = rankStyles[rank] || rankStyles[3]

                return (
                  <div
                    key={entry.name}
                    className={`rounded-xl border ${style.border} ${style.bg} p-5 flex flex-col gap-3 transition-all hover:scale-[1.01]`}
                  >
                    {/* Rank badge row */}
                    <div className="flex items-center justify-between">
                      <div className={`w-10 h-10 rounded-full ${style.badgeBg} border-2 ${style.badgeBorder} flex items-center justify-center flex-shrink-0`}>
                        <span className={`text-lg font-black ${style.badgeText}`}>{rank}</span>
                      </div>
                      {rank === 1 && <Trophy size={16} className="text-amber-400/70" />}
                    </div>

                    {/* Advisor name */}
                    <h4 className="text-base font-bold text-white leading-tight truncate">
                      {entry.name}
                    </h4>

                    {/* NNA hero metric */}
                    <div>
                      <p className={`text-2xl font-black ${entry.nna >= 0 ? 'text-[hsl(var(--success))]' : 'text-[hsl(var(--destructive))]'}`}>
                        {entry.nna >= 0 ? '+' : ''}{formatNumberTo3Digits(entry.nna, { unit: '$', includeSign: false })}
                      </p>
                      <p className="text-[10px] text-white/40 uppercase tracking-wide mt-0.5">Net New Assets</p>
                    </div>

                    {/* Secondary metrics */}
                    <div className="flex items-center gap-4 pt-2 border-t border-white/10">
                      <div className="flex items-center gap-1">
                        {entry.aua_growth_pct >= 0 ? (
                          <TrendingUp size={11} className="text-[hsl(var(--success))]" />
                        ) : (
                          <ArrowDownRight size={11} className="text-[hsl(var(--destructive))]" />
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
                )
              })}
      </div>
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
}

function LeaderboardTable({ data, searchQuery }: LeaderboardTableProps) {
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

  // Separate firm house account from individual advisors
  const firmEntry = data.find(e => e.name === FIRM_ACCOUNT_NAME)
  const individualData = data.filter(e => e.name !== FIRM_ACCOUNT_NAME)

  // Filter individuals by search; show firm entry if search matches or no search active
  const filteredData = searchQuery.trim()
    ? individualData.filter(entry => entry.name.toLowerCase().includes(searchQuery.toLowerCase()))
    : individualData
  const showFirmEntry = !!firmEntry && (
    !searchQuery.trim() || firmEntry.name.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const sortedData = [...filteredData].sort((a, b) => {
    const aVal = a[sortField]
    const bVal = b[sortField]
    let cmp = 0
    if (typeof aVal === 'string' && typeof bVal === 'string') {
      cmp = sortDirection === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal)
    } else {
      cmp = sortDirection === 'asc' ? Number(aVal) - Number(bVal) : Number(bVal) - Number(aVal)
    }
    // Stable secondary sort: name as tiebreaker for equal numeric values
    if (cmp === 0 && sortField !== 'name') {
      cmp = a.name.localeCompare(b.name)
    }
    return cmp
  }).map((item, idx) => ({ ...item, rank: idx + 1 }))

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
            return (
              <tr
                key={entry.name}
                className="border-b border-white/5 hover:bg-white/5 transition-colors"
              >
                <td className="w-10 px-2 py-2">
                  <RankBadge rank={entry.rank} />
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
          {/* Firm house account — shown below ranked advisors, not included in rankings */}
          {showFirmEntry && firmEntry && (
            <>
              <tr>
                <td colSpan={6} className="px-2 pt-3 pb-0.5 border-t border-white/10">
                  <span className="text-[9px] text-white/25 uppercase tracking-widest font-semibold">Firm Account</span>
                </td>
              </tr>
              <tr className="border-b border-white/5 bg-white/[0.015]">
                <td className="w-10 px-2 py-2">
                  <span className="inline-flex items-center justify-center w-5 h-5 rounded-full text-[8px] font-bold border border-white/10 bg-white/5 text-white/30">
                    --
                  </span>
                </td>
                <td className="w-[28%] px-2 py-2">
                  <span className="font-medium text-white/50 truncate block">{firmEntry.name}</span>
                </td>
                <td className="w-[18%] px-2 py-2 text-right text-white/40">
                  {formatCurrency(firmEntry.total_aua)}
                </td>
                <td className="w-[18%] px-2 py-2 text-right">
                  <span className={`${firmEntry.nna >= 0 ? 'text-[hsl(var(--success))]' : 'text-[hsl(var(--destructive))]'} opacity-50`}>
                    {firmEntry.nna >= 0 ? '+' : ''}{formatNumberTo3Digits(firmEntry.nna, { unit: '$', includeSign: false })}
                  </span>
                </td>
                <td className="w-[16%] px-2 py-2 text-right text-white/40">
                  <span>
                    {firmEntry.aua_growth_pct >= 0 ? '+' : ''}{firmEntry.aua_growth_pct.toFixed(1)}%
                  </span>
                </td>
                <td className="w-[10%] px-2 py-2 text-right text-white/40">
                  {firmEntry.new_clients}
                </td>
              </tr>
            </>
          )}
        </tbody>
      </table>
      {searchQuery && sortedData.length === 0 && !showFirmEntry && (
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
