<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-09-F5-fix</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-09</date>
    <status>complete</status>
  </metadata>

  <objective>
    Add calendar-aligned QTD and YTD windows to the leaderboard publisher output in
    bd-portal-advisor-publisher. The F5 QTD/YTD bug is now fully diagnosed by both
    0.4.0_DS_ClientPlatform (Lambda investigation, complete) and 0.4.0_DE_ClientPlatform
    (frontend investigation, complete). Root cause: the Lambda only emits rolling trailing
    windows (3M, 1Y). The frontend maps the "QTD" toggle to the "3M" key and the "YTD"
    toggle to the "1Y" key. In March 2026, trailing 90 days != calendar Q1 (Jan 1 - today),
    so QTD and YTD show different values when they should be identical.

    Fix: emit explicit calendar-aligned "qtd" and "ytd" keys in the leaderboard JSON so
    the frontend can consume them directly instead of approximating with trailing windows.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py</file>
    </files>
  </scope>

  <context>
    Prior investigation findings (from your own F5-DS task order, 2026-03-06):
    - build_advisor_books() in lambda_function.py (lines 398-407) correctly computes
      qtd_start and ytd_start as Jan 1, 2026 for any Q1 date.
    - The Lambda date logic is correct. The problem is that the leaderboard output
      (architect_leaderboard.json, implementor_leaderboard.json) only contains rolling
      trailing window keys (3M, 6M, 1Y, etc.), not calendar period keys.

    Prior DE finding (from F5-DE task order, 2026-03-06):
    - AdvisorsTab.tsx periodToChartWindow maps 'qtd' -> '3M' and 'ytd' -> '1Y'
    - The frontend CANNOT fix this alone because the Lambda does not emit a 'qtd' or
      'ytd' keyed dataset. The frontend must map to an existing key.
    - Once DS emits 'qtd' and 'ytd' keys, 0.4.0_DE_ClientPlatform will update
      periodToChartWindow to map 'qtd' -> 'qtd' and 'ytd' -> 'ytd' directly.
  </context>

  <requirements>
    <requirement id="1">Add a "qtd" key to architect_leaderboard.json and
      implementor_leaderboard.json. QTD computes from the first day of the current
      calendar quarter to the Lambda run date. For Q1 2026 (Jan-Mar): Jan 1 to today.
      For Q2 (Apr-Jun): Apr 1 to today. Etc.</requirement>
    <requirement id="2">Add a "ytd" key to both leaderboard JSONs. YTD computes from
      Jan 1 of the current year to the Lambda run date.</requirement>
    <requirement id="3">Both keys must contain the same data shape as the existing
      trailing window keys (3M, 6M, 1Y) — per-advisor NNA, AUA, ranking, and whatever
      other metrics exist in those window objects. Reuse the same aggregation logic,
      just with calendar-aligned date boundaries instead of trailing-day counts.</requirement>
    <requirement id="4">Verify: in Q1 (months 1-3), qtd and ytd must produce identical
      date ranges and therefore identical output. Add a code comment noting this
      expected equivalence.</requirement>
    <requirement id="5">The existing trailing window keys (3M, 6M, 1Y) must remain
      unchanged. This is additive — do not remove or rename existing keys.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">architect_leaderboard.json contains "qtd" and "ytd" keys with
      per-advisor metrics using calendar-aligned date boundaries.</criterion>
    <criterion id="2">implementor_leaderboard.json contains the same "qtd" and "ytd"
      keys.</criterion>
    <criterion id="3">In Q1 2026, qtd and ytd produce identical values.</criterion>
    <criterion id="4">Existing 3M/6M/1Y keys unchanged.</criterion>
    <criterion id="5">Code committed locally with --author flag. DT brief written
      for deploy (this will require a bd-portal-advisor-publisher Lambda redeploy).</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not modify the portal frontend — 0.4.0_DE_ClientPlatform will
      update periodToChartWindow after this Lambda change is deployed.</constraint>
    <constraint>Do not change the date logic for existing trailing window keys.</constraint>
    <constraint>The qtd_start and ytd_start computation already exists in
      build_advisor_books() (lines 398-407). Reuse that logic — do not reimplement
      quarter boundary math.</constraint>
  </constraints>

  <dependencies/>

  <deliverables>
    <deliverable type="commit">Lambda code change adding qtd/ytd keys to leaderboard
      publisher output. Committed locally with --author flag.</deliverable>
    <deliverable type="document">DT brief at docs/briefs/devops-brief-49fnv3-f5-qtd-publisher-fix.md
      for 0.4.0_DT_ClientPlatform to deploy.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md (F5 section)</ref>
    <ref type="prior-ds">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_49FNV3.F5-DS.qtd-ytd-lambda-investigation.md (investigation complete — Lambda date logic is correct, output keys are the gap)</ref>
    <ref type="prior-de">org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI_49FNV3.F5-DE.qtd-ytd-frontend-investigation.md (investigation complete — frontend maps qtd->3M, needs qtd key from Lambda)</ref>
    <ref type="source">infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py</ref>
  </references>
</task_order>
