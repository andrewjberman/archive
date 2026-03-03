# Task Order: adv_drill + cla_timeseries Implementation — 0.4.0_DS_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-ADVI-004-ds-adv_drill_cla</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
    <thread_serial>ADVI-004</thread_serial>
    <thread_ref>org/threads/ADVI-004-pattern-0-advdrill--clatimeseries-data-c/</thread_ref>
  </metadata>

  <objective>
    Implement adv_drill and cla_timeseries in the bd-portal-publisher Lambda per the
    binding contract agreed in ADVI-004. The thread receipt in your threads/ folder is
    the specification — implement exactly what was agreed, not the PRD's suggested shapes.
  </objective>

  <references>
    <ref type="receipt">org/tier2_senior/0.4.0_DS_ClientPlatform/threads/ADVI-004-pattern-0-advdrill--clatimeseries-data-c_0.4.0_DE_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md</ref>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
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
        - Include colorMap field per series with portal color tokens (not placeholders)
      Read the receipt for exact field names, nesting, and value types.
    </requirement>
    <requirement id="A1.2">
      Source data: nna_aua_by_advisor.parquet (architect grain) joined with
      client_performance.parquet (relationship grain) and rel_architect_lookup.parquet
      for architect-to-client mapping. These were confirmed in the ADVI-004 thread
      as the grounding data sources.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM A2 — cla_timeseries                                       -->
    <!-- ================================================================ -->
    <requirement id="A2.1">
      Add cla_timeseries to timeseries_chart.json. Implement per the ADVI-004 receipt:
        - cla.total: firm-wide NMNC vs NMEC AUM stacked area (two categories)
        - cla.geo: per-state NMNC/NMEC breakdown
        - cla.adv: per-architect NMNC/NMEC breakdown (architect is terminal grain for ADV-CLA)
      Include colorMap per series with actual portal tokens per receipt.
    </requirement>
    <requirement id="A2.2">
      NMNC/NMEC classification: implement per the definition agreed in the ADVI-004
      thread (first_seen_date in client_dimension.parquet). Read the receipt to confirm
      the exact classification rule and window. Do not assume a 12-month rule unless
      the receipt explicitly specifies it.
    </requirement>
    <requirement id="A2.3">
      BLOCKED — cla.geo_city_drill: do NOT implement city-level drill-down within
      cla_timeseries. The gold layer lacks relationship_id on the city parquet, making
      city-grain CLA classification impossible without a separate gold-layer enhancement.
      Flag this as a known blocker in data_contract.xml under the cla_timeseries section:
        "cla.geo_city_drill: BLOCKED -- city parquet missing relationship_id.
        Requires gold-layer enhancement task before implementation."
    </requirement>

    <!-- ================================================================ -->
    <!-- DATA CONTRACT UPDATE (quality gate)                               -->
    <!-- ================================================================ -->
    <requirement id="DC.1">
      Update data_contract.xml with both adv_drill and cla_timeseries output shapes,
      S3 key, grain definitions, colorMap spec, and NMNC/NMEC classification logic.
      Include the cla.geo_city_drill blocker note.
      Commit data_contract.xml update BEFORE signaling DT for Stream B1 deploy.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">adv_drill present in timeseries_chart.json with per-architect per-client cumulative NNA and colorMap per receipt.</criterion>
    <criterion id="2">cla.total, cla.geo, cla.adv present in timeseries_chart.json with NMNC/NMEC series per receipt.</criterion>
    <criterion id="3">cla.geo_city_drill NOT implemented; blocker documented in data_contract.xml.</criterion>
    <criterion id="4">data_contract.xml updated and committed before DT deploy.</criterion>
    <criterion id="5">All field names, nesting, and value types match the ADVI-004 receipt exactly.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Implement per the ADVI-004 receipt. Do not deviate from the agreed contract.</constraint>
    <constraint>Do NOT implement cla.geo_city_drill. Flag the blocker in data_contract.xml.</constraint>
    <constraint>data_contract.xml update is a non-negotiable gate before DT deploy (Stream B1).</constraint>
    <constraint>Do NOT deploy. Hand off to 0.4.0_DT via session log with commit hash.</constraint>
    <constraint>No emojis in any code or log output.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" -m "..."</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">bd-portal-publisher/lambda_function.py: adv_drill + cla_timeseries</deliverable>
    <deliverable type="document">data_contract.xml updated with A1+A2 shapes + geo_city_drill blocker</deliverable>
  </deliverables>
</task_order>
```
