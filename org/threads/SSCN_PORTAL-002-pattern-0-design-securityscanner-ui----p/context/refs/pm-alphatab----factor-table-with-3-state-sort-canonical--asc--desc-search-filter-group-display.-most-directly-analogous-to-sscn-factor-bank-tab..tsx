/**
 * Alpha Tab - Factor Attribution
 *
 * Shows how much alpha each factor contributes to the portfolio
 * Features:
 * - Total Alpha summary (separated from factors)
 * - Filter by factor group (size, growth, value, etc.)
 * - Search by factor name
 * - Sortable columns
 * - Color-coded Trade column
 */

import React, { useState, useMemo } from 'react'
import { Search, HelpCircle } from 'lucide-react'
import { Panel } from '@/ui/components/panels/Panel'
import { PanelHeader } from '@/ui/components/panels/PanelHeader'
import { PanelContent } from '@/ui/components/panels/PanelContent'
import { Tooltip } from '@/components/Tooltip'
import type { AlphaFactor } from '@/types/portfolio-optimization'
import { FACTOR_DESCRIPTIONS } from '../utils/factorDescriptions'
import { canonicalGroupIndex } from '../utils/factorOrder'

interface AlphaTabProps {
  alphaFactors: AlphaFactor[]
}

export function AlphaTab({ alphaFactors }: AlphaTabProps) {
  const [viewMode, setViewMode] = useState<'factor' | 'group'>('factor')
  const [searchQuery, setSearchQuery] = useState('')
  const [groupFilter, setGroupFilter] = useState<string>('all')
  // 3-state sort: 'default' (Yang's canonical order) → 'desc' → 'asc' → 'default'
  const [sortColumn, setSortColumn] = useState<keyof AlphaFactor | null>(null)
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc')

  // Separate Total Alpha from individual factors
  const totalAlpha = useMemo(() => {
    return alphaFactors.find(f => f.factor === 'alpha' || f.name === 'Total Alpha')
  }, [alphaFactors])

  const individualFactors = useMemo(() => {
    return alphaFactors.filter(f => f.factor !== 'alpha' && f.name !== 'Total Alpha')
  }, [alphaFactors])

  // Get unique groups for filter dropdown
  const groups = useMemo(() => {
    const uniqueGroups = new Set(individualFactors.map(f => f.group).filter(g => g !== '-'))
    return ['all', ...Array.from(uniqueGroups).sort()]
  }, [individualFactors])

  // Aggregate individual factors by group for By Group view
  const groupedFactors = useMemo(() => {
    const map = new Map<string, { group: string; initial: number; optimized: number; benchmark: number; trade: number; initialBet: number; optimizedBet: number }>()
    for (const f of individualFactors) {
      const key = f.group || '—'
      const existing = map.get(key)
      if (existing) {
        existing.initial += f.initial ?? 0
        existing.optimized += f.optimized ?? 0
        existing.benchmark += f.benchmark ?? 0
        existing.trade += f.trade ?? 0
        existing.initialBet += f.initialBet ?? 0
        existing.optimizedBet += f.optimizedBet ?? 0
      } else {
        map.set(key, {
          group: key,
          initial: f.initial ?? 0,
          optimized: f.optimized ?? 0,
          benchmark: f.benchmark ?? 0,
          trade: f.trade ?? 0,
          initialBet: f.initialBet ?? 0,
          optimizedBet: f.optimizedBet ?? 0,
        })
      }
    }
    return Array.from(map.values()).sort((a, b) => canonicalGroupIndex(a.group) - canonicalGroupIndex(b.group))
  }, [individualFactors])

  // Filter and sort factors
  const filteredFactors = useMemo(() => {
    let filtered = individualFactors

    // Search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(
        f => f.factor.toLowerCase().includes(query) || f.name.toLowerCase().includes(query)
      )
    }

    // Group filter
    if (groupFilter !== 'all') {
      filtered = filtered.filter(f => f.group === groupFilter)
    }

    // Sort — null sortColumn means Yang's canonical order (array index from lambda)
    if (sortColumn !== null) {
      filtered = [...filtered].sort((a, b) => {
        const aVal = a[sortColumn]
        const bVal = b[sortColumn]

        if (typeof aVal === 'number' && typeof bVal === 'number') {
          return sortDirection === 'asc' ? aVal - bVal : bVal - aVal
        }

        return sortDirection === 'asc'
          ? String(aVal).localeCompare(String(bVal))
          : String(bVal).localeCompare(String(aVal))
      })
    }

    return filtered
  }, [individualFactors, searchQuery, groupFilter, sortColumn, sortDirection])

  // 3-state cycle: click → desc, click → asc, click → default (canonical)
  const handleSort = (column: keyof AlphaFactor) => {
    if (sortColumn === column) {
      if (sortDirection === 'desc') {
        setSortDirection('asc')
      } else {
        // asc → back to default
        setSortColumn(null)
      }
    } else {
      setSortColumn(column)
      setSortDirection('desc')
    }
  }

  // Show placeholder if no data
  if (alphaFactors.length === 0) {
    return (
      <Panel variant="chart">
        <PanelHeader
          title="Alpha Decomposition"
          helpText="Factor attribution showing how each alpha factor contributes to portfolio performance relative to benchmark."
        />
        <PanelContent>
          <div className="text-center py-12 text-white/40">
            No alpha factor data available
            <br />
            <span className="text-sm">Load portfolio data to see factor decomposition</span>
          </div>
        </PanelContent>
      </Panel>
    )
  }

  return (
    <Panel variant="chart">
      <PanelHeader
        title="Alpha Decomposition"
        helpText="Factor attribution showing how each alpha factor contributes to portfolio performance relative to benchmark."
        actions={
          <div className="flex items-center gap-3">
            {/* Search — only in By Factor mode */}
            {viewMode === 'factor' && (
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-white/40" />
                <input
                  type="text"
                  placeholder="Search factor..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-[200px] pl-10 pr-4 py-1.5 bg-white/10 border border-white/20 rounded-lg text-white text-sm placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-[hsl(var(--primary))]"
                />
              </div>
            )}

            {/* View Toggle */}
            <div className="flex items-center gap-2">
              <label className="text-xs text-white/50 tracking-wider">View:</label>
              <div className="flex gap-1">
                <button
                  onClick={() => setViewMode('factor')}
                  className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                    viewMode === 'factor'
                      ? 'bg-[hsl(var(--primary))] text-white'
                      : 'bg-white/10 text-white/60 hover:bg-white/15 hover:text-white/80'
                  }`}
                >
                  By Factor
                </button>
                <button
                  onClick={() => setViewMode('group')}
                  className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                    viewMode === 'group'
                      ? 'bg-[hsl(var(--primary))] text-white'
                      : 'bg-white/10 text-white/60 hover:bg-white/15 hover:text-white/80'
                  }`}
                >
                  By Group
                </button>
              </div>
            </div>

            {/* Group Filter — only in By Factor mode */}
            {viewMode === 'factor' && (
              <div className="flex items-center gap-2">
                <label className="text-xs text-white/50 tracking-wider">Group:</label>
                <select
                  value={groupFilter}
                  onChange={(e) => setGroupFilter(e.target.value)}
                  className="px-3 py-1.5 rounded-lg bg-white/10 border border-white/20 text-white text-sm font-medium focus:outline-none focus:ring-2 focus:ring-[hsl(var(--primary))] min-w-[140px]"
                >
                  {groups.map(group => (
                    <option key={group} value={group} className="bg-[hsl(var(--bg-header))] text-white">
                      {group === 'all' ? 'All Groups' : group}
                    </option>
                  ))}
                </select>
              </div>
            )}
          </div>
        }
      />

      <PanelContent>
        {/* Nested container - rounded edges, no padding (table fills edge-to-edge) */}
        <div className="rounded-lg border border-white/10 overflow-hidden">
          {/* By Group view */}
          {viewMode === 'group' && (
            <div className="overflow-x-auto">
            <table className="w-full border-collapse text-sm">
              {totalAlpha && (
                <thead>
                  <tr className="bg-[hsl(var(--bg-header))] border-b-2 border-white/20">
                    <th colSpan={2} className="py-4 px-6 text-left font-semibold text-base text-white uppercase tracking-wider">
                      Total Alpha
                    </th>
                    <th className="py-4 px-6 text-right">
                      <div className="text-xs text-white/40 font-normal mb-1">Initial</div>
                      <div className="text-lg font-mono font-semibold text-white">{totalAlpha.initial?.toFixed(2) ?? '—'}</div>
                    </th>
                    <th className="py-4 px-6 text-right">
                      <div className="text-xs text-white/40 font-normal mb-1">Optimized</div>
                      <div className="text-lg font-mono font-semibold text-white">{totalAlpha.optimized?.toFixed(2) ?? '—'}</div>
                    </th>
                    <th className="py-4 px-6 text-right">
                      <div className="text-xs text-white/40 font-normal mb-1">Benchmark</div>
                      <div className="text-lg font-mono font-semibold text-white/60">{totalAlpha.benchmark?.toFixed(2) ?? '—'}</div>
                    </th>
                    <th className="py-4 px-6 text-right">
                      <div className="text-xs text-white/40 font-normal mb-1">Trade</div>
                      <div className={`text-lg font-mono font-semibold ${getTradeColor(totalAlpha.trade ?? 0)}`}>
                        {totalAlpha.trade !== undefined ? (totalAlpha.trade >= 0 ? '+' : '') + totalAlpha.trade.toFixed(2) : '—'}
                      </div>
                    </th>
                    <th className="py-4 px-6 text-right">
                      <div className="text-xs text-white/40 font-normal mb-1">Initial Bet</div>
                      <div className="text-lg font-mono font-semibold text-white/60">{totalAlpha.initialBet?.toFixed(2) ?? '—'}</div>
                    </th>
                    <th className="py-4 px-6 text-right">
                      <div className="text-xs text-white/40 font-normal mb-1">Optimized Bet</div>
                      <div className="text-lg font-mono font-semibold text-white">{totalAlpha.optimizedBet?.toFixed(2) ?? '—'}</div>
                    </th>
                  </tr>
                </thead>
              )}
              <thead>
                <tr className="bg-[hsl(var(--bg-header))] border-b border-white/10">
                  <th className="py-3 px-6 text-left font-semibold text-xs uppercase tracking-wide text-white/40">Group</th>
                  <th className="py-3 px-6" />
                  <th className="py-3 px-6 text-right font-semibold text-xs uppercase tracking-wide text-white/40">Initial</th>
                  <th className="py-3 px-6 text-right font-semibold text-xs uppercase tracking-wide text-white/40">Optimized</th>
                  <th className="py-3 px-6 text-right font-semibold text-xs uppercase tracking-wide text-white/40">Benchmark</th>
                  <th className="py-3 px-6 text-right font-semibold text-xs uppercase tracking-wide text-white/40">Trade</th>
                  <th className="py-3 px-6 text-right font-semibold text-xs uppercase tracking-wide text-white/40">Initial Bet</th>
                  <th className="py-3 px-6 text-right font-semibold text-xs uppercase tracking-wide text-white/40">Optimized Bet</th>
                </tr>
              </thead>
              <tbody>
                {groupedFactors.map((g) => (
                  <tr key={g.group} className="border-b border-white/5 odd:bg-white/[0.05] hover:bg-white/10">
                    <td className="py-3 px-6 font-medium text-white/80 capitalize">{g.group}</td>
                    <td className="py-3 px-6" />
                    <td className="py-3 px-6 text-right font-mono text-white/80">{g.initial.toFixed(2)}</td>
                    <td className="py-3 px-6 text-right font-mono text-white/80">{g.optimized.toFixed(2)}</td>
                    <td className="py-3 px-6 text-right font-mono text-white/60">{g.benchmark.toFixed(2)}</td>
                    <td className={`py-3 px-6 text-right font-mono font-semibold ${getTradeColor(g.trade)}`}>
                      {(g.trade >= 0 ? '+' : '') + g.trade.toFixed(2)}
                    </td>
                    <td className={`py-3 px-6 text-right font-mono ${getTradeColor(g.initialBet)}`}>{g.initialBet.toFixed(2)}</td>
                    <td className={`py-3 px-6 text-right font-mono ${getTradeColor(g.optimizedBet)}`}>{g.optimizedBet.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            </div>
          )}

          {/* By Factor view (default) */}
          {viewMode === 'factor' && (
          <div className="overflow-x-auto">
          <table className="w-full border-collapse text-sm">
            {/* Total Alpha Summary Row */}
            {totalAlpha && (
              <thead>
                <tr className="bg-[hsl(var(--bg-header))] border-b-2 border-white/20">
                  {/* Factor + Group columns merged */}
                  <th colSpan={2} className="py-4 px-6 text-left font-semibold text-base text-white uppercase tracking-wider">
                    Total Alpha
                  </th>
                  {/* Values aligned with columns */}
                  <th className="py-4 px-6 text-right">
                    <div className="text-xs text-white/40 font-normal mb-1">Initial</div>
                    <div className="text-lg font-mono font-semibold text-white">
                      {totalAlpha.initial?.toFixed(2) ?? '—'}
                    </div>
                  </th>
                  <th className="py-4 px-6 text-right">
                    <div className="text-xs text-white/40 font-normal mb-1">Optimized</div>
                    <div className="text-lg font-mono font-semibold text-white">
                      {totalAlpha.optimized?.toFixed(2) ?? '—'}
                    </div>
                  </th>
                  <th className="py-4 px-6 text-right">
                    <div className="text-xs text-white/40 font-normal mb-1">Benchmark</div>
                    <div className="text-lg font-mono font-semibold text-white/60">
                      {totalAlpha.benchmark?.toFixed(2) ?? '—'}
                    </div>
                  </th>
                  <th className="py-4 px-6 text-right">
                    <div className="text-xs text-white/40 font-normal mb-1">Trade</div>
                    <div className={`text-lg font-mono font-semibold ${getTradeColor(totalAlpha.trade ?? 0)}`}>
                      {totalAlpha.trade !== undefined ? (totalAlpha.trade >= 0 ? '+' : '') + totalAlpha.trade.toFixed(2) : '—'}
                    </div>
                  </th>
                  <th className="py-4 px-6 text-right">
                    <div className="text-xs text-white/40 font-normal mb-1">Initial Bet</div>
                    <div className="text-lg font-mono font-semibold text-white/60">
                      {totalAlpha.initialBet?.toFixed(2) ?? '—'}
                    </div>
                  </th>
                  <th className="py-4 px-6 text-right">
                    <div className="text-xs text-white/40 font-normal mb-1">Optimized Bet</div>
                    <div className="text-lg font-mono font-semibold text-white">
                      {totalAlpha.optimizedBet?.toFixed(2) ?? '—'}
                    </div>
                  </th>
                </tr>
              </thead>
            )}

            {/* Column Headers */}
            <thead>
              <tr className="bg-[hsl(var(--bg-header))] border-b border-white/10">
                <SortableHeader
                  label="Factor"
                  column="factor"
                  sortColumn={sortColumn}
                  sortDirection={sortDirection}
                  onSort={handleSort}
                />
                <SortableHeader
                  label="Group"
                  column="group"
                  sortColumn={sortColumn}
                  sortDirection={sortDirection}
                  onSort={handleSort}
                />
                <SortableHeader
                  label="Initial"
                  column="initial"
                  sortColumn={sortColumn}
                  sortDirection={sortDirection}
                  onSort={handleSort}
                  align="right"
                />
                <SortableHeader
                  label="Optimized"
                  column="optimized"
                  sortColumn={sortColumn}
                  sortDirection={sortDirection}
                  onSort={handleSort}
                  align="right"
                />
                <SortableHeader
                  label="Benchmark"
                  column="benchmark"
                  sortColumn={sortColumn}
                  sortDirection={sortDirection}
                  onSort={handleSort}
                  align="right"
                />
                <SortableHeader
                  label="Trade"
                  column="trade"
                  sortColumn={sortColumn}
                  sortDirection={sortDirection}
                  onSort={handleSort}
                  align="right"
                />
                <SortableHeader
                  label="Initial Bet"
                  column="initialBet"
                  sortColumn={sortColumn}
                  sortDirection={sortDirection}
                  onSort={handleSort}
                  align="right"
                />
                <SortableHeader
                  label="Optimized Bet"
                  column="optimizedBet"
                  sortColumn={sortColumn}
                  sortDirection={sortDirection}
                  onSort={handleSort}
                  align="right"
                />
              </tr>
            </thead>
            <tbody>
              {filteredFactors.map((factor) => (
                <tr key={factor.factor} className="border-b border-white/5 odd:bg-white/[0.05] hover:bg-white/10">
                  <td className="py-3 px-6 font-medium text-white/80">
                    <div className="flex items-center gap-1.5">
                      <span>{factor.name || factor.factor}</span>
                      <Tooltip content={FACTOR_DESCRIPTIONS[factor.factor] ?? factor.factor} side="right">
                        <HelpCircle size={13} className="text-white/30 hover:text-white/60 transition-colors cursor-help flex-shrink-0" />
                      </Tooltip>
                    </div>
                  </td>
                  <td className="py-3 px-6 text-white/60 capitalize">{factor.group}</td>
                  <td className="py-3 px-6 text-right font-mono text-white/80">
                    {factor.initial?.toFixed(2) ?? '—'}
                  </td>
                  <td className="py-3 px-6 text-right font-mono text-white/80">
                    {factor.optimized?.toFixed(2) ?? '—'}
                  </td>
                  <td className="py-3 px-6 text-right font-mono text-white/60">
                    {factor.benchmark?.toFixed(2) ?? '—'}
                  </td>
                  <td className={`py-3 px-6 text-right font-mono font-semibold ${getTradeColor(factor.trade ?? 0)}`}>
                    {factor.trade !== undefined ? (factor.trade >= 0 ? '+' : '') + factor.trade.toFixed(2) : '—'}
                  </td>
                  <td className={`py-3 px-6 text-right font-mono ${getTradeColor(factor.initialBet ?? 0)}`}>
                    {factor.initialBet?.toFixed(2) ?? '—'}
                  </td>
                  <td className={`py-3 px-6 text-right font-mono ${getTradeColor(factor.optimizedBet ?? 0)}`}>
                    {factor.optimizedBet?.toFixed(2) ?? '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        )}
        </div>
      </PanelContent>
    </Panel>
  )
}

// ============================================================================
// Helper Components
// ============================================================================

interface SortableHeaderProps {
  label: string
  column: keyof AlphaFactor
  sortColumn: keyof AlphaFactor | null
  sortDirection: 'asc' | 'desc'
  onSort: (column: keyof AlphaFactor) => void
  align?: 'left' | 'right'
}

function SortableHeader({
  label,
  column,
  sortColumn,
  sortDirection,
  onSort,
  align = 'left'
}: SortableHeaderProps) {
  const isActive = sortColumn === column
  const textAlign = align === 'right' ? 'text-right' : 'text-left'

  return (
    <th
      className={`py-3 px-6 ${textAlign} font-semibold text-xs uppercase tracking-wide text-white/40 cursor-pointer hover:text-white/60 transition-colors`}
      onClick={() => onSort(column)}
    >
      <div className={`flex items-center gap-1 ${align === 'right' ? 'justify-end' : ''}`}>
        {label}
        {isActive && (
          <span className="text-[hsl(var(--primary))]">
            {sortDirection === 'asc' ? '\u2191' : '\u2193'}
          </span>
        )}
      </div>
    </th>
  )
}

// ============================================================================
// Utility Functions
// ============================================================================

function getTradeColor(value: number): string {
  if (value > 0.1) return 'text-[hsl(var(--success))]'
  if (value < -0.1) return 'text-[hsl(var(--danger))]'
  return 'text-white/40'
}
