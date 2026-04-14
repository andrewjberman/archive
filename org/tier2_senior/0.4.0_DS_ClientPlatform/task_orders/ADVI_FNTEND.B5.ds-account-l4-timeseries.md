<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-advi-fntend-b5-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>ADVI_FNTEND</project_code>
    <wave>A</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 5: B9)</ref>
  </references>

  <objective>
    Add account-level inception-to-date timeseries under `PlatinumAccountSummary`
    (AUA + flows, same `*_canonical` convention as advisor lifetime activity).
  </objective>

  <acceptance_criteria>
    1. Account summary artifacts have timeseries array
    2. Fields mirror advisor Lifetime Activity (aua_canonical, nna_canonical, inflows_canonical, outflows_canonical, date)
    3. MCP COMPLETE to COO
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io` on account-summary writer.
    Phase 2: `python -m py_compile`.
    Phase 3: `comp-validate`.
  </compiler_tools_mandate>

  <dependencies>
    <none/>
  </dependencies>
</task_order>
