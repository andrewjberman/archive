# ADVI_REBORN.W4-003 — RD: Role filter checkboxes on employee leaderboard

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-07-reborn-w4-003-rd</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <!-- Completed 2026-04-07. Portal DEV commit b6db90b. Role checkboxes with 44px targets, color-coded, filtering all views. -->
    <project_code>ADVI_REBORN</project_code>
    <priority>high</priority>
    <phase>WS4</phase>
  </metadata>

  <objective>
    Add role filter checkboxes to the AdvisorsTab leaderboard. Users can check/uncheck
    Architect, Implementor, Consultant, etc. to reorganize the leaderboard by role.
    All roles checked by default. Unchecking a role removes those advisors from the
    ranking and re-ranks the remaining.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_REBORN_PRD.md</ref>
    <ref type="design-qa">org/ref/design/PORTAL_DESIGN_QA.md</ref>
    <ref type="chart-colors">portal/src/lib/chartColors.ts</ref>
  </references>

  <scope>
    File: portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx

    1. Add role filter state: `useState<Set<AdvisorRole>>` initialized with all roles checked
    2. Add checkbox row in the PanelHeader or below it: one checkbox per role (Architect, Implementor, Consultant, etc.)
    3. Filter LeaderboardEntry[] by selected roles: `entry.roles.some(r => selectedRoles.has(r))`
    4. Re-rank filtered entries (recalculate rank based on current metric sort)
    5. Update Top3Highlights, LeaderboardNnaCards, LeaderboardAuaView, LeaderboardGrowthView to use filtered data
    6. Show active filter count: "Showing X of Y advisors" or similar indicator
    7. Remove the "Architects-only" comment at line 4 — leaderboard now shows all roles

    Design:
    - Checkboxes use 44px touch targets (mobile-ready per ADHC_DESIGN audit)
    - Labels: text-xs text-white/50 tracking-wider (canonical pattern)
    - Each role gets a color dot from chartColors.ts
    - All colors from @/lib/chartColors — no hardcoded hex
  </scope>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_REBORN.W4-002" status="complete">LeaderboardEntry must have roles field typed</dependency>
  </dependencies>

  <commit_pattern>feat(AdvisorsTab): role filter checkboxes on employee leaderboard</commit_pattern>
</task_order>
