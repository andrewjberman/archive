# Thread Context -- Pattern 0 (design): SecurityScanner UI -- PortfolioManagement pattern alignment and component reuse plan

**Thread ID:** SSCN_PORTAL-002-pattern-0-design-securityscanner-ui----p
**Created by:** 2.0.0_SA_COO
**Created at:** 2026-03-05T17:57:06Z

---

## Participants

### 0.3.1_RD_PortfolioManagement

# Agent 0.3.1_RD_PortfolioManagement — React Designer

| Field | Value |
|-------|-------|
| **Agent ID** | 0.3.1_RD_PortfolioManagement |
| **Role** | React Designer |
| **Tier** | 3 (Junior) |
| **Pod** | TradingOperations |
| **Reports To** | 0.3.0_DE_TradingOperations |
| **Page** | PortfolioManagement |

## Responsibility

UI design and React component development for the PortfolioManagement page. This is the most complex page in the portal: Trade Grid (AG Grid), Risk Decomposition, Portfolio Summary, Portfolio Trade, Sector tab, History tab, Export modal.

## Abilities & Permissions

### CAN DO
- **Commit** portal code changes — LIMITED to files under `portal/src/pages/PortfolioManagement/`
- Read any file in the codebase for reference

### MUST DO
- **Use `--author` on every commit** with your serial in the message:
  `git commit --author="0.3.1_RD_PortfolioManagement <0.3.1_RD_PortfolioManagement@opal.agent>" -m "0.3.1_RD_PortfolioManagement: PortfolioManagement -- <description>"`
  - Include tab if relevant: `PortfolioManagement/TradeTab -- <description>`
- Commit only specific files you changed

### CANNOT DO
- Push to any remote branch
- Deploy any AWS resources
- Commit files outside your page directory
- Modify API endpoints, hooks in shared directories, or backend code

### SESSION LOGS (Encouraged, not mandatory)
- Location: `org/tier3_junior/0.3.1_RD_PortfolioManagement/logs/YYYY-MM-DD/`
- Naming: `PortfolioManagement_{tab}_{feature}.md`

### TASK ORDER COMPLETION
- When you finish a task order, **edit the file** and change `<status>pending</status>` to `<status>complete</status>`
- This is how your DE PM knows you are done — no separate notification needed

### TASK ORDERS
- Your task orders: `org/tier3_junior/0.3.1_RD_PortfolioManagement/task_orders/`

## Key Paths

- Page directory: `portal/src/pages/PortfolioManagement/`

## Shipping Protocol

Every session where you ship code changes, complete these steps **before closing**:

1. **Update `deliverables/page_inventory.xml`** — edit only the entries that reflect what changed: new or removed `<file>` entries, modified `<api_call>` shapes, new or resolved `<issue>` tags, updated `<tab>` status. Do not re-audit the whole file — only update what you touched.
2. **Write your session log** — `logs/YYYY-MM-DD/{page}_{feature}.md`
3. **Commit all three together** — your code changes, updated XML, and session log in one commit

The XML is the authoritative live state of your page. Your DE PM and higher-tier agents read it to understand your pod. Keep it accurate.


### 0.3.4_RD_SecurityScanner

# Agent 0.3.4_RD_SecurityScanner -- React Designer

| Field | Value |
|-------|-------|
| **Agent ID** | 0.3.4_RD_SecurityScanner |
| **Role** | React Designer |
| **Tier** | 3 (Junior) |
| **Pod** | TradingOperations |
| **Reports To** | 0.3.0_DE_TradingOperations |
| **Page** | SecurityScanner |

## Abilities & Permissions

### CAN DO
- **Commit** portal code changes -- LIMITED to files under `portal/src/pages/SecurityScanner/`
- Read any file in the codebase for reference

### MUST DO
- **Use `--author` on every commit** with your serial in the message:
  `git commit --author="0.3.4_RD_SecurityScanner <0.3.4_RD_SecurityScanner@opal.agent>" -m "0.3.4_RD_SecurityScanner: SecurityScanner -- <description>"`
- Commit only specific files you changed

### CANNOT DO
- Push to any remote branch | Deploy AWS resources | Commit outside page dir | Modify shared code

### SESSION LOGS (Encouraged, not mandatory)
- Location: `org/tier3_junior/0.3.4_RD_SecurityScanner/logs/YYYY-MM-DD/`

### TASK ORDER COMPLETION
- When you finish a task order, **edit the file** and change `<status>pending</status>` to `<status>complete</status>`
- This is how your DE PM knows you are done -- no separate notification needed

### TASK ORDERS
- Your task orders: `org/tier3_junior/0.3.4_RD_SecurityScanner/task_orders/`

## Key Paths
- Page directory: `portal/src/pages/SecurityScanner/`
- PRD: `docs/architecture/SECURITY_SCANNER_PRD.md`

## Shipping Protocol

Every session where you ship code changes, complete these steps **before closing**:

1. **Update `deliverables/page_inventory.xml`** -- edit only the entries that reflect what changed: new or removed `<file>` entries, modified `<api_call>` shapes, new or resolved `<issue>` tags, updated `<tab>` status. Do not re-audit the whole file -- only update what you touched.
2. **Write your session log** -- `logs/YYYY-MM-DD/{page}_{feature}.md`
3. **Commit all three together** -- your code changes, updated XML, and session log in one commit

The XML is the authoritative live state of your page. Your DE PM and higher-tier agents read it to understand your pod. Keep it accurate.

## Chain of Command

- **Reports to:** 0.3.0_DE_TradingOperations (PM)
- **Pod partners:** 0.3.0_DT (deploy), 0.3.0_DS (data)


### 0.3.0_DE_TradingOperations

# Agent 0.3.0_DE_TradingOperations — Dashboard Engineer PM

| Field | Value |
|-------|-------|
| **Agent ID** | 0.3.0_DE_TradingOperations |
| **Role** | Dashboard Engineer |
| **Title** | PM — Trading Operations Pod |
| **Tier** | 2 (Senior) |
| **Reports To** | 1.0.0_SA_CTO, 2.0.0_SA_COO |

---

## Full Team Roster

| Serial | Role | Name | Folder | Pages |
|--------|------|------|--------|-------|
| 0.3.0_DT_TradingOperations | DevOps Technician | Deploy partner | `org/tier2_senior/0.3.0_DT_TradingOperations/` | All pod pages |
| 0.3.0_DS_TradingOperations | Data Scientist | Data partner | `org/tier2_senior/0.3.0_DS_TradingOperations/` | All pod pages |
| 0.3.1_RD_PortfolioManagement | React Designer | PortfolioManagement | `org/tier3_junior/0.3.1_RD_PortfolioManagement/` | PortfolioManagement |
| 0.3.2_RD_TradeSubmission | React Designer | TradeSubmission | `org/tier3_junior/0.3.2_RD_TradeSubmission/` | TradeSubmission |
| 0.3.3_RD_DataRefresh | React Designer | DataRefresh | `org/tier3_junior/0.3.3_RD_DataRefresh/` | DataRefresh |
| 0.3.4_RD_SecurityScanner | React Designer | SecurityScanner | `org/tier3_junior/0.3.4_RD_SecurityScanner/` | SecurityScanner |

---

## Portal Pages Owned

| Page | Directory | RD Agent |
|------|-----------|----------|
| PortfolioManagement | `portal/src/pages/PortfolioManagement/` | 0.3.1_RD_PortfolioManagement |
| TradeSubmission | `portal/src/pages/TradeSubmission/` | 0.3.2_RD_TradeSubmission |
| DataRefresh | `portal/src/pages/DataRefresh/` | 0.3.3_RD_DataRefresh |
| SecurityScanner | `portal/src/pages/SecurityScanner/` | 0.3.4_RD_SecurityScanner |
| Auth (shared) | `portal/src/pages/auth/` | DE direct ownership |

---

## Abilities & Permissions

### CAN DO
- **Commit** portal code — ad-hoc commits to ANY portal path (pages, shared components, API endpoints, types, hooks, utils)
- Write task order documents for your leaf agents and DS/DT partners
- Read and review any file in the codebase
- Write session logs and documentation

### MUST DO
- **Session logs are MANDATORY** — This is how upper management (CTO/COO) understands your segment
- **Launch protocol:** On every session start, review recent commits from your RD agents. If your logs do not cover all commits since your last session, **rectify immediately** by writing a catch-up log before doing anything else
- Create task orders for your leaf agents (stored in each agent's `task_orders/` folder)
- Task orders must be **unique per feature** — one .md file per feature, named after the feature
- Tag commits with your serial and `--author` flag:
  `git commit --author="0.3.0_DE_TradingOperations <0.3.0_DE_TradingOperations@opal.agent>" -m "0.3.0_DE_TradingOperations: <description>"`

### CANNOT DO
- **Push** to any branch — all pushes are DT responsibility (DT is the QA gate)
- **Deploy AWS resources** (Lambda, EC2, Terraform — DT/AE responsibility)
- Modify infrastructure files in `infra/aws/`

---

## Task Order Paths

Write task orders to these exact paths:

```
org/tier3_junior/0.3.1_RD_PortfolioManagement/task_orders/{feature_name}.md
org/tier3_junior/0.3.2_RD_TradeSubmission/task_orders/{feature_name}.md
org/tier3_junior/0.3.3_RD_DataRefresh/task_orders/{feature_name}.md
org/tier3_junior/0.3.4_RD_SecurityScanner/task_orders/{feature_name}.md
org/tier2_senior/0.3.0_DS_TradingOperations/task_orders/{feature_name}.md
org/tier2_senior/0.3.0_DT_TradingOperations/task_orders/{feature_name}.md
```

Receive task orders from CTO/COO/Andrew at:
```
org/tier2_senior/0.3.0_DE_TradingOperations/task_orders/
```

---

## Session Logs

Location: `org/tier2_senior/0.3.0_DE_TradingOperations/logs/YYYY-MM-DD/`
Template: Standard log format in AGENT_START_HERE.md. Required sections: Current State and Next Steps.

---

## Launch Protocol (Every Session)

```
1. Read your own recent logs (org/tier2_senior/0.3.0_DE_TradingOperations/logs/)
2. Review recent git commits from your RD agents:
   grep for 0.3.1_RD, 0.3.2_RD, 0.3.3_RD, 0.3.4_RD in commit messages
3. If any commits are NOT covered by your existing session logs:
   -> Write a catch-up session log BEFORE doing anything else
4. Check task_orders/ for new instructions from CTO/COO/Andrew
5. Check task order status of outstanding orders you've issued
6. Proceed with normal work
```

## Session Log Format

**DE logs include commit hashes in the header:**

```
**Portal DEV commits:** `abc1234` -> `def5678` -> `ghi9012`
**Workspace CLOUD commit:** `jkl3456`
```

**Files Modified must be a table with commit column:**

```
| File | Change | Committed |
|------|--------|-----------|
| portal/src/pages/X/Component.tsx | What changed | Yes - `abc1234` |
| docs/briefs/feature.md | New brief | Yes - CLOUD `jkl3456` |
```

**When something breaks, embed a Postmortem section** between Work Completed and Decisions Made:

```
## Postmortem: [What broke]

### Root Cause
[Specific cause — name the file, function, or data shape that was wrong]

### Mismatches Found

| Field | Expected (portal) | Actual (backend) |
|-------|-------------------|------------------|
| views | { aua, nna, geo, adv } | { geo, adv } only |

### Resolution
- Task A: [what was fixed] — DONE / BLOCKED / [Agent name]
- Task B: [what remains] — BLOCKED on [Agent]
```

**Next Steps must name the receiving agent in brackets:**
`[DevOps] Run gold layer FULL mode — brief at docs/briefs/devops-brief-feature.md`
`[Dashboard Engineer] Verify Distribution tab after data refresh`


---

## Reference Material

### Briefing Notes

This is a Pattern 0 design-alignment thread for SSCN_PORTAL. The COO's directive is: SecurityScanner must mirror PortfolioManagement's visual language as closely as possible. PM is the most production-complete page in the portal. SSCN should reuse PM patterns rather than reinvent them.

The data architecture is already settled (SSCN_PORTAL-001):
- Server-side precompute monthly: per-factor percentiles per universe
- Client-side: composite score + rank (sum of pctls * weight / 100)
- API: GET /api/scoped/security-scanner/factors, /universe/{universeId}/data, /universe/{universeId}/scanner
- JSON row shape: { ticker, name, mktVal, sector, industryGroup, values: Record<FactorCode, number|null>, pctls: Record<FactorCode, number|null> }
- 6 universes: sp500/r1000/r1000v/acwx/eafe/eafev
- 284 scoring factor columns in source data

This thread resolves the DESIGN side:
1. Which PM utilities/patterns can be imported directly by SSCN (zero copying)?
2. Which PM patterns need abstraction to a shared location before SSCN uses them?
3. What new SSCN-specific components are needed (no PM equivalent)?
4. What does the SSCN DESIGN_SPEC.md skeleton look like?

The output is an approved component reuse plan that 0.3.4_RD_SecurityScanner can build against.


### pm-alphatab----factor-table-with-3-state-sort-canonical--asc--desc-search-filter-group-display.-most-directly-analogous-to-sscn-factor-bank-tab..tsx

```
/**
 * Alpha Tab - Factor Attribution
 *
 * Shows how much alpha each factor contributes to the portfolio
 * Features:
 * - Total Alpha summary (separated from factors)
 * - Filter by factor group (size, growth, value, etc.)
 * - Search by factor name
 * - Sortable columns
 * - Color-coded Trade column
 */

import React, { useState, useMemo } from 'react'
import { Search, HelpCircle } from 'lucide-react'
import { Panel } from '@/ui/components/panels/Panel'
import { PanelHeader } from '@/ui/components/panels/PanelHeader'
import { PanelContent } from '@/ui/components/panels/PanelContent'
import { Tooltip } from '@/components/Tooltip'
import type { AlphaFactor } from '@/types/portfolio-optimization'
import { FACTOR_DESCRIPTIONS } from '../utils/factorDescriptions'
import { canonicalGroupIndex } from '../utils/factorOrder'

interface AlphaTabProps {
  alphaFactors: AlphaFactor[]
}

export function AlphaTab({ alphaFactors }: AlphaTabProps) {
  const [viewMode, setViewMode] = useState<'factor' | 'group'>('factor')
  const [searchQuery, setSearchQuery] = useState('')
  const [groupFilter, setGroupFilter] = useState<string>('all')
  // 3-state sort: 'default' (Yang's canonical order) → 'desc' → 'asc' → 'default'
  const [sortColumn, setSortColumn] = useState<keyof AlphaFactor | null>(null)
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc')

  // Separate Total Alpha from individual factors
  const totalAlpha = useMemo(() => {
    return alphaFactors.find(f => f.factor === 'alpha' || f.name === 'Total Alpha')
  }, [alphaFactors])

  const individualFactors = useMemo(() => {
    return alphaFactors.filter(f => f.factor !== 'alpha' && f.name !== 'Total Alpha')
  }, [alphaFactors])

  // Get unique groups for filter dropdown
  const groups = useMemo(() => {
    const uniqueGroups = new Set(individualFactors.map(f => f.group).filter(g => g !== '-'))
    return ['all', ...Array.from(uniqueGroups).sort()]
  }, [individualFactors])

  // Aggregate individual factors by group for By Group view
  const groupedFactors = useMemo(() => {
    const map = new Map<string, { group: string; initial: number; optimized: number; benchmark: number; trade: number; initialBet: number; optimizedBet: number }>()
    for (const f of individualFactors) {
      const key = f.group || '—'
      const existing = map.get(key)
      if (existing) {
        existing.initial += f.initial ?? 0
        existing.optimized += f.optimized ?? 0
        existing.benchmark += f.benchmark ?? 0
        existing.trade += f.trade ?? 0
        existing.initialBet += f.initialBet ?? 0
        existing.optimizedBet += f.optimizedBet ?? 0
      } else {
        map.set(key, {
          group: key,
          initial: f.initial ?? 0,
          optimized: f.optimized ?? 0,
          benchmark: f.benchmark ?? 0,
          trade: f.trade ?? 0,
          initialBet: f.initialBet ?? 0,
          optimizedBet: f.optimizedBet ?? 0,
        })
      }
    }
    return Array.from(map.values()).sort((a, b) => canonicalGroupIndex(a.group) - canonicalGroupIndex(b.group))
  }, [individualFactors])

  // Filter and sort factors
  const filteredFactors = useMemo(() => {
    let filtered = individualFactors

    // Search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(
        f => f.factor.toLowerCase().includes(query) || f.name.toLowerCase().includes(query)
      )
    }

    // Group filter
    if (groupFilter !== 'all') {
      filtered = filtered.filter(f => f.group === groupFilter)
    }

    // Sort — null sortColumn means Yang's canonical order (array index from lambda)
    if (sortColumn !== null) {
      filtered = [...filtered].sort((a, b) => {
        const aVal = a[sortColumn]
        const bVal = b[sortColumn]

        if (typeof aVal === 'number' && typeof bVal === 'number') {
          return sortDirection === 'asc' ? aVal - bVal : bVal - aVal
        }

        return sortDirection === 'asc'
          ? String(aVal).localeCompare(String(bVal))
          : String(bVal).localeCompare(String(aVal))
      })
    }

    return filtered
  }, [individualFactors, searchQuery, groupFilter, sortColumn, sortDirection])

  // 3-state cycle: click → desc, click → asc, click → default (canonical)
  const handleSort = (column: keyof AlphaFactor) => {
    if (sortColumn === column) {
      if (sortDirection === 'desc') {
        setSortDirection('asc')
      } else {
        // asc → back to default
        setSortColumn(null)
      }
    } else {
      setSortColumn(column)
      setSortDirection('desc')
    }
  }

  // Show placeholder if no data
  if (alphaFactors.length === 0) {
    return (
      <Panel variant="chart">
        <PanelHeader
          title="Alpha Decomposition"
          helpText="Factor attribution showing how each alpha factor contributes to portfolio performance relative to benchmark."
        />
        <PanelContent>
          <div className="text-center py-12 text-white/40">
            No alpha factor data available
            <br />
            <span className="text-sm">Load portfolio data to see factor decomposition</span>
          </div>
        </PanelContent>
      </Panel>
    )
  }

  return (
    <Panel variant="chart">
      <PanelHeader
        title="Alpha Decomposition"
        helpText="Factor attribution showing how each alpha factor contributes to portfolio performance relative to benchmark."
        actions={
          <div className="flex items-center gap-3">
            {/* Search — only in By Factor mode */}
            {viewMode === 'factor' && (
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-white/40" />
                <input
                  type="text"
                  placeholder="Search factor..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-[200px] pl-10 pr-4 py-1.5 bg-white/10 border border-white/20 rounded-lg text-white text-sm placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-[hsl(var(--primary))]"
                />
              </div>
            )}

            {/* View Toggle */}
            <div className="flex items-center gap-2">
              <label className="text-xs text-white/50 tracking-wider">View:</label>
              <div className="flex gap-1">
                <button
                  onClick={() => setViewMode('factor')}
                  className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                    viewMode === 'factor'
                      ? 'bg-[hsl(var(--primary))] text-white'
                      : 'bg-white/10 text-white/60 hover:bg-white/15 hover:text-white/80'
                  }`}
                >
                  By Factor
                </button>
                <button
                  onClick={() => setViewMode('group')}
                  className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                    viewMode === 'group'
                      ? 'bg-[hsl(var(--primary))] text-white'
                      : 'bg-white/10 text-white/60 hover:bg-white/15 hover:text-white/80'
                  }`}
                >
                  By Group
                </button>
              </div>
            </div>

            {/* Group Filter — only in By Factor mode */}
            {viewMode === 'factor' && (
              <div className="flex items-center gap-2">
                <label className="text-xs text-white/50 tracking-wider">Group:</label>
                <select
                  value={groupFilter}
                  onChange={(e) => setGroupFilter(e.target.value)}
                  className="px-3 py-1.5 rounded-lg bg-white/10 border border-white/20 text-white text-sm font-medium focus:outline-none focus:ring-2 focus:ring-[hsl(var(--primary))] min-w-[140px]"
                >
                  {groups.map(group => (
                    <option key={group} value={group} className="bg-[hsl(var(--bg-header))] text-white">
                      {group === 'all' ? 'All Groups' : group}
                    </option>
                  ))}
                </select>
              </div>
            )}
          </div>
        }
      />

      <PanelContent>
        {/* Nested container - rounded edges, no padding (table fills edge-to-edge) */}
        <div className="rounded-lg border border-white/10 overflow-hidden">
          {/* By Group view */}
          {viewMode === 'group' && (
            <div className="overflow-x-auto">
            <table className="w-full border-collapse text-sm">
              {totalAlpha && (
                <thead>
                  <tr className="bg-[hsl(var(--bg-header))] border-b-2 border-white/20">
                    <th colSpan={2} className="py-4 px-6 text-left font-semibold text-base text-white uppercase tracking-wider">
                      Total Alpha
                    </th>
                    <th className="py-4 px-6 text-right">
                      <div className="text-xs text-white/40 font-normal mb-1">Initial</div>
                      <div className="text-lg font-mono font-semibold text-white">{totalAlpha.initial?.toFixed(2) ?? '—'}</div>
                    </th>
                    <th className="py-4 px-6 text-right">
                      <div className="text-xs text-white/40 font-normal mb-1">Optimized</div>
                      <div className="text-lg font-mono font-semibold text-white">{totalAlpha.optimized?.toFixed(2) ?? '—'}</div>
                    </th>
                    <th className="py-4 px-6 text-right">
                      <div className="text-xs text-white/40 font-normal mb-1">Benchmark</div>
                      <div className="text-lg font-mono font-semibold text-white/60">{totalAlpha.benchmark?.toFixed(2) ?? '—'}</div>
                    </th>
                    <th className="py-4 px-6 text-right">
                      <div className="text-xs text-white/40 font-normal mb-1">Trade</div>
                      <div className={`text-lg font-mono font-semibold ${getTradeColor(totalAlpha.trade ?? 0)}`}>
                        {totalAlpha.trade !== undefined ? (totalAlpha.trade >= 0 ? '+' : '') + totalAlpha.trade.toFixed(2) : '—'}
                      </div>
                    </th>
                    <th className="py-4 px-6 text-right">
                      <div className="text-xs text-white/40 font-normal mb-1">Initial Bet</div>
                      <div className="text-lg font-mono font-semibold text-white/60">{totalAlpha.initialBet?.toFixed(2) ?? '—'}</div>
                    </th>
                    <th className="py-4 px-6 text-right">
                      <div className="text-xs text-white/40 font-normal mb-1">Optimized Bet</div>
                      <div className="text-lg font-mono font-semibold text-white">{totalAlpha.optimizedBet?.toFixed(2) ?? '—'}</div>
                    </th>
                  </tr>
                </thead>
              )}
              <thead>
                <tr className="bg-[hsl(var(--bg-header))] border-b border-white/10">
                  <th className="py-3 px-6 text-left font-semibold text-xs uppercase tracking-wide text-white/40">Group</th>
                  <th className="py-3 px-6" />
                  <th className="py-3 px-6 text-right font-semibold text-xs uppercase tracking-wide text-white/40">Initial</th>
                  <th className="py-3 px-6 text-right font-semibold text-xs uppercase tracking-wide text-white/40">Optimized</th>
                  <th className="py-3 px-6 text-right font-semibold text-xs uppercase tracking-wide text-white/40">Benchmark</th>
                  <th className="py-3 px-6 text-right font-semibold text-xs uppercase tracking-wide text-white/40">Trade</th>
                  <th className="py-3 px-6 text-right font-semibold text-xs uppercase tracking-wide text-white/40">Initial Bet</th>
                  <th className="py-3 px-6 text-right font-semibold text-xs uppercase tracking-wide text-white/40">Optimized Bet</th>
                </tr>
              </thead>
              <tbody>
                {groupedFactors.map((g) => (
                  <tr key={g.group} className="border-b border-white/5 odd:bg-white/[0.05] hover:bg-white/10">
                    <td className="py-3 px-6 font-medium text-white/80 capitalize">{g.group}</td>
                    <td className="py-3 px-6" />
                    <td className="py-3 px-6 text-right font-mono text-white/80">{g.initial.toFixed(2)}</td>
                    <td className="py-3 px-6 text-right font-mono text-white/80">{g.optimized.toFixed(2)}</td>
                    <td className="py-3 px-6 text-right font-mono text-white/60">{g.benchmark.toFixed(2)}</td>
                    <td className={`py-3 px-6 text-right font-mono font-semibold ${getTradeColor(g.trade)}`}>
                      {(g.trade >= 0 ? '+' : '') + g.trade.toFixed(2)}
                    </td>
                    <td className={`py-3 px-6 text-right font-mono ${getTradeColor(g.initialBet)}`}>{g.initialBet.toFixed(2)}</td>
                    <td className={`py-3 px-6 text-right font-mono ${getTradeColor(g.optimizedBet)}`}>{g.optimizedBet.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            </div>
          )}

          {/* By Factor view (default) */}
          {viewMode === 'factor' && (
          <div className="overflow-x-auto">
          <table className="w-full border-collapse text-sm">
            {/* Total Alpha Summary Row */}
            {totalAlpha && (
              <thead>
                <tr className="bg-[hsl(var(--bg-header))] border-b-2 border-white/20">
                  {/* Factor + Group columns merged */}
                  <th colSpan={2} className="py-4 px-6 text-left font-semibold text-base text-white uppercase tracking-wider">
                    Total Alpha
                  </th>
                  {/* Values aligned with columns */}
                  <th className="py-4 px-6 text-right">
                    <div className="text-xs text-white/40 font-normal mb-1">Initial</div>
                    <div className="text-lg font-mono font-semibold text-white">
                      {totalAlpha.initial?.toFixed(2) ?? '—'}
                    </div>
                  </th>
                  <th className="py-4 px-6 text-right">
                    <div className="text-xs text-white/40 font-normal mb-1">Optimized</div>
                    <div className="text-lg font-mono font-semibold text-white">
                      {totalAlpha.optimized?.toFixed(2) ?? '—'}
                    </div>
                  </th>
                  <th className="py-4 px-6 text-right">
                    <div className="text-xs text-white/40 font-normal mb-1">Benchmark</div>
                    <div className="text-lg font-mono font-semibold text-white/60">
                      {totalAlpha.benchmark?.toFixed(2) ?? '—'}
                    </div>
                  </th>
                  <th className="py-4 px-6 text-right">
                    <div className="text-xs text-white/40 font-normal mb-1">Trade</div>
                    <div className={`text-lg font-mono font-semibold ${getTradeColor(totalAlpha.trade ?? 0)}`}>
                      {totalAlpha.trade !== undefined ? (totalAlpha.trade >= 0 ? '+' : '') + totalAlpha.trade.toFixed(2) : '—'}
                    </div>
                  </th>
                  <th className="py-4 px-6 text-right">
                    <div className="text-xs text-white/40 font-normal mb-1">Initial Bet</div>
                    <div className="text-lg font-mono font-semibold text-white/60">
                      {totalAlpha.initialBet?.toFixed(2) ?? '—'}
                    </div>
                  </th>
                  <th className="py-4 px-6 text-right">
                    <div className="text-xs text-white/40 font-normal mb-1">Optimized Bet</div>
                    <div className="text-lg font-mono font-semibold text-white">
                      {totalAlpha.optimizedBet?.toFixed(2) ?? '—'}
                    </div>
                  </th>
                </tr>
              </thead>
            )}

            {/* Column Headers */}
            <thead>
              <tr className="bg-[hsl(var(--bg-header))] border-b border-white/10">
                <SortableHeader
                  label="Factor"
                  column="factor"
                  sortColumn={sortColumn}
                  sortDirection={sortDirection}
                  onSort={handleSort}
                />
                <SortableHeader
                  label="Group"
                  column="group"
                  sortColumn={sortColumn}
                  sortDirection={sortDirection}
                  onSort={handleSort}
                />
                <SortableHeader
                  label="Initial"
                  column="initial"
                  sortColumn={sortColumn}
                  sortDirection={sortDirection}
                  onSort={handleSort}
                  align="right"
                />
                <SortableHeader
                  label="Optimized"
                  column="optimized"
                  sortColumn={sortColumn}
                  sortDirection={sortDirection}
                  onSort={handleSort}
                  align="right"
                />
                <SortableHeader
                  label="Benchmark"
                  column="benchmark"
                  sortColumn={sortColumn}
                  sortDirection={sortDirection}
                  onSort={handleSort}
                  align="right"
                />
                <SortableHeader
                  label="Trade"
                  column="trade"
                  sortColumn={sortColumn}
                  sortDirection={sortDirection}
                  onSort={handleSort}
                  align="right"
                />
                <SortableHeader
                  label="Initial Bet"
                  column="initialBet"
                  sortColumn={sortColumn}
                  sortDirection={sortDirection}
                  onSort={handleSort}
                  align="right"
                />
                <SortableHeader
                  label="Optimized Bet"
                  column="optimizedBet"
                  sortColumn={sortColumn}
                  sortDirection={sortDirection}
                  onSort={handleSort}
                  align="right"
                />
              </tr>
            </thead>
            <tbody>
              {filteredFactors.map((factor) => (
                <tr key={factor.factor} className="border-b border-white/5 odd:bg-white/[0.05] hover:bg-white/10">
                  <td className="py-3 px-6 font-medium text-white/80">
                    <div className="flex items-center gap-1.5">
                      <span>{factor.name || factor.factor}</span>
                      <Tooltip content={FACTOR_DESCRIPTIONS[factor.factor] ?? factor.factor} side="right">
                        <HelpCircle size={13} className="text-white/30 hover:text-white/60 transition-colors cursor-help flex-shrink-0" />
                      </Tooltip>
                    </div>
                  </td>
                  <td className="py-3 px-6 text-white/60 capitalize">{factor.group}</td>
                  <td className="py-3 px-6 text-right font-mono text-white/80">
                    {factor.initial?.toFixed(2) ?? '—'}
                  </td>
                  <td className="py-3 px-6 text-right font-mono text-white/80">
                    {factor.optimized?.toFixed(2) ?? '—'}
                  </td>
                  <td className="py-3 px-6 text-right font-mono text-white/60">
                    {factor.benchmark?.toFixed(2) ?? '—'}
                  </td>
                  <td className={`py-3 px-6 text-right font-mono font-semibold ${getTradeColor(factor.trade ?? 0)}`}>
                    {factor.trade !== undefined ? (factor.trade >= 0 ? '+' : '') + factor.trade.toFixed(2) : '—'}
                  </td>
                  <td className={`py-3 px-6 text-right font-mono ${getTradeColor(factor.initialBet ?? 0)}`}>
                    {factor.initialBet?.toFixed(2) ?? '—'}
                  </td>
                  <td className={`py-3 px-6 text-right font-mono ${getTradeColor(factor.optimizedBet ?? 0)}`}>
                    {factor.optimizedBet?.toFixed(2) ?? '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        )}
        </div>
      </PanelContent>
    </Panel>
  )
}

// ============================================================================
// Helper Components
// ============================================================================

interface SortableHeaderProps {
  label: string
  column: keyof AlphaFactor
  sortColumn: keyof AlphaFactor | null
  sortDirection: 'asc' | 'desc'
  onSort: (column: keyof AlphaFactor) => void
  align?: 'left' | 'right'
}

function SortableHeader({
  label,
  column,
  sortColumn,
  sortDirection,
  onSort,
  align = 'left'
}: SortableHeaderProps) {
  const isActive = sortColumn === column
  const textAlign = align === 'right' ? 'text-right' : 'text-left'

  return (
    <th
      className={`py-3 px-6 ${textAlign} font-semibold text-xs uppercase tracking-wide text-white/40 cursor-pointer hover:text-white/60 transition-colors`}
      onClick={() => onSort(column)}
    >
      <div className={`flex items-center gap-1 ${align === 'right' ? 'justify-end' : ''}`}>
        {label}
        {isActive && (
          <span className="text-[hsl(var(--primary))]">
            {sortDirection === 'asc' ? '\u2191' : '\u2193'}
          </span>
        )}
      </div>
    </th>
  )
}

// ============================================================================
// Utility Functions
// ============================================================================

function getTradeColor(value: number): string {
  if (value > 0.1) return 'text-[hsl(var(--success))]'
  if (value < -0.1) return 'text-[hsl(var(--danger))]'
  return 'text-white/40'
}
```

### pm-colorutils----getgradientbackground-redyellowgreen-gradient-getwhitetogreengradient.-primary-candidate-for-sscn-quintile-coloring-on-universe-scanner-tab..ts

```
/**
 * Gradient color utilities for PortfolioManagement
 *
 * Extracted from PortfolioGrid.tsx so ModelTab and other consumers
 * can reuse the same gradient logic.
 */

/**
 * Get gradient background color based on value relative to min/max
 *
 * Color mapping:
 * - Max value -> Bright green (#10b981)
 * - Zero (0) -> Yellow (#eab308)
 * - Min value -> Bright red (#ef4444)
 *
 * When inverted = true:
 * - Max value -> Bright red (high = bad)
 * - Zero (0) -> Yellow
 * - Min value -> Bright green (low = good)
 */
export function getGradientBackground(value: number, min: number, max: number, inverted = false): string {
  // Handle edge cases
  if (min === max) return 'rgba(234, 179, 8, 0.2)' // Yellow if all same

  // Normalize value to 0-1 range
  let normalized: number

  if (value >= 0) {
    // Positive values: interpolate from yellow (0) to green/red (max)
    if (max <= 0) {
      normalized = 0
    } else {
      normalized = value / max
    }

    const yellow = { r: 234, g: 179, b: 8 }   // #eab308
    const positive = inverted
      ? { r: 239, g: 68, b: 68 }   // #ef4444 (red when inverted — high risk = bad)
      : { r: 16, g: 185, b: 129 }  // #10b981 (green — high alpha = good)

    const r = Math.round(yellow.r + (positive.r - yellow.r) * normalized)
    const g = Math.round(yellow.g + (positive.g - yellow.g) * normalized)
    const b = Math.round(yellow.b + (positive.b - yellow.b) * normalized)

    const opacity = 0.5 + (normalized * 0.35)

    return `rgba(${r}, ${g}, ${b}, ${opacity})`
  } else {
    // Negative values: interpolate from yellow (0) to red/green (min)
    if (min >= 0) {
      normalized = 0
    } else {
      normalized = Math.abs(value / min)
    }

    const yellow = { r: 234, g: 179, b: 8 }   // #eab308
    const negative = inverted
      ? { r: 16, g: 185, b: 129 }  // #10b981 (green when inverted — low risk = good)
      : { r: 239, g: 68, b: 68 }   // #ef4444 (red — negative alpha = bad)

    const r = Math.round(yellow.r + (negative.r - yellow.r) * normalized)
    const g = Math.round(yellow.g + (negative.g - yellow.g) * normalized)
    const b = Math.round(yellow.b + (negative.b - yellow.b) * normalized)

    const opacity = 0.5 + (normalized * 0.35)

    return `rgba(${r}, ${g}, ${b}, ${opacity})`
  }
}

/**
 * Simple white-to-green gradient for non-negative values (Model tab).
 * Maps 0 -> white, max -> green.
 */
export function getWhiteToGreenGradient(value: number, min: number, max: number): string {
  if (max === min) return 'rgba(255, 255, 255, 0.1)'

  const range = max - min
  const normalized = range > 0 ? (value - min) / range : 0
  const clamped = Math.max(0, Math.min(1, normalized))

  // White to green
  const white = { r: 255, g: 255, b: 255 }
  const green = { r: 16, g: 185, b: 129 } // #10b981

  const r = Math.round(white.r + (green.r - white.r) * clamped)
  const g = Math.round(white.g + (green.g - white.g) * clamped)
  const b = Math.round(white.b + (green.b - white.b) * clamped)

  const opacity = 0.15 + (clamped * 0.45)

  return `rgba(${r}, ${g}, ${b}, ${opacity})`
}
```

### pm-designspec----portfoliomanagement-ui-design-spec-panel-framework-tab-layout-snapshot-header-design-token-references-use-this-as-the-visual-template.md

```
# Portfolio Management - UI Design Specification

## Overview

Redesign the Portfolio Management page to match the canonical panel design framework used throughout the Opal portal. This page is a **tool/write function** (not read), so we'll use **mock data** for the snapshot and time series sections.

---

## Reference Pages for Design Patterns

Study these existing pages for design patterns:

| Pattern | Reference File |
|---------|----------------|
| Page header + snapshot metrics | `Positioning/Positioning.tsx` |
| Panel framework (Card variant="gradient") | `Positioning/components/HoldingsTable.tsx` |
| Time series charts | `FactorTilts/tabs/FactorTiltTimeSeriesTab.tsx` |
| Radial/summary charts | `Positioning/components/PortfolioRadialCharts.tsx` |
| Tab navigation | `Positioning/Positioning.tsx` |
| Table with sorting/filtering | `Positioning/components/HoldingsTable.tsx` |
| Color tokens | `lib/designTokens.ts` |

---

## Page Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PAGE HEADER                                                                │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ [Icon] Portfolio Management           [Strategy Selector: PFDE ▼]     │ │
│  │ Review and execute portfolio rebalancing trades                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│  PORTFOLIO SNAPSHOT (Panel - always visible)                               │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌───────┐ │ │
│  │ │   AUM   │ │Positions│ │  Beta   │ │ Active  │ │Expected │ │Turnover│ │ │
│  │ │ $30.2M  │ │   72    │ │  1.02   │ │ Share   │ │ Alpha   │ │  8.2% │ │ │
│  │ │         │ │         │ │         │ │  12.4%  │ │  1.8%   │ │       │ │ │
│  │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └───────┘ │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│  PERFORMANCE TIME SERIES (Panel - always visible)                          │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ Performance vs Benchmark                              [1M|3M|6M|1Y]    │ │
│  │ ┌────────────────────────────────────────────────────────────────────┐ │ │
│  │ │                    ════════════════════════                        │ │ │
│  │ │              ══════                      ══════                    │ │ │
│  │ │         ═════                                  ═════               │ │ │
│  │ │    ═════  Portfolio ━━━  Benchmark ━━━              ═════          │ │ │
│  │ └────────────────────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│  WORKFLOW TABS                                                              │
│  ┌──────────────────┬──────────────────┬──────────────────┐                │
│  │   ① Import       │   ② Review       │   ③ Export       │                │
│  └──────────────────┴──────────────────┴──────────────────┘                │
├─────────────────────────────────────────────────────────────────────────────┤
│  TAB CONTENT AREA                                                           │
│  [Content varies by active tab - see below]                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Section 1: Portfolio Snapshot Panel

### Design Requirements

- Use the `Panel` component from `@/ui/components/panels` (PanelHeader, PanelContent pattern)
- OR use `Card variant="gradient"` with proper styling
- 6 metric cards in a responsive grid (6 columns on desktop, 3 on tablet, 2 on mobile)
- Each metric card should have:
  - Icon with colored background (following existing color patterns)
  - Label (uppercase, small, muted)
  - Value (large, bold, white)
  - Optional delta/change indicator

### Metrics to Display (Mock Data)

| Metric | Mock Value | Icon | Color |
|--------|------------|------|-------|
| AUM | $30.2M | DollarSign | emerald-500 |
| Positions | 72 | Briefcase | blue-500 |
| Beta | 1.02 | TrendingUp | purple-500 |
| Active Share | 12.4% | Activity | amber-500 |
| Expected Alpha | +1.8% | Target | cyan-500 |
| Turnover | 8.2% | RefreshCw | rose-500 |

### Color Pattern Reference

Follow the color tokens from existing panels:
```typescript
// From designTokens.ts / existing components
emerald: 'bg-emerald-500/10 text-emerald-400'
blue: 'bg-blue-500/10 text-blue-400'
purple: 'bg-purple-500/10 text-purple-400'
amber: 'bg-amber-500/10 text-amber-400'
cyan: 'bg-cyan-500/10 text-cyan-400'
rose: 'bg-rose-500/10 text-rose-400'
```

---

## Section 2: Performance Time Series Panel

### Design Requirements

- Use `Card variant="gradient"` wrapper
- Header with title + period selector buttons (1M, 3M, 6M, 1Y)
- Recharts AreaChart with dual series (Portfolio vs Benchmark)
- Follow the chart styling from `FactorTiltTimeSeriesTab.tsx`
- Height: 200-250px

### Chart Styling

```typescript
// Portfolio line
stroke: '#4CAF50' // Green
fill: 'url(#portfolioGradient)' // Green gradient fade

// Benchmark line
stroke: '#64748b' // Slate/gray (muted)
fill: 'url(#benchmarkGradient)' // Gray gradient fade
strokeDasharray: '4 4' // Dashed line for benchmark
```

### Mock Data Structure

Generate 365 days of mock performance data:
```typescript
const mockPerformanceData = generateMockTimeSeries({
  days: 365,
  portfolioVolatility: 0.15,
  benchmarkVolatility: 0.12,
  portfolioAlpha: 0.02, // 2% annual alpha
})
```

---

## Section 3: Tab Content Areas

### Tab 1: Import

**Purpose**: Upload optimizer output file (JSON or pickle)

**Layout**:
```
┌─────────────────────────────────────────────────────────────────┐
│  UPLOAD PANEL (Card variant="gradient")                         │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                                                           │  │
│  │     ┌──────────────────────────────────────────────┐     │  │
│  │     │          [Upload Icon]                       │     │  │
│  │     │                                              │     │  │
│  │     │   Drag and drop your optimizer output here   │     │  │
│  │     │        or click to browse                    │     │  │
│  │     │                                              │     │  │
│  │     │         [.json]  [.pkl]                      │     │  │
│  │     └──────────────────────────────────────────────┘     │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  IMPORT PREVIEW (Card variant="gradient") - Shows after upload  │
│  ┌─────────────────────────────────┬─────────────────────────┐  │
│  │ Import Summary                  │ Trade Breakdown         │  │
│  │ ─────────────────               │ ─────────────────       │  │
│  │ Strategy: PFDE                  │ ┌───┐ ┌───┐ ┌───┐      │  │
│  │ As of Date: Jan 15, 2024        │ │32 │ │28 │ │12 │      │  │
│  │ Total Positions: 72             │ │BUY│ │SELL│ │HOLD│     │  │
│  │ AUM: $30.2M                     │ └───┘ └───┘ └───┘      │  │
│  │ Expected Turnover: 8.2%         │                         │  │
│  └─────────────────────────────────┴─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Design Notes**:
- Drag-drop zone: dashed border, highlight on drag-over with primary color
- File type badges in monospace font
- After upload: show success state with green checkmark
- Preview panel uses 2-column layout

---

### Tab 2: Review

**Purpose**: Review and edit trade recommendations

**Layout**:
```
┌─────────────────────────────────────────────────────────────────┐
│  TRADE SUMMARY PANEL (Card variant="gradient")                  │
│  ┌───────────┬───────────┬───────────┬───────────┬───────────┐ │
│  │  BUYS     │  SELLS    │ TURNOVER  │ OVERRIDES │  HOLDS    │ │
│  │   32      │   28      │   8.2%    │    0      │   12      │ │
│  │  $2.4M    │  $2.1M    │   $2.3M   │           │           │ │
│  │  ↑ green  │  ↓ red    │  ↔ blue   │  ✏ amber  │  — gray   │ │
│  └───────────┴───────────┴───────────┴───────────┴───────────┘ │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  ACTION BAR                                                     │
│  72 positions • 32 buys • 28 sells    [Accept All] [Reset All] │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  TRADE TABLE (Card variant="gradient")                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ [Search...]  [Sector ▼]  [Action ▼]      72 trades [CSV]  │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │ Ticker│Name     │Sector│Curr%│Sugg%│Delta│Alpha│Action│...│  │
│  │───────┼─────────┼──────┼─────┼─────┼─────┼─────┼──────┼───│  │
│  │ AAPL  │Apple Inc│Tech  │3.20 │3.80 │+0.60│0.012│ BUY  │...│  │
│  │ MSFT  │Microsoft│Tech  │4.10 │3.50 │-0.60│0.008│ SELL │...│  │
│  │ ...   │...      │...   │...  │...  │...  │...  │...   │...│  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Table Columns**:
| Column | Width | Align | Notes |
|--------|-------|-------|-------|
| Ticker | 80px | left | Bold, monospace |
| Name | flex | left | Truncate with tooltip |
| Sector | 120px | left | Badge style |
| Current Wt | 80px | right | 2 decimals + % |
| Suggested Wt | 80px | right | 2 decimals + % |
| Delta | 80px | right | Color-coded (+green, -red) |
| Alpha | 80px | right | 4 decimals |
| Action | 70px | center | Badge (BUY=green, SELL=red, HOLD=gray) |
| Override | 60px | center | Checkbox |
| Final Wt | 80px | right | Input (disabled until override checked) |
| Comment | 150px | left | Text input |

**Design Notes**:
- Follow `HoldingsTable.tsx` patterns exactly
- Sticky header on scroll
- Row highlight on hover (`hover:bg-white/5`)
- Overridden rows get subtle amber background (`bg-amber-500/5`)
- Max height with scroll (600px)

---

### Tab 3: Export

**Purpose**: Final review and CSV download for Schwab

**Layout**:
```
┌─────────────────────────────────────────────────────────────────┐
│  EXPORT CONFIGURATION (Card variant="gradient")                 │
│  ┌─────────────────────────────┬─────────────────────────────┐  │
│  │ Schwab Account Number       │ Export Summary              │  │
│  │ ┌─────────────────────────┐ │ ─────────────────           │  │
│  │ │ [                     ] │ │ Strategy: PFDE              │  │
│  │ └─────────────────────────┘ │ Trades to Export: 60        │  │
│  │                             │ Estimated Value: $4.5M      │  │
│  │                             │ Overridden: 3               │  │
│  └─────────────────────────────┴─────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  TRADES TO EXECUTE (Card variant="gradient")                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ [Read-only trade table - HOLD trades filtered out]        │  │
│  │ Shows only BUY and SELL trades that will be exported      │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  CONFIRMATION (Card variant="gradient")                         │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ [✓] I confirm I have reviewed all trades and am ready     │  │
│  │     to export for execution.                              │  │
│  │                                                           │  │
│  │ This will generate a CSV file formatted for Schwab's      │  │
│  │ trade upload system.                                      │  │
│  │                                        ┌─────────────────┐│  │
│  │                                        │ Download CSV    ││  │
│  │                                        │ [↓]             ││  │
│  │                                        └─────────────────┘│  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Design Notes**:
- Download button: Primary color, disabled until checkbox checked
- Warning messages in amber if validation fails
- Success message in green when ready to export
- Trade table is read-only (no edit columns)

---

## Mock Data Generator

Create `utils/mockData.ts` with generators for:

```typescript
// Mock portfolio metrics
export const MOCK_PORTFOLIO_METRICS = {
  aum: 30_200_000,
  positions: 72,
  beta: 1.02,
  activeShare: 0.124,
  expectedAlpha: 0.018,
  turnover: 0.082,
  asOfDate: '2024-01-15',
}

// Mock trade data (72 positions)
export function generateMockTrades(): TradeRecord[] {
  // Generate realistic mock trades across sectors
  // Mix of BUY (32), SELL (28), HOLD (12)
}

// Mock performance time series (365 days)
export function generateMockPerformance(): PerformanceDataPoint[] {
  // Generate daily returns with slight alpha
}
```

---

## Color Palette Summary

| Element | Color Token | Usage |
|---------|-------------|-------|
| BUY action | emerald-400/500 | Badges, positive deltas |
| SELL action | red-400/500 | Badges, negative deltas |
| HOLD action | white/40-60 | Muted, neutral |
| Override indicator | amber-400/500 | Warning, user changes |
| Primary button | hsl(var(--primary)) | Download, primary actions |
| Panel background | Card variant="gradient" | All panels |
| Text primary | white | Values, important text |
| Text secondary | white/60-80 | Labels, descriptions |
| Text muted | white/40 | Hints, disabled |

---

## Implementation Checklist

- [ ] Refactor `PortfolioSnapshot.tsx` to use Panel component pattern
- [ ] Create `utils/mockData.ts` with generators
- [ ] Update `PerformanceChart.tsx` to match canonical chart styling
- [ ] Redesign `ImportTab.tsx` with proper panel layout
- [ ] Redesign `ReviewTab.tsx` with summary panel + action bar
- [ ] Redesign `ExportTab.tsx` with configuration + confirmation panels
- [ ] Update `TradeTable.tsx` to match `HoldingsTable.tsx` exactly
- [ ] Add responsive breakpoints for mobile/tablet
- [ ] Ensure all colors follow design tokens
- [ ] Test with mock data throughout

---

## Files to Reference

```
src/ui/components/panels/           # Panel, PanelHeader, PanelContent
src/components/Card.tsx             # Card variant="gradient"
src/pages/Positioning/              # Overall page structure
src/pages/FactorTilts/              # Time series charts
src/lib/designTokens.ts             # Color tokens
src/pages/Positioning/components/HoldingsTable.tsx  # Table patterns
```
```

### pm-factororder----canonicalgrouporder-15-groups-canonicalgroupindex.-directly-applicable-to-sscn-factor-bank-tab-category-ordering..ts

```
/**
 * Yang's canonical factor group ordering.
 *
 * Matches the signal DataFrame row order in the alpha PKL.
 * Source of truth: portal/src/pages/PortfolioManagement/utils/factorDescriptions.ts (comment order).
 * Implementation pattern mirrors ECONOMY_ORDER in TradeTab.tsx (line 249).
 */

export const CANONICAL_GROUP_ORDER = [
  'size',
  'efficiency',
  'growth',
  'management',
  'profitability',
  'quality',
  'value',
  'analyst',
  'governance',
  'crowding',
  'insider',
  'short',
  'beta',
  'momentum',
  'technical',
] as const

export type CanonicalGroup = typeof CANONICAL_GROUP_ORDER[number]

export function canonicalGroupIndex(group: string): number {
  const idx = (CANONICAL_GROUP_ORDER as readonly string[]).indexOf(group.toLowerCase())
  return idx === -1 ? CANONICAL_GROUP_ORDER.length : idx
}
```

### pm-main-page----tab-layout-shared-component-imports-pageheadercleanbadge--tabnavigation-usage-pattern.tsx

```
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
```

### security-scanner-prd----full-portal-spec-4-tabs-scoring-algorithm-universes-scannerheaderpanel-requiresdev-gate.md

```
# Security Scanner PRD

**Project:** `SSCN_PORTAL`
**Macro:** `SSCN`
**Author:** 1.0.0_SA_CTO
**Date:** 2026-03-05
**Status:** Phase 0 -- PRD + data architecture pending

---

## Overview

Port Yang's `Factor_Scanning_Model.xlsm` to the Opal Capital portal as a new page called **Security Scanner**. The Excel workbook provides multi-factor security screening across 6 universes and 255 factors across 11 categories, letting PMs select factors, assign weights, and see dynamically ranked securities.

---

## System Being Ported

The Excel workbook has 4 tabs:

### Tab 1 (1-Configuration)

Factor selection UI with "Selected Factors" and "Factor Bank" sections, universe dropdown, YES/NO toggles. 255 factors across 11 categories (Size, Efficiency, Growth, Management, Profitability, Quality, Sentiment, Systematic, Value, Yield, Institutional). Factor metadata includes: code, display name, category, coverage (PPS), relationship (Positive/Inverse), IC, autocorrelation, systematic flag.

### Tab 2 (2-Universe Data)

Full security dataset for the selected universe. All factor raw values for all securities. Read-only reference.

### Tab 3 (3-Factor Data)

Complete factor metadata -- all 255 factors with their properties (code, name, category, asset class, relationship, IC, autocorrelation, coverage, systematic flag). Static reference data.

### Tab 4 (4-Security Scanner)

Interactive scoring -- weight table (user-editable), composite score formula `=(FactorScore1*Weight1 + ... + FactorScoreN*WeightN)/100`, auto-sort by composite, rank column, per-factor percentile scores + raw values.

VBA handles: auto-sort on weight change (Worksheet_Calculate), factor move between Bank/Selected (Worksheet_Change), alternating row formatting, yellow IC highlighting, auto-rerank on open.

---

## Portal Page Design

| Field | Value |
|-------|-------|
| **Page name** | Security Scanner |
| **Route** | `/security-scanner` |
| **Sidebar** | Tools section, above Portfolio Management |
| **Icon** | `ScanLine` (from lucide-react) |
| **Access** | `requiresDev: true` (dev-only during buildout) |

### Directory Structure

```
portal/src/pages/SecurityScanner/
  SecurityScanner.tsx      # Main page orchestrator
  index.ts                 # Re-export
  types.ts                 # TabType, FactorDefinition, SecurityRow, UniverseId, etc.
  components/
    ScannerHeaderPanel.tsx  # Universe selector, factor chips, weight controls
  tabs/
    FactorBankTab.tsx       # Tab 1: Factor selection (maps Excel Tab 1)
    UniverseDataTab.tsx     # Tab 2: Full security dataset (maps Excel Tab 2)
    FactorDataTab.tsx       # Tab 3: Factor metadata reference (maps Excel Tab 3)
    UniverseScannerTab.tsx  # Tab 4: Weighted scoring + ranking (maps Excel Tab 4)
  hooks/
    useScannerState.ts      # Central state: selectedUniverse, selectedFactors, weights
```

---

## Header Panel (ScannerHeaderPanel)

Persistent above all tabs. Contains:

- **Universe dropdown** -- S&P 500, Russell 1000, Russell 1000 Value, MSCI ACWI ex-US, MSCI EAFE, MSCI EAFE Value
- **Selected factor chips** -- visual summary of active factors with count badge
- **Weight controls** -- inline editable weights per factor (must sum to 100%), or equal-weight button
- Summary stats: universe size, number of selected factors, total weight validation

State owned by parent `SecurityScanner.tsx`, passed down as props to both header and all tabs.

---

## Tab 1: Factor Bank

Maps to Excel "1-Configuration". Two sections:

- **Selected Factors** -- factors currently active (toggleable)
- **Factor Bank** -- all 255 factors, organized by 11 categories, with add/remove toggle
- Each factor row shows: category, display name, code, coverage (PPS), relationship, IC, autocorrelation, systematic flag
- Yellow highlight for highest-IC factor per category (matching Excel behavior)
- Filtering/search by category, name, or code

**Header interaction:** Selecting/deselecting factors here updates the header's selected factors and the scorer in Tab 4.

---

## Tab 2: Universe Data

Maps to Excel "2-Universe Data". Full security table for the selected universe:

- Columns: Ticker, Company Name, Market Value, Country (shown for international universes), Sector, Industry Group, then all selected factor raw values
- Sortable columns, AutoFilter equivalent
- Country column hidden for US universes (S&P 500, Russell 1000, Russell 1000 Value)

**Header interaction:** Changing universe in header reloads this tab's data.

---

## Tab 3: Factor Data

Maps to Excel "3-Factor Data". Static reference table showing all 255 factors:

- Columns: Factor Code, Factor Name, Category, Relationship (Positive/Inverse), Asset Class, Coverage, IC, Autocorrelation, Systematic (Yes/No)
- Conditional formatting: green highlight for "Systematic Equity" asset class, red for "No" systematic
- Sortable, filterable by category
- This tab is independent of header selections -- always shows the full factor universe

**Header interaction:** None -- this is static reference data.

---

## Tab 4: Universe Scanner

Maps to Excel "4-Security Scanner". The primary interactive tab:

- **Weight table** at top -- user edits weights for selected factors (must sum to 100%)
- **Scored securities table** -- all securities in selected universe, with:
  - Rank, Ticker, Name, Composite Score, Market Value, Country (conditional), Industry Group
  - Per-factor columns: Score (percentile 0-100) + Raw Value
- **Composite score** computed client-side: `(Sum of FactorScore_i * Weight_i) / 100`
- **Auto-sort** by composite score descending when weights change
- **Conditional formatting**: quintile colors on score columns, gradient on composite
- Filtering by sector, industry group, country, market cap range

**Header interaction:** Responds to both universe changes AND factor/weight changes.

---

## Universes

| Universe | Excel Column | Approx Size |
|----------|-------------|-------------|
| S&P 500 | `wt_ivv` | ~500 |
| Russell 1000 | `wt_iwb` | ~1000 |
| Russell 1000 Value | `wt_iwd` | ~850 |
| MSCI ACWI ex-US | `wt_acwx` | ~1650 |
| MSCI EAFE | `wt_efa` | ~700 |
| MSCI EAFE Value | `wt_efv` | ~400 |

---

## Factor Categories (11)

| Category | Factor Count | Examples |
|----------|-------------|----------|
| Size | 11 | mkt_val, bv, ev, sales, assets |
| Efficiency | 11 | asset_turn_chg_1yr, receiv_turn_chg_1yr |
| Growth | 25 | sales_gr_1yr, eps_gr_1yr, eps_fwd_gr_1yr |
| Management | 11 | asset_gr_1yr, capex_gr_1yr, debt_iss_gr_1yr |
| Profitability | 28 | roe, roa, roic, ebit_margin |
| Quality | 26 | accruals, fcf_accruals, asset_quality |
| Sentiment | 29 | earn_rev_up, earn_rev_down, rec_chg |
| Systematic | 38 | beta, vol, mom, reversal |
| Value | 30 | ev_ebit, pe, pb, pcf |
| Yield | 27 | div_yld, fcf_yld, earn_yld |
| Institutional | 19 | active_pctout, passive_pctout, hedge_pctout |
| **Total** | **255** | |

---

## Scoring Algorithm

Per-factor percentile: `rank(factor_value, method='average') * 100` (0-100 scale).
Inverse-relationship factors: negate value before ranking.
Composite: `(Sum of percentile_i * weight_i) / 100`.

---

## Data Architecture (Deferred)

Data source decisions deferred to a Pattern 0 thread (DS + DE + AE). Key questions for that thread:

- Where does the FactSet factor data live? (S3 static JSON vs Lambda-computed)
- How is the data refreshed? (Monthly FactSet export pipeline)
- Client-side percentile calculation vs server-side pre-computation
- API endpoint structure (`/api/private/security-scanner/...` or `/api/general/...`)

Current Excel data source: `Screening_DIVZ_IDVZ_20251028.xlsx` -- 255 factors, ~3000 securities, 6 universe weight columns.

### XLSM Audit Script (Thread Context Input)

An extraction script is available to produce a full structured audit of the source Excel workbook (`Factor_Scanning_Model.xlsm`). The output is a single markdown file containing sheet structure, all column headers, formulas, data validation rules, conditional formatting, factor metadata, and the complete VBA source code (all modules verbatim). This audit file should be generated before the Pattern 0 thread starts and provided as thread context to all participants.

**Script:** `scripts/extract_xlsm_audit.py`

```bash
python scripts/extract_xlsm_audit.py <path_to_Factor_Scanning_Model.xlsm>
```

**Output:** `docs/architecture/SECURITY_SCANNER_XLSM_AUDIT.md`

The script uses `openpyxl` (cell data, formulas, conditional formatting) and `oletools` (VBA extraction from `vbaProject.bin`). Both are installed.

---

## Existing Patterns to Reuse

| Pattern | Source | Location |
|---------|--------|----------|
| Multi-tab layout | AdvisorIntelligence | `portal/src/pages/AdvisorIntelligence/` |
| Tab navigation | Shared hook | `portal/src/hooks/useTabNavigation.ts` |
| Tab UI component | Shared component | `portal/src/components/TabNavigation.tsx` |
| Page header | Shared component | `portal/src/components/PageHeaderVariants.tsx` (`PageHeaderCleanBadge`) |
| Error boundary per tab | AdvisorIntelligence | `ErrorBoundary` + `TabErrorFallback` |
| Gradient/quintile coloring | PortfolioManagement | `portal/src/pages/PortfolioManagement/utils/colorUtils.ts` |
| Canonical factor order | PortfolioManagement | `portal/src/pages/PortfolioManagement/utils/factorOrder.ts` |
| State pattern (simple) | AdvisorIntelligence | `useState` for entity selection |

---

## Next Steps

1. COO reads this PRD
2. Pattern 0 thread (DS + DE + AE) for data architecture decisions
3. Task order decomposition to Pod 3 DE after data architecture is resolved
4. RD agent `0.3.4_RD_SecurityScanner` receives implementation task orders
```

---

## Participant Background

### 0.3.1_RD_PortfolioManagement -- Recent Commits

# Recent commits by 0.3.1_RD_PortfolioManagement

23cb2391 org(0.3.0_DT_TradingOperations): seed TradingOperations pod, pod-aligned RD serials

### 0.3.4_RD_SecurityScanner -- Recent Commits

# Recent commits by 0.3.4_RD_SecurityScanner

17ec8a99 org(1.0.0_SA_CTO): SSCN_PORTAL scaffolding + PRDs (Security Scanner, Trade Engine Visual Polish, Yang V2 Feedback)

### 0.3.0_DE_TradingOperations -- Recent Session Logs

#### wave2_pod_inventory_activation.md

# Wave 2 Pod Inventory Activation — 0.3.0_DE_TradingOperations

**Date:** 2026-03-02
**Start Time:** ~19:00
**End Time:** ~19:30

## Objective

Complete Wave 2 activation task order from 1.0.0_SA_CTO. Produce pod_inventory.xml as permanent
ground-truth context for the TradingOperations pod: PortfolioManagement, TradeSubmission, DataRefresh.

## Work Completed

- Read org/AGENT_START_HERE.md (orientation protocol)
- Read org/tier2_senior/0.3.0_DE_TradingOperations/README.md and prompt.md (identity)
- Read org/tier1_exec/1.0.0_SA_CTO/logs/2026-03-02/org_activation_plan.md (full 6-wave plan)
- Read task order: org/tier2_senior/0.3.0_DE_TradingOperations/task_orders/pod_inventory.md
- Read all 3 RD page_inventory.xml deliverables:
  - org/tier3_junior/0.3.1_RD_PortfolioManagement/deliverables/page_inventory.xml (55 files)
  - org/tier3_junior/0.3.2_RD_TradeSubmission/deliverables/page_inventory.xml (16 files)
  - org/tier3_junior/0.3.3_RD_DataRefresh/deliverables/page_inventory.xml (12 files)
- Read portal/src/api/endpoints/portfolio-optimization.ts (full)
- Read portal/src/api/endpoints/trade-submission.ts (full)
- Read portal/src/api/endpoints/portfolio.ts (full)
- Read portal/src/api/portal-proxy.ts (DataRefresh section, lines 1838-1975 via grep)
- Read portal/src/hooks/useYangData.ts (thin YangDataContext wrapper — not used by this pod)
- Wrote deliverable: org/tier2_senior/0.3.0_DE_TradingOperations/deliverables/pod_inventory.xml
- Marked task order status: complete

## Decisions Made

- **Decision: useYangData.ts not consumed by this pod** — DataRefresh reads manifest.json directly for
  freshness; PM/TS do not use Yang timestamp. Documented as low-criticality external dependency.

- **Decision: Intra-pod bridge is the highest-value architectural insight** — exportAndSubmit() in
  portfolio.ts is the sole connection between PortfolioManagement and TradeSubmission. Documented
  as HIGH criticality intra_pod_workflow with full endpoint chain.

- **Decision: Dual auto-save paths flagged as risk** — PM has legacy (trade-based via updateAutoSave)
  AND new optimization-state (via saveOptimizationAutoSave). Both run 60s intervals. Zustand store
  (usePortfolioStore) and React Query coexist, creating state split complexity.

- **Decision: DataRefresh is dev-gated (scoped API)** — not accessible to regular users. Noted in
  pod_health operational_note.

## Files Modified

- `org/tier2_senior/0.3.0_DE_TradingOperations/deliverables/pod_inventory.xml` — created
- `org/tier2_senior/0.3.0_DE_TradingOperations/task_orders/pod_inventory.md` — status: pending -> complete
- `org/tier2_senior/0.3.0_DE_TradingOperations/logs/2026-03-02/wave2_pod_inventory_activation.md` — this file

## Blockers

None. All 3 RD deliverables were present. All portal endpoint files were present and readable.
useYangData.ts was present but is not consumed by this pod.

---

## Current State

**Status:** COMPLETE
**Active branch:** CLOUD

pod_inventory.xml is written at the correct path and follows the schema specified in the task order.
All sections are populated from actual file reads (no inference). Task order marked complete.
The deliverable is ready for the Wave 3 DS agent (0.3.0_DS_TradingOperations) to consume as input
for the data_contract.xml task.

## Next Steps

> Ordered list for next session pickup.

1. **Receive Wave 3 task order** from 1.0.0_SA_CTO — DS data_contract.xml task order will reference
   this pod_inventory.xml as primary input. No action required from DE until task order arrives.

2. **Monitor open issues in PortfolioManagement** — 9 TODO stubs in calculation hooks are technical
   debt. If Andrew or CTO flags these for sprint work, issue task orders to 0.3.1_RD_PortfolioManagement
   with specific hooks to address (useOptimizationCalculations.ts lines 61-72, usePortfolioEditStore.ts:143).

3. **Track getSecurityDetails backend** — 0.3.0_DS_TradingOperations or a DT should confirm whether
   opal-pm-optimization-loader or a separate Lambda handles /api/private/portfolio-management/security/{ticker}.
   Currently unimplemented — breaks SecurityLookupModal add-security flow.

**Files to touch next:**
- None for DE until Wave 3 DS task order is issued

**Do NOT:**
- Modify any portal source files — this was a read-and-document activation task
- Issue Wave 3 DS task orders — that is the CTO's responsibility after Wave 2 is fully complete
  across all 4 DE pods


### 0.3.0_DE_TradingOperations -- Pending Task Orders

#### trade_engine_polish_TO1_threshold_highlighting.md

# Task Order: Trade Engine Visual Polish — TO-1: Threshold Highlighting

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-trade-polish-to1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-03-04</date>
    <status>pending</status>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/TRADE_ENGINE_VISUAL_POLISH.md</ref>
    <ref type="cto-handoff">org/tier1_exec/1.0.0_SA_CTO/deliverables/coo_handoff_trade_engine_visual_polish.md</ref>
  </references>

  <objective>
    Apply threshold-based conditional text coloring to Risk Decomposition, Alpha tab, and Sector tab
    columns. Covers PRD items 2, 3, 4, and 5. All changes are cosmetic — no data contract changes,
    no API changes. Route to 0.3.1_RD_PortfolioManagement or handle directly.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/PortfolioManagement/components/OptimizationSummaryHeader.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/tabs/AlphaTab.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/tabs/SectorTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      PRD Item 2 — Risk Decomposition Exposure columns (OptimizationSummaryHeader.tsx lines 359-367):
        Initial Exposure:   green if > 0.1,  red if &lt; -0.1, neutral otherwise
        Optimized Exposure: green if > 0.1,  red if &lt; -0.1, neutral otherwise
        Trade (Exposure):   green if > 0.05, red if &lt; -0.05, neutral otherwise
      Apply text color: hsl(var(--success)) for green, hsl(var(--danger)) for red,
      text-white/70 for neutral.
    </requirement>
    <requirement id="2">
      PRD Item 3 — Risk Decomposition Contribution columns (OptimizationSummaryHeader.tsx lines 373-381):
        Initial Contribution:   red if > 5, no green threshold (one-directional)
        Optimized Contribution: red if > 5, no green threshold (one-directional)
        Delta (Contribution):   green if &lt; -2 (reducing risk = good), red if > 2
      Same color tokens as above.
    </requirement>
    <requirement id="3">
      PRD Item 4 — Alpha tab (AlphaTab.tsx). Currently only Trade uses getTradeColor with +-0.01.
      Change ALL three columns (Initial Bet, Optimized Bet, Trade) to +-0.1 threshold:
        green if > 0.1, red if &lt; -0.1, neutral otherwise
      Apply in both the By Factor view (line 431, 434-438) and the By Group view (lines 278-282).
      Update or replace the getTradeColor function if it is hardcoded to +-0.01 for these columns.
    </requirement>
    <requirement id="4">
      PRD Item 5 — Sector tab (SectorTab.tsx). Currently Trade columns use +-0.01 threshold.
      New thresholds:
        Initial Bet:   green if > 2,   red if &lt; -2
        Optimized Bet: green if > 2,   red if &lt; -2
        Trade:         green if > 0.5, red if &lt; -0.5
    </requirement>
    <requirement id="5">
      bunx tsc -b must pass clean after all changes.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Risk Decomp table: Exposure and Contribution columns color per spec. Neutral band renders white/70.</criterion>
    <criterion id="2">Alpha tab By Factor + By Group: all three columns use +-0.1 thresholds. Old +-0.01 threshold replaced.</criterion>
    <criterion id="3">Sector tab: bet columns use +-2, trade column uses +-0.5.</criterion>
    <criterion id="4">No TypeScript errors. No regression on other PortfolioManagement tabs.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>No data contract changes. No new props through component boundaries if avoidable — these are purely local styling decisions.</constraint>
    <constraint>Reuse existing color token pattern (hsl(var(--success)), hsl(var(--danger))) that is already in use in the file. Do not introduce new CSS classes or Tailwind utilities that do not already exist in the portal.</constraint>
    <constraint>DT pushes portal DEV after DE reviews. DE must not signal DT push until DE has visually inspected the changes.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">portal DEV commit(s) with items 2-5 complete</deliverable>
    <deliverable type="document">Session log noting commit hashes and a brief confirmation that tsc passes</deliverable>
  </deliverables>
</task_order>
```

#### trade_engine_polish_TO2_gradient_color_scales.md

# Task Order: Trade Engine Visual Polish — TO-2: Gradient Color Scales

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-trade-polish-to2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-03-04</date>
    <status>pending</status>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/TRADE_ENGINE_VISUAL_POLISH.md</ref>
    <ref type="cto-handoff">org/tier1_exec/1.0.0_SA_CTO/deliverables/coo_handoff_trade_engine_visual_polish.md</ref>
  </references>

  <objective>
    Apply continuous gradient background color scales to Model tab (items 6) and Trade tab
    (items 8, 9). Adds initialBet gradient and a new derived finalBet column. Pattern is
    getGradientBackground already used by PortfolioGrid.tsx (lines 466-516).
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/PortfolioManagement/tabs/ModelTab.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/components/PortfolioGrid.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      PRD Item 6 — Model tab (ModelTab.tsx):
      Apply continuous gradient to Coefficient and Weight columns.
      Scale: white (low) to green (high) — same direction as positive values = good.
      Reuse getGradientBackground from PortfolioGrid.tsx. If not currently importable,
      extract it to a shared util (e.g., portal/src/pages/PortfolioManagement/utils/colorUtils.ts)
      and update both files to import from there.
    </requirement>
    <requirement id="2">
      PRD Item 8 — Trade tab (PortfolioGrid.tsx): apply gradient to totalRisk and specRisk columns.
      Scale: INVERTED — green (low risk) to red (high risk). Higher value = more red.
      getGradientBackground likely needs an invert flag or a separate inverted-gradient call.
      Read the existing implementation (lines 466-516) before implementing.
    </requirement>
    <requirement id="3">
      PRD Item 9a — Trade tab: apply same gradient as optimizedBet to initialBet column.
      optimizedBet already has the full red-yellow-green gradient via getGradientBackground.
      initialBet currently shows black text with no gradient. Apply the same treatment.
    </requirement>
    <requirement id="4">
      PRD Item 9b — Trade tab: add new finalBet column.
      finalBet = finalWeight - benchmarkWeight (derived client-side, same pattern as finalTrade).
      Place finalBet adjacent to optimizedBet and initialBet in column order.
      Apply the same gradient coloring as optimizedBet and initialBet.
      Use a valueGetter (not a data field) to compute finalBet from finalWeight and benchmarkWeight.
    </requirement>
    <requirement id="5">
      bunx tsc -b must pass clean after all changes.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Model tab Coefficient and Weight cells show white-to-green gradient backgrounds.</criterion>
    <criterion id="2">Trade tab totalRisk and specRisk cells show green-to-red (inverted) gradient.</criterion>
    <criterion id="3">initialBet has same gradient treatment as optimizedBet.</criterion>
    <criterion id="4">finalBet column present, positioned adjacent to initialBet/optimizedBet, gradient applied, value = finalWeight - benchmarkWeight.</criterion>
    <criterion id="5">No TypeScript errors. getGradientBackground is either still in place or cleanly refactored to a shared util used by both callers.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Read getGradientBackground (PortfolioGrid.tsx lines 466-516) before writing any gradient code. Do not duplicate the logic; import or extract it.</constraint>
    <constraint>finalBet is a derived field only — do not add it to any TypeScript interface or data contract. It is computed in the valueGetter at render time.</constraint>
    <constraint>No Lambda, Terraform, or API changes. This is pure frontend.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">portal DEV commit(s) with items 6, 8, 9 complete</deliverable>
    <deliverable type="document">Session log with commit hashes and tsc confirmation</deliverable>
  </deliverables>
</task_order>
```

#### trade_engine_polish_TO3_trade_tab_formatting.md

# Task Order: Trade Engine Visual Polish — TO-3: Trade Tab Formatting

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-trade-polish-to3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-03-04</date>
    <status>pending</status>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/TRADE_ENGINE_VISUAL_POLISH.md</ref>
    <ref type="cto-handoff">org/tier1_exec/1.0.0_SA_CTO/deliverables/coo_handoff_trade_engine_visual_polish.md</ref>
  </references>

  <objective>
    Two formatting changes to PortfolioGrid.tsx AG Grid column definitions:
    zero-weight cells display as dash, and size column cells get color-coded backgrounds.
    Covers PRD items 7 and 10.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/PortfolioManagement/components/PortfolioGrid.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      PRD Item 7 — Zero weight to dash:
      For columns initialWeight, optimizedWeight, finalWeight, benchmarkWeight:
      When value === 0, display "–" (en-dash, U+2013) instead of "0.00%".
      Implement via value formatter: if value === 0, return "–"; else return the existing
      percentage format. Do not change non-zero formatting.
    </requirement>
    <requirement id="2">
      PRD Item 10 — Size column coloring:
      Size column currently shows raw S/M/L/O value, bold, centered, no background color.
      Add cellStyle (or cellRenderer) that sets a muted translucent background per value:
        L (Large):   rgba(34, 197, 94, 0.15)   — green muted
        M (Mid):     rgba(234, 179, 8, 0.15)   — yellow muted
        O (Other):   rgba(239, 68, 68, 0.15)   — red muted
        S (Small):   rgba(239, 68, 68, 0.15)   — red muted (same as O)
      These are background colors, not text colors. Keep existing text styling intact.
    </requirement>
    <requirement id="3">
      bunx tsc -b must pass clean after all changes.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Securities with 0.00% weight show "–" in all four weight columns. Non-zero weights unchanged.</criterion>
    <criterion id="2">Size column cells: L = green tint, M = yellow tint, O = red tint, S = red tint. No change to text or bold formatting.</criterion>
    <criterion id="3">No TypeScript errors.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not change value formatters for non-zero weights — only the zero case is affected.</constraint>
    <constraint>Use rgba with 0.15 alpha or similar muted value appropriate for the dark theme. Do not use full-opacity colors that clash with selected row highlighting.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">portal DEV commit with items 7 and 10 complete</deliverable>
    <deliverable type="document">Session log with commit hash and tsc confirmation</deliverable>
  </deliverables>
</task_order>
```

#### trade_engine_polish_TO4_capitalize_canonical_order.md

# Task Order: Trade Engine Visual Polish — TO-4: Capitalize + Canonical Group Ordering

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-trade-polish-to4</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-03-04</date>
    <status>pending</status>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/TRADE_ENGINE_VISUAL_POLISH.md</ref>
    <ref type="cto-handoff">org/tier1_exec/1.0.0_SA_CTO/deliverables/coo_handoff_trade_engine_visual_polish.md</ref>
  </references>

  <objective>
    Create shared CANONICAL_GROUP_ORDER constant, apply capitalize CSS to all group name cells,
    and replace alphabetical group sort with canonical order in AlphaTab, ModelTab, and
    SecurityDetailModal. Covers PRD items 1, 11, and 13.
  </objective>

  <scope>
    <files>
      <file action="create">portal/src/pages/PortfolioManagement/utils/factorOrder.ts</file>
      <file action="modify">portal/src/pages/PortfolioManagement/tabs/AlphaTab.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/tabs/ModelTab.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/components/SecurityDetailModal.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Create portal/src/pages/PortfolioManagement/utils/factorOrder.ts with:

        export const CANONICAL_GROUP_ORDER = [
          'size',
          'efficiency',
          'growth',
          'management',
          'profitability',
          'quality',
          'value',
          'analyst',
          'governance',
          'crowding',
          'insider',
          'short',
          'beta',
          'momentum',
          'technical',
        ] as const

        export type CanonicalGroup = typeof CANONICAL_GROUP_ORDER[number]

        export function canonicalGroupIndex(group: string): number {
          const idx = (CANONICAL_GROUP_ORDER as readonly string[]).indexOf(group.toLowerCase())
          return idx === -1 ? CANONICAL_GROUP_ORDER.length : idx
        }

      This order matches the signal DataFrame row order in Yang's alpha PKL. Source of truth
      is portal/src/pages/PortfolioManagement/utils/factorDescriptions.ts (comment order).
      Implementation pattern mirrors ECONOMY_ORDER in TradeTab.tsx (line 249).
    </requirement>
    <requirement id="2">
      PRD Item 13 — AlphaTab.tsx By Group sort (line 74):
      Replace the .localeCompare sort with canonicalGroupIndex sort:
        - Before: a.group.localeCompare(b.group)
        - After:  canonicalGroupIndex(a.group) - canonicalGroupIndex(b.group)
      Import canonicalGroupIndex from utils/factorOrder.ts.
    </requirement>
    <requirement id="3">
      PRD Item 1 — AlphaTab.tsx By Factor view group cells (line 421):
      Add CSS class "capitalize" (or style text-transform: capitalize) to group name cells.
      The By Group view already has capitalize at line 273 — leave that intact.
    </requirement>
    <requirement id="4">
      PRD Item 13 — ModelTab.tsx By Group sort:
      Apply the same canonical group ordering via canonicalGroupIndex to ModelTab's By Group
      aggregated view (where groups are currently sorted alphabetically or by Lambda response order).
      Read ModelTab.tsx before implementing to confirm where the sort happens.
    </requirement>
    <requirement id="5">
      PRD Item 1 — ModelTab.tsx:
      Apply capitalize CSS to group column cells (wherever group names appear in the table).
    </requirement>
    <requirement id="6">
      PRD Item 11 — SecurityDetailModal.tsx:
      1. Apply capitalize CSS class to group name cells in the factor list.
      2. Sort the factor list by canonical group order (canonicalGroupIndex on the group field).
         Within each group, preserve the original factor order from the data array.
    </requirement>
    <requirement id="7">
      bunx tsc -b must pass clean after all changes.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">factorOrder.ts exists with the 15-group CANONICAL_GROUP_ORDER array, exactly as specified.</criterion>
    <criterion id="2">AlphaTab By Group view: groups appear in canonical order (size first, technical last), not alphabetical.</criterion>
    <criterion id="3">AlphaTab By Factor view: group name cells show capitalized text (Size, Efficiency, etc.).</criterion>
    <criterion id="4">ModelTab By Group view: groups in canonical order; group cells capitalized.</criterion>
    <criterion id="5">SecurityDetailModal: factor list sorted by canonical group order; group cells capitalized.</criterion>
    <criterion id="6">No TypeScript errors. No regression on the By Factor views (which are already correct).</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>CANONICAL_GROUP_ORDER must live in factorOrder.ts — do not inline it in each component file. All three components import from the shared util.</constraint>
    <constraint>Groups not in CANONICAL_GROUP_ORDER sort to the end (canonicalGroupIndex returns CANONICAL_GROUP_ORDER.length for unknown groups). This is the fallback pattern — do not throw on unknown groups.</constraint>
    <constraint>Do not modify factorDescriptions.ts. It is the source of truth (read-only reference).</constraint>
    <constraint>Capitalize is a CSS presentation concern only — do not transform the data string. The underlying group value remains lowercase in the data model.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">portal DEV commit(s) with factorOrder.ts + items 1, 11, 13 complete</deliverable>
    <deliverable type="document">Session log with commit hash and tsc confirmation</deliverable>
  </deliverables>
</task_order>
```

#### trade_engine_polish_TO5_reset_zero_button.md

# Task Order: Trade Engine Visual Polish — TO-5: Reset Zero Button

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-04-trade-polish-to5</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-03-04</date>
    <status>pending</status>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/TRADE_ENGINE_VISUAL_POLISH.md</ref>
    <ref type="cto-handoff">org/tier1_exec/1.0.0_SA_CTO/deliverables/coo_handoff_trade_engine_visual_polish.md</ref>
  </references>

  <objective>
    Add "Reset Zero" button to the Trade tab button group. When clicked, sets finalTrade = 0 for
    ALL securities (hold everything as-is; propose no trades). Covers PRD item 12.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/PortfolioManagement/tabs/TradeTab.tsx</file>
      <file action="modify">portal/src/pages/PortfolioManagement/PortfolioManagement.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Button placement: in TradeTab.tsx button group (line ~368), insert "Reset Zero" between
      "Reset All" and "Export". The button group currently has:
        Reset Selected | Reset All | Export | Submit
      After change:
        Reset Selected | Reset All | Reset Zero | Export | Submit
    </requirement>
    <requirement id="2">
      Button behavior — "Reset Zero":
      Sets finalTrade = 0 for ALL securities.
      Implementation: finalWeight = initialWeight for every security.
      This is the "hold everything" state — tell the optimizer to make no changes.
      This is DISTINCT from "Reset All" which sets finalWeight = optimizedWeight (optimizer's suggestion).
    </requirement>
    <requirement id="3">
      TradeTab.tsx: add onResetZero prop (callback, no arguments). Wire the button to call it.
      Match the pattern of the existing onResetAll prop — read TradeTab.tsx before implementing
      to confirm the exact prop signature pattern.
    </requirement>
    <requirement id="4">
      PortfolioManagement.tsx: implement handleResetZero. It should iterate over all securities
      in state and set each security's finalWeight to its initialWeight (and finalTrade to 0).
      Read PortfolioManagement.tsx and usePortfolioEditStore to understand the correct state
      mutation path before implementing. Do not assume — cite the state update mechanism.
    </requirement>
    <requirement id="5">
      bunx tsc -b must pass clean.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Reset Zero button appears in the correct position between Reset All and Export.</criterion>
    <criterion id="2">Clicking Reset Zero sets finalTrade = 0 for all securities and finalWeight = initialWeight for all securities.</criterion>
    <criterion id="3">Reset All still works correctly (finalWeight = optimizedWeight) — no regression.</criterion>
    <criterion id="4">No TypeScript errors.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Read TradeTab.tsx (around line 368) and PortfolioManagement.tsx BEFORE implementing. The existing button callbacks are the implementation pattern to follow.</constraint>
    <constraint>Do not use finalWeight = 0 — that would set holdings to zero. The correct operation is finalWeight = initialWeight (hold current positions).</constraint>
    <constraint>No backend changes, no API calls, no Lambda changes. Pure frontend state operation.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">portal DEV commit with item 12 complete</deliverable>
    <deliverable type="document">Session log with commit hash and tsc confirmation</deliverable>
  </deliverables>
</task_order>
```


### 0.3.0_DE_TradingOperations -- Recent Commits

# Recent commits by 0.3.0_DE_TradingOperations

17ec8a99 org(1.0.0_SA_CTO): SSCN_PORTAL scaffolding + PRDs (Security Scanner, Trade Engine Visual Polish, Yang V2 Feedback)
d9686db0 org(2.0.0_SA_COO): ADVI-006 run + trade engine polish task orders

