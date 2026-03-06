<task_order>
  <metadata>
    <id>ADVI_49FNV3.N1-N2-DE.firm-dashboard-and-advisor-book-wiring</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-06</date>
    <status>pending</status>
    <thread_serial>ADVI_49FNV3-002</thread_serial>
    <thread_ref>org/threads/ADVI_49FNV3-002-pattern-0-books-tab-design-brief-n1-n2/</thread_ref>
  </metadata>

  <objective>
    Wire N1 (Firm Admin Dashboard) and N2 (Advisor Book View) in the Books tab. Both phases use
    existing published data — no backend Lambda changes required for Phase 1b. The design brief and
    TypeScript interfaces are the binding contract.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Add TypeScript interfaces from
      `docs/architecture/advisor_intelligence/books_tab_design_brief.md` Section 6:
      `AdvisorBookResponse`, `AdvisorBookClient`, `ClientDetailResponse`, `ClientAccount`,
      `ClientTaxDetail`, `CostBasisYear`, `GainPosition`, `OpenLot`.
      No `any` types. These are the agreed interfaces from thread ADVI_49FNV3-002.</requirement>
    <requirement id="2">N1 Firm Admin Dashboard -- wire four panels using existing data endpoints:
      - Firm Overview KPIs: `getClientsTab()` -> `headline.total_aua`, `headline.account_count`, `headline.client_count`
      - Tax Status Breakdown: `getClientsTab()` -> `tax.taxable/taxable_pct`, `tax.tax_deferred/tax_deferred_pct`, `tax.tax_free/tax_free_pct`
      - Engagement Summary: `getClientsTab()` -> `engagement.net_flows_ttm`, `engagement.avg_relationship_years`, `engagement.active_clients_pct`
      - AUA by Advisor (1Y): `getArchitectLeaderboard()` -> `windows['1Y'].entries[]` sorted client-side by `total_aua` desc. Reuse the existing `AdvisorSummaryTable` pattern (Option A from thread). Row click -> N2 drill.
    </requirement>
    <requirement id="3">N2 Advisor Book View -- clicking an advisor row in N1 sets selectedAdvisorId state
      and renders the L2 panels from the design brief using `getAdvisorBook(advisorId)` ->
      `advisors/{advisor_id}/book.json`. Panels: Summary KPIs, Tax Exposure, Engagement, Clients table.</requirement>
    <requirement id="4">CRITICAL -- advisorId slug fix: replace the current whitespace-only slug
      (`replace(/\s+/g,'_')`) in BooksTab with an exact replica of the publisher's `_advisor_id()` function:
      `name.toLowerCase().trim().replace(/[^a-z0-9_]+/g, '_').replace(/^_+|_+$/g, '') || 'unknown'`
      This prevents 404s for advisor names containing punctuation or suffixes (e.g. "Travis Penfield Jr.").</requirement>
    <requirement id="5">Access gate: N1/N2 is internal-only for MVP. Gate the Books tab view with
      `isInternal() || isDev()` per the design brief. No advisor-facing access until Y14 gating is implemented.</requirement>
    <requirement id="6">Median AUA is NOT in clients_tab.json headline. Do not display it in N1.
      Only show confirmed fields from the thread discussion.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">N1 renders all four panels with real data from clients_tab.json + architect_leaderboard.json.</criterion>
    <criterion id="2">Clicking an advisor in N1 drills to N2 showing their book data.</criterion>
    <criterion id="3">advisorId slug matches the publisher's _advisor_id() function exactly.</criterion>
    <criterion id="4">TypeScript compiles cleanly. No `any` types in new code.</criterion>
    <criterion id="5">Portal DEV commits with `--author` flag. Session log written.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Scope is N1+N2 (Phase 1b) only. Do NOT implement L3/L4 (Phase 2a) in this task order.</constraint>
    <constraint>Do NOT stub panels for income_fees or portfolio_composition -- those are Phase 2b (data unavailable).</constraint>
    <constraint>No backend changes. All data exists in published S3 JSON.</constraint>
    <constraint>After wiring, issue RD task order to implement the visual layout for N1+N2.</constraint>
  </constraints>

  <dependencies/>

  <deliverables>
    <deliverable type="commit">Portal DEV commits: types.ts interface additions + N1/N2 wiring in ClientsTab.tsx.</deliverable>
    <deliverable type="document">Session log noting any data gaps found vs design brief.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md</ref>
    <ref type="thread">org/threads/ADVI_49FNV3-002-pattern-0-books-tab-design-brief-n1-n2/messages/</ref>
    <ref type="brief">docs/architecture/advisor_intelligence/books_tab_design_brief.md</ref>
  </references>
</task_order>
