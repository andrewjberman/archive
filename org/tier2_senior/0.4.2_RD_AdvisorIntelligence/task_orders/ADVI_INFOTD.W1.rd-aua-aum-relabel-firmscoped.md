<task_order>
<metadata>
  <to_id>ADVI_INFOTD.W1</to_id>
  <project>ADVI_INFOTD</project>
  <title>RD-FE: AUA->AUM display relabel on firm-scoped views (AdvisorIntelligence unconditional ~90 sites; ModelPortfolios conditional on effectiveFirmId!=='global' ~15 sites) — display labels ONLY, never keys</title>
  <assigned_to>0.4.2_RD_AdvisorIntelligence~B</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-06-02</issued_date>
  <status>DISPATCHED — RD~B PRIORITY-1 (gates the held S5 first-promotion). FE-only, INDEPENDENT (no data dep), can land immediately.</status>
  <dispatch_held>false</dispatch_held>
  <priority>HIGH — Andrew-direct; first-promotion-bundle (S5 + NNA + INFOTD-W1 + INFOTD-W2). The held S5 PROD promote waits on this + W2.</priority>
  <references>
    <ref type="prd">docs/architecture/ADVI_INFOTD.md (sec.3.W1 — full file:line inventory)</ref>
    <ref type="rule">always-firm-scoped: AdvisorIntelligence/index.tsx:42</ref>
    <ref type="rule">conditional: ModelPortfolios.tsx:259/:269/:651/:1770 (effectiveFirmId!=='global')</ref>
  </references>
</metadata>

<scope>
**Andrew-direct:** for a single firm the correct asset term is AUM/"Assets under Management" (a firm MANAGES its own assets), NOT AUA/"Assets under Advisory" (Opal advising ACROSS firms). Rename the user-facing DISPLAY LABEL "AUA"->"AUM" and "Assets under Advisory"->"Assets under Management" on firm-scoped views.

## Two scoping rules (verified in PRD)
- **AdvisorIntelligence = ALWAYS firm-scoped (NO Opal-aggregate view)** -> rename UNCONDITIONALLY (~90 sites across ~22 files). index.tsx:42 firmId = internal ? selectedFirmId : (claims?.firmId ?? '49financial'); no 'global'/'all' option.
- **ModelPortfolios HAS a global view that MUST keep "AUA"** -> rename CONDITIONALLY on effectiveFirmId !== 'global' (~15 sites). Firm view -> "AUM"; global view -> "AUA". Precedent in-file at :1770.

## Implementation (recommended): introduce a helper
Add `assetsLabel(firmScoped: boolean)` (e.g. src/lib/assetsLabel.ts) returning AUM/AUA short + long forms. AdvisorIntelligence passes `true` always; ModelPortfolios passes `effectiveFirmId !== 'global'`. Also NORMALIZE the current expansion inconsistency — codebase mixes "Assets Under Advisory" / "assets under advisement" / "Assets Under Administration" (HeaderMetrics:47, AssetIntelligenceTab:151) -> standardize firm-scoped to "Assets under Management".

## Inventory (PRD sec.3.W1 has every file:line)
- ModelPortfolios.tsx (~15, conditional): :609/:620/:643/:705/:725/:735/:748/:818/:943/:1027/:1174(label only, keep id:'growth')/:1224/:1226/:1474/:1770.
- AdvisorIntelligence ~90 across ~22 files: AdvisorsTab, AdvisorPublicProfile, PartnerAnalytics, AdvisorAnalytics, AUATrendChart, AssetIntelligenceTab, DistributionTab, FeeSummaryPanel, FeeEfficiencyPanel, ClientsTab, ClientsTable, ClientListPanel, ConsolidatedOverviewPanel, TaxCostBasisPanel, PortfolioBalancePanel, HeaderMetrics, AUACompositionChart, SmallAccountsByRoleModal, AdvisorBookView, AdvisorBookAccountDetail, AdvisorBookAccountModal, InflectionInsightsPanel, partner index headers, per-firm constants.ts cityAua tooltips. (PeersTab = zero AUA strings.)

## CRITICAL — DO NOT RENAME (renaming breaks logic): display strings ONLY
Never touch: value:'aua' toggle values; dataKey="total_aua"; name="AUA" series binding (AdvisorAnalytics:620 rename `name` display only); sortKey/field/col 'aua'; key:'existing_aua' (AUACompositionChart:43 rename `label` only); LeaderboardMetric='aua'|'nna'|'gro' type; data fields (total_aua/fee_earning_aua/hh_aua); AUA_COLOR(S); component/type names (AUATrendChart, AUACompositionChart); geo_aua_grain; 'gold_aua' layout config; code comments. (PRD sec.3.W1 lists the exact ~13 key sites to leave.)
</scope>

<acceptance>
- [ ] AC1 — firm-scoped user (peter@inflectionwealth.com/Inflection + a 49F external user): EVERY asset-metric label on ModelPortfolios (firm view) AND every AdvisorIntelligence surface reads "AUM"/"Assets under Management". The GLOBAL ModelPortfolios view (internal/Opal) still reads "AUA". No mode toggle / data key / sort key / series binding renamed (ZERO logic regression). tsc -b + eslint green.
- [ ] CLOSURE (visual smoke, Andrew/CTO — headless FE smoke fabric-down): rendered labels confirmed on Inflection + a 49F-external view + the internal/global view.

Land on portal DEV (Rule 19, main tree stays DEV). Bundles into the FIRST DEV->PROD promotion with S5 (99d049d9) + NNA (9df6ea69) + INFOTD-W2 — you own the single 5-phase promote on CTO GO once W1+W2 land+smoke. Do NOT promote in isolation. RAVC2 diff + AC1 to ws CTO + COO.
</acceptance>

<notes>
Decomposed by COO from ws CTO PRD e5f750f7f (Andrew-direct). RD~B owns (AI pages + the S5 ModelPortfolios change). Priority-1 of your queue (gates the held S5). INFOTD.W2F (Count FE consume) follows after DS INFOTD.W2D served-verify; INFPRM.P0 (sweep) is next after the INFOTD first-bundle work. Display-label-only — numbers unchanged.
</notes>
</task_order>
