<task_order>
  <metadata>
    <id>0.4.2_RD_AdvisorIntelligence-2026-03-17-leaderboard-windows</id>
    <issued_by>0.4.2_RD_AdvisorIntelligence</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-17</date>
    <status>pending</status>
  </metadata>

  <objective>
    Add MTD, QTD, and YTD window keys to the architect leaderboard gold script output.
    The Advisors tab now has a unified [MTD | QTD | YTD] period toggle that drives both
    the Top Performers panel and the Leaderboard panel. The frontend currently falls back
    to trailing windows (MTD->3M, QTD->3M, YTD->1Y) because the gold script only produces
    trailing calendar keys (3M, 6M, 1Y, 2Y, 3Y). This task adds true calendar-anchored
    windows so NNA and Growth figures match the toggle labels exactly.
  </objective>

  <scope>
    <files>
      <file action="modify">Gold script that produces architect_leaderboard.json</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts (ChartWindowOption union)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Add three new window keys to `LeaderboardResponse.windows`:
      - `MTD`: transactions from the 1st of the current month through data_as_of
      - `QTD`: transactions from the 1st of the current quarter through data_as_of
      - `YTD`: transactions from Jan 1 of the current year through data_as_of
      Each window contains the same `LeaderboardWindowData` shape: `entry_count`, `summary`, `entries[]`.
    </requirement>
    <requirement id="2">
      Within each window, `LeaderboardEntry` fields should reflect the window period:
      - `nna`: sum of NNA within the window date range
      - `aua_growth_pct`: AUA growth % from window start to data_as_of
      - `new_clients`: count of new clients onboarded within the window
      - `total_aua`: current point-in-time AUA (same across all windows -- this is a snapshot)
      - `client_count`, `account_count`: current point-in-time (same across all windows)
    </requirement>
    <requirement id="3">
      Add `MTD`, `QTD`, `YTD` to `available_windows[]` in the response.
    </requirement>
    <requirement id="4">
      Existing trailing windows (3M, 6M, 1Y, 2Y, 3Y) must continue to be produced -- do not remove them.
      Other consumers may depend on them.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      `architect_leaderboard.json` contains `windows.MTD`, `windows.QTD`, `windows.YTD`
      with correctly bounded NNA/growth/new_clients figures.
    </criterion>
    <criterion id="2">
      Selecting MTD on the frontend shows different NNA rankings than QTD or YTD
      (assuming transaction data spans more than one month).
    </criterion>
    <criterion id="3">
      `total_aua` is identical across all windows for the same architect.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>
      Do not change the shape of `LeaderboardEntry` -- only add new window keys.
      The frontend `LeaderboardRow` component renders all entries identically regardless of window.
    </constraint>
    <constraint>
      `aua_growth_pct` for MTD/QTD/YTD must use beginning-of-period AUA as the denominator.
      If beginning-of-period AUA is not available for an architect (new during the period),
      use null/0 -- do not fabricate a growth figure.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.2_RD_AdvisorIntelligence" task="advisors-tab-redesign" status="complete"/>
  </dependencies>

  <context>
    The frontend currently maps periods to windows in `AdvisorsTab.tsx`:
    ```
    function periodToChartWindow(p: PeriodKey): ChartWindowOption {
      if (p === 'mtd') return '3M'   // FALLBACK -- should be 'MTD'
      if (p === 'qtd') return '3M'   // FALLBACK -- should be 'QTD'
      return '1Y'                     // ytd -> should be 'YTD'
    }
    ```
    Once the gold script produces the new keys, DE or RD will update this mapping
    and add 'MTD' | 'QTD' | 'YTD' to the `ChartWindowOption` type union.

    The AUA metric view grays out the period toggle because `total_aua` is a snapshot.
    If DS wants to support period-specific AUA (e.g. "AUA as of quarter start"), that
    would be a separate enhancement -- not part of this task order.
  </context>

  <deliverables>
    <deliverable type="commit">Updated gold script producing MTD/QTD/YTD windows in architect_leaderboard.json</deliverable>
    <deliverable type="document">Brief confirming window date boundaries and any edge cases (new architects mid-period, missing historical AUA for growth calc)</deliverable>
  </deliverables>
</task_order>
