# Task Order: Yang V2 Y15 — Books Tab L2/L3/L4 MVP — 0.4.2_RD_AdvisorIntelligence

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-05-ADVI-Y15-books-tab-l2-l3-l4</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-05</date>
    <status>pending</status>
    <priority>HIGH</priority>
    <stream>Y15</stream>
    <thread_serial>ADVI-006</thread_serial>
  </metadata>

  <objective>
    Implement the Books tab (ClientsTab.tsx) L2/L3/L4 MVP per the ADVI-006 design brief.
    The data already exists on S3 (book.json per advisor, client JSON per relationship).
    No new backend work is required for MVP.

    Access model: admin/internal only (gated by isInternal() || isDev()).
    No advisor-facing routing. No advisor-mode landing UX. That requires Gap A resolution.

    Gate: DE type wiring (ADVI-Y-phase3-de-type-wiring) must be committed to portal DEV.
  </objective>

  <references>
    <ref type="design-brief" priority="PRIMARY">docs/architecture/advisor_intelligence/books_tab_design_brief.md</ref>
    <ref type="portal-books">portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</ref>
    <ref type="portal-client-detail">portal/src/pages/AdvisorIntelligence/ClientDetail/ClientDetailPage.tsx</ref>
    <ref type="types">portal/src/pages/AdvisorIntelligence/types.ts — AdvisorBookResponse, ClientDetailResponse (after DE gate)</ref>
    <ref type="api">portal/src/api/endpoints/advisor-intelligence.ts — getAdvisorBook(), getClientDetail() (after DE gate)</ref>
    <ref type="primitives">Portal panel primitives (Panel, PanelHeader, PanelContent) from existing AdvisorsTab/DistributionTab usage</ref>
  </references>

  <gate>
    DE type wiring must be confirmed (getAdvisorBook, getClientDetail endpoints + all types).
    Read DE's portal DEV commit before starting.
  </gate>

  <requirements>

    <!-- ================================================================ -->
    <!-- ACCESS MODEL                                                      -->
    <!-- ================================================================ -->
    <requirement id="Y15.access">
      The Books tab is admin/internal only for MVP. The existing gate in ClientsTab.tsx
      (isInternal() || isDev() check via useAuth()) must remain. Do not add advisor-facing
      routing or URL patterns. Do not add any "scoped advisor" access mode.

      Gap A (advisor identity mapping to opal-users-v2) is unresolved — advisor-mode
      access is blocked until that gap is closed by DS + DT. This task order builds
      the admin-visible MVP only.
    </requirement>

    <!-- ================================================================ -->
    <!-- L2 — ADVISOR BOOK VIEW                                           -->
    <!-- ================================================================ -->
    <requirement id="Y15.L2">
      The L2 view shows an individual advisor's aggregate book.

      For admin users, there is a dropdown or list of available advisors. Selecting an
      advisor fetches getAdvisorBook(advisorId) and renders four panels:

      Panel 1 — Advisor Book Summary (from design brief Section 1.1):
        Total AUA, Client Count, Account Count, NNA MTD/QTD/YTD,
        Growth QTD%/YTD%, Data As Of.

      Panel 2 — Tax Exposure (from design brief Section 1.2):
        Taxable, Tax Deferred, Tax Free with AUA amounts and percentages.
        Qualified vs Non-Qualified breakdown.
        Non-Qualified Cost Basis, Unrealized Gain.
        Short Term Gain, Long Term Gain.

      Panel 3 — Engagement (from design brief Section 1.3):
        Net Flows TTM, Inflows TTM, Outflows TTM (currency format).
        Avg Tenure — display as years (avg_tenure_days / 365.25, 1 decimal place).

      Panel 4 — Clients (from design brief Section 1.4):
        Table: client_name, AUA columns.
        Row click navigates to L3 using client_key.

      HIDDEN (do not stub):
        income_fees panel — hardcoded zeros, do not show.
        portfolio_composition panel — empty, do not show.

      Use formatCurrency for all dollar values. Use existing Panel primitives.
    </requirement>

    <!-- ================================================================ -->
    <!-- L3 — CLIENT DETAIL (RELATIONSHIP VIEW)                           -->
    <!-- ================================================================ -->
    <requirement id="Y15.L3">
      L3 is the existing ClientDetail page or a new view within Books.
      Fetches getClientDetail(clientKey) on navigation from L2 clients table.
      Read ClientDetailPage.tsx to understand what already exists before adding panels.

      Render five panels (from design brief Sections 2.1-2.5):

      Panel 1 — Client Summary (Section 2.1):
        Total AUA, Account Count, Data As Of.

      Panel 2 — Accounts (Section 2.2):
        Table: account_id, tax_status, total_aua, cum_inflows, cum_outflows, nna,
        num_positions columns.
        Row click sets selectedAccountId state (triggers L4 inline drill — see Y15.L4).

      Panel 3 — Tax Intelligence (Section 2.3):
        Taxable/Tax Deferred/Tax Free with AUA + percentages.
        Qualified/Non-Qualified breakdown.
        cost_basis_by_year table: year, cost_basis, market_value, unrealized_gain.
        top_gain_positions table: asset_name, ticker, unrealized_gain, cost_basis,
        market_value, term.

      Panel 4 — Taxable Open Lots (Section 2.4):
        Label MUST read "Taxable Open Lots" — not "Holdings" or "Lots".
        Table of open_lots[]: asset_name, ticker, quantity, cost_basis, market_value,
        unrealized_gain, term, acquisition_date.
        Filters: Term toggle (Short/Long) and Account dropdown (filtered by account_id).

      Panel 5 — Engagement (Section 2.5):
        Net Flows TTM (currency), Avg Relationship Years (1 decimal place).

      HIDDEN (do not stub):
        income_fees panel — hardcoded zeros, do not show.
        portfolio.allocation — empty, do not show.

      Back navigation returns to L2.
    </requirement>

    <!-- ================================================================ -->
    <!-- L4 — ACCOUNT + HOLDINGS INLINE DRILL                            -->
    <!-- ================================================================ -->
    <requirement id="Y15.L4">
      L4 is NOT a new route. It is an inline expansion inside L3, triggered by clicking
      an account row in the Accounts panel (Panel 2).

      State: selectedAccountId: string | null (null = no account selected)
      When selectedAccountId is set, expand an inline section below the Accounts panel:

      Sub-panel 1 — Account Detail (Section 3.1):
        Show the selected account's fields from accounts[selectedIndex]:
        account_id, tax_status, total_aua, cum_inflows, cum_outflows, nna, num_positions.

      Sub-panel 2 — Taxable Open Lots (Account-Scoped) (Section 3.2):
        Filter tax.open_lots[] by account_id === selectedAccountId.
        Same table structure as L3 Panel 4 but scoped to this account.
        Label: "Taxable Open Lots — {account_id}".

      A "Clear selection" or "Close" affordance sets selectedAccountId back to null.

      No new API calls for L4 — all data comes from the same L3 JSON payload.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">L2 renders 4 panels: Summary, Tax Exposure, Engagement, Clients table. isInternal/isDev gate maintained.</criterion>
    <criterion id="2">L2 clients table row click navigates to L3 with client_key.</criterion>
    <criterion id="3">L3 renders 5 panels: Client Summary, Accounts, Tax Intelligence, Taxable Open Lots, Engagement.</criterion>
    <criterion id="4">Panel 4 label is exactly "Taxable Open Lots".</criterion>
    <criterion id="5">L4 is inline inside L3 (no new route). Triggered by account row click. Shows Account Detail + scoped lots.</criterion>
    <criterion id="6">income_fees and portfolio_composition panels are not rendered anywhere (not stub, not hidden div).</criterion>
    <criterion id="7">All currency values use formatCurrency. Tenure/years use correct division formula.</criterion>
    <criterion id="8">tsc clean. getAdvisorBook and getClientDetail typed against AdvisorBookResponse/ClientDetailResponse.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT start before DE type wiring portal DEV commit is confirmed.</constraint>
    <constraint>Do NOT add advisor-facing routing or scoped access mode. Admin-only MVP.</constraint>
    <constraint>Do NOT stub income_fees or portfolio_composition panels — they must be completely absent from the DOM.</constraint>
    <constraint>L4 is inline expansion, not a new page/route.</constraint>
    <constraint>Panel label "Taxable Open Lots" is binding — see design brief Section 2.4.</constraint>
    <constraint>Do NOT use emojis in any code or log output.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "..."</constraint>
  </constraints>

  <backend_gaps_for_reference>
    These gaps are documented in the design brief Section 5 for awareness only.
    RD does NOT implement these — they are DS + DT future work.
    Do not block L2/L3/L4 MVP on them. Build with what exists.

    Gap A: Advisor identity mapping (opal-users-v2 advisorKey) — required for advisor-mode access
    Gap B: Relationship performance timeseries — no timeseries key in client JSON yet
    Gap C: Account metadata enrichment (account_name, account_type, etc.)
    Gap D: Positions list + weights
    Gap E: Non-taxable holdings/lots expansion
    Gap F: Income/fees + portfolio taxonomy (upstream data not available)
  </backend_gaps_for_reference>

  <deliverables>
    <deliverable type="commit">portal DEV: Books tab L2 advisor book + L3 client detail + L4 inline account drill</deliverable>
    <deliverable type="document">Session log with portal DEV commit hash</deliverable>
  </deliverables>

</task_order>
```
