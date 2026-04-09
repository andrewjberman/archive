# ADVI_NNAFEE.006 — DT: Phase 2 Deploy (Employee Leaderboard)

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-06-nnafee-006-dt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-06</date>
    <status>archived</status>
    <project_code>ADVI_NNAFEE</project_code>
    <priority>medium</priority>
    <phase>2</phase>
  </metadata>

  <objective>
    Push Phase 2 portal changes (employee leaderboard replacing architect
    leaderboard) to portal DEV. Verify the new leaderboard renders with live
    data from `employee_leaderboard.json` and that role filtering works correctly.
  </objective>

  <context>
    Phase 2 replaces the Architect Leaderboard in the Advisors tab with a unified
    Employee Leaderboard. DE (.004) wires the new endpoint and types. RD (.005)
    builds the new leaderboard with role checkboxes, time windows, and row expansion.

    No infrastructure changes needed -- the JSON is already served via the existing
    CloudFront wildcard behavior.

    The old `architect_leaderboard.json` continues to be produced by 11a (dual-write)
    so there is no data-side risk during the transition.
  </context>

  <scope>
    ## 1. Pre-Deploy Validation

    - `bunx tsc -b` clean
    - Verify `employee_leaderboard.json` is accessible at expected S3 path
    - Visual spot-check:
      - Window toggle switches data (3M vs YTD show different numbers)
      - Role checkboxes filter metrics (unchecking Implementor changes AUA/NNA values)
      - Row expansion shows all roles regardless of checkbox state
      - Scatter plot renders (if implemented)

    ## 2. Push to Portal DEV

    - Commit on portal `DEV` branch
    - Push to remote
    - Verify deployed portal loads Advisors tab with new leaderboard

    ## 3. Verification Checklist

    - [ ] All 8 time windows load (3M, 6M, 1Y, 2Y, 3Y, MTD, QTD, YTD)
    - [ ] Default: Architect + Implementor checked, table shows combined metrics
    - [ ] Uncheck Implementor: table values change (not row count), rank recomputes
    - [ ] "vs Expected" column shows "--" when roles are filtered
    - [ ] Row expansion shows all roles with unchecked roles muted
    - [ ] Search filters by name
    - [ ] Sort by NNA/AUA/Efficiency reorders correctly
    - [ ] Old architect leaderboard components removed (no dead code)

    ## 4. Cleanup

    After verifying the new leaderboard works:
    - Remove `getImplementorLeaderboard()` from endpoint file if unused
    - Remove old `LeaderboardResponse` type if no longer referenced
    - Keep `getArchitectLeaderboard()` for now (11a still dual-writes)
  </scope>

  <deliverables>
    <deliverable id="push">Portal DEV pushed with Phase 2 changes</deliverable>
    <deliverable id="verify">All verification checklist items pass</deliverable>
    <deliverable id="cleanup">Dead code from old leaderboard removed</deliverable>
  </deliverables>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_NNAFEE.004" status="staged"/>
    <dependency agent="0.4.2_RD_AdvisorIntelligence" task="ADVI_NNAFEE.005" status="staged"/>
  </dependencies>
</task_order>
