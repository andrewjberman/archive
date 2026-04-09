# ADVI_REBORN.W5-005 -- DE: Advisors Tab Data Path End-to-End Fix

<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-08-reborn-w5-005-de</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-08</date>
    <status>pending</status>
    <priority>critical</priority>
    <project_code>ADVI_REBORN</project_code>
  </metadata>

  <objective>The Advisors tab is not surfacing any data. Identify whether the issue is frontend mapping, API routing, or gold runner output connectivity -- and fix it. You own this end to end. Ambiguity and failure are not acceptable.</objective>

  <context>
  W5-002 fixed a case mismatch in periodToWindowKey() (lowercase vs uppercase window keys).
  RD confirmed employee_leaderboard.json exists on S3 (681KB, updated 2026-04-07).
  Despite these fixes, the Advisors tab still shows no data per Andrew.

  The case fix was necessary but not sufficient. The data path needs to be traced
  end to end: gold script output -> S3 artifact -> CloudFront/API routing ->
  frontend fetch -> component rendering. The break could be at any layer.

  Key files:
  - Gold: D_00.portal_aggregates.py build_employee_leaderboard() (line ~2680)
  - S3: gold/artifacts/employee_leaderboard.json (confirmed present, 681KB)
  - API: src/api/endpoints/advisor-intelligence.ts getEmployeeLeaderboard()
  - Frontend: src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx
  - Routing: shared-advisor-router (CloudFront -> API Gateway -> Lambda -> S3)

  RD 0.4.2 is available to assist on the frontend side. You lead the investigation
  and coordinate with RD. If the issue is frontend-only, direct RD to fix it.
  If the issue spans API/routing/data, you fix it and hand RD the frontend piece.
  </context>

  <deliverables>
  1. Trace the full data path: S3 artifact -> API endpoint -> frontend fetch -> render
  2. Identify the exact layer where data drops (network tab, API response, component state)
  3. Fix the issue or direct RD to fix the frontend component
  4. Verify the Advisors tab renders leaderboard data after the fix
  </deliverables>

  <dependencies>W5-002 RD case fix (complete). employee_leaderboard.json on S3 (confirmed).</dependencies>
</task_order>
