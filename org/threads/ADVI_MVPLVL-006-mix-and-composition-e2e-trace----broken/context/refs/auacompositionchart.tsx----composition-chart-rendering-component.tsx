/**
 * AUA Composition Chart
 *
 * Stacked area chart showing rolling 12-month AUA composition:
 * - Existing AUA (bottom - gray): Long-term client base
 * - Rolling 12M NMEC (middle - blue): Existing clients adding new money
 * - Rolling 12M NMNC (top - green): New clients bringing new money
 *
 * Uses TTM (trailing twelve months) rolling calculations for smooth visualization.
 */

import { useMemo } from 'react'
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
} from 'recharts'
import { Panel, PanelHeader, PanelContent } from '@/ui/components/panels'
import { LoadingInline } from '@/components/LoadingSpinner'
import { formatCurrency, formatNumberTo3Digits } from '@/lib/universalNumberFormatter'
import type { RollingTimeseries } from '../types'

interface AUACompositionChartProps {
  data: RollingTimeseries | undefined
  isLoading: boolean
}

// Chart colors matching the data scientist's suggestion
const COLORS = {
  nmnc: '#4CAF50',     // Green - New clients
  nmec: '#2196F3',     // Blue - Existing clients + new money
  existing: '#6B7280', // Gray - Stable long-term base
}

// Category order for stacking (bottom to top)
const CATEGORIES = [
  { key: 'existing_aua', label: 'Existing AUA', color: COLORS.existing },
  { key: 'rolling_12m_nmec', label: 'Rolling 12M NMEC', color: COLORS.nmec },
  { key: 'rolling_12m_nmnc', label: 'Rolling 12M NMNC', color: COLORS.nmnc },
]

export function AUACompositionChart({ data, isLoading }: AUACompositionChartProps) {
  // Transform data for Recharts
  const chartData = useMemo(() => {
    if (!data?.data || data.data.length === 0) return []

    return data.data.map(point => ({
      month: point.month,
      existing_aua: point.existing_aua,
      rolling_12m_nmec: point.rolling_12m_nmec,
      rolling_12m_nmnc: point.rolling_12m_nmnc,
      total_aua: point.total_aua,
      // For tooltip
      nmnc_pct: point.nmnc_pct,
      nmec_pct: point.nmec_pct,
      existing_pct: point.existing_pct,
      nmnc_client_count: point.nmnc_client_count,
      nmec_client_count: point.nmec_client_count,
    }))
  }, [data])

  return (
    <Panel variant="chart">
      <PanelHeader
        title="AUA Composition (Rolling 12M)"
        helpText="Total AUA broken down by client segment. Rolling 12-month trailing metrics smooth out monthly volatility."
      />
      <PanelContent className="pt-6">
        {isLoading ? (
          <LoadingInline className="h-[400px]" />
        ) : chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={400}>
            <AreaChart
              data={chartData}
              margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
            >
              {/* Gradient Definitions */}
              <defs>
                {CATEGORIES.map(cat => (
                  <linearGradient key={`gradient-${cat.key}`} id={`gradient-${cat.key}`} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={cat.color} stopOpacity={0.6} />
                    <stop offset="100%" stopColor={cat.color} stopOpacity={0.2} />
                  </linearGradient>
                ))}
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis
                dataKey="month"
                stroke="rgba(255,255,255,0.5)"
                tick={{ fontSize: 11 }}
                angle={-45}
                textAnchor="end"
                height={60}
                tickFormatter={(value) => {
                  const [year, month] = value.split('-')
                  const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                  return `${monthNames[parseInt(month) - 1]} '${year.slice(2)}`
                }}
              />
              <YAxis
                stroke="rgba(255,255,255,0.5)"
                tick={{ fontSize: 12 }}
                tickFormatter={(value) => formatNumberTo3Digits(value, { unit: '$', includeSign: false })}
              />
              <RechartsTooltip
                wrapperStyle={{ zIndex: 40 }}
                cursor={{ stroke: 'rgba(94,114,228,0.5)', strokeWidth: 2 }}
                content={({ active, payload, label }) => {
                  if (!active || !payload || payload.length === 0 || !label) return null

                  const dataPoint = payload[0]?.payload

                  // Format month label
                  const [year, month] = String(label).split('-')
                  const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                  const formattedLabel = `${monthNames[parseInt(month) - 1]} ${year}`

                  return (
                    <div className="bg-[hsl(var(--semantic-background-chartTooltipBg))] border-2 border-[hsl(var(--primary))] rounded-lg px-4 py-3 shadow-xl">
                      {/* Date */}
                      <div className="text-[hsl(var(--semantic-text-chartTooltip))] font-bold text-sm mb-2">{formattedLabel}</div>

                      {/* Total AUA */}
                      <div className="flex items-center justify-between gap-6 mb-2">
                        <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm">Total AUA</span>
                        <span className="text-[hsl(var(--semantic-text-chartTooltip))] font-semibold text-sm">
                          {formatCurrency(dataPoint?.total_aua ?? 0)}
                        </span>
                      </div>

                      {/* Divider */}
                      <div className="border-t border-[hsl(var(--semantic-text-chartTooltip))]/20 my-2" />

                      {/* Breakdown - reverse order for top-to-bottom display */}
                      <div className="space-y-1.5">
                        {/* NMNC */}
                        <div className="flex items-center justify-between gap-6">
                          <div className="flex items-center gap-2">
                            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: COLORS.nmnc }} />
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-xs">Rolling 12M NMNC</span>
                          </div>
                          <div className="text-right">
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))] text-xs font-medium">
                              {formatCurrency(dataPoint?.rolling_12m_nmnc ?? 0)}
                            </span>
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))]/50 text-xs ml-1">
                              ({dataPoint?.nmnc_pct?.toFixed(1)}%)
                            </span>
                          </div>
                        </div>
                        {/* NMEC */}
                        <div className="flex items-center justify-between gap-6">
                          <div className="flex items-center gap-2">
                            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: COLORS.nmec }} />
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-xs">Rolling 12M NMEC</span>
                          </div>
                          <div className="text-right">
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))] text-xs font-medium">
                              {formatCurrency(dataPoint?.rolling_12m_nmec ?? 0)}
                            </span>
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))]/50 text-xs ml-1">
                              ({dataPoint?.nmec_pct?.toFixed(1)}%)
                            </span>
                          </div>
                        </div>
                        {/* Existing */}
                        <div className="flex items-center justify-between gap-6">
                          <div className="flex items-center gap-2">
                            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: COLORS.existing }} />
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-xs">Existing AUA</span>
                          </div>
                          <div className="text-right">
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))] text-xs font-medium">
                              {formatCurrency(dataPoint?.existing_aua ?? 0)}
                            </span>
                            <span className="text-[hsl(var(--semantic-text-chartTooltip))]/50 text-xs ml-1">
                              ({dataPoint?.existing_pct?.toFixed(1)}%)
                            </span>
                          </div>
                        </div>
                      </div>

                      {/* Divider */}
                      <div className="border-t border-[hsl(var(--semantic-text-chartTooltip))]/20 my-2" />

                      {/* Client counts */}
                      <div className="text-[hsl(var(--semantic-text-chartTooltip))]/50 text-[10px]">
                        NMNC Clients: {dataPoint?.nmnc_client_count?.toLocaleString()} | NMEC Clients: {dataPoint?.nmec_client_count?.toLocaleString()}
                      </div>
                    </div>
                  )
                }}
              />
              <Legend
                wrapperStyle={{ paddingTop: '20px' }}
                content={() => (
                  <div className="flex flex-wrap justify-center gap-x-8 gap-y-2 pt-4">
                    {[...CATEGORIES].reverse().map(cat => (
                      <div key={cat.key} className="flex items-center gap-2">
                        <div className="w-6 h-1 rounded" style={{ backgroundColor: cat.color }} />
                        <span className="text-sm text-white/90">{cat.label}</span>
                      </div>
                    ))}
                  </div>
                )}
              />
              {/* Render Areas - stacked (bottom to top) */}
              {CATEGORIES.map(cat => (
                <Area
                  key={cat.key}
                  type="monotone"
                  dataKey={cat.key}
                  stackId="aua"
                  stroke={cat.color}
                  strokeWidth={2}
                  fill={`url(#gradient-${cat.key})`}
                  fillOpacity={1}
                  isAnimationActive={true}
                />
              ))}
            </AreaChart>
          </ResponsiveContainer>
        ) : (
          <div className="h-[400px] flex items-center justify-center">
            <p className="text-white/60">No composition data available</p>
          </div>
        )}
      </PanelContent>
    </Panel>
  )
}
