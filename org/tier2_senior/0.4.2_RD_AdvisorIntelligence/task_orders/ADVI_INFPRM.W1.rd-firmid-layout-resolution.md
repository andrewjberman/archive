<task_order>
<metadata>
  <to_id>ADVI_INFPRM.W1</to_id>
  <project>ADVI_INFPRM</project>
  <title>RD-FE: resolve the 3 firmId-scoped layout gates from firmId (not firmOverride) — fixes Role Composition (S1) + Book view (S3) for external Inflection; durable SHARED.006 two-param useTenantLayout</title>
  <assigned_to>0.4.2_RD_AdvisorIntelligence~C</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-06-02</issued_date>
  <status>READY-TO-DISPATCH (Andrew-directed parallel velocity 2026-06-02). Assigned to the 2nd RD-FE lane (0.4.2_RD_AdvisorIntelligence~C) MSTR is spawning — runs PARALLEL to RD~B's INFOTD/INFNNA track. COO dispatches on ~C register. (If MSTR spawns a different serial, COO re-addresses.) Authored correct-by-construction off INFPRM.P0 finding c35e3cd40.</status>
  <dispatch_held>false</dispatch_held>
  <priority>HIGH — Andrew-direct (5 screenshots). INFPRM = 2nd PROD promotion (after INFOTD). W1 (FE-only) fixes 2 of 3 symptoms.</priority>
  <references>
    <ref type="prd">docs/architecture/ADVI_INFPRM.md (sec.3.W1)</ref>
    <ref type="p0_finding">docs/briefs/advi-infprm-p0-firmoverride-resolution-sweep-finding-20260602.md (c35e3cd40, RD~B) — Deliverable (a) site table</ref>
    <ref type="reference_fix">PartnerAnalytics.tsx:173 useTenantLayout(firmId ?? firmOverride) — F1 already-fixed pattern (empirical token-fallback proof)</ref>
    <ref type="scope_doc">TenantLayoutConfig.ts:14-46 (firmId-scoped vs firmOverride-scoped; SHARED.006 two-param plan)</ref>
  </references>
</metadata>

<scope>
**Andrew-direct (screenshots).** Root cause (P0-confirmed): firmOverride = internal ? FIRM_ID : undefined (inflection/index.tsx:154) — for EXTERNAL users firmOverride=undefined flows into useTenantLayout() → useTenantLayout.ts:36 if(!firmId) return DEFAULT_LAYOUT → external Inflection users get DEFAULT_LAYOUT(49F) instead of their firm layout. W1 fixes the LAYOUT half (FE-only); W2 (AE) fixes the one DATA backend bug separately.

## The 3 sites to repoint useTenantLayout(firmOverride) → firmId (P0 Deliverable-a, RD-verified)
| File:line | Symptom fixed | Change |
|---|---|---|
| AdvisorPublicProfile.tsx:1155 | S1 — Role Composition wrongly renders for Inflection (+ profile-tab panel gate) | read firmId (honors INFLECTION roles.composition.enabled=false at inflection/layout.ts:135 vs DEFAULT=true) |
| AdvisorBookView.tsx:143 | S3 — Book view "Could not load book data" (handler-choice) | read firmId (resolves usesStaticClientDetail=true for Inflection → static adapter getPlatinumAdvisorSummaryStaticInflection, FE-fine, no edge change) |
| ClientsTab.tsx:150 (dataSourceLayout) | wrong L3/L4 handler + asset-class taxonomy | read firmId |

Already-correct (CONFIRM asymmetry, do NOT change): inflection/index.tsx:132, AdvisorsTab:241, ClientsTab:142, DistributionTab:813, PartnerAnalytics:173.

## DURABLE FIX (preferred) — SHARED.006 two-param hook
Implement `useTenantLayout(firmId, firmOverride?)` (TenantLayoutConfig.ts:40-46 plan): firmId-scoped fields (panels.* / roles.* / tabs.* / routes.*) resolve from firmId; dataSources.* from firmOverride ?? firmId. STRICTLY ADDITIVE (current single-param call-sites keep working). Then repoint the 3 sites to pass firmId. (Minimum fix if you defer the refactor: pass firmId at each of the 3 sites + thread firmId down from the index — mirror the F1 PartnerAnalytics:173 fix.)

## MANDATORY — cross-tenant regression matrix (CVO-verified; asymmetric bug)
Test ALL FOUR tenant contexts, not just Inflection — fixing external must NOT break the internal/firmOverride path:
- Inflection (external): Role Composition GONE, Book view LOADS (static adapter), correct firm layout.
- 49 Financial (external): unchanged, correct.
- demo: unchanged.
- internal/Opal (firmOverride defined): NO regression (still resolves from firmOverride/firmId correctly).
</scope>

<acceptance>
- [ ] AC1 — logged in as Peter (external Inflection): Role Composition panel does NOT render (INFLECTION roles.composition.enabled=false honored); Book view LOADS (Inflection static client-detail handler, not 49F dynamic-Lambda); no 49F-specific panel on any Inflection surface. 49F/demo/internal UNCHANGED (regression matrix all 4 contexts green). tsc -b + eslint green.
- [ ] CLOSURE: CVO verifies the cross-tenant regression matrix (the asymmetric-bug bar) + Andrew/CTO visual smoke (rendered-pixel; headless fabric-down) across all 4 contexts.

Lands on portal DEV (Rule 19). INFPRM = 2nd PROD promotion (separate from the INFOTD first bundle) — coordinate the promote with COO/CTO; do NOT fold into the INFOTD promote unless CTO/Andrew direct. RAVC2 diff + AC1 + regression-matrix evidence to ws CTO + COO + CVO.
</acceptance>

<notes>
Authored by COO from RD~B's P0 finding c35e3cd40 (Andrew-direct parallel-velocity 2026-06-02). 2nd RD-FE lane (parallel to RD~B). W1 (this, layout, FE-only) runs PARALLEL to W2 (AE, the getClientsTab backend bug — Symptom 2) — they're independent (W1=layout sites, W2=data leg). W1 fully fixes S1 (Role Composition) + S3 (Book view) for Inflection. Most data fetches are already FE-fine (static-S3 JWT-resolved per P0); only getClientsTab (Symptom 2) needs the W2 backend fix. CC RD~B (owns the _shared surface + F1 reference) for any coordination on the shared hook.
</notes>
</task_order>
