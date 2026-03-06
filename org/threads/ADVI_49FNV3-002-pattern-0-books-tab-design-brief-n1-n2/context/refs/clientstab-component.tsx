/**
 * Books Tab - Advisor Intelligence (Y15: L2/L3/L4 MVP)
 *
 * Admin/internal only (gated by isInternal() || isDev()).
 *
 * Drill hierarchy:
 *   All Advisors (summary table) -> L2 (advisor book) -> L3 (client detail) -> L4 (inline account drill)
 *
 * L2: Advisor Book Summary, Tax Exposure, Engagement, Clients table
 * L3: Client Summary, Accounts, Tax Intelligence, Taxable Open Lots, Engagement
 * L4: Inline expansion inside L3 (account detail + scoped lots)
 *
 * HIDDEN (per task order): income_fees, portfolio_composition — not in DOM.
 */

import { useState, useEffect, useMemo } from 'react'
import { Panel, PanelHeader, PanelContent } from '@/ui/components/panels'
import { LoadingInline } from '@/components/LoadingSpinner'
import {
  ChevronRight,
  ChevronDown,
  ArrowLeft,
  Users,
  Search,
  X,
} from 'lucide-react'
import { formatCurrency } from '@/lib/universalNumberFormatter'
import { getArchitectLeaderboard, getAdvisorBook, getBooksClientDetail } from '@/api/endpoints/advisor-intelligence'
import { useAuth } from '@/hooks/useAuth'
import type {
  LeaderboardEntry,
  AdvisorBookResponse,
  AdvisorClient,
  BooksClientDetailResponse,
  BooksClientAccount,
  OpenLot,
  CostBasisYear,
  GainPosition,
} from '../types'

interface BooksTabProps {
  firmId: string
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export function BooksTab({ firmId }: BooksTabProps) {
  const { isInternal, isDev } = useAuth()
  const isFirmAdmin = isInternal() || isDev()

  // Advisor list (from leaderboard)
  const [advisorSummary, setAdvisorSummary] = useState<LeaderboardEntry[]>([])
  const [isLoading, setIsLoading] = useState(true)

  // L2: Advisor book
  const [selectedAdvisorId, setSelectedAdvisorId] = useState<string | null>(null)
  const [advisorBookData, setAdvisorBookData] = useState<AdvisorBookResponse | null>(null)
  const [isLoadingAdvisor, setIsLoadingAdvisor] = useState(false)

  // L3: Client detail
  const [selectedClientKey, setSelectedClientKey] = useState<string | null>(null)
  const [clientDetailData, setClientDetailData] = useState<BooksClientDetailResponse | null>(null)
  const [isLoadingClient, setIsLoadingClient] = useState(false)

  // L4: Inline account drill
  const [selectedAccountId, setSelectedAccountId] = useState<string | null>(null)

  // Advisor dropdown
  const [isAdvisorDropdownOpen, setIsAdvisorDropdownOpen] = useState(false)

  // Fetch advisor list
  useEffect(() => {
    if (!firmId || !isFirmAdmin) {
      setIsLoading(false)
      return
    }
    setIsLoading(true)
    getArchitectLeaderboard()
      .then((data) => {
        if (data?.windows?.['1Y']?.entries) {
          setAdvisorSummary(data.windows['1Y'].entries)
        }
        setIsLoading(false)
      })
      .catch((err) => {
        console.error('[BooksTab] Failed to fetch advisor list:', err)
        setIsLoading(false)
      })
  }, [firmId, isFirmAdmin])

  // Fetch advisor book when selected
  useEffect(() => {
    if (!selectedAdvisorId) {
      setAdvisorBookData(null)
      return
    }
    let cancelled = false
    setIsLoadingAdvisor(true)
    getAdvisorBook(selectedAdvisorId)
      .then((data) => {
        if (!cancelled) {
          setAdvisorBookData(data)
          setIsLoadingAdvisor(false)
        }
      })
      .catch((err) => {
        if (!cancelled) {
          console.error('[BooksTab] Failed to fetch advisor book:', err)
          setAdvisorBookData(null)
          setIsLoadingAdvisor(false)
        }
      })
    return () => { cancelled = true }
  }, [selectedAdvisorId])

  // Fetch client detail when selected (L3)
  useEffect(() => {
    if (!selectedClientKey) {
      setClientDetailData(null)
      return
    }
    let cancelled = false
    setIsLoadingClient(true)
    getBooksClientDetail(selectedClientKey)
      .then((data) => {
        if (!cancelled) {
          setClientDetailData(data)
          setIsLoadingClient(false)
        }
      })
      .catch((err) => {
        if (!cancelled) {
          console.error('[BooksTab] Failed to fetch client detail:', err)
          setClientDetailData(null)
          setIsLoadingClient(false)
        }
      })
    return () => { cancelled = true }
  }, [selectedClientKey])

  // Reset on firm change
  useEffect(() => {
    setSelectedAdvisorId(null)
    setSelectedClientKey(null)
    setSelectedAccountId(null)
    setAdvisorBookData(null)
    setClientDetailData(null)
  }, [firmId])

  // Navigate to L3
  const handleClientClick = (clientKey: string) => {
    setSelectedClientKey(clientKey)
    setSelectedAccountId(null)
  }

  // Navigate back to L2
  const handleBackToL2 = () => {
    setSelectedClientKey(null)
    setClientDetailData(null)
    setSelectedAccountId(null)
  }

  // Navigate back to advisor list
  const handleBackToList = () => {
    setSelectedAdvisorId(null)
    setAdvisorBookData(null)
    setSelectedClientKey(null)
    setClientDetailData(null)
    setSelectedAccountId(null)
  }

  // Select advisor from list or dropdown
  const handleSelectAdvisor = (advisorName: string) => {
    const advisorId = advisorName.toLowerCase().replace(/\s+/g, '_')
    setSelectedAdvisorId(advisorId)
    setSelectedClientKey(null)
    setClientDetailData(null)
    setSelectedAccountId(null)
    setIsAdvisorDropdownOpen(false)
  }

  if (!firmId) {
    return (
      <Panel variant="chart">
        <PanelContent className="py-12 text-center">
          <p className="text-white/60">Select a partner to view books</p>
        </PanelContent>
      </Panel>
    )
  }

  if (isLoading) {
    return <LoadingInline className="py-12" />
  }

  // L3: Client detail view
  if (selectedClientKey) {
    if (isLoadingClient) {
      return <LoadingInline className="py-12" />
    }

    const clientName = advisorBookData?.clients.find(c => c.client_key === selectedClientKey)?.client_name ?? selectedClientKey

    return (
      <div className="flex flex-col gap-4">
        {/* Breadcrumb */}
        <div className="flex items-center gap-2 text-sm">
          <button onClick={handleBackToList} className="text-white/50 hover:text-white transition-colors">
            All Advisors
          </button>
          <span className="text-white/30">/</span>
          <button onClick={handleBackToL2} className="text-white/50 hover:text-white transition-colors">
            {advisorBookData?.book_name ?? 'Advisor'}
          </button>
          <span className="text-white/30">/</span>
          <span className="text-white font-medium">{clientName}</span>
        </div>

        {/* Back button */}
        <button
          onClick={handleBackToL2}
          className="flex items-center gap-1.5 text-sm text-white/60 hover:text-white transition-colors w-fit"
        >
          <ArrowLeft size={14} />
          Back to Book
        </button>

        {clientDetailData ? (
          <L3ClientDetail
            data={clientDetailData}
            clientName={clientName}
            selectedAccountId={selectedAccountId}
            onSelectAccount={setSelectedAccountId}
          />
        ) : (
          <Panel variant="chart">
            <PanelContent className="py-12 text-center">
              <p className="text-white/40">Client detail data not available</p>
            </PanelContent>
          </Panel>
        )}
      </div>
    )
  }

  // L2: Advisor book view
  if (selectedAdvisorId && advisorBookData) {
    return (
      <div className="flex flex-col gap-4">
        {/* Breadcrumb */}
        <div className="flex items-center gap-2 text-sm">
          <button onClick={handleBackToList} className="text-white/50 hover:text-white transition-colors">
            All Advisors
          </button>
          <span className="text-white/30">/</span>
          <span className="text-white font-medium">{advisorBookData.book_name}</span>
        </div>

        {/* Back button */}
        <button
          onClick={handleBackToList}
          className="flex items-center gap-1.5 text-sm text-white/60 hover:text-white transition-colors w-fit"
        >
          <ArrowLeft size={14} />
          All Advisors
        </button>

        <L2AdvisorBook data={advisorBookData} onClientClick={handleClientClick} />
      </div>
    )
  }

  if (selectedAdvisorId && isLoadingAdvisor) {
    return <LoadingInline className="py-12" />
  }

  // Default: Advisor list
  return (
    <div className="flex flex-col gap-4">
      {/* Header with advisor dropdown */}
      {isFirmAdmin && (
        <div className="flex items-center gap-3">
          <div className="relative">
            <button
              onClick={() => setIsAdvisorDropdownOpen(!isAdvisorDropdownOpen)}
              className="flex items-center gap-2 px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-sm text-white hover:bg-white/10 hover:border-white/20 transition-colors"
            >
              <Users size={14} className="text-white/50" />
              <span>Select Advisor</span>
              <ChevronDown size={14} className={`text-white/50 transition-transform ${isAdvisorDropdownOpen ? 'rotate-180' : ''}`} />
            </button>
            {isAdvisorDropdownOpen && (
              <div className="absolute top-full left-0 mt-1 bg-[#1e1e2d] border border-white/20 rounded-lg shadow-xl z-50 min-w-[200px] max-h-64 overflow-y-auto">
                {[...advisorSummary].sort((a, b) => b.total_aua - a.total_aua).map((advisor) => (
                  <div
                    key={advisor.name}
                    onClick={() => handleSelectAdvisor(advisor.name)}
                    className="px-3 py-2.5 cursor-pointer hover:bg-white/10 transition-colors"
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
        </div>
      )}

      {/* Advisor Summary Table */}
      {advisorSummary.length > 0 ? (
        <AdvisorSummaryTable data={advisorSummary} onSelectAdvisor={handleSelectAdvisor} />
      ) : (
        <Panel variant="chart">
          <PanelContent className="py-12 text-center">
            <p className="text-white/40">No advisor data available</p>
          </PanelContent>
        </Panel>
      )}
    </div>
  )
}

// ============================================================================
// L2 — ADVISOR BOOK VIEW
// ============================================================================

function L2AdvisorBook({ data, onClientClick }: { data: AdvisorBookResponse; onClientClick: (clientKey: string) => void }) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
      {/* Panel 1: Book Summary */}
      <Panel variant="chart">
        <PanelHeader title="Advisor Book Summary" />
        <PanelContent>
          <div className="space-y-4">
            {/* Hero metrics */}
            <div className="grid grid-cols-3 gap-3">
              <MetricCard label="Total AUA" value={formatCurrency(data.summary.total_aua)} large />
              <MetricCard label="Clients" value={data.summary.client_count.toLocaleString()} />
              <MetricCard label="Accounts" value={data.summary.account_count.toLocaleString()} />
            </div>

            {/* NNA */}
            <div>
              <p className="text-[10px] text-white/40 uppercase tracking-wide mb-2">Net New Assets</p>
              <div className="grid grid-cols-3 gap-3">
                <NnaMetric label="MTD" value={data.nna.mtd} />
                <NnaMetric label="QTD" value={data.nna.qtd} />
                <NnaMetric label="YTD" value={data.nna.ytd} />
              </div>
            </div>

            {/* Growth */}
            <div>
              <p className="text-[10px] text-white/40 uppercase tracking-wide mb-2">Growth</p>
              <div className="grid grid-cols-2 gap-3">
                <GrowthMetric label="QTD" value={data.growth.qtd_pct} />
                <GrowthMetric label="YTD" value={data.growth.ytd_pct} />
              </div>
            </div>

            {/* Data As Of */}
            <p className="text-[10px] text-white/30">Data as of {data.data_as_of}</p>
          </div>
        </PanelContent>
      </Panel>

      {/* Panel 2: Tax Exposure */}
      <Panel variant="chart">
        <PanelHeader title="Tax Exposure" />
        <PanelContent>
          <div className="space-y-3">
            <TaxRow label="Taxable" amount={data.tax_exposure.taxable} pct={data.tax_exposure.taxable_pct} color="#EF4444" />
            <TaxRow label="Tax Deferred" amount={data.tax_exposure.tax_deferred} pct={data.tax_exposure.tax_deferred_pct} color="#F59E0B" />
            <TaxRow label="Tax Free" amount={data.tax_exposure.tax_free} pct={data.tax_exposure.tax_free_pct} color="#10B981" />
          </div>
        </PanelContent>
      </Panel>

      {/* Panel 3: Engagement */}
      <Panel variant="chart">
        <PanelHeader title="Engagement" />
        <PanelContent>
          <div className="space-y-3">
            <div className="grid grid-cols-3 gap-3">
              <FlowMetric label="Net Flows TTM" value={data.engagement.net_flows_ttm} signed />
              <FlowMetric label="Inflows TTM" value={data.engagement.inflows_ttm} />
              <FlowMetric label="Outflows TTM" value={data.engagement.outflows_ttm} />
            </div>
            <div className="flex items-center justify-between text-xs pt-2 border-t border-white/10">
              <span className="text-white/50">Avg Tenure</span>
              <span className="text-white/80 font-medium">
                {(data.engagement.avg_tenure_days / 365.25).toFixed(1)} yrs
              </span>
            </div>
          </div>
        </PanelContent>
      </Panel>

      {/* Panel 4: Clients Table */}
      <Panel variant="chart">
        <PanelHeader title="Clients" />
        <PanelContent noPadding>
          <ClientsTable clients={data.clients} onClientClick={onClientClick} />
        </PanelContent>
      </Panel>
    </div>
  )
}

// ============================================================================
// L3 — CLIENT DETAIL VIEW
// ============================================================================

interface L3ClientDetailProps {
  data: BooksClientDetailResponse
  clientName: string
  selectedAccountId: string | null
  onSelectAccount: (id: string | null) => void
}

function L3ClientDetail({ data, clientName, selectedAccountId, onSelectAccount }: L3ClientDetailProps) {
  // L3 filters for Taxable Open Lots
  const [lotTermFilter, setLotTermFilter] = useState<'all' | 'short' | 'long'>('all')
  const [lotAccountFilter, setLotAccountFilter] = useState<string>('all')

  // Filtered open lots (L3 Panel 4)
  const filteredLots = useMemo(() => {
    let lots = data.tax?.open_lots ?? []
    if (lotTermFilter !== 'all') {
      const termMatch = lotTermFilter === 'short' ? 'Short' : 'Long'
      lots = lots.filter(l => l.term === termMatch)
    }
    if (lotAccountFilter !== 'all') {
      lots = lots.filter(l => l.account_id === lotAccountFilter)
    }
    return lots
  }, [data.tax?.open_lots, lotTermFilter, lotAccountFilter])

  // L4: Account-scoped lots
  const selectedAccount = useMemo(() => {
    if (!selectedAccountId) return null
    return data.accounts?.find(a => a.account_id === selectedAccountId) ?? null
  }, [data.accounts, selectedAccountId])

  const accountScopedLots = useMemo(() => {
    if (!selectedAccountId) return []
    return (data.tax?.open_lots ?? []).filter(l => l.account_id === selectedAccountId)
  }, [data.tax?.open_lots, selectedAccountId])

  // Unique account IDs for filter dropdown
  const accountIds = useMemo(() => {
    return [...new Set((data.tax?.open_lots ?? []).map(l => l.account_id))]
  }, [data.tax?.open_lots])

  return (
    <div className="flex flex-col gap-4">
      {/* Panel 1: Client Summary */}
      <Panel variant="chart">
        <PanelHeader title="Client Summary" />
        <PanelContent>
          <div className="grid grid-cols-3 gap-4">
            <MetricCard label="Total AUA" value={formatCurrency(data.headline.total_aua)} large />
            <MetricCard label="Accounts" value={data.headline.account_count.toLocaleString()} />
            <MetricCard label="Data As Of" value={data.data_as_of} />
          </div>
        </PanelContent>
      </Panel>

      {/* Panel 2: Accounts Table */}
      <Panel variant="chart">
        <PanelHeader title="Accounts" />
        <PanelContent noPadding>
          <AccountsTable
            accounts={data.accounts ?? []}
            selectedAccountId={selectedAccountId}
            onSelectAccount={onSelectAccount}
          />
        </PanelContent>
      </Panel>

      {/* L4: Inline Account Drill */}
      {selectedAccountId && selectedAccount && (
        <Panel variant="chart">
          <PanelHeader
            title={`Account Detail -- ${selectedAccountId}`}
            actions={
              <button
                onClick={() => onSelectAccount(null)}
                className="flex items-center gap-1 text-xs text-white/50 hover:text-white transition-colors"
              >
                <X size={12} />
                Close
              </button>
            }
          />
          <PanelContent>
            <div className="space-y-4">
              {/* Account Detail */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <MetricCard label="Tax Status" value={selectedAccount.tax_status} />
                <MetricCard label="Total AUA" value={formatCurrency(selectedAccount.total_aua)} />
                <MetricCard label="Cum Inflows" value={formatCurrency(selectedAccount.cum_inflows)} />
                <MetricCard label="Cum Outflows" value={formatCurrency(selectedAccount.cum_outflows)} />
                <NnaMetric label="NNA" value={selectedAccount.nna} />
                <MetricCard label="Positions" value={selectedAccount.num_positions.toLocaleString()} />
              </div>

              {/* Taxable Open Lots (Account-Scoped) */}
              {accountScopedLots.length > 0 && (
                <div>
                  <p className="text-xs font-semibold text-white/70 uppercase tracking-wide mb-2">
                    Taxable Open Lots -- {selectedAccountId}
                  </p>
                  <OpenLotsTable lots={accountScopedLots} />
                </div>
              )}
            </div>
          </PanelContent>
        </Panel>
      )}

      {/* Panel 3: Tax Intelligence */}
      <Panel variant="chart">
        <PanelHeader title="Tax Intelligence" />
        <PanelContent>
          {data.tax ? (
            <TaxIntelligenceL3 tax={data.tax} />
          ) : (
            <p className="text-sm text-white/40 text-center py-4">Tax data not available</p>
          )}
        </PanelContent>
      </Panel>

      {/* Panel 4: Taxable Open Lots */}
      <Panel variant="chart">
        <PanelHeader
          title="Taxable Open Lots"
          actions={
            <div className="flex items-center gap-2">
              {/* Term toggle */}
              <div className="flex gap-0.5 bg-white/10 rounded-lg p-0.5">
                {(['all', 'short', 'long'] as const).map((t) => (
                  <button
                    key={t}
                    onClick={() => setLotTermFilter(t)}
                    className={`px-2 py-1 text-xs font-medium rounded-md transition-colors ${
                      lotTermFilter === t
                        ? 'bg-white/20 text-white'
                        : 'text-white/50 hover:text-white hover:bg-white/10'
                    }`}
                  >
                    {t === 'all' ? 'All' : t === 'short' ? 'Short' : 'Long'}
                  </button>
                ))}
              </div>
              {/* Account filter */}
              {accountIds.length > 1 && (
                <select
                  value={lotAccountFilter}
                  onChange={(e) => setLotAccountFilter(e.target.value)}
                  className="bg-white/10 text-white text-xs rounded-md px-2 py-1 border border-white/10 outline-none"
                >
                  <option value="all">All Accounts</option>
                  {accountIds.map((id) => (
                    <option key={id} value={id}>{id}</option>
                  ))}
                </select>
              )}
            </div>
          }
        />
        <PanelContent noPadding>
          {filteredLots.length > 0 ? (
            <OpenLotsTable lots={filteredLots} />
          ) : (
            <div className="py-6 text-center text-sm text-white/40">
              No taxable open lots{lotTermFilter !== 'all' || lotAccountFilter !== 'all' ? ' matching filters' : ''}
            </div>
          )}
        </PanelContent>
      </Panel>

      {/* Panel 5: Engagement */}
      <Panel variant="chart">
        <PanelHeader title="Engagement" />
        <PanelContent>
          <div className="grid grid-cols-2 gap-4">
            <FlowMetric label="Net Flows TTM" value={data.engagement.net_flows_ttm} signed />
            <div className="bg-white/5 rounded-lg p-3 text-center">
              <p className="text-lg font-bold text-white">
                {data.engagement.avg_relationship_years.toFixed(1)}
              </p>
              <p className="text-[10px] text-white/50 mt-0.5">Avg Relationship Years</p>
            </div>
          </div>
        </PanelContent>
      </Panel>
    </div>
  )
}

// ============================================================================
// SHARED METRIC COMPONENTS
// ============================================================================

function MetricCard({ label, value, large }: { label: string; value: string; large?: boolean }) {
  return (
    <div className="bg-white/5 rounded-lg p-3 text-center">
      <p className={`font-bold text-white ${large ? 'text-xl' : 'text-sm'}`}>{value}</p>
      <p className="text-[10px] text-white/50 mt-0.5">{label}</p>
    </div>
  )
}

function NnaMetric({ label, value }: { label: string; value: number }) {
  const color = value >= 0 ? 'text-[#10B981]' : 'text-[#EF4444]'
  return (
    <div className="bg-white/5 rounded-lg p-3 text-center">
      <p className={`text-sm font-bold ${color}`}>
        {value >= 0 ? '+' : ''}{formatCurrency(value)}
      </p>
      <p className="text-[10px] text-white/50 mt-0.5">{label}</p>
    </div>
  )
}

function GrowthMetric({ label, value }: { label: string; value: number }) {
  const color = value >= 0 ? 'text-[#10B981]' : 'text-[#EF4444]'
  return (
    <div className="bg-white/5 rounded-lg p-3 text-center">
      <p className={`text-sm font-bold ${color}`}>
        {value >= 0 ? '+' : ''}{value.toFixed(1)}%
      </p>
      <p className="text-[10px] text-white/50 mt-0.5">{label}</p>
    </div>
  )
}

function FlowMetric({ label, value, signed }: { label: string; value: number; signed?: boolean }) {
  const color = signed ? (value >= 0 ? 'text-[#10B981]' : 'text-[#EF4444]') : 'text-white'
  return (
    <div className="bg-white/5 rounded-lg p-3 text-center">
      <p className={`text-sm font-bold ${color}`}>
        {signed && value >= 0 ? '+' : ''}{formatCurrency(value)}
      </p>
      <p className="text-[10px] text-white/50 mt-0.5">{label}</p>
    </div>
  )
}

function TaxRow({ label, amount, pct, color }: { label: string; amount: number; pct: number; color: string }) {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2">
        <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: color }} />
        <span className="text-xs text-white/70">{label}</span>
      </div>
      <div className="flex items-center gap-3">
        <span className="text-xs text-white/60">{pct.toFixed(1)}%</span>
        <span className="text-xs text-white font-medium">{formatCurrency(amount)}</span>
      </div>
    </div>
  )
}

// ============================================================================
// CLIENTS TABLE (L2 Panel 4)
// ============================================================================

function ClientsTable({ clients, onClientClick }: { clients: AdvisorClient[]; onClientClick: (key: string) => void }) {
  const sorted = useMemo(() =>
    [...clients].sort((a, b) => b.aua - a.aua),
  [clients])

  if (sorted.length === 0) {
    return <div className="py-6 text-center text-sm text-white/40">No clients</div>
  }

  return (
    <div className="overflow-y-auto" style={{ maxHeight: 320 }}>
      <table className="w-full text-xs">
        <thead className="bg-[hsl(var(--bg-header))] sticky top-0 z-10">
          <tr className="border-b border-white/20">
            <th className="text-left px-4 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Client</th>
            <th className="text-right px-4 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">AUA</th>
            <th className="w-8" />
          </tr>
        </thead>
        <tbody>
          {sorted.map((client) => (
            <tr
              key={client.client_key}
              onClick={() => onClientClick(client.client_key)}
              className="border-b border-white/5 hover:bg-white/5 cursor-pointer transition-colors group"
            >
              <td className="px-4 py-2.5 text-sm text-white font-medium">{client.client_name}</td>
              <td className="px-4 py-2.5 text-right text-white/70">{formatCurrency(client.aua)}</td>
              <td className="px-2 py-2.5">
                <ChevronRight size={14} className="text-white/30 group-hover:text-white/60 transition-colors" />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

// ============================================================================
// ACCOUNTS TABLE (L3 Panel 2)
// ============================================================================

function AccountsTable({ accounts, selectedAccountId, onSelectAccount }: {
  accounts: BooksClientAccount[]
  selectedAccountId: string | null
  onSelectAccount: (id: string | null) => void
}) {
  if (accounts.length === 0) {
    return <div className="py-6 text-center text-sm text-white/40">No accounts</div>
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-xs">
        <thead className="bg-[hsl(var(--bg-header))] sticky top-0 z-10">
          <tr className="border-b border-white/20">
            <th className="text-left px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Account</th>
            <th className="text-left px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Tax Status</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">AUA</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Inflows</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Outflows</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">NNA</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Positions</th>
          </tr>
        </thead>
        <tbody>
          {accounts.map((acct) => {
            const isSelected = acct.account_id === selectedAccountId
            return (
              <tr
                key={acct.account_id}
                onClick={() => onSelectAccount(isSelected ? null : acct.account_id)}
                className={`border-b border-white/5 cursor-pointer transition-colors ${
                  isSelected ? 'bg-white/10' : 'hover:bg-white/5'
                }`}
              >
                <td className="px-3 py-2.5 text-white font-medium">{acct.account_id}</td>
                <td className="px-3 py-2.5 text-white/70">{acct.tax_status}</td>
                <td className="px-3 py-2.5 text-right text-white/80">{formatCurrency(acct.total_aua)}</td>
                <td className="px-3 py-2.5 text-right text-white/60">{formatCurrency(acct.cum_inflows)}</td>
                <td className="px-3 py-2.5 text-right text-white/60">{formatCurrency(acct.cum_outflows)}</td>
                <td className="px-3 py-2.5 text-right">
                  <span className={acct.nna >= 0 ? 'text-[#10B981]' : 'text-[#EF4444]'}>
                    {acct.nna >= 0 ? '+' : ''}{formatCurrency(acct.nna)}
                  </span>
                </td>
                <td className="px-3 py-2.5 text-right text-white/60">{acct.num_positions}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

// ============================================================================
// TAX INTELLIGENCE (L3 Panel 3)
// ============================================================================

function TaxIntelligenceL3({ tax }: { tax: BooksClientDetailResponse['tax'] }) {
  return (
    <div className="space-y-4">
      {/* Tax status breakdown */}
      <div className="space-y-2">
        <TaxRow label="Taxable" amount={tax.taxable} pct={tax.taxable_pct} color="#EF4444" />
        <TaxRow label="Tax Deferred" amount={tax.tax_deferred} pct={tax.tax_deferred_pct} color="#F59E0B" />
        <TaxRow label="Tax Free" amount={tax.tax_free} pct={tax.tax_free_pct} color="#10B981" />
      </div>

      {/* Qualified / Non-Qualified */}
      <div className="border-t border-white/10 pt-3 space-y-2">
        <div className="flex items-center justify-between text-xs">
          <span className="text-white/50">Qualified</span>
          <span className="text-white/80 font-medium">{formatCurrency(tax.qualified_aua)} ({tax.qualified_pct.toFixed(1)}%)</span>
        </div>
        <div className="flex items-center justify-between text-xs">
          <span className="text-white/50">Non-Qualified</span>
          <span className="text-white/80 font-medium">{formatCurrency(tax.non_qualified_aua)} ({tax.non_qualified_pct.toFixed(1)}%)</span>
        </div>
      </div>

      {/* Cost Basis by Year */}
      {tax.cost_basis_by_year.length > 0 && (
        <div className="border-t border-white/10 pt-3">
          <p className="text-[10px] text-white/40 uppercase tracking-wide mb-2">Cost Basis by Year</p>
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-white/10">
                <th className="text-left py-1.5 text-[10px] text-white/50">Year</th>
                <th className="text-right py-1.5 text-[10px] text-white/50">Cost Basis</th>
                <th className="text-right py-1.5 text-[10px] text-white/50">Market Value</th>
                <th className="text-right py-1.5 text-[10px] text-white/50">Unrealized Gain</th>
              </tr>
            </thead>
            <tbody>
              {tax.cost_basis_by_year.map((row: CostBasisYear) => (
                <tr key={row.year} className="border-b border-white/5">
                  <td className="py-1.5 text-white/70">{row.year}</td>
                  <td className="py-1.5 text-right text-white/60">{formatCurrency(row.cost_basis)}</td>
                  <td className="py-1.5 text-right text-white/60">{formatCurrency(row.market_value)}</td>
                  <td className="py-1.5 text-right">
                    <span className={row.unrealized_gain >= 0 ? 'text-[#10B981]' : 'text-[#EF4444]'}>
                      {row.unrealized_gain >= 0 ? '+' : ''}{formatCurrency(row.unrealized_gain)}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Top Gain Positions */}
      {tax.top_gain_positions.length > 0 && (
        <div className="border-t border-white/10 pt-3">
          <p className="text-[10px] text-white/40 uppercase tracking-wide mb-2">Top Gain Positions</p>
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-white/10">
                <th className="text-left py-1.5 text-[10px] text-white/50">Name</th>
                <th className="text-left py-1.5 text-[10px] text-white/50">Ticker</th>
                <th className="text-right py-1.5 text-[10px] text-white/50">Gain</th>
                <th className="text-right py-1.5 text-[10px] text-white/50">Cost Basis</th>
                <th className="text-right py-1.5 text-[10px] text-white/50">Mkt Value</th>
                <th className="text-left py-1.5 text-[10px] text-white/50">Term</th>
              </tr>
            </thead>
            <tbody>
              {tax.top_gain_positions.map((pos: GainPosition, i: number) => (
                <tr key={i} className="border-b border-white/5">
                  <td className="py-1.5 text-white/70 max-w-[120px] truncate">{pos.asset_name}</td>
                  <td className="py-1.5 text-white/50">{pos.ticker ?? '--'}</td>
                  <td className="py-1.5 text-right">
                    <span className={pos.unrealized_gain >= 0 ? 'text-[#10B981]' : 'text-[#EF4444]'}>
                      {formatCurrency(pos.unrealized_gain)}
                    </span>
                  </td>
                  <td className="py-1.5 text-right text-white/60">{formatCurrency(pos.cost_basis)}</td>
                  <td className="py-1.5 text-right text-white/60">{formatCurrency(pos.market_value)}</td>
                  <td className="py-1.5 text-white/50">{pos.term}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

// ============================================================================
// OPEN LOTS TABLE (shared between L3 Panel 4 and L4)
// ============================================================================

function OpenLotsTable({ lots }: { lots: OpenLot[] }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-xs">
        <thead className="bg-[hsl(var(--bg-header))] sticky top-0 z-10">
          <tr className="border-b border-white/20">
            <th className="text-left px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Name</th>
            <th className="text-left px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Ticker</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Qty</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Cost Basis</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Mkt Value</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Gain</th>
            <th className="text-left px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Term</th>
            <th className="text-left px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Acq. Date</th>
          </tr>
        </thead>
        <tbody>
          {lots.map((lot, i) => (
            <tr key={i} className="border-b border-white/5 hover:bg-white/5 transition-colors">
              <td className="px-3 py-2 text-white/70 max-w-[120px] truncate">{lot.asset_name}</td>
              <td className="px-3 py-2 text-white/50">{lot.ticker ?? '--'}</td>
              <td className="px-3 py-2 text-right text-white/60">{lot.quantity.toLocaleString()}</td>
              <td className="px-3 py-2 text-right text-white/60">{formatCurrency(lot.cost_basis)}</td>
              <td className="px-3 py-2 text-right text-white/60">{formatCurrency(lot.market_value)}</td>
              <td className="px-3 py-2 text-right">
                <span className={lot.unrealized_gain >= 0 ? 'text-[#10B981]' : 'text-[#EF4444]'}>
                  {lot.unrealized_gain >= 0 ? '+' : ''}{formatCurrency(lot.unrealized_gain)}
                </span>
              </td>
              <td className="px-3 py-2 text-white/50">{lot.term}</td>
              <td className="px-3 py-2 text-white/50">{lot.acquisition_date ?? '--'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

// ============================================================================
// ADVISOR SUMMARY TABLE (All Advisors view)
// ============================================================================

function AdvisorSummaryTable({ data, onSelectAdvisor }: { data: LeaderboardEntry[]; onSelectAdvisor: (name: string) => void }) {
  return (
    <Panel variant="chart">
      <PanelHeader title="Advisor Summary" />
      <PanelContent noPadding>
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead className="bg-[hsl(var(--bg-header))] sticky top-0 z-10">
              <tr className="border-b border-white/20">
                <th className="text-left px-4 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Advisor</th>
                <th className="text-right px-4 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">AUA</th>
                <th className="text-right px-4 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Clients</th>
                <th className="text-right px-4 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">NNA (1Y)</th>
                <th className="text-right px-4 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Growth</th>
                <th className="w-8" />
              </tr>
            </thead>
            <tbody>
              {[...data].sort((a, b) => b.total_aua - a.total_aua).slice(0, 20).map((advisor, i) => (
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
                  <td className="text-right px-4 py-3 text-white/80 font-mono">{formatCurrency(advisor.total_aua)}</td>
                  <td className="text-right px-4 py-3 text-white/70">{advisor.client_count.toLocaleString()}</td>
                  <td className="text-right px-4 py-3">
                    <span className={`font-mono ${advisor.nna >= 0 ? 'text-[#10B981]' : 'text-[#EF4444]'}`}>
                      {advisor.nna >= 0 ? '+' : ''}{formatCurrency(advisor.nna)}
                    </span>
                  </td>
                  <td className="text-right px-4 py-3">
                    <span className={`font-medium ${advisor.aua_growth_pct >= 0 ? 'text-[#10B981]' : 'text-[#EF4444]'}`}>
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
        {data.length > 20 && (
          <div className="px-4 py-2 text-center text-[10px] text-white/40 border-t border-white/5">
            Showing top 20 of {data.length} advisors
          </div>
        )}
      </PanelContent>
    </Panel>
  )
}
