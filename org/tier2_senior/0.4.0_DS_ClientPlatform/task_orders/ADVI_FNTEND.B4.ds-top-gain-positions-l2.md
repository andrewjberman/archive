<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-advi-fntend-b4-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>pending</status><!-- GO sent 2026-04-14T21:30Z Wave A parallel dispatch -->
    <project_code>ADVI_FNTEND</project_code>
    <wave>A</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 4: B6)</ref>
  </references>

  <objective>
    Populate `top_gain_positions` on advisor-summary (L2).
    Client-summary (L3) — type exists via `clientDetail.tax.top_gain_positions`, but artifact population NOT verified (flagged by RD audit 2026-04-14). Verify + expand scope if empty.
  </objective>

  <acceptance_criteria>
    1. Advisor-summary artifacts have top_gain_positions populated (not [])
    2. **Refined 2026-04-14 per RD audit + CTO ratification:** top_gain_positions is non-empty on ≥95% of open advisor-summaries with taxable activity (type-present != data-present)
    3. Spot-check 3 client-summary artifacts — top_gain_positions non-empty. If empty, expand this TO's scope to cover L3 emission before COMPLETE.
    4. MCP COMPLETE to COO with L2 + L3 population status + coverage % against taxable-activity denominator
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io` on advisor-summary writer to confirm top_gain_positions plumbed; `comp-platinum reverse top_gain_positions` (confirm AdvisorBookView is the sole consumer at L2).
    Phase 2: `python -m py_compile`.
    Phase 3: `comp-validate` after rerun.
  </compiler_tools_mandate>

  <dependencies>
    <none/>
  </dependencies>
</task_order>
