# ADVI_REBORN.W3-002 — DS: Gold Truth Reference

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-07-reborn-w3-002-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <project_code>ADVI_REBORN</project_code>
    <phase>WS3</phase>
  </metadata>

  <objective>
    Produce exact gold-truth values for a specific date: AUA, NNA, client_count, account_count at firm level and for top 3 advisors. Write to gold/manifests/reconciliation_reference.json.
  </objective>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_REBORN.W1-002" status="complete">Needs validation script results to know which sources agree</dependency>
  </dependencies>

  <commit_pattern>feat(gold): reconciliation reference for portal validation</commit_pattern>
</task_order>
