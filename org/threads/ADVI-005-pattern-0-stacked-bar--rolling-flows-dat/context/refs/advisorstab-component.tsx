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
