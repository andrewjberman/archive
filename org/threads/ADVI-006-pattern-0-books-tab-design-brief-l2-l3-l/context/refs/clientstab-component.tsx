/**
 * Books Tab - Advisor Intelligence
 *
 * Individual advisor book drilldown. For admin users, provides
 * advisor selector and client-level detail. For advisor users (future),
 * this is their home page.
 *
 * Layout:
 * +------------------------------------------------------------+
 * |  [Book] [Client]    |  Search clients...                    |
 * +-----------------------------+------------------------------+
 * |    AI Executive Summary     |      Headline Numbers         |
 * +----------+----------+------+-----+-------------------------+
 * |   Tax    |  Income  | Portfolio  |     Engagement           |
 * |  Intel   |  & Fees  |   Comp    |      Metrics             |
 * +----------+----------+-----------+-------------------------+
 */

import { useState, useEffect, useMemo } from 'react'
import { useSelectTracking } from '@/hooks/useFilterTracking'
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts'
import { Panel } from '@/ui/components/panels'
import { LoadingInline } from '@/components/LoadingSpinner'
import {
  Sparkles,
  DollarSign,
  Users,
  Wallet,
  TrendingUp,
  PiggyBank,
  Receipt,
  Activity,
  Search,
  ChevronDown,
  Building2,
  User,
  ChevronRight,
} from 'lucide-react'
import { formatCurrency, formatNumberTo3Digits } from '@/lib/universalNumberFormatter'
import { getClientsTab, getClientDetail, getArchitectLeaderboard, getAdvisorBook } from '@/api/endpoints/advisor-intelligence'
import { useAuth } from '@/hooks/useAuth'
import type {
  ClientsTabResponse,
  ClientDetailResponse,
  ClientOption,
  ClientsTabHeadline,
  ClientsTabTax,
  ClientsTabIncomeFees,
  ClientsTabPortfolio,
  ClientsTabEngagement,
  LeaderboardEntry,
  AdvisorBookResponse,
} from '../types'

interface BooksTabProps {
  firmId: string
}

type ViewMode = 'book' | 'client'

// Special value for "All Advisors" selection
const ALL_ADVISORS = '__all__'

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export function BooksTab({ firmId }: BooksTabProps) {
  // Auth context for role-based UI
  const { isInternal, isDev } = useAuth()

  // Firm admin can see advisor dropdown and summary table
  // All current users are internal (Opal employees), so everyone sees firm_admin view
  const isFirmAdmin = isInternal() || isDev()

  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [bookData, setBookData] = useState<ClientsTabResponse | null>(null)
  const [clientDetailData, setClientDetailData] = useState<ClientDetailResponse | null>(null)
  const [viewMode, setViewMode] = useSelectTracking<ViewMode>('view-mode', 'book', 'advisor-intelligence-clients')
  const [selectedClient, setSelectedClient] = useState<ClientOption | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [isDropdownOpen, setIsDropdownOpen] = useState(false)
  const [isLoadingClient, setIsLoadingClient] = useState(false)

  // Advisor selection state (for firm admin view)
  const [selectedAdvisor, setSelectedAdvisor] = useState<string>(ALL_ADVISORS)
  const [advisorSummary, setAdvisorSummary] = useState<LeaderboardEntry[]>([])
  const [isAdvisorDropdownOpen, setIsAdvisorDropdownOpen] = useState(false)
  const [advisorBookData, setAdvisorBookData] = useState<AdvisorBookResponse | null>(null)
  const [isLoadingAdvisor, setIsLoadingAdvisor] = useState(false)

  // Fetch book data on mount
  useEffect(() => {
    if (!firmId) {
      setIsLoading(false)
      return
    }

    let cancelled = false
    setIsLoading(true)
    setError(null)

    getClientsTab()
      .then((data) => {
        if (!cancelled) {
          setBookData(data)
          setIsLoading(false)
        }
      })
      .catch((err) => {
        if (!cancelled) {
          console.error('Failed to fetch clients tab data:', err)
          setError(err.message || 'Failed to load data')
          setIsLoading(false)
        }
      })

    return () => { cancelled = true }
  }, [firmId])

  // Fetch client detail when a client is selected
  useEffect(() => {
    console.log('[ClientsTab] selectedClient changed:', selectedClient)
    if (!selectedClient) {
      setClientDetailData(null)
      return
    }

    let cancelled = false
    setIsLoadingClient(true)
    console.log('[ClientsTab] Fetching client detail for:', selectedClient.key)

    getClientDetail(selectedClient.key)
      .then((data) => {
        if (!cancelled) {
          setClientDetailData(data)
          setIsLoadingClient(false)
        }
      })
      .catch((err) => {
        if (!cancelled) {
          console.error('Failed to fetch client detail:', err)
          // Keep showing book data on error, just log it
          setClientDetailData(null)
          setIsLoadingClient(false)
        }
      })

    return () => { cancelled = true }
  }, [selectedClient])

  // Reset to book view when firm changes
  useEffect(() => {
    setViewMode('book')
    setSelectedClient(null)
    setSearchQuery('')
    setClientDetailData(null)
    setSelectedAdvisor(ALL_ADVISORS)
    // eslint-disable-next-line react-hooks/exhaustive-deps -- setViewMode is stable
  }, [firmId])

  // Fetch advisor summary for firm admin view
  useEffect(() => {
    if (!firmId || !isFirmAdmin) return

    let cancelled = false
    getArchitectLeaderboard()
      .then((data) => {
        if (!cancelled && data?.windows?.['1Y']?.entries) {
          setAdvisorSummary(data.windows['1Y'].entries)
        }
      })
      .catch((err) => {
        if (!cancelled) {
          console.error('Failed to fetch advisor summary:', err)
        }
      })

    return () => { cancelled = true }
  }, [firmId, isFirmAdmin])

  // Fetch advisor book data when a specific advisor is selected
  useEffect(() => {
    if (!firmId || selectedAdvisor === ALL_ADVISORS) {
      setAdvisorBookData(null)
      return
    }

    // Convert advisor name to ID format (e.g., "Travis Penfield" → "travis_penfield")
    const advisorId = selectedAdvisor.toLowerCase().replace(/\s+/g, '_')

    let cancelled = false
    setIsLoadingAdvisor(true)

    getAdvisorBook(advisorId)
      .then((data) => {
        if (!cancelled) {
          setAdvisorBookData(data)
          setIsLoadingAdvisor(false)
        }
      })
      .catch((err) => {
        if (!cancelled) {
          console.error('Failed to fetch advisor book:', err)
          setAdvisorBookData(null)
          setIsLoadingAdvisor(false)
        }
      })

    return () => { cancelled = true }
  }, [firmId, selectedAdvisor])

  // Get clients list - use advisor book clients when advisor selected, otherwise firm book
  const clientsList = useMemo(() => {
    if (selectedAdvisor !== ALL_ADVISORS && advisorBookData?.clients) {
      // Map advisor clients to ClientOption format
      const mapped = advisorBookData.clients.map(c => ({
        key: c.client_key,
        name: c.client_name,
        aua: c.aua,
      }))
      console.log('[ClientsTab] clientsList from advisor book:', mapped.length, 'clients')
      return mapped
    }
    console.log('[ClientsTab] clientsList from firm book:', bookData?.clients?.length ?? 0, 'clients')
    return bookData?.clients ?? []
  }, [selectedAdvisor, advisorBookData, bookData])

  // Get selected advisor name for display
  const selectedAdvisorName = useMemo(() => {
    if (selectedAdvisor === ALL_ADVISORS) return 'All Advisors'
    if (advisorBookData?.book_name) return advisorBookData.book_name
    const advisor = advisorSummary.find(a => a.name === selectedAdvisor)
    return advisor?.name ?? selectedAdvisor
  }, [selectedAdvisor, advisorSummary, advisorBookData])

  // Filter clients based on search query
  const filteredClients = useMemo(() => {
    if (!searchQuery.trim()) return clientsList
    const query = searchQuery.toLowerCase()
    return clientsList.filter(c => c.name.toLowerCase().includes(query))
  }, [searchQuery, clientsList])

  // Calculate relationship years - compute once when client data changes
  // Use state to store computed value and update in effect to avoid impure render
  const [clientRelationshipYears, setClientRelationshipYears] = useState(0)
  useEffect(() => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const rawDetail = clientDetailData as any
    if (!rawDetail?.summary?.relationship_start_date) {
      setClientRelationshipYears(0)
      return
    }
    const startDate = new Date(rawDetail.summary.relationship_start_date).getTime()
    const years = (Date.now() - startDate) / (365.25 * 24 * 60 * 60 * 1000)
    setClientRelationshipYears(years)
  }, [clientDetailData])

  if (!firmId) {
    return (
      <Panel variant="chart">
        <PanelContent className="py-12 text-center">
          <p className="text-white/60">Select a partner to view client data</p>
        </PanelContent>
      </Panel>
    )
  }

  if (isLoading) {
    return <LoadingInline className="py-12" />
  }

  if (error) {
    return (
      <Panel variant="chart">
        <PanelContent className="py-12 text-center">
          <p className="text-red-400">Error: {error}</p>
        </PanelContent>
      </Panel>
    )
  }

  // Select data based on view mode
  // Check that clientDetailData has the expected structure
  // Note: Client detail files use different schema (summary vs headline, exposure.tax vs tax)
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const rawClientDetail = clientDetailData as any
  const hasValidClientDetail = clientDetailData && (rawClientDetail?.summary || clientDetailData.headline)
  const isClientView = viewMode === 'client' && selectedClient && hasValidClientDetail
  const isAdvisorView = selectedAdvisor !== ALL_ADVISORS && advisorBookData

  // Default fallback values
  const defaultHeadline: ClientsTabHeadline = { total_aua: 0, account_count: 0, client_count: 0, fee_rate_pct: 0, income_yield_pct: 0 }
  const defaultTax: ClientsTabTax = { taxable: 0, taxable_pct: 0, tax_deferred: 0, tax_deferred_pct: 0, tax_free: 0, tax_free_pct: 0, capital_gains_ttm: 0 }
  const defaultIncomeFees: ClientsTabIncomeFees = { dividends_ttm: 0, interest_ttm: 0, total_income_ttm: 0, income_yield_pct: 0, management_fees_ttm: 0, fee_rate_pct: 0 }
  const defaultPortfolio: ClientsTabPortfolio = { allocation: [], weighted_expense_ratio: 0, unique_holdings: 0, top_5_concentration_pct: 0 }
  const defaultEngagement: ClientsTabEngagement = { trading_buys_ttm: 0, trading_sells_ttm: 0, net_flows_ttm: 0, avg_relationship_years: 0, active_clients_pct: 0 }

  // Map client detail data (different schema) to panel component types
  // Client detail has: summary, exposure.tax, snapshots, timeseries
  const clientHeadline: ClientsTabHeadline | null = rawClientDetail?.summary ? {
    total_aua: rawClientDetail.summary.total_aua ?? 0,
    account_count: rawClientDetail.summary.account_count ?? 0,
    client_count: 1, // Single client
    fee_rate_pct: 0, // Not available in client detail
    income_yield_pct: 0, // Not available in client detail
  } : null

  const clientTax: ClientsTabTax | null = rawClientDetail?.exposure?.tax ? {
    taxable: rawClientDetail.exposure.tax.taxable ?? 0,
    taxable_pct: rawClientDetail.exposure.tax.taxable_pct ?? 0,
    tax_deferred: rawClientDetail.exposure.tax.tax_deferred ?? 0,
    tax_deferred_pct: rawClientDetail.exposure.tax.tax_deferred_pct ?? 0,
    tax_free: rawClientDetail.exposure.tax.tax_free ?? 0,
    tax_free_pct: rawClientDetail.exposure.tax.tax_free_pct ?? 0,
    capital_gains_ttm: 0, // Not available
  } : null

  // Calculate net flows from timeseries if available
  const clientNetFlowsTTM = rawClientDetail?.timeseries?.data?.slice(-12).reduce(
    (sum: number, d: { net_flows?: number }) => sum + (d.net_flows ?? 0), 0
  ) ?? 0

  const clientEngagement: ClientsTabEngagement | null = rawClientDetail?.summary ? {
    trading_buys_ttm: 0, // Not available
    trading_sells_ttm: 0, // Not available
    net_flows_ttm: clientNetFlowsTTM,
    avg_relationship_years: clientRelationshipYears,
    active_clients_pct: 100, // Single client, assume active
  } : null

  // Map advisor book data to existing panel component types
  const advisorHeadline: ClientsTabHeadline | null = advisorBookData ? {
    total_aua: advisorBookData.summary.total_aua,
    account_count: advisorBookData.summary.account_count,
    client_count: advisorBookData.summary.client_count,
    fee_rate_pct: advisorBookData.income_fees.avg_fee_rate_pct,
    income_yield_pct: advisorBookData.income_fees.avg_income_yield_pct,
  } : null

  const advisorTax: ClientsTabTax | null = advisorBookData ? {
    taxable: advisorBookData.tax_exposure.taxable,
    taxable_pct: advisorBookData.tax_exposure.taxable_pct,
    tax_deferred: advisorBookData.tax_exposure.tax_deferred,
    tax_deferred_pct: advisorBookData.tax_exposure.tax_deferred_pct,
    tax_free: advisorBookData.tax_exposure.tax_free,
    tax_free_pct: advisorBookData.tax_exposure.tax_free_pct,
    capital_gains_ttm: 0, // Not available in advisor book
  } : null

  const advisorIncomeFees: ClientsTabIncomeFees | null = advisorBookData ? {
    dividends_ttm: 0, // Not available in advisor book (only total income)
    interest_ttm: 0, // Not available in advisor book
    total_income_ttm: advisorBookData.income_fees.income_total_ttm,
    income_yield_pct: advisorBookData.income_fees.avg_income_yield_pct,
    management_fees_ttm: advisorBookData.income_fees.fees_total_ttm,
    fee_rate_pct: advisorBookData.income_fees.avg_fee_rate_pct,
  } : null

  const advisorPortfolio: ClientsTabPortfolio | null = advisorBookData ? {
    allocation: advisorBookData.portfolio_composition.asset_allocation.map(a => ({
      name: a.label,
      pct: a.pct,
    })),
    weighted_expense_ratio: advisorBookData.portfolio_composition.avg_expense_ratio,
    unique_holdings: 0, // Not available in advisor book
    top_5_concentration_pct: 0, // Not available in advisor book
  } : null

  const advisorEngagement: ClientsTabEngagement | null = advisorBookData ? {
    trading_buys_ttm: 0, // Not available in advisor book
    trading_sells_ttm: 0, // Not available in advisor book
    net_flows_ttm: advisorBookData.engagement.net_flows_ttm,
    avg_relationship_years: advisorBookData.engagement.avg_tenure_days / 365,
    active_clients_pct: 100, // Not available in advisor book, assume 100%
  } : null

  // Select appropriate data source: client detail > advisor book > firm book > defaults
  // Note: Client detail uses mapped values (clientHeadline, clientTax, etc.) due to different schema
  const headlineData: ClientsTabHeadline = isClientView
    ? (clientHeadline ?? defaultHeadline)
    : isAdvisorView
    ? (advisorHeadline ?? defaultHeadline)
    : (bookData?.headline ?? defaultHeadline)

  const taxData: ClientsTabTax = isClientView
    ? (clientTax ?? defaultTax)
    : isAdvisorView
    ? (advisorTax ?? defaultTax)
    : (bookData?.tax ?? defaultTax)

  const incomeFeesData: ClientsTabIncomeFees = isClientView
    ? defaultIncomeFees // Client detail doesn't have income/fees breakdown
    : isAdvisorView
    ? (advisorIncomeFees ?? defaultIncomeFees)
    : (bookData?.income_fees ?? defaultIncomeFees)

  const portfolioData: ClientsTabPortfolio = isClientView
    ? defaultPortfolio // Client detail doesn't have portfolio composition
    : isAdvisorView
    ? (advisorPortfolio ?? defaultPortfolio)
    : (bookData?.portfolio ?? defaultPortfolio)

  const engagementData: ClientsTabEngagement = isClientView
    ? (clientEngagement ?? defaultEngagement)
    : isAdvisorView
    ? (advisorEngagement ?? defaultEngagement)
    : (bookData?.engagement ?? defaultEngagement)

  const handleClientSelect = (client: ClientOption) => {
    console.log('[ClientsTab] handleClientSelect called:', client)
    setSelectedClient(client)
    setSearchQuery('')
    setIsDropdownOpen(false)
  }

  return (
    <Panel variant="chart" className="p-0">
      {/* Header Bar: View Mode Toggle + Advisor Picker (firm admin) + Client Picker */}
      <div className="flex items-center gap-4 p-4 border-b border-white/10">
        {/* View Mode Toggle */}
        <div className="flex items-center bg-white/10 rounded-lg p-1">
          <button
            onClick={() => {
              setViewMode('book')
              setSelectedClient(null)
            }}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-sm font-medium transition-all ${
              viewMode === 'book'
                ? 'bg-[hsl(var(--primary))] text-white'
                : 'text-white/60 hover:text-white/80 hover:bg-white/10'
            }`}
          >
            <Building2 size={14} />
            Book
          </button>
          <button
            onClick={() => setViewMode('client')}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-sm font-medium transition-all ${
              viewMode === 'client'
                ? 'bg-[hsl(var(--primary))] text-white'
                : 'text-white/60 hover:text-white/80 hover:bg-white/10'
            }`}
          >
            <User size={14} />
            Client
          </button>
        </div>

        {/* Advisor Picker - only for firm admin */}
        {isFirmAdmin && (
          <div className="relative">
            <button
              onClick={() => setIsAdvisorDropdownOpen(!isAdvisorDropdownOpen)}
              className="flex items-center gap-2 px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-sm text-white hover:bg-white/10 hover:border-white/20 transition-colors"
            >
              <Users size={14} className="text-white/50" />
              <span className="max-w-[140px] truncate">{selectedAdvisorName}</span>
              <ChevronDown size={14} className={`text-white/50 transition-transform ${isAdvisorDropdownOpen ? 'rotate-180' : ''}`} />
            </button>

            {/* Advisor Dropdown */}
            {isAdvisorDropdownOpen && (
              <div className="absolute top-full left-0 mt-1 bg-[#1e1e2d] border border-white/20 rounded-lg shadow-xl z-50 min-w-[200px] max-h-64 overflow-y-auto">
                {/* All Advisors option */}
                <div
                  onClick={() => {
                    setSelectedAdvisor(ALL_ADVISORS)
                    setIsAdvisorDropdownOpen(false)
                  }}
                  className={`px-3 py-2.5 cursor-pointer hover:bg-white/10 transition-colors ${
                    selectedAdvisor === ALL_ADVISORS ? 'bg-white/15' : ''
                  }`}
                >
                  <span className="text-sm text-white font-medium">All Advisors</span>
                </div>
                <div className="border-t border-white/10" />
                {/* Individual advisors - sorted by AUA descending */}
                {[...advisorSummary].sort((a, b) => b.total_aua - a.total_aua).map((advisor) => (
                  <div
                    key={advisor.name}
                    onClick={() => {
                      setSelectedAdvisor(advisor.name)
                      setIsAdvisorDropdownOpen(false)
                    }}
                    className={`px-3 py-2.5 cursor-pointer hover:bg-white/10 transition-colors ${
                      selectedAdvisor === advisor.name ? 'bg-white/15' : ''
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-white">{advisor.name}</span>
                      <span className="text-xs text-white/50">{formatCurrency(advisor.total_aua)}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Client Picker - always visible */}
        <div className="relative flex-1 max-w-md">
          <div
            className={`flex items-center gap-2 border rounded-lg px-3 py-2 transition-colors ${
              viewMode === 'client'
                ? 'bg-white/10 border-white/20 cursor-pointer hover:border-white/30'
                : 'bg-white/5 border-white/10 cursor-pointer hover:border-white/20'
            }`}
            onClick={() => {
              if (viewMode === 'book') setViewMode('client')
              setIsDropdownOpen(!isDropdownOpen)
            }}
          >
            <Search size={14} className="text-white/50" />
            <input
              type="text"
              placeholder={selectedClient ? selectedClient.name : "Search clients..."}
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value)
                if (viewMode === 'book') setViewMode('client')
                setIsDropdownOpen(true)
              }}
              onClick={(e) => {
                e.stopPropagation()
                if (viewMode === 'book') setViewMode('client')
                setIsDropdownOpen(true)
              }}
              className="flex-1 bg-transparent text-sm text-white placeholder-white/50 outline-none"
            />
            <ChevronDown size={14} className={`text-white/50 transition-transform ${isDropdownOpen ? 'rotate-180' : ''}`} />
          </div>

          {/* Dropdown */}
          {isDropdownOpen && (
            <div className="absolute top-full left-0 right-0 mt-1 bg-[#1e1e2d] border border-white/20 rounded-lg shadow-xl z-50 max-h-64 overflow-y-auto">
              {filteredClients.length === 0 ? (
                <div className="px-3 py-4 text-sm text-white/50 text-center">
                  No clients found
                </div>
              ) : (
                filteredClients.map((client) => (
                  <div
                    key={client.key}
                    onClick={() => handleClientSelect(client)}
                    className={`px-3 py-2.5 cursor-pointer hover:bg-white/10 transition-colors ${
                      selectedClient?.key === client.key ? 'bg-white/15' : ''
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-white">{client.name}</span>
                      <span className="text-xs text-white/60">{formatCurrency(client.aua)}</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </div>

        {/* Selected advisor/client badge */}
        {(selectedAdvisor !== ALL_ADVISORS || selectedClient) && (
          <div className="text-sm text-white/70 flex items-center gap-2">
            {selectedClient ? (
              <>
                Viewing: <span className="text-white font-medium">{selectedClient.name}</span>
                {isLoadingClient && <span className="text-white/50 text-xs">(Loading...)</span>}
              </>
            ) : selectedAdvisor !== ALL_ADVISORS && (
              <>
                Advisor: <span className="text-white font-medium">{selectedAdvisorName}</span>
                {isLoadingAdvisor && <span className="text-white/50 text-xs">(Loading...)</span>}
              </>
            )}
          </div>
        )}
      </div>

      {/* Advisor Summary Table - Show when "All Advisors" selected and firm admin */}
      {isFirmAdmin && selectedAdvisor === ALL_ADVISORS && advisorSummary.length > 0 && (
        <div className="p-4 border-b border-white/10">
          <AdvisorSummaryTable
            data={advisorSummary}
            onSelectAdvisor={(advisorName) => {
              setSelectedAdvisor(advisorName)
            }}
          />
        </div>
      )}

      {/* Content Area - always visible */}
      <div className="p-4 space-y-4">
        {/* Top Row: AI Summary + Headline Numbers */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <SubPanel>
            <SubPanelHeader title="AI Executive Summary" />
            <div className="flex items-center justify-center h-[140px]">
              <div className="flex flex-col items-center">
                <Sparkles size={28} className="text-[hsl(var(--primary))]/40 mb-2" />
                <p className="text-xs text-white/50 text-center max-w-[200px]">
                  {isClientView
                    ? `AI summary for ${selectedClient?.name} coming soon.`
                    : selectedAdvisor !== ALL_ADVISORS
                    ? `Insights for ${selectedAdvisorName} coming soon.`
                    : "Firm-wide insights coming soon."
                  }
                </p>
              </div>
            </div>
          </SubPanel>
          <SubPanel>
            <SubPanelHeader title="Headline Numbers" />
            <HeadlineNumbersContent data={headlineData} isClientView={!!isClientView} />
          </SubPanel>
        </div>

        {/* Bottom Row: 4 equal panels */}
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
          <SubPanel>
            <SubPanelHeader title="Tax Intelligence" />
            <TaxIntelligenceContent data={taxData} />
          </SubPanel>
          <SubPanel>
            <SubPanelHeader title="Income & Fees" />
            <IncomeFeesContent data={incomeFeesData} />
          </SubPanel>
          <SubPanel>
            <SubPanelHeader title="Portfolio Composition" />
            <PortfolioCompositionContent data={portfolioData} />
          </SubPanel>
          <SubPanel>
            <SubPanelHeader title="Engagement Metrics" />
            <EngagementMetricsContent data={engagementData} />
          </SubPanel>
        </div>
      </div>
    </Panel>
  )
}

// ============================================================================
// SUB-PANEL COMPONENTS (Internal containers within the main panel)
// ============================================================================

function PanelContent({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  return <div className={className}>{children}</div>
}

function SubPanel({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={`bg-white/5 rounded-lg border border-white/10 overflow-hidden ${className}`}>
      {children}
    </div>
  )
}

function SubPanelHeader({ title }: { title: string }) {
  return (
    <div className="px-4 py-2.5 bg-[hsl(var(--bg-header))] rounded-t-lg">
      <h3 className="text-xs font-semibold text-white uppercase tracking-wide">{title}</h3>
    </div>
  )
}

// ============================================================================
// CONTENT COMPONENTS (Just the inner content, no panel wrapper)
// ============================================================================

/** Headline Numbers Content */
function HeadlineNumbersContent({ data, isClientView }: { data: ClientsTabHeadline; isClientView?: boolean }) {
  const metrics = isClientView ? [
    { label: 'Total AUA', value: formatCurrency(data.total_aua), icon: DollarSign },
    { label: 'Accounts', value: data.account_count.toLocaleString(), icon: Wallet },
    { label: 'Fee Rate', value: `${data.fee_rate_pct.toFixed(2)}%`, icon: Receipt },
    { label: 'Income Yield', value: `${data.income_yield_pct.toFixed(2)}%`, icon: TrendingUp },
  ] : [
    { label: 'Total AUA', value: formatCurrency(data.total_aua), icon: DollarSign },
    { label: 'Accounts', value: data.account_count.toLocaleString(), icon: Wallet },
    { label: 'Clients', value: data.client_count.toLocaleString(), icon: Users },
    { label: 'Fee Rate', value: `${data.fee_rate_pct.toFixed(2)}%`, icon: Receipt },
    { label: 'Income Yield', value: `${data.income_yield_pct.toFixed(2)}%`, icon: TrendingUp },
  ]

  return (
    <div className="p-3">
      <div className="grid grid-cols-2 gap-2">
        {/* Total AUA - large, spans full width */}
        <div className="col-span-2 bg-white/5 rounded-lg p-2.5 text-center">
          <p className="text-xl font-bold text-white">{metrics[0].value}</p>
          <p className="text-[10px] text-white/50">{metrics[0].label}</p>
        </div>
        {/* Other metrics - 2x2 grid */}
        {metrics.slice(1).map((metric, i) => (
          <div key={i} className="bg-white/5 rounded-lg p-2 flex items-center gap-2">
            <metric.icon size={14} className="text-white/40 flex-shrink-0" />
            <div>
              <p className="text-sm font-semibold text-white">{metric.value}</p>
              <p className="text-[10px] text-white/50">{metric.label}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// ============================================================================
// BOTTOM ROW CONTENT COMPONENTS
// ============================================================================

const TAX_COLORS = ['#EF4444', '#F59E0B', '#10B981'] // Taxable, Deferred, Free

/** Tax Intelligence Content */
function TaxIntelligenceContent({ data }: { data: ClientsTabTax }) {
  const pieData = [
    { name: 'Taxable', value: data.taxable_pct, amount: data.taxable },
    { name: 'Tax-Deferred', value: data.tax_deferred_pct, amount: data.tax_deferred },
    { name: 'Tax-Free', value: data.tax_free_pct, amount: data.tax_free },
  ]

  return (
    <div className="p-4">
      {/* Pie Chart */}
      <div className="flex justify-center">
        <ResponsiveContainer width="100%" height={140}>
          <PieChart>
            <Pie
              data={pieData}
              cx="50%"
              cy="50%"
              innerRadius={40}
              outerRadius={60}
              dataKey="value"
              stroke="rgba(0,0,0,0.3)"
              strokeWidth={1}
            >
              {pieData.map((_, i) => (
                <Cell key={i} fill={TAX_COLORS[i]} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Legend */}
      <div className="space-y-1.5 mt-3">
        {pieData.map((item, i) => (
          <div key={i} className="flex items-center justify-between text-xs">
            <div className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: TAX_COLORS[i] }} />
              <span className="text-white/70">{item.name}</span>
            </div>
            <span className="text-white/90 font-medium">{item.value}%</span>
          </div>
        ))}
      </div>

      {/* Capital Gains callout */}
      <div className="mt-4 pt-3 border-t border-white/10">
        <div className="flex items-center justify-between text-xs">
          <span className="text-white/50">TTM Capital Gains</span>
          <span className="text-white/80 font-medium">{formatCurrency(data.capital_gains_ttm)}</span>
        </div>
      </div>
    </div>
  )
}

/** Income & Fees Content */
function IncomeFeesContent({ data }: { data: ClientsTabIncomeFees }) {
  return (
    <div className="p-4">
      {/* Income Section */}
      <div className="space-y-2">
        <div className="flex items-center gap-2 text-white/50 text-xs">
          <PiggyBank size={14} />
          <span>TTM Income</span>
        </div>
        <div className="bg-white/5 rounded-lg p-2.5">
          <p className="text-base font-bold text-[#10B981]">{formatCurrency(data.total_income_ttm)}</p>
          <div className="flex justify-between text-[10px] text-white/50 mt-1">
            <span>Div: {formatNumberTo3Digits(data.dividends_ttm, { unit: '$' })}</span>
            <span>Int: {formatNumberTo3Digits(data.interest_ttm, { unit: '$' })}</span>
          </div>
        </div>
        <div className="flex justify-between text-xs">
          <span className="text-white/50">Income Yield</span>
          <span className="text-[#10B981] font-medium">{data.income_yield_pct.toFixed(2)}%</span>
        </div>
      </div>

      {/* Fees Section */}
      <div className="space-y-2 mt-4">
        <div className="flex items-center gap-2 text-white/50 text-xs">
          <Receipt size={14} />
          <span>TTM Fees</span>
        </div>
        <div className="bg-white/5 rounded-lg p-2.5">
          <p className="text-base font-bold text-white">{formatCurrency(data.management_fees_ttm)}</p>
          <p className="text-[10px] text-white/50 mt-1">Management Fees</p>
        </div>
        <div className="flex justify-between text-xs">
          <span className="text-white/50">Fee Rate</span>
          <span className="text-white/80 font-medium">{data.fee_rate_pct.toFixed(2)}%</span>
        </div>
      </div>
    </div>
  )
}

/** Portfolio Composition Content */
function PortfolioCompositionContent({ data }: { data: ClientsTabPortfolio }) {
  const ALLOCATION_COLORS = ['#3B82F6', '#8B5CF6', '#EC4899', '#F59E0B', '#6B7280']

  return (
    <div className="p-4">
      {/* Allocation bars */}
      <div className="space-y-2.5">
        {data.allocation.map((item, i) => (
          <div key={i} className="space-y-1">
            <div className="flex justify-between text-xs">
              <span className="text-white/70">{item.name}</span>
              <span className="text-white/90 font-medium">{item.pct}%</span>
            </div>
            <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
              <div
                className="h-full rounded-full transition-all"
                style={{ width: `${item.pct}%`, backgroundColor: ALLOCATION_COLORS[i] }}
              />
            </div>
          </div>
        ))}
      </div>

      {/* Metrics */}
      <div className="pt-3 border-t border-white/10 space-y-1.5 mt-4">
        <div className="flex items-center justify-between text-xs">
          <span className="text-white/50">Holdings</span>
          <span className="text-white/80 font-medium">{data.unique_holdings.toLocaleString()}</span>
        </div>
        <div className="flex items-center justify-between text-xs">
          <span className="text-white/50">Top 5 Conc.</span>
          <span className="text-white/80 font-medium">{data.top_5_concentration_pct}%</span>
        </div>
        <div className="flex items-center justify-between text-xs">
          <span className="text-white/50">Avg ER</span>
          <span className="text-white/80 font-medium">{data.weighted_expense_ratio.toFixed(2)}%</span>
        </div>
      </div>
    </div>
  )
}

/** Engagement Metrics Content */
function EngagementMetricsContent({ data }: { data: ClientsTabEngagement }) {
  return (
    <div className="p-4">
      {/* Net Flows */}
      <div className="bg-white/5 rounded-lg p-3 text-center">
        <p className={`text-lg font-bold ${data.net_flows_ttm >= 0 ? 'text-[#10B981]' : 'text-[#EF4444]'}`}>
          {data.net_flows_ttm >= 0 ? '+' : ''}{formatCurrency(data.net_flows_ttm)}
        </p>
        <p className="text-[10px] text-white/50 mt-1">TTM Net Flows</p>
      </div>

      {/* Trading Activity */}
      <div className="space-y-2 mt-4">
        <div className="flex items-center gap-2 text-white/50 text-xs">
          <Activity size={14} />
          <span>TTM Trading</span>
        </div>
        <div className="grid grid-cols-2 gap-2">
          <div className="bg-white/5 rounded-lg p-2 text-center">
            <p className="text-sm font-semibold text-[#10B981]">{data.trading_buys_ttm.toLocaleString()}</p>
            <p className="text-[10px] text-white/50">Buys</p>
          </div>
          <div className="bg-white/5 rounded-lg p-2 text-center">
            <p className="text-sm font-semibold text-[#EF4444]">{data.trading_sells_ttm.toLocaleString()}</p>
            <p className="text-[10px] text-white/50">Sells</p>
          </div>
        </div>
      </div>

      {/* Relationship Metrics */}
      <div className="pt-3 border-t border-white/10 space-y-1.5 mt-4">
        <div className="flex items-center justify-between text-xs">
          <span className="text-white/50">Avg Tenure</span>
          <span className="text-white/80 font-medium">{data.avg_relationship_years.toFixed(2)} yrs</span>
        </div>
        <div className="flex items-center justify-between text-xs">
          <span className="text-white/50">Active</span>
          <span className="text-[#10B981] font-medium">{data.active_clients_pct}%</span>
        </div>
      </div>
    </div>
  )
}

// ============================================================================
// ADVISOR SUMMARY TABLE (Firm Admin View)
// ============================================================================

interface AdvisorSummaryTableProps {
  data: LeaderboardEntry[]
  onSelectAdvisor: (advisorName: string) => void
}

/** Advisor Summary Table - Shows when "All Advisors" is selected */
function AdvisorSummaryTable({ data, onSelectAdvisor }: AdvisorSummaryTableProps) {
  return (
    <SubPanel>
      <SubPanelHeader title="Advisor Summary" />
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-white/10">
              <th className="text-left text-[10px] font-medium text-white/50 uppercase tracking-wide px-4 py-2">Advisor</th>
              <th className="text-right text-[10px] font-medium text-white/50 uppercase tracking-wide px-4 py-2">AUA</th>
              <th className="text-right text-[10px] font-medium text-white/50 uppercase tracking-wide px-4 py-2">Clients</th>
              <th className="text-right text-[10px] font-medium text-white/50 uppercase tracking-wide px-4 py-2">NNA (1Y)</th>
              <th className="text-right text-[10px] font-medium text-white/50 uppercase tracking-wide px-4 py-2">Growth</th>
              <th className="w-8"></th>
            </tr>
          </thead>
          <tbody>
            {data.slice(0, 10).map((advisor, i) => (
              <tr
                key={advisor.name}
                onClick={() => onSelectAdvisor(advisor.name)}
                className="border-b border-white/5 hover:bg-white/5 cursor-pointer transition-colors group"
              >
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] text-white/30 w-4">{i + 1}</span>
                    <span className="text-sm text-white font-medium">{advisor.name}</span>
                  </div>
                </td>
                <td className="text-right px-4 py-3">
                  <span className="text-sm text-white/80 font-mono">{formatCurrency(advisor.total_aua)}</span>
                </td>
                <td className="text-right px-4 py-3">
                  <span className="text-sm text-white/70">{advisor.client_count.toLocaleString()}</span>
                </td>
                <td className="text-right px-4 py-3">
                  <span className={`text-sm font-mono ${advisor.nna >= 0 ? 'text-[#10B981]' : 'text-[#EF4444]'}`}>
                    {advisor.nna >= 0 ? '+' : ''}{formatCurrency(advisor.nna)}
                  </span>
                </td>
                <td className="text-right px-4 py-3">
                  <span className={`text-sm font-medium ${advisor.aua_growth_pct >= 0 ? 'text-[#10B981]' : 'text-[#EF4444]'}`}>
                    {advisor.aua_growth_pct >= 0 ? '+' : ''}{advisor.aua_growth_pct.toFixed(1)}%
                  </span>
                </td>
                <td className="px-2 py-3">
                  <ChevronRight size={14} className="text-white/30 group-hover:text-white/60 transition-colors" />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {data.length > 10 && (
        <div className="px-4 py-2 text-center text-[10px] text-white/40 border-t border-white/5">
          Showing top 10 of {data.length} advisors
        </div>
      )}
    </SubPanel>
  )
}
