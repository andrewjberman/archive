<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-office-w5</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>ADVI_OFFICE</project_code>
  </metadata>

  <references>
    <ref type="prd_addendum">docs/architecture/ADVI_OFFICE_ADDENDUM.md</ref>
    <ref type="source">data/black_diamond/scripts/gold/D_00b.portal_timeseries.py</ref>
    <ref type="blocking_from">ADVI_OFFICE.W1 — D_00b fix #3 still outstanding</ref>
  </references>

  <objective>
    Fix D_00b's _build_rel_office_dim_d00b so the OFC stacked timeseries in
    timeseries_chart.json shows 10 offices instead of collapsing all 178 advisors
    to a single "Other" bucket. This unblocks the Continuous AUA and Continuous NNA
    charts for the OFC cohort in the portal.

    Also verify D_01's distribution.total for the OFC period view — this powers the
    bell curve at L0 (no office selected). Confirm it's non-empty after the fix runs.
  </objective>

  <context>
    Fix #1 and #2 (crashes) were resolved in commit 15512bed. Fix #3 is the remaining gap:
    the _build_rel_office_dim_d00b function at D_00b line 248 uses modal office aggregation
    (groupby relationship_id, mode office). Something in the account_team join or the
    account_office_dim lookup is causing all relationships to resolve to 'Other' or a single
    bucket.

    The continuous chart in the portal (OFC cohort, View=Continuous) currently shows:
    - AUA: "No chart data available" (filteredChartData empty — data?.ofc is null/empty)
    - NNA: "No NNA advisor data available" (nna_ofc data empty or malformed)

    D_01 has been verified as correct: build_ofc_view emits distribution.total and
    distribution.by_segment per period. The only data-layer gap is D_00b fix #3.

    After fixing and uploading D_00b, MCP-signal 0.6.0_AE_PartnerETL with commit hash
    and S3 upload confirmation to trigger W7 gold re-run.

    comp-validate context: set before running validation:
    printf "SERIAL=0.4.0_DS_ClientPlatform\nTO_ID=ADVI_OFFICE.W5\n" > .comp-graph/.agent_context
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing:
      <run>comp-pipescript io D_00b --no-portal</run>
      <expect>S3-DYNAMIC READS section shows dim_advisor_office.csv. WRITES shows TIMESERIES_CHART.</expect>
      <if_mismatch>If dim_advisor_office.csv absent from S3-DYNAMIC, the dim is not being loaded at runtime — check the load path in D_00b around line 1170</if_mismatch>

      <run>comp-pipescript postdeps D_00b</run>
      <expect>Precondition: gold/dimensions/dim_advisor_office.csv must exist on S3 (BLOCKING)</expect>
      <if_mismatch>If dim not on S3, upload it before running — AE W2 should have done this already; verify with aws s3 ls s3://opal-data-bd/gold/dimensions/dim_advisor_office.csv</if_mismatch>

    Phase 2 — before uploading to S3:
      Run a local dry-run with the fixed script. Validate output:
      <run>comp-validate D_00b --artifact /tmp/timeseries_chart.json</run>
      <expect>No configured checks for D_00b currently, but manually verify: top-level 'ofc' key present; ofc.categories has >= 5 office names (not just 'Other'); ofc.data array has >= 30 entries</expect>
      <if_mismatch>If ofc.categories is ['Other'] or empty, fix #3 is still not working — check the join between account_team and account_office_dim at D_00b line 1170</if_mismatch>

    Phase 3 — after AE W7 gold run confirms:
      Append row to org/compiler-tools-log.md (auto-logged by comp-* wrapper if context is set).
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>gold/artifacts/timeseries_chart.json</shared_resource>
    <shared_resource>platinum/firm/cumulative_chart.json</shared_resource>
    <also_in_to>ADVI_OFFICE.W7 (AE — gold run triggered after this fix ships)</also_in_to>
    <also_in_to>ADVI_OFFICE.W6 (DE — bell curve and continuous chart gated on this data)</also_in_to>
    <required_action>
      After committing and uploading D_00b, MCP-message 0.6.0_AE_PartnerETL:
      "ADVI_OFFICE W5 ready — D_00b fix #3 complete. Commit: {hash}. S3 upload confirmed.
      Please trigger W7 gold run (D_00b → D_04 chain). OFC timeseries fix."
    </required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. timeseries_chart.json top-level 'ofc' key present with categories list >= 5 office names
       (not just ['Other'] or a single bucket)
    2. timeseries_chart.json 'nna_ofc' key present with categories list >= 5 office names
    3. After W7 gold run: platinum/firm/cumulative_chart.json 'ofc' key present with data
    4. After W7 gold run: portal Continuous AUA + OFC shows stacked area chart (not "No chart data")
    5. comp-pipescript deployed D_00b shows MATCH before triggering W7
    6. Session log includes: (a) root cause of the _build_rel_office_dim_d00b bug,
       (b) dry-run spot-check showing categories list, (c) MCP signal to AE
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/D_00b.portal_timeseries.py</file>
    </files>
    <out_of_scope>
      D_01 (already correct — verified). Frontend (DE W6). Gold run trigger (AE W7).
    </out_of_scope>
  </scope>

  <deliverables>
    - Commit D_00b fix to CLOUD with DS author
    - Upload D_00b to S3 (build-and-upload.sh or direct cp)
    - MCP message to 0.6.0_AE_PartnerETL with commit hash + S3 upload + W7 GO
    - Session log with compiler tools section + root cause + dry-run validation
  </deliverables>
</task_order>
