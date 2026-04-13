# ADVI_REBORN.W3-003 — DE+RD: Cross-Panel Reconciliation Matrix

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-07-reborn-w3-003-de-rd</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <!-- 2026-04-13 COO close-out (CTO memo, Andrew-directed cross-org reconciliation): DEPRECATED. Reconciliation happened organically during ADVI_PROFIL ship (portal-v2.1.39 / d2e78631). -->
    <project_code>ADVI_REBORN</project_code>
    <phase>WS3</phase>
  </metadata>

  <objective>
    Using the gold-truth reference from W3-002, verify every portal panel displays the exact matching number. Build the reconciliation matrix (metric x component). Flag every mismatch.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_REBORN_WS1_WS3_VALIDATION.md</ref>
  </references>

  <deliverable>Reconciliation matrix with pass/fail per cell for AUA, NNA, client_count, account_count across all 8 display locations.</deliverable>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_REBORN.W3-002" status="complete">Needs reference values</dependency>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_REBORN.W1-005" status="complete">Needs endpoint map</dependency>
  </dependencies>

  <commit_pattern>audit(REBORN): cross-panel reconciliation matrix</commit_pattern>
</task_order>
