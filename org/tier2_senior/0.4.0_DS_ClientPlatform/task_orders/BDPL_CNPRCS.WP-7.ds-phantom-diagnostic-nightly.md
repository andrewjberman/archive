<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-bdpl-cnprcs-wp7</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>complete</status>
    <!-- CLOSED 2026-05-12 by 2.0.0_SA_COO per Andrew directive: bulk-close pending/unaddressed pre-May 2026 TOs. Inherits closure from parent project state or supersession. Re-author as new TO if work still required. -->
    <project_code>BDPL_CNPRCS</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/BD_CANONICAL_PRICES_CLASSIFICATION_REFACTOR.md (WP-7)</ref>
  </references>

  <objective>
    Permanent nightly phantom-valuation diagnostic.
    Script: `data/black_diamond/scripts/diagnostics/diag_phantom_valuations.py`.

    Scans gold/holdings_lots latest for:
      (cost_per_unit < $5) AND (current_price > $20) AND (price_quality = 'yahoo_equity')

    Cross-check against silver/bd_assets to confirm BD SuperClass is Fixed Income or
    To Be Classified (the phantom signature). Report committed to
    `data/black_diamond/diagnostics/phantom_scan_{YYYY-MM-DD}.md`.

    Runs nightly as part of the gold QC pass.
  </objective>

  <acceptance_criteria>
    1. First full-book scan committed
    2. Diagnostic wired into nightly gold QC pass (AE confirms cron/invocation)
    3. Post-WP-5: report returns 0 hits for 3 consecutive nights
    4. MCP COMPLETE to COO with first-scan output path
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io` on the diagnostic.
    Phase 2: `python -m py_compile`.
    Phase 3: Confirm in nightly QC pass.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="BDPL_ASTDIM.W4" status="staged" description="silver/bd_assets required for cross-check"/>
  </dependencies>

  <next>
    Can start parallel with WP-4 once BDPL_ASTDIM W4 lands. Feeds WP-5 acceptance gate.
  </next>
</task_order>
