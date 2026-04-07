# ADVI_REBORN.W4-001 — DS: Add roles to leaderboard data + per-role leaderboard files

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-07-reborn-w4-001-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <!-- Already implemented: D_00 employee_leaderboard.json includes roles[] per entry
         and all advisors across all 5 roles. Built from C_08 advisor_fee_detail.
         No code change needed -- shipped with the D_00 rewrite on 2026-04-07. -->
    <project_code>ADVI_REBORN</project_code>
    <priority>high</priority>
    <phase>WS4</phase>
  </metadata>

  <objective>
    Add role information to the employee leaderboard so the portal can filter
    by Architect/Implementor/Consultant/etc. Currently the leaderboard is
    architects-only with no role field on entries.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_REBORN_PRD.md</ref>
  </references>

  <context>
    Current state:
    - LeaderboardEntry (types.ts:864) has: rank, name, nna, aua_growth_pct, new_clients, aua, client_count, account_count — NO roles field
    - LeaderboardResponse.leaderboard_type is typed as 'architect' | 'implementor' but only architect data exists
    - Gold script C_08 already has per-advisor role data (roles array per advisor)
    - The fee_detail parquet has per-role breakdowns

    What the portal needs:
    - Each LeaderboardEntry must include a `roles: string[]` field (e.g., ["architect", "implementor"])
    - The leaderboard should include ALL advisors with any role, not just architects
    - Frontend will filter client-side using checkboxes
  </context>

  <requirements>
    <requirement id="1">Add `roles` field to each entry in the leaderboard JSON output. Each advisor gets their array of roles from the fee/assignment data.</requirement>
    <requirement id="2">Include ALL advisors with any advisory role in the leaderboard (not just architects). The portal will filter by role checkboxes.</requirement>
    <requirement id="3">Ensure leaderboard metrics (NNA, AUA, growth, clients) are still computed correctly when an advisor has multiple roles.</requirement>
    <requirement id="4">Commit and verify the output JSON has the roles field populated.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Every LeaderboardEntry in the JSON has a roles array</criterion>
    <criterion id="2">Advisors with implementor/consultant roles appear in the leaderboard</criterion>
    <criterion id="3">Existing architect metrics are unchanged</criterion>
  </acceptance_criteria>

  <commit_pattern>feat(REBORN): add roles to employee leaderboard data</commit_pattern>
</task_order>
