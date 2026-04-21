# ADVI_INFLEC W5.0.2 — AdvisorIntelligence Folder Structure Proposal
**Author:** 0.4.0_DE_ClientPlatform
**Date:** 2026-04-21
**TO:** ADVI_INFLEC.W5.0.2.de-propose-folder-structure
**Input:** W5.0.1 inventory (40 components: 30 SHARED / 5 49F-SPECIFIC / 5 AMBIGUOUS)
**Status:** PENDING W5.0.3 CTO review of AMBIGUOUS rows

---

## Proposed Directory Layout

```
portal/src/pages/AdvisorIntelligence/
  index.tsx                           # NEW — firmId router (replaces AdvisorIntelligence.tsx at root)
  index.ts                            # existing re-export (unchanged)
  _shared/
    types.ts                          # AMBIGUOUS — see CTO Q1; placed here pending review
    AdvisorBookAccountDetail.tsx
    AdvisorBookAccountModal.tsx
    AdvisorBookClientDetail.tsx
    AdvisorBookView.tsx               # AMBIGUOUS — see CTO Q1
    AdvisorPublicProfile.tsx          # AMBIGUOUS — see CTO Q3
    SmallAccountsByRoleModal.tsx      # AMBIGUOUS — see CTO Q2; proposed SHARED with thresholdUsd prop
    ClientDetail/
      index.ts
      types.ts
      ClientDetailPage.tsx            # 49F-SPECIFIC origin; refactored — see §3
      panels/
        AISummaryPanel.tsx
        ConcentrationPanel.tsx
        index.ts
        MixTimeseriesPanel.tsx
        PortfolioBalancePanel.tsx
        TimeSeriesPanel.tsx
    components/
      AUACompositionChart.tsx
      AUATrendChart.tsx               # 49F-SPECIFIC origin; refactored — see §3
      DimensionSelector.tsx
      HeaderMetrics.tsx
      MetricSelector.tsx
      PartnerAnalytics.tsx            # 49F-SPECIFIC origin; refactored — see §3
    lib/
      clientName.ts
      composition.ts
    panels/
      CanonicalBookView.tsx
      ClientListPanel.tsx
      ClientsTable.tsx
      ConsolidatedOverviewPanel.tsx
      TaxCostBasisPanel.tsx
      types.ts
      useSyncedHeight.tsx
    tabs/
      AdvisorsTab.tsx                 # AMBIGUOUS — see CTO Q1; placed here pending review
      AssetIntelligenceTab.tsx
      ClientsTab.tsx
      DistributionTab.tsx             # 49F-SPECIFIC origin; refactored — see §3
      FeeEfficiencyPanel.tsx
      FeeRoleBreakdownPanel.tsx
      FeeSummaryPanel.tsx
  _partners/
    49financial/
      index.tsx                       # NEW — 49F page assembly (BD source panel, firmId default)
      constants.ts                    # NEW — BD_SOURCE_ATTRIBUTION, AVAILABLE_FIRMS, firmId default
    inflection/
      index.tsx                       # NEW STUB — empty page assembly (W5.1 populates)
      constants.ts                    # NEW STUB — empty constants (W5.1 populates)
```

---

## Component File-Move Plan (40 rows)

| Current Path | Proposed Target Path | Category | Migration Action |
|---|---|---|---|
| `AdvisorIntelligence.tsx` | `_partners/49financial/index.tsx` | 49F-SPECIFIC | Rename + extract BD panel and firmId default to `_partners/49financial/constants.ts`; new `index.tsx` router replaces page root |
| `AdvisorBookAccountDetail.tsx` | `_shared/AdvisorBookAccountDetail.tsx` | SHARED | Move, update import paths |
| `AdvisorBookAccountModal.tsx` | `_shared/AdvisorBookAccountModal.tsx` | SHARED | Move, update import paths |
| `AdvisorBookClientDetail.tsx` | `_shared/AdvisorBookClientDetail.tsx` | SHARED | Move, update import paths |
| `AdvisorBookView.tsx` | `_shared/AdvisorBookView.tsx` | AMBIGUOUS | Move provisionally; ROLE_ORDER/ROLE_LABELS inline hardcode extraction to `_partners/49financial/constants.ts` IF CTO Q1 resolves as 49F-specific |
| `AdvisorPublicProfile.tsx` | `_shared/AdvisorPublicProfile.tsx` | AMBIGUOUS | Move provisionally; Book/Profile access model may need `bookAccessPolicy` prop injection IF CTO Q3 resolves as 49F-specific |
| `ClientDetail/ClientDetailPage.tsx` | `_shared/ClientDetail/ClientDetailPage.tsx` | 49F-SPECIFIC | Move; extract firmId URL-param default (`'bd'`) to `defaultFirmId` prop; partner page-root injects `defaultFirmId="bd"` |
| `ClientDetail/index.ts` | `_shared/ClientDetail/index.ts` | SHARED | Move, update import paths |
| `ClientDetail/panels/AISummaryPanel.tsx` | `_shared/ClientDetail/panels/AISummaryPanel.tsx` | SHARED | Move, update import paths |
| `ClientDetail/panels/ConcentrationPanel.tsx` | `_shared/ClientDetail/panels/ConcentrationPanel.tsx` | SHARED | Move, update import paths |
| `ClientDetail/panels/index.ts` | `_shared/ClientDetail/panels/index.ts` | SHARED | Move, update import paths |
| `ClientDetail/panels/MixTimeseriesPanel.tsx` | `_shared/ClientDetail/panels/MixTimeseriesPanel.tsx` | SHARED | Move, update import paths |
| `ClientDetail/panels/PortfolioBalancePanel.tsx` | `_shared/ClientDetail/panels/PortfolioBalancePanel.tsx` | SHARED | Move, update import paths |
| `ClientDetail/panels/TimeSeriesPanel.tsx` | `_shared/ClientDetail/panels/TimeSeriesPanel.tsx` | SHARED | Move, update import paths |
| `ClientDetail/types.ts` | `_shared/ClientDetail/types.ts` | SHARED | Move, update import paths |
| `components/AUACompositionChart.tsx` | `_shared/components/AUACompositionChart.tsx` | SHARED | Move, update import paths |
| `components/AUATrendChart.tsx` | `_shared/components/AUATrendChart.tsx` | 49F-SPECIFIC | Move; replace hardcoded `"Source: SS&C Black Diamond Wealth Solutions."` string with `sourceAttribution?: string` prop; partner page-root supplies the BD string from `_partners/49financial/constants.ts` |
| `components/DimensionSelector.tsx` | `_shared/components/DimensionSelector.tsx` | SHARED | Move, update import paths |
| `components/HeaderMetrics.tsx` | `_shared/components/HeaderMetrics.tsx` | SHARED | Move, update import paths |
| `components/MetricSelector.tsx` | `_shared/components/MetricSelector.tsx` | SHARED | Move, update import paths |
| `components/PartnerAnalytics.tsx` | `_shared/components/PartnerAnalytics.tsx` | 49F-SPECIFIC | Move; replace both `PanelFooter content="Source: SS&C Black Diamond Wealth Solutions."` instances with `sourceAttribution?: string` prop; partner page-root supplies value from constants |
| `index.ts` | `index.ts` | SHARED | Keep at root; no path change; update re-export target if AdvisorIntelligence.tsx is renamed |
| `lib/clientName.ts` | `_shared/lib/clientName.ts` | SHARED | Move, update import paths |
| `lib/composition.ts` | `_shared/lib/composition.ts` | SHARED | Move, update import paths |
| `panels/CanonicalBookView.tsx` | `_shared/panels/CanonicalBookView.tsx` | SHARED | Move, update import paths |
| `panels/ClientListPanel.tsx` | `_shared/panels/ClientListPanel.tsx` | SHARED | Move, update import paths |
| `panels/ClientsTable.tsx` | `_shared/panels/ClientsTable.tsx` | SHARED | Move, update import paths |
| `panels/ConsolidatedOverviewPanel.tsx` | `_shared/panels/ConsolidatedOverviewPanel.tsx` | SHARED | Move, update import paths |
| `panels/TaxCostBasisPanel.tsx` | `_shared/panels/TaxCostBasisPanel.tsx` | SHARED | Move, update import paths |
| `panels/types.ts` | `_shared/panels/types.ts` | SHARED | Move, update import paths |
| `panels/useSyncedHeight.tsx` | `_shared/panels/useSyncedHeight.tsx` | SHARED | Move, update import paths |
| `SmallAccountsByRoleModal.tsx` | `_shared/SmallAccountsByRoleModal.tsx` | AMBIGUOUS | Move provisionally; $40k threshold extraction proposed — see §4, Recommendation R1 |
| `tabs/AdvisorsTab.tsx` | `_shared/tabs/AdvisorsTab.tsx` | AMBIGUOUS | Move provisionally; role-label sourcing from `@/lib/chartColors` stays as-is pending CTO Q1 |
| `tabs/AssetIntelligenceTab.tsx` | `_shared/tabs/AssetIntelligenceTab.tsx` | SHARED | Move, update import paths (legacy tab, may be archived in W5.0.4 per DE discretion) |
| `tabs/ClientsTab.tsx` | `_shared/tabs/ClientsTab.tsx` | SHARED | Move, update import paths |
| `tabs/DistributionTab.tsx` | `_shared/tabs/DistributionTab.tsx` | 49F-SPECIFIC | Move; replace hardcoded BD source/tooltip copy with `sourceLabel?: string` + `tooltipAttribution?: { stateNna: string; cityAua: string }` props; partner page-root supplies BD strings |
| `tabs/FeeEfficiencyPanel.tsx` | `_shared/tabs/FeeEfficiencyPanel.tsx` | SHARED | Move, update import paths |
| `tabs/FeeRoleBreakdownPanel.tsx` | `_shared/tabs/FeeRoleBreakdownPanel.tsx` | SHARED | Move, update import paths |
| `tabs/FeeSummaryPanel.tsx` | `_shared/tabs/FeeSummaryPanel.tsx` | SHARED | Move, update import paths |
| `types.ts` | `_shared/types.ts` | AMBIGUOUS | Move provisionally; `AdvisorRole` union and `TaxDeferredCandidate.architect` field depend on CTO Q1 resolution |

### New Files (not moves)

| New File | Purpose |
|---|---|
| `index.tsx` | firmId router — reads firmId from AuthContext, dispatches to partner view |
| `_partners/49financial/index.tsx` | 49F page assembly — composes shared shell + BD source panel + firmId default |
| `_partners/49financial/constants.ts` | BD_SOURCE_ATTRIBUTION, AVAILABLE_FIRMS list, firmId default `'bd'`, BD tooltip copy |
| `_partners/inflection/index.tsx` | Stub — `export function InflectionAdvisorIntelligence() { return null; }` |
| `_partners/inflection/constants.ts` | Stub — empty exports, documented as W5.1 scope |

---

## Section 3 — 49F-SPECIFIC Refactor Approach

**Design principle:** For components whose only 49F-ism is attribution copy (vendor name string), prefer prop-extraction over file-duplication. The shared component stays in `_shared/` with an optional prop; the partner constants file owns the string. This avoids maintaining two near-identical copies of a large component (e.g., PartnerAnalytics.tsx is ~2000 lines).

For structural 49F-isms (AVAILABLE_FIRMS list, firmId default logic, Black Diamond Connected panel), these move to `_partners/49financial/` because they represent a 49F policy decision, not a rendering detail.

| Component | 49F-ism | Refactor Approach | Prop / Constant |
|---|---|---|---|
| `AdvisorIntelligence.tsx` | AVAILABLE_FIRMS hardcode; `'bd'` default; "Black Diamond Connected" panel layout | Move to `_partners/49financial/index.tsx` — not extractable as a prop; it IS the partner assembly | Partner owns the page root entirely |
| `ClientDetail/ClientDetailPage.tsx` | `firmId \|\| 'bd'` URL-param fallback | Add `defaultFirmId: string` prop; partner page-root passes `"bd"` | `_partners/49financial/constants.ts: DEFAULT_FIRM_ID = 'bd'` |
| `components/AUATrendChart.tsx` | `"Source: SS&C Black Diamond Wealth Solutions."` footer string | Add `sourceAttribution?: string` prop; omit renders no footer | `_partners/49financial/constants.ts: BD_SOURCE_ATTRIBUTION` |
| `components/PartnerAnalytics.tsx` | Same BD footer in 2 render paths | Same `sourceAttribution?: string` prop pattern | Same constant |
| `tabs/DistributionTab.tsx` | BD footer + 2 tooltip copy strings (3 locations) | Add `sourceLabel?: string` + `tooltipAttribution?: { stateNna: string; cityAua: string }` | `_partners/49financial/constants.ts: BD_SOURCE_ATTRIBUTION, BD_TOOLTIP_ATTRIBUTION` |

---

## Section 4 — index.tsx Router Composition Pattern

```tsx
// AdvisorIntelligence/index.tsx
import { useAuth } from '@/contexts/AuthContext';
import { Partner49FinancialView } from './_partners/49financial';
// import { InflectionView } from './_partners/inflection';  // W5.1

const PARTNER_VIEWS: Record<string, React.ComponentType<{ firmId: string }>> = {
  bd: Partner49FinancialView,
  // inflection: InflectionView,  // W5.1
};
const DEFAULT_PARTNER_VIEW = Partner49FinancialView;

export function AdvisorIntelligence() {
  const { claims, internal } = useAuth();
  const firmId = internal ? 'bd' : (claims?.firmId ?? 'bd');
  const PartnerView = PARTNER_VIEWS[firmId] ?? DEFAULT_PARTNER_VIEW;
  return <PartnerView firmId={firmId} />;
}
```

**Notes:**
- firmId resolution lives here in the router — not inside any individual partner component or shared component.
- `DEFAULT_PARTNER_VIEW = Partner49FinancialView` preserves the current behavior for unmapped firmIds.
- AVAILABLE_FIRMS list is removed from component code entirely; the router's `PARTNER_VIEWS` map IS the canonical firm registry.
- Adding Inflection = one `import` + one key in `PARTNER_VIEWS` (W5.1).

---

## Section 5 — AMBIGUOUS Row Recommendations for CTO Review

### R1 — SmallAccountsByRoleModal.tsx ($40k threshold) — CONCRETE RECOMMENDATION

**Recommendation: SHARED with `thresholdUsd: number` prop.**

The $40k threshold is a business rule that will vary by partner (fee schedules differ between 49F and Inflection). Making it a required prop now costs one prop call site but avoids a file fork later. DE recommends this regardless of CTO Q2 resolution:
- If Inflection uses the same $40k: partner config passes `40_000`, net code change is zero beyond the prop addition.
- If Inflection uses a different threshold: partner config passes its value, no conditional in the shared component.

Proposed prop: `thresholdUsd: number` (required, not optional — prevents silent use of a stale hardcode if a new partner forgets to pass it).
Proposed constant: `_partners/49financial/constants.ts: SMALL_ACCOUNT_THRESHOLD_USD = 40_000`.

### Q1 — Role Vocabulary (AdvisorBookView, AdvisorsTab, AdvisorPublicProfile, types.ts)

**CTO Question:** Are advisor roles (`architect` / `consultant` / `implementor` / `additional_advisor` / `local_ops`) 49F-specific vocabulary from BD's data model, or will Inflection expose the same 5-role taxonomy?

- **If same taxonomy:** All four files stay in `_shared/` unchanged. `AdvisorRole` union in `types.ts` is SHARED. No further action.
- **If different taxonomy:** `AdvisorRole` union in `types.ts` becomes `string` (generic) in `_shared/`; concrete role unions (`BD_AdvisorRole`, `InflectionAdvisorRole`) live in each partner's constants file. ROLE_LABELS/ROLE_COLORS/ROLE_ORDER in `AdvisorBookView.tsx`, `AdvisorsTab.tsx`, `@/lib/chartColors.ts` all become partner-injected props.

DE recommendation pending CTO answer. Files placed in `_shared/` provisionally.

### Q2 — $40k Threshold (SmallAccountsByRoleModal.tsx)

See R1 above — DE has a concrete recommendation that resolves this without waiting for CTO answer.

### Q3 — Book/Profile Access Model (AdvisorPublicProfile.tsx)

**CTO Question:** Does the "architect sees Book view; non-architect sees Profile-only" access model encode 49F's role hierarchy, or will Inflection adopt the same gating?

- **If same model:** `AdvisorPublicProfile.tsx` is SHARED, no changes needed.
- **If different model:** The tab-toggle condition needs a `bookAccessPolicy: (role: string) => boolean` prop injected by the partner page-root.

File placed in `_shared/` provisionally.

---

## Section 6 — _partners/49financial/constants.ts Sketch

```ts
// _partners/49financial/constants.ts
export const DEFAULT_FIRM_ID = 'bd' as const;
export const AVAILABLE_FIRMS = [{ id: 'bd', name: '49 Financial' }] as const;
export const BD_SOURCE_ATTRIBUTION = 'Source: SS&C Black Diamond Wealth Solutions.';
export const BD_TOOLTIP_ATTRIBUTION = {
  stateNna: 'State-level NNA from Black Diamond.',
  cityAua: 'City/State-level AUA from Black Diamond account data.',
} as const;
export const SMALL_ACCOUNT_THRESHOLD_USD = 40_000;
// ROLE constants (conditional on CTO Q1): move here if roles are 49F-specific
```

---

## Section 7 — Pre-Execution Gates (W5.0.3 / W5.0.4 Prerequisites)

Before W5.0.4 execution can begin:

| Gate | Owner | Blocks |
|---|---|---|
| CTO Q1 resolved (role taxonomy) | CTO | AdvisorBookView, AdvisorsTab, AdvisorPublicProfile, types.ts final placement |
| CTO Q3 resolved (Book/Profile access model) | CTO | AdvisorPublicProfile final prop design |
| R1 accepted (SmallAccountsByRoleModal prop extraction) | CTO / COO | SmallAccountsByRoleModal migration approach |
| W5.0.2 proposal accepted | CTO / COO | W5.0.4 execution start |

The 30 SHARED components and 5 49F-SPECIFIC components (with prop-extraction approach as specified above) are **unblocked** — W5.0.4 can begin their file moves immediately after CTO accepts this proposal.

The 5 AMBIGUOUS components (4 pending CTO Q1/Q3; 1 resolved by R1) are **blocked** pending CTO W5.0.3 sign-off.
