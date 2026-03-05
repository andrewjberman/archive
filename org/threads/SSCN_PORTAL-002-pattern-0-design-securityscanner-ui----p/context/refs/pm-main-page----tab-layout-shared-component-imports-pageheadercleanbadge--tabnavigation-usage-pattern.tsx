import { useEffect, useState, useMemo } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import { Layers, History, Activity, PieChart, Code, FileText } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { PageThemeProvider } from '@/contexts/PageThemeContext'
import { PageHeaderCleanBadge } from '@/components/PageHeaderVariants'
import { useTabNavigation } from '@/hooks/useTabNavigation'
import { TabNavigation } from '@/components/TabNavigation'
import { toast } from 'sonner'

import { HistoryTab } from './tabs/HistoryTab'
import { AlphaTab } from './tabs/AlphaTab'
import { SectorTab } from './tabs/SectorTab'
import { ModelTab } from './tabs/ModelTab'
import { TradeTab } from './tabs/TradeTab'
import { OptimizationSummaryHeader } from './components/OptimizationSummaryHeader'
import { UploadPortfolioModal } from './components/UploadPortfolioModal'
import { usePortfolioStore } from './hooks/usePortfolioStore'
import { useFunds, useAutoSaveQuery, FALLBACK_FUNDS, portfolioKeys } from './hooks/usePortfolioApi'
import { useAutoSave } from './hooks/useAutoSave'
import { useOptimizationAutoSave } from './hooks/useOptimizationAutoSave'
import { useOptimizationState } from './hooks/useOptimizationState'
import { optimizationKeys } from './hooks/usePortfolioOptimizationApi'
import { loadOptimizationData } from '@/api/endpoints/portfolio-optimization'
import { saveOptimizationAutoSave } from '@/api/endpoints/portfolio'
import { filterToStyleFactors } from './utils/riskFactorFilter'
import type { TabType } from './types'
import type { FundCode } from '@/api/endpoints/portfolio'
import type { OptimizationSnapshot } from '@/types/portfolio-optimization'

export function PortfolioManagement() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { activeTab, handleTabChange, tabContentRef } = useTabNavigation<TabType>('alpha', {
    analyticsGroup: 'portfolio-management',
  })

  // =====================
  // Task #6: Page Load Logic - Auto-save Integration
  // =====================
  const store = usePortfolioStore()

  // 1. Fetch funds on mount
  const { data: fundsData, isLoading: isLoadingFunds } = useFunds()

  // Sort funds: PFDE first, then alphabetically.
  // Fall back to static list if the API returns nothing (e.g. endpoint not wired up yet).
  const sortedFunds = useMemo(() => {
    const funds = fundsData?.funds?.length ? fundsData.funds : FALLBACK_FUNDS
    return [...funds].sort((a, b) => {
      if (a.code === 'PFDE') return -1
      if (b.code === 'PFDE') return 1
      return a.code.localeCompare(b.code)
    })
  }, [fundsData?.funds])

  useEffect(() => {
    if (sortedFunds.length > 0) {
      console.log('[Portfolio] Loaded funds:', sortedFunds.map(f => f.code))

      // Auto-select first fund (PFDE) if none selected
      if (!store.selectedFund) {
        const firstFund = sortedFunds[0]
        console.log('[Portfolio] Auto-selecting first fund:', firstFund.code)

        // If TAX fund, also select first sub-account
        if (firstFund.hasSubAccounts && firstFund.accounts && firstFund.accounts.length > 0) {
          store.setFund(firstFund.code, firstFund.accounts[0].id)
        } else {
          store.setFund(firstFund.code)
        }
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sortedFunds])

  // 2. Fetch auto-save when fund selected
  const { data: autoSaveData, isLoading: isLoadingAutoSave } = useAutoSaveQuery(
    store.selectedFund,
    store.selectedAccount
  )

  useEffect(() => {
    if (autoSaveData?.exists && autoSaveData.autosave) {
      const autosave = autoSaveData.autosave
      console.log('[Portfolio] Auto-save found:', autosave.sessionId)
      console.log('[Portfolio] Auto-save has', autosave.securities?.length ?? autosave.trades?.length ?? 0, 'items')
      console.log('[Portfolio] Overrides count:', autosave.overridesCount)

      // Only pass to legacy store for old-format autosaves (have 'trades').
      // New-format autosaves (have 'securities') are loaded via Resume button.
      if (autosave.trades) {
        store.loadAutoSave(autosave)
      }
    } else if (autoSaveData && !autoSaveData.exists) {
      console.log('[Portfolio] No auto-save found for', store.selectedFund, store.selectedAccount)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [autoSaveData])

  // 3. Start auto-save interval (60s, only if changes)
  const { isSaving, lastSaved, saveError } = useAutoSave()

  useEffect(() => {
    if (isSaving) {
      console.log('[Portfolio] Auto-save in progress...')
    } else if (lastSaved) {
      console.log('[Portfolio] Last saved at:', lastSaved)
    } else if (saveError) {
      console.error('[Portfolio] Auto-save error:', saveError)
    }
  }, [isSaving, lastSaved, saveError])

  // Portfolio Optimization State (for all tabs)
  // Date is set after file upload - starts empty (no auto-load)
  const [optimizationDate, setOptimizationDate] = useState<string>('')
  const optimization = useOptimizationState(store.selectedFund || 'PFDE', optimizationDate)

  // Auto-save optimization state every 60s (full state, not delta)
  const optimizationAutoSave = useOptimizationAutoSave({
    fund: store.selectedFund,
    account: store.selectedAccount,
    optimizationDate: optimizationDate,
    modelDate: optimizationDate,  // TODO: Get from actual data
    securities: optimization.securities,
    alphaFactors: optimization.alphaFactors,
    sectorAllocations: optimization.sectorAllocations,
    modelCoefficients: optimization.modelCoefficients,
    modelGroups: optimization.modelGroups,
    riskFactors: optimization.riskFactors,
    summary: optimization.summary,
    isDirty: optimization.isDirty
  })

  // Upload state
  const [showUploadModal, setShowUploadModal] = useState(false)

  // Fund change handler
  const handleFundChange = (fund: FundCode, account: string | null) => {
    store.setFund(fund, account)
  }

  // Resume last session
  const handleResumeSession = () => {
    console.log('[Portfolio] Resume button clicked')

    if (!autoSaveData?.exists || !autoSaveData.autosave) {
      console.error('[Portfolio] No autosave data available')
      toast.error('No saved session found')
      return
    }

    const autosave = autoSaveData.autosave
    console.log('[Portfolio] Full autosave object:', autosave)
    console.log('[Portfolio] Resuming session:', autosave.sessionId)
    console.log('[Portfolio] Saved data:', {
      optimizationDate: autosave.optimizationDate,
      securities: autosave.securities?.length || autosave.trades?.length || 0,
      overrides: autosave.overridesCount || 0,
      allKeys: Object.keys(autosave)
    })

    // Check if autosave has full optimization data (new format)
    const hasFullData = autosave.securities && autosave.alphaFactors

    if (hasFullData) {
      // NEW FORMAT: Load data directly from autosave (includes overrides!)
      console.log('[Portfolio] Loading data directly from autosave (new format)')
      console.log('[Portfolio] Autosave securities sample:', autosave.securities?.slice(0, 2))
      console.log('[Portfolio] Autosave alphaFactors sample:', autosave.alphaFactors?.slice(0, 2))
      console.log('[Portfolio] Autosave summary:', autosave.summary)

      // Load all data directly from autosave into optimization state
      // CRITICAL: Do NOT set optimizationDate in parent - it would trigger backend fetch!
      // We're loading from autosave, not from S3 PKL/XLSX files
      optimization.setSecurities(autosave.securities || [])
      optimization.setAlphaFactors(autosave.alphaFactors || [])
      optimization.setSectorAllocations(autosave.sectorAllocations || [])
      optimization.setModelCoefficients(autosave.modelCoefficients || [])
      optimization.setModelGroups(autosave.modelGroups || [])
      optimization.setBaselineRiskFactors(autosave.riskFactors || [])
      optimization.setSummary(autosave.summary || null)  // Load saved summary with all metrics
      optimization.setOptimizationDate(autosave.optimizationDate || '')
      optimization.setModelDate(autosave.modelDate || autosave.optimizationDate || '')

      // DON'T set optimizationDate in parent state!
      // It would trigger usePortfolioData fetch which causes 500 error
      // Session is now active because data is loaded in optimization state

      console.log('[Portfolio] Loaded from autosave:', {
        securities: autosave.securities?.length,
        alphaFactors: autosave.alphaFactors?.length,
        modelCoefficients: autosave.modelCoefficients?.length,
        sectorAllocations: autosave.sectorAllocations?.length,
        riskFactors: autosave.riskFactors?.length
      })

      // Background: fetch factors from Lambda and merge into securities.
      // The initial autosave strips factors[] to stay under payload limits.
      // This restores them without overwriting any PM override data.
      const hasSomeFactors = autosave.securities?.some((s: any) => s.factors?.length > 0)
      if (!hasSomeFactors && autosave.optimizationDate && store.selectedFund) {
        const fetchFund = store.selectedFund
        const fetchDate = autosave.optimizationDate

        console.log('[Portfolio] Autosave has no factors — fetching in background for', fetchFund, fetchDate)

        queryClient.fetchQuery({
          queryKey: optimizationKeys.data(fetchFund, fetchDate.replace(/-/g, '')),
          queryFn: () => loadOptimizationData(fetchFund, fetchDate),
          staleTime: 10 * 60 * 1000,
        }).then(data => {
          if (!data?.securities?.length) return
          const factorsMap: Record<string, any[]> = {}
          data.securities.forEach((sec: any) => {
            if (sec.factors?.length) factorsMap[sec.ticker] = sec.factors
          })
          const count = Object.keys(factorsMap).length
          if (count > 0) {
            optimization.mergeSecurityFactors(factorsMap)
            console.log(`[Portfolio] Background factor fetch complete — merged factors for ${count} securities`)
          }
        }).catch(err => {
          console.warn('[Portfolio] Background factor fetch failed (non-fatal):', err?.message)
        })
      }

      // Show success
      const lastSavedTime = new Date(autosave.lastSaved).toLocaleString()
      const overridesText = autosave.overridesCount > 0
        ? ` (${autosave.overridesCount} overrides)`
        : ''

      toast.success(`Resumed session from ${lastSavedTime}${overridesText}`)
    } else {
      // OLD FORMAT: Only has optimizationDate, need to fetch from S3
      console.log('[Portfolio] Old autosave format - fetching from S3')

      const savedDate = autosave.optimizationDate || autosave.asOfDate
      if (!savedDate) {
        console.error('[Portfolio] No optimizationDate in autosave')
        toast.error('Cannot resume - optimization date not found in autosave')
        return
      }

      // Trigger optimization data load from S3
      const dateWithoutHyphens = savedDate.replace(/-/g, '')
      console.log('[Portfolio] Setting optimizationDate to:', dateWithoutHyphens)
      setOptimizationDate(dateWithoutHyphens)

      toast.success('Loading session...')
    }

    console.log('[Portfolio] Resume complete')
  }

  // Open upload modal (check for existing autosave first)
  const handleUploadClick = () => {
    if (!store.selectedFund) {
      toast.error('Please select a fund first')
      return
    }

    // Check if autosave exists - warn before overwriting
    if (autoSaveData?.exists && autoSaveData.autosave) {
      const lastSaved = new Date(autoSaveData.autosave.lastSaved).toLocaleString()
      const confirmed = window.confirm(
        `You have unsaved work from ${lastSaved}.\n\n` +
        `Uploading new files will replace this session.\n\n` +
        `Continue with upload?`
      )

      if (!confirmed) {
        return // User cancelled
      }
    }

    setShowUploadModal(true)
  }

  // Handle upload completion - update date to trigger data reload
  const handleUploadComplete = (data: OptimizationSnapshot) => {
    console.log('[Portfolio] Upload complete, data loaded:', data.securities?.length || 0, 'securities')
    console.log('[Portfolio] CRITICAL - Check these values:')
    console.log('[Portfolio]   optimizationDate from backend:', data.optimizationDate)
    console.log('[Portfolio]   modelDate from backend:', data.modelDate)
    console.log('[Portfolio]   Data structure:', {
      securities: data.securities?.length || 0,
      alphaFactors: data.alphaFactors?.length || 0,
      sectorAllocations: data.sectorAllocations?.length || 0,
      modelCoefficients: data.modelCoefficients?.length || 0,
      modelGroups: data.modelGroups?.length || 0,
      riskFactors: data.riskFactors?.length || 0,
      optimizationDate: data.optimizationDate
    })
    console.log('[Portfolio] First 2 securities:', data.securities?.slice(0, 2))

    // Convert date to YYYYMMDD format (remove hyphens)
    const dateWithoutHyphens = data.optimizationDate.replace(/-/g, '')
    console.log('[Portfolio] Setting optimization date to:', dateWithoutHyphens, '(from backend response)')

    // Clear all stale optimization and autosave/version caches so prior-session data
    // cannot bleed through after a fresh upload.
    queryClient.removeQueries({ queryKey: optimizationKeys.all })
    queryClient.removeQueries({ queryKey: portfolioKeys.autosave(store.selectedFund || null, store.selectedAccount || null) })
    queryClient.removeQueries({ queryKey: portfolioKeys.versions(store.selectedFund || null, store.selectedAccount || null) })

    // Seed the fresh data directly into the React Query cache — no second fetch needed.
    queryClient.setQueryData(
      optimizationKeys.data(store.selectedFund || 'PFDE', dateWithoutHyphens),
      data
    )

    // Update optimization date — usePortfolioData reads from cache above (instant, no fetch)
    setOptimizationDate(dateWithoutHyphens)

    // Create initial autosave with full optimization data (non-blocking)
    createInitialAutosave(data).catch(err => {
      console.warn('[Portfolio] Autosave creation failed (non-fatal):', err.message)
    })

    toast.success('Portfolio data loaded into all tabs')
  }

  // Create initial autosave after upload
  const createInitialAutosave = async (data: OptimizationSnapshot) => {
    if (!store.selectedFund) return

    console.log('[Portfolio] Creating initial autosave for optimization session')
    console.log('[Portfolio] Data to save:', {
      securities: data.securities?.length,
      alphaFactors: data.alphaFactors?.length,
      sectorAllocations: data.sectorAllocations?.length,
      modelCoefficients: data.modelCoefficients?.length,
      modelGroups: data.modelGroups?.length,
      riskFactors: data.riskFactors?.length,
      optimizationDate: data.optimizationDate
    })
    console.log('[Portfolio] First 3 securities:', data.securities?.slice(0, 3))
    console.log('[Portfolio] First 3 alphaFactors:', data.alphaFactors?.slice(0, 3))

    try {
      // Strip out heavy nested data to stay under 5 MB limit
      // We only need essential fields for resume - can reload factors from backend if needed
      const lightweightSecurities = data.securities.map(sec => ({
        ticker: sec.ticker,
        name: sec.name,
        economy: sec.economy,
        economyName: sec.economyName,
        sector: sec.sector,
        industryGroup: sec.industryGroup,
        marketCap: sec.marketCap,
        price: sec.price,
        size: sec.size,
        initialWeight: sec.initialWeight,
        optimizedWeight: sec.optimizedWeight,
        benchmarkWeight: sec.benchmarkWeight,
        minWeight: sec.minWeight,
        maxWeight: sec.maxWeight,
        trade: sec.trade,
        initialBet: sec.initialBet,
        optimizedBet: sec.optimizedBet,
        alpha: sec.alpha,
        totalRisk: sec.totalRisk,
        specRisk: sec.specRisk,
        // DON'T include factors[] array - saves ~4 MB
      }))

      const payload = {
        sessionId: `opt_${Date.now()}`,
        optimizationDate: data.optimizationDate,
        modelDate: data.modelDate || data.optimizationDate,
        securities: lightweightSecurities,  // Stripped version (no factors[] arrays)
        alphaFactors: data.alphaFactors,
        sectorAllocations: data.sectorAllocations,
        modelCoefficients: data.modelCoefficients,
        modelGroups: data.modelGroups,
        riskFactors: filterToStyleFactors(data.riskFactors),  // Only 12 style factors (not 100+)
        summary: data.summary,
        overridesCount: 0  // Fresh upload - no overrides yet
      }

      console.log('[Portfolio] Calling saveOptimizationAutoSave with payload size:', JSON.stringify(payload).length, 'bytes')

      await saveOptimizationAutoSave(
        store.selectedFund,
        store.selectedAccount,
        payload
      )

      console.log('[Portfolio] Initial autosave created successfully')
    } catch (error) {
      console.error('[Portfolio] Failed to create initial autosave:', error)
      console.error('[Portfolio] Error details:', error)
      // Non-fatal - user can still work, just won't have autosave
    }
  }


  return (
    <PageThemeProvider accentColor="hsl(var(--primary))">
      <div className="space-y-6">
        {/* Header */}
        <PageHeaderCleanBadge
          icon={Layers}
          title="Portfolio Management"
          description={
            <>
              Optimize portfolio allocation with <span className="font-bold">factor-based analysis and constraint validation</span>.
            </>
          }
        />

        {/* Optimization Summary Header (includes fund selector + upload + summary stats) */}
        <OptimizationSummaryHeader
          selectedFund={store.selectedFund}
          selectedAccount={store.selectedAccount}
          availableFunds={sortedFunds}
          onFundChange={handleFundChange}
          isLoadingFunds={isLoadingFunds}
          autoSaveData={autoSaveData}
          onResumeSession={handleResumeSession}
          hasActiveSession={optimization.securities.length > 0}
          isSaving={optimizationAutoSave.isSaving}
          lastSaved={optimizationAutoSave.lastSaved}
          saveError={optimizationAutoSave.saveError}
          onUploadClick={handleUploadClick}
          isUploading={false}
          summary={optimization.summary}
          riskFactors={optimization.riskFactors}
          securities={optimization.securities}
        />

        {/* Upload Portfolio Modal */}
        <UploadPortfolioModal
          isOpen={showUploadModal}
          onClose={() => setShowUploadModal(false)}
          fund={store.selectedFund || 'PFDE'}
          onUploadComplete={handleUploadComplete}
        />

        {/* Portfolio Management Tabs */}
        <TabNavigation
          tabs={[
            { id: 'alpha', label: 'Alpha', icon: Activity },
            { id: 'sector', label: 'Sector', icon: PieChart },
            { id: 'model', label: 'Model', icon: Code },
            { id: 'trade', label: 'Trade', icon: FileText },
            { id: 'history', label: 'History', icon: History },
          ]}
          activeTab={activeTab}
          onTabChange={(tabId) => handleTabChange(tabId as TabType)}
        />

        {/* Tab Content */}
        <div ref={tabContentRef}>
          {activeTab === 'alpha' && <AlphaTab alphaFactors={optimization.alphaFactors} />}
          {activeTab === 'sector' && <SectorTab sectorAllocations={optimization.sectorAllocations} securities={optimization.securities} />}
          {activeTab === 'model' && (
            <ModelTab
              coefficients={optimization.modelCoefficients}
              groups={optimization.modelGroups}
            />
          )}
          {activeTab === 'trade' && (
            <TradeTab
              securities={optimization.securities}
              constraintViolations={optimization.constraintViolations}
              onUpdateWeight={optimization.updateSecurityWeight}
              onUpdateFinalTrade={optimization.updateFinalTrade}
              onResetAll={optimization.resetAllWeights}
              onResetZero={optimization.resetZeroWeights}
              onAddSecurity={optimization.addSecurity}
              onRemoveSecurity={optimization.removeSecurity}
              onBulkUpdate={optimization.bulkUpdateWeights}
              optimizationDate={optimization.optimizationDate || optimizationDate}
            />
          )}
          {activeTab === 'history' && <HistoryTab />}
        </div>

        {/* Execute Save Button - Removed for now (not needed during debugging) */}
      </div>
    </PageThemeProvider>
  )
}
