# Task Order: Stacked Bar + Rolling 1Y Data Implementation — 0.4.0_DS_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-ADVI-005-ds-rolling_flows_data</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
    <thread_serial>ADVI-005</thread_serial>
    <thread_ref>org/threads/ADVI-005-pattern-0-stacked-bar--rolling-flows-dat/</thread_ref>
  </metadata>

  <objective>
    Update script 10 (10_generate_advisor_rolling_flows.py) to produce stacked_bar and
    rolling_1y output per the binding contract agreed in ADVI-005. The receipt in your
    threads/ folder is the specification.
  </objective>

  <references>
    <ref type="receipt">org/tier2_senior/0.4.0_DS_ClientPlatform/threads/ADVI-005-pattern-0-stacked-bar--rolling-flows-dat_0.4.0_DE_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md</ref>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
  </references>

  <requirements>

    <!-- ================================================================ -->
    <!-- STREAM A3 — stacked_bar + rolling_1y                             -->
    <!-- ================================================================ -->
    <requirement id="A3.1">
      Add stacked_bar to advisor_rolling_flows.json output per ADVI-005 receipt:
        - stacked_bar.architects.{qtd|ytd|1y|3y|max}: AdvisorBarEntry[]
        - stacked_bar.implementors.{qtd|ytd|1y|3y|max}: AdvisorBarEntry[]
        - AdvisorBarEntry = { advisor_name, advisor_id, inflows, outflows, nna_net }
        - Outflows: positive magnitude (>= 0) — frontend negates for chart rendering
        - nna_net: signed (can be negative)
        - Period boundaries: qtd/ytd calendar-anchored (existing _get_period_boundaries),
          1y/3y trailing windows (365/1095 days), max = inception-to-date
      Use existing _compute_nna_for_range() with new start dates for 1y/3y/max.
    </requirement>
    <requirement id="A3.2">
      Add rolling_1y to advisor_rolling_flows.json output per ADVI-005 receipt:
        - rolling_1y.architects: AdvisorRolling1YSeries[]
        - rolling_1y.implementors: AdvisorRolling1YSeries[]
        - AdvisorRolling1YSeries = { advisor_name, advisor_id, series: Rolling1YDataPoint[] }
        - Rolling1YDataPoint = { date, nna, inflows, outflows } — daily points, all 3 fields
        - Rolling window fixed at 1Y (365 days)
        - Emit full history (not sliced to a period — frontend slices by period toggle)
        - Outflows: positive magnitude (same convention as stacked_bar)
    </requirement>
    <requirement id="A3.3">
      Backward compatibility: keep existing top-level keys (generated_at, data_as_of,
      firm_id, summary, architects, implementors with legacy 30d/90d/1Y windows).
      stacked_bar and rolling_1y are additive optional keys.
    </requirement>
    <requirement id="A3.4">
      Data feasibility caveat from ADVI-005 receipt: for rolling_1y to have a full
      3Y x-axis of 1Y-rolling values, ~4Y of underlying daily history is needed.
      Emit whatever history exists. If less than 4Y available, note actual min date
      in your session log and in data_contract.xml.
    </requirement>

    <!-- ================================================================ -->
    <!-- DATA CONTRACT UPDATE (quality gate)                               -->
    <!-- ================================================================ -->
    <requirement id="DC.1">
      Update data_contract.xml with the new advisor_rolling_flows.json shape:
        - stacked_bar schema (period keys, AdvisorBarEntry fields, sign convention)
        - rolling_1y schema (series structure, daily cadence, all 3 fields)
        - Period boundary definitions (calendar-anchored vs trailing)
        - Data history coverage caveat
      Commit data_contract.xml update BEFORE signaling DT for Stream B2 deploy.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">stacked_bar present in advisor_rolling_flows.json with 5 periods x 2 role types, all AdvisorBarEntry fields per receipt.</criterion>
    <criterion id="2">rolling_1y present with daily points, all 3 fields (nna/inflows/outflows), for architects and implementors.</criterion>
    <criterion id="3">Outflows are positive magnitude everywhere.</criterion>
    <criterion id="4">Legacy keys (summary, architects, implementors with window series) preserved.</criterion>
    <criterion id="5">data_contract.xml updated before DT deploy.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Implement per ADVI-005 receipt. Do not deviate from agreed field names or sign conventions.</constraint>
    <constraint>data_contract.xml update gates DT deploy (Stream B2). Non-negotiable.</constraint>
    <constraint>Do NOT remove or modify existing legacy output keys. Additive only.</constraint>
    <constraint>Do NOT deploy. Hand off to 0.4.0_DT via session log with commit hash.</constraint>
    <constraint>No emojis in code or log output.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" -m "..."</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">10_generate_advisor_rolling_flows.py: stacked_bar + rolling_1y per ADVI-005 receipt</deliverable>
    <deliverable type="document">data_contract.xml updated with A3 shapes, sign convention, period definitions</deliverable>
  </deliverables>
</task_order>
```
