<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-042-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-04-09</date>
    <status>complete</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>10</wave>
    <phase>Advisors tab rank delta data</phase>
    <mcp_identity>Register with MCP as "0.4.0_DS_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Add period_start_aua to every leaderboard window entry so DE can compute each
    advisor's rank change since period start. The start AUA is already computed when
    deriving aua_growth_pct -- this is a one-field addition in two places.
  </objective>

  <context>
    DE .043 adds a RANK column to the leaderboard showing rank change (↑3 green / ↓10 red)
    since the selected period's start. To compute rank delta client-side, DE needs to
    sort all entries by period_start_aua to derive start ranks, then compare against
    current ranks (sort by total_aua). This requires period_start_aua per window entry.

    The value already exists at compute time:
      D_00 leaderboard builder: snap_start / start_vals (line ~535-539)
      D_02 implementor leaderboard builder: snap_start / start_snap (line ~572-575)
    In both cases, the start AUA is computed right before aua_growth_pct. It is just
    not being written to the output dict.
  </context>

  <fix_1 label="Add period_start_aua to D_00 leaderboard entries">
    <description>
      In D_00.portal_aggregates.py, find the per-window leaderboard entry construction
      (around line 535-610 where aua_growth_pct is computed and appended to the window).
      The start_vals dict (line ~539) contains the advisor's AUA at snap_start.

      In the entry dict, add:
        'period_start_aua': round(float(start_aua), 2)
      where start_aua = the total_aua value from start_vals for this advisor.

      If the advisor has no data at snap_start (new advisor, no history), set:
        'period_start_aua': None
      DE handles None by treating rank change as N/A (no icon shown).
    </description>
  </fix_1>

  <fix_2 label="Add period_start_aua to D_02 implementor leaderboard entries">
    <description>
      Same fix in D_02.advisor_client_detail.py build_implementor_leaderboard().
      Around line 575-606 where aua_growth_pct is computed from start_snap.
      Add 'period_start_aua' to each implementor window entry dict.
      Same None handling for advisors with no start data.
    </description>
  </fix_2>

  <fix_3 label="Include period_start_aua in D_04 leaderboard whitelist">
    <description>
      D_04.client_portal_summary.py build_leaderboard() trims the source leaderboard
      to a specific field whitelist (around line 1195):
        'aua_growth_pct', 'new_clients', 'client_count', 'account_count', ...

      Add 'period_start_aua' to this whitelist so the field passes through to
      platinum/firm/leaderboard.json.

      Also add to PlatinumLeaderboardEntry type in types.ts (DE .043 will do this,
      but DS should verify the field name is exactly 'period_start_aua' so DE can
      match it without ambiguity).
    </description>
  </fix_3>

  <acceptance_criteria>
    1. platinum/firm/leaderboard.json window entries have period_start_aua field
    2. Spot-check QTD window: Travis Penfield period_start_aua is a plausible value
       below his current $427.3M (should be his AUA at start of Q2 2026 = ~Jan 1 2026)
    3. Entries for newly active advisors have period_start_aua: null (not absent/0)
    4. Field present in both QTD and YTD windows
    5. Session log: note which advisors have null period_start_aua and why
  </acceptance_criteria>


  <compiler_tools>
    comp-pipescript io D_00
      -- Pinpoints the exact line in D_00 where the leaderboard window entries are built
         and aua_growth_pct is computed. The start_aua is computed right before it.
         Run this before searching the file -- D_00 is long and the leaderboard builder
         is buried.

    comp-pipescript consumers employee_leaderboard.json
      -- Shows what reads employee_leaderboard.json downstream (D_04 and others).
         Confirms D_04's whitelist trim is the only gate between D_00 output and platinum.
  </compiler_tools>

</task_order>
