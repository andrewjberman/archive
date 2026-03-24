/**
 * Books Tab - Advisor Intelligence
 *
 * Canonical 3-panel framework identical across all drill levels:
 *   Row 1: Overview (KPI metrics)
 *   Row 2: Mix Pie (left) + Concentration Pie (right) — equal width
 *   Row 3: Cost Basis & Tax Liability (taxable / tax-deferred / tax-free AUA)
 *
 * Drill hierarchy:
 *   N1 (Firm Dashboard) -> L2 (Advisor Book) -> L3 (Relationship) -> L4 (Account)
 */

import { useState, useEffect, useMemo, lazy, Suspense, Fragment } from 'react'
import { Panel, PanelHeader, PanelContent } from '@/ui/components/panels'
import { LoadingInline } from '@/components/LoadingSpinner'
const ApexChart = lazy(() => import('react-apexcharts'))
import {
  ChevronRight,
  ChevronDown,
  ArrowLeft,
  Users,
  X,
} from 'lucide-react'
import { formatCurrency, formatNumberTo3Digits } from '@/lib/universalNumberFormatter'
import {
  getArchitectLeaderboard,
  getAdvisorBook,
  getBooksClientDetail,
  getClientsTab,
  getBooksRelationshipComposition,
  getBooksAccountComposition,
  getFirmMixViews,
  getBooksRelationshipTimeseries,
  getMixTimeseries,
  getAdvisorTimeseries,
  getAdvisorMixTimeseries,
} from '@/api/endpoints/advisor-intelligence'
import { useAuth } from '@/hooks/useAuth'
import type {
  LeaderboardEntry,
  AdvisorBookResponse,
  AdvisorClient,
  BooksClientDetailResponse,
  BooksClientAccount,
  BooksCompositionResponse,
  ConcentrationItem,
  OpenLot,
  CostBasisYear,
  GainPosition,
  ClientsTabResponse,
  PortfolioAllocationItem,
  AssetAllocationItem,
  FirmMixPeriodPoint,
  FirmMixViewsResponse,
  FirmMixClassValue,
  MixTimeseriesPoint,
} from '../types'

// ============================================================================
// CANONICAL DATA SHAPES
// ============================================================================

interface CanonicalOverview {
  title: string
  totalAua: number
  metrics: { label: string; value: string }[]
  dataAsOf?: string
}

interface CanonicalTax {
  taxable: number
  taxablePct: number
  taxDeferred: number
  taxDeferredPct: number
  taxFree: number
  taxFreePct: number
  capitalGainsTtm?: number
  costBasisByYear?: CostBasisYear[]
  topGainPositions?: GainPosition[]
}

// ============================================================================
// COMPOSITION FETCHER (tries Lambda endpoint, falls back to synthesis)
// ============================================================================

// S3 bucket suffix -> DynamoDB firm key (mirrors advisor-intelligence.ts LAMBDA_FIRM_ID)
const FIRM_KEY: Record<string, string> = { bd: '49financial' }

/**
 * Fetch composition from the Lambda for any entity scope.
 * Returns null on any error (endpoint not deployed, 400, 404, network).
 * Callers fall back to synthesized data when null.
 *
 * Endpoint pattern: /api/scoped/partners/books/{entityType}/{entityId}/composition?firmId=
 *
 * Currently deployed entity types: relationship, account
 * Pending (see devops brief): firm, advisor
 */
async function fetchComposition(
  entityType: string,
  entityId: string,
  firmId: string,
): Promise<BooksCompositionResponse | null> {
  try {
    const apiBase = import.meta.env.VITE_PORTAL_API_URL ?? ''
    const firmKey = FIRM_KEY[firmId] ?? firmId
    const url = `${apiBase}/api/scoped/partners/books/${entityType}/${entityId}/composition?firmId=${firmKey}`
    const token = localStorage.getItem('accessToken')
    const res = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
      },
    })
    if (!res.ok) return null
    return await res.json()
  } catch {
    return null
  }
}

// ============================================================================
// COMPOSITION DATA SYNTHESIS (fallback when Lambda endpoint is not deployed)
// ============================================================================

function synthesizeFromPortfolio(
  allocation: PortfolioAllocationItem[],
  totalAua: number,
): BooksCompositionResponse {
  return {
    generated_at: '', data_as_of: '', scope: {},
    mix: allocation.map((a) => ({
      asset_class: a.name.toLowerCase().replace(/\s+/g, '_'),
      label: a.name,
      market_value: totalAua * a.pct,
      pct: a.pct,
    })),
    concentration: { top_n: 0, items: [], other: { market_value: 0, pct: 0 } },
    unclassified: { count: 0, market_value: 0 },
  }
}

function synthesizeFromAssetAllocation(
  items: AssetAllocationItem[],
  totalAua: number,
): BooksCompositionResponse {
  return {
    generated_at: '', data_as_of: '', scope: {},
    mix: items.map((a) => ({
      asset_class: a.category,
      label: a.label,
      market_value: totalAua * a.pct,
      pct: a.pct,
    })),
    concentration: { top_n: 0, items: [], other: { market_value: 0, pct: 0 } },
    unclassified: { count: 0, market_value: 0 },
  }
}

function taxFromAccountStatus(taxStatus: string, totalAua: number): CanonicalTax {
  const s = taxStatus.toLowerCase()
  const isTaxable = s.includes('taxable') && !s.includes('deferred') && !s.includes('free')
  const isDeferred = s.includes('deferred')
  const isFree = s.includes('free')
  return {
    taxable: isTaxable ? totalAua : 0, taxablePct: isTaxable ? 100 : 0,
    taxDeferred: isDeferred ? totalAua : 0, taxDeferredPct: isDeferred ? 100 : 0,
    taxFree: isFree ? totalAua : 0, taxFreePct: isFree ? 100 : 0,
  }
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

interface BooksTabProps {
  firmId: string
  firmOverride?: string
}

export function BooksTab({ firmId, firmOverride }: BooksTabProps) {
  const { isInternal, isDev } = useAuth()
  const isFirmAdmin = isInternal() || isDev()
  const effectiveFirm = firmOverride || firmId

  // N1 data
  const [advisorSummary, setAdvisorSummary] = useState<LeaderboardEntry[]>([])
  const [clientsTabData, setClientsTabData] = useState<ClientsTabResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // L2 data
  const [selectedAdvisorId, setSelectedAdvisorId] = useState<string | null>(null)
  const [advisorBookData, setAdvisorBookData] = useState<AdvisorBookResponse | null>(null)
  const [isLoadingAdvisor, setIsLoadingAdvisor] = useState(false)

  // L3 data
  const [selectedClientKey, setSelectedClientKey] = useState<string | null>(null)
  const [clientDetailData, setClientDetailData] = useState<BooksClientDetailResponse | null>(null)
  const [isLoadingClient, setIsLoadingClient] = useState(false)
  const [compositionData, setCompositionData] = useState<BooksCompositionResponse | null>(null)

  // N1: Firm composition (async from Lambda, fallback to synthesis)
  const [firmComposition, setFirmComposition] = useState<BooksCompositionResponse | null>(null)

  // L2: Advisor composition (async from Lambda, fallback to synthesis)
  const [advisorComposition, setAdvisorComposition] = useState<BooksCompositionResponse | null>(null)

  // L4 data
  const [selectedAccountId, setSelectedAccountId] = useState<string | null>(null)
  const [accountCompositionData, setAccountCompositionData] = useState<BooksCompositionResponse | null>(null)

  // N1: quarterly firm mix (for the metrics bar at firm level)
  const [firmMixViews, setFirmMixViews] = useState<FirmMixViewsResponse | null>(null)

  // L2: raw timeseries for quarterly computation
  const [l2AuaTimeseries, setL2AuaTimeseries] = useState<{ date: string; total_aua: number }[] | null>(null)
  const [l2MixTimeseries, setL2MixTimeseries] = useState<MixTimeseriesPoint[] | null>(null)

  // L3: raw timeseries for quarterly computation
  const [l3AuaTimeseries, setL3AuaTimeseries] = useState<{ date: string; total_aua: number }[] | null>(null)
  const [l3MixTimeseries, setL3MixTimeseries] = useState<MixTimeseriesPoint[] | null>(null)

  // Shared state
  const [selectedAssetClass, setSelectedAssetClass] = useState<string | null>(null)
  const [isAdvisorDropdownOpen, setIsAdvisorDropdownOpen] = useState(false)

  // ── Data Fetching ───────────────────────────────────────────────

  // N1: Advisor list + firm dashboard
  useEffect(() => {
    if (!firmId || !isFirmAdmin) { setIsLoading(false); return }
    setIsLoading(true)
    Promise.all([
      getArchitectLeaderboard(firmOverride),
      getClientsTab(firmOverride),
      getFirmMixViews(effectiveFirm).catch(() => null),
    ])
      .then(([lb, ct, fmv]) => {
        if (lb?.windows?.['1Y']?.entries) setAdvisorSummary(lb.windows['1Y'].entries)
        setClientsTabData(ct)
        setFirmMixViews(fmv ?? null)
        setIsLoading(false)
      })
      .catch((err) => { console.error('[BooksTab] N1 fetch failed:', err); setIsLoading(false) })
  }, [firmId, isFirmAdmin, firmOverride])

  // L2: Advisor book
  useEffect(() => {
    if (!selectedAdvisorId) { setAdvisorBookData(null); return }
    let cancelled = false
    setIsLoadingAdvisor(true)
    getAdvisorBook(selectedAdvisorId, firmOverride)
      .then((d) => { if (!cancelled) { setAdvisorBookData(d); setIsLoadingAdvisor(false) } })
      .catch((err) => { if (!cancelled) { console.error('[BooksTab] L2 fetch failed:', err); setAdvisorBookData(null); setIsLoadingAdvisor(false) } })
    return () => { cancelled = true }
  }, [selectedAdvisorId, firmOverride])

  // L2: Advisor AUA timeseries (for quarterly mix bar)
  useEffect(() => {
    if (!selectedAdvisorId) { setL2AuaTimeseries(null); return }
    getAdvisorTimeseries(selectedAdvisorId, effectiveFirm)
      .then(d => setL2AuaTimeseries(d?.data ?? null))
      .catch(() => setL2AuaTimeseries(null))
  }, [selectedAdvisorId, effectiveFirm])

  // L2: Advisor mix timeseries (for quarterly mix bar)
  useEffect(() => {
    if (!selectedAdvisorId) { setL2MixTimeseries(null); return }
    getAdvisorMixTimeseries(selectedAdvisorId, effectiveFirm, 'Max')
      .then(d => setL2MixTimeseries(d?.data ?? null))
      .catch(() => setL2MixTimeseries(null))
  }, [selectedAdvisorId, effectiveFirm])

  // L3: Client detail
  useEffect(() => {
    if (!selectedClientKey) { setClientDetailData(null); setCompositionData(null); return }
    let cancelled = false
    setIsLoadingClient(true)
    getBooksClientDetail(selectedClientKey, firmOverride)
      .then((d) => { if (!cancelled) { setClientDetailData(d); setIsLoadingClient(false) } })
      .catch((err) => { if (!cancelled) { console.error('[BooksTab] L3 fetch failed:', err); setClientDetailData(null); setIsLoadingClient(false) } })
    return () => { cancelled = true }
  }, [selectedClientKey, firmOverride])

  // L3: Composition
  useEffect(() => {
    if (!selectedClientKey) { setCompositionData(null); return }
    let cancelled = false
    getBooksRelationshipComposition(selectedClientKey, effectiveFirm)
      .then((d) => { if (!cancelled) setCompositionData(d) })
      .catch(() => { if (!cancelled) setCompositionData(null) })
    return () => { cancelled = true }
  }, [selectedClientKey, effectiveFirm])

  // L4: Account composition
  useEffect(() => {
    if (!selectedAccountId) { setAccountCompositionData(null); return }
    let cancelled = false
    getBooksAccountComposition(selectedAccountId, effectiveFirm)
      .then((d) => { if (!cancelled) setAccountCompositionData(d) })
      .catch(() => { if (!cancelled) setAccountCompositionData(null) })
    return () => { cancelled = true }
  }, [selectedAccountId, effectiveFirm])

  // N1: Firm-level composition (Lambda -> fallback to portfolio synthesis)
  useEffect(() => {
    if (!clientsTabData) { setFirmComposition(null); return }
    let cancelled = false
    fetchComposition('firm', 'all', effectiveFirm).then((comp) => {
      if (cancelled) return
      if (comp) {
        setFirmComposition(comp)
      } else {
        // Lambda endpoint not deployed yet — synthesize from portfolio allocation
        setFirmComposition(synthesizeFromPortfolio(
          clientsTabData.portfolio.allocation,
          clientsTabData.headline.total_aua,
        ))
      }
    })
    return () => { cancelled = true }
  }, [clientsTabData, effectiveFirm])

  // L3: Relationship AUA timeseries (for quarterly mix bar)
  useEffect(() => {
    if (!selectedClientKey) { setL3AuaTimeseries(null); return }
    getBooksRelationshipTimeseries(selectedClientKey, effectiveFirm)
      .then(d => setL3AuaTimeseries(d?.data ?? null))
      .catch(() => setL3AuaTimeseries(null))
  }, [selectedClientKey, effectiveFirm])

  // L3: Relationship mix timeseries (for quarterly mix bar)
  useEffect(() => {
    if (!selectedClientKey) { setL3MixTimeseries(null); return }
    getMixTimeseries(selectedClientKey, effectiveFirm, 'Max')
      .then(d => setL3MixTimeseries(d ?? null))
      .catch(() => setL3MixTimeseries(null))
  }, [selectedClientKey, effectiveFirm])

  // L2: Derived quarterly mix from timeseries
  const l2QuarterlyMix = useMemo((): FirmMixPeriodPoint[] | null => {
    if (!l2AuaTimeseries || !l2MixTimeseries) return null
    return deriveQuarterlyFromTimeseries(l2AuaTimeseries, l2MixTimeseries)
  }, [l2AuaTimeseries, l2MixTimeseries])

  // L3: Derived quarterly mix from timeseries
  const l3QuarterlyMix = useMemo((): FirmMixPeriodPoint[] | null => {
    if (!l3AuaTimeseries || !l3MixTimeseries) return null
    return deriveQuarterlyFromTimeseries(l3AuaTimeseries, l3MixTimeseries)
  }, [l3AuaTimeseries, l3MixTimeseries])

  // L2: Advisor-level composition (Lambda -> fallback to asset allocation synthesis)
  useEffect(() => {
    if (!selectedAdvisorId || !advisorBookData) { setAdvisorComposition(null); return }
    let cancelled = false
    fetchComposition('advisor', selectedAdvisorId, effectiveFirm).then((comp) => {
      if (cancelled) return
      if (comp) {
        setAdvisorComposition(comp)
      } else {
        // Lambda endpoint not deployed yet — synthesize from book asset allocation
        setAdvisorComposition(synthesizeFromAssetAllocation(
          advisorBookData.portfolio_composition.asset_allocation,
          advisorBookData.summary.total_aua,
        ))
      }
    })
    return () => { cancelled = true }
  }, [selectedAdvisorId, advisorBookData, effectiveFirm])

  // Reset on firm change
  useEffect(() => {
    setSelectedAdvisorId(null); setSelectedClientKey(null); setSelectedAccountId(null)
    setAdvisorBookData(null); setClientDetailData(null); setCompositionData(null)
    setAccountCompositionData(null); setFirmComposition(null); setAdvisorComposition(null)
    setSelectedAssetClass(null); setFirmMixViews(null)
    setL2AuaTimeseries(null); setL2MixTimeseries(null)
    setL3AuaTimeseries(null); setL3MixTimeseries(null)
  }, [firmId])

  // ── Navigation ──────────────────────────────────────────────────

  const handleSelectAdvisor = (name: string) => {
    const id = name.toLowerCase().trim().replace(/[^a-z0-9_]+/g, '_').replace(/^_+|_+$/g, '') || 'unknown'
    setSelectedAdvisorId(id)
    setSelectedClientKey(null); setClientDetailData(null); setSelectedAccountId(null)
    setIsAdvisorDropdownOpen(false); setSelectedAssetClass(null)
  }

  const handleClientClick = (key: string) => {
    setSelectedClientKey(key); setSelectedAccountId(null); setSelectedAssetClass(null)
  }

  const handleBackToL2 = () => {
    setSelectedClientKey(null); setClientDetailData(null); setCompositionData(null)
    setSelectedAccountId(null); setAccountCompositionData(null); setSelectedAssetClass(null)
    setL3AuaTimeseries(null); setL3MixTimeseries(null)
  }

  const handleBackToList = () => {
    setSelectedAdvisorId(null); setAdvisorBookData(null)
    setL2AuaTimeseries(null); setL2MixTimeseries(null)
    handleBackToL2()
  }

  // ── Derived ─────────────────────────────────────────────────────

  const selectedAccount = useMemo(() => {
    if (!selectedAccountId || !clientDetailData) return null
    return clientDetailData.accounts?.find((a) => a.account_id === selectedAccountId) ?? null
  }, [clientDetailData?.accounts, selectedAccountId])

  const accountScopedLots = useMemo(() => {
    if (!selectedAccountId || !clientDetailData) return []
    return (clientDetailData.tax?.open_lots ?? []).filter((l) => l.account_id === selectedAccountId)
  }, [clientDetailData?.tax?.open_lots, selectedAccountId])

  // ── Guards ──────────────────────────────────────────────────────

  if (!firmId) {
    return (
      <Panel variant="chart">
        <PanelContent className="py-12 text-center"><p className="text-white/60">Select a partner to view books</p></PanelContent>
      </Panel>
    )
  }
  if (isLoading) return <LoadingInline className="py-12" />

  // ── L3: Relationship Detail ─────────────────────────────────────

  if (selectedClientKey) {
    if (isLoadingClient) return <LoadingInline className="py-12" />
    const clientName = advisorBookData?.clients.find((c) => c.client_key === selectedClientKey)?.client_name ?? selectedClientKey

    const l3Tax: CanonicalTax | null = clientDetailData?.tax ? {
      taxable: clientDetailData.tax.taxable, taxablePct: clientDetailData.tax.taxable_pct,
      taxDeferred: clientDetailData.tax.tax_deferred, taxDeferredPct: clientDetailData.tax.tax_deferred_pct,
      taxFree: clientDetailData.tax.tax_free, taxFreePct: clientDetailData.tax.tax_free_pct,
      costBasisByYear: clientDetailData.tax.cost_basis_by_year,
      topGainPositions: clientDetailData.tax.top_gain_positions,
    } : null

    return (
      <div className="flex flex-col gap-4">
        <Breadcrumb
          segments={[
            { label: 'All Advisors', onClick: handleBackToList },
            { label: advisorBookData?.book_name ?? 'Advisor', onClick: handleBackToL2 },
            { label: clientName },
          ]}
        />
        <BackButton label="Back to Book" onClick={handleBackToL2} />

        {clientDetailData ? (
          <>
            <CanonicalBookView
              overview={{
                title: clientName,
                totalAua: clientDetailData.headline.total_aua,
                metrics: [{ label: 'Accounts', value: clientDetailData.headline.account_count.toLocaleString() }],
                dataAsOf: clientDetailData.data_as_of,
              }}
              composition={compositionData}
              tax={l3Tax}
              selectedAssetClass={selectedAssetClass}
              onSelectAssetClass={setSelectedAssetClass}
              quarterlyMix={l3QuarterlyMix}
            />

            {/* Accounts Table */}
            <Panel variant="chart">
              <PanelHeader title="Accounts" />
              <PanelContent noPadding>
                <AccountsTable
                  accounts={clientDetailData.accounts ?? []}
                  selectedAccountId={selectedAccountId}
                  onSelectAccount={(id) => { setSelectedAccountId(id); setSelectedAssetClass(null) }}
                />
              </PanelContent>
            </Panel>

            {/* L4: Account Drill (inline canonical view) */}
            {selectedAccountId && selectedAccount && (
              <div className="flex flex-col gap-4 pl-4 border-l-2 border-white/10">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-semibold text-white">Account: {selectedAccountId}</p>
                  <button onClick={() => setSelectedAccountId(null)} className="flex items-center gap-1 text-xs text-white/50 hover:text-white transition-colors">
                    <X size={12} /> Close
                  </button>
                </div>

                <CanonicalBookView
                  overview={{
                    title: selectedAccountId,
                    totalAua: selectedAccount.total_aua,
                    metrics: [
                      { label: 'Tax Status', value: selectedAccount.tax_status },
                      { label: 'NNA', value: `${selectedAccount.nna >= 0 ? '+' : ''}${formatCurrency(selectedAccount.nna)}` },
                      { label: 'Positions', value: selectedAccount.num_positions.toLocaleString() },
                    ],
                  }}
                  composition={accountCompositionData}
                  tax={taxFromAccountStatus(selectedAccount.tax_status, selectedAccount.total_aua)}
                  selectedAssetClass={selectedAssetClass}
                  onSelectAssetClass={setSelectedAssetClass}
                  quarterlyMix={null}
                />

                {accountScopedLots.length > 0 && (
                  <Panel variant="chart">
                    <PanelHeader title={`Open Lots -- ${selectedAccountId}`} />
                    <PanelContent noPadding><OpenLotsTable lots={accountScopedLots} /></PanelContent>
                  </Panel>
                )}
              </div>
            )}

            {/* L3 Open Lots */}
            {clientDetailData.tax?.open_lots && clientDetailData.tax.open_lots.length > 0 && (
              <OpenLotsWithFilters lots={clientDetailData.tax.open_lots} />
            )}
          </>
        ) : (
          <Panel variant="chart">
            <PanelContent className="py-12 text-center"><p className="text-white/40">Client detail data not available</p></PanelContent>
          </Panel>
        )}
      </div>
    )
  }

  // ── L2: Advisor Book ────────────────────────────────────────────

  if (selectedAdvisorId && advisorBookData) {
    return (
      <div className="flex flex-col gap-4">
        <Breadcrumb
          segments={[
            { label: 'All Advisors', onClick: handleBackToList },
            { label: advisorBookData.book_name },
          ]}
        />
        <BackButton label="Back to Firm Overview" onClick={handleBackToList} />

        <CanonicalBookView
          overview={{
            title: advisorBookData.book_name,
            totalAua: advisorBookData.summary.total_aua,
            metrics: [
              { label: 'Clients', value: advisorBookData.summary.client_count.toLocaleString() },
              { label: 'Accounts', value: advisorBookData.summary.account_count.toLocaleString() },
            ],
            dataAsOf: advisorBookData.data_as_of,
          }}
          composition={advisorComposition}
          tax={{
            taxable: advisorBookData.tax_exposure.taxable, taxablePct: advisorBookData.tax_exposure.taxable_pct,
            taxDeferred: advisorBookData.tax_exposure.tax_deferred, taxDeferredPct: advisorBookData.tax_exposure.tax_deferred_pct,
            taxFree: advisorBookData.tax_exposure.tax_free, taxFreePct: advisorBookData.tax_exposure.tax_free_pct,
          }}
          selectedAssetClass={selectedAssetClass}
          onSelectAssetClass={setSelectedAssetClass}
          quarterlyMix={l2QuarterlyMix}
        />

        <Panel variant="chart">
          <PanelHeader title="Clients" />
          <PanelContent noPadding>
            <ClientsTable clients={advisorBookData.clients} onClientClick={handleClientClick} />
          </PanelContent>
        </Panel>
      </div>
    )
  }

  if (selectedAdvisorId && isLoadingAdvisor) return <LoadingInline className="py-12" />

  // ── N1: Firm Dashboard ──────────────────────────────────────────

  return (
    <div className="flex flex-col gap-4">
      {clientsTabData && (
        <CanonicalBookView
          overview={{
            title: 'Firm Overview',
            totalAua: clientsTabData.headline.total_aua,
            metrics: [
              { label: 'Clients', value: clientsTabData.headline.client_count.toLocaleString() },
              { label: 'Accounts', value: clientsTabData.headline.account_count.toLocaleString() },
            ],
          }}
          composition={firmComposition}
          tax={{
            taxable: clientsTabData.tax.taxable, taxablePct: clientsTabData.tax.taxable_pct,
            taxDeferred: clientsTabData.tax.tax_deferred, taxDeferredPct: clientsTabData.tax.tax_deferred_pct,
            taxFree: clientsTabData.tax.tax_free, taxFreePct: clientsTabData.tax.tax_free_pct,
            capitalGainsTtm: clientsTabData.tax.capital_gains_ttm,
          }}
          selectedAssetClass={selectedAssetClass}
          onSelectAssetClass={setSelectedAssetClass}
          quarterlyMix={firmMixViews?.views.quarterly.slice(-4) ?? null}
        />
      )}

      {/* Advisor selector + list */}
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
                {[...advisorSummary].sort((a, b) => b.total_aua - a.total_aua).map((adv) => (
                  <div key={adv.name} onClick={() => handleSelectAdvisor(adv.name)} className="px-3 py-2.5 cursor-pointer hover:bg-white/10 transition-colors">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-white">{adv.name}</span>
                      <span className="text-xs text-white/50">{formatCurrency(adv.total_aua)}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {advisorSummary.length > 0 ? (
        <AdvisorSummaryTable data={advisorSummary} onSelectAdvisor={handleSelectAdvisor} />
      ) : (
        <Panel variant="chart">
          <PanelContent className="py-12 text-center"><p className="text-white/40">No advisor data available</p></PanelContent>
        </Panel>
      )}
    </div>
  )
}

// ============================================================================
// CANONICAL BOOK VIEW — Identical layout at every drill level
// ============================================================================

function CanonicalBookView({
  overview, composition, tax, selectedAssetClass, onSelectAssetClass, quarterlyMix,
}: {
  overview: CanonicalOverview
  composition: BooksCompositionResponse | null
  tax: CanonicalTax | null
  selectedAssetClass: string | null
  onSelectAssetClass: (cls: string | null) => void
  quarterlyMix: FirmMixPeriodPoint[] | null
}) {
  return (
    <>
      {/* Row 1+2: Consolidated Overview (donut + holdings + quarterly bar) */}
      <ConsolidatedOverviewPanel
        overview={overview}
        composition={composition}
        selectedAssetClass={selectedAssetClass}
        onSelectAssetClass={onSelectAssetClass}
        quarterlyMix={quarterlyMix}
      />

      {/* Row 3: Cost Basis & Tax Liability */}
      <TaxCostBasisPanel tax={tax} />
    </>
  )
}

// ============================================================================
// CONSOLIDATED OVERVIEW PANEL (Rows 1+2) — donut + holdings + quarterly bar
// ============================================================================

const METRIC_CARD_STYLE: Record<string, { dot: string; border: string; from: string; to: string; label: string }> = {
  'Clients':    { dot: 'bg-sky-400',     border: 'border-sky-500/25',     from: 'from-sky-500/15',     to: 'to-sky-500/5',     label: 'text-sky-300/70' },
  'Accounts':   { dot: 'bg-emerald-400', border: 'border-emerald-500/25', from: 'from-emerald-500/15', to: 'to-emerald-500/5', label: 'text-emerald-300/70' },
  'NNA':        { dot: 'bg-violet-400',  border: 'border-violet-500/25',  from: 'from-violet-500/15',  to: 'to-violet-500/5',  label: 'text-violet-300/70' },
  'Tax Status': { dot: 'bg-amber-400',   border: 'border-amber-500/25',   from: 'from-amber-500/15',   to: 'to-amber-500/5',   label: 'text-amber-300/70' },
  'Positions':  { dot: 'bg-purple-400',  border: 'border-purple-500/25',  from: 'from-purple-500/15',  to: 'to-purple-500/5',  label: 'text-purple-300/70' },
}
const METRIC_CARD_DEFAULT = { dot: 'bg-slate-400', border: 'border-slate-500/25', from: 'from-slate-500/15', to: 'to-slate-500/5', label: 'text-slate-300/70' }

// Canonical asset class colors
const MIX_PIE_COLORS: Record<string, string> = {
  equity:           '#3b82f6',
  equities:         '#3b82f6',
  fixed_income:     '#10b981',
  structured_notes: '#f97316',
  alternatives:     '#f97316',
  real_estate:      '#f97316',
  hedge:            '#f97316',
  cash:             '#f59e0b',
  other:            '#6B7280',
  untracked:        '#6B7280',
}

function colorFor(assetClass: string): string {
  return MIX_PIE_COLORS[assetClass] || MIX_PIE_COLORS[assetClass.toLowerCase().replace(/\s+/g, '_')] || '#6B7280'
}

/**
 * Derive last 4 quarter-end snapshots from raw daily timeseries.
 * Returns FirmMixPeriodPoint[] (ascending) so the quarterly bar has 4 points
 * and can compute 3 QoQ growth rates.
 */
function deriveQuarterlyFromTimeseries(
  auaTs: { date: string; total_aua: number }[],
  mixTs: MixTimeseriesPoint[],
): FirmMixPeriodPoint[] {
  if (!auaTs.length || !mixTs.length) return []

  const auaSorted = [...auaTs].sort((a, b) => a.date.localeCompare(b.date))
  const mixSorted = [...mixTs].sort((a, b) => a.date.localeCompare(b.date))
  const maxDate = auaSorted[auaSorted.length - 1].date

  // Find last 4 quarter-end dates <= maxDate
  const maxDateObj = new Date(maxDate + 'T00:00:00Z')
  const qm0 = Math.floor(maxDateObj.getUTCMonth() / 3) * 3 + 3  // last completed quarter-end month

  const quarterEnds: Date[] = []
  for (let i = 0; i < 4; i++) {
    let qm = qm0 - i * 3
    let qy = maxDateObj.getUTCFullYear()
    while (qm <= 0) { qm += 12; qy-- }
    // last day of quarter-end month
    quarterEnds.unshift(new Date(Date.UTC(qy, qm, 0)))
  }

  function closestAuaPt(target: string) {
    let best = auaSorted[0]
    for (const pt of auaSorted) {
      if (pt.date <= target) best = pt
      else break
    }
    return best
  }

  function closestMixPt(target: string) {
    let best = mixSorted[0]
    for (const pt of mixSorted) {
      if (pt.date <= target) best = pt
      else break
    }
    return best
  }

  return quarterEnds.map((qEnd) => {
    const isoDate = qEnd.toISOString().slice(0, 10)
    const aua = closestAuaPt(isoDate)
    const mix = closestMixPt(isoDate)
    const total = aua.total_aua
    const qNum = Math.floor((qEnd.getUTCMonth()) / 3) + 1
    const qy = qEnd.getUTCFullYear()
    return {
      period: `${qy}-Q${qNum}`,
      label: `Q${qNum} '${String(qy).slice(-2)}`,
      end_date: isoDate,
      total_aua: total,
      equity:           { value: total * mix.equity,           pct: mix.equity },
      fixed_income:     { value: total * mix.fixed_income,     pct: mix.fixed_income },
      alternatives:     { value: total * mix.alternatives,     pct: mix.alternatives },
      cash:             { value: total * mix.cash,             pct: mix.cash },
    } as FirmMixPeriodPoint
  })
}

function getClassAua(pt: FirmMixPeriodPoint, cls: string | null): number {
  if (!cls) return pt.total_aua
  const val = (pt as unknown as Record<string, unknown>)[cls]
  if (val && typeof val === 'object' && 'value' in val) return (val as FirmMixClassValue).value
  return 0
}

function QuarterlyMetricsBar({
  quarterlyMix, selectedAssetClass, currentAua, currentSelectedAua,
}: {
  quarterlyMix: FirmMixPeriodPoint[] | null
  selectedAssetClass: string | null
  currentAua: number
  currentSelectedAua: number | null
}) {
  const calcQoQ = (cur: number, prior: number | null): number | null => {
    if (!prior || prior === 0) return null
    return (cur / prior - 1) * 100
  }
  const getPctColor = (pct: number | null): string => {
    if (pct === null) return 'text-white/40'
    return pct > 0 ? 'text-emerald-400' : pct < 0 ? 'text-red-400' : 'text-white/40'
  }
  const fmtPct = (pct: number | null): string => {
    if (pct === null) return ''
    return `${pct >= 0 ? '+' : ''}${pct.toFixed(1)}%`
  }
  const dotColor = (pct: number | null): string =>
    pct === null ? 'bg-white/30' : pct > 0 ? 'bg-emerald-400' : pct < 0 ? 'bg-red-400' : 'bg-white/30'

  const displayCurrentAua = selectedAssetClass ? (currentSelectedAua ?? 0) : currentAua
  const pts = quarterlyMix ?? []
  const q1 = pts[pts.length - 1] ?? null
  const q2 = pts[pts.length - 2] ?? null
  const q3 = pts[pts.length - 3] ?? null
  const q0b = pts[pts.length - 4] ?? null

  const q1Aua = q1 ? getClassAua(q1, selectedAssetClass) : null
  const q2Aua = q2 ? getClassAua(q2, selectedAssetClass) : null
  const q3Aua = q3 ? getClassAua(q3, selectedAssetClass) : null
  const q0bAua = q0b ? getClassAua(q0b, selectedAssetClass) : null

  const currentQoQ = calcQoQ(displayCurrentAua, q1Aua)
  const q1QoQ = calcQoQ(q1Aua ?? 0, q2Aua)
  const q2QoQ = calcQoQ(q2Aua ?? 0, q3Aua)
  const q3QoQ = calcQoQ(q3Aua ?? 0, q0bAua)

  return (
    <div className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center">
      <div className="flex flex-wrap items-center justify-evenly gap-x-4 gap-y-2 w-full">
        <div className="flex flex-col items-center px-3 py-1 rounded bg-[hsl(253,74%,85%)]/15 border border-[hsl(253,74%,85%)]/40 min-w-[80px]">
          <div className="text-[10px] text-white/80 font-semibold mb-0.5">{selectedAssetClass ? 'Current' : 'Current AUA'}</div>
          <div className="flex items-center gap-1">
            <span className="text-sm font-bold text-white">{formatCurrency(displayCurrentAua)}</span>
            {currentQoQ !== null && <span className={`text-[10px] font-medium ${getPctColor(currentQoQ)}`}>{fmtPct(currentQoQ)}</span>}
          </div>
        </div>
        <div className="flex flex-col items-center min-w-[80px]">
          <div className="flex items-center gap-1 mb-0.5">
            <div className={`w-1.5 h-1.5 rounded-full ${dotColor(q1QoQ)}`} />
            <span className="text-[10px] text-white/50">{q1?.label ?? '—'}</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="text-xs font-semibold text-white">{q1Aua !== null ? formatCurrency(q1Aua) : '—'}</span>
            {q1QoQ !== null && <span className={`text-[10px] font-medium ${getPctColor(q1QoQ)}`}>{fmtPct(q1QoQ)}</span>}
          </div>
        </div>
        <div className="flex flex-col items-center min-w-[80px]">
          <div className="flex items-center gap-1 mb-0.5">
            <div className={`w-1.5 h-1.5 rounded-full ${dotColor(q2QoQ)}`} />
            <span className="text-[10px] text-white/50">{q2?.label ?? '—'}</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="text-xs font-semibold text-white">{q2Aua !== null ? formatCurrency(q2Aua) : '—'}</span>
            {q2QoQ !== null && <span className={`text-[10px] font-medium ${getPctColor(q2QoQ)}`}>{fmtPct(q2QoQ)}</span>}
          </div>
        </div>
        <div className="flex flex-col items-center min-w-[80px]">
          <div className="flex items-center gap-1 mb-0.5">
            <div className="w-1.5 h-1.5 rounded-full bg-white/30" />
            <span className="text-[10px] text-white/50">{q3?.label ?? '—'}</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="text-xs font-semibold text-white">{q3Aua !== null ? formatCurrency(q3Aua) : '—'}</span>
            {q3QoQ !== null && <span className={`text-[10px] font-medium ${getPctColor(q3QoQ)}`}>{fmtPct(q3QoQ)}</span>}
          </div>
        </div>
      </div>
    </div>
  )
}

function ConsolidatedOverviewPanel({
  overview, composition, selectedAssetClass, onSelectAssetClass, quarterlyMix,
}: {
  overview: CanonicalOverview
  composition: BooksCompositionResponse | null
  selectedAssetClass: string | null
  onSelectAssetClass: (cls: string | null) => void
  quarterlyMix: FirmMixPeriodPoint[] | null
}) {
  const hasMix = composition && composition.mix.length > 0

  // Detect schema: N1/L2 (per-class top_holdings) vs L3/L4 (flat concentration.items)
  const hasPreAggregated = (composition?.mix.some(m => (m.top_holdings?.length ?? 0) > 0)) ?? false

  const MAX_ITEMS = 9

  // Resolved display items
  const cappedItems: ConcentrationItem[] = (() => {
    if (!composition) return []
    if (hasPreAggregated) {
      if (selectedAssetClass) {
        // Per-class top holdings already pre-capped at 9 by script 12
        return composition.mix.find(m => m.asset_class === selectedAssetClass)?.top_holdings ?? []
      } else {
        // Global top 9
        return composition.top_holdings ?? []
      }
    } else {
      // L3/L4: filter flat list, cap at 9
      const all = composition.concentration.items
      const filtered = selectedAssetClass
        ? all.filter(it => it.asset_class === selectedAssetClass)
        : all
      return filtered.slice(0, MAX_ITEMS)
    }
  })()

  // "Other" bucket display
  const otherEntry: { pct: number; market_value: number } | null = (() => {
    if (!composition) return null
    if (hasPreAggregated) {
      if (selectedAssetClass) {
        return composition.mix.find(m => m.asset_class === selectedAssetClass)?.other ?? null
      } else {
        return composition.other ?? null
      }
    } else {
      // L3/L4 schema
      if (!selectedAssetClass && composition.concentration.other.pct > 0) {
        return composition.concentration.other
      }
      return null
    }
  })()

  const showOther = otherEntry !== null && otherEntry.pct > 0
  const maxPct = cappedItems.length > 0 ? cappedItems[0].pct : 1

  const selectedMixItem = composition?.mix.find(i => i.asset_class === selectedAssetClass)

  const centerLabels = selectedMixItem
    ? {
        show: true,
        name: { show: true, fontSize: '10px', fontWeight: 600, color: 'rgba(255,255,255,0.55)', offsetY: -8, formatter: () => selectedMixItem.label },
        value: { show: true, fontSize: '18px', fontWeight: 700, color: '#ffffff', offsetY: 4, formatter: () => formatCurrency(selectedMixItem.market_value) },
        total: { show: true, showAlways: true, label: selectedMixItem.label, fontSize: '10px', fontWeight: 600, color: 'rgba(255,255,255,0.45)', formatter: () => formatCurrency(selectedMixItem.market_value) },
      }
    : {
        show: true,
        name: { show: false },
        value: { show: true, fontSize: '18px', fontWeight: 700, color: '#ffffff', offsetY: 4, formatter: () => formatCurrency(overview.totalAua) },
        total: { show: true, showAlways: true, label: 'Total AUA', fontSize: '10px', fontWeight: 600, color: 'rgba(255,255,255,0.45)', formatter: () => formatCurrency(overview.totalAua) },
      }

  const holdingsTitle = hasMix && selectedAssetClass
    ? `Top ${selectedMixItem?.label ?? selectedAssetClass.replace(/_/g, ' ')} Holdings`
    : 'Top Holdings'

  return (
    <Panel variant="chart">
      <PanelHeader title={overview.title} />
      <PanelContent>
        {/* Metric cards — full-width flex row, each card grows to fill */}
        <div className="flex gap-3 mb-5">
          <div className="flex-1 rounded-xl border border-indigo-500/25 bg-gradient-to-br from-indigo-500/15 to-indigo-500/5 p-4">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-2 h-2 rounded-full bg-indigo-400 flex-shrink-0" />
              <span className="text-[10px] text-indigo-300/70 uppercase tracking-widest font-medium">Total AUA</span>
            </div>
            <p className="text-3xl font-black text-white tracking-tight leading-none">{formatCurrency(overview.totalAua)}</p>
            {overview.dataAsOf && <p className="text-[10px] text-indigo-400/50 mt-2">as of {overview.dataAsOf}</p>}
          </div>
          {overview.metrics.map((m) => {
            const s = METRIC_CARD_STYLE[m.label] ?? METRIC_CARD_DEFAULT
            return (
              <div key={m.label} className={`flex-1 rounded-xl border ${s.border} bg-gradient-to-br ${s.from} ${s.to} p-4`}>
                <div className="flex items-center gap-2 mb-3">
                  <div className={`w-2 h-2 rounded-full ${s.dot} flex-shrink-0`} />
                  <span className={`text-[10px] ${s.label} uppercase tracking-widest font-medium`}>{m.label}</span>
                </div>
                <p className="text-2xl font-bold text-white leading-none">{m.value}</p>
              </div>
            )
          })}
        </div>

        <div className="flex min-h-[320px]">
          {/* LEFT: donut + legend + quarterly bar */}
          <div className="flex-1 flex flex-col gap-4 pr-5">
            <p className="text-[10px] text-white/50 uppercase tracking-widest font-medium mb-1">Asset Mix</p>
            <div className="flex items-start gap-4">
              {/* Donut */}
              {hasMix ? (
                <div style={{ width: 220, height: 220, flexShrink: 0 }}>
                  <Suspense fallback={<div className="flex items-center justify-center h-full"><span className="text-xs text-white/20">...</span></div>}>
                    <ApexChart
                      key={`consolidated-donut-${selectedAssetClass ?? 'all'}`}
                      type="donut"
                      width={220}
                      height={220}
                      series={composition.mix.map(item => item.market_value)}
                      options={{
                        chart: {
                          type: 'donut',
                          background: 'transparent',
                          animations: { enabled: true, speed: 800, animateGradually: { enabled: true, delay: 150 }, dynamicAnimation: { enabled: true, speed: 350 } },
                          dropShadow: { enabled: true, top: 4, left: 0, blur: 10, opacity: 0.35 },
                          events: {
                            dataPointSelection: (_event: unknown, _chartContext: unknown, config: { dataPointIndex: number }) => {
                              const cls = composition.mix[config.dataPointIndex]?.asset_class
                              if (cls) onSelectAssetClass(selectedAssetClass === cls ? null : cls)
                            },
                          },
                        },
                        colors: composition.mix.map(item => colorFor(item.asset_class)),
                        labels: composition.mix.map(item => item.label),
                        stroke: { show: true, width: 2, colors: ['rgba(0,0,0,0.3)'] },
                        dataLabels: { enabled: false },
                        plotOptions: { pie: { expandOnClick: false, donut: { size: '60%', labels: centerLabels } } },
                        legend: { show: false },
                        tooltip: { enabled: false },
                        states: { hover: { filter: { type: 'lighten', value: 0.08 } }, active: { filter: { type: 'darken', value: 0.1 } } },
                      }}
                    />
                  </Suspense>
                </div>
              ) : (
                <div style={{ width: 220, height: 220, flexShrink: 0 }} className="flex items-center justify-center">
                  <span className="text-xs text-white/30">{composition ? 'No allocation data' : 'Loading...'}</span>
                </div>
              )}

              {/* Clickable legend */}
              {hasMix && (
                <div className="flex-1 flex flex-col gap-2 pt-2">
                  {composition.mix.map((item) => {
                    const isSelected = selectedAssetClass === item.asset_class
                    const isDimmed = selectedAssetClass && !isSelected
                    return (
                      <button
                        key={item.asset_class}
                        onClick={() => onSelectAssetClass(isSelected ? null : item.asset_class)}
                        className={`flex items-center gap-2.5 px-2.5 py-1.5 rounded-lg transition-all text-left focus:outline-none ${
                          isSelected ? 'bg-white/15 ring-1 ring-white/30' : isDimmed ? 'opacity-30 hover:opacity-60' : 'hover:bg-white/10'
                        }`}
                      >
                        <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: colorFor(item.asset_class) }} />
                        <span className="text-[11px] text-white/80 flex-1">{item.label}</span>
                        <span className="text-[11px] font-semibold text-white/70">{formatCurrency(item.market_value)}</span>
                        <span className="text-[10px] text-white/40 w-10 text-right">{(item.pct * 100).toFixed(1)}%</span>
                      </button>
                    )
                  })}
                </div>
              )}
            </div>

            {/* Quarterly metrics bar */}
            <QuarterlyMetricsBar
              quarterlyMix={quarterlyMix}
              selectedAssetClass={selectedAssetClass}
              currentAua={overview.totalAua}
              currentSelectedAua={selectedMixItem?.market_value ?? null}
            />
          </div>

          {/* Vertical divider */}
          <div className="w-px self-stretch bg-white/10 mx-2 flex-shrink-0" />

          {/* RIGHT: top holdings bars */}
          <div className="flex-1 flex flex-col gap-2 pl-5">
            <p className="text-[10px] text-white/50 uppercase tracking-widest font-medium mb-1">{holdingsTitle}</p>
            {cappedItems.length > 0 ? (
              <div className="flex flex-col gap-2.5 overflow-y-auto" style={{ maxHeight: 280 }}>
                {cappedItems.map((item, idx) => (
                  <div key={item.key} className="flex items-center gap-2.5">
                    <span className="text-[10px] text-white/30 w-4 text-right flex-shrink-0 font-mono">{idx + 1}</span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-baseline justify-between mb-1">
                        <span className="text-[11px] text-white/85 truncate leading-tight">{item.label}</span>
                        <span className="text-[11px] font-semibold text-white/70 ml-2 flex-shrink-0">{(item.pct * 100).toFixed(1)}%</span>
                      </div>
                      <div className="h-1.5 bg-white/[0.08] rounded-full overflow-hidden">
                        <div
                          className="h-full rounded-full transition-all"
                          style={{ width: `${(item.pct / maxPct) * 100}%`, backgroundColor: colorFor(item.asset_class) }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
                {showOther && otherEntry && (
                  <div className="flex items-center gap-2.5">
                    <span className="text-[10px] text-white/20 w-4 text-right flex-shrink-0">~</span>
                    <div className="flex-1">
                      <div className="flex items-baseline justify-between mb-1">
                        <span className="text-[11px] text-white/40 italic">Other</span>
                        <span className="text-[11px] text-white/30 ml-2">{(otherEntry.pct * 100).toFixed(1)}%</span>
                      </div>
                      <div className="h-1.5 bg-white/[0.05] rounded-full overflow-hidden">
                        <div className="h-full rounded-full bg-white/20"
                          style={{ width: `${(otherEntry.pct / maxPct) * 100}%` }} />
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex items-center justify-center py-8">
                <span className="text-xs text-white/30">
                  {!composition ? 'Loading...' : !hasPreAggregated && composition.concentration.items.length === 0 ? 'No holdings data at this level' : 'No holdings for selected class'}
                </span>
              </div>
            )}
          </div>
        </div>
      </PanelContent>
    </Panel>
  )
}

// ============================================================================
// TAX & COST BASIS PANEL (Row 3)
// ============================================================================

function TaxCostBasisPanel({ tax }: { tax: CanonicalTax | null }) {
  if (!tax) {
    return (
      <Panel variant="chart">
        <PanelHeader title="Cost Basis & Tax Liability" />
        <PanelContent className="py-6 text-center">
          <span className="text-sm text-white/40">Tax data not available</span>
        </PanelContent>
      </Panel>
    )
  }

  const totalTaxAua = tax.taxable + tax.taxDeferred + tax.taxFree
  const taxBuckets = [
    { label: 'Taxable', amount: tax.taxable, pct: tax.taxablePct, color: '#EF4444', bg: 'bg-red-500/10', border: 'border-red-500/20' },
    { label: 'Tax Deferred', amount: tax.taxDeferred, pct: tax.taxDeferredPct, color: '#F59E0B', bg: 'bg-amber-500/10', border: 'border-amber-500/20' },
    { label: 'Tax Free', amount: tax.taxFree, pct: tax.taxFreePct, color: '#10B981', bg: 'bg-emerald-500/10', border: 'border-emerald-500/20' },
  ]

  return (
    <Panel variant="chart">
      <PanelHeader title="Cost Basis & Tax Liability" />
      <PanelContent>
        <div className="space-y-5">
          {/* Stacked bar */}
          {totalTaxAua > 0 && (
            <div>
              <p className="text-[10px] text-white/40 uppercase tracking-widest mb-2.5">AUA by Tax Status</p>
              <div className="flex h-5 rounded-lg overflow-hidden gap-px">
                {taxBuckets.filter((b) => b.pct > 0).map((b) => (
                  <div
                    key={b.label}
                    className="flex items-center justify-center"
                    style={{ width: `${b.pct}%`, backgroundColor: b.color }}
                  >
                    {b.pct >= 10 && (
                      <span className="text-[9px] font-bold text-white/90 leading-none">{b.pct.toFixed(0)}%</span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Tax status cards */}
          <div className="grid grid-cols-3 gap-2">
            {taxBuckets.map((b) => (
              <div key={b.label} className={`rounded-lg border ${b.border} ${b.bg} p-3`}>
                <div className="flex items-center gap-1.5 mb-2">
                  <div className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ backgroundColor: b.color }} />
                  <span className="text-[10px] text-white/50 uppercase tracking-wide leading-tight">{b.label}</span>
                </div>
                <p className="text-base font-bold text-white leading-tight">{formatCurrency(b.amount)}</p>
                <p className="text-[10px] text-white/40 mt-0.5">{b.pct.toFixed(1)}%</p>
              </div>
            ))}
          </div>

          {/* Capital Gains TTM */}
          {tax.capitalGainsTtm != null && (
            <div className="flex items-center justify-between rounded-lg bg-white/[0.03] border border-white/[0.08] px-4 py-3">
              <span className="text-xs text-white/50 uppercase tracking-wide">Capital Gains (TTM)</span>
              <span className={`text-lg font-bold ${tax.capitalGainsTtm >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                {tax.capitalGainsTtm >= 0 ? '+' : ''}{formatCurrency(tax.capitalGainsTtm)}
              </span>
            </div>
          )}

          {/* Cost Basis by Year (L3+) */}
          {tax.costBasisByYear && tax.costBasisByYear.length > 0 && (
            <div>
              <p className="text-[10px] text-white/40 uppercase tracking-widest mb-2.5">Cost Basis by Year</p>
              <div className="rounded-lg overflow-hidden border border-white/[0.08]">
                <table className="w-full text-xs">
                  <thead>
                    <tr className="bg-white/[0.04] border-b border-white/10">
                      <th className="text-left px-3 py-2 text-[10px] text-white/50 font-semibold uppercase tracking-wide">Year</th>
                      <th className="text-right px-3 py-2 text-[10px] text-white/50 font-semibold uppercase tracking-wide">Cost Basis</th>
                      <th className="text-right px-3 py-2 text-[10px] text-white/50 font-semibold uppercase tracking-wide">Market Value</th>
                      <th className="text-right px-3 py-2 text-[10px] text-white/50 font-semibold uppercase tracking-wide">Unrealized Gain</th>
                    </tr>
                  </thead>
                  <tbody>
                    {tax.costBasisByYear.map((row, i) => (
                      <tr key={row.year} className={`border-b border-white/5 ${i % 2 === 1 ? 'bg-white/[0.02]' : ''}`}>
                        <td className="px-3 py-2 text-white/70 font-medium">{row.year}</td>
                        <td className="px-3 py-2 text-right text-white/60">{formatCurrency(row.cost_basis)}</td>
                        <td className="px-3 py-2 text-right text-white/60">{formatCurrency(row.market_value)}</td>
                        <td className="px-3 py-2 text-right">
                          <span className={row.unrealized_gain >= 0 ? 'text-emerald-400' : 'text-red-400'}>
                            {row.unrealized_gain >= 0 ? '+' : ''}{formatCurrency(row.unrealized_gain)}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Top Gain Positions (L3+) */}
          {tax.topGainPositions && tax.topGainPositions.length > 0 && (
            <div>
              <p className="text-[10px] text-white/40 uppercase tracking-widest mb-2.5">Top Gain Positions</p>
              <div className="rounded-lg overflow-hidden border border-white/[0.08]">
                <table className="w-full text-xs">
                  <thead>
                    <tr className="bg-white/[0.04] border-b border-white/10">
                      <th className="text-left px-3 py-2 text-[10px] text-white/50 font-semibold uppercase tracking-wide">Name</th>
                      <th className="text-left px-3 py-2 text-[10px] text-white/50 font-semibold uppercase tracking-wide">Ticker</th>
                      <th className="text-right px-3 py-2 text-[10px] text-white/50 font-semibold uppercase tracking-wide">Gain</th>
                      <th className="text-right px-3 py-2 text-[10px] text-white/50 font-semibold uppercase tracking-wide">Cost Basis</th>
                      <th className="text-right px-3 py-2 text-[10px] text-white/50 font-semibold uppercase tracking-wide">Mkt Value</th>
                      <th className="text-left px-3 py-2 text-[10px] text-white/50 font-semibold uppercase tracking-wide">Term</th>
                    </tr>
                  </thead>
                  <tbody>
                    {tax.topGainPositions.map((pos, i) => (
                      <tr key={i} className={`border-b border-white/5 ${i % 2 === 1 ? 'bg-white/[0.02]' : ''}`}>
                        <td className="px-3 py-2 text-white/70 max-w-[120px] truncate">{pos.asset_name}</td>
                        <td className="px-3 py-2 text-white/50 font-mono">{pos.ticker ?? '--'}</td>
                        <td className="px-3 py-2 text-right">
                          <span className={pos.unrealized_gain >= 0 ? 'text-emerald-400 font-bold' : 'text-red-400 font-bold'}>
                            {pos.unrealized_gain >= 0 ? '+' : ''}{formatCurrency(pos.unrealized_gain)}
                          </span>
                        </td>
                        <td className="px-3 py-2 text-right text-white/60">{formatCurrency(pos.cost_basis)}</td>
                        <td className="px-3 py-2 text-right text-white/60">{formatCurrency(pos.market_value)}</td>
                        <td className="px-3 py-2">
                          <span className={`px-1.5 py-0.5 rounded text-[9px] font-semibold ${pos.term === 'Short' ? 'bg-amber-500/15 text-amber-400' : 'bg-emerald-500/15 text-emerald-400'}`}>
                            {pos.term}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </PanelContent>
    </Panel>
  )
}


// ============================================================================
// OPEN LOTS WITH FILTERS (L3)
// ============================================================================

function OpenLotsWithFilters({ lots }: { lots: OpenLot[] }) {
  const [termFilter, setTermFilter] = useState<'all' | 'short' | 'long'>('all')
  const [accountFilter, setAccountFilter] = useState<string>('all')

  const accountIds = useMemo(() => [...new Set(lots.map((l) => l.account_id))], [lots])

  const filtered = useMemo(() => {
    let result = lots
    if (termFilter !== 'all') {
      const match = termFilter === 'short' ? 'Short' : 'Long'
      result = result.filter((l) => l.term === match)
    }
    if (accountFilter !== 'all') result = result.filter((l) => l.account_id === accountFilter)
    return result
  }, [lots, termFilter, accountFilter])

  return (
    <Panel variant="chart">
      <PanelHeader
        title="Taxable Open Lots"
        actions={
          <div className="flex items-center gap-2">
            <div className="flex gap-0.5 bg-white/10 rounded-lg p-0.5">
              {(['all', 'short', 'long'] as const).map((t) => (
                <button
                  key={t}
                  onClick={() => setTermFilter(t)}
                  className={`px-2 py-1 text-xs font-medium rounded-md transition-colors ${
                    termFilter === t ? 'bg-white/20 text-white' : 'text-white/50 hover:text-white hover:bg-white/10'
                  }`}
                >
                  {t === 'all' ? 'All' : t === 'short' ? 'Short' : 'Long'}
                </button>
              ))}
            </div>
            {accountIds.length > 1 && (
              <select
                value={accountFilter}
                onChange={(e) => setAccountFilter(e.target.value)}
                className="bg-white/10 text-white text-xs rounded-md px-2 py-1 border border-white/10 outline-none"
              >
                <option value="all">All Accounts</option>
                {accountIds.map((id) => <option key={id} value={id}>{id}</option>)}
              </select>
            )}
          </div>
        }
      />
      <PanelContent noPadding>
        {filtered.length > 0 ? (
          <OpenLotsTable lots={filtered} />
        ) : (
          <div className="py-6 text-center text-sm text-white/40">
            No taxable open lots{termFilter !== 'all' || accountFilter !== 'all' ? ' matching filters' : ''}
          </div>
        )}
      </PanelContent>
    </Panel>
  )
}

// ============================================================================
// TABLE COMPONENTS
// ============================================================================

// Field-name normalizers (Lambda sends current_units/accrued_gain; future target is quantity/unrealized_gain)
function lotQty(lot: OpenLot): number { return lot.current_units ?? lot.quantity ?? 0 }
function lotGain(lot: OpenLot): number { return lot.accrued_gain ?? lot.unrealized_gain ?? 0 }

function termBadge(term: string) {
  const s = term === 'Short'
    ? 'bg-amber-500/15 text-amber-400'
    : term === 'Long'
    ? 'bg-emerald-500/15 text-emerald-400'
    : term === 'Hybrid'
    ? 'bg-indigo-500/15 text-indigo-400'
    : 'bg-white/5 text-white/40'
  return <span className={`px-1.5 py-0.5 rounded text-[9px] font-semibold ${s}`}>{term || '--'}</span>
}

function OpenLotsTable({ lots }: { lots: OpenLot[] }) {
  const [expanded, setExpanded] = useState<Set<string>>(new Set())

  const grouped = useMemo(() => {
    const map = new Map<string, OpenLot[]>()
    for (const lot of lots) {
      const key = `${lot.asset_name ?? ''}||${lot.ticker ?? ''}`
      const group = map.get(key) ?? []
      group.push(lot)
      map.set(key, group)
    }
    return [...map.entries()].map(([key, items]) => ({ key, items }))
  }, [lots])

  const toggle = (key: string) =>
    setExpanded(prev => { const n = new Set(prev); if (n.has(key)) { n.delete(key) } else { n.add(key) } return n })

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-xs">
        <thead className="bg-[hsl(var(--bg-header))] sticky top-0 z-10">
          <tr className="border-b border-white/20">
            <th className="w-7" />
            <th className="text-left px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Name</th>
            <th className="text-left px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Ticker</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Qty</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Avg Cost</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Mkt Value</th>
            <th className="text-right px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Gain</th>
            <th className="text-left px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Term</th>
            <th className="text-left px-3 py-2 text-[10px] font-semibold text-white/80 uppercase tracking-wider">Acq. Date</th>
          </tr>
        </thead>
        <tbody>
          {grouped.map(({ key, items }) => {
            const isMulti = items.length > 1
            const isOpen = expanded.has(key)
            const totalQty = items.reduce((s, l) => s + lotQty(l), 0)
            const hasQty = totalQty > 0
            const totalCost = items.reduce((s, l) => s + (l.cost_basis ?? 0), 0)
            const totalMv = items.reduce((s, l) => s + (l.market_value ?? 0), 0)
            const totalGain = items.reduce((s, l) => s + lotGain(l), 0)
            const avgCost = hasQty ? totalCost / totalQty : null
            // Use cost_per_unit from first lot as fallback if no qty-based avg
            const displayCost = avgCost ?? items[0]?.cost_per_unit ?? totalCost
            const terms = new Set(items.map(l => l.term).filter(Boolean))
            const term = terms.size > 1 ? 'Hybrid' : (items[0]?.term ?? '--')
            const acqDates = items.map(l => l.acquisition_date).filter(Boolean) as string[]
            const latestAcq = acqDates.length > 0 ? [...acqDates].sort().at(-1) ?? null : null

            return (
              <Fragment key={key}>
                <tr
                  className={`border-b border-white/5 transition-colors ${isMulti ? 'cursor-pointer hover:bg-white/5' : 'hover:bg-white/5'}`}
                  onClick={() => isMulti && toggle(key)}
                >
                  <td className="px-2 py-2 text-center text-white/30">
                    {isMulti && (isOpen ? <ChevronDown size={12} /> : <ChevronRight size={12} />)}
                  </td>
                  <td className="px-3 py-2 text-white/70 max-w-[140px] truncate">
                    {items[0]?.asset_name ?? '--'}
                    {isMulti && <span className="ml-1.5 text-[9px] text-white/25 font-mono">{items.length}x</span>}
                  </td>
                  <td className="px-3 py-2 text-white/50 font-mono">{items[0]?.ticker ?? '--'}</td>
                  <td className="px-3 py-2 text-right text-white/60">{hasQty ? totalQty.toLocaleString() : '--'}</td>
                  <td className="px-3 py-2 text-right text-white/60">{formatCurrency(displayCost)}</td>
                  <td className="px-3 py-2 text-right text-white/60">{formatCurrency(totalMv)}</td>
                  <td className="px-3 py-2 text-right">
                    <span className={totalGain >= 0 ? 'text-[#10B981]' : 'text-[#EF4444]'}>
                      {totalGain >= 0 ? '+' : ''}{formatCurrency(totalGain)}
                    </span>
                  </td>
                  <td className="px-3 py-2">{termBadge(term)}</td>
                  <td className="px-3 py-2 text-white/50">{latestAcq ?? '--'}</td>
                </tr>
                {isOpen && items.map((lot, li) => {
                  const qty = lotQty(lot)
                  const gain = lotGain(lot)
                  return (
                    <tr key={`${key}-${li}`} className="border-b border-white/[0.04] bg-white/[0.025]">
                      <td />
                      <td className="px-3 py-1.5 pl-7 text-white/35 text-[10px] italic">Lot {li + 1}</td>
                      <td className="px-3 py-1.5 text-white/25 font-mono text-[10px]">{lot.ticker ?? '--'}</td>
                      <td className="px-3 py-1.5 text-right text-white/40 text-[10px]">{qty > 0 ? qty.toLocaleString() : '--'}</td>
                      <td className="px-3 py-1.5 text-right text-white/40 text-[10px]">
                        {lot.cost_per_unit != null ? formatCurrency(lot.cost_per_unit) : formatCurrency(lot.cost_basis ?? 0)}
                      </td>
                      <td className="px-3 py-1.5 text-right text-white/40 text-[10px]">{formatCurrency(lot.market_value ?? 0)}</td>
                      <td className="px-3 py-1.5 text-right text-[10px]">
                        <span className={gain >= 0 ? 'text-[#10B981]/60' : 'text-[#EF4444]/60'}>
                          {gain >= 0 ? '+' : ''}{formatCurrency(gain)}
                        </span>
                      </td>
                      <td className="px-3 py-1.5 text-[10px]">{termBadge(lot.term ?? '')}</td>
                      <td className="px-3 py-1.5 text-white/30 text-[10px]">{lot.acquisition_date ?? '--'}</td>
                    </tr>
                  )
                })}
              </Fragment>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

function ClientsTable({ clients, onClientClick }: { clients: AdvisorClient[]; onClientClick: (key: string) => void }) {
  const sorted = useMemo(() => [...clients].sort((a, b) => b.aua - a.aua), [clients])
  if (sorted.length === 0) return <div className="py-6 text-center text-sm text-white/40">No clients</div>

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
          {sorted.map((c, i) => (
            <tr
              key={c.client_key}
              onClick={() => onClientClick(c.client_key)}
              className={`border-b border-white/5 hover:bg-white/5 cursor-pointer transition-colors group${i % 2 === 1 ? ' bg-white/[0.025]' : ''}`}
            >
              <td className="px-4 py-2.5 text-sm text-white font-medium">{c.client_name}</td>
              <td className="px-4 py-2.5 text-right text-white/70">{formatCurrency(c.aua)}</td>
              <td className="px-2 py-2.5"><ChevronRight size={14} className="text-white/30 group-hover:text-white/60 transition-colors" /></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function AccountsTable({ accounts, selectedAccountId, onSelectAccount }: {
  accounts: BooksClientAccount[]
  selectedAccountId: string | null
  onSelectAccount: (id: string | null) => void
}) {
  if (accounts.length === 0) return <div className="py-6 text-center text-sm text-white/40">No accounts</div>

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
            const sel = acct.account_id === selectedAccountId
            return (
              <tr
                key={acct.account_id}
                onClick={() => onSelectAccount(sel ? null : acct.account_id)}
                className={`border-b border-white/5 cursor-pointer transition-colors ${sel ? 'bg-white/10' : 'hover:bg-white/5'}`}
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

// Canonical column layout — matches AdvisorsTab.tsx LeaderboardRow
const BOOKS_COL = 'w-[160px] flex-shrink-0 text-center px-4'
const BOOKS_DIV = <div className="w-px self-stretch bg-white/10 flex-shrink-0" />

function ArchitectRankBadge({ rank }: { rank: number }) {
  const colors: Record<number, string> = {
    1: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/40',
    2: 'bg-gray-400/20 text-gray-300 border-gray-400/40',
    3: 'bg-orange-600/20 text-orange-400 border-orange-600/40',
  }
  return (
    <span className={`inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-bold border ${colors[rank] || 'bg-white/5 text-white/50 border-white/10'}`}>
      {rank}
    </span>
  )
}

function AdvisorSummaryTable({ data, onSelectAdvisor }: { data: LeaderboardEntry[]; onSelectAdvisor: (name: string) => void }) {
  const sorted = useMemo(() => [...data].sort((a, b) => b.total_aua - a.total_aua).slice(0, 20), [data])

  // Hero = AUA (default context for Books tab), secondary = uniform text-sm
  const HERO = 'text-2xl font-black'
  const SEC = 'text-sm font-medium'

  return (
    <Panel variant="chart">
      <PanelHeader title="Architect Summary" />
      <PanelContent noPadding>
        <div className="p-5 flex flex-col gap-3">
          {sorted.map((adv, i) => {
            const rank = i + 1
            const isTop3 = rank <= 3
            const nnaPos = adv.nna >= 0
            const groPos = adv.aua_growth_pct >= 0
            const borderColor = rank === 1 ? 'border-amber-500/40' : rank === 2 ? 'border-slate-400/30' : rank === 3 ? 'border-orange-600/30' : 'border-white/8'
            return (
              <div
                key={adv.name}
                onClick={() => onSelectAdvisor(adv.name)}
                className={`rounded-xl border ${borderColor} bg-white/[0.02] overflow-hidden hover:border-white/20 transition-colors cursor-pointer`}
              >
                <div className="px-8 py-5 flex items-center">
                  <div className="flex-shrink-0 mr-5">
                    <ArchitectRankBadge rank={rank} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className={`text-lg font-bold ${isTop3 ? 'text-white' : 'text-white/90'}`}>{adv.name}</div>
                  </div>
                  {/* NNA */}
                  {BOOKS_DIV}
                  <div className={BOOKS_COL}>
                    <div className={`${SEC} ${nnaPos ? 'text-[hsl(var(--success))]' : 'text-red-400'}`}>
                      {nnaPos ? '+' : ''}{formatNumberTo3Digits(adv.nna, { unit: '$', includeSign: false })}
                    </div>
                    <div className="text-[10px] text-white/30 uppercase mt-1">NNA</div>
                  </div>
                  {/* AUA — hero */}
                  {BOOKS_DIV}
                  <div className={BOOKS_COL}>
                    <div className={`${HERO} text-white`}>
                      {formatCurrency(adv.total_aua)}
                    </div>
                    <div className="text-[10px] text-white/30 uppercase mt-1">AUA</div>
                  </div>
                  {/* GRO */}
                  {BOOKS_DIV}
                  <div className={BOOKS_COL}>
                    <div className={`${SEC} ${groPos ? 'text-emerald-400' : 'text-red-400'}`}>
                      {groPos ? '+' : ''}{adv.aua_growth_pct.toFixed(1)}%
                    </div>
                    <div className="text-[10px] text-white/30 uppercase mt-1">GRO</div>
                  </div>
                  {/* New Clients */}
                  {BOOKS_DIV}
                  <div className={BOOKS_COL}>
                    <div className={`${SEC} text-white/60`}>{adv.new_clients}</div>
                    <div className="text-[10px] text-white/30 uppercase mt-1">New Clients</div>
                  </div>
                </div>
              </div>
            )
          })}
        </div>

        {data.length > 20 && (
          <div className="px-4 py-2 text-center text-[10px] text-white/40 border-t border-white/5">
            Showing top 20 of {data.length} architects
          </div>
        )}
      </PanelContent>
    </Panel>
  )
}

// ============================================================================
// SHARED PRIMITIVES
// ============================================================================

function MetricCard({ label, value, large }: { label: string; value: string; large?: boolean }) {
  return (
    <div className="bg-white/5 rounded-lg p-3 text-center">
      <p className={`font-bold text-white ${large ? 'text-xl' : 'text-sm'}`}>{value}</p>
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

function Breadcrumb({ segments }: { segments: { label: string; onClick?: () => void }[] }) {
  return (
    <div className="flex items-center gap-1.5">
      {segments.map((seg, i) => (
        <span key={i} className="flex items-center gap-1.5">
          {i > 0 && <ChevronRight size={14} className="text-indigo-500/60 flex-shrink-0" />}
          {seg.onClick ? (
            <button
              onClick={seg.onClick}
              className="text-base font-semibold text-indigo-400 hover:text-indigo-200 hover:underline underline-offset-2 transition-colors"
            >
              {seg.label}
            </button>
          ) : (
            <span className="text-base font-bold text-white">{seg.label}</span>
          )}
        </span>
      ))}
    </div>
  )
}

function BackButton({ label, onClick }: { label: string; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="flex items-center gap-1.5 text-base font-semibold text-indigo-400 hover:text-indigo-200 hover:underline underline-offset-2 transition-colors w-fit"
    >
      <ArrowLeft size={16} /> {label}
    </button>
  )
}
