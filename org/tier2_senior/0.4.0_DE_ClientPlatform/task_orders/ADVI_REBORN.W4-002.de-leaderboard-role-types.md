# ADVI_REBORN.W4-002 — DE: Add roles to LeaderboardEntry type + filter support

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-07-reborn-w4-002-de</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <!-- 2026-04-13 COO close-out (CTO memo, Andrew-directed cross-org reconciliation): DEPRECATED. Leaderboard typing rebuilt in ADVI_PROFIL AdvisorsTab rewrite (portal-v2.1.39 / d2e78631). -->
    <project_code>ADVI_REBORN</project_code>
    <priority>high</priority>
    <phase>WS4</phase>
  </metadata>

  <objective>
    Update LeaderboardEntry type to include roles, and add a role filter type
    for the frontend checkboxes.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_REBORN_PRD.md</ref>
  </references>

  <scope>
    1. Update LeaderboardEntry (types.ts:864) — add `roles: string[]`
    2. Add AdvisorRole type: `type AdvisorRole = 'architect' | 'implementor' | 'consultant' | 'solicitor'` (or whatever roles exist in the data — confirm with DS)
    3. Update LeaderboardResponse.leaderboard_type to reflect it now includes all roles
    4. Run bunx tsc -b, fix any errors
  </scope>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_REBORN.W4-001" status="complete">DS must add roles to leaderboard JSON first</dependency>
  </dependencies>

  <commit_pattern>feat(REBORN): add roles to LeaderboardEntry type</commit_pattern>
</task_order>
