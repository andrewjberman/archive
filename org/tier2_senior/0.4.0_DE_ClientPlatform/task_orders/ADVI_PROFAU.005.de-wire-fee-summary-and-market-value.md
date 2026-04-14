<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-14-profau-005</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>complete</status>
    <project_code>ADVI_PROFAU</project_code>
  </metadata>

  <references>
    <ref type="audit_response">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/profau_gap_audit_response.md (Q4, Q5)</ref>
  </references>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform"
                task="ADVI_PROFAU.004.de-type-fix-platinum-advisor-summary"
                status="staged"
                description="Run .005 after .004 — types.ts must be fixed so AdvisorClient and related types are clean before adding renders."/>
  </dependencies>

  <objective>
    Wire two EXISTS-UPSTREAM fields that are already live in platinum JSON but never rendered
    in the frontend. No gold script changes needed.

    Q4 — `fee_summary` at L3 (per-client): render FeeSummaryByAccount from
    `platinum/clients/{id}/summary.json → fee_summary` in the client detail view.

    Q5 — `total_market_value` at L4 (per-account): render total_market_value from
    `platinum/accounts/{id}/summary.json → total_market_value` in the account detail view.

    These are both EXISTS-UPSTREAM (data already emitted by D_04 and verified live).
    No dependency on PROFAU .003 QA run or any DS work.
  </objective>

  <context>
    WHAT IS NOT IN THIS TO:
    - Q1 (capital_gains_ttm + cost_basis_by_year in TaxCostBasisPanel at L2): deferred to
      ADVI_PROFAU.006 — gates on .003 QA run confirming platinum/advisors/{id}/summary.json
      has capital_gains_ttm + cost_basis_by_year in tax_exposure. DS will MCP-signal when QA clears.
    - Q2 (is_fee_paying per AdvisorClient at L3): deferred to ADVI_PROFAU.007 — gates on DS
      authoring Q2 DS TO to add is_fee_paying bool to D_02 book.clients. Not live in JSON yet.
    - Q6 (PlatinumAdvisorSummary type drift): handled in .004.
    - Q3/Q7 (fee_earning_mask billability alignment): DS TOs not yet authored.

    WHAT IS IN THIS TO (both EXISTS-UPSTREAM):
    Q4 — fee_summary at L3:
      Source: platinum/clients/{id}/summary.json → fee_summary.by_account[]{account_id, fee_bps, implied_revenue}
      D_02 line 811: _build_fee_summary_by_account. D_04 line 687: passthrough. Data is live.
      Type: PlatinumClientSummary.fee_summary: FeeSummaryByAccount | null (already declared).
      comp-transform: shows fee_summary as UNUSED on PlatinumClientSummary. DE one-liner.
      Render location: AdvisorBookClientDetail.tsx or ConsolidatedOverviewPanel at L3.
      Suggested render: per-account bps display (e.g. "X bps / $Y implied revenue" row per account).

    Q5 — total_market_value at L4:
      Source: platinum/accounts/{id}/summary.json → total_market_value (C_05 → D_04 passthrough)
      Type: PlatinumAccountSummary.total_market_value: number (already declared, live in JSON).
      Render location: AdvisorBookAccountDetail.tsx at L4 header or balance row.
      Suggested render: "Market Value: $X" in account summary header.

    comp-transform baseline:
      PlatinumClientSummary — UNUSED: accounts, fee_summary, mix_periods, name, tax, total_aua
      PlatinumAccountSummary — 6 declared, 4 rendered, OK (total_market_value is one of the 2 unrendered)
  </context>

  <scope>
    <files>
      <file action="edit">portal/src/pages/AdvisorIntelligence/AdvisorBookView.tsx or relevant L3/L4 sub-components</file>
    </files>
    <out_of_scope>
      TaxCostBasisPanel at L2 — deferred to .006 (gates on .003 QA).
      is_fee_paying per AdvisorClient — deferred to .007 (gates on DS Q2 TO).
      Any gold script changes. Any new API endpoint wiring. types.ts (handled by .004).
    </out_of_scope>
  </scope>

  <acceptance_criteria>
    1. `bun run typecheck` passes with 0 new errors.
    2. L3 (client detail): fee_summary renders — at minimum shows per-account fee bps or implied revenue for clients that have fee data. Null-safe: advisors without fee_summary show nothing (no crash).
    3. L4 (account detail): total_market_value renders — "Market Value: $X" or equivalent label visible in account header/summary. Null-safe.
    4. comp-transform schema-check AdvisorBookView after change: fee_summary removed from UNUSED list on PlatinumClientSummary.
    5. No console errors when drilling L3 or L4 on PROD after deploy.
    6. Session log with compiler tools section committed.
    7. MCP message to 2.0.0_SA_COO: "PROFAU .005 complete — fee_summary L3 + total_market_value L4 wired."
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1 (before writing): Run `comp-transform schema-check AdvisorBookView` — confirm
    fee_summary UNUSED on PlatinumClientSummary. Run `comp-blast AdvisorBookView` — confirm
    blast radius (3 endpoints, 1 Lambda, isolated).
    Phase 2 (before commit): `bun run typecheck` — 0 new errors.
    Phase 3 (after commit): Run `comp-transform schema-check AdvisorBookView` — confirm
    fee_summary removed from UNUSED. Append one line to org/compiler-tools-log.md.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>portal/src/pages/AdvisorIntelligence/AdvisorBookView.tsx (and sub-components)</shared_resource>
    <required_action>
      Run .005 after .004 lands on CLOUD — pull latest before editing. This is the FOURTH
      portal edit in the session flow: W6-004 → W3 → .004 → .005. No simultaneous edits.
    </required_action>
    <deferred_items>
      .006 (Q1 TaxCostBasisPanel L2): staged pending PROFAU .003 QA confirmation from DS.
      .007 (Q2 is_fee_paying): staged pending DS Q2 TO authoring and execution.
    </deferred_items>
  </cross_domain_coordination>
</task_order>
