# ADVI_REBORN.W5-003 -- DS: Books Tab Performance Investigation

<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-08-reborn-w5-003-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-08</date>
    <status>complete</status>
    <project_code>ADVI_REBORN</project_code>
  </metadata>

  <objective>Investigate and fix the Books tab (ClientsTab.tsx) slow load. Design a lighter initial payload strategy.</objective>

  <context>
  Books tab fires 4 parallel requests on mount (ClientsTab.tsx lines 303-328):
  1. getEmployeeLeaderboard() -- static S3 JSON (fast)
  2. getClientsTab() -- Lambda call returning FULL firm client dataset (heavy)
  3. getFirmMixViews() -- Lambda call
  4. getAdvisorFeeEfficiency() -- static S3 JSON (fast)

  getClientsTab() returns every client with headline, tax, income_fees, portfolio,
  engagement sections. This is the bottleneck.

  Additionally, the Advisor List panel (AdvisorSummaryTable, line 698) is empty
  when employee_leaderboard.json is missing from S3. Both this panel and the
  Advisors tab (W5-002) depend on the same artifact.

  Books tab is a 4-level drill hierarchy: Firm -> Advisor -> Relationship -> Account.
  Each drill level triggers multiple additional API calls.
  </context>

  <deliverables>
  1. Measure getClientsTab() payload size and response time
  2. Design pagination or lazy-loading for the clients-tab endpoint
     (e.g., return summary-only on initial load, fetch detail on drill)
  3. Verify employee_leaderboard.json exists on S3 (if not, coordinate with AE for gold re-run)
  4. Propose changes to D_00/Lambda endpoint to support lighter initial payload
  </deliverables>

  <dependencies>W5-001 (NNA validation may trigger gold re-run that also produces employee_leaderboard.json)</dependencies>
</task_order>
