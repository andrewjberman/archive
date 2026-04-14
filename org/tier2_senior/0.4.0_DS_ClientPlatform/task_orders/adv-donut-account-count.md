<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-adv-donut-account-count</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>complete</status>
    <project_code></project_code>
  </metadata>

  <references>
    <ref type="diagnosis">RD message 20260414T170700Z — ADV donut segments missing account_count</ref>
    <ref type="pattern">D_01.partner_analytics.py line 879 — GEO .027 Issue 1 account_count fix</ref>
  </references>

  <objective>
    Add account_count to each ADV donut segment in D_01.partner_analytics.py.
    Frontend (getRadialCount on DonutSegment) is already wired — data fix only,
    no portal changes needed.
  </objective>

  <context>
    RD diagnosis confirmed by COO code read:
    - GEO segments (line 879): have account_count + client_count (added in .027 Issue 1)
    - OFC segments: have account_count (from OfcAdvisorListPanel data shape)
    - ADV segments (lines 1015-1026): have relationship_count + pct_of_firm_clients but NOT account_count

    Frontend: getRadialCount reads DonutSegment.account_count. When null, falls back to
    client_count — which is actually relationship_count, so "# Accounts" label shows wrong
    number. Fix: emit account_count = unique accounts managed by that advisor.

    Pattern to follow: GEO .027 Issue 1 (line 879):
      'account_count': int(row['account_count']),  # unique accounts in that state
      'client_count':  int(row['account_count']),  # kept for backward compat

    Apply the equivalent to ADV segments — account_count = unique accounts where
    this advisor has a role (same account scope as the advisor's tagged AUA).
  </context>

  <scope>
    <file>data/black_diamond/scripts/gold/D_01.partner_analytics.py</file>
    <change>
      In the ADV segment construction block (around lines 1015-1061),
      add account_count to each segment dict alongside existing relationship_count.

      account_count = unique account_ids managed by that advisor
      (use the same account scope as the AUA computation for that segment).

      Follow the GEO pattern (line 879) exactly — keep relationship_count for
      backward compat, add account_count as the correct unique-account count.

      Also add account_count to the "Other" catchall segment (if present),
      summing account_counts of collapsed segments (same pattern as GEO line 893).
    </change>
  </scope>

  <compiler_tools_mandate>
    <phase name="before_write">
      Set context: printf "SERIAL=0.4.0_DS_ClientPlatform\nTO_ID=adv-donut-account-count\n" > .comp-graph/.agent_context
      <run>comp-pipescript io D_01.partner_analytics.py</run>
      <expect>ADV segment dict in WRITES section; account_count not currently in output fields</expect>
    </phase>
    <phase name="before_commit">
      <run>py_compile data/black_diamond/scripts/gold/D_01.partner_analytics.py</run>
      <expect>No syntax errors</expect>
    </phase>
    <phase name="after_upload">
      MCP to 0.6.0_AE_PartnerETL with S3 ETag (GO for AE D_01+D_04 re-run TO).
      MCP to 2.0.0_SA_COO.
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>s3://opal-data-bd/gold/artifacts/partner_analytics*.json</shared_resource>
    <also_in_to>adv-donut-account-count-ae (AE — D_01+D_04 re-run after this upload)</also_in_to>
    <required_action>
      After commit + S3 upload, MCP 0.6.0_AE_PartnerETL with GO signal and ETag.
    </required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. ADV donut segments in partner_analytics artifacts contain account_count field.
    2. account_count is a positive integer (unique account count, not relationship count).
    3. py_compile passes.
    4. D_01 uploaded to S3 — ETag confirmed.
    5. MCP to AE + COO.
    6. Session log.
  </acceptance_criteria>

  <deliverables>
    - D_01.partner_analytics.py modified and committed.
    - D_01 uploaded to S3.
    - MCP to 0.6.0_AE_PartnerETL (AE re-run GO) and 2.0.0_SA_COO.
    - Session log.
  </deliverables>
</task_order>
