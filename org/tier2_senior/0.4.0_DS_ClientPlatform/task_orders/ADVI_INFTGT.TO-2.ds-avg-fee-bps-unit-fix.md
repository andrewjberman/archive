<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFTGT.TO-2</id>
    <project>ADVI_INFTGT</project>
    <title>[P0] Fix avg_fee_bps_earned unit math — INF_D_04:2184 * 10000.0 → * 100</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>active</status>
    <priority>P0 — partner-blocking</priority>
    <authorized_by>Andrew direct GO 2026-05-11; PRD ADVI_INFTGT v0.1 (1.0.0_SA_CTO)</authorized_by>
  </metadata>

  <context>
    Peter Lee Advisor Public Profile shows "Avg Fee Rate: 10246 bps" — nonsensical.
    Root cause at INF_D_04.client_portal_summary.py:2184:
      `avg_fee_bps = round(float(avg_annual_fee_pct) * 10000.0, 1)`
    If upstream returns percent (e.g. 1.0246 meaning 1.0246%), multiply by 100 (not 10000)
    to get bps: 1.0246 * 100 = 102.46 bps (plausible for a ~1% fee advisor).
    PRD §4.2 + §5.2 confirms location. One-line fix.
  </context>

  <scope>
    <step>Phase 1 — Confirm: `comp-pipescript io INF_D_04`; `comp-blast build_advisor_summary`.
      Verify upstream `weighted_avg_annual_fee_pct` field units (percent or decimal fraction).
      Check with actual Peter Lee data: 10246 / 10000 = 1.0246% → plausible, confirms
      upstream is percent and multiplier should be * 100.</step>

    <step>Phase 2 — Fix: Change line 2184 from `* 10000.0` to `* 100`.
      Add sanity warn-log: `if avg_fee_bps > 1000: logger.warning(f"WARN: avg_fee_bps {avg_fee_bps:.1f} > 1000 for {advisor_key}")`.
      Emit null for fee fields when source is null or out-of-range (&gt; 1000 bps after fix = bug).</step>

    <step>Pre-commit gate: `.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_D_04.client_portal_summary.py`</step>

    <step>Local verify: run INF_D_04 standalone; check Peter Lee avg_fee_bps_earned is in 30–150 bps range.</step>

    <step>Commit + push + S3 deploy + comp-pipescript deployed MATCH.</step>

    <step>RAVC2 to COO with before/after value for Peter Lee avg_fee_bps_earned.</step>
  </scope>

  <acceptance_criteria>
    1. All four advisor profiles show avg_fee_bps_earned between 30 and 150 bps OR null (not 10000+).
    2. Sanity warn-log fires for any value &gt; 1000.
    3. Pre-commit gate exits 0.
    4. S3 deploy MATCH (comp-pipescript deployed).
    5. RAVC2 includes before/after Peter Lee value.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      `comp-pipescript io INF_D_04`
      `comp-blast build_advisor_summary`
    </phase>
    <phase id="2" when="before commit">
      `.tools/ds-commit-gate.sh` on INF_D_04.client_portal_summary.py
    </phase>
    <phase id="3" when="after commit">
      `comp-pipescript deployed INF_D_04` MATCH
      `comp-validate INF_D_04 --artifact /tmp/advisor_summary.json`
    </phase>
  </compiler_tools_mandate>
</task_order>
