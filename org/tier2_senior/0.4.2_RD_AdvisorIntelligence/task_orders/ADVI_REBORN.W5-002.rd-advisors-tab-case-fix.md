# ADVI_REBORN.W5-002 -- RD: Fix Advisors Tab Window Key Case Mismatch

<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-08-reborn-w5-002-rd</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-08</date>
    <status>pending</status>
    <project_code>ADVI_REBORN</project_code>
  </metadata>

  <objective>Fix the Advisors tab showing no data. Root cause is a case mismatch between periodToWindowKey() and the employee_leaderboard.json keys.</objective>

  <context>
  AdvisorsTab.tsx lines 111-115: periodToWindowKey() returns lowercase 'qtd'/'ytd'.
  employee_leaderboard.json (produced by D_00.portal_aggregates.py line 88) uses
  uppercase keys: 'QTD', 'YTD', 'MTD', '3M', '6M', '1Y', '2Y', '3Y'.

  The lookup filteredArchitectData.windows['qtd'] returns undefined because the
  actual key is 'QTD'. This makes the entire leaderboard section empty.

  Note: periodToChartWindow() (lines 105-109) correctly returns uppercase, so the
  Top3Highlights section may already work. The leaderboard views at lines 406, 412, 417
  are the ones broken.
  </context>

  <deliverables>
  1. Fix periodToWindowKey() to return uppercase keys matching the JSON ('QTD', 'YTD')
  2. Verify the leaderboard views render correctly after the fix
  3. Commit to portal DEV
  </deliverables>

  <dependencies>
  Depends on employee_leaderboard.json existing on S3 (see W5-001 DS validation).
  If the artifact is missing, the tab will still be empty regardless of this fix.
  </dependencies>
</task_order>
