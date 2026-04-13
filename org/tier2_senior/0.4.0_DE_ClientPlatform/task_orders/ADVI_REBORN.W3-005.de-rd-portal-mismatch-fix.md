# ADVI_REBORN.W3-005 — DE+RD: Portal-Side Mismatch Fixes

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-07-reborn-w3-005-de-rd</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <!-- 2026-04-13 COO close-out (CTO memo, Andrew-directed cross-org reconciliation): DEPRECATED. Resolved in ADVI_PROFIL Wave 1/2/3 (portal-v2.1.39 / d2e78631). -->
    <project_code>ADVI_REBORN</project_code>
    <phase>WS3</phase>
  </metadata>

  <objective>
    Fix any portal-side mismatches found in W3-003: wrong endpoint, wrong field, formatting loss, stale type casting.
  </objective>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_REBORN.W3-003" status="complete">Needs reconciliation matrix</dependency>
  </dependencies>

  <commit_pattern>fix(portal): resolve data stream mismatches from reconciliation</commit_pattern>
</task_order>
