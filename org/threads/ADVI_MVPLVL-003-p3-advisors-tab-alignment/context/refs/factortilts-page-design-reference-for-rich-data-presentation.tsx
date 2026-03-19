/**
 * Factor Tilts Page
 *
 * Shows factor exposure analysis for model portfolios:
 * - Radar chart visualization of factor profiles
 * - Regression summary metrics (R², alpha, factor tilts)
 * - Bar chart comparison across portfolios
 * - Time series of factor exposures
 *
 * Architecture follows Positioning page patterns:
 * - PageThemeProvider for accent color
 * - Card variant="gradient" for panels
 * - Tab navigation for different views
 *
 * TIERED DATA LOADING (Jan 2026 optimization):
 * - Tier 1 (~46 KB): Loaded on page mount - powers Overview and Bars view
 * - Tier 2 (~196 KB): Lazy loaded on "Factor Spreads" tab click
 * - Tier 3 (~2.1 MB): Lazy loaded on "Time Series" toggle click
 * - Default page load reduced from ~2.3 MB to ~46 KB (99% reduction)
 */

import { useState, useEffect, useCallback } from 'react'
import { PageThemeProvider } from '@/contexts/PageThemeContext'
import { PageHeaderCleanBadge } from '@/components/PageHeaderVariants'
import { TabNavigation } from '@/components/TabNavigation'
import { useTabNavigation } from '@/hooks/useTabNavigation'
import { useSelectTracking } from '@/hooks/useFilterTracking'
import { LoadingContainer } from '@/components/LoadingSpinner'
import { Scale, SlidersHorizontal, Split } from 'lucide-react'
import { FactorTiltOverviewPanel } from './panels/FactorTiltOverviewPanel'
import { FactorTiltBarsTab } from './tabs/FactorTiltBarsTab'
import { FactorTiltTimeSeriesTab } from './tabs/FactorTiltTimeSeriesTab'
import {
  transformSnapshotToDataset,
  mergeSpreadsIntoDataset,
  mergeTimeSeriesIntoDataset,
  computeAggregateMetrics,
  WINDOWS,
} from './constants'
import {
  getFactorTiltsSnapshot,
  getFactorTiltsSpreads,
  getFactorTiltsTimeSeries,
} from '@/api/portal-proxy'
import { getAUMMetrics } from '@/api/endpoints/aum'
import { useYangDataAsOf } from '@/hooks/useDataSource'
import type {
  FactorTiltsDataset,
  PortfolioId,
  WindowId,
  TabType,
} from './types'

export function FactorTilts() {
  // Page state with analytics tracking
  const [selectedScope, setSelectedScope] = useSelectTracking<PortfolioId>('portfolio-scope', 'AGG', 'factor-tilts')
  const [selectedWindow, setSelectedWindow] = useSelectTracking<WindowId>('time-window', '3M', 'factor-tilts')
  const { activeTab, handleTabChange, tabContentRef } = useTabNavigation<TabType>('bars', { analyticsGroup: 'factor-tilts' })

  // Tiered data state
  const [data, setData] = useState<FactorTiltsDataset | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [dataAsOf, setDataAsOf] = useState<string | null>(null)

  // Register factor_tilts data_as_of with central registry
  useYangDataAsOf('factor_tilts', dataAsOf)

  // Tiered loading state
  const [tier2Loaded, setTier2Loaded] = useState(false)
  const [tier2Loading, setTier2Loading] = useState(false)
  const [tier3Loaded, setTier3Loaded] = useState(false)
  const [tier3Loading, setTier3Loading] = useState(false)

  // ============================================================================
  // TIER 1: Load on page mount (snapshot data ~46 KB)
  // ============================================================================
  useEffect(() => {
    Promise.all([
      getFactorTiltsSnapshot(),
      getAUMMetrics()
    ])
      .then(([snapshotData, aumData]) => {
        // Store data_as_of for display and registry
        const asOf = snapshotData.data_as_of || snapshotData.as_of || null
        setDataAsOf(asOf)
        console.log('[FactorTilts] Tier 1 snapshot loaded:', asOf)

        // Transform snapshot to FactorTiltsDataset format
        const transformed = transformSnapshotToDataset(snapshotData)

        // Calculate portfolio weights from AUM data
        const totalAUM = aumData.total.aum
        const aumWeights: Record<string, number> = {}

        for (const model of aumData.by_model) {
          const weight = model.aum / totalAUM
          aumWeights[model.model_name] = weight
          console.log(`[FactorTilts] AUM weight for ${model.model_name}: ${(weight * 100).toFixed(1)}%`)
        }

        // Compute AGG metrics for each window and add to summary
        const aggRows = WINDOWS.map(window =>
          computeAggregateMetrics(transformed.summary, aumWeights, window.id)
        )

        // Replace any existing AGG rows with computed ones
        const summaryWithoutAGG = transformed.summary.filter(row => row.model !== 'AGG')
        transformed.summary = [...summaryWithoutAGG, ...aggRows]

        // CRITICAL: Also update aggregateTiltsByWindow with weighted AGG values
        for (const aggRow of aggRows) {
          transformed.aggregateTiltsByWindow[aggRow.window] = aggRow.factors
        }

        console.log('[FactorTilts] Computed AUM-weighted AGG metrics for all windows')

        setData(transformed)
        setIsLoading(false)
      })
      .catch((err) => {
        console.error('[FactorTilts] Failed to load Tier 1 data:', err)
        setError('Failed to load factor tilts data. Please try refreshing the page.')
        setIsLoading(false)
      })
  }, [])

  // ============================================================================
  // TIER 2: Load on Factor Spreads tab click (~196 KB)
  // ============================================================================
  const loadTier2 = useCallback(async () => {
    if (tier2Loaded || tier2Loading || !data) return

    setTier2Loading(true)
    console.log('[FactorTilts] Loading Tier 2 (factor spreads)...')

    try {
      const spreadsData = await getFactorTiltsSpreads()
      const factorCount = Object.keys(spreadsData.factorSpreads || {}).length
      console.log('[FactorTilts] Tier 2 loaded:', factorCount, 'factor spreads')

      setData(prevData => {
        if (!prevData) return prevData
        return mergeSpreadsIntoDataset(prevData, spreadsData)
      })
      setTier2Loaded(true)
    } catch (err) {
      console.error('[FactorTilts] Failed to load Tier 2:', err)
    } finally {
      setTier2Loading(false)
    }
  }, [tier2Loaded, tier2Loading, data])

  // ============================================================================
  // TIER 3: Load on Time Series toggle (~2.1 MB)
  // ============================================================================
  const loadTier3 = useCallback(async () => {
    if (tier3Loaded || tier3Loading || !data) return

    setTier3Loading(true)
    console.log('[FactorTilts] Loading Tier 3 (model tilt time series)...')

    try {
      const timeseriesData = await getFactorTiltsTimeSeries()
      const factorCount = Object.keys(timeseriesData.timeSeries || {}).length
      const pointCount = Object.values(timeseriesData.timeSeries || {})[0]?.length || 0
      console.log('[FactorTilts] Tier 3 loaded:', factorCount, 'factors with', pointCount, 'data points each')

      setData(prevData => {
        if (!prevData) return prevData
        return mergeTimeSeriesIntoDataset(prevData, timeseriesData)
      })
      setTier3Loaded(true)
    } catch (err) {
      console.error('[FactorTilts] Failed to load Tier 3:', err)
    } finally {
      setTier3Loading(false)
    }
  }, [tier3Loaded, tier3Loading, data])

  // Handle tab change with lazy loading
  const handleTabChangeWithLazyLoad = (tabId: string) => {
    handleTabChange(tabId as TabType)

    // Trigger Tier 2 load when switching to Factor Spreads tab
    if (tabId === 'timeseries') {
      loadTier2()
    }
  }

  // Render tab content
  const renderTabContent = () => {
    if (isLoading) {
      return <LoadingContainer />
    }

    if (error || !data) {
      return (
        <div className="flex items-center justify-center h-64">
          <p className="text-danger">{error || 'No data available'}</p>
        </div>
      )
    }

    switch (activeTab) {
      case 'bars':
        return (
          <FactorTiltBarsTab
            data={data}
            dataAsOf={dataAsOf}
            onLoadTier3={loadTier3}
            tier3Loading={tier3Loading}
            tier3Loaded={tier3Loaded}
          />
        )
      case 'timeseries':
        return (
          <FactorTiltTimeSeriesTab
            data={data}
            dataAsOf={dataAsOf}
            tier2Loading={tier2Loading}
            tier2Loaded={tier2Loaded}
          />
        )
      default:
        return null
    }
  }

  return (
    <PageThemeProvider accentColor="hsl(var(--model-default))">
      <div className="space-y-6">
        <PageHeaderCleanBadge
          icon={Scale}
          title="Factor Tilts"
          description={<><span className="font-bold">Factor exposure analysis and regression metrics</span> across model portfolios.</>}
        />

        {/* Overview Panel (Radar + Summary Table) */}
        {isLoading ? (
          <div className="bg-[hsl(var(--bg-card))] rounded-lg border border-white/10">
            <LoadingContainer />
          </div>
        ) : error || !data ? (
          <div className="flex items-center justify-center h-64 bg-[hsl(var(--bg-card))] rounded-lg border border-white/10">
            <p className="text-danger">{error || 'No data available'}</p>
          </div>
        ) : (
          <FactorTiltOverviewPanel
            data={data}
            selectedScope={selectedScope}
            setSelectedScope={setSelectedScope}
            selectedWindow={selectedWindow}
            setSelectedWindow={setSelectedWindow}
            dataAsOf={dataAsOf}
          />
        )}

        {/* Tab Navigation */}
        <TabNavigation
          tabs={[
            { id: 'bars', label: 'Portfolio Factors', icon: SlidersHorizontal },
            { id: 'timeseries', label: 'Factor Spreads', icon: Split }
          ]}
          activeTab={activeTab}
          onTabChange={handleTabChangeWithLazyLoad}
        />

        {/* Tab Content */}
        <div ref={tabContentRef}>
          {renderTabContent()}
        </div>
      </div>
    </PageThemeProvider>
  )
}
