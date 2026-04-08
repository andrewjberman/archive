# ADVI_REBORN.W1-002 — DS: Cross-Script Validation Script

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-07-reborn-w1-002-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <project_code>ADVI_REBORN</project_code>
    <phase>WS1</phase>
  </metadata>

  <objective>
    Write E_20.cross_script_validation.py. For every metric (AUA, NNA, client_count, account_count, fee_bps, growth), read the latest output of every script that produces it. Compare firm-level values. Report any discrepancy > $1.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_REBORN_WS1_WS3_VALIDATION.md</ref>
  </references>

  <deliverable>data/black_diamond/scripts/gold/E_20.cross_script_validation.py</deliverable>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_REBORN.W1-001" status="complete">Needs manifest to know which scripts to compare</dependency>
  </dependencies>

  <commit_pattern>feat(gold): E_20 cross-script validation</commit_pattern>
</task_order>
