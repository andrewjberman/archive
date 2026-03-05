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
