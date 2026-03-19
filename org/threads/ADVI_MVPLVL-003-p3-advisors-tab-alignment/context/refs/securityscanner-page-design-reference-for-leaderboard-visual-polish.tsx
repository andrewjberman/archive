/**
 * SecurityScanner — page orchestrator.
 *
 * Multi-factor security screening tool ported from Yang's Factor_Scanning_Model.xlsm.
 * PMs select factors, assign weights, and see dynamically ranked securities
 * across 6 universes.
 *
 * Composition order mirrors PortfolioManagement.tsx:
 *   PageThemeProvider > PageHeaderCleanBadge > ScannerHeaderPanel (sticky)
 *   > TabNavigation > tab content area
 *
 * Contracted: SSCN_DESIGN_CONTRACT.md Section 8
 */

import { useEffect, useRef } from 'react'
import { ScanLine } from 'lucide-react'
import { PageThemeProvider } from '@/contexts/PageThemeContext'
import { PageHeaderCleanBadge } from '@/components/PageHeaderVariants'
import { useTabNavigation } from '@/hooks/useTabNavigation'
import { TabNavigation } from '@/components/TabNavigation'
import { ScannerHeaderPanel } from './components/ScannerHeaderPanel'
import { useScannerState } from './hooks/useScannerState'
import { useFactorMetadata } from './hooks/useScannerApi'
import { FactorBankTab } from './tabs/FactorBankTab'
import { UniverseDataTab } from './tabs/UniverseDataTab'

import { UniverseScannerTab } from './tabs/UniverseScannerTab'
import type { TabType, FactorDefinition } from './types'

/** Categories to seed as defaults, one top-IC factor each. */
const DEFAULT_CATEGORIES = ['value', 'growth', 'quality', 'momentum', 'size']

const SCANNER_TABS = [
  { id: 'factor-bank' as const, label: 'Factor Bank' },
  { id: 'universe-data' as const, label: 'Universe Data' },
  { id: 'universe-scanner' as const, label: 'Security Scanner' },
]

export function SecurityScanner() {
  const { activeTab, handleTabChange, tabContentRef } =
    useTabNavigation<TabType>('factor-bank', {
      analyticsGroup: 'security-scanner',
    })

  const scannerState = useScannerState()
  const { data: factorData } = useFactorMetadata()
  const defaultsSeeded = useRef(false)

  useEffect(() => {
    if (!factorData || defaultsSeeded.current) return
    defaultsSeeded.current = true
    const picks: FactorDefinition[] = []
    for (const cat of DEFAULT_CATEGORIES) {
      const candidates = factorData.factors.filter(f => f.category === cat)
      if (candidates.length === 0) continue
      candidates.sort((a, b) => Math.abs(b.ic) - Math.abs(a.ic))
      picks.push(candidates[0])
    }
    if (picks.length > 0) {
      scannerState.initializeDefaults(picks)
    }
  }, [factorData])

  return (
    <PageThemeProvider accentColor="hsl(var(--primary))">
      <div className="space-y-6">
        {/* Page header */}
        <PageHeaderCleanBadge
          icon={ScanLine}
          title="Security Scanner"
          description="Multi-factor screening across 6 universes with weighted composite ranking."
        />

        {/* Always-visible sticky scanner controls */}
        <div className="sticky top-0 z-40">
          <ScannerHeaderPanel
            selectedUniverseId={scannerState.selectedUniverseId}
            selectedFactors={scannerState.selectedFactors}
            allFactors={factorData?.factors ?? []}
            weights={scannerState.weights}
            totalWeight={scannerState.totalWeight}
            isWeightValid={scannerState.isWeightValid}
            onUniverseChange={scannerState.setUniverse}
            onRemoveFactor={scannerState.removeFactor}
            onSetWeight={scannerState.setWeight}
            onEqualWeight={scannerState.setEqualWeight}
            onClearSelection={scannerState.clearSelection}
          />
        </div>

        {/* Tab navigation */}
        <TabNavigation
          tabs={SCANNER_TABS}
          activeTab={activeTab}
          onTabChange={(id) => handleTabChange(id as TabType)}
        />

        {/* Tab content */}
        <div ref={tabContentRef}>
          {activeTab === 'factor-bank' && (
            <FactorBankTab
              selectedFactors={scannerState.selectedFactors}
              onAddFactor={scannerState.addFactor}
              onRemoveFactor={scannerState.removeFactor}
            />
          )}
          {activeTab === 'universe-data' && (
            <UniverseDataTab
              selectedUniverseId={scannerState.selectedUniverseId}
              selectedFactors={scannerState.selectedFactors}
            />
          )}
          {activeTab === 'universe-scanner' && (
            <UniverseScannerTab
              selectedUniverseId={scannerState.selectedUniverseId}
              selectedFactors={scannerState.selectedFactors}
              weights={scannerState.weights}
              isWeightValid={scannerState.isWeightValid}
            />
          )}
        </div>
      </div>
    </PageThemeProvider>
  )
}
