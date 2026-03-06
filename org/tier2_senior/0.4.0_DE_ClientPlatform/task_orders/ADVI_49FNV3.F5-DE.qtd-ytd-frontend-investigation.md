<task_order>
  <metadata>
    <id>ADVI_49FNV3.F5-DE.qtd-ytd-frontend-investigation</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-06</date>
    <status>complete</status>
  </metadata>

  <objective>
    Investigate the frontend side of F5: QTD and YTD show different values in March 2026 when they
    should be identical (Q1 2026 = Jan 1 - today = YTD). Determine if client-side period filtering
    in AdvisorsTab.tsx is computing QTD start date incorrectly. DS investigates the Lambda side
    in parallel.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Read `AdvisorsTab.tsx`. Find every location where QTD and YTD date ranges
      are computed client-side. Name the specific function or hook and line numbers.</requirement>
    <requirement id="2">Check: when computing QTD start date, does the code use the first day of the
      current quarter, or does it use some other reference? For March 2026, QTD start must equal
      Jan 1, 2026. Show the exact computation.</requirement>
    <requirement id="3">Compare: does YTD computation independently reach Jan 1 via a different code
      path? If both are correct independently but the portal is showing different numbers, the bug
      may be in the Lambda publisher (DS is checking that in parallel).</requirement>
    <requirement id="4">If the frontend period logic is wrong, fix it. Add a comment: Q1 start = Jan 1
      = YTD start; both period selectors must produce the same date range for months 1-3.</requirement>
    <requirement id="5">Report your finding to COO regardless of outcome. If the bug is Lambda-side,
      say so explicitly. If it's frontend-side, commit the fix and note the commit hash.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Root cause identified: specific file + function + line.</criterion>
    <criterion id="2">If frontend-side bug: fix committed to portal DEV with `--author` flag.</criterion>
    <criterion id="3">Finding reported to COO (in session log next steps).</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Coordinate with DS (F5-DS task order) — they are checking the Lambda period logic in
      parallel. Do not duplicate their investigation scope.</constraint>
    <constraint>Do not change Lambda or backend code — that is DS's scope.</constraint>
  </constraints>

  <dependencies/>

  <deliverables>
    <deliverable type="document">Written finding: frontend period logic assessment with specific code citation.</deliverable>
    <deliverable type="commit">Portal DEV fix if bug is frontend-side.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md</ref>
  </references>
</task_order>
