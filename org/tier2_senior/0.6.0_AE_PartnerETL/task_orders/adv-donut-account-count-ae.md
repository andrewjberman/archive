<task_order>
  <metadata>
    <id>0.6.0_AE_PartnerETL-2026-04-14-adv-donut-account-count</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-14</date>
    <status>complete</status>
    <!-- CLOSED 2026-05-12 by 2.0.0_SA_COO per Andrew directive: bulk-close pending/unaddressed pre-May 2026 TOs. Inherits closure from parent project state or supersession. Re-author as new TO if work still required. -->
    <project_code></project_code>
  </metadata>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform"
                task="adv-donut-account-count"
                status="pending"
                description="DS commits D_01 change + uploads to S3. MCP GO signal with ETag triggers this TO."/>
  </dependencies>

  <objective>
    Re-run D_01 + D_04 on QA runner after DS adds account_count to ADV donut segments.
    Verify platinum partner_analytics artifacts contain account_count on ADV segments.
    No portal deploy needed — frontend already handles it.
  </objective>

  <context>
    D_01 produces partner_analytics gold artifacts. D_04 passes them through to platinum.
    Both must re-run to push the account_count addition to platinum.
    Run order: D_01 first, then D_04.
    All upstream data (silver, account_performance) is current from today's runs.
    QA runner: bd-gold-qa-runner (i-0090b823a4a0997e3, AutoShutdown=disabled).
    Can run locally --upload if QA runner has capacity constraints (same as W9b pattern).
  </context>

  <scope>
    1. Verify D_01 ETag matches DS upload before running.
    2. Run D_01 on QA runner (or locally --upload).
    3. Run D_04 on QA runner (or locally --upload).
    4. Spot-check: verify account_count present on ADV segments in platinum artifact:
       aws s3 cp s3://opal-data-bd/platinum/firm/partner_analytics_quarterly.json - |
         python -c "import sys,json; d=json.load(sys.stdin); seg=d['views']['adv']['current']['donut']['segments'][0]; print('account_count:', seg.get('account_count','MISSING'))"
       Expected: positive integer (not MISSING, not null).
  </scope>

  <compiler_tools_mandate>
    <phase name="before_run">
      Set context: printf "SERIAL=0.6.0_AE_PartnerETL\nTO_ID=adv-donut-account-count-ae\n" > .comp-graph/.agent_context
      <run>comp-pipescript deployed D_01.partner_analytics.py</run>
      <expect>MATCH — DS ETag on S3 must match before running</expect>
    </phase>
    <phase name="after_run">
      Spot-check account_count on ADV segment (command above).
      MCP to 2.0.0_SA_COO: "ADV account_count live in platinum."
      MCP to 0.4.2_RD_AdvisorIntelligence: "ADV account_count live — donut subtext fix deployed."
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <required_action>Do not overlap with any other D_01 or D_04 run. Confirm QA runner is idle.</required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. D_01 + D_04 exit 0.
    2. platinum/firm/partner_analytics_quarterly.json ADV segment has account_count as positive integer.
    3. MCP to COO + RD confirming live.
    4. Session log.
  </acceptance_criteria>

  <deliverables>
    - D_01 + D_04 re-run complete.
    - ADV account_count confirmed in platinum.
    - MCP to COO + RD.
    - Session log.
  </deliverables>
</task_order>
