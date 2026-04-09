<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-49push-006-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-08</date>
    <status>pending -- BLOCKED on .005 (AE deploy)</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>2</wave>
    <phase>P1</phase>
    <mcp_identity>Register with MCP as "0.4.0_DS_ClientPlatform~A" (not the base serial). This is your instance ID for this session. Use it for register_agent, heartbeat, and inbox-watch.</mcp_identity>
  </metadata>

  <objective>
    Validate the platinum/ output produced by D_04 on the gold runner. Spot-check
    10 advisors, 50 clients, and 100 accounts to verify data accuracy and number
    consistency against gold/ source files.
  </objective>

  <context>
    D_04 has been deployed and run by AE (.005). The platinum/ prefix in opal-data-bd
    now contains ~5,300 pre-sliced JSON files. This TO validates that the output is correct.

    PRD: docs/architecture/ADVI_49PUSH_P1_PRD.md (section: Number Consistency Principle)

    BLOCKED: Do NOT begin until AE (0.6.0_AE_PartnerETL) confirms .005 is complete.
    Check your inbox for the GO signal, or check agent status for AE's summary.
  </context>

  <compiler_tools_mandate>
    Use comp-pipescript to verify D_04's I/O matches what was deployed:

    1. comp-pipescript io D_04
       -- verify D_04's reads and writes match the script design

    2. comp-pipescript consumers D_04
       -- should be empty (D_04 is terminal, no other script reads platinum/)
  </compiler_tools_mandate>

  <requirements>
    <requirement id="1">
      Download and inspect platinum/ files from S3 (opal-data-bd bucket):
      - platinum/firm/dashboard.json -- verify all sections present (leaderboard, clients_tab, fee_efficiency)
      - platinum/firm/mix_summary.json -- verify mix snapshot + quarterly bars
    </requirement>

    <requirement id="2">
      ADVISOR SPOT-CHECK (10 advisors):
      For 10 advisors, compare platinum/advisors/{id}/summary.json against:
      - gold/entities/advisors/{id}/book.json (D_02) -- client list, AUA, NNA
      - gold/entities/advisors/{id}/mix.json (D_03) -- mix data
      - gold/entities/advisors/{id}/composition.json (D_03) -- composition
      Verify fields match. Document any discrepancies.
    </requirement>

    <requirement id="3">
      CLIENT SPOT-CHECK (50 clients):
      For 50 clients, compare platinum/clients/{rel_id}/summary.json against:
      - gold/entities/clients/{rel_id}/detail.json (D_02)
      - gold/entities/clients/{rel_id}_composition.json (D_03)
      - gold/entities/clients/{rel_id}_views.json (C_06)
      Verify fields match. Check fee_summary section against fee_rate_history.parquet.
    </requirement>

    <requirement id="4">
      ACCOUNT SPOT-CHECK (100 accounts):
      For 100 accounts, verify platinum/accounts/{acct_id}/summary.json contains valid
      3-class mix + top holdings. Cross-reference against holdings_lots parquet if feasible.
    </requirement>

    <requirement id="5">
      NUMBER CONSISTENCY CHECK (the critical test):
      - Firm total_aua in dashboard.json = sum of all advisor summary total_aua values
      - Each advisor total_aua = sum of their clients' total_aua values
      - Firm NNA = sum of advisor NNA values
      Document exact numbers and any rounding discrepancies (tolerance: <$1).
    </requirement>

    <requirement id="6">
      TIMESERIES SPOT-CHECK:
      For 5 clients, compare platinum/clients/{rel_id}/mix_timeseries.json and
      concentration.json against the C_06 full envelope (gold/entities/clients/{rel_id}.json).
      Verify daily values match for sampled dates.
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>Validation report: docs/briefs/ADVI_49PUSH_P1_validation_report.md</deliverable>
    <deliverable>Number consistency results (pass/fail with exact figures)</deliverable>
    <deliverable>Message to COO (2.0.0_SA_COO) with summary: pass/fail + any issues found</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT begin validation until .005 (AE deploy) is confirmed complete</rule>
    <rule>Do NOT modify D_04 -- if you find bugs, report them for a separate fix TO</rule>
    <rule>Do NOT validate by re-running D_04 locally -- validate the deployed S3 output</rule>
  </do_not>
</task_order>
