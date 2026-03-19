/**
 * Client Detail Page
 *
 * Simple 2x2 layout:
 * - Top left (1x1): AI Executive Summary
 * - Top right (1x1): Portfolio Balance pie charts
 * - Bottom (2x1): Time Series
 */

import { useState, useEffect } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, User } from 'lucide-react'
import { PageThemeProvider } from '@/contexts/PageThemeContext'
import { Panel, PanelContent } from '@/ui/components/panels'
import { LoadingInline } from '@/components/LoadingSpinner'
import { AISummaryPanel } from './panels/AISummaryPanel'
import { PortfolioBalancePanel } from './panels/PortfolioBalancePanel'
import { TimeSeriesPanel } from './panels/TimeSeriesPanel'
import type { ClientDetailResponse } from './types'

export function ClientDetailPage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()

  const firmId = searchParams.get('firmId') || '49financial'
  const architectKey = searchParams.get('architectKey')
  const clientKey = searchParams.get('clientKey')
  const clientLabel = searchParams.get('clientLabel') || 'Client'

  const [clientData, setClientData] = useState<ClientDetailResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (!clientKey) {
      // eslint-disable-next-line react-hooks/set-state-in-effect -- valid data fetching pattern
      setIsLoading(false)
      return
    }
    // TODO: Replace with actual API call
    setTimeout(() => {
      setClientData(null)
      setIsLoading(false)
    }, 300)
  }, [firmId, architectKey, clientKey])

  const handleBack = () => navigate('/advisor-intelligence')

  if (!clientKey) {
    return (
      <PageThemeProvider accentColor="hsl(var(--primary))">
        <Panel variant="chart">
          <PanelContent className="py-12 text-center">
            <p className="text-white/60">No client selected.</p>
            <button onClick={handleBack} className="mt-4 text-[hsl(var(--primary))] hover:underline">
              ← Back to Assets Overview
            </button>
          </PanelContent>
        </Panel>
      </PageThemeProvider>
    )
  }

  return (
    <PageThemeProvider accentColor="hsl(var(--primary))">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center gap-4">
          <button
            onClick={handleBack}
            className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
          >
            <ArrowLeft size={20} className="text-white/60" />
          </button>
          <div className="flex items-center gap-3">
            <User size={24} className="text-[hsl(var(--primary))]" />
            <div>
              <h1 className="text-xl font-semibold text-white">{clientLabel}</h1>
              <p className="text-sm text-white/50">
                Architect: {architectKey?.replace(/_/g, ' ') || 'Unknown'}
              </p>
            </div>
          </div>
        </div>

        {isLoading ? (
          <LoadingInline className="py-12" />
        ) : (
          <>
            {/* Top Row: 1x1 + 1x1 */}
            <div className="grid grid-cols-2 gap-6">
              <AISummaryPanel data={clientData} />
              <PortfolioBalancePanel data={clientData} />
            </div>

            {/* Bottom Row: 2x1 */}
            <TimeSeriesPanel data={clientData} />
          </>
        )}
      </div>
    </PageThemeProvider>
  )
}
