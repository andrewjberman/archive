<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-ofc-l2-advisor-distribution</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>pending</status>
    <project_code>ADVI_OFFICE</project_code>
  </metadata>

  <references>
    <ref type="diagnosis">DE message 20260414T170700Z — OFC L2 advisor distribution for bell curve</ref>
    <ref type="function">D_01.partner_analytics.py line 549 — calculate_distribution_stats()</ref>
  </references>

  <objective>
    Add per-advisor AUA distribution stats to platinum/advisors/{slug}/summary.json so that
    when an advisor is selected in the OFC L1 advisor list, the bell curve updates to show
    that advisor's account AUA distribution. Frontend is already wired (selectedAdvisorKey
    state, clickable advisor rows).
  </objective>

  <context>
    Andrew's UX spec: OFC L1 advisor list → click advisor → bell curve shows that
    advisor's distribution (not the office aggregate).

    D_01 already has calculate_distribution_stats() (line 549) — log-spaced histogram,
    same bell curve shape used for GEO/OFC firm-level distributions.

    Current platinum/advisors/{slug}/summary.json has: book.clients, tax_exposure,
    mix_periods, role_breakdown, etc. Does NOT have a distribution field.

    Recommended path: add distribution computation to D_03 (which produces per-advisor
    platinum summaries). For each advisor, compute calculate_distribution_stats() over
    their account AUA values (accounts where they have any role). Write as
    summary.distribution = {total: {...histogram...}} at the top level.

    D_04 then passes the updated D_03 output through to platinum unchanged.

    The frontend will look up summary.distribution.total when an advisor is selected in
    OFC L1 (DE adds the one lookup branch after this ships).
  </context>

  <scope>
    <file>data/black_diamond/scripts/gold/D_03.composition_artifacts.py (or equivalent advisor summary script)</file>
    <change>
      1. Run comp-pipescript io on D_03 to confirm it produces per-advisor platinum summaries
         and has access to account-level AUA data needed for distribution computation.

      2. For each advisor, compute:
           distribution = calculate_distribution_stats(advisor_account_aua_series)
           where advisor_account_aua_series = total_aua for accounts where advisor has any role.

      3. Add to the advisor summary dict:
           'distribution': {'total': distribution}

      4. If D_03 does not have account-level AUA access, check whether the distribution
         can be derived from data available at D_03 runtime, or whether D_01's
         account_performance.parquet read should be reused. Report to COO if the
         implementation path differs from above before coding.
    </change>
  </scope>

  <compiler_tools_mandate>
    <phase name="before_write">
      Set context: printf "SERIAL=0.4.0_DS_ClientPlatform\nTO_ID=ofc-l2-advisor-distribution\n" > .comp-graph/.agent_context
      <run>comp-pipescript io D_03.composition_artifacts.py</run>
      <expect>platinum/advisors/{slug}/summary.json in WRITES; confirm account AUA data available at runtime</expect>
      If account-level AUA is NOT in D_03 scope, report to COO before implementing.
    </phase>
    <phase name="before_commit">
      <run>py_compile {modified script}</run>
      <expect>No syntax errors</expect>
      Spot-check: platinum/advisors/travis_penfield/summary.json has distribution.total.histogram
    </phase>
    <phase name="after_upload">
      MCP to 0.6.0_AE_PartnerETL with GO for D_03+D_04 re-run.
      MCP to 0.4.0_DE_ClientPlatform: distribution field shape confirmed, add lookup branch.
      MCP to 2.0.0_SA_COO.
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>platinum/advisors/{slug}/summary.json</shared_resource>
    <also_in_to>AE D_03+D_04 re-run (stage after DS upload)</also_in_to>
    <also_in_to>DE: one-line lookup branch in OFC L1 click handler (after AE confirms field live)</also_in_to>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. platinum/advisors/travis_penfield/summary.json has distribution.total (histogram, count, total, mean, median).
    2. Distribution values are plausible (Travis has ~X accounts, histogram bins make sense for his AUA range).
    3. py_compile passes.
    4. MCP to AE (D_03+D_04 re-run GO), DE (shape confirmed), COO.
    5. Session log.
  </acceptance_criteria>

  <deliverables>
    - Modified gold script committed.
    - Script uploaded to S3.
    - MCP to AE, DE, COO.
    - Session log.
  </deliverables>
</task_order>
