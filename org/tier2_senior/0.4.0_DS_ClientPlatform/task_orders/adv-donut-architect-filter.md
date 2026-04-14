<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-adv-donut-architect-filter</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>complete</status>
    <project_code></project_code>
  </metadata>

  <references>
    <ref type="diagnosis">DE message 20260414T170700Z — Alex Bright (local_ops primary) appearing in top-9 ADV donut</ref>
  </references>

  <objective>
    Filter D_01 ADV donut segment selection to primary_role === 'architect' advisors only.
    Top-9 should show architects by AUA, not any advisor who happens to be tagged as
    architect on a few accounts.
  </objective>

  <context>
    D_01 builds ADV donut by grouping account AUA by the 'architect' field (rel_arch_lookup,
    line 993). This produces top-9 by AUA across all people tagged as architect on any account.
    An advisor whose primary role is local_ops (e.g. Alex Bright) can appear if they are
    the architect on enough accounts. Andrew's UX intent: ADV donut = top 9 people whose
    PRIMARY role is architect.

    primary_role source: either derive from role_breakdown in the leaderboard (D_00c output),
    or compute inline in D_01 from the account_team/role data available at build time.
    Recommended: look up primary_role from the leaderboard artifact if D_00c runs before D_01,
    or derive from ROLE_COLS (line 929) by finding which role has highest AUA per advisor.

    After filtering, the "Other" catchall bucket should still aggregate remaining architects
    that don't make the top-9 cutoff — not non-architects.
  </context>

  <scope>
    <file>data/black_diamond/scripts/gold/D_01.partner_analytics.py</file>
    <change>
      In the ADV donut segment construction (around lines 1040-1075):
      Before top-9 AUA selection, filter the advisor set to those whose
      primary_role is 'architect'. Derive primary_role by identifying which
      role column (architect/implementor/consultant/local_ops/additional_advisor)
      has highest total AUA for each advisor from the available role data.

      The Other bucket should contain only architects outside the top-9,
      not non-architect advisors filtered out.
    </change>
  </scope>

  <compiler_tools_mandate>
    <phase name="before_write">
      Set context: printf "SERIAL=0.4.0_DS_ClientPlatform\nTO_ID=adv-donut-architect-filter\n" > .comp-graph/.agent_context
      <run>comp-pipescript io D_01.partner_analytics.py</run>
      <expect>views.adv in WRITES; confirm where role data is available at ADV segment construction time</expect>
    </phase>
    <phase name="before_commit">
      <run>py_compile data/black_diamond/scripts/gold/D_01.partner_analytics.py</run>
      <expect>No syntax errors</expect>
      Spot-check: verify Alex Bright is NOT in views.adv segments, verify Travis Penfield IS.
    </phase>
    <phase name="after_upload">
      MCP to 0.6.0_AE_PartnerETL with S3 ETag — AE bundles this with adv-donut-account-count-ae
      D_01+D_04 re-run if the account_count fix runs first, or triggers a new run.
      MCP to 2.0.0_SA_COO.
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>s3://opal-data-bd/gold/artifacts/partner_analytics*.json</shared_resource>
    <note>
      If adv-donut-account-count D_01 change is already uploaded but AE has not yet run,
      bundle this fix into the same D_01 file before uploading — do not create two separate
      D_01 S3 uploads. Coordinate with AE timing.
    </note>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. views.adv donut segments contain only advisors with primary_role === 'architect'.
    2. Alex Bright NOT in top-9 ADV segments (or Other bucket only if still an architect).
    3. Travis Penfield, and other known primary architects, still appear correctly.
    4. py_compile passes.
    5. D_01 uploaded to S3, MCP to AE + COO.
    6. Session log.
  </acceptance_criteria>

  <deliverables>
    - D_01.partner_analytics.py modified and committed.
    - D_01 uploaded to S3.
    - MCP to 0.6.0_AE_PartnerETL + 2.0.0_SA_COO.
    - Session log.
  </deliverables>
</task_order>
