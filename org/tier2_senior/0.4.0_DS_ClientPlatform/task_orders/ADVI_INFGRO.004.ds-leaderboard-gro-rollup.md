<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFGRO.004</id>
    <project>ADVI_INFGRO</project>
    <title>Extend INF_D_00c.portal_leaderboard — emit AUA-weighted GRO rollups per advisor + firm</title>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_note>Receiver routing TBD — COO bench-state check 2026-05-12 morning. DS~A + DS~C killed or STANDDOWN 2026-05-11 ~22:31Z. Do NOT pick up this TO until COO issues GO.</dispatch_note>
    <priority>P0</priority>
    <estimated_effort>2-3 hours</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFGRO_PRD.md §4.5 + §6.TO-INFGRO.004</ref>
    <ref type="script">data/orion/scripts/gold/INF_D_00c.portal_leaderboard.py</ref>
    <ref type="current_input">gold/timeseries/client_performance.parquet (extended by TO-003)</ref>
    <ref type="current_output">platinum/firm/leaderboard.json</ref>
    <ref type="blast">INF_D_00c has NO downstream script consumers (comp-blast result — terminal producer). Portal reads directly.</ref>
    <ref type="gates">TO-INFGRO.003 COMPLETE — DS~A MCP-self-signals that client_performance.parquet includes new 5 columns.</ref>
  </references>

  <context>
    INF_D_00c.portal_leaderboard reads gold/timeseries/client_performance.parquet and
    produces platinum/firm/leaderboard.json consumed by the portal's AdvisorsTab.

    After TO-003, client_performance.parquet will include nna_$, return_pct_twr, return_$,
    epsilon_$, epsilon_data_quality per (client, period). INF_D_00c must aggregate these
    to per-advisor + firm-level rollups and emit them in leaderboard.json.

    INF_D_00c has NO downstream script consumers (comp-blast confirmed). Its output goes
    directly to the portal. Extension is safe — additive new fields in leaderboard.json.

    AUA-weighted rollup math for return_pct_twr:
      advisor.return_pct_twr = Σ(client.return_pct_twr × client.aua_start) / Σ(client.aua_start)
    NNA and epsilon sum directly (dollar amounts, not percentages).
  </context>

  <scope>
    <step>
      Read INF_D_00c.portal_leaderboard.py in full.
      Understand: how it reads client_performance.parquet, how per-advisor aggregation
      currently works, what fields are currently emitted per advisor in leaderboard.json,
      and what the JSON schema looks like for an advisor entry.
    </step>
    <step>
      Read current platinum/firm/leaderboard.json (sample) to understand the existing schema.
      Confirm that new fields will be additive (no existing field renamed or removed).
    </step>
    <step>
      Extend the aggregation step to compute, per advisor:
        - advisor_nna_$ = Σ(client.nna_$) for all clients under advisor [simple sum]
        - advisor_return_pct_twr = Σ(client.return_pct_twr × client.aua_start) / Σ(client.aua_start)
                                   [AUA-weighted; exclude clients where return_pct_twr is null]
        - advisor_return_$ = Σ(client.return_$) [sum; null-safe]
        - advisor_epsilon_$ = Σ(client.epsilon_$) [sum; null-safe]
      And at firm level:
        - firm_nna_$ = Σ(advisor_nna_$)
        - firm_return_pct_twr = Σ(advisor.return_pct_twr × advisor.aua_start) / Σ(advisor.aua_start)
        - firm_return_$ = Σ(advisor_return_$)
        - firm_epsilon_$ = Σ(advisor_epsilon_$)
    </step>
    <step>
      Emit the new fields in leaderboard.json under each advisor entry AND in the
      firm-level section. Preserve all existing fields unchanged.
    </step>
    <step>
      Spot-check Peter Lee: manually verify advisor_return_pct_twr matches
      AUA-weighted average of Peter's clients' twr values in client_performance.parquet.
    </step>
    <step>
      Pre-commit gate: `.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_D_00c.portal_leaderboard.py`
      Then safe-deploy + comp-pipescript deployed MATCH.
    </step>
  </scope>

  <compiler_tools_mandate>
    <phase name="before_write">
      - comp-pipescript io INF_D_00c (confirm reads client_performance + writes leaderboard.json)
      - comp-blast INF_D_00c (confirm no downstream script consumers)
      - comp-platinum reverse leaderboard.json (identify portal consumer — AdvisorsTab.tsx)
    </phase>
    <phase name="before_commit">
      - .tools/ds-commit-gate.sh INF_D_00c.portal_leaderboard.py (EXIT 0 required)
    </phase>
    <phase name="after_commit">
      - comp-pipescript deployed INF_D_00c (MATCH required)
      - Sample leaderboard.json read — confirm new fields present for all 4 advisors
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    Upstream: DS~A TO-INFGRO.003 must complete first (client_performance.parquet extended).
    This is same-lane (DS~A) so no MCP coordination needed — complete sequentially.

    Downstream: DE TO-INFGRO.005 (portal rendering) reads leaderboard.json.
    MCP DE when platinum/firm/leaderboard.json is confirmed on S3 with new fields.
    DE must NOT start TO-005 until this TO signals RAVC2-complete with leaderboard.json
    sample confirming per-advisor GRO fields present.
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion id="AC1">platinum/firm/leaderboard.json per-advisor entries include new fields:
      advisor_nna_$, advisor_return_pct_twr, advisor_return_$, advisor_epsilon_$.</criterion>
    <criterion id="AC2">Firm-level section includes: firm_nna_$, firm_return_pct_twr, firm_return_$, firm_epsilon_$.</criterion>
    <criterion id="AC3">AUA-weighted Peter Lee spot-check: advisor_return_pct_twr matches manual
      Σ(client_twr × client_aua_start) / Σ(client_aua_start) within 0.01% tolerance.</criterion>
    <criterion id="AC4">All pre-existing leaderboard.json fields unchanged (spot-check 3 existing fields).</criterion>
    <criterion id="AC5">comp-pipescript deployed MATCH.</criterion>
    <criterion id="AC6">Pre-commit gate PASS.</criterion>
  </acceptance_criteria>

  <session_log_requirement>
    Session log in org/tier2_senior/0.4.0_DS_ClientPlatform/logs/{date}/
    Include Compiler Tools section + Peter Lee spot-check values.
    MCP DE with leaderboard.json sample path + new field list when complete.
  </session_log_requirement>
</task_order>
