# ADVI_REBORN.W3-004 — DS: Mismatch Root Cause Diagnosis + Fix

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-07-reborn-w3-004-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <project_code>ADVI_REBORN</project_code>
    <phase>WS3</phase>
  </metadata>

  <objective>
    For every mismatch found in W3-003: diagnose root cause (wrong S3 source, stale cache, computation divergence, type coercion loss). Write fix if in gold scripts.
  </objective>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_REBORN.W3-003" status="complete">Needs reconciliation matrix with mismatches</dependency>
  </dependencies>

  <commit_pattern>fix(gold): resolve data stream mismatches from reconciliation</commit_pattern>
</task_order>
