/**
 * Advisor Intelligence Page - v5
 *
 * Partner AUA analytics and reporting dashboard
 * Features:
 * - Partner firm selection (dropdown in Partner Analytics header)
 * - Tab 1: Distribution (firm-level cohort analysis -- snapshot + continuous)
 * - Tab 2: Advisors (advisor-level activity -- top 3, rolling flows, leaderboard)
 * - Tab 3: Books (individual advisor book drilldown)
 */

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useAuth } from '@/hooks/useAuth'
import { PageThemeProvider } from '@/contexts/PageThemeContext'
import { PageHeaderCleanBadge } from '@/components/PageHeaderVariants'
import { TabNavigation } from '@/components/TabNavigation'
import { useTabNavigation } from '@/hooks/useTabNavigation'
import { Panel, PanelHeader, PanelContent } from '@/ui/components/panels'
import { Brain, PieChart, Trophy, BookOpen, AlertTriangle } from 'lucide-react'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { PartnerAnalytics } from './components/PartnerAnalytics'
import { DistributionTab } from './tabs/DistributionTab'
import { AdvisorsTab } from './tabs/AdvisorsTab'
import { BooksTab } from './tabs/ClientsTab'
import { getPartnerAnalytics } from '@/api/endpoints/advisor-intelligence'
import { formatPanelTimestamp } from '@/lib/dateUtils'

type TabType = 'distribution' | 'advisors' | 'books'
type GranularityOption = 'monthly' | 'quarterly' | 'annually'

/**
 * Tab Error Fallback UI
 * Shows error within the tab context instead of breaking the entire page
 */
function TabErrorFallback({ tabName }: { tabName: string }) {
  return (
    <Panel variant="chart">
      <PanelContent className="py-12">
        <div className="flex flex-col items-center justify-center text-center px-4">
          <div className="w-16 h-16 rounded-full bg-red-500/10 flex items-center justify-center mb-4">
            <AlertTriangle className="w-8 h-8 text-red-400" />
          </div>
          <h3 className="text-lg font-semibold text-white mb-2">
            Unable to Load {tabName}
          </h3>
          <p className="text-sm text-white/60 mb-6 max-w-md">
            We encountered an error while loading this tab. The rest of the page is still functional.
          </p>
          <div className="flex gap-3">
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-[hsl(var(--primary))] hover:bg-[hsl(var(--primary))]/90 text-white rounded-lg font-medium transition-colors text-sm"
            >
              Refresh Page
            </button>
            <button
              onClick={() => window.history.back()}
              className="px-4 py-2 bg-white/5 hover:bg-white/10 text-white/70 rounded-lg font-medium transition-colors border border-white/10 text-sm"
            >
              Go Back
            </button>
          </div>
        </div>
      </PanelContent>
    </Panel>
  )
}

export function AdvisorIntelligence() {
  const { activeTab, handleTabChange, tabContentRef } = useTabNavigation<TabType>(
    'distribution',
    { analyticsGroup: 'advisor-intelligence' }
  )

  const { isInternal, claims } = useAuth()
  const internal = isInternal()

  // Selected partner firm — 'bd' for 49 Financial (S3 bucket suffix, not display name)
  // Internal users default to 'bd' and can switch via firm picker
  // External users derive from JWT firmId
  const [selectedFirmId, setSelectedFirmId] = useState<string>(
    internal ? 'bd' : (claims?.firmId ?? 'bd')
  )

  // firmOverride: appended as ?firm= on static S3 calls for internal users
  // External users rely on X-Firm-Id injected from JWT by auth-validator-edge
  const firmOverride = internal ? selectedFirmId : undefined

  // Granularity for NMNC/NMEC classification — drives which header_metrics file is fetched
  const [granularity, setGranularity] = useState<GranularityOption>('quarterly')

  // Fetch partner analytics using React Query — refetches when granularity or firm changes
  const {
    data: analyticsData = null,
    isLoading
  } = useQuery({
    queryKey: ['partner-analytics', granularity, firmOverride],
    queryFn: () => getPartnerAnalytics(granularity, firmOverride),
    staleTime: 5 * 60 * 1000,
    refetchOnWindowFocus: false,
    refetchOnMount: false,
  })

  const handlePartnerChange = (firmId: string) => {
    setSelectedFirmId(firmId)
  }

  return (
    <PageThemeProvider accentColor="hsl(var(--primary))">
      <div className="space-y-6">
        <PageHeaderCleanBadge
          icon={Brain}
          title="Advisor Intelligence"
          description={<>Partner <strong>AUA analytics and reporting</strong> dashboard.</>}
        />

        {/* Partner Analytics - Permanent header above all tabs */}
        <PartnerAnalytics
          data={analyticsData}
          isLoading={isLoading}
          selectedFirmId={selectedFirmId}
          onPartnerChange={handlePartnerChange}
          granularity={granularity}
          onGranularityChange={setGranularity}
          firmOverride={firmOverride}
        />

        {/* Tab Navigation - 3 Tabs */}
        <TabNavigation
          tabs={[
            { id: 'distribution', label: 'Distribution', icon: PieChart },
            { id: 'advisors', label: 'Advisors', icon: Trophy },
            { id: 'books', label: 'Books', icon: BookOpen },
          ]}
          activeTab={activeTab}
          onTabChange={(tabId) => handleTabChange(tabId as TabType)}
        />

        {/* Tab Content - Wrapped with Error Boundaries */}
        <div ref={tabContentRef}>
          {activeTab === 'distribution' && (
            <ErrorBoundary fallback={<TabErrorFallback tabName="Distribution" />}>
              <DistributionTab firmId={selectedFirmId} analyticsData={analyticsData} analyticsLoading={isLoading} granularity={granularity} firmOverride={firmOverride} />
            </ErrorBoundary>
          )}
          {activeTab === 'advisors' && (
            <ErrorBoundary fallback={<TabErrorFallback tabName="Advisors" />}>
              <AdvisorsTab firmId={selectedFirmId} firmOverride={firmOverride} />
            </ErrorBoundary>
          )}
          {activeTab === 'books' && (
            <ErrorBoundary fallback={<TabErrorFallback tabName="Books" />}>
              <BooksTab firmId={selectedFirmId} firmOverride={firmOverride} />
            </ErrorBoundary>
          )}
        </div>

        {/* Data Source Note */}
        <Panel variant="chart">
          <PanelHeader title="Data Source" />
          <PanelContent className="pt-6">
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 bg-[hsl(var(--success))] rounded-full animate-pulse" />
                <p className="text-sm text-white/60">
                  <span className="text-[hsl(var(--success))] font-semibold">Black Diamond Connected:</span> Partner AUA and NNA data from Black Diamond Wealth Platform.
                </p>
              </div>
              <div className="text-xs text-white/40">
                Data refreshed daily. Last update: {formatPanelTimestamp(analyticsData?.generated_at) || 'N/A'}
              </div>
            </div>
          </PanelContent>
        </Panel>
      </div>
    </PageThemeProvider>
  )
}
