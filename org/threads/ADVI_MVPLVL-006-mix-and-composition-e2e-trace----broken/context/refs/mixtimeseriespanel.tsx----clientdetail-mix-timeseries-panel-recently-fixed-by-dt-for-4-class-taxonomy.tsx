/**
 * Mix Timeseries Panel
 *
 * 100% stacked area chart showing asset class allocation over time.
 * 4 series: equity, fixed_income, alternatives, cash.
 * Independent 1Y/3Y/Max window toggle. Click an area to filter Concentration panel.
 */

import { useState, useEffect, useMemo, useCallback } from 'react'
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts'
import { Panel, PanelHeader, PanelContent } from '@/ui/components/panels'
import { getMixTimeseries } from '@/api/endpoints/advisor-intelligence'
import type { MixTimeseriesPoint, MixAssetClass, MixWindow } from '../../types'

// ============================================================================
// Config
// ============================================================================

// Canonical asset class colors — must match CMA portal and PartnerAnalytics
const ASSET_CLASSES: { key: MixAssetClass; label: string; color: string }[] = [
  { key: 'equity',       label: 'Equity',       color: '#3b82f6' }, // Blue
  { key: 'fixed_income', label: 'Fixed Income', color: '#10b981' }, // Green
  { key: 'alternatives', label: 'Alternatives', color: '#f97316' }, // Orange
  { key: 'cash',         label: 'Cash',         color: '#f59e0b' }, // Gold
]

const WINDOW_OPTIONS: MixWindow[] = ['1Y', '3Y', 'Max']

// ============================================================================
// Component
// ============================================================================

interface MixTimeseriesPanelProps {
  relationshipId: string
  firmId: string
  selectedAssetClass: MixAssetClass | null
  onSelectAssetClass: (cls: MixAssetClass | null) => void
}

export function MixTimeseriesPanel({
  relationshipId,
  firmId,
  selectedAssetClass,
  onSelectAssetClass,
}: MixTimeseriesPanelProps) {
  const [window, setWindow] = useState<MixWindow>('1Y')
  const [data, setData] = useState<MixTimeseriesPoint[] | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    setIsLoading(true)
    getMixTimeseries(relationshipId, firmId, window)
      .then((res) => {
        if (!cancelled) setData(res)
      })
      .catch(() => {
        if (!cancelled) setData(null)
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false)
      })
    return () => { cancelled = true }
  }, [relationshipId, firmId, window])

  const hasData = data !== null && data.length > 0

  // XAxis tick formatter: show month labels
  const formatXTick = useCallback((value: string) => {
    if (!value) return ''
    const d = new Date(value + 'T00:00:00')
    return d.toLocaleDateString('en-US', { month: 'short', year: '2-digit' })
  }, [])

  // Show ~6 ticks max
  const tickInterval = useMemo(() => {
    return Math.max(1, Math.floor((data?.length ?? 0) / 6))
  }, [data])

  const handleAreaClick = useCallback((cls: MixAssetClass) => {
    onSelectAssetClass(selectedAssetClass === cls ? null : cls)
  }, [selectedAssetClass, onSelectAssetClass])

  return (
    <Panel variant="chart" className="h-[320px]">
      <PanelHeader
        title="Asset Class Mix"
        helpText="Allocation percentage over time (100% stacked)"
        actions={
          <div className="flex gap-1 bg-white/5 rounded-lg p-1">
            {WINDOW_OPTIONS.map((opt) => (
              <button
                key={opt}
                onClick={() => setWindow(opt)}
                className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                  window === opt
                    ? 'bg-[hsl(var(--primary))] text-white shadow-sm shadow-[hsl(var(--primary))]/30'
                    : 'bg-white/5 text-white/60 hover:bg-white/10 hover:text-white/80'
                }`}
              >
                {opt}
              </button>
            ))}
          </div>
        }
      />
      <PanelContent className="h-full p-4">
        {isLoading ? (
          <div className="flex items-center justify-center h-full">
            <span className="text-xs text-white/40">Loading...</span>
          </div>
        ) : !hasData ? (
          <div className="flex items-center justify-center h-full">
            <span className="text-xs text-white/40">No allocation data available for this client</span>
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data!} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
              <defs>
                {ASSET_CLASSES.map(({ key, color }) => (
                  <linearGradient key={`mix-grad-${key}`} id={`mix-grad-${key}`} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={color} stopOpacity={0.6} />
                    <stop offset="100%" stopColor={color} stopOpacity={0.2} />
                  </linearGradient>
                ))}
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
              <XAxis
                dataKey="date"
                stroke="rgba(255,255,255,0.3)"
                tick={{ fontSize: 10 }}
                tickFormatter={formatXTick}
                interval={tickInterval}
              />
              <YAxis
                stroke="rgba(255,255,255,0.3)"
                tick={{ fontSize: 10 }}
                tickFormatter={(v: number) => `${Math.round(v * 100)}%`}
                domain={[0, 1]}
              />
              <Tooltip
                wrapperStyle={{ zIndex: 40 }}
                cursor={{ stroke: 'rgba(94,114,228,0.5)', strokeWidth: 2 }}
                content={({ active, payload, label }) => {
                  if (!active || !payload?.length) return null
                  return (
                    <div className="bg-[hsl(var(--semantic-background-chartTooltipBg))] border-2 border-[hsl(var(--primary))] rounded-lg px-4 py-3 shadow-xl">
                      <p className="font-medium text-[hsl(var(--semantic-text-chartTooltip))] text-xs mb-1">{label}</p>
                      {payload.map((p, i) => {
                        const cls = ASSET_CLASSES.find(c => c.key === p.dataKey)
                        return (
                          <p key={i} className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-xs">
                            {cls?.label ?? p.dataKey}: {((p.value as number) * 100).toFixed(1)}%
                          </p>
                        )
                      })}
                    </div>
                  )
                }}
              />
              {ASSET_CLASSES.map(({ key, color }) => {
                const dimmed = selectedAssetClass !== null && selectedAssetClass !== key
                return (
                  <Area
                    key={key}
                    type="monotone"
                    dataKey={key}
                    stackId="mix"
                    fill={`url(#mix-grad-${key})`}
                    stroke={color}
                    strokeWidth={1}
                    fillOpacity={dimmed ? 0.3 : 1}
                    strokeOpacity={dimmed ? 0.3 : 1}
                    style={{ cursor: 'pointer' }}
                    onClick={() => handleAreaClick(key)}
                    dot={false}
                    activeDot={false}
                  />
                )
              })}
            </AreaChart>
          </ResponsiveContainer>
        )}
      </PanelContent>
    </Panel>
  )
}
