# Task Order: adv_drill + cla_timeseries Implementation — 0.4.0_DS_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-ADVI_V1VERS.004.ds-adv-drill-cla</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-03</date>
    <status>complete</status>
    <thread_serial>ADVI_V1VERS-004</thread_serial>
    <thread_ref>org/threads/ADVI-004-pattern-0-advdrill--clatimeseries-data-c/</thread_ref>
  </metadata>

  <objective>
    Implement adv_drill and cla_timeseries in the bd-portal-publisher Lambda per the
    binding contract agreed in ADVI-004, with CTO scope correction: cla.geo_city_drill
    IS in scope (cdim.primary_city exists in 04_build_client_dimension.py, publisher
    already loads cdim). Full cla structure includes total, geo_drill, adv_drill,
    and geo_city_drill.
  </objective>

  <references>
    <ref type="receipt">org/tier2_senior/0.4.0_DS_ClientPlatform/threads/ADVI-004-pattern-0-advdrill--clatimeseries-data-c_0.4.0_DE_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md</ref>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref type="source">data/black_diamond/scripts/gold/04_build_client_dimension.py</ref>
  </references>

  <requirements>

    <!-- ================================================================ -->
    <!-- STREAM A1 — adv_drill                                            -->
    <!-- ================================================================ -->
    <requirement id="A1.1">
      Add adv_drill to bd-portal-publisher/lambda_function.py output in
      timeseries_chart.json. Implement per the ADVI-004 receipt contract:
        - Per-architect -> per-client cumulative NNA time series
        - Structure mirrors existing geo_drill pattern
      Read the receipt for exact field names, nesting, and value types.
      No backend colorMap field — RD uses frontend hex palettes.
    </requirement>
    <requirement id="A1.2">
      Source data (already loaded in load_all()):
        - gold/client_performance.parquet (perf): date, relationship_id, total_aua, nna (cumulative)
        - gold/client_dimension.parquet (cdim): relationship_id, relationship_name, primary_architect
      No additional parquet files needed for adv_drill. These were confirmed in the
      ADVI-004 receipt (turn 7) as the grounding data sources.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM A2 — cla_timeseries (full scope including geo_city_drill) -->
    <!-- ================================================================ -->
    <requirement id="A2.0">
      FIRST ACTION: Read data/black_diamond/scripts/gold/04_build_client_dimension.py
      and confirm the primary_city field exists (lines 17, 267-268). The publisher
      Lambda already loads cdim. This confirms geo_city_drill is feasible as a
      Lambda-only change — no gold-layer enhancement needed.
    </requirement>
    <requirement id="A2.1">
      Add cla to timeseries_chart.json with the full structure:
        "cla": {
          "total": CumulativeChartView,
          "geo_drill": { "&lt;STATE&gt;": CumulativeChartView },
          "adv_drill": { "&lt;architect_display_name&gt;": CumulativeChartView },
          "geo_city_drill": { "&lt;STATE&gt;": { "&lt;city&gt;": CumulativeChartView } }
        }
      Each CumulativeChartView has two categories: NMNC and NMEC, with AUM values
      per date point. Use cdim.primary_city for the city dimension in geo_city_drill.
      No backend colorMap field — RD handles colors in frontend.
    </requirement>
    <requirement id="A2.2">
      NMNC/NMEC classification: apply the same cohort rule as the existing CLA logic
      in the publisher (months_since_first_seen &lt;= 12). Read the receipt and the
      publisher Lambda to confirm the exact classification implementation.
    </requirement>
    <requirement id="A2.3">
      Extend build_timeseries_chart() in bd-portal-publisher/lambda_function.py to
      produce all four cla sub-keys. The publisher already loads cdim — use it for
      the city dimension. This is a Lambda-only code change.
    </requirement>

    <!-- ================================================================ -->
    <!-- DATA CONTRACT UPDATE (quality gate)                               -->
    <!-- ================================================================ -->
    <requirement id="DC.1">
      Update data_contract.xml with both adv_drill and cla output shapes, S3 key,
      grain definitions, and NMNC/NMEC classification logic. Include the full cla
      schema with geo_city_drill (not blocked).
      Commit data_contract.xml update BEFORE signaling DT for Stream B1 deploy.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">adv_drill present in timeseries_chart.json with per-architect per-client cumulative NNA per receipt.</criterion>
    <criterion id="2">cla.total, cla.geo_drill, cla.adv_drill, cla.geo_city_drill all present in timeseries_chart.json with NMNC/NMEC series.</criterion>
    <criterion id="3">cla.geo_city_drill uses cdim.primary_city for city dimension.</criterion>
    <criterion id="4">NMNC/NMEC classification uses months_since_first_seen &lt;= 12 cohort rule.</criterion>
    <criterion id="5">data_contract.xml updated and committed before DT deploy.</criterion>
    <criterion id="6">No backend colorMap field emitted — colors are frontend-only.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Implement per the ADVI-004 receipt with CTO scope correction: geo_city_drill IS in scope.</constraint>
    <constraint>Read 04_build_client_dimension.py to confirm primary_city before starting A2.</constraint>
    <constraint>No backend colorMap field. RD uses existing CATEGORY_COLORS/GEO_COLORS hex palettes.</constraint>
    <constraint>data_contract.xml update is a non-negotiable gate before DT deploy (Stream B1).</constraint>
    <constraint>Do NOT deploy. Hand off to 0.4.0_DT via session log with commit hash.</constraint>
    <constraint>No emojis in any code or log output.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" -m "..."</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">bd-portal-publisher/lambda_function.py: adv_drill + full cla (total, geo_drill, adv_drill, geo_city_drill)</deliverable>
    <deliverable type="document">data_contract.xml updated with A1+A2 shapes including geo_city_drill</deliverable>
  </deliverables>
</task_order>
```
