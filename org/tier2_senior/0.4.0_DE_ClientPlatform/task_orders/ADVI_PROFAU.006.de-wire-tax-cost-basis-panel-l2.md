<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-14-profau-006</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>ADVI_PROFAU</project_code>
  </metadata>

  <references>
    <ref type="audit_response">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/profau_gap_audit_response.md (Q1)</ref>
    <ref type="qa_confirmation">DS message 20260414T — platinum/advisors/{id}/summary.json confirmed to have capital_gains_ttm + cost_basis_by_year</ref>
  </references>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform"
                task="ADVI_OFFICE.W3.de-ofc-frontend"
                status="pending"
                description="Finish W3 first — different component (DistributionTab vs AdvisorBookView) but pull latest CLOUD before editing."/>
    <dependency agent="0.4.0_DS_ClientPlatform"
                task="ADVI_PROFAU.003.ds-d02-book-level-tax-aggregates"
                status="complete"
                description="QA confirmed 2026-04-14: capital_gains_ttm (float) + cost_basis_by_year (list) present in platinum/advisors/{id}/summary.json.tax_exposure."/>
  </dependencies>

  <objective>
    Wire TaxCostBasisPanel at L2 (advisor/book view) in AdvisorBookView. The data is now
    confirmed live in platinum/advisors/{id}/summary.json.tax_exposure. Closes Q1 from
    the PROFAU gap audit.
  </objective>

  <context>
    QA-confirmed platinum shape (DS verification 2026-04-14, checked travis_penfield + 2 others):

    platinum/advisors/{id}/summary.json -> tax_exposure:
      capital_gains_ttm: number (float, $USD)
      cost_basis_by_year: Array of {
        purchase_year: number,
        cost_basis: number,
        market_value: number,
        unrealized_gain: number
      }  -- 30 entries for Travis
      tax_exposure_fee_paying: { ... }  (PROFAU.002, already live)
      tax_exposure_no_fee: { ... }      (PROFAU.002, already live)

    IMPORTANT — cost_basis_by_year is a LIST, not a dict. Iterate by index or
    purchase_year field. Do NOT try to access by year as a key.

    Wiring path:
    - getPlatinumAdvisorSummary() -> PlatinumAdvisorSummary.tax_exposure (type already
      updated in .004 to include these fields)
    - AdvisorBookView L2 passes tax props to TaxCostBasisPanel
    - At L3 (per-client), these panels already render from clientDetail.tax.* (LIVE)
    - At L2 (advisor/book), the same TaxCostBasisPanel component should render using
      bookData.tax_exposure.capital_gains_ttm and bookData.tax_exposure.cost_basis_by_year

    NOT IN THIS TO:
    - top_gain_positions at L2 — D_04 holdings_lots join not yet done; pass [] as placeholder
    - The top_gain_positions work is a future .008 TO (requires D_04 holdings_lots aggregation)
  </context>

  <scope>
    <files>
      <file action="edit">portal/src/pages/AdvisorIntelligence/AdvisorBookView.tsx — L2 tax prop build (lines ~259-266)</file>
    </files>
    <out_of_scope>
      types.ts — already updated in .004.
      top_gain_positions — pass [] placeholder, do not fetch or compute.
      L3/L4 panels — handled by .005 and already live.
      Any gold scripts.
    </out_of_scope>
  </scope>

  <acceptance_criteria>
    1. `bun run typecheck` passes with 0 new errors.
    2. TaxCostBasisPanel renders at L2 (advisor/book) with capital_gains_ttm value visible.
    3. cost_basis_by_year chart/table renders — iterates list by purchase_year field, not dict key access.
    4. top_gain_positions passed as [] — no crash, no empty-state error if component handles null/empty gracefully.
    5. Null-safe: advisors with no tax_exposure data show nothing (no crash).
    6. comp-transform schema-check AdvisorBookView: capital_gains_ttm removed from UNUSED list.
    7. Session log with compiler tools section committed.
    8. MCP message to 2.0.0_SA_COO: "PROFAU .006 complete."
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1 (before writing): comp-transform schema-check AdvisorBookView — confirm
    capital_gains_ttm is accessible via PlatinumAdvisorSummary.tax_exposure after .004 fix.
    Phase 2 (before commit): bun run typecheck — 0 new errors.
    Phase 3 (after commit): comp-transform schema-check AdvisorBookView — confirm
    capital_gains_ttm no longer UNUSED. Append one line to org/compiler-tools-log.md.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>portal/src/pages/AdvisorIntelligence/AdvisorBookView.tsx</shared_resource>
    <required_action>
      Pull latest CLOUD after W3 lands before editing AdvisorBookView. W3 touches
      DistributionTab (different component) so no direct conflict, but types.ts changes
      from .004 must be present — confirm .004 commit (0050c05) is in your local HEAD.
    </required_action>
    <deploy_note>
      .006 may ship in the same DT W4 deploy as W3+.004+.005 if DE completes before DT
      begins deploying. If DT has already started W4 when .006 is done, .006 ships in a
      separate follow-up deploy. Coordinate with DT (0.4.0_DT_ClientPlatform) before
      they push PROD.
    </deploy_note>
  </cross_domain_coordination>
</task_order>
