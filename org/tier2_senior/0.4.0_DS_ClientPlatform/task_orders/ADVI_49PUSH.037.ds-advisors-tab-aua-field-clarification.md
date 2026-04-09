<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-037-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-04-09</date>
    <status>complete -- 0.4.0_DS_ClientPlatform~C, commit 10df0f0f</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>9</wave>
    <phase>Advisors tab data correctness</phase>
    <mcp_identity>Register with MCP as "0.4.0_DS_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Confirm and if necessary fix that platinum/firm/leaderboard.json uses TOTAL MANAGED AUA
    (tagged AUA -- all accounts where the advisor appears in any role) as the primary AUA
    field for every leaderboard entry. This must NOT be fee-paying AUA, fee-weighted AUA,
    split-weighted AUA, or any C_08-derived variant. If tagged to it, it counts.
  </objective>

  <context>
    Andrew (2026-04-09): "This should be using TOTAL MANAGED AUA, not fee paying AUA,
    not the bizarre metric some DS came up with of some kind of weighted fee paying AUA
    or whatever that is. If they are tagged on it, it comes up in their AUA."

    The Advisors tab leaderboard reads platinum/firm/leaderboard.json →
    PlatinumLeaderboardEntry.total_aua. The portal renders total_aua as the advisor's
    AUA figure throughout the Advisors tab (rankings, Top 3 highlights, bar chart).

    In ADVI_49PUSH.006, D_02 was updated to build advisor books using SCD point-in-time
    multi-role tagging, producing tagged_aua = sum of AUA for all accounts where the
    advisor appears in any of the 5 roles on the latest date. D_04 then reads these
    book.json files to build the leaderboard.

    The question is: does D_04 write tagged_aua as total_aua in leaderboard entries,
    or is it pulling from an older field (managed_aua from C_08, fee_earning_aua, etc.)?
  </context>

  <fix_1 label="Verify and fix leaderboard total_aua source">
    <description>
      Step 1: In D_04's leaderboard builder, find where PlatinumLeaderboardEntry.total_aua
      is populated. Grep D_04.client_portal_summary.py for 'total_aua' in the leaderboard
      context. Check which source field it reads from:

        CORRECT:   book['summary']['tagged_aua']        -- all accounts, any role, current date
        INCORRECT: book['summary']['fee_earning_aua']   -- only accounts with positive splits
        INCORRECT: book['summary']['managed_aua']       -- C_08 split-weighted AUA
        INCORRECT: book['summary']['aua'] or similar C_08 field

      Step 2: If total_aua is already reading from tagged_aua -- no change needed.
      Confirm by spot-checking leaderboard.json for Travis Penfield:
        total_aua should equal ~$427M (tagged_aua from .006 session validation)
        NOT ~$149M (C_08 managed_aua) and NOT ~$343M (fee_earning_aua)

      Step 3: If total_aua is reading from any other source, fix D_04 to use tagged_aua.
      Update the field assignment in the leaderboard builder. No other changes needed.

      Step 4: Confirm the same total_aua field is what flows into:
        - leaderboard.json entries[].total_aua
        - leaderboard.json windows.QTD.summary.total_aua (the window-level summary)
        - leaderboard.json windows.YTD.summary.total_aua
      The window-level summary.total_aua should be FIRM headline AUA (same rule as
      ADV-AUA center total in .030) -- NOT a sum of advisor tagged AUAs.
      If the summary.total_aua is currently summing advisor AUAs, fix it to use
      the firm headline AUA from D_00 header_metrics.
    </description>
  </fix_1>

  <acceptance_criteria>
    1. leaderboard.json entries[].total_aua = tagged_aua for each advisor
    2. Travis Penfield spot-check: total_aua ~= $427M (within last run's margin)
    3. Window summary.total_aua = firm headline AUA, not sum of advisor tagged AUAs
    4. Session log: confirmed source field (tagged_aua) and spot-check values
    5. If a fix was required: D_04 committed on CLOUD
  </acceptance_criteria>


  <compiler_tools>
    comp-platinum reverse platinum/firm/leaderboard.json
      -- Traces leaderboard.json back through D_04 → D_00 → account_performance.
         Immediately shows which source field D_04 reads for total_aua. Confirms
         whether it's tagged_aua, managed_aua, or something else without reading
         150 lines of D_04.

    comp-pipescript io D_00
      -- Shows exactly which output field from D_00 feeds into employee_leaderboard.json.
         Tells you where managed_aua originates in the leaderboard builder.

    comp-blast gold/artifacts/employee_leaderboard.json
      -- Shows all downstream consumers of the leaderboard artifact.
         Run before any change to D_00's leaderboard output.
  </compiler_tools>

</task_order>
