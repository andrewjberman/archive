<task_order>
  <metadata>
    <id>ADVI_49FNV3.F5-DS.qtd-ytd-lambda-investigation</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-06</date>
    <status>complete</status>
  </metadata>

  <objective>
    Investigate the Lambda side of F5: QTD and YTD show different values in March 2026 when they
    should be identical (Q1 2026 = Jan 1 - today = YTD). Determine if the period boundary
    computation error is in the Lambda publisher (server-side) or frontend (client-side).
    This task covers the Lambda/backend side only. DE investigates the frontend side in parallel.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Read `bd-portal-advisor-publisher/lambda_function.py`. Find every location where
      QTD and YTD period boundaries are computed. Name the specific function and line numbers.</requirement>
    <requirement id="2">Check: does the Lambda compute Q1 start date as the floor-to-quarter of the
      current date, or does it hard-code a reference date? Is it using `pandas.tseries.offsets` or
      custom logic? Show the actual code path.</requirement>
    <requirement id="3">If the Lambda is computing QTD and YTD differently when they should be the same,
      fix the period boundary logic. Add an assertion or comment: when month is Jan/Feb/Mar, QTD start
      = Jan 1 = YTD start.</requirement>
    <requirement id="4">If the Lambda period computation is correct (QTD = YTD in Q1), report this
      finding to COO so the bug can be routed to DE (frontend side).</requirement>
    <requirement id="5">Audit all period boundary computations in the Lambda while you're there — the
      PRD flags this as potentially systemic. Note any other period boundaries that look incorrect.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Root cause identified and located: specific file + function + line number.</criterion>
    <criterion id="2">If Lambda-side: fix committed, DT brief written for deploy.</criterion>
    <criterion id="3">If frontend-side: written finding handed to COO to route to DE.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Coordinate with DE (F5-DE task order) — they are investigating the frontend period logic
      in parallel. Report findings to COO so both sides can be compared before a fix is deployed.</constraint>
    <constraint>Do not modify the portal frontend — that is DE's scope.</constraint>
  </constraints>

  <dependencies/>

  <deliverables>
    <deliverable type="document">Written finding: where the bug lives (Lambda or frontend) with specific code citation.</deliverable>
    <deliverable type="commit">Lambda fix if bug is Lambda-side. DT brief if deploy needed.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md</ref>
  </references>
</task_order>
