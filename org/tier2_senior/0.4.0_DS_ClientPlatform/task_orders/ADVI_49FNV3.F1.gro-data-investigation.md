<task_order>
  <metadata>
    <id>ADVI_49FNV3.F1.gro-data-investigation</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-06</date>
    <status>pending</status>
  </metadata>

  <objective>
    Investigate and fix F1: GRO mode (growth decomposition) shows "Growth decomposition data unavailable"
    in the Assets Overview panel. The frontend is fully wired. Either the Lambda publisher is not emitting
    `growth_decomposition`, or the gold layer data feeding it is empty. Root-cause and fix.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Read `bd-portal-publisher/lambda_function.py`. Search for `growth_decomposition`.
      If the field is not emitted, implement it: shape is
      `{ period: "YYYY-MM", market: float, nna: float, total: float }`
      where `market = aua_end - aua_start - nna`. Emit it as `timeseries_chart.growth_decomposition`.</requirement>
    <requirement id="2">If the field IS present in the Lambda but the output is empty or null, trace to
      the gold layer source. Check `client_performance.parquet` or equivalent. Name the specific column
      used for `aua_start`, `aua_end`, and `nna` per period. Determine if any months have null values.</requirement>
    <requirement id="3">Fix the root cause (Lambda logic or gold layer gap). Do NOT modify the portal
      frontend — it is already wired per the PRD.</requirement>
    <requirement id="4">Write a DT brief at `docs/briefs/devops-brief-49fnv3-f1-gro-publisher-fix.md`
      so DT can deploy the Lambda change.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">GRO mode renders a 3-line chart (market, nna, total) with real non-null data
      for at least the past 12 months.</criterion>
    <criterion id="2">Lambda change committed to CLOUD with `--author` flag. DT brief written.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not modify the portal frontend. The issue is data-side only.</constraint>
    <constraint>Every data field named must be cited to a specific file, function, or parquet column.
      Do not assert a field exists without verifying it in the code or schema.</constraint>
  </constraints>

  <dependencies/>

  <deliverables>
    <deliverable type="commit">Lambda fix committed. DT brief at docs/briefs/devops-brief-49fnv3-f1-gro-publisher-fix.md</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md</ref>
  </references>
</task_order>
