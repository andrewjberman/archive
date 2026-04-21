# ADVI_INFLEC W5.0.1 — AdvisorIntelligence Component Inventory
**Author:** 0.4.0_DE_ClientPlatform  
**Date:** 2026-04-21  
**TO:** ADVI_INFLEC.W5.0.1.de-audit-advisor-intelligence-components  
**Status:** COMPLETE — pending W5.0.3 CTO review of AMBIGUOUS rows

## Count Summary

**40 components total: 30 SHARED | 5 49F-SPECIFIC | 5 AMBIGUOUS**

---

## Inventory Table

| File | Component / Export | Category | Evidence (file:line or description) | Proposed Target Folder |
|------|--------------------|----------|--------------------------------------|------------------------|
| `AdvisorIntelligence.tsx` | `AdvisorIntelligence` (page root) | 49F-SPECIFIC | L34: `AVAILABLE_FIRMS = [{id: 'bd', name: '49 Financial'}]` hardcoded firm list; L159: `internal ? 'bd' : (claims?.firmId ?? 'bd')` — 'bd' default fallback when no JWT firmId; L287-293: "Black Diamond Connected" source panel hard-wired into page layout | `_partners/49financial/` (firm picker + firmId default + BD source panel must move to partner config) |
| `AdvisorBookAccountDetail.tsx` | `AdvisorBookAccountDetail` | SHARED | No partner-specific references. Pure renderer — receives account data via props, renders AUA chart + account composition. | `_shared/` |
| `AdvisorBookAccountModal.tsx` | `AdvisorBookAccountModal` | SHARED | No partner-specific references. Modal wrapper around AdvisorBookAccountDetail with overlay backdrop. | `_shared/` |
| `AdvisorBookClientDetail.tsx` | `AdvisorBookClientDetail` | SHARED | No partner-specific references. Pure renderer — receives L3 client detail via props (PlatinumClientSummary adapter lives in parent). | `_shared/` |
| `AdvisorBookView.tsx` | `AdvisorBookView` | AMBIGUOUS | L483-492: inline `ROLE_ORDER` and `ROLE_LABELS` hardcoded as `['architect', 'consultant', 'implementor', 'additional_advisor', 'local_ops']` (NOT sourced from `@/lib/chartColors` ADVISOR_ROLE_LABELS — independent hardcode). Also renders "Small Accounts by Role" panel using these role keys. **CTO Q:** Are these five role names (architect / consultant / implementor / additional_advisor / local_ops) unique to 49F's BD data model, or will Inflection expose the same role taxonomy? If different, ROLE_ORDER + ROLE_LABELS move to `_partners/49financial/` and the Small Accounts panel becomes a partner injection point. | AMBIGUOUS — CTO review |
| `AdvisorPublicProfile.tsx` | `AdvisorPublicProfile`, `NonAdminProfileTab` | AMBIGUOUS | L130: `ROLE_ORDER_INDEX` hardcoded with same 5 role keys (architect/consultant/implementor/additional_advisor/local_ops); L152: fallback to `ADVISOR_ROLE_LABELS` from `@/lib/chartColors`. Also owns the Book vs Profile tab toggle logic — may encode 49F's specific advisor-role hierarchy (architect sees "Book" view; non-architects see "Profile"). **CTO Q:** Will Inflection have the same "architect = sees full book" access model, or does the Book/Profile split need to be a partner-configurable policy? | AMBIGUOUS — CTO review |
| `ClientDetail/ClientDetailPage.tsx` | `ClientDetailPage` | 49F-SPECIFIC | L31: `const firmId = searchParams.get('firmId') \|\| 'bd'` — 'bd' fallback when URL param missing. | `_partners/49financial/` (firmId default) or extract default to partner-config injection |
| `ClientDetail/index.ts` | re-export | SHARED | Re-export only, no logic. | `_shared/` |
| `ClientDetail/panels/AISummaryPanel.tsx` | `AISummaryPanel` | SHARED | No partner-specific references. Renders exec-summary bullets from generic `AdvisorExecSummary` type. | `_shared/` |
| `ClientDetail/panels/ConcentrationPanel.tsx` | `ConcentrationPanel` | SHARED | No partner-specific references. Generic top-holdings concentration chart. | `_shared/` |
| `ClientDetail/panels/index.ts` | re-export | SHARED | Re-export only. | `_shared/` |
| `ClientDetail/panels/MixTimeseriesPanel.tsx` | `MixTimeseriesPanel` | SHARED | No partner-specific references. Generic asset-class mix timeseries (equity/fixed_income/alternatives/cash). | `_shared/` |
| `ClientDetail/panels/PortfolioBalancePanel.tsx` | `PortfolioBalancePanel` | SHARED | No partner-specific references. AUA balance chart at client level. | `_shared/` |
| `ClientDetail/panels/TimeSeriesPanel.tsx` | `TimeSeriesPanel` | SHARED | No partner-specific references. Generic AUA + NNA timeseries with mode/interval toggles. | `_shared/` |
| `ClientDetail/types.ts` | local types | SHARED | Local ClientDetail prop types. No partner-specific fields. | `_shared/` |
| `components/AUACompositionChart.tsx` | `AUACompositionChart` | SHARED | No partner-specific references. Generic AUA composition donut. | `_shared/` |
| `components/AUATrendChart.tsx` | `AUATrendChart` | 49F-SPECIFIC | L319: footer copy `"Source: SS&C Black Diamond Wealth Solutions. ..."` hardcoded — BD-custodian attribution. | `_partners/49financial/` (source footer) or partner-configurable `sourceAttribution` prop |
| `components/DimensionSelector.tsx` | `DimensionSelector` | SHARED | No partner-specific references. Generic dimension (GEO/ADV/OFC) selector. | `_shared/` |
| `components/HeaderMetrics.tsx` | `HeaderMetrics` | SHARED | No partner-specific references. Generic metrics card row. | `_shared/` |
| `components/MetricSelector.tsx` | `MetricSelector` | SHARED | No partner-specific references. Generic metric toggle (AUA/NNA/GEO/ADV). | `_shared/` |
| `components/PartnerAnalytics.tsx` | `PartnerAnalytics` | 49F-SPECIFIC | L754: `"Source: SS&C Black Diamond Wealth Solutions."` in PanelFooter; L1978: same footer in second render path. Two independent occurrences — not a conditional. | `_partners/49financial/` (source footer) or partner-configurable `sourceAttribution` prop injected by partner router |
| `index.ts` | re-export | SHARED | Re-export only, no logic. | `_shared/` |
| `lib/clientName.ts` | `formatClientName` | SHARED | Pure string utility — flips "Last, First" to "First Last". No partner-specific logic. | `_shared/lib/` |
| `lib/composition.ts` | `normalizeMixTo4Class`, `platinumToComposition` | SHARED | Pure composition helpers — no partner-specific logic. `platinumToComposition` adapts platinum mix/concentration payload to shared BooksCompositionResponse shape. | `_shared/lib/` |
| `panels/CanonicalBookView.tsx` | `CanonicalBookView` | SHARED | No partner-specific references. Generic book overview layout (composition + tax + client list slots). | `_shared/panels/` |
| `panels/ClientListPanel.tsx` | `ClientListPanel` | SHARED | No partner-specific references. Generic client list with Book Growth tile and NNA column. | `_shared/panels/` |
| `panels/ClientsTable.tsx` | `ClientsTable` | SHARED | No partner-specific references. Generic sortable client table. | `_shared/panels/` |
| `panels/ConsolidatedOverviewPanel.tsx` | `ConsolidatedOverviewPanel` | SHARED | No partner-specific references. Generic consolidated firm overview panel. | `_shared/panels/` |
| `panels/TaxCostBasisPanel.tsx` | `TaxCostBasisPanel` | SHARED | No partner-specific references. Generic tax/cost-basis panel with tax-status donut and cost-basis-by-year chart. | `_shared/panels/` |
| `panels/types.ts` | panel prop types | SHARED | Generic panel prop interfaces (`CanonicalTax`, etc.). No partner-specific fields. | `_shared/panels/` |
| `panels/useSyncedHeight.tsx` | `useSyncedHeight` | SHARED | Generic ResizeObserver hook for panel height synchronization. | `_shared/panels/` |
| `SmallAccountsByRoleModal.tsx` | `SmallAccountsByRoleModal` | AMBIGUOUS | L47: display text `"accounts under $40,000"` — the $40k threshold (`SMALL_ACCOUNT_AUA_THRESHOLD_USD`) is a business rule. **CTO Q:** Is the $40k small-account threshold 49F-specific (driven by 49F's fee structure/BD data model), or will Inflection use the same threshold? If different, either the threshold becomes a partner-configurable prop or this modal moves to `_partners/49financial/`. | AMBIGUOUS — CTO review |
| `tabs/AdvisorsTab.tsx` | `AdvisorsTab` | AMBIGUOUS | L87-92: `ROLE_LABELS` sourced from `ADVISOR_ROLE_LABELS` in `@/lib/chartColors` (which hardcodes architect/implementor/consultant/local_ops/additional_advisor). AdvisorsTab also contains role-filter checkboxes keyed on these same role names. **CTO Q:** Same role-vocabulary question as AdvisorBookView row. If Inflection uses the same 5-role schema, AdvisorsTab is SHARED. If not, the role-filter UI and color/label mapping become 49F-specific injection points. | AMBIGUOUS — CTO review |
| `tabs/AssetIntelligenceTab.tsx` | `AssetIntelligenceTab` | SHARED | Legacy tab — not wired in v5 (confirmed per prompt.md "AssetIntelligenceTab.tsx is legacy — present but not wired in v5"). No partner-specific references. | `_shared/` (legacy — may be archived rather than migrated) |
| `tabs/ClientsTab.tsx` | `BooksTab` | SHARED | No partner-specific references. Receives `firmId`/`firmOverride` as props; no hardcoded 'bd' fallbacks inside. | `_shared/` |
| `tabs/DistributionTab.tsx` | `DistributionTab` | 49F-SPECIFIC | L953: `"Source: SS&C Black Diamond Wealth Solutions."` footer; L3170: `"State-level NNA from Black Diamond."` tooltip copy; L3172-3173: `"City/State-level AUA from Black Diamond account data."` tooltip copy — BD-custodian copy in 3 places. | `_partners/49financial/` (source attribution) or partner-configurable `sourceLabel` prop |
| `tabs/FeeEfficiencyPanel.tsx` | `FeeEfficiencyPanel` | SHARED | No partner-specific references. Note: L932 tooltip mentions "may differ slightly from tagged AUA in the leaderboard for multi-role advisors" — this is a methodology note about fee calculation, NOT a BD/49F reference; preserve per CHART-ALIGN-FE scope rules. | `_shared/` |
| `tabs/FeeRoleBreakdownPanel.tsx` | `FeeRoleBreakdownPanel` | SHARED | No partner-specific references. Generic fee breakdown by role (renders whatever role keys the data supplies). | `_shared/` |
| `tabs/FeeSummaryPanel.tsx` | `FeeSummaryPanel` | SHARED | No partner-specific references. Generic fee summary panel (weighted avg bps + annual implied revenue). | `_shared/` |
| `types.ts` | shared type definitions | AMBIGUOUS | L183: `architect: string` field in `TaxDeferredCandidate` (role name hardcoded as a field name); L930: `AdvisorRole = 'architect' \| 'implementor' \| 'consultant' \| 'local_ops' \| 'additional_advisor'` — role union hardcoded. **CTO Q:** Will Inflection expose the same advisor-role taxonomy in its platinum/firm/leaderboard.json? If yes, `AdvisorRole` union stays SHARED. If Inflection has different roles, this type becomes 49F-specific and a partner-neutral union (or generic `string`) is needed for the shared layer. | AMBIGUOUS — CTO review |

---

## Evidence Summary for 49F-SPECIFIC Rows

| File | Line(s) | Exact Evidence |
|------|---------|----------------|
| `AdvisorIntelligence.tsx` | L34 | `const AVAILABLE_FIRMS = [{ id: 'bd', name: '49 Financial' }]` |
| `AdvisorIntelligence.tsx` | L159 | `internal ? 'bd' : (claims?.firmId ?? 'bd')` |
| `AdvisorIntelligence.tsx` | L287 | JSX: `<span ...>Black Diamond Connected:</span> Partner AUA and NNA data from Black Diamond Wealth Platform.` |
| `ClientDetail/ClientDetailPage.tsx` | L31 | `const firmId = searchParams.get('firmId') \|\| 'bd'` |
| `components/AUATrendChart.tsx` | L319 | `content={"Source: SS\&C Black Diamond Wealth Solutions. ..."}` |
| `components/PartnerAnalytics.tsx` | L754 | `<PanelFooter content="Source: SS\&C Black Diamond Wealth Solutions." .../>` |
| `components/PartnerAnalytics.tsx` | L1978 | same footer, second render path |
| `tabs/DistributionTab.tsx` | L953 | `<PanelFooter content="Source: SS\&C Black Diamond Wealth Solutions." .../>` |
| `tabs/DistributionTab.tsx` | L3170 | `"State-level NNA from Black Diamond."` (tooltip copy) |
| `tabs/DistributionTab.tsx` | L3172-3173 | `"City/State-level AUA from Black Diamond account data."` (tooltip copy) |

---

## CTO Questions for W5.0.3 Review

| Row | File | Question |
|-----|------|----------|
| Q1 | `AdvisorBookView.tsx`, `AdvisorsTab.tsx`, `AdvisorPublicProfile.tsx`, `types.ts` | Are advisor roles (architect / consultant / implementor / additional_advisor / local_ops) 49F-specific vocabulary from BD's data model, or will Inflection expose the same 5-role taxonomy in its platinum output? If Inflection uses different role names, all role-keyed logic (ROLE_LABELS, ROLE_ORDER, ROLE_COLORS, AdvisorRole union) must split: 49F-specific constants move to `_partners/49financial/`, shared layer uses generic `string` keys. |
| Q2 | `SmallAccountsByRoleModal.tsx` | Is the $40k small-account threshold (`SMALL_ACCOUNT_AUA_THRESHOLD_USD`) a 49F-specific business rule (driven by 49F's fee schedule), or will Inflection use the same threshold? If different, the threshold becomes a partner-configurable prop injected by the partner router. |
| Q3 | `AdvisorPublicProfile.tsx` | Does the Book vs Profile tab split (architect = Book access; non-architect = Profile-only) encode a 49F-specific access model, or will Inflection adopt the same role-gated access pattern? |

---

## Methodology Notes

**Grep strategy:** Two passes. Pass 1 (broad): `diverge|divergence|attribution|leaderboard.*chart|chart.*leaderboard|time.window|tagging.window|snapshot.*nna|nna.*snapshot|may differ|caveat|methodology`. Pass 2 (targeted): `49financial|'bd'|"bd"|schwab|Schwab|BD\b|Black Diamond|custodian`.

**Pass 1 result:** Zero chart-leaderboard caveat text found (CHART-ALIGN-FE context).

**Pass 2 result:** 10 hits across 5 files — see Evidence Summary above. Zero hits in panels/, lib/, ClientDetail/panels/, or any pure renderer.

**Role-label sourcing:** `AdvisorsTab.tsx` and `AdvisorPublicProfile.tsx` source role labels from `ADVISOR_ROLE_LABELS` in `@/lib/chartColors.ts` (L525-528) — the 49F-ism is in the shared lib, not in AdvisorIntelligence/ directly. `AdvisorBookView.tsx` has an INDEPENDENT inline `ROLE_LABELS` hardcode (not from chartColors) — direct 49F-ism inside the file.

**firmId prop vs hardcode:** Components that ACCEPT `firmId` as a prop are classified SHARED. Only components that HARDCODE a firm identifier or default to 'bd' are 49F-SPECIFIC.

**comp-transform Phase 3 output:** `comp-transform fields AdvisorIntelligence` reports 3 rendered fields at the page-root level (`analyticsData` root, `.generated_at`, `employeeData` root) — expected, since the page root is an orchestrator that passes firmId/data to child components rather than rendering fields directly.

---

## CTO SIGN-OFF — W5.0.3 Review (2026-04-21)

**Signed off by:** 1.0.0_SA_CTO via MCP 20260421T210739Z
**Resolutions per 1.0.0_SA_CTO — parameterize, don't fork:**

### Q1/Q4 — Role vocabulary: VERDICT: 49F-specific VALUES, shared SHAPE

- `_shared/types.ts`: add `type AdvisorRoleKey = string` + `interface AdvisorRoleMeta { key: string; label: string; color: string; order: number }`. Remove `AdvisorRole` union; rename `TaxDeferredCandidate.architect` to `primaryAdvisor: string | null`.
- `_partners/49financial/roles.ts`: `type FortyNineFinancialRole = 'architect' | 'implementor' | 'consultant' | 'local_ops' | 'additional_advisor'` + `FORTY_NINE_FINANCIAL_ROLES: Record<FortyNineFinancialRole, AdvisorRoleMeta>` (current ROLE_LABELS/ORDER/COLORS).
- `_partners/inflection/roles.ts`: `type InflectionRole = 'individual' | 'firm' | 'routing'` + `INFLECTION_ROLES: Record<InflectionRole, AdvisorRoleMeta>` (`individual` = advisor-name-keyed, `firm` = "Inflection Wealth Management", `routing` = excluded from leaderboard).
- `AdvisorBookView`, `AdvisorsTab`, `AdvisorPublicProfile` take `roleMeta: Record<string, AdvisorRoleMeta>` prop injected by partner router via `useFirmConfig()`. Drop inline ROLE_ORDER/ROLE_LABELS.
- `lib/chartColors.ts` `ADVISOR_ROLE_LABELS` — MOVE to `_partners/49financial/roles.ts`. chartColors.ts stays partner-agnostic.
- `types.ts` L183 `TaxDeferredCandidate.architect: string` — RENAME to `primaryAdvisor: string | null` (role-agnostic).

Reclassification: `AdvisorBookView.tsx`, `AdvisorsTab.tsx`, `AdvisorPublicProfile.tsx`, `types.ts` move from AMBIGUOUS to SHARED (parameterized).

### Q2 — $40k threshold: VERDICT: 49F fee-schedule-specific, component stays SHARED

- `SmallAccountsByRoleModal` takes `threshold: number` + `roleMeta: Record<string, AdvisorRoleMeta>` props.
- Inflection: partner router does NOT render the Small Accounts surface (soft-hide; `threshold: null` signal).
- 49F: partner router injects `threshold: 40_000` from `_partners/49financial/constants.ts`.

Reclassification: `SmallAccountsByRoleModal.tsx` moves from AMBIGUOUS to SHARED (parameterized).

### Q3 — Book/Profile access model: VERDICT: 49F pyramid-gated, parameterize via access-policy prop

- `AdvisorPublicProfile` takes `accessPolicy: 'gated-by-role' | 'book-only' | 'profile-only'` prop.
- 49F: `'gated-by-role'` + current user role passed by partner router.
- Inflection: `'book-only'` (every Rep sees own book; no pyramid gating).

### Additional — Source attribution strings: parameterize (CTO suggestion accepted)

- `AUATrendChart`, `PartnerAnalytics`, `DistributionTab` take `sourceAttribution: string` prop.
- 49F constant: `"Source: SS&C Black Diamond Wealth Solutions."`
- Inflection constant: `"Source: Orion Portfolio Solutions."`
- `DistributionTab` additionally takes `tooltipAttribution: { stateNna: string; cityAua: string }` prop.

### Remaining true-fork components (after all parameterizations)

- `AdvisorIntelligence.tsx` → `_partners/49financial/index.tsx` (AVAILABLE_FIRMS + 'bd' default + BD layout panel). NOT extractable as props — this IS the partner page assembly.
- `ClientDetail/ClientDetailPage.tsx` → make `firmId` a REQUIRED prop (no fallback). Partner page-root passes the firmId. Cleaner than prop-injected default.

### NET RESULT after W5.0.3 resolutions

**40 components total: 35 SHARED (parameterized) | 2 49F-SPECIFIC (true forks) | 3 config files | 0 AMBIGUOUS**

(Previously: 30 SHARED / 5 49F-SPECIFIC / 5 AMBIGUOUS — 5 AMBIGUOUS all resolved to SHARED-with-params; 3 of the original 49F-SPECIFIC resolved to SHARED-with-params)

### W5.0.4 Prerequisites (all gates cleared)

- CTO sign-off: GIVEN 2026-04-21
- W5.0.1 complete: YES (051f7ab3)
- W5.0.2 complete: YES (f5900e5a)
- W5.0.4 execution: pending COO GO
