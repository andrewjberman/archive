<task_order>
  <metadata>
    <id>ADVI_49FNV3.N1-N2-RD.firm-dashboard-and-advisor-book-ui</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-06</date>
    <status>complete</status>
    <thread_serial>ADVI_49FNV3-002</thread_serial>
    <thread_ref>org/threads/ADVI_49FNV3-002-pattern-0-books-tab-design-brief-n1-n2/</thread_ref>
  </metadata>

  <objective>
    Implement the visual layout for N1 (Firm Admin Dashboard) and N2 (Advisor Book View) in the
    Books tab. DE wires the data and types first (ADVI_49FNV3.N1-N2-DE task order); RD implements
    the visual panels using the confirmed data structure.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">N1 Firm Admin Dashboard -- four-panel grid layout:
      1. Firm Overview KPIs: headline total_aua, account_count, client_count as KPI cards
      2. Tax Status Breakdown: horizontal bar or donut showing taxable/tax_deferred/tax_free with AUA + percentages
      3. Engagement Summary: net_flows_ttm, avg_relationship_years, active_clients_pct as KPI tiles
      4. AUA by Advisor (1Y): table (AdvisorSummaryTable pattern) sorted by total_aua desc, row click drills to N2
    </requirement>
    <requirement id="2">N2 Advisor Book View -- activated by clicking an advisor in N1:
      Per design brief Section 1 (docs/architecture/advisor_intelligence/books_tab_design_brief.md):
      - 1.1 Advisor Book Summary: total_aua, client_count, account_count, NNA mtd/qtd/ytd, growth qtd/ytd as KPI cards
      - 1.2 Tax Exposure: taxable/deferred/free plus qualified/non-qualified breakdown
      - 1.3 Engagement: net_flows_ttm, inflows_ttm, outflows_ttm, avg_tenure_days (display as years)
      - 1.4 Clients table: client_name, aua, row click navigates to L3 (leave L3 to Phase 2a)
    </requirement>
    <requirement id="3">Hidden panels (DO NOT stub): income_fees, portfolio_composition.
      These fields contain hardcoded zeros in the publisher. Do not render them at all.</requirement>
    <requirement id="4">Reuse existing portal primitive components: Panel, PanelHeader, PanelContent,
      formatCurrency, formatNumberTo3Digits, LoadingInline. Do not invent new layout primitives.</requirement>
    <requirement id="5">Back/breadcrumb navigation: when in N2, show a "Back to Firm Overview" link
      that returns to N1 state.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">N1 four panels render with correct data from clients_tab.json + architect_leaderboard.json.</criterion>
    <criterion id="2">Clicking an advisor in N1 transitions to N2 with that advisor's book data.</criterion>
    <criterion id="3">N2 panels render all confirmed fields. No panels for income_fees or portfolio.</criterion>
    <criterion id="4">Back navigation returns to N1.</criterion>
    <criterion id="5">Portal DEV commit with `--author` flag.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>DE wiring complete (ADVI_49FNV3.N1-N2-DE marked complete 2026-03-06). Dependency resolved. DT pre-implemented functional panels in commit 1dc96b5 (DEV) -- RD reviews visual quality and polishes as needed.</constraint>
    <constraint>Do not implement L3/L4 visual panels -- Phase 2a only.</constraint>
    <constraint>Do not render any field that DE has not confirmed is in the published JSON.
      Design brief Section 5 lists gaps -- those panels stay hidden.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_49FNV3.N1-N2-DE.firm-dashboard-and-advisor-book-wiring" status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Portal DEV commit implementing N1+N2 visual layout.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md</ref>
    <ref type="thread">org/threads/ADVI_49FNV3-002-pattern-0-books-tab-design-brief-n1-n2/messages/</ref>
    <ref type="brief">docs/architecture/advisor_intelligence/books_tab_design_brief.md</ref>
  </references>
</task_order>
