<task_order>
<metadata>
  <to_id>ADVI_INFPRM.P0</to_id>
  <project>ADVI_INFPRM</project>
  <title>RD: empirical confirm each firm-scoped symptom + full _shared sweep of useTenantLayout(firmOverride)/getPlatinum*(firmOverride) — produce exhaustive site list + FE-vs-edge determination (sizes W1/W2)</title>
  <assigned_to>0.4.2_RD_AdvisorIntelligence~B</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-06-02</issued_date>
  <status>DISPATCHED — RD~B PRIORITY-2 (after the INFOTD first-bundle work W1+W2F; CTO says P0 can start in parallel, so interleave the investigation as capacity allows). Read-heavy; gates INFPRM W1/W2 scope.</status>
  <dispatch_held>false</dispatch_held>
  <priority>HIGH — Andrew-direct (5 screenshots); but SECOND-promotion (after INFOTD). P0 is the fast sizing pass that unblocks W1/W2 authoring.</priority>
  <references>
    <ref type="prd">docs/architecture/ADVI_INFPRM.md (sec.2 root cause + sec.3.P0)</ref>
    <ref type="root">_partners/inflection/index.tsx:154 (firmOverride = internal ? FIRM_ID : undefined — the source)</ref>
    <ref type="scope_doc">TenantLayoutConfig.ts:14-46 (firmId-scoped vs firmOverride-scoped fields + SHARED.006 two-param plan)</ref>
    <ref type="reference_fix">ADVI_INFMVP F1 — PartnerAnalytics.tsx:101 (already-fixed pattern: takes both firmId + firmOverride)</ref>
  </references>
</metadata>

<scope>
**Andrew-direct (screenshots):** external partner users (peter@inflectionwealth.com, firmId=inflection) hit a cluster of panel-visibility + data-load bugs that internal/Opal users don't. CONFIRMED single root cause: firm-scoped (external) firmId doesn't flow into panel/role/layout gates or the data dispatch — those resolve from firmOverride, which is undefined for external users -> DEFAULT_LAYOUT(49F) + unscoped/failed fetches.

## P0 deliverable (this TO — the sizing pass)
1. **Empirically confirm each symptom's exact failing gate/fetch:**
   - Symptom 1 (Role Composition wrongly renders for Inflection) — confirmed: AdvisorPublicProfile.tsx:1155 useTenantLayout(firmOverride)->DEFAULT_LAYOUT->showRoleComposition=true; should honor INFLECTION_LAYOUT roles.composition.enabled=false. Re-confirm live.
   - Symptom 2 (Firm Overview absent for Peter, present for internal Andrew) — PIN the exact gate: ClientsTab.tsx:806/820 — is it a layout-visibility gate or a data query keyed on undefined firmOverride returning empty?
   - Symptom 3 (Book view 'Could not load book data') — confirm the two-part mechanism: AdvisorBookView.tsx:143 handler-choice (49F dynamic-Lambda vs Inflection static) + :162 getPlatinumAdvisorSummary(advisorId, firmOverride=undefined) unscoped fetch. Decide: pure FE routing (firmOverride undefined) OR does it ALSO need an edge/X-Firm-Id/Lambda@Edge auth-scope fix for external users?
2. **Sweep EVERY _shared AdvisorIntelligence consumer** for (a) useTenantLayout(firmOverride) [firmId-scoped gate read from firmOverride] and (b) getPlatinum*(..., firmOverride) data fetches that break on undefined firmOverride. Known starting set: AdvisorPublicProfile.tsx:1155, AdvisorBookView.tsx:143, ClientsTab.tsx (Firm Overview + L3/L4 fetches); also check AdvisorAnalytics.tsx, DistributionTab.tsx, the partner index pass-downs (:207/:225/:239/:255/:268). PartnerAnalytics is ALREADY FIXED (F1) — reference pattern, exclude.

## AC-P0
A confirmed, EXHAUSTIVE list of: (a) firmId-scoped gates wrongly reading firmOverride, and (b) data fetches that fail for firmOverride=undefined — with a per-site determination: FE-only fix vs needs-edge/backend (AE). This feeds the W1/W2 decomposition. Read-only investigation; no code change in P0 (flag before any write).
</scope>

<acceptance>
- [ ] AC-P0 — exhaustive confirmed site list (gates + fetches), FE-vs-edge determination per site, all 3 symptoms' exact mechanism pinned. RAVC2 the finding to ws CTO + COO (+ CVO for awareness). On receipt, COO + CTO author INFPRM W1 (firmId-scoped gate resolution, durable = SHARED.006 two-param useTenantLayout(firmId,firmOverride?)) + W2 (route firm data; AE-conditional if P0 finds an edge need).
</acceptance>

<notes>
Decomposed by COO from ws CTO PRD e5f750f7f (Andrew-direct). This is the audit-sweep ADVI_INFMVP F1 flagged (F1 fixed the first instance in PartnerAnalytics). INFPRM ships in a LATER promotion than INFOTD (CTO rec). Priority-wise: INFOTD W1+W2F come first (they gate the held S5 first-promote); start P0's read-heavy investigation in parallel/interleaved as capacity allows. W1/W2 full TOs authored post-P0 (P0 sizes them + decides AE-conditional). REGRESSION MATRIX (49F/demo/internal) will be MANDATORY on W1/W2 — asymmetric bug; CVO verifies the matrix.
</notes>
</task_order>
